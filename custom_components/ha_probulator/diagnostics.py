"""Diagnostics for HA Probulator."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import ProbulatorCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a monitored target."""
    coordinator: ProbulatorCoordinator = hass.data[DOMAIN][entry.entry_id]
    data = dict(coordinator.data)
    for key in ("last_success", "last_failure"):
        if data.get(key) is not None:
            data[key] = data[key].isoformat()
    return {
        "entry": {
            "title": entry.title,
            "data": dict(entry.data),
            "options": dict(entry.options),
        },
        "state": data,
    }
