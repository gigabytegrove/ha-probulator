"""Ensure release identity stays synchronized across backend and frontend."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class VersionSyncTests(unittest.TestCase):
    def test_manifest_const_and_frontend_versions_match(self) -> None:
        manifest = json.loads(
            (ROOT / "custom_components/ha_probulator/manifest.json").read_text()
        )
        const_text = (ROOT / "custom_components/ha_probulator/const.py").read_text()
        frontend = (
            ROOT / "custom_components/ha_probulator/frontend/ha-probulator-cards.js"
        ).read_text()

        const_match = re.search(r'^VERSION = "([^"]+)"$', const_text, re.MULTILINE)
        frontend_match = re.search(
            r'^const PROBULATOR_FRONTEND_VERSION = "([^"]+)";$',
            frontend,
            re.MULTILINE,
        )

        self.assertIsNotNone(const_match)
        self.assertIsNotNone(frontend_match)
        self.assertEqual(manifest["version"], const_match.group(1))
        self.assertEqual(manifest["version"], frontend_match.group(1))


if __name__ == "__main__":
    unittest.main()
