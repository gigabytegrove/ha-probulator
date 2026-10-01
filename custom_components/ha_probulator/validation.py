"""Input validation and normalization for HA Probulator."""

from __future__ import annotations

from ipaddress import ip_address
import re
from typing import Any

from .const import (
    MAX_GROUP_LENGTH,
    MAX_HOST_LENGTH,
    MAX_NAME_LENGTH,
    MAX_PROBE_CYCLE_SECONDS,
)

_HOST_LABEL = re.compile(r"^[A-Za-z0-9_](?:[A-Za-z0-9_-]{0,61}[A-Za-z0-9_])?$")
_FORBIDDEN_HOST_CHARS = frozenset("/\\?#@,;")


class ValidationError(ValueError):
    """Validation error with a translation-safe error code."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _clean_text(value: Any) -> str:
    """Strip user text and reject control characters."""
    text = str(value or "").strip()
    if any(ord(char) < 32 or ord(char) == 127 for char in text):
        raise ValidationError("invalid_text")
    return text


def normalize_name(value: Any) -> str:
    """Normalize and validate a friendly target name."""
    name = _clean_text(value)
    if not name:
        raise ValidationError("required")
    if len(name) > MAX_NAME_LENGTH:
        raise ValidationError("name_too_long")
    return name


def normalize_group(value: Any) -> str:
    """Normalize and validate an optional group label."""
    group = _clean_text(value)
    if len(group) > MAX_GROUP_LENGTH:
        raise ValidationError("group_too_long")
    return group


def normalize_host(value: Any) -> str:
    """Normalize an IPv4/IPv6 address or DNS host without resolving it.

    Host resolution is intentionally not performed during setup so an offline target
    can still be configured for monitoring.
    """
    host = _clean_text(value)
    if not host:
        raise ValidationError("required")
    if host.startswith("[") and host.endswith("]"):
        host = host[1:-1].strip()

    if not host or len(host) > MAX_HOST_LENGTH:
        raise ValidationError("host_too_long" if host else "required")
    if "://" in host or any(char in host for char in _FORBIDDEN_HOST_CHARS):
        raise ValidationError("invalid_host")
    if any(char.isspace() for char in host):
        raise ValidationError("invalid_host")

    try:
        return ip_address(host).compressed
    except ValueError:
        pass

    # Do not reinterpret a malformed dotted-quad as a DNS name. This avoids
    # platform-dependent legacy numeric-address parsing (for example leading zeros).
    if host.count(".") == 3 and all(
        label.isdigit() for label in host.split(".")
    ):
        raise ValidationError("invalid_host")

    # A colon that is not part of a valid IP address usually means host:port or an
    # invalid IPv6 literal. Port is configured separately.
    if ":" in host:
        raise ValidationError("invalid_host")

    if host.endswith("."):
        host = host[:-1]
    if not host:
        raise ValidationError("invalid_host")

    try:
        ascii_host = host.encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise ValidationError("invalid_host") from exc

    if len(ascii_host) > MAX_HOST_LENGTH:
        raise ValidationError("host_too_long")

    labels = ascii_host.split(".")
    if any(not label or len(label) > 63 or not _HOST_LABEL.fullmatch(label) for label in labels):
        raise ValidationError("invalid_host")

    return ascii_host


def validate_probe_budget(*, timeout: float, retries: int, retry_delay: float) -> None:
    """Reject configurations that can monopolize one coordinator for too long."""
    worst_case = ((retries + 1) * timeout) + (retries * retry_delay)
    if worst_case > MAX_PROBE_CYCLE_SECONDS:
        raise ValidationError("probe_budget_too_large")


def format_target(host: str, port: int) -> str:
    """Return an unambiguous host:port display string, including IPv6 brackets."""
    display_host = f"[{host}]" if ":" in host and not host.startswith("[") else host
    return f"{display_host}:{port}"
