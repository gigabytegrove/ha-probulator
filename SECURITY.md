# Security Policy

Please do not publish security vulnerabilities in a public issue.

Report security-sensitive problems privately to the repository owner through GitHub's available private security reporting/contact mechanisms.

HA Probulator intentionally performs outbound TCP connection attempts to user-configured hosts and ports. It does not execute data received from those endpoints, does not require remote credentials, and does not transmit monitoring data to Gigabyte Grove.
