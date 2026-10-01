"""Runtime control switches for HA Probulator."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DATA_MANAGER, DOMAIN
from .coordinator import ProbulatorCoordinator
from .entity import ProbulatorEntity
from .runtime import ProbulatorRuntimeManager


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up runtime control switches."""
    coordinator: ProbulatorCoordinator = hass.data[DOMAIN][entry.entry_id]
    manager: ProbulatorRuntimeManager = hass.data[DOMAIN][DATA_MANAGER]
    async_add_entities(
        [
            ProbulatorMonitoringSwitch(coordinator, entry, manager),
            ProbulatorMaintenanceSwitch(coordinator, entry, manager),
        ]
    )


class ProbulatorMonitoringSwitch(ProbulatorEntity, SwitchEntity):
    """Enable or disable active probing without deleting the target."""

    _attr_translation_key = "monitoring"
    _attr_icon = "mdi:radar"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: ProbulatorCoordinator,
        entry: ConfigEntry,
        manager: ProbulatorRuntimeManager,
    ) -> None:
        super().__init__(coordinator, entry, "monitoring")
        self._manager = manager

    @property
    def is_on(self) -> bool:
        """Return whether active probing is enabled."""
        return self._manager.monitoring_enabled(self.coordinator.target_id)

    async def async_turn_on(self, **kwargs) -> None:
        """Enable active probing."""
        await self._manager.async_set_monitoring(self.coordinator.target_id, True)

    async def async_turn_off(self, **kwargs) -> None:
        """Disable active probing."""
        await self._manager.async_set_monitoring(self.coordinator.target_id, False)


class ProbulatorMaintenanceSwitch(ProbulatorEntity, SwitchEntity):
    """Suppress operational status changes while continuing to collect probes."""

    _attr_translation_key = "maintenance"
    _attr_icon = "mdi:wrench-clock"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: ProbulatorCoordinator,
        entry: ConfigEntry,
        manager: ProbulatorRuntimeManager,
    ) -> None:
        super().__init__(coordinator, entry, "maintenance")
        self._manager = manager

    @property
    def is_on(self) -> bool:
        """Return maintenance state."""
        return self._manager.in_maintenance(self.coordinator.target_id)

    async def async_turn_on(self, **kwargs) -> None:
        """Start indefinite maintenance mode."""
        await self._manager.async_set_maintenance(self.coordinator.target_id, True)

    async def async_turn_off(self, **kwargs) -> None:
        """End maintenance mode."""
        await self._manager.async_set_maintenance(self.coordinator.target_id, False)
