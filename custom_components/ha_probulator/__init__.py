"""HA Probulator integration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CARD_FILE,
    CARD_PATH,
    CONF_ADAPTIVE_POLLING,
    CONF_DEGRADED_SCAN_INTERVAL,
    CONF_DEPENDENCY_TARGET_ID,
    CONF_FLAP_THRESHOLD,
    CONF_FLAP_WINDOW,
    CONF_OFFLINE_SCAN_INTERVAL,
    CONF_PRESET,
    DATA_FRONTEND_REGISTERED,
    DATA_MANAGER,
    DATA_SERVICES_REGISTERED,
    DEFAULT_ADAPTIVE_POLLING,
    DEFAULT_DEGRADED_SCAN_INTERVAL,
    DEFAULT_DEPENDENCY_TARGET_ID,
    DEFAULT_FLAP_THRESHOLD,
    DEFAULT_FLAP_WINDOW,
    DEFAULT_OFFLINE_SCAN_INTERVAL,
    DEFAULT_PRESET,
    DOMAIN,
    VERSION,
)
from .coordinator import ProbulatorCoordinator
from .runtime import ProbulatorRuntimeManager
from .services import async_setup_services

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.BUTTON,
    Platform.SWITCH,
]


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up HA Probulator global runtime, actions, and dashboard assets."""
    domain_data = hass.data.setdefault(DOMAIN, {})

    if DATA_MANAGER not in domain_data:
        manager = ProbulatorRuntimeManager(hass)
        await manager.async_load()
        domain_data[DATA_MANAGER] = manager

    if not domain_data.get(DATA_SERVICES_REGISTERED):
        async_setup_services(hass)
        domain_data[DATA_SERVICES_REGISTERED] = True

    if not domain_data.get(DATA_FRONTEND_REGISTERED):
        card_file = Path(__file__).parent / "frontend" / CARD_FILE
        if card_file.is_file():
            await hass.http.async_register_static_paths(
                [StaticPathConfig(CARD_PATH, str(card_file), cache_headers=True)]
            )
            add_extra_js_url(hass, f"{CARD_PATH}?v={VERSION}")
        domain_data[DATA_FRONTEND_REGISTERED] = True

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a monitored target from a config entry."""
    manager: ProbulatorRuntimeManager = hass.data[DOMAIN][DATA_MANAGER]
    coordinator = ProbulatorCoordinator(hass, entry, manager)
    manager.register(coordinator)

    try:
        await coordinator.async_config_entry_first_refresh()
    except BaseException:
        manager.unregister(coordinator.target_id)
        raise

    hass.data[DOMAIN][entry.entry_id] = coordinator
    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a monitored target."""
    if not await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        return False

    coordinator: ProbulatorCoordinator | None = hass.data.get(DOMAIN, {}).pop(
        entry.entry_id,
        None,
    )
    if coordinator is not None:
        manager: ProbulatorRuntimeManager = hass.data[DOMAIN][DATA_MANAGER]
        manager.unregister(coordinator.target_id)
    return True


async def _async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload after config-entry data or options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate pre-1.2 target entries without changing established entity IDs."""
    if entry.version > 2:
        return False

    data = dict(entry.data)
    options = dict(entry.options)

    if entry.version < 2:
        data.setdefault(CONF_PRESET, DEFAULT_PRESET)

    options.setdefault(CONF_DEPENDENCY_TARGET_ID, DEFAULT_DEPENDENCY_TARGET_ID)
    options.setdefault(CONF_ADAPTIVE_POLLING, DEFAULT_ADAPTIVE_POLLING)
    options.setdefault(
        CONF_DEGRADED_SCAN_INTERVAL,
        DEFAULT_DEGRADED_SCAN_INTERVAL,
    )
    options.setdefault(CONF_OFFLINE_SCAN_INTERVAL, DEFAULT_OFFLINE_SCAN_INTERVAL)
    options.setdefault(CONF_FLAP_WINDOW, DEFAULT_FLAP_WINDOW)
    options.setdefault(CONF_FLAP_THRESHOLD, DEFAULT_FLAP_THRESHOLD)

    hass.config_entries.async_update_entry(
        entry,
        data=data,
        options=options,
        version=2,
        minor_version=1,
    )
    return True
