"""Shared entity helpers for HA Probulator."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_TARGET_ID, DOMAIN, VERSION
from .coordinator import ProbulatorCoordinator


class ProbulatorEntity(CoordinatorEntity[ProbulatorCoordinator]):
    """Base entity for one HA Probulator target."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ProbulatorCoordinator,
        entry: ConfigEntry,
        key: str,
    ) -> None:
        super().__init__(coordinator)
        self._entry = entry
        target_id = str(entry.data.get(CONF_TARGET_ID, entry.entry_id))
        self._attr_unique_id = f"{target_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, target_id)},
            name=entry.title,
            manufacturer="Gigabyte Grove",
            model="HA Probulator TCP Target",
            sw_version=VERSION,
        )
