"""Monitoring presets for HA Probulator."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TargetPreset:
    """Suggested defaults for a target role."""

    key: str
    name: str
    port: int
    icon: str
    group: str
    warning_latency_ms: float
    critical_latency_ms: float
    scan_interval: int = 30
    timeout: float = 3.0
    retries: int = 1


PRESETS: dict[str, TargetPreset] = {
    "generic": TargetPreset(
        key="generic",
        name="Generic TCP service",
        port=443,
        icon="mdi:lan-connect",
        group="",
        warning_latency_ms=150,
        critical_latency_ms=500,
    ),
    "router": TargetPreset(
        key="router",
        name="Router / gateway",
        port=443,
        icon="mdi:router-network",
        group="Core Network",
        warning_latency_ms=25,
        critical_latency_ms=100,
        scan_interval=20,
        timeout=2.0,
        retries=2,
    ),
    "switch": TargetPreset(
        key="switch",
        name="Network switch",
        port=443,
        icon="mdi:switch",
        group="Core Network",
        warning_latency_ms=20,
        critical_latency_ms=75,
        scan_interval=20,
        timeout=2.0,
        retries=2,
    ),
    "server": TargetPreset(
        key="server",
        name="Server",
        port=22,
        icon="mdi:server",
        group="Servers",
        warning_latency_ms=50,
        critical_latency_ms=200,
    ),
    "nas": TargetPreset(
        key="nas",
        name="NAS / storage",
        port=443,
        icon="mdi:nas",
        group="Servers",
        warning_latency_ms=50,
        critical_latency_ms=200,
    ),
    "web": TargetPreset(
        key="web",
        name="HTTPS service",
        port=443,
        icon="mdi:web",
        group="WAN",
        warning_latency_ms=250,
        critical_latency_ms=750,
    ),
    "dns": TargetPreset(
        key="dns",
        name="DNS service (TCP)",
        port=53,
        icon="mdi:dns",
        group="DNS",
        warning_latency_ms=100,
        critical_latency_ms=300,
        timeout=2.0,
        retries=2,
    ),
    "home_assistant": TargetPreset(
        key="home_assistant",
        name="Home Assistant",
        port=8123,
        icon="mdi:home-assistant",
        group="Home Automation",
        warning_latency_ms=75,
        critical_latency_ms=250,
    ),
    "proxmox": TargetPreset(
        key="proxmox",
        name="Proxmox VE",
        port=8006,
        icon="mdi:server-network",
        group="Servers",
        warning_latency_ms=75,
        critical_latency_ms=250,
    ),
    "ssh": TargetPreset(
        key="ssh",
        name="SSH service",
        port=22,
        icon="mdi:console-network",
        group="Servers",
        warning_latency_ms=100,
        critical_latency_ms=300,
    ),
    "smtp": TargetPreset(
        key="smtp",
        name="SMTP service",
        port=25,
        icon="mdi:email-fast",
        group="Mail",
        warning_latency_ms=250,
        critical_latency_ms=750,
    ),
}


def get_preset(key: str) -> TargetPreset:
    """Return a preset, falling back to generic safely."""
    return PRESETS.get(key, PRESETS["generic"])
