"""Rolling state and statistics for HA Probulator."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .probe import ProbeSample


@dataclass(slots=True)
class _ObservedSample:
    timestamp: datetime
    success: bool
    latency_ms: float | None


class ProbeMetrics:
    """Track debounced reachability and rolling probe statistics."""

    def __init__(
        self,
        *,
        window_size: int,
        failure_threshold: int,
        recovery_threshold: int,
        warning_latency_ms: float,
        critical_latency_ms: float,
    ) -> None:
        self._samples: deque[_ObservedSample] = deque(maxlen=window_size)
        self.failure_threshold = failure_threshold
        self.recovery_threshold = recovery_threshold
        self.warning_latency_ms = warning_latency_ms
        self.critical_latency_ms = critical_latency_ms

        self.reachable: bool | None = None
        self.consecutive_failures = 0
        self.consecutive_successes = 0
        self.total_probes = 0
        self.successful_probes = 0
        self.failed_probes = 0
        self.last_success: datetime | None = None
        self.last_failure: datetime | None = None
        self.last_error: str | None = None
        self.latest: ProbeSample | None = None

    @property
    def status(self) -> str:
        """Return the current human-readable target status."""
        if self.reachable is False:
            return "offline"
        if self.reachable is None:
            return "probing"
        if self.latest is not None and not self.latest.success:
            return "degraded"
        if self.quality in {"warning", "critical"}:
            return "degraded"
        return "online"

    @property
    def quality(self) -> str:
        """Return latency/reachability quality independent from status wording."""
        if self.reachable is False:
            return "offline"
        if self.reachable is None or self.latest is None:
            return "unknown"
        if not self.latest.success:
            return "warning"
        latency = self.latest.latency_ms
        if latency is None:
            return "unknown"
        if latency >= self.critical_latency_ms:
            return "critical"
        if latency >= self.warning_latency_ms:
            return "warning"
        return "good"

    def record(self, sample: ProbeSample) -> dict[str, Any]:
        """Record a sample and return the complete current snapshot."""
        self.latest = sample
        self.total_probes += 1
        self._samples.append(
            _ObservedSample(sample.timestamp, sample.success, sample.latency_ms)
        )

        if sample.success:
            self.successful_probes += 1
            self.consecutive_successes += 1
            self.consecutive_failures = 0
            self.last_success = sample.timestamp
            self.last_error = None
            if self.reachable is not True and (
                self.consecutive_successes >= self.recovery_threshold
            ):
                self.reachable = True
        else:
            self.failed_probes += 1
            self.consecutive_failures += 1
            self.consecutive_successes = 0
            self.last_failure = sample.timestamp
            self.last_error = sample.error
            if self.reachable is not False and (
                self.consecutive_failures >= self.failure_threshold
            ):
                self.reachable = False

        return self.snapshot()

    def snapshot(self) -> dict[str, Any]:
        """Return state and statistics derived from the current window."""
        successful = [
            sample.latency_ms
            for sample in self._samples
            if sample.success and sample.latency_ms is not None
        ]
        window_count = len(self._samples)
        window_successes = sum(1 for sample in self._samples if sample.success)

        average = round(sum(successful) / len(successful), 3) if successful else None
        minimum = round(min(successful), 3) if successful else None
        maximum = round(max(successful), 3) if successful else None
        success_rate = (
            round((window_successes / window_count) * 100.0, 3)
            if window_count
            else None
        )

        history = [
            {
                "timestamp": sample.timestamp.isoformat(),
                "latency_ms": sample.latency_ms,
                "success": sample.success,
            }
            for sample in list(self._samples)[-30:]
        ]

        return {
            "reachable": self.reachable,
            "status": self.status,
            "quality": self.quality,
            "response_time_ms": self.latest.latency_ms if self.latest else None,
            "average_response_time_ms": average,
            "min_response_time_ms": minimum,
            "max_response_time_ms": maximum,
            "success_rate": success_rate,
            "consecutive_failures": self.consecutive_failures,
            "consecutive_successes": self.consecutive_successes,
            "total_probes": self.total_probes,
            "successful_probes": self.successful_probes,
            "failed_probes": self.failed_probes,
            "last_success": self.last_success,
            "last_failure": self.last_failure,
            "last_error": self.last_error,
            "attempts": self.latest.attempts if self.latest else 0,
            "latency_history": history,
        }
