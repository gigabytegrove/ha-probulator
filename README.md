# HA Probulator

**LAN, WAN, and TCP service availability monitoring for Home Assistant.**

HA Probulator monitors TCP endpoints directly from Home Assistant and exposes the results as ordinary Home Assistant devices and entities. Its custom dashboard cards are optional: the same reachability, latency, reliability, and state data can be used with built-in cards, templates, automations, history, and third-party dashboards.

The name is intentionally a little ridiculous. The monitoring is not.

## What it does

- Monitors a host/IP plus TCP port from Home Assistant itself.
- Does **not** depend on ICMP/ping, so devices that ignore ping can still be monitored.
- Requires no external monitoring server, daemon, database, or Uptime Kuma installation.
- Configures targets entirely through the Home Assistant UI, including role-based setup presets.
- Supports retries, connection timeouts, failure/recovery debounce thresholds, adaptive polling, dependency relationships, and configurable polling intervals.
- Tracks current, average, minimum, maximum, 95th-percentile response time, and TCP latency jitter.
- Tracks rolling probe success rate, probe counters, status-change times, and outage duration.
- Exposes target state as normal Home Assistant entities and attributes.
- Includes an immediate **Probe now** button for every target.
- Includes optional HA Probulator dashboard cards with Home Assistant theme support.
- Groups targets for filtered overview/summary/manager cards and group-targeted actions.
- Fires `ha_probulator_status_changed` for effective target state changes, including degraded, unstable, offline, dependency-offline, disabled, and maintenance-aware transitions.
- Provides Home Assistant diagnostics for each target.

## Installation

