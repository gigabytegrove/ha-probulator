"""Home Assistant actions for HA Probulator."""

from __future__ import annotations

import asyncio
from functools import partial

import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.service import async_register_admin_service

from .const import (
    DATA_MANAGER,
    DOMAIN,
    SERVICE_END_MAINTENANCE,
    SERVICE_PROBE,
    SERVICE_SET_MONITORING,
    SERVICE_START_MAINTENANCE,
)
from .runtime import ProbulatorRuntimeManager

ATTR_TARGET_ID = "target_id"
ATTR_GROUP = "group"
ATTR_ENABLED = "enabled"
ATTR_DURATION_MINUTES = "duration_minutes"

TARGET_SCHEMA = {
    vol.Optional(ATTR_TARGET_ID): cv.string,
    vol.Optional(ATTR_GROUP): cv.string,
}


def _manager(hass: HomeAssistant) -> ProbulatorRuntimeManager:
    return hass.data[DOMAIN][DATA_MANAGER]


def _targets_for_call(
    hass: HomeAssistant,
    call: ServiceCall,
):
    manager = _manager(hass)
    target_id = str(call.data.get(ATTR_TARGET_ID, "") or "").strip() or None
    group = str(call.data.get(ATTR_GROUP, "") or "").strip() or None
    targets = manager.select_targets(target_id=target_id, group=group)
    if not targets:
        raise ServiceValidationError(
            "No HA Probulator targets matched the requested target_id/group"
        )
    return manager, targets


async def _async_probe(hass: HomeAssistant, call: ServiceCall) -> None:
    """Probe matching targets immediately."""
    _manager_obj, targets = _targets_for_call(hass, call)
    await asyncio.gather(*(target.async_request_refresh() for target in targets))


async def _async_set_monitoring(hass: HomeAssistant, call: ServiceCall) -> None:
    """Enable or disable matching targets."""
    manager, targets = _targets_for_call(hass, call)
    enabled = bool(call.data[ATTR_ENABLED])
    await asyncio.gather(
        *(
            manager.async_set_monitoring(target.target_id, enabled)
            for target in targets
        )
    )


async def _async_start_maintenance(hass: HomeAssistant, call: ServiceCall) -> None:
    """Start maintenance for matching targets."""
    manager, targets = _targets_for_call(hass, call)
    duration = int(call.data.get(ATTR_DURATION_MINUTES, 0))
    await asyncio.gather(
        *(
            manager.async_set_maintenance(
                target.target_id,
                True,
                duration_minutes=duration,
            )
            for target in targets
        )
    )


async def _async_end_maintenance(hass: HomeAssistant, call: ServiceCall) -> None:
    """End maintenance for matching targets."""
    manager, targets = _targets_for_call(hass, call)
    await asyncio.gather(
        *(
            manager.async_set_maintenance(target.target_id, False)
            for target in targets
        )
    )


def async_setup_services(hass: HomeAssistant) -> None:
    """Register administrator-only HA Probulator actions."""
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_PROBE,
        partial(_async_probe, hass),
        schema=vol.Schema(TARGET_SCHEMA),
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_SET_MONITORING,
        partial(_async_set_monitoring, hass),
        schema=vol.Schema(
            {
                **TARGET_SCHEMA,
                vol.Required(ATTR_ENABLED): cv.boolean,
            }
        ),
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_START_MAINTENANCE,
        partial(_async_start_maintenance, hass),
        schema=vol.Schema(
            {
                **TARGET_SCHEMA,
                vol.Optional(ATTR_DURATION_MINUTES, default=0): vol.All(
                    vol.Coerce(int),
                    vol.Range(min=0, max=10080),
                ),
            }
        ),
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_END_MAINTENANCE,
        partial(_async_end_maintenance, hass),
        schema=vol.Schema(TARGET_SCHEMA),
    )
