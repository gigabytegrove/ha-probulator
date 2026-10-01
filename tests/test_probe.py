"""Tests for HA Probulator TCP probe behavior."""

import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from _bootstrap import probe


class _Writer:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True

    async def wait_closed(self) -> None:
        return None


class ProbeTests(IsolatedAsyncioTestCase):
    async def test_success_closes_connection(self) -> None:
        writer = _Writer()

        async def open_ok(*args, **kwargs):
            return object(), writer

        with patch.object(asyncio, "open_connection", open_ok):
            result = await probe.async_tcp_probe(
                "example.invalid",
                443,
                timeout=1,
                retries=0,
                retry_delay=0,
            )

        self.assertTrue(result.success)
        self.assertIsNotNone(result.latency_ms)
        self.assertEqual(result.attempts, 1)
        self.assertTrue(writer.closed)

    async def test_retries_until_success(self) -> None:
        calls = 0
        writer = _Writer()

        async def flaky(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls < 3:
                raise OSError("not yet")
            return object(), writer

        with patch.object(asyncio, "open_connection", flaky):
            result = await probe.async_tcp_probe(
                "example.invalid",
                443,
                timeout=1,
                retries=2,
                retry_delay=0,
            )

        self.assertTrue(result.success)
        self.assertEqual(result.attempts, 3)
        self.assertEqual(calls, 3)

    async def test_exhausted_retries_return_failure(self) -> None:
        async def fail(*args, **kwargs):
            raise OSError("refused")

        with patch.object(asyncio, "open_connection", fail):
            result = await probe.async_tcp_probe(
                "example.invalid",
                443,
                timeout=1,
                retries=1,
                retry_delay=0,
            )

        self.assertFalse(result.success)
        self.assertIsNone(result.latency_ms)
        self.assertEqual(result.attempts, 2)
        self.assertIn("OSError", result.error or "")


if __name__ == "__main__":
    unittest.main()
