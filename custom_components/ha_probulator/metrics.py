"""Rolling state and statistics for HA Probulator."""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from itertools import pairwise
from typing import Any

from .const import (
    DEFAULT_FLAP_THRESHOLD,
    DEFAULT_FLAP_WINDOW,
    LATENCY_HISTORY_LIMIT,
)
from .probe import ProbeSample


@dataclass(slots=True)
class _ObservedSample:
    timestamp: datetime
    success: bool
    latency_ms: float | None


class ProbeMetrics:
    """Track debounced reachability, outages, and rolling probe statistics."""

    def __init__(
        self,
        *,
        window_size: int,
        failure_threshold: int,
        recovery_threshold: int,
        warning_latency_ms: float,
        critical_latency_ms: float,
        flap_window: int = DEFAULT_FLAP_WINDOW,
        flap_threshold: int = DEFAULT_FLAP_THRESHOLD,
    ) -> None:
        self._samples: deque[_ObservedSample] = deque(maxlen=window_size)
        self.failure_threshold = failure_threshold
        self.recovery_threshold = recovery_threshold
        self.warning_latency_ms = warning_latency_ms
        self.critical_latency_ms = critical_latency_ms
        self.flap_window = flap_window
        self.flap_threshold = flap_threshold

        self.reachable: bool | None = None
        self.consecutive_failures = 0
        self.consecutive_successes = 0
        self.total_probes = 0
        self.successful_probes = 0
        self.failed_probes = 0
        self.last_success: datetime | None = None
        self.last_failure: datetime | None = None
        self.last_check: datetime | None = None
        self.last_status_change: datetime | None = None
        self.outage_started: datetime | None = None
        self.last_outage_duration_seconds: float | None = None
        self._failure_streak_started: datetime | None = None
        self.last_error: str | None = None
        self.latest: ProbeSample | None = None

    @property
    def status(self) -> str:
        """Return the current human-readable target status."""
        if self.reachable is False:
            return "offline"
        if self.reachable is None:
            return "probing"
        if self.flapping:
            return "unstable"
        if self.latest is not None and not self.latest.success:
            return "degraded"
        if self.quality in {"warning", "critical"}:
            return "degraded"
        return "online"

    @property
    def flap_transitions(self) -> int:
        """Return success/failure transitions inside the configured flap window."""
        recent = list(self._samples)[-self.flap_window :]
        if len(recent) < 2:
            return 0
        return sum(
            previous.success != current.success
            for previous, current in pairwise(recent)
        )

    @property
    def flapping(self) -> bool:
        """Return whether the target is changing state unusually often."""
        return self.flap_transitions >= self.flap_threshold

    def restore_persistent(self, data: dict[str, Any]) -> None:
        """Restore low-churn lifetime metadata from persistent storage."""
        self.total_probes = int(data.get("total_probes") or 0)
        self.successful_probes = int(data.get("successful_probes") or 0)
        self.failed_probes = int(data.get("failed_probes") or 0)
        self.last_outage_duration_seconds = data.get("last_outage_duration_seconds")

        for key in ("last_success", "last_failure"):
            raw = data.get(key)
            if not raw:
                continue
            try:
                value = datetime.fromisoformat(str(raw))
            except ValueError:
                continue
            setattr(self, key, value)

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
        previous_status = self.status
        previous_reachable = self.reachable

        self.latest = sample
        self.last_check = sample.timestamp
        self.total_probes += 1
        self._samples.append(
            _ObservedSample(sample.timestamp, sample.success, sample.latency_ms)
        )

        if sample.success:
            self.successful_probes += 1
            self.consecutive_successes += 1
            self.consecutive_failures = 0
            self._failure_streak_started = None
            self.last_success = sample.timestamp
            self.last_error = None
            if self.reachable is not True and (
                self.consecutive_successes >= self.recovery_threshold
            ):
                self.reachable = True
        else:
            self.failed_probes += 1
            if self.consecutive_failures == 0:
                self._failure_streak_started = sample.timestamp
            self.consecutive_failures += 1
            self.consecutive_successes = 0
            self.last_failure = sample.timestamp
            self.last_error = sample.error
            if self.reachable is not False and (
                self.consecutive_failures >= self.failure_threshold
            ):
                self.reachable = False

        if previous_reachable is not False and self.reachable is False:
            self.outage_started = self._failure_streak_started or sample.timestamp
        elif previous_reachable is False and self.reachable is True:
            if self.outage_started is not None:
                self.last_outage_duration_seconds = round(
                    max(0.0, (sample.timestamp - self.outage_started).total_seconds()),
                    3,
                )
            self.outage_started = None

        current_status = self.status
        if self.last_status_change is None or current_status != previous_status:
            self.last_status_change = sample.timestamp

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
        p95 = None
        if successful:
            ordered = sorted(successful)
            rank = max(0, math.ceil(len(ordered) * 0.95) - 1)
            p95 = round(ordered[rank], 3)

        jitter = None
        if len(successful) >= 2:
            jitter = round(
                sum(
                    abs(current - previous)
                    for previous, current in pairwise(successful)
                )
                / (len(successful) - 1),
                3,
            )

        success_rate = (
            round((window_successes / window_count) * 100.0, 3)
            if window_count
            else None
        )
        current_outage = None
        if self.outage_started is not None and self.last_check is not None:
            current_outage = round(
                max(0.0, (self.last_check - self.outage_started).total_seconds()),
                3,
            )

        history = [
            {
                "timestamp": sample.timestamp.isoformat(),
                "latency_ms": sample.latency_ms,
                "success": sample.success,
            }
            for sample in list(self._samples)[-LATENCY_HISTORY_LIMIT:]
        ]

        return {
            "reachable": self.reachable,
            "status": self.status,
            "quality": self.quality,
            "flapping": self.flapping,
            "flap_transitions": self.flap_transitions,
            "flap_window": self.flap_window,
            "flap_threshold": self.flap_threshold,
            "response_time_ms": self.latest.latency_ms if self.latest else None,
            "average_response_time_ms": average,
            "min_response_time_ms": minimum,
            "max_response_time_ms": maximum,
            "p95_response_time_ms": p95,
            "jitter_ms": jitter,
            "success_rate": success_rate,
            "window_samples": window_count,
            "consecutive_failures": self.consecutive_failures,
            "consecutive_successes": self.consecutive_successes,
            "total_probes": self.total_probes,
            "successful_probes": self.successful_probes,
            "failed_probes": self.failed_probes,
            "last_success": self.last_success,
            "last_failure": self.last_failure,
            "last_check": self.last_check,
            "last_status_change": self.last_status_change,
            "outage_started": self.outage_started,
            "current_outage_duration_seconds": current_outage,
            "last_outage_duration_seconds": self.last_outage_duration_seconds,
            "last_error": self.last_error,
            "attempts": self.latest.attempts if self.latest else 0,
            "latency_history": history,
        }
