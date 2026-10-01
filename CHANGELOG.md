# Changelog

## 1.0.0 - 2026-10-01

Initial HA Probulator release.

- Converted the proven Network Probe concept into a distributable Home Assistant integration.
- Added UI-only target setup, reconfiguration, and monitoring options.
- Added TCP reachability probing with retries, timeouts, and failure/recovery debounce thresholds.
- Added current and rolling latency statistics, success rate, counters, and success/failure timestamps.
- Added native Home Assistant binary sensor, sensor, and manual probe button entities.
- Added diagnostics and `ha_probulator_status_changed` events.
- Added optional bundled Target, Overview, and Summary dashboard cards.
- Preserved Minimal, Normal, and Extended single-target card modes.
- Added theme variables and card-level presentation overrides.
- Added HACS metadata, validation workflow, documentation, and unit tests.
