"""Buttons for HA Probulator."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
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
    """Set up manual probe button."""
    coordinator: ProbulatorCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ProbulatorProbeNowButton(coordinator, entry)])


class ProbulatorProbeNowButton(ProbulatorEntity, ButtonEntity):
    """Request an immediate probe."""

    _attr_translation_key = "probe_now"
    _attr_icon = "mdi:radar"

    def __init__(self, coordinator: ProbulatorCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry, "probe_now")

    async def async_press(self) -> None:
        """Refresh the target immediately."""
        await self.coordinator.async_request_refresh()
