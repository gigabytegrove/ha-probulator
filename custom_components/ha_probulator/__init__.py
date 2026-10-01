"""HA Probulator integration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CARD_FILE, CARD_PATH, DOMAIN, VERSION
from .coordinator import ProbulatorCoordinator

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR, Platform.BUTTON]
DATA_FRONTEND_REGISTERED = "_frontend_registered"


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up HA Probulator and expose its optional dashboard cards."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    if domain_data.get(DATA_FRONTEND_REGISTERED):
        return True

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
    coordinator = ProbulatorCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a monitored target."""
    if not await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        return False
    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return True


async def _async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload after config-entry data or options change."""
    await hass.config_entries.async_reload(entry.entry_id)
