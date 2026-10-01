"""Config flow for HA Probulator."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, UnitOfTime
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_CRITICAL_LATENCY,
    CONF_FAILURE_THRESHOLD,
    CONF_GROUP,
    CONF_ICON,
    CONF_RECOVERY_THRESHOLD,
    CONF_RETRIES,
    CONF_RETRY_DELAY,
    CONF_SCAN_INTERVAL,
    CONF_STATISTICS_WINDOW,
    CONF_TARGET_ID,
    CONF_TIMEOUT,
    CONF_WARNING_LATENCY,
    DEFAULT_CRITICAL_LATENCY,
    DEFAULT_FAILURE_THRESHOLD,
    DEFAULT_GROUP,
    DEFAULT_ICON,
    DEFAULT_PORT,
    DEFAULT_RECOVERY_THRESHOLD,
    DEFAULT_RETRIES,
    DEFAULT_RETRY_DELAY,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_STATISTICS_WINDOW,
    DEFAULT_TIMEOUT,
    DEFAULT_WARNING_LATENCY,
    DOMAIN,
    MAX_RETRIES,
    MAX_SCAN_INTERVAL,
    MAX_STATISTICS_WINDOW,
    MAX_THRESHOLD,
    MAX_TIMEOUT,
    MIN_SCAN_INTERVAL,
    MIN_STATISTICS_WINDOW,
    MIN_TIMEOUT,
)


def _text(value: Any) -> str:
    return str(value or "").strip()


def _target_schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
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
                CONF_PORT, default=defaults.get(CONF_PORT, DEFAULT_PORT)
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


def _options_schema(defaults: dict[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            vol.Optional(
                CONF_GROUP, default=defaults.get(CONF_GROUP, DEFAULT_GROUP)
            ): selector.TextSelector(),
            vol.Required(
                CONF_ICON, default=defaults.get(CONF_ICON, DEFAULT_ICON)
            ): selector.IconSelector(),
            vol.Required(
                CONF_SCAN_INTERVAL,
                default=defaults.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
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
                CONF_TIMEOUT, default=defaults.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)
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
                CONF_RETRIES, default=defaults.get(CONF_RETRIES, DEFAULT_RETRIES)
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=MAX_RETRIES,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_RETRY_DELAY,
                default=defaults.get(CONF_RETRY_DELAY, DEFAULT_RETRY_DELAY),
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
                CONF_FAILURE_THRESHOLD,
                default=defaults.get(
                    CONF_FAILURE_THRESHOLD, DEFAULT_FAILURE_THRESHOLD
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=MAX_THRESHOLD,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_RECOVERY_THRESHOLD,
                default=defaults.get(
                    CONF_RECOVERY_THRESHOLD, DEFAULT_RECOVERY_THRESHOLD
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=MAX_THRESHOLD,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_WARNING_LATENCY,
                default=defaults.get(CONF_WARNING_LATENCY, DEFAULT_WARNING_LATENCY),
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
                CONF_CRITICAL_LATENCY,
                default=defaults.get(CONF_CRITICAL_LATENCY, DEFAULT_CRITICAL_LATENCY),
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
                CONF_STATISTICS_WINDOW,
                default=defaults.get(
                    CONF_STATISTICS_WINDOW, DEFAULT_STATISTICS_WINDOW
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=MIN_STATISTICS_WINDOW,
                    max=MAX_STATISTICS_WINDOW,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
        }
    )


def _normalize_target_input(user_input: dict[str, Any]) -> dict[str, Any]:
    return {
        CONF_NAME: _text(user_input[CONF_NAME]),
        CONF_HOST: _text(user_input[CONF_HOST]).rstrip("."),
        CONF_PORT: int(user_input[CONF_PORT]),
    }


def _validate_target(values: dict[str, Any]) -> dict[str, str]:
    errors: dict[str, str] = {}
    if not values[CONF_NAME]:
        errors[CONF_NAME] = "required"
    host = values[CONF_HOST]
    if not host or any(char.isspace() for char in host) or "://" in host:
        errors[CONF_HOST] = "invalid_host"
    return errors


def _normalize_options(user_input: dict[str, Any]) -> dict[str, Any]:
    return {
        CONF_GROUP: _text(user_input.get(CONF_GROUP)),
        CONF_ICON: _text(user_input.get(CONF_ICON)) or DEFAULT_ICON,
        CONF_SCAN_INTERVAL: int(user_input[CONF_SCAN_INTERVAL]),
        CONF_TIMEOUT: float(user_input[CONF_TIMEOUT]),
        CONF_RETRIES: int(user_input[CONF_RETRIES]),
        CONF_RETRY_DELAY: float(user_input[CONF_RETRY_DELAY]),
        CONF_FAILURE_THRESHOLD: int(user_input[CONF_FAILURE_THRESHOLD]),
        CONF_RECOVERY_THRESHOLD: int(user_input[CONF_RECOVERY_THRESHOLD]),
        CONF_WARNING_LATENCY: float(user_input[CONF_WARNING_LATENCY]),
        CONF_CRITICAL_LATENCY: float(user_input[CONF_CRITICAL_LATENCY]),
        CONF_STATISTICS_WINDOW: int(user_input[CONF_STATISTICS_WINDOW]),
    }


class ProbulatorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle HA Probulator config entries."""

    VERSION = 1

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
        """Create a new monitored target."""
        errors: dict[str, str] = {}
        suggested = user_input

        if user_input is not None:
            values = _normalize_target_input(user_input)
            suggested = values
            errors = _validate_target(values)
            if not errors:
                self._async_abort_entries_match(
                    {CONF_HOST: values[CONF_HOST], CONF_PORT: values[CONF_PORT]}
                )
                target_id = uuid4().hex
                await self.async_set_unique_id(target_id)
                return self.async_create_entry(
                    title=values[CONF_NAME],
                    data={
                        CONF_TARGET_ID: target_id,
                        CONF_HOST: values[CONF_HOST],
                        CONF_PORT: values[CONF_PORT],
                    },
                    options=_normalize_options(
                        {
                            CONF_GROUP: DEFAULT_GROUP,
                            CONF_ICON: DEFAULT_ICON,
                            CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
                            CONF_TIMEOUT: DEFAULT_TIMEOUT,
                            CONF_RETRIES: DEFAULT_RETRIES,
                            CONF_RETRY_DELAY: DEFAULT_RETRY_DELAY,
                            CONF_FAILURE_THRESHOLD: DEFAULT_FAILURE_THRESHOLD,
                            CONF_RECOVERY_THRESHOLD: DEFAULT_RECOVERY_THRESHOLD,
                            CONF_WARNING_LATENCY: DEFAULT_WARNING_LATENCY,
                            CONF_CRITICAL_LATENCY: DEFAULT_CRITICAL_LATENCY,
                            CONF_STATISTICS_WINDOW: DEFAULT_STATISTICS_WINDOW,
                        }
                    ),
                )

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                _target_schema(), suggested or {}
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
            values = _normalize_target_input(user_input)
            suggested = values
            errors = _validate_target(values)
            if not errors:
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
        errors: dict[str, str] = {}
        suggested = user_input or dict(self.config_entry.options)

        if user_input is not None:
            values = _normalize_options(user_input)
            suggested = values
            if values[CONF_CRITICAL_LATENCY] <= values[CONF_WARNING_LATENCY]:
                errors[CONF_CRITICAL_LATENCY] = "critical_must_exceed_warning"
            if not errors:
                return self.async_create_entry(title="", data=values)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                _options_schema(dict(self.config_entry.options)), suggested
            ),
            errors=errors,
        )
