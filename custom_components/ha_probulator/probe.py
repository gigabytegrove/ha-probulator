"""TCP probing primitives for HA Probulator."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class ProbeSample:
    """One completed probe cycle."""

    timestamp: datetime
    success: bool
    latency_ms: float | None
    attempts: int
    error: str | None = None


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
                asyncio.open_connection(host=host, port=port), timeout=timeout
            )
            latency_ms = round((loop.time() - started) * 1000.0, 3)
            return ProbeSample(
                timestamp=datetime.now(timezone.utc),
                success=True,
                latency_ms=latency_ms,
                attempts=attempt,
            )
        except (TimeoutError, asyncio.TimeoutError, OSError) as exc:
            message = str(exc).strip()
            last_error = type(exc).__name__ + (f": {message}" if message else "")
        finally:
            if writer is not None:
                writer.close()
                try:
                    await writer.wait_closed()
                except (ConnectionError, OSError):
                    pass

        if attempt < attempts and retry_delay > 0:
            await asyncio.sleep(retry_delay)

    return ProbeSample(
        timestamp=datetime.now(timezone.utc),
        success=False,
        latency_ms=None,
        attempts=attempts,
        error=last_error or "Connection failed",
    )
