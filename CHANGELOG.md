# Changelog

## 1.2.0 - 2026-10-01

Operational intelligence and large-installation polish.

- Added role-based setup presets for routers, switches, servers, NAS, HTTPS, DNS, Home Assistant, Proxmox VE, SSH, SMTP, and generic TCP targets.
- Added persistent native Monitoring and Maintenance switches without deleting/recreating config entries.
- Added timed maintenance and administrator-only Probe, Set monitoring, Start maintenance, and End maintenance Home Assistant actions with target/group/all scoping.
- Added target dependency relationships, dependency-loop prevention, dependency-offline status, dependent refresh propagation, and a Home Assistant Repairs warning for missing dependencies.
- Added rolling flap detection, the Unstable status, a native Flapping binary sensor, and transition/window diagnostics.
- Added adaptive polling with separate healthy/degraded/offline intervals.
- Added deterministic startup staggering and a shared 20-probe concurrency limiter for large installations.
- Added hidden probe-cycle and queue-wait diagnostic sensors for runtime self-health.
- Persisted lifetime probe counters, last success/failure, last outage duration, maintenance state, and monitoring enabled state across Home Assistant restarts.
- Added a status-aware HA Probulator Manager dashboard card with live search, group filtering, and per-target operational controls.
- Added multi-select bulk Probe, Maintenance, End maintenance, Enable, and Disable operations to the Manager card.
- Expanded cards for maintenance, disabled, dependency-offline, and unstable states.
- Added frontend/backend version handshake and a cache-busted resource URL keyed to the integration version.
- Added reduced-motion support and hostile target-text rendering tests.
- Added explicit config-entry migration to the 1.2 schema while preserving existing target IDs/entity identities.
- Added administrator-only portable clone/import/export actions with dependency remapping and normal config-flow validation.
- Added non-invasive target suggestions from network-address attributes already known to Home Assistant; no subnet or port scan is performed.
- Added native Overall and per-group aggregate devices with Healthy, Availability, and Average response time entities.
- Removed the redundant default `HA Probulator` heading from Overview cards, including legacy saved defaults, while preserving explicitly customized titles.
- Switched dashboard cards to Home Assistant's natural Section-grid height so cards no longer reserve large empty row blocks below their rendered content.

## 1.1.0 - 2026-10-01

Hardening, observability, and distribution pass.

- Added strict host/name/group normalization without requiring the target to be online during setup.
- Added IPv4/IPv6/IDNA handling and unambiguous bracketed IPv6 host:port presentation.
- Rejected URLs, embedded ports, control characters, malformed numeric IPv4-like targets, and oversized input.
- Added a 60-second worst-case probe-cycle budget to prevent pathological timeout/retry configurations.
- Replaced raw operating-system exception strings with stable probe failure categories.
- Preserved task cancellation correctly and enabled Happy Eyeballs connection behavior for dual-stack hostnames.
- Added p95 response time, last check, last status change, successful/failed probe counters, and current/last outage duration.
- Added rolling TCP latency jitter as a native Home Assistant sensor, attribute, and optional card metric.
- Expanded `ha_probulator_status_changed` event data with stable target IDs, p95 latency, sanitized failure category, and check timestamp.
- Redacted monitored hosts/targets from Home Assistant diagnostics intended for sharing.
- Added monitoring customization during initial target setup instead of silently forcing defaults.
- Fixed duplicate detection during reconfiguration when only the friendly name changes.
- Improved custom cards with status-first sorting, IPv6-safe target display, p95 latency, check/status timestamps, outage duration, and keyboard behavior.
- Added native visual editors for Target, Overview, and Summary cards, including metric visibility and common theme controls.
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
