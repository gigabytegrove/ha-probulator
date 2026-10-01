# Changelog

## 1.1.0 - 2026-10-01

Hardening, observability, and distribution pass.

- Added strict host/name/group normalization without requiring the target to be online during setup.
- Added IPv4/IPv6/IDNA handling and unambiguous bracketed IPv6 host:port presentation.
- Rejected URLs, embedded ports, control characters, malformed numeric IPv4-like targets, and oversized input.
- Added a 60-second worst-case probe-cycle budget to prevent pathological timeout/retry configurations.
- Replaced raw operating-system exception strings with stable probe failure categories.
- Preserved task cancellation correctly and enabled Happy Eyeballs connection behavior for dual-stack hostnames.
- Added p95 response time, last check, last status change, successful/failed probe counters, and current/last outage duration.
- Expanded `ha_probulator_status_changed` event data with stable target IDs, p95 latency, sanitized failure category, and check timestamp.
- Redacted monitored hosts/targets from Home Assistant diagnostics intended for sharing.
- Added monitoring customization during initial target setup instead of silently forcing defaults.
- Fixed duplicate detection during reconfiguration when only the friendly name changes.
- Improved custom cards with status-first sorting, IPv6-safe target display, p95 latency, check/status timestamps, outage duration, and keyboard behavior.
- Expanded the regression suite for validation, cancellation, failure classification, percentile statistics, debounce behavior, and outage tracking.
- Pinned GitHub Actions to immutable commit SHAs and added Dependabot for action updates.
- Added deterministic tagged-release packaging with manifest/tag verification and SHA-256 checksums.
- Prevented HACS validation from intentionally failing CI while the repository remains private.

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