[![Open your Home Assistant instance and open HA Probulator in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=gigabytegrove&repository=ha-probulator&category=integration)

### HACS custom repository

1. In HACS, open **Integrations**.
2. Add `https://github.com/gigabytegrove/ha-probulator` as a custom repository in the **Integration** category.
3. Install **HA Probulator**.
4. Restart Home Assistant.
5. Open **Settings → Devices & services → Add integration** and search for **HA Probulator**.

### Manual

Copy:

```text
custom_components/ha_probulator
```

to:

```text
/config/custom_components/ha_probulator
```

Restart Home Assistant, then add HA Probulator from **Settings → Devices & services**.

## Adding a target

Each HA Probulator config entry represents one monitored TCP endpoint. Setup first asks for a target role preset such as **Router / gateway**, **Network switch**, **Server**, **NAS**, **HTTPS**, **DNS**, **Home Assistant**, **Proxmox VE**, **SSH**, or **SMTP**. The preset only supplies suggestions; every value remains editable.

Then enter:

- **Name** — friendly device name in Home Assistant.
- **Host or IP address** — for example `192.168.1.1`, `nas.local`, or `1.1.1.1`.
- **TCP port** — the service HA Probulator should connect to.

The target does not need to be online while you add it. HA Probulator is specifically intended to monitor failures, so setup does not reject an endpoint merely because it is currently unavailable.

Setup then includes a **Monitoring options** step so the polling interval, retry/debounce behavior, dependency, adaptive polling, flap detection, thresholds, group, and icon can be customized before the target is created. After setup, use **Configure** to adjust those monitoring options and **Reconfigure** to change the target name, host, or port.

## Monitoring options

| Option | Default | Purpose |
| --- | ---: | --- |
| Probe interval | 30 s | Normal healthy-target probe interval |
| Adaptive polling | enabled | Probe unhealthy targets more aggressively |
| Degraded interval | 10 s | Interval while degraded, unstable, or probing |
| Offline interval | 15 s | Interval while offline |
| Connection timeout | 3.0 s | Maximum time allowed for each TCP attempt |
| Retries | 1 | Additional attempts during the same probe cycle |
| Retry delay | 0.25 s | Delay between retry attempts |
| Failures before offline | 2 | Debounce threshold before marking the target offline |
| Successes before recovery | 1 | Debounce threshold before marking the target online |
| Warning latency | 150 ms | Response time considered degraded |
| Critical latency | 500 ms | Response time considered critical/degraded |
| Statistics window | 120 probes | Rolling sample count used for latency and success-rate statistics |
| Flap window | 10 probes | Recent results used for instability detection |
| Flap threshold | 4 transitions | Changes required to mark a target unstable |
| Depends on | none | Optional upstream Probulator target |
| Group | blank | Optional label used by overview/summary/manager cards |

HA Probulator rejects timeout/retry combinations whose theoretical worst-case probe cycle exceeds 60 seconds. This prevents a single misconfigured target from tying up its coordinator for minutes at a time.

## Home Assistant entities

Every target is represented as a Home Assistant device. Entity IDs are generated normally by Home Assistant from the device/entity names, so a target named `Core Router` will typically produce entities similar to:

```text
binary_sensor.core_router_reachable
binary_sensor.core_router_flapping
sensor.core_router_response_time
sensor.core_router_average_response_time
sensor.core_router_95th_percentile_response_time
sensor.core_router_jitter
sensor.core_router_minimum_response_time
sensor.core_router_maximum_response_time
sensor.core_router_success_rate
sensor.core_router_consecutive_failures
sensor.core_router_last_check
sensor.core_router_current_outage_duration
sensor.core_router_status
sensor.core_router_quality
button.core_router_probe_now
switch.core_router_monitoring
switch.core_router_maintenance_mode
```

Additional diagnostic entities such as total probes, last success, and last failure are created disabled by default and can be enabled from the device page.

### Reachability attributes

The primary `binary_sensor.*_reachable` entity also exposes the values most useful to templates, automations, and HA Probulator cards:

```text
host
port
group
status
underlying_status
monitoring_enabled
maintenance
maintenance_until
dependency_target_id
dependency_name
dependency_status
quality
flapping
flap_transitions
response_time_ms
average_response_time_ms
p95_response_time_ms
jitter_ms
min_response_time_ms
max_response_time_ms
success_rate
consecutive_failures
consecutive_successes
total_probes
successful_probes
failed_probes
last_check
last_status_change
last_success
last_failure
outage_started
current_outage_duration_seconds
last_outage_duration_seconds
last_error
attempts
scan_interval
current_scan_interval
adaptive_polling
degraded_scan_interval
offline_scan_interval
probe_cycle_ms
probe_queue_wait_ms
initial_stagger_seconds
timeout
retries
failure_threshold
recovery_threshold
warning_latency_ms
critical_latency_ms
latency_history
```

`probulator: true` and `probulator_kind: target` are also exposed so cards can safely discover HA Probulator targets without relying on entity naming.

## Native group and overall health

HA Probulator automatically creates virtual aggregate devices for **Overall** and for every non-empty target group. Each aggregate device exposes normal Home Assistant entities:

```text
binary_sensor.ha_probulator_overall_healthy
sensor.ha_probulator_overall_availability
sensor.ha_probulator_overall_average_response_time
```

Named groups receive the same three entities. Group health ignores targets intentionally placed in Maintenance or disabled monitoring, while still exposing those counts as attributes. Availability is the average rolling success rate of active group members.

## Built-in Home Assistant cards

Custom cards are optional. HA Probulator works normally with built-in Home Assistant cards.

### Tile

```yaml
type: tile
entity: binary_sensor.core_router_reachable
name: Core Router
```

### Gauge

```yaml
type: gauge
entity: sensor.core_router_success_rate
name: Router availability
min: 0
max: 100
```

### Statistics graph

```yaml
type: statistics-graph
entities:
  - sensor.core_router_response_time
stat_types:
  - mean
  - min
  - max
```

## Custom cards

### Responsive Sections sizing

HA Probulator cards understand Home Assistant's current Sections grid sizing contract. Target cards default to a two-column-friendly width but expose a 3–12 column resize range; Summary cards expose 6–12 columns; Overview and Manager default to a full Section row.

The card internals use CSS container queries, so layout is based on the **actual width Home Assistant gives the card**, not the browser width. Names, target addresses, groups, metrics, status pills, and Extended details reflow instead of being clipped on narrow cards.

Home Assistant Sections itself is row-based rather than masonry. A short card placed beside a much taller card will keep the next grid row below the taller card. For that reason Overview and Manager intentionally default to full width; you can still resize them manually if you prefer a mixed-height row.

The dashboard card bundle is shipped inside the integration and registered automatically when Home Assistant loads HA Probulator. No separate card repository is required. All four cards now include visual Home Assistant card editors, so their common settings can be configured from the dashboard UI instead of requiring YAML.

### Target card

```yaml
type: custom:probulator-card
entity: binary_sensor.core_router_reachable
mode: normal
```

Supported modes:

- `minimal` — name/status and current response time.
- `normal` — status plus current/average response time and success rate.
- `extended` — the full target view, including host/port, group, min/p95/max response time, jitter, failure information, last check/status change, outage duration, timestamps, sanitized last-error category, and a recent latency sparkline.

The visual editor can select the target, mode, icon/name overrides, individual metric visibility, sparkline visibility, and common theme overrides.

Optional presentation overrides:

```yaml
type: custom:probulator-card
entity: binary_sensor.core_router_reachable
mode: extended
name: Internet Edge
icon: mdi:router-network
show_response: true
show_average: true
show_success: true
show_p95: true
show_jitter: true
show_sparkline: true
online_color: "#00c853"
degraded_color: "#ffab00"
offline_color: "#d50000"
```

### Overview card

Auto-discovers every HA Probulator target:

Overview cards do not add a product-name heading by default. Set `title:` only when you actually want an internal card title. Legacy cards that saved the old default `HA Probulator` title automatically suppress it.


```yaml
type: custom:probulator-overview-card
title: Network
sort: status
```

`sort: status` (the default) puts offline and degraded targets first. Use `sort: name` for alphabetical ordering.

Filter by group:

```yaml
type: custom:probulator-overview-card
title: Core Network
group: Core
```

Or explicitly choose targets:

```yaml
type: custom:probulator-overview-card
title: WAN Services
entities:
  - binary_sensor.primary_dns_reachable
  - binary_sensor.secondary_dns_reachable
```

### Summary card

```yaml
type: custom:probulator-summary-card
title: Network status
```

Or summarize one group:

```yaml
type: custom:probulator-summary-card
title: Servers
group: Servers
```


### Manager card

The Manager card is the operational surface for larger installations:

```yaml
type: custom:probulator-manager-card
title: HA Probulator Manager
sort: status
show_actions: true
```

It supports live search, group filtering, status-first sorting, per-target **Probe**, **Maintenance**, and **Enable/Disable** actions, plus multi-select bulk operations with **Select visible**, **Probe**, **Maintenance**, **End maintenance**, **Enable**, and **Disable**. Those buttons call HA Probulator's native administrator-only Home Assistant actions; the card is not maintaining a separate state model.

## Themes

HA Probulator cards inherit the active Home Assistant theme. They also expose CSS variables that can be placed in any Home Assistant theme:

```yaml
Probulator Dark:
  probulator-online-color: "#37d67a"
  probulator-degraded-color: "#f5b642"
  probulator-offline-color: "#ef5350"
  probulator-unknown-color: "#90a4ae"
  probulator-card-background: "var(--ha-card-background)"
  probulator-card-border-radius: "14px"
  probulator-gap: "12px"
  probulator-metric-font-size: "1.25rem"
```

The matching CSS custom properties are:

```text
--probulator-online-color
--probulator-degraded-color
--probulator-offline-color
--probulator-unknown-color
--probulator-card-background
--probulator-card-border-radius
--probulator-gap
--probulator-metric-font-size
```

Card-level color/background overrides take precedence over theme defaults where supplied.


## Operational intelligence

### Maintenance mode

Every target has a native **Maintenance mode** switch. Maintenance mode continues collecting probes and statistics but suppresses normal operational status transitions. It can also be started for a fixed duration through the `ha_probulator.start_maintenance` action.

### Monitoring enable/disable

Every target has a native **Monitoring** switch. Turning monitoring off stops active TCP probes without deleting the target or losing its configuration. The effective status becomes `disabled`.

### Dependencies

A target can depend on another HA Probulator target. If the upstream target is unavailable, the dependent target becomes `dependency_offline` rather than looking like an unrelated outage. Configuration prevents dependency loops, and Home Assistant Repairs warns if a configured dependency later disappears.

### Flapping / instability

HA Probulator can detect repeated success/failure changes inside a configurable rolling window. A reachable target that crosses the flap threshold becomes `unstable`, and `binary_sensor.*_flapping` is available for automations.

### Adaptive polling and scale

Healthy targets use their normal interval. Degraded, unstable, probing, and offline targets can temporarily use shorter intervals. Initial probes are deterministically staggered, and a shared concurrency semaphore prevents large installations from launching an unbounded number of TCP connection attempts at once.

Hidden diagnostic sensors can expose probe-cycle duration and queue wait, making it possible to see when the Home Assistant host itself is becoming a monitoring bottleneck.

## Home Assistant actions

HA Probulator registers administrator-only actions:

- `ha_probulator.probe`
- `ha_probulator.set_monitoring`
- `ha_probulator.start_maintenance`
- `ha_probulator.end_maintenance`
- `ha_probulator.clone_target`
- `ha_probulator.export_config`
- `ha_probulator.import_config`
- `ha_probulator.suggest_targets`

Each action can target a stable Probulator target ID, a group, or—when both are omitted—all loaded targets.

### Portable configuration

`ha_probulator.export_config` returns both a structured bundle and formatted JSON. The bundle excludes Home Assistant config-entry IDs and uses temporary portable references for dependency relationships.

`ha_probulator.import_config` recreates targets through the same hardened config flow used by manual setup, generates fresh local target IDs, and reconnects dependency relationships after creation.

`ha_probulator.clone_target` copies one target's monitoring behavior to a new name/host/port while deliberately clearing the dependency until you explicitly choose one.

### Safe target suggestions

`ha_probulator.suggest_targets` inspects host/IP-like attributes already present in Home Assistant state data and returns candidate targets. It **does not scan the LAN, sweep ports, or open any connection**. Suggestions indicate whether the exact host/port is already monitored.

## Automations and templates

Because HA Probulator uses normal Home Assistant entities, no special automation syntax is required.

### Trigger when a target remains offline

```yaml
triggers:
  - trigger: state
    entity_id: binary_sensor.core_router_reachable
    to: "off"
    for: "00:02:00"
```

### Trigger on poor rolling success rate

```yaml
triggers:
  - trigger: numeric_state
    entity_id: sensor.core_router_success_rate
    below: 95
```

### Use a card/automation attribute in a template

```jinja2
{{ state_attr('binary_sensor.core_router_reachable', 'response_time_ms') }}
```

### Status-change event

HA Probulator also emits:

```text
ha_probulator_status_changed
```

Event data contains a stable target ID, config entry ID, target name/address, group, previous/new status, quality, current and p95 response time, rolling success rate, consecutive failure count, sanitized failure category, and check timestamp.

## Status behavior

HA Probulator separates an individual failed probe from the debounced target state.

For example, with the default failure threshold of `2`:

1. The first failed probe cycle changes the reported status to `degraded`, but the reachability binary sensor remains on.
2. A second consecutive failed probe cycle changes the target to `offline` and the reachability binary sensor turns off.
3. A successful probe recovers the target according to the configured recovery threshold.

Latency at or above the warning/critical thresholds also produces a `degraded` status while the target remains reachable.

## Probe model

HA Probulator 1.2 uses TCP connection probes. A successful TCP connection proves that Home Assistant can reach the configured service port; it does not assert that the application protocol behind that port is healthy.

This is deliberate. TCP monitoring is small, local, predictable, and works with devices that do not answer ICMP echo requests.

## Privacy and network behavior

HA Probulator runs entirely inside Home Assistant. It does not send monitoring data to Gigabyte Grove or any third-party service. It only attempts TCP connections to the targets you configure.

Host names and IP addresses are redacted from Home Assistant diagnostics intended for sharing. Probe failures are exposed as stable categories such as `timeout`, `dns_error`, or `connection_refused`; raw operating-system exception text is not placed into entity attributes or dashboard cards.

## Development

Validation includes:

- Python bytecode compilation.
- Unit tests for retry/cancellation/error classification, input hardening, IPv4/IPv6/IDNA handling, debounce/outage behavior, and rolling statistics.
- JSON validation.
- JavaScript syntax validation.
- Executable frontend registration and hostile-text rendering smoke tests.
- Backend/frontend/manifest version synchronization checks.
- Home Assistant Hassfest.
- HACS integration validation.

## License

MIT. See [LICENSE](LICENSE).

## Release integrity

Tagged releases are built only when the tag version matches the integration manifest. The release workflow produces a deterministic `ha-probulator-vX.Y.Z.zip` and a `SHA256SUMS` file so manual downloads can be verified.

CI dependencies are pinned to immutable commit SHAs and Dependabot is configured to propose updates rather than silently following moving action branches.
