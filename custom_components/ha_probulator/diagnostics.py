"""Diagnostics for HA Probulator."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant

from .const import DATA_MANAGER, DOMAIN
from .coordinator import ProbulatorCoordinator
from .runtime import ProbulatorRuntimeManager

TO_REDACT = {CONF_HOST, "target"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return privacy-aware diagnostics for a monitored target."""
    coordinator: ProbulatorCoordinator = hass.data[DOMAIN][entry.entry_id]
    data = dict(coordinator.data)
    manager: ProbulatorRuntimeManager = hass.data[DOMAIN][DATA_MANAGER]
    runtime = dict(manager._state(coordinator.target_id))

    for key, value in list(data.items()):
        if isinstance(value, datetime):
            data[key] = value.isoformat()

    return {
        "entry": {
            "title": entry.title,
            "data": async_redact_data(dict(entry.data), TO_REDACT),
            "options": dict(entry.options),
        },
        "state": async_redact_data(data, TO_REDACT),
        "runtime": async_redact_data(runtime, TO_REDACT),
    }
