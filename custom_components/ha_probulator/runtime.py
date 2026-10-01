"""Shared runtime state for HA Probulator."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import DOMAIN

if TYPE_CHECKING:
    from .coordinator import ProbulatorCoordinator

STORAGE_VERSION = 1
STORAGE_KEY = f"{DOMAIN}.runtime"
SAVE_DELAY_SECONDS = 10
DEFAULT_MAX_CONCURRENT_PROBES = 20

_PERSISTED_METRIC_KEYS = (
    "total_probes",
    "successful_probes",
    "failed_probes",
    "last_success",
    "last_failure",
    "last_outage_duration_seconds",
    "outage_count",
    "total_outage_duration_seconds",
    "longest_outage_duration_seconds",
    "stable_since",
)


class ProbulatorRuntimeManager:
    """Own persistent runtime controls and cross-target coordination."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.store: Store[dict[str, Any]] = Store(
            hass,
            STORAGE_VERSION,
            STORAGE_KEY,
            private=True,
            atomic_writes=True,
        )
        self.probe_semaphore = asyncio.Semaphore(DEFAULT_MAX_CONCURRENT_PROBES)
        self._states: dict[str, dict[str, Any]] = {}
        self._coordinators: dict[str, ProbulatorCoordinator] = {}

    async def async_load(self) -> None:
        """Load persistent target runtime state."""
        stored = await self.store.async_load() or {}
        targets = stored.get("targets", {})
        if isinstance(targets, dict):
            self._states = {
                str(target_id): dict(value)
                for target_id, value in targets.items()
                if isinstance(value, dict)
            }

    def register(self, coordinator: ProbulatorCoordinator) -> None:
        """Register a live target coordinator."""
        self._coordinators[coordinator.target_id] = coordinator
        self._state(coordinator.target_id)

    def unregister(self, target_id: str) -> None:
        """Unregister a target coordinator while retaining persistent state."""
        self._coordinators.pop(target_id, None)

    def _state(self, target_id: str) -> dict[str, Any]:
        return self._states.setdefault(
            target_id,
            {
                "monitoring_enabled": True,
                "maintenance": False,
                "maintenance_until": None,
            },
        )

    def _schedule_save(self) -> None:
        self.store.async_delay_save(
            lambda: {"targets": self._states},
            SAVE_DELAY_SECONDS,
        )

    def monitoring_enabled(self, target_id: str) -> bool:
        """Return whether active probing is enabled."""
        return bool(self._state(target_id).get("monitoring_enabled", True))

    def maintenance_until(self, target_id: str) -> datetime | None:
        """Return the maintenance expiry when one exists."""
        state = self._state(target_id)
        if not state.get("maintenance", False):
            return None
        raw = state.get("maintenance_until")
        if not raw:
            return None
        try:
            parsed = datetime.fromisoformat(str(raw))
        except ValueError:
            state["maintenance_until"] = None
            self._schedule_save()
            return None
        return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)

    def in_maintenance(self, target_id: str) -> bool:
        """Return maintenance state and expire timed maintenance automatically."""
        state = self._state(target_id)
        if not state.get("maintenance", False):
            return False
        until = self.maintenance_until(target_id)
        if until is not None and until <= datetime.now(UTC):
            state["maintenance"] = False
            state["maintenance_until"] = None
            self._schedule_save()
            return False
        return True

    async def async_set_monitoring(self, target_id: str, enabled: bool) -> None:
        """Persist monitoring state and refresh the target."""
        state = self._state(target_id)
        state["monitoring_enabled"] = bool(enabled)
        self._schedule_save()
        if coordinator := self._coordinators.get(target_id):
            await coordinator.async_request_refresh()

    async def async_set_maintenance(
        self,
        target_id: str,
        enabled: bool,
        *,
        duration_minutes: int = 0,
    ) -> None:
        """Persist maintenance state and refresh the target."""
        state = self._state(target_id)
        state["maintenance"] = bool(enabled)
        if enabled and duration_minutes > 0:
            state["maintenance_until"] = (
                datetime.now(UTC) + timedelta(minutes=duration_minutes)
            ).isoformat()
        else:
            state["maintenance_until"] = None
        self._schedule_save()
        if coordinator := self._coordinators.get(target_id):
            await coordinator.async_request_refresh()

    def dependency_name(self, target_id: str | None) -> str | None:
        """Return a dependency target's friendly name."""
        if not target_id:
            return None
        coordinator = self._coordinators.get(target_id)
        return coordinator.entry.title if coordinator is not None else None

    def dependency_exists(self, target_id: str | None) -> bool:
        """Return whether a dependency target is currently loaded."""
        return not target_id or target_id in self._coordinators

    def notify_dependents(self, target_id: str) -> None:
        """Refresh dependents when an upstream effective status changes."""
        for coordinator in self._coordinators.values():
            if coordinator.dependency_target_id != target_id:
                continue
            self.hass.async_create_task(
                coordinator.async_request_refresh(),
                f"HA Probulator dependency refresh: {coordinator.entry.title}",
            )

    def dependency_status(self, target_id: str | None) -> str | None:
        """Return the effective status for a dependency target."""
        if not target_id:
            return None
        coordinator = self._coordinators.get(target_id)
        if coordinator is None or not coordinator.data:
            return "unknown"
        return str(coordinator.data.get("status", "unknown"))

    def coordinator_for_target(self, target_id: str) -> ProbulatorCoordinator | None:
        """Return a live coordinator by stable target ID."""
        return self._coordinators.get(target_id)

    def select_targets(
        self,
        *,
        target_id: str | None = None,
        group: str | None = None,
    ) -> list[ProbulatorCoordinator]:
        """Select live targets by stable ID, group, or all targets."""
        if target_id:
            coordinator = self._coordinators.get(target_id)
            return [coordinator] if coordinator is not None else []
        if group:
            wanted = group.strip().casefold()
            return [
                coordinator
                for coordinator in self._coordinators.values()
                if coordinator.group.casefold() == wanted
            ]
        return list(self._coordinators.values())

    def runtime_snapshot(self, target_id: str) -> dict[str, Any]:
        """Return a copy of persistent runtime state for diagnostics."""
        return dict(self._state(target_id))

    def restore_metrics(self, target_id: str) -> dict[str, Any]:
        """Return the persisted metric subset for a target."""
        state = self._state(target_id)
        return {key: state.get(key) for key in _PERSISTED_METRIC_KEYS}

    def persist_metrics(self, target_id: str, snapshot: dict[str, Any]) -> None:
        """Persist low-churn lifetime/outage metadata without writing every probe."""
        state = self._state(target_id)
        changed = False
        for key in _PERSISTED_METRIC_KEYS:
            value = snapshot.get(key)
            if isinstance(value, datetime):
                value = value.isoformat()
            if state.get(key) != value:
                state[key] = value
                changed = True
        if changed:
            self._schedule_save()

    async def async_probe_targets(
        self,
        *,
        target_id: str | None = None,
        group: str | None = None,
    ) -> int:
        """Request an immediate probe for matching targets."""
        targets = self.select_targets(target_id=target_id, group=group)
        if not targets:
            return 0
        await asyncio.gather(*(target.async_request_refresh() for target in targets))
        return len(targets)
