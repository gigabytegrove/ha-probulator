"""Tests for HA Probulator rolling state and statistics."""

import unittest
from datetime import UTC, datetime, timedelta

from _bootstrap import metrics, probe


class ProbeMetricsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)
        self.metrics = metrics.ProbeMetrics(
            window_size=3,
            failure_threshold=2,
            recovery_threshold=1,
            warning_latency_ms=100,
            critical_latency_ms=300,
        )

    def sample(self, offset: int, success: bool, latency: float | None = None):
        return probe.ProbeSample(
            timestamp=self.base + timedelta(seconds=offset),
            success=success,
            latency_ms=latency,
            attempts=1,
            error=None if success else probe.ProbeError.REFUSED,
        )

    def test_success_sets_online_and_statistics(self) -> None:
        state = self.metrics.record(self.sample(0, True, 12.5))
        self.assertTrue(state["reachable"])
        self.assertEqual(state["status"], "online")
        self.assertEqual(state["quality"], "good")
        self.assertEqual(state["average_response_time_ms"], 12.5)
        self.assertEqual(state["p95_response_time_ms"], 12.5)
        self.assertEqual(state["success_rate"], 100.0)
        self.assertEqual(state["last_check"], self.base)
        self.assertEqual(state["last_status_change"], self.base)

    def test_failure_is_debounced_before_offline(self) -> None:
        self.metrics.record(self.sample(0, True, 10))
        first = self.metrics.record(self.sample(1, False))
        self.assertTrue(first["reachable"])
        self.assertEqual(first["status"], "degraded")
        self.assertEqual(first["consecutive_failures"], 1)

        second = self.metrics.record(self.sample(2, False))
        self.assertFalse(second["reachable"])
        self.assertEqual(second["status"], "offline")
        self.assertEqual(second["consecutive_failures"], 2)
        self.assertEqual(second["outage_started"], self.base + timedelta(seconds=1))

    def test_success_recovers_after_offline_and_records_outage(self) -> None:
        self.metrics.record(self.sample(0, False))
        self.metrics.record(self.sample(1, False))
        recovered = self.metrics.record(self.sample(6, True, 20))
        self.assertTrue(recovered["reachable"])
        self.assertEqual(recovered["status"], "online")
        self.assertEqual(recovered["consecutive_failures"], 0)
        self.assertIsNone(recovered["outage_started"])
        self.assertEqual(recovered["last_outage_duration_seconds"], 6.0)
        self.assertEqual(recovered["outage_count"], 1)
        self.assertEqual(recovered["total_outage_duration_seconds"], 6.0)
        self.assertEqual(recovered["longest_outage_duration_seconds"], 6.0)
        self.assertEqual(recovered["mean_outage_duration_seconds"], 6.0)
        self.assertEqual(recovered["stable_since"], self.base + timedelta(seconds=6))

    def test_current_outage_duration_advances_on_checks(self) -> None:
        self.metrics.record(self.sample(0, False))
        offline = self.metrics.record(self.sample(1, False))
        self.assertEqual(offline["current_outage_duration_seconds"], 1.0)
        later = self.metrics.record(self.sample(11, False))
        self.assertEqual(later["current_outage_duration_seconds"], 11.0)

    def test_latency_thresholds_mark_degraded(self) -> None:
        warning = self.metrics.record(self.sample(0, True, 150))
        self.assertEqual(warning["quality"], "warning")
        self.assertEqual(warning["status"], "degraded")

        critical = self.metrics.record(self.sample(1, True, 350))
        self.assertEqual(critical["quality"], "critical")
        self.assertEqual(critical["status"], "degraded")

    def test_rolling_window_limits_statistics_and_p95(self) -> None:
        self.metrics.record(self.sample(0, True, 10))
        self.metrics.record(self.sample(1, True, 20))
        self.metrics.record(self.sample(2, False))
        state = self.metrics.record(self.sample(3, True, 40))
        self.assertEqual(state["average_response_time_ms"], 30.0)
        self.assertEqual(state["p95_response_time_ms"], 40)
        self.assertEqual(state["jitter_ms"], 20.0)
        self.assertAlmostEqual(state["success_rate"], 66.667, places=3)
        self.assertEqual(state["window_samples"], 3)
        self.assertEqual(len(state["latency_history"]), 3)

    def test_flapping_detects_repeated_success_failure_transitions(self) -> None:
        metrics_obj = metrics.ProbeMetrics(
            window_size=12,
            failure_threshold=2,
            recovery_threshold=1,
            warning_latency_ms=100,
            critical_latency_ms=300,
            flap_window=6,
            flap_threshold=3,
        )
        metrics_obj.record(self.sample(0, True, 10))
        metrics_obj.record(self.sample(1, False))
        metrics_obj.record(self.sample(2, True, 12))
        state = metrics_obj.record(self.sample(3, False))
        self.assertTrue(state["flapping"])
        self.assertEqual(state["flap_transitions"], 3)
        self.assertEqual(state["status"], "unstable")

    def test_persistent_lifetime_metrics_restore(self) -> None:
        restored = metrics.ProbeMetrics(
            window_size=10,
            failure_threshold=2,
            recovery_threshold=1,
            warning_latency_ms=100,
            critical_latency_ms=300,
        )
        restored.restore_persistent(
            {
                "total_probes": 100,
                "successful_probes": 97,
                "failed_probes": 3,
                "last_success": self.base.isoformat(),
                "last_failure": (self.base - timedelta(minutes=1)).isoformat(),
                "last_outage_duration_seconds": 42.5,
                "outage_count": 5,
                "total_outage_duration_seconds": 120.0,
                "longest_outage_duration_seconds": 50.0,
                "stable_since": self.base.isoformat(),
            }
        )
        state = restored.snapshot()
        self.assertEqual(state["total_probes"], 100)
        self.assertEqual(state["successful_probes"], 97)
        self.assertEqual(state["failed_probes"], 3)
        self.assertEqual(state["last_success"], self.base)
        self.assertEqual(state["last_outage_duration_seconds"], 42.5)
        self.assertEqual(state["outage_count"], 5)
        self.assertEqual(state["total_outage_duration_seconds"], 120.0)
        self.assertEqual(state["longest_outage_duration_seconds"], 50.0)
        self.assertEqual(state["mean_outage_duration_seconds"], 24.0)
        self.assertEqual(state["stable_since"], self.base)


if __name__ == "__main__":
    unittest.main()
