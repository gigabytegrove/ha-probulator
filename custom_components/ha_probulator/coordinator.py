"""Data coordinator for HA Probulator."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_ADAPTIVE_POLLING,
    CONF_CRITICAL_LATENCY,
    CONF_DEGRADED_SCAN_INTERVAL,
    CONF_DEPENDENCY_TARGET_ID,
    CONF_FAILURE_THRESHOLD,
    CONF_FLAP_THRESHOLD,
    CONF_FLAP_WINDOW,
    CONF_GROUP,
    CONF_ICON,
    CONF_OFFLINE_SCAN_INTERVAL,
    CONF_RECOVERY_THRESHOLD,
    CONF_RETRIES,
    CONF_RETRY_DELAY,
    CONF_SCAN_INTERVAL,
    CONF_STATISTICS_WINDOW,
    CONF_TARGET_ID,
    CONF_TIMEOUT,
    CONF_WARNING_LATENCY,
    DEFAULT_ADAPTIVE_POLLING,
    DEFAULT_CRITICAL_LATENCY,
    DEFAULT_DEGRADED_SCAN_INTERVAL,
    DEFAULT_DEPENDENCY_TARGET_ID,
    DEFAULT_FAILURE_THRESHOLD,
    DEFAULT_FLAP_THRESHOLD,
    DEFAULT_FLAP_WINDOW,
    DEFAULT_GROUP,
    DEFAULT_ICON,
    DEFAULT_OFFLINE_SCAN_INTERVAL,
    DEFAULT_RECOVERY_THRESHOLD,
    DEFAULT_RETRIES,
    DEFAULT_RETRY_DELAY,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_STATISTICS_WINDOW,
    DEFAULT_TIMEOUT,
    DEFAULT_WARNING_LATENCY,
    EVENT_STATUS_CHANGED,
    NAME,
)
from .metrics import ProbeMetrics
from .probe import async_tcp_probe
from .runtime import ProbulatorRuntimeManager
from .validation import format_target, safe_retries_for_budget

_LOGGER = logging.getLogger(__name__)

_BLOCKING_DEPENDENCY_STATUSES = {"offline", "dependency_offline", "disabled"}


class ProbulatorCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinate one monitored target."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        manager: ProbulatorRuntimeManager,
    ) -> None:
        self.entry = entry
        self.manager = manager
        self.target_id = str(entry.data.get(CONF_TARGET_ID, entry.entry_id))
        self.host = str(entry.data[CONF_HOST])
        self.port = int(entry.data[CONF_PORT])
        self.group = str(entry.options.get(CONF_GROUP, DEFAULT_GROUP)).strip()
        self.icon = (
            str(entry.options.get(CONF_ICON, DEFAULT_ICON)).strip() or DEFAULT_ICON
        )
        self.dependency_target_id = str(
            entry.options.get(
                CONF_DEPENDENCY_TARGET_ID,
                DEFAULT_DEPENDENCY_TARGET_ID,
            )
            or ""
        ).strip()
        self.timeout = float(entry.options.get(CONF_TIMEOUT, DEFAULT_TIMEOUT))
        configured_retries = int(entry.options.get(CONF_RETRIES, DEFAULT_RETRIES))
        self.retry_delay = float(
            entry.options.get(CONF_RETRY_DELAY, DEFAULT_RETRY_DELAY)
        )
        self.retries = safe_retries_for_budget(
            timeout=self.timeout,
            retries=configured_retries,
            retry_delay=self.retry_delay,
        )
        if self.retries != configured_retries:
            _LOGGER.warning(
                "Reduced HA Probulator retry count from %s to %s because the stored "
                "configuration exceeds the 60-second probe-cycle safety budget",
                configured_retries,
                self.retries,
            )

        self.base_scan_interval = int(
            entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )
        self.adaptive_polling = bool(
            entry.options.get(CONF_ADAPTIVE_POLLING, DEFAULT_ADAPTIVE_POLLING)
        )
        self.degraded_scan_interval = int(
            entry.options.get(
                CONF_DEGRADED_SCAN_INTERVAL,
                DEFAULT_DEGRADED_SCAN_INTERVAL,
            )
        )
        self.offline_scan_interval = int(
            entry.options.get(
                CONF_OFFLINE_SCAN_INTERVAL,
                DEFAULT_OFFLINE_SCAN_INTERVAL,
            )
        )
        self._has_update = False
        self._last_effective_status = "probing"

        self.metrics = ProbeMetrics(
            window_size=int(
                entry.options.get(CONF_STATISTICS_WINDOW, DEFAULT_STATISTICS_WINDOW)
            ),
            failure_threshold=int(
                entry.options.get(CONF_FAILURE_THRESHOLD, DEFAULT_FAILURE_THRESHOLD)
            ),
            recovery_threshold=int(
                entry.options.get(CONF_RECOVERY_THRESHOLD, DEFAULT_RECOVERY_THRESHOLD)
            ),
            warning_latency_ms=float(
                entry.options.get(CONF_WARNING_LATENCY, DEFAULT_WARNING_LATENCY)
            ),
            critical_latency_ms=float(
                entry.options.get(CONF_CRITICAL_LATENCY, DEFAULT_CRITICAL_LATENCY)
            ),
            flap_window=int(entry.options.get(CONF_FLAP_WINDOW, DEFAULT_FLAP_WINDOW)),
            flap_threshold=int(
                entry.options.get(CONF_FLAP_THRESHOLD, DEFAULT_FLAP_THRESHOLD)
            ),
        )
        self.metrics.restore_persistent(manager.restore_metrics(self.target_id))

        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"{NAME}: {entry.title}",
            update_interval=timedelta(seconds=self.base_scan_interval),
        )

    def _adaptive_interval(self, underlying_status: str) -> int:
        """Choose a polling interval based on current target health."""
        if not self.adaptive_polling:
            return self.base_scan_interval
        if underlying_status in {"degraded", "unstable", "probing"}:
            return min(self.base_scan_interval, self.degraded_scan_interval)
        if underlying_status == "offline":
            return min(self.base_scan_interval, self.offline_scan_interval)
        return self.base_scan_interval

    def _effective_status(
        self,
        *,
        monitoring_enabled: bool,
        maintenance: bool,
        underlying_status: str,
        dependency_status: str | None,
    ) -> str:
        """Return the user-facing status after runtime policy is applied."""
        if not monitoring_enabled:
            return "disabled"
        if maintenance:
            return "maintenance"
        if dependency_status in _BLOCKING_DEPENDENCY_STATUSES:
            return "dependency_offline"
        return underlying_status

    def _metadata(
        self,
        snapshot: dict[str, Any],
        *,
        monitoring_enabled: bool,
        maintenance: bool,
        dependency_status: str | None,
    ) -> dict[str, Any]:
        """Attach configuration and runtime metadata to a metrics snapshot."""
        underlying_status = str(snapshot["status"])
        effective_status = self._effective_status(
            monitoring_enabled=monitoring_enabled,
            maintenance=maintenance,
            underlying_status=underlying_status,
            dependency_status=dependency_status,
        )
        maintenance_until = self.manager.maintenance_until(self.target_id)
        current_interval = self._adaptive_interval(underlying_status)
        self.update_interval = timedelta(seconds=current_interval)

        snapshot.update(
            {
                "target_id": self.target_id,
                "name": self.entry.title,
                "host": self.host,
                "port": self.port,
                "target": format_target(self.host, self.port),
                "group": self.group,
                "icon": self.icon,
                "monitoring_enabled": monitoring_enabled,
                "maintenance": maintenance,
                "maintenance_until": maintenance_until,
                "dependency_target_id": self.dependency_target_id or None,
                "dependency_name": self.manager.dependency_name(
                    self.dependency_target_id
                ),
                "dependency_status": dependency_status,
                "underlying_status": underlying_status,
                "status": effective_status,
                "scan_interval": self.base_scan_interval,
                "current_scan_interval": current_interval,
                "adaptive_polling": self.adaptive_polling,
                "degraded_scan_interval": self.degraded_scan_interval,
                "offline_scan_interval": self.offline_scan_interval,
                "timeout": self.timeout,
                "retries": self.retries,
                "retry_delay": self.retry_delay,
                "failure_threshold": self.metrics.failure_threshold,
                "recovery_threshold": self.metrics.recovery_threshold,
                "warning_latency_ms": self.metrics.warning_latency_ms,
                "critical_latency_ms": self.metrics.critical_latency_ms,
            }
        )
        return snapshot

    async def _async_update_data(self) -> dict[str, Any]:
        monitoring_enabled = self.manager.monitoring_enabled(self.target_id)
        maintenance = self.manager.in_maintenance(self.target_id)

        if monitoring_enabled:
            async with self.manager.probe_semaphore:
                sample = await async_tcp_probe(
                    self.host,
                    self.port,
                    timeout=self.timeout,
                    retries=self.retries,
                    retry_delay=self.retry_delay,
                )
            snapshot = self.metrics.record(sample)
            self.manager.persist_metrics(self.target_id, snapshot)
        else:
            sample = None
            snapshot = self.metrics.snapshot()

        dependency_status = self.manager.dependency_status(
            self.dependency_target_id or None
        )
        snapshot = self._metadata(
            snapshot,
            monitoring_enabled=monitoring_enabled,
            maintenance=maintenance,
            dependency_status=dependency_status,
        )

        current_status = str(snapshot["status"])
        previous_status = self._last_effective_status
        status_changed = self._has_update and current_status != previous_status

        if status_changed and current_status != "maintenance":
            checked_at = (
                sample.timestamp.isoformat()
                if sample is not None
                else snapshot.get("last_check")
            )
            if hasattr(checked_at, "isoformat"):
                checked_at = checked_at.isoformat()
            self.hass.bus.async_fire(
                EVENT_STATUS_CHANGED,
                {
                    "target_id": self.target_id,
                    "entry_id": self.entry.entry_id,
                    "name": self.entry.title,
                    "host": self.host,
                    "port": self.port,
                    "target": snapshot["target"],
                    "group": self.group,
                    "previous_status": previous_status,
                    "status": current_status,
                    "underlying_status": snapshot["underlying_status"],
                    "dependency_target_id": snapshot["dependency_target_id"],
                    "dependency_status": snapshot["dependency_status"],
                    "maintenance": maintenance,
                    "quality": snapshot["quality"],
                    "flapping": snapshot["flapping"],
                    "flap_transitions": snapshot["flap_transitions"],
                    "response_time_ms": snapshot["response_time_ms"],
                    "p95_response_time_ms": snapshot["p95_response_time_ms"],
                    "jitter_ms": snapshot["jitter_ms"],
                    "success_rate": snapshot["success_rate"],
                    "consecutive_failures": snapshot["consecutive_failures"],
                    "last_error": snapshot["last_error"],
                    "checked_at": checked_at,
                },
            )

        self._last_effective_status = current_status
        self._has_update = True

        if status_changed:
            self.manager.notify_dependents(self.target_id)

        return snapshot
