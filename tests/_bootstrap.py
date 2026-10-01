"""Import pure HA Probulator modules without requiring Home Assistant in unit tests."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
CUSTOM_COMPONENTS = ROOT / "custom_components"
DOMAIN_DIR = CUSTOM_COMPONENTS / "ha_probulator"

if "custom_components" not in sys.modules:
    package = ModuleType("custom_components")
    package.__path__ = [str(CUSTOM_COMPONENTS)]
    sys.modules["custom_components"] = package

if "custom_components.ha_probulator" not in sys.modules:
    package = ModuleType("custom_components.ha_probulator")
    package.__path__ = [str(DOMAIN_DIR)]
    sys.modules["custom_components.ha_probulator"] = package

probe = importlib.import_module("custom_components.ha_probulator.probe")
metrics = importlib.import_module("custom_components.ha_probulator.metrics")
validation = importlib.import_module("custom_components.ha_probulator.validation")
