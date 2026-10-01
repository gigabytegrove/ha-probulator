"""Tests for HA Probulator rolling state and statistics."""

from datetime import datetime, timedelta, timezone
import unittest

from _bootstrap import metrics, probe


class ProbeMetricsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = datetime(2026, 10, 1, 12, 0, tzinfo=timezone.utc)
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
            error=None if success else "ConnectionRefusedError",
        )

    def test_success_sets_online_and_statistics(self) -> None:
        state = self.metrics.record(self.sample(0, True, 12.5))
        self.assertTrue(state["reachable"])
        self.assertEqual(state["status"], "online")
        self.assertEqual(state["quality"], "good")
        self.assertEqual(state["average_response_time_ms"], 12.5)
        self.assertEqual(state["success_rate"], 100.0)

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

    def test_success_recovers_after_offline(self) -> None:
        self.metrics.record(self.sample(0, False))
        self.metrics.record(self.sample(1, False))
        recovered = self.metrics.record(self.sample(2, True, 20))
        self.assertTrue(recovered["reachable"])
        self.assertEqual(recovered["status"], "online")
        self.assertEqual(recovered["consecutive_failures"], 0)

    def test_latency_thresholds_mark_degraded(self) -> None:
        warning = self.metrics.record(self.sample(0, True, 150))
        self.assertEqual(warning["quality"], "warning")
        self.assertEqual(warning["status"], "degraded")

        critical = self.metrics.record(self.sample(1, True, 350))
        self.assertEqual(critical["quality"], "critical")
        self.assertEqual(critical["status"], "degraded")

    def test_rolling_window_limits_statistics(self) -> None:
        self.metrics.record(self.sample(0, True, 10))
        self.metrics.record(self.sample(1, True, 20))
        self.metrics.record(self.sample(2, False))
        state = self.metrics.record(self.sample(3, True, 40))
        self.assertEqual(state["average_response_time_ms"], 30.0)
        self.assertAlmostEqual(state["success_rate"], 66.667, places=3)
        self.assertEqual(len(state["latency_history"]), 3)


if __name__ == "__main__":
    unittest.main()
