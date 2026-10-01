"""Home Assistant actions for HA Probulator."""

from __future__ import annotations

import asyncio
import json
from functools import partial
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
)
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.service import async_register_admin_service

from .const import (
    CONF_DEPENDENCY_TARGET_ID,
    CONF_PRESET,
    CONF_TARGET_ID,
    DATA_MANAGER,
    DEFAULT_PRESET,
    DOMAIN,
    SERVICE_CLONE_TARGET,
    SERVICE_END_MAINTENANCE,
    SERVICE_EXPORT_CONFIG,
    SERVICE_IMPORT_CONFIG,
    SERVICE_PROBE,
    SERVICE_SET_MONITORING,
    SERVICE_START_MAINTENANCE,
    SERVICE_SUGGEST_TARGETS,
)
from .runtime import ProbulatorRuntimeManager
from .validation import ValidationError, normalize_host

ATTR_TARGET_ID = "target_id"
ATTR_GROUP = "group"
ATTR_ENABLED = "enabled"
ATTR_DURATION_MINUTES = "duration_minutes"
ATTR_SOURCE_TARGET_ID = "source_target_id"
ATTR_PAYLOAD = "payload"

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
        *(manager.async_set_monitoring(target.target_id, enabled) for target in targets)
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
        *(manager.async_set_maintenance(target.target_id, False) for target in targets)
    )


def _portable_target(
    entry: ConfigEntry,
    index: int,
    id_to_ref: dict[str, str],
) -> dict[str, Any]:
    """Return a portable target payload with no Home Assistant config-entry IDs."""
    target_id = str(entry.data.get(CONF_TARGET_ID, entry.entry_id))
    dependency_target_id = str(
        entry.options.get(CONF_DEPENDENCY_TARGET_ID, "") or ""
    ).strip()
    options = dict(entry.options)
    options[CONF_DEPENDENCY_TARGET_ID] = ""
    return {
        "portable_id": id_to_ref[target_id],
        CONF_NAME: entry.title,
        CONF_PRESET: str(entry.data.get(CONF_PRESET, DEFAULT_PRESET)),
        CONF_HOST: entry.data[CONF_HOST],
        CONF_PORT: entry.data[CONF_PORT],
        "dependency_ref": id_to_ref.get(dependency_target_id),
        "options": options,
        "order": index,
    }


async def _async_export_config(
    hass: HomeAssistant,
    call: ServiceCall,
) -> ServiceResponse:
    """Return a portable HA Probulator configuration bundle."""
    entries = sorted(
        hass.config_entries.async_entries(DOMAIN),
        key=lambda entry: (entry.title.casefold(), entry.entry_id),
    )
    id_to_ref = {
        str(entry.data.get(CONF_TARGET_ID, entry.entry_id)): f"target-{index + 1}"
        for index, entry in enumerate(entries)
    }
    targets = [
        _portable_target(entry, index, id_to_ref) for index, entry in enumerate(entries)
    ]
    bundle = {
        "format": "ha-probulator",
        "format_version": 1,
        "targets": targets,
    }
    return {
        "bundle": bundle,
        "json": json.dumps(bundle, indent=2, sort_keys=True),
        "target_count": len(targets),
    }


