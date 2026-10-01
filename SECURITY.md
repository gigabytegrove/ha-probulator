# Security Policy

Please do not publish security vulnerabilities in a public issue.

Use GitHub private vulnerability reporting when it is enabled for this repository. If private reporting is not available, contact the repository owner privately before disclosing details publicly.

## Security boundaries

HA Probulator intentionally performs outbound TCP connection attempts to user-configured hosts and ports from the Home Assistant host. Only Home Assistant administrators should be permitted to create or reconfigure HA Probulator targets.

HA Probulator:

- does not execute application data returned by a monitored service;
- does not require or store credentials for monitored TCP services;
- does not transmit monitoring data to Gigabyte Grove or another telemetry service;
- redacts monitored host/target values from shareable diagnostics;
- exposes stable failure categories instead of raw operating-system exception text;
- bounds configuration input and rejects probe settings that can exceed a 60-second theoretical probe cycle;
- preserves asyncio cancellation so shutdown/reload operations cannot be trapped in retry handling.

As with any network-monitoring integration, an administrator can intentionally configure connections to services reachable from the Home Assistant host. Treat Home Assistant administrative access as trusted.

## Dependencies and CI

The integration has no third-party Python runtime dependencies. GitHub Actions used by the repository are pinned to immutable commit SHAs, and Dependabot is configured to propose action updates.
