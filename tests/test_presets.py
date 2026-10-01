"""Tests for HA Probulator role presets."""

import unittest

from _bootstrap import presets


class PresetTests(unittest.TestCase):
    def test_known_home_assistant_preset(self) -> None:
        preset = presets.get_preset("home_assistant")
        self.assertEqual(preset.port, 8123)
        self.assertEqual(preset.icon, "mdi:home-assistant")
        self.assertEqual(preset.group, "Home Automation")

    def test_unknown_preset_falls_back_to_generic(self) -> None:
        self.assertEqual(
            presets.get_preset("definitely-not-real"),
            presets.PRESETS["generic"],
        )

    def test_all_presets_have_valid_tcp_ports_and_thresholds(self) -> None:
        for preset in presets.PRESETS.values():
            with self.subTest(preset=preset.key):
                self.assertGreaterEqual(preset.port, 1)
                self.assertLessEqual(preset.port, 65535)
                self.assertLess(
                    preset.warning_latency_ms,
                    preset.critical_latency_ms,
                )


if __name__ == "__main__":
    unittest.main()
