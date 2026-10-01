"""Config flow for HA Probulator."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, UnitOfTime
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector
from homeassistant.helpers.selector import SelectOptionDict

from .const import (
    CONF_ADAPTIVE_POLLING,
    CONF_CRITICAL_LATENCY,
    CONF_DEGRADED_SCAN_INTERVAL,
    CONF_DEPENDENCY_TARGET_ID,
    CONF_FAILURE_THRESHOLD,
    CONF_FLAP_THRESHOLD,
    CONF_FLAP_WINDOW,
    CONF_GROUP,
    CONF_ICON,
    CONF_OFFLINE_SCAN_INTERVAL,
    CONF_PRESET,
    CONF_RECOVERY_THRESHOLD,
    CONF_RETRIES,
    CONF_RETRY_DELAY,
    CONF_SCAN_INTERVAL,
    CONF_STATISTICS_WINDOW,
    CONF_TARGET_ID,
    CONF_TIMEOUT,
    CONF_WARNING_LATENCY,
    DEFAULT_ADAPTIVE_POLLING,
    DEFAULT_CRITICAL_LATENCY,
    DEFAULT_DEGRADED_SCAN_INTERVAL,
    DEFAULT_DEPENDENCY_TARGET_ID,
    DEFAULT_FAILURE_THRESHOLD,
    DEFAULT_FLAP_THRESHOLD,
    DEFAULT_FLAP_WINDOW,
    DEFAULT_GROUP,
    DEFAULT_ICON,
    DEFAULT_OFFLINE_SCAN_INTERVAL,
    DEFAULT_PORT,
    DEFAULT_PRESET,
    DEFAULT_RECOVERY_THRESHOLD,
    DEFAULT_RETRIES,
    DEFAULT_RETRY_DELAY,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_STATISTICS_WINDOW,
    DEFAULT_TIMEOUT,
    DEFAULT_WARNING_LATENCY,
    DOMAIN,
    MAX_FLAP_THRESHOLD,
    MAX_FLAP_WINDOW,
    MAX_RETRIES,
    MAX_SCAN_INTERVAL,
    MAX_STATISTICS_WINDOW,
    MAX_THRESHOLD,
    MAX_TIMEOUT,
    MIN_FLAP_THRESHOLD,
    MIN_FLAP_WINDOW,
    MIN_SCAN_INTERVAL,
    MIN_STATISTICS_WINDOW,
    MIN_TIMEOUT,
)
from .presets import PRESETS, get_preset
from .validation import (
    ValidationError,
    normalize_group,
    normalize_host,
    normalize_name,
    validate_probe_budget,
)


def _preset_schema(default: str = DEFAULT_PRESET) -> vol.Schema:
    options = [
        SelectOptionDict(value=preset.key, label=preset.name)
        for preset in PRESETS.values()
    ]
    return vol.Schema(
        {
            vol.Required(CONF_PRESET, default=default): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=options,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            )
        }
    )


def _target_schema(
    defaults: dict[str, Any] | None = None,
    *,
    default_port: int = DEFAULT_PORT,
) -> vol.Schema:
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_NAME, default=defaults.get(CONF_NAME, "")
            ): selector.TextSelector(),
            vol.Required(
                CONF_HOST, default=defaults.get(CONF_HOST, "")
            ): selector.TextSelector(),
            vol.Required(
                CONF_PORT, default=defaults.get(CONF_PORT, default_port)
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=65535,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
        }
    )


def _dependency_options(
    hass: HomeAssistant,
    *,
    exclude_entry_id: str | None = None,
) -> list[SelectOptionDict]:
    options = [SelectOptionDict(value="", label="None")]
    for entry in hass.config_entries.async_entries(DOMAIN):
        if entry.entry_id == exclude_entry_id:
            continue
        target_id = str(entry.data.get(CONF_TARGET_ID, entry.entry_id))
        options.append(SelectOptionDict(value=target_id, label=entry.title))
    return options


def _default_options(preset_key: str = DEFAULT_PRESET) -> dict[str, Any]:
    preset = get_preset(preset_key)
    return {
        CONF_GROUP: preset.group or DEFAULT_GROUP,
        CONF_ICON: preset.icon or DEFAULT_ICON,
        CONF_SCAN_INTERVAL: preset.scan_interval or DEFAULT_SCAN_INTERVAL,
        CONF_TIMEOUT: preset.timeout or DEFAULT_TIMEOUT,
        CONF_RETRIES: preset.retries if preset.retries >= 0 else DEFAULT_RETRIES,
        CONF_RETRY_DELAY: DEFAULT_RETRY_DELAY,
        CONF_FAILURE_THRESHOLD: DEFAULT_FAILURE_THRESHOLD,
        CONF_RECOVERY_THRESHOLD: DEFAULT_RECOVERY_THRESHOLD,
        CONF_WARNING_LATENCY: preset.warning_latency_ms or DEFAULT_WARNING_LATENCY,
        CONF_CRITICAL_LATENCY: preset.critical_latency_ms or DEFAULT_CRITICAL_LATENCY,
        CONF_STATISTICS_WINDOW: DEFAULT_STATISTICS_WINDOW,
        CONF_DEPENDENCY_TARGET_ID: DEFAULT_DEPENDENCY_TARGET_ID,
        CONF_ADAPTIVE_POLLING: DEFAULT_ADAPTIVE_POLLING,
        CONF_DEGRADED_SCAN_INTERVAL: DEFAULT_DEGRADED_SCAN_INTERVAL,
        CONF_OFFLINE_SCAN_INTERVAL: DEFAULT_OFFLINE_SCAN_INTERVAL,
        CONF_FLAP_WINDOW: DEFAULT_FLAP_WINDOW,
        CONF_FLAP_THRESHOLD: DEFAULT_FLAP_THRESHOLD,
    }


def _options_schema(
    defaults: dict[str, Any],
    dependency_options: list[SelectOptionDict],
) -> vol.Schema:
    merged = {**_default_options(), **defaults}
    return vol.Schema(
        {
            vol.Optional(
                CONF_GROUP, default=merged[CONF_GROUP]
            ): selector.TextSelector(),
            vol.Required(CONF_ICON, default=merged[CONF_ICON]): selector.IconSelector(),
            vol.Optional(
                CONF_DEPENDENCY_TARGET_ID,
                default=merged[CONF_DEPENDENCY_TARGET_ID],
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=dependency_options,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_SCAN_INTERVAL, default=merged[CONF_SCAN_INTERVAL]
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=MIN_SCAN_INTERVAL,
                    max=MAX_SCAN_INTERVAL,
                    step=1,
                    unit_of_measurement=UnitOfTime.SECONDS,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_ADAPTIVE_POLLING, default=merged[CONF_ADAPTIVE_POLLING]
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_DEGRADED_SCAN_INTERVAL,
                default=merged[CONF_DEGRADED_SCAN_INTERVAL],
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=MIN_SCAN_INTERVAL,
                    max=MAX_SCAN_INTERVAL,
                    step=1,
                    unit_of_measurement=UnitOfTime.SECONDS,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_OFFLINE_SCAN_INTERVAL,
                default=merged[CONF_OFFLINE_SCAN_INTERVAL],
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=MIN_SCAN_INTERVAL,
                    max=MAX_SCAN_INTERVAL,
                    step=1,
                    unit_of_measurement=UnitOfTime.SECONDS,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_TIMEOUT, default=merged[CONF_TIMEOUT]
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=MIN_TIMEOUT,
                    max=MAX_TIMEOUT,
                    step=0.1,
                    unit_of_measurement=UnitOfTime.SECONDS,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_RETRIES, default=merged[CONF_RETRIES]
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=MAX_RETRIES,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_RETRY_DELAY, default=merged[CONF_RETRY_DELAY]
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=5,
                    step=0.05,
                    unit_of_measurement=UnitOfTime.SECONDS,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_FAILURE_THRESHOLD, default=merged[CONF_FAILURE_THRESHOLD]
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=MAX_THRESHOLD,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_RECOVERY_THRESHOLD, default=merged[CONF_RECOVERY_THRESHOLD]
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=MAX_THRESHOLD,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_WARNING_LATENCY, default=merged[CONF_WARNING_LATENCY]
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=30000,
                    step=1,
                    unit_of_measurement=UnitOfTime.MILLISECONDS,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_CRITICAL_LATENCY, default=merged[CONF_CRITICAL_LATENCY]
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=60000,
                    step=1,
                    unit_of_measurement=UnitOfTime.MILLISECONDS,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_STATISTICS_WINDOW, default=merged[CONF_STATISTICS_WINDOW]
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=MIN_STATISTICS_WINDOW,
                    max=MAX_STATISTICS_WINDOW,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_FLAP_WINDOW, default=merged[CONF_FLAP_WINDOW]
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=MIN_FLAP_WINDOW,
                    max=MAX_FLAP_WINDOW,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_FLAP_THRESHOLD, default=merged[CONF_FLAP_THRESHOLD]
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=MIN_FLAP_THRESHOLD,
                    max=MAX_FLAP_THRESHOLD,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
        }
    )


def _normalize_target_input(
    user_input: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, str]]:
    errors: dict[str, str] = {}
    values: dict[str, Any] = {CONF_PORT: int(user_input[CONF_PORT])}

    try:
        values[CONF_NAME] = normalize_name(user_input[CONF_NAME])
    except ValidationError as exc:
        errors[CONF_NAME] = exc.code
        values[CONF_NAME] = str(user_input.get(CONF_NAME, "")).strip()

    try:
        values[CONF_HOST] = normalize_host(user_input[CONF_HOST])
    except ValidationError as exc:
        errors[CONF_HOST] = exc.code
        values[CONF_HOST] = str(user_input.get(CONF_HOST, "")).strip()

    return values, errors


def _normalize_options(
    user_input: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, str]]:
    errors: dict[str, str] = {}
    try:
        group = normalize_group(user_input.get(CONF_GROUP))
    except ValidationError as exc:
        errors[CONF_GROUP] = exc.code
        group = str(user_input.get(CONF_GROUP, "")).strip()

    values = {
        CONF_GROUP: group,
        CONF_ICON: str(user_input.get(CONF_ICON) or DEFAULT_ICON).strip(),
        CONF_DEPENDENCY_TARGET_ID: str(
            user_input.get(CONF_DEPENDENCY_TARGET_ID) or ""
        ).strip(),
        CONF_SCAN_INTERVAL: int(user_input[CONF_SCAN_INTERVAL]),
        CONF_ADAPTIVE_POLLING: bool(user_input[CONF_ADAPTIVE_POLLING]),
        CONF_DEGRADED_SCAN_INTERVAL: int(user_input[CONF_DEGRADED_SCAN_INTERVAL]),
        CONF_OFFLINE_SCAN_INTERVAL: int(user_input[CONF_OFFLINE_SCAN_INTERVAL]),
        CONF_TIMEOUT: float(user_input[CONF_TIMEOUT]),
        CONF_RETRIES: int(user_input[CONF_RETRIES]),
        CONF_RETRY_DELAY: float(user_input[CONF_RETRY_DELAY]),
        CONF_FAILURE_THRESHOLD: int(user_input[CONF_FAILURE_THRESHOLD]),
        CONF_RECOVERY_THRESHOLD: int(user_input[CONF_RECOVERY_THRESHOLD]),
        CONF_WARNING_LATENCY: float(user_input[CONF_WARNING_LATENCY]),
        CONF_CRITICAL_LATENCY: float(user_input[CONF_CRITICAL_LATENCY]),
        CONF_STATISTICS_WINDOW: int(user_input[CONF_STATISTICS_WINDOW]),
        CONF_FLAP_WINDOW: int(user_input[CONF_FLAP_WINDOW]),
        CONF_FLAP_THRESHOLD: int(user_input[CONF_FLAP_THRESHOLD]),
    }

    if values[CONF_CRITICAL_LATENCY] <= values[CONF_WARNING_LATENCY]:
        errors[CONF_CRITICAL_LATENCY] = "critical_must_exceed_warning"

    if values[CONF_FLAP_THRESHOLD] >= values[CONF_FLAP_WINDOW]:
        errors[CONF_FLAP_THRESHOLD] = "flap_threshold_too_high"

    try:
        validate_probe_budget(
            timeout=values[CONF_TIMEOUT],
            retries=values[CONF_RETRIES],
            retry_delay=values[CONF_RETRY_DELAY],
        )
    except ValidationError as exc:
        errors["base"] = exc.code

    return values, errors


def _would_create_dependency_cycle(
    hass: HomeAssistant,
    entry: config_entries.ConfigEntry,
    dependency_target_id: str,
) -> bool:
    if not dependency_target_id:
        return False

    this_target_id = str(entry.data.get(CONF_TARGET_ID, entry.entry_id))
    if dependency_target_id == this_target_id:
        return True

    by_target = {
        str(item.data.get(CONF_TARGET_ID, item.entry_id)): str(
            item.options.get(CONF_DEPENDENCY_TARGET_ID, "")
        )
        for item in hass.config_entries.async_entries(DOMAIN)
    }
    cursor = dependency_target_id
    visited: set[str] = set()

    while cursor:
        if cursor == this_target_id:
            return True
        if cursor in visited:
            return True
        visited.add(cursor)
        cursor = by_target.get(cursor, "")

    return False


class ProbulatorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle HA Probulator config entries."""

    VERSION = 2
    MINOR_VERSION = 1

    def __init__(self) -> None:
        self._pending_preset = DEFAULT_PRESET
        self._pending_target: dict[str, Any] | None = None

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlow:
        """Return the options flow."""
        return ProbulatorOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Choose a target role preset."""
        if user_input is not None:
            self._pending_preset = str(user_input.get(CONF_PRESET, DEFAULT_PRESET))
            return await self.async_step_target()

        return self.async_show_form(
            step_id="user",
            data_schema=_preset_schema(self._pending_preset),
        )

    async def async_step_target(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Collect a new monitored target."""
        errors: dict[str, str] = {}
        suggested = user_input or {}
        preset = get_preset(self._pending_preset)

        if user_input is not None:
            values, errors = _normalize_target_input(user_input)
            suggested = values
            if not errors:
                self._async_abort_entries_match(
                    {CONF_HOST: values[CONF_HOST], CONF_PORT: values[CONF_PORT]}
                )
                self._pending_target = values
                return await self.async_step_monitoring()

        return self.async_show_form(
            step_id="target",
            data_schema=self.add_suggested_values_to_schema(
                _target_schema(default_port=preset.port), suggested
            ),
            errors=errors,
        )

    async def async_step_monitoring(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure monitoring behavior before creating the target."""
        if self._pending_target is None:
            return self.async_abort(reason="setup_incomplete")

        defaults = _default_options(self._pending_preset)
        errors: dict[str, str] = {}
        suggested = user_input or defaults

        if user_input is not None:
            values, errors = _normalize_options(user_input)
            suggested = values
            if not errors:
                self._async_abort_entries_match(
                    {
                        CONF_HOST: self._pending_target[CONF_HOST],
                        CONF_PORT: self._pending_target[CONF_PORT],
                    }
                )
                target_id = uuid4().hex
                await self.async_set_unique_id(target_id)
                return self.async_create_entry(
                    title=self._pending_target[CONF_NAME],
                    data={
                        CONF_TARGET_ID: target_id,
                        CONF_PRESET: self._pending_preset,
                        CONF_HOST: self._pending_target[CONF_HOST],
                        CONF_PORT: self._pending_target[CONF_PORT],
                    },
                    options=values,
                )

        return self.async_show_form(
            step_id="monitoring",
            data_schema=self.add_suggested_values_to_schema(
                _options_schema(
                    defaults,
                    _dependency_options(self.hass),
                ),
                suggested,
            ),
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Change the target address or display name."""
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}
        defaults = {
            CONF_NAME: entry.title,
            CONF_HOST: entry.data[CONF_HOST],
            CONF_PORT: entry.data[CONF_PORT],
        }
        suggested = user_input or defaults

        if user_input is not None:
            values, errors = _normalize_target_input(user_input)
            suggested = values
            if not errors:
                if (
                    values[CONF_HOST] != entry.data[CONF_HOST]
                    or values[CONF_PORT] != entry.data[CONF_PORT]
                ):
                    self._async_abort_entries_match(
                        {CONF_HOST: values[CONF_HOST], CONF_PORT: values[CONF_PORT]}
                    )
                return self.async_update_and_abort(
                    entry,
                    title=values[CONF_NAME],
                    data_updates={
                        CONF_HOST: values[CONF_HOST],
                        CONF_PORT: values[CONF_PORT],
                    },
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                _target_schema(defaults), suggested
            ),
            errors=errors,
        )


class ProbulatorOptionsFlow(OptionsFlow):
    """Configure monitoring behavior for a target."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage target options."""
        preset_key = str(self.config_entry.data.get(CONF_PRESET, DEFAULT_PRESET))
        errors: dict[str, str] = {}
        suggested = user_input or {
            **_default_options(preset_key),
            **dict(self.config_entry.options),
        }

        if user_input is not None:
            values, errors = _normalize_options(user_input)
            suggested = values
            dependency = values[CONF_DEPENDENCY_TARGET_ID]
            if dependency and _would_create_dependency_cycle(
                self.hass,
                self.config_entry,
                dependency,
            ):
                errors[CONF_DEPENDENCY_TARGET_ID] = "dependency_cycle"
            if not errors:
                return self.async_create_entry(title="", data=values)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                _options_schema(
                    dict(self.config_entry.options),
                    _dependency_options(
                        self.hass,
                        exclude_entry_id=self.config_entry.entry_id,
                    ),
                ),
                suggested,
            ),
            errors=errors,
        )
