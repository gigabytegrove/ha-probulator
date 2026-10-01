"""Sensors for HA Probulator."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import ProbulatorCoordinator
from .entity import ProbulatorEntity


@dataclass(frozen=True, kw_only=True)
class ProbulatorSensorDescription(SensorEntityDescription):
    """Describe a Probulator sensor."""

    value_fn: Callable[[dict[str, Any]], Any]


SENSORS: tuple[ProbulatorSensorDescription, ...] = (
    ProbulatorSensorDescription(
        key="response_time_ms",
        translation_key="response_time",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("response_time_ms"),
    ),
    ProbulatorSensorDescription(
        key="average_response_time_ms",
        translation_key="average_response_time",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("average_response_time_ms"),
    ),
    ProbulatorSensorDescription(
        key="p95_response_time_ms",
        translation_key="p95_response_time",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("p95_response_time_ms"),
    ),
    ProbulatorSensorDescription(
        key="jitter_ms",
        translation_key="jitter",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("jitter_ms"),
    ),
    ProbulatorSensorDescription(
        key="min_response_time_ms",
        translation_key="minimum_response_time",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("min_response_time_ms"),
    ),
    ProbulatorSensorDescription(
        key="max_response_time_ms",
        translation_key="maximum_response_time",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("max_response_time_ms"),
    ),
    ProbulatorSensorDescription(
        key="success_rate",
        translation_key="success_rate",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("success_rate"),
    ),
    ProbulatorSensorDescription(
        key="consecutive_failures",
        translation_key="consecutive_failures",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("consecutive_failures"),
    ),
    ProbulatorSensorDescription(
        key="successful_probes",
        translation_key="successful_probes",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("successful_probes"),
    ),
    ProbulatorSensorDescription(
        key="failed_probes",
        translation_key="failed_probes",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("failed_probes"),
    ),
    ProbulatorSensorDescription(
        key="total_probes",
        translation_key="total_probes",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("total_probes"),
    ),
    ProbulatorSensorDescription(
        key="last_check",
        translation_key="last_check",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("last_check"),
    ),
    ProbulatorSensorDescription(
        key="last_status_change",
        translation_key="last_status_change",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("last_status_change"),
    ),
    ProbulatorSensorDescription(
        key="last_success",
        translation_key="last_success",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("last_success"),
    ),
    ProbulatorSensorDescription(
        key="last_failure",
        translation_key="last_failure",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("last_failure"),
    ),
    ProbulatorSensorDescription(
        key="current_outage_duration_seconds",
        translation_key="current_outage_duration",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("current_outage_duration_seconds"),
    ),
    ProbulatorSensorDescription(
        key="last_outage_duration_seconds",
        translation_key="last_outage_duration",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("last_outage_duration_seconds"),
    ),
    ProbulatorSensorDescription(
        key="probe_cycle_ms",
        translation_key="probe_cycle",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("probe_cycle_ms"),
    ),
    ProbulatorSensorDescription(
        key="probe_queue_wait_ms",
        translation_key="probe_queue_wait",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("probe_queue_wait_ms"),
    ),
    ProbulatorSensorDescription(
        key="flap_transitions",
        translation_key="flap_transitions",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("flap_transitions"),
    ),
    ProbulatorSensorDescription(
        key="current_scan_interval",
        translation_key="current_scan_interval",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("current_scan_interval"),
    ),
    ProbulatorSensorDescription(
        key="outage_count",
        translation_key="outage_count",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("outage_count"),
    ),
    ProbulatorSensorDescription(
        key="longest_outage_duration_seconds",
        translation_key="longest_outage_duration",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("longest_outage_duration_seconds"),
    ),
    ProbulatorSensorDescription(
        key="mean_outage_duration_seconds",
        translation_key="mean_outage_duration",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("mean_outage_duration_seconds"),
    ),
    ProbulatorSensorDescription(
        key="stable_since",
        translation_key="stable_since",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("stable_since"),
    ),
    ProbulatorSensorDescription(
        key="status",
        translation_key="status",
        icon="mdi:state-machine",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("status"),
    ),
    ProbulatorSensorDescription(
        key="quality",
        translation_key="quality",
        icon="mdi:signal",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("quality"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up target sensors."""
    coordinator: ProbulatorCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [ProbulatorSensor(coordinator, entry, description) for description in SENSORS]
    )


class ProbulatorSensor(ProbulatorEntity, SensorEntity):
    """One metric sensor."""

    entity_description: ProbulatorSensorDescription

    def __init__(
        self,
        coordinator: ProbulatorCoordinator,
        entry: ConfigEntry,
        description: ProbulatorSensorDescription,
    ) -> None:
        super().__init__(coordinator, entry, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> str | int | float | datetime | None:
        """Return the current metric value."""
        return self.entity_description.value_fn(self.coordinator.data)