async def _create_from_import(
    hass: HomeAssistant,
    payload: dict[str, Any],
) -> ConfigEntry | None:
    """Create one target through the integration's import config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_IMPORT},
        data=payload,
    )
    entry = result.get("result")
    return entry if isinstance(entry, ConfigEntry) else None


async def _async_import_config(
    hass: HomeAssistant,
    call: ServiceCall,
) -> ServiceResponse:
    """Import a portable HA Probulator configuration bundle."""
    raw_payload = call.data[ATTR_PAYLOAD]
    try:
        bundle = (
            json.loads(raw_payload) if isinstance(raw_payload, str) else raw_payload
        )
    except json.JSONDecodeError as exc:
        raise ServiceValidationError("Import payload is not valid JSON") from exc

    if not isinstance(bundle, dict) or bundle.get("format") != "ha-probulator":
        raise ServiceValidationError("Import payload is not an HA Probulator bundle")
    if bundle.get("format_version") != 1:
        raise ServiceValidationError("Unsupported HA Probulator import format version")

    targets = bundle.get("targets")
    if not isinstance(targets, list) or not targets:
        raise ServiceValidationError("Import bundle does not contain any targets")
    if len(targets) > 500:
        raise ServiceValidationError(
            "Import bundle exceeds the 500-target safety limit"
        )

    created: dict[str, ConfigEntry] = {}
    skipped: list[dict[str, str]] = []

    for item in targets:
        if not isinstance(item, dict):
            skipped.append({"target": "<invalid>", "reason": "invalid_target"})
            continue
        portable_id = str(item.get("portable_id", "")).strip()
        if not portable_id or portable_id in created:
            skipped.append(
                {
                    "target": str(item.get(CONF_NAME, "<unnamed>")),
                    "reason": "invalid_portable_id",
                }
            )
            continue

        flow_payload = {
            CONF_NAME: item.get(CONF_NAME, ""),
            CONF_PRESET: item.get(CONF_PRESET, DEFAULT_PRESET),
            CONF_HOST: item.get(CONF_HOST, ""),
            CONF_PORT: item.get(CONF_PORT),
            "options": item.get("options", {}),
        }
        entry = await _create_from_import(hass, flow_payload)
        if entry is None:
            skipped.append(
                {
                    "target": str(item.get(CONF_NAME, "<unnamed>")),
                    "reason": "duplicate_or_invalid",
                }
            )
            continue
        created[portable_id] = entry

    # Restore imported dependency relationships only after every possible target has
    # a fresh local stable target ID.
    by_ref = {
        ref: str(entry.data.get(CONF_TARGET_ID, entry.entry_id))
        for ref, entry in created.items()
    }
    for item in targets:
        if not isinstance(item, dict):
            continue
        portable_id = str(item.get("portable_id", "")).strip()
        dependency_ref = str(item.get("dependency_ref", "") or "").strip()
        if not dependency_ref or portable_id not in created:
            continue
        dependency_target_id = by_ref.get(dependency_ref)
        if dependency_target_id is None:
            continue
        entry = created[portable_id]
        options = dict(entry.options)
        options[CONF_DEPENDENCY_TARGET_ID] = dependency_target_id
        hass.config_entries.async_update_entry(entry, options=options)

    return {
        "created": len(created),
        "skipped": skipped,
        "created_targets": [
            {
                "portable_id": ref,
                "name": entry.title,
                "target_id": str(entry.data.get(CONF_TARGET_ID, entry.entry_id)),
            }
            for ref, entry in created.items()
        ],
    }


async def _async_clone_target(
    hass: HomeAssistant,
    call: ServiceCall,
) -> ServiceResponse:
    """Clone one target's monitoring behavior to a new endpoint."""
    manager = _manager(hass)
    source_target_id = str(call.data[ATTR_SOURCE_TARGET_ID]).strip()
    source = manager.coordinator_for_target(source_target_id)
    if source is None:
        raise ServiceValidationError("Source HA Probulator target was not found")

    name = str(call.data[CONF_NAME]).strip()
    host = str(call.data[CONF_HOST]).strip()
    port = int(call.data.get(CONF_PORT, source.port))

    options = dict(source.entry.options)
    options[CONF_DEPENDENCY_TARGET_ID] = ""
    payload = {
        CONF_NAME: name,
        CONF_PRESET: source.entry.data.get(CONF_PRESET, DEFAULT_PRESET),
        CONF_HOST: host,
        CONF_PORT: port,
        "options": options,
    }
    entry = await _create_from_import(hass, payload)
    if entry is None:
        raise ServiceValidationError(
            "Clone could not be created because the destination is invalid "
            "or already exists"
        )

    return {
        "created": True,
        "name": entry.title,
        "target_id": str(entry.data.get(CONF_TARGET_ID, entry.entry_id)),
    }


async def _async_suggest_targets(
    hass: HomeAssistant,
    call: ServiceCall,
) -> ServiceResponse:
    """Return non-invasive target suggestions from data Home Assistant already knows."""
    manager = _manager(hass)
    monitored: dict[str, set[int]] = {}
    for coordinator in manager.select_targets():
        monitored.setdefault(coordinator.host.casefold(), set()).add(coordinator.port)

    candidate_attributes = (
        "ip_address",
        "ip",
        "host",
        "hostname",
        "address",
    )
    candidates: dict[tuple[str, int], dict[str, Any]] = {}

    for state in hass.states.async_all():
        attrs = state.attributes
        for attribute in candidate_attributes:
            raw_host = attrs.get(attribute)
            if not isinstance(raw_host, str) or not raw_host.strip():
                continue
            try:
                host = normalize_host(raw_host)
            except ValidationError:
                continue

            raw_port = attrs.get("port")
            try:
                port = int(raw_port) if raw_port is not None else 443
            except (TypeError, ValueError):
                port = 443
            if port < 1 or port > 65535:
                port = 443

            key = (host.casefold(), port)
            if key in candidates:
                continue
            candidates[key] = {
                "name": str(attrs.get("friendly_name") or state.entity_id),
                "host": host,
                "port": port,
                "source_entity": state.entity_id,
                "source_attribute": attribute,
                "suggested_preset": "generic",
                "already_monitored": port in monitored.get(host.casefold(), set()),
                "monitored_ports": sorted(monitored.get(host.casefold(), set())),
            }

    ordered = sorted(
        candidates.values(),
        key=lambda item: (
            item["already_monitored"],
            str(item["name"]).casefold(),
            str(item["host"]).casefold(),
            int(item["port"]),
        ),
    )
    return {
        "candidates": ordered[:250],
        "candidate_count": min(len(ordered), 250),
        "truncated": len(ordered) > 250,
        "method": "home_assistant_known_attributes",
        "network_scan_performed": False,
    }


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
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_EXPORT_CONFIG,
        partial(_async_export_config, hass),
        supports_response=SupportsResponse.ONLY,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_IMPORT_CONFIG,
        partial(_async_import_config, hass),
        schema=vol.Schema({vol.Required(ATTR_PAYLOAD): vol.Any(str, dict)}),
        supports_response=SupportsResponse.ONLY,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_CLONE_TARGET,
        partial(_async_clone_target, hass),
        schema=vol.Schema(
            {
                vol.Required(ATTR_SOURCE_TARGET_ID): cv.string,
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_HOST): cv.string,
                vol.Optional(CONF_PORT): vol.All(
                    vol.Coerce(int),
                    vol.Range(min=1, max=65535),
                ),
            }
        ),
        supports_response=SupportsResponse.ONLY,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_SUGGEST_TARGETS,
        partial(_async_suggest_targets, hass),
        supports_response=SupportsResponse.ONLY,
    )
