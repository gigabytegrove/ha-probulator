"""Tests for HA Probulator input hardening."""

import unittest

from _bootstrap import validation


class ValidationTests(unittest.TestCase):
    def test_ipv4_is_normalized(self) -> None:
        self.assertEqual(validation.normalize_host(" 192.168.1.1 "), "192.168.1.1")

    def test_ambiguous_ipv4_with_leading_zeroes_is_rejected(self) -> None:
        with self.assertRaisesRegex(validation.ValidationError, "invalid_host"):
            validation.normalize_host("192.168.001.001")

    def test_ipv6_brackets_are_removed_and_display_is_unambiguous(self) -> None:
        host = validation.normalize_host("[2001:db8::1]")
        self.assertEqual(host, "2001:db8::1")
        self.assertEqual(validation.format_target(host, 443), "[2001:db8::1]:443")

    def test_dns_name_is_idna_normalized(self) -> None:
        self.assertEqual(validation.normalize_host("BÜCHER.Example."), "xn--bcher-kva.example")

    def test_url_is_rejected(self) -> None:
        with self.assertRaisesRegex(validation.ValidationError, "invalid_host"):
            validation.normalize_host("https://example.com")

    def test_host_port_is_rejected(self) -> None:
        with self.assertRaisesRegex(validation.ValidationError, "invalid_host"):
            validation.normalize_host("example.com:443")

    def test_control_characters_are_rejected(self) -> None:
        with self.assertRaisesRegex(validation.ValidationError, "invalid_text"):
            validation.normalize_name("router\nname")

    def test_group_length_is_bounded(self) -> None:
        with self.assertRaisesRegex(validation.ValidationError, "group_too_long"):
            validation.normalize_group("x" * 81)

    def test_probe_budget_accepts_default_shape(self) -> None:
        validation.validate_probe_budget(timeout=3, retries=1, retry_delay=0.25)

    def test_probe_budget_rejects_pathological_cycle(self) -> None:
        with self.assertRaisesRegex(
            validation.ValidationError, "probe_budget_too_large"
        ):
            validation.validate_probe_budget(timeout=30, retries=5, retry_delay=5)

    def test_legacy_retry_count_is_reduced_to_budget(self) -> None:
        self.assertEqual(
            validation.safe_retries_for_budget(
                timeout=30,
                retries=5,
                retry_delay=5,
            ),
            0,
        )
        self.assertEqual(
            validation.safe_retries_for_budget(
                timeout=3,
                retries=1,
                retry_delay=0.25,
            ),
            1,
        )


if __name__ == "__main__":
    unittest.main()
