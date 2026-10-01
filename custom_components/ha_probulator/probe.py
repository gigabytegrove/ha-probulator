"""TCP probing primitives for HA Probulator."""

from __future__ import annotations

import asyncio
import errno
import socket
from contextlib import suppress
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class ProbeError(StrEnum):
    """Stable, non-sensitive probe failure categories."""

    TIMEOUT = "timeout"
    DNS = "dns_error"
    REFUSED = "connection_refused"
    NETWORK_UNREACHABLE = "network_unreachable"
    HOST_UNREACHABLE = "host_unreachable"
    CONNECTION_RESET = "connection_reset"
    INVALID_TARGET = "invalid_target"
    CONNECTION_ERROR = "connection_error"


@dataclass(frozen=True, slots=True)
class ProbeSample:
    """One completed probe cycle."""

    timestamp: datetime
    success: bool
    latency_ms: float | None
    attempts: int
    error: str | None = None


def _classify_error(exc: BaseException) -> str:
    """Convert an exception into a stable error code without leaking raw details."""
    if isinstance(exc, TimeoutError):
        return ProbeError.TIMEOUT
    if isinstance(exc, socket.gaierror):
        return ProbeError.DNS
    if isinstance(exc, ConnectionRefusedError):
        return ProbeError.REFUSED
    if isinstance(exc, ConnectionResetError):
        return ProbeError.CONNECTION_RESET
    if isinstance(exc, (ValueError, UnicodeError)):
        return ProbeError.INVALID_TARGET
    if isinstance(exc, OSError):
        if exc.errno == errno.ENETUNREACH:
            return ProbeError.NETWORK_UNREACHABLE
        if exc.errno == errno.EHOSTUNREACH:
            return ProbeError.HOST_UNREACHABLE
        if exc.errno == errno.ECONNREFUSED:
            return ProbeError.REFUSED
        if exc.errno == errno.ECONNRESET:
            return ProbeError.CONNECTION_RESET
    return ProbeError.CONNECTION_ERROR


async def async_tcp_probe(
    host: str,
    port: int,
    *,
    timeout: float,
    retries: int,
    retry_delay: float,
) -> ProbeSample:
    """Probe a TCP service and return a completed sample.

    A probe succeeds when a TCP connection can be established. It deliberately does
    not use ICMP so targets that ignore ping can still be monitored.
    """

    loop = asyncio.get_running_loop()
    last_error: str | None = None
    attempts = max(1, retries + 1)

    for attempt in range(1, attempts + 1):
        writer: asyncio.StreamWriter | None = None
        started = loop.time()
        try:
            _reader, writer = await asyncio.wait_for(
                asyncio.open_connection(
                    host=host,
                    port=port,
                    happy_eyeballs_delay=0.25,
                    interleave=1,
                ),
                timeout=timeout,
            )
            latency_ms = round((loop.time() - started) * 1000.0, 3)
            return ProbeSample(
                timestamp=datetime.now(UTC),
                success=True,
                latency_ms=latency_ms,
                attempts=attempt,
            )
        except asyncio.CancelledError:
            raise
        except (TimeoutError, OSError, ValueError, UnicodeError) as exc:
            last_error = _classify_error(exc)
        finally:
            if writer is not None:
                writer.close()
                with suppress(ConnectionError, OSError):
                    await writer.wait_closed()

        if attempt < attempts and retry_delay > 0:
            await asyncio.sleep(retry_delay)

    return ProbeSample(
        timestamp=datetime.now(UTC),
        success=False,
        latency_ms=None,
        attempts=attempts,
        error=last_error or ProbeError.CONNECTION_ERROR,
    )
