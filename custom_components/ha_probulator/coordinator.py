"""Data coordinator for HA Probulator."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_CRITICAL_LATENCY,
    CONF_FAILURE_THRESHOLD,
    CONF_GROUP,
    CONF_ICON,
    CONF_RECOVERY_THRESHOLD,
    CONF_RETRIES,
    CONF_RETRY_DELAY,
    CONF_SCAN_INTERVAL,
    CONF_STATISTICS_WINDOW,
    CONF_TARGET_ID,
    CONF_TIMEOUT,
    CONF_WARNING_LATENCY,
    DEFAULT_CRITICAL_LATENCY,
    DEFAULT_FAILURE_THRESHOLD,
    DEFAULT_GROUP,
    DEFAULT_ICON,
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
from .validation import format_target

_LOGGER = logging.getLogger(__name__)


class ProbulatorCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinate one monitored target."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        self.target_id = str(entry.data.get(CONF_TARGET_ID, entry.entry_id))
        self.host = str(entry.data[CONF_HOST])
        self.port = int(entry.data[CONF_PORT])
        self.group = str(entry.options.get(CONF_GROUP, DEFAULT_GROUP)).strip()
        self.icon = str(entry.options.get(CONF_ICON, DEFAULT_ICON)).strip() or DEFAULT_ICON
        self.timeout = float(entry.options.get(CONF_TIMEOUT, DEFAULT_TIMEOUT))
        self.retries = int(entry.options.get(CONF_RETRIES, DEFAULT_RETRIES))
        self.retry_delay = float(
            entry.options.get(CONF_RETRY_DELAY, DEFAULT_RETRY_DELAY)
        )
        self._has_sample = False

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
        )

        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"{NAME}: {entry.title}",
            update_interval=timedelta(
                seconds=int(entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
            ),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        previous_status = self.metrics.status
        sample = await async_tcp_probe(
            self.host,
            self.port,
            timeout=self.timeout,
            retries=self.retries,
            retry_delay=self.retry_delay,
        )
        snapshot = self.metrics.record(sample)
        snapshot.update(
            {
                "target_id": self.target_id,
                "name": self.entry.title,
                "host": self.host,
                "port": self.port,
                "target": format_target(self.host, self.port),
                "group": self.group,
                "icon": self.icon,
                "scan_interval": int(
                    self.entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
                ),
                "timeout": self.timeout,
                "retries": self.retries,
                "retry_delay": self.retry_delay,
                "failure_threshold": self.metrics.failure_threshold,
                "recovery_threshold": self.metrics.recovery_threshold,
                "warning_latency_ms": self.metrics.warning_latency_ms,
                "critical_latency_ms": self.metrics.critical_latency_ms,
            }
        )

        current_status = snapshot["status"]
        if self._has_sample and current_status != previous_status:
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
                    "quality": snapshot["quality"],
                    "response_time_ms": snapshot["response_time_ms"],
                    "p95_response_time_ms": snapshot["p95_response_time_ms"],
                    "success_rate": snapshot["success_rate"],
                    "consecutive_failures": snapshot["consecutive_failures"],
                    "last_error": snapshot["last_error"],
                    "checked_at": sample.timestamp.isoformat(),
                },
            )
        self._has_sample = True
        return snapshot
