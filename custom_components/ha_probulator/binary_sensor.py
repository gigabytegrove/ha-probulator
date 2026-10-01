"""Binary sensors for HA Probulator."""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import ProbulatorCoordinator
from .entity import ProbulatorEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up reachability for one target."""
    coordinator: ProbulatorCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ProbulatorReachableSensor(coordinator, entry)])


class ProbulatorReachableSensor(ProbulatorEntity, BinarySensorEntity):
    """Primary reachability entity and card data source."""

    _attr_translation_key = "reachable"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, coordinator: ProbulatorCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry, "reachable")

    @property
    def icon(self) -> str:
        """Return the configured target icon."""
        return self.coordinator.icon

    @property
    def is_on(self) -> bool | None:
        """Return debounced reachability."""
        return self.coordinator.data.get("reachable")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose card/automation-friendly variables."""
        data = self.coordinator.data

        def iso(key: str) -> str | None:
            value = data.get(key)
            return value.isoformat() if value is not None else None

        return {
            "probulator": True,
            "probulator_kind": "target",
            "target_id": data.get("target_id"),
            "target_name": self._entry.title,
            "target": data.get("target"),
            "host": data.get("host"),
            "port": data.get("port"),
            "group": data.get("group"),
            "status": data.get("status"),
            "quality": data.get("quality"),
            "response_time_ms": data.get("response_time_ms"),
            "average_response_time_ms": data.get("average_response_time_ms"),
            "p95_response_time_ms": data.get("p95_response_time_ms"),
            "min_response_time_ms": data.get("min_response_time_ms"),
            "max_response_time_ms": data.get("max_response_time_ms"),
            "success_rate": data.get("success_rate"),
            "window_samples": data.get("window_samples"),
            "consecutive_failures": data.get("consecutive_failures"),
            "consecutive_successes": data.get("consecutive_successes"),
            "total_probes": data.get("total_probes"),
            "successful_probes": data.get("successful_probes"),
            "failed_probes": data.get("failed_probes"),
            "last_check": iso("last_check"),
            "last_status_change": iso("last_status_change"),
            "last_success": iso("last_success"),
            "last_failure": iso("last_failure"),
            "outage_started": iso("outage_started"),
            "current_outage_duration_seconds": data.get(
                "current_outage_duration_seconds"
            ),
            "last_outage_duration_seconds": data.get("last_outage_duration_seconds"),
            "last_error": data.get("last_error"),
            "attempts": data.get("attempts"),
            "scan_interval": data.get("scan_interval"),
            "timeout": data.get("timeout"),
            "retries": data.get("retries"),
            "retry_delay": data.get("retry_delay"),
            "failure_threshold": data.get("failure_threshold"),
            "recovery_threshold": data.get("recovery_threshold"),
            "warning_latency_ms": data.get("warning_latency_ms"),
            "critical_latency_ms": data.get("critical_latency_ms"),
            "latency_history": data.get("latency_history", []),
        }
