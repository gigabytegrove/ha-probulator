const PROBULATOR_FRONTEND_VERSION = "1.2.2";

const PROBULATOR_STYLE = `
  :host {
    --probulator-online-color: var(--success-color, #43a047);
    --probulator-degraded-color: var(--warning-color, #f9a825);
    --probulator-offline-color: var(--error-color, #d32f2f);
    --probulator-unstable-color: var(--warning-color, #fb8c00);
    --probulator-maintenance-color: var(--primary-color, #039be5);
    --probulator-dependency-color: var(--error-color, #d32f2f);
    --probulator-disabled-color: var(--secondary-text-color, #757575);
    --probulator-unknown-color: var(--secondary-text-color, #757575);
    --probulator-card-background: var(--ha-card-background, var(--card-background-color, #fff));
    --probulator-card-border-radius: var(--ha-card-border-radius, 12px);
    --probulator-gap: 12px;
    --probulator-metric-font-size: 1.25rem;
    --probulator-card-padding: 16px;
    --probulator-row-gap: 10px;
    --probulator-field-gap: 10px;
    display: block;
    min-width: 0;
    container-type: inline-size;
  }
  ha-card {
    overflow: hidden;
    min-width: 0;
    width: 100%;
    box-sizing: border-box;
    background: var(--probulator-card-background);
    border-radius: var(--probulator-card-border-radius);
  }
  .wrap { padding: var(--probulator-card-padding); min-width:0; box-sizing:border-box; }
  .header { display:flex; align-items:center; gap:10px; min-width:0; }
  .grow { flex:1; min-width:0; }
  .name { font-weight:600; min-width:0; overflow-wrap:anywhere; }
  .sub { color:var(--secondary-text-color); font-size:.82rem; min-width:0; overflow-wrap:anywhere; }
  .status { display:flex; align-items:center; gap:7px; font-size:.86rem; text-transform:capitalize; white-space:nowrap; }
  .dot { width:10px; height:10px; border-radius:50%; background:var(--probulator-unknown-color); box-shadow:0 0 0 3px color-mix(in srgb, var(--probulator-unknown-color) 18%, transparent); }
  .online .dot { background:var(--probulator-online-color); box-shadow:0 0 0 3px color-mix(in srgb, var(--probulator-online-color) 18%, transparent); }
  .degraded .dot { background:var(--probulator-degraded-color); box-shadow:0 0 0 3px color-mix(in srgb, var(--probulator-degraded-color) 18%, transparent); }
  .offline .dot, .dependency_offline .dot { background:var(--probulator-offline-color); box-shadow:0 0 0 3px color-mix(in srgb, var(--probulator-offline-color) 18%, transparent); }
  .unstable .dot { background:var(--probulator-unstable-color); box-shadow:0 0 0 3px color-mix(in srgb, var(--probulator-unstable-color) 18%, transparent); }
  .maintenance .dot { background:var(--probulator-maintenance-color); box-shadow:0 0 0 3px color-mix(in srgb, var(--probulator-maintenance-color) 18%, transparent); }
  .disabled .dot { background:var(--probulator-disabled-color); box-shadow:0 0 0 3px color-mix(in srgb, var(--probulator-disabled-color) 18%, transparent); }
  .metric-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:var(--probulator-gap); margin-top:14px; }
  .metric { min-width:0; }
  .metric .value { font-size:var(--probulator-metric-font-size); font-weight:600; line-height:1.2; min-width:0; overflow-wrap:anywhere; }
  .metric .label { margin-top:2px; color:var(--secondary-text-color); font-size:.75rem; }
  .details { display:grid; grid-template-columns:max-content 1fr; column-gap:12px; row-gap:7px; margin-top:16px; font-size:.84rem; }
  .details .label { color:var(--secondary-text-color); }
  .details .value { min-width:0; overflow-wrap:anywhere; }
  .minimal { padding:12px 14px; }
  .minimal .latency { margin-left:auto; font-weight:600; }
  .spark { height:44px; margin-top:14px; width:100%; }
  .spark svg { display:block; width:100%; height:44px; overflow:visible; }
  .spark polyline { fill:none; stroke:var(--primary-color); stroke-width:2; vector-effect:non-scaling-stroke; }
  .empty { color:var(--secondary-text-color); padding:18px; }
  .targets { display:grid; gap:10px; }
  .target-row { display:grid; grid-template-columns:minmax(0,1fr) auto auto; gap:12px; align-items:center; padding:10px 0; border-top:1px solid var(--divider-color); cursor:pointer; }
  .target-row:first-child { border-top:0; }
  .custom-target-row { display:block; }
  .custom-target-row .custom-layout { width:100%; }
  .target-name { min-width:0; overflow-wrap:anywhere; }
  .pill { border-radius:999px; padding:3px 8px; font-size:.76rem; text-transform:capitalize; background:color-mix(in srgb, var(--secondary-text-color) 10%, transparent); }
  .pill.online { color:var(--probulator-online-color); }
  .pill.degraded { color:var(--probulator-degraded-color); }
  .pill.offline, .pill.dependency_offline { color:var(--probulator-offline-color); }
  .pill.unstable { color:var(--probulator-unstable-color); }
  .pill.maintenance { color:var(--probulator-maintenance-color); }
  .pill.disabled { color:var(--probulator-disabled-color); }
  .manager-toolbar { display:grid; grid-template-columns:minmax(0,1fr) minmax(140px,220px); gap:10px; margin:14px 0; }
  .manager-input, .manager-select { box-sizing:border-box; width:100%; min-height:40px; border:1px solid var(--divider-color); border-radius:10px; background:var(--card-background-color); color:var(--primary-text-color); padding:8px 10px; font:inherit; }
  .manager-row { display:grid; grid-template-columns:auto minmax(0,1.5fr) minmax(90px,.6fr) minmax(78px,.5fr) minmax(170px,.9fr); gap:12px; align-items:center; padding:11px 0; border-top:1px solid var(--divider-color); }
  .manager-check { width:18px; height:18px; accent-color:var(--primary-color); }
  .manager-bulk { display:flex; gap:7px; align-items:center; flex-wrap:wrap; margin:0 0 12px; }
  .manager-bulk-count { color:var(--secondary-text-color); font-size:.78rem; margin-right:auto; }
  .manager-row[hidden] { display:none; }
  .manager-metrics { color:var(--secondary-text-color); font-size:.8rem; line-height:1.45; }
  .manager-actions { display:flex; justify-content:flex-end; gap:6px; flex-wrap:wrap; }
  .manager-action { border:1px solid var(--divider-color); border-radius:9px; background:transparent; color:var(--primary-text-color); cursor:pointer; padding:6px 8px; font:inherit; font-size:.76rem; }
  .manager-action:hover { background:color-mix(in srgb, var(--primary-color) 10%, transparent); }
  .manager-action:focus-visible { outline:2px solid var(--primary-color); outline-offset:2px; }
  .manager-info { cursor:pointer; min-width:0; }
  .manager-info:focus-visible { outline:2px solid var(--primary-color); outline-offset:3px; border-radius:4px; }
  .manager-count { color:var(--secondary-text-color); font-size:.78rem; margin-top:10px; }
  .version-warning { margin:12px 0; padding:10px 12px; border-radius:10px; background:color-mix(in srgb, var(--warning-color) 16%, transparent); color:var(--primary-text-color); font-size:.82rem; }
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { scroll-behavior:auto !important; transition:none !important; animation:none !important; }
  }
  .summary { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin-top:14px; }
  .summary-box { padding:12px; border-radius:10px; background:color-mix(in srgb, var(--primary-text-color) 5%, transparent); }
  .summary-box .n { font-size:1.35rem; font-weight:700; }
  .summary-box .l { color:var(--secondary-text-color); font-size:.75rem; margin-top:2px; }
  .footer { color:var(--secondary-text-color); font-size:.78rem; margin-top:12px; }
  .custom-layout { display:grid; gap:var(--probulator-row-gap); min-width:0; }
  .custom-line { display:flex; align-items:center; gap:var(--probulator-field-gap); min-width:0; flex-wrap:wrap; }
  .custom-field { min-width:0; }
  .custom-grow { flex:1 1 auto; }
  .custom-spacer { flex:1 1 20px; min-width:8px; }
  .custom-divider { width:100%; border-top:1px solid var(--divider-color); height:0; }
  .custom-primary { font-weight:600; overflow-wrap:anywhere; }
  .custom-secondary { color:var(--secondary-text-color); font-size:.82rem; overflow-wrap:anywhere; }
  .custom-metric { display:flex; flex-direction:column; min-width:62px; }
  .custom-metric-label { color:var(--secondary-text-color); font-size:.7rem; line-height:1.2; text-transform:uppercase; }
  .custom-metric-value { font-weight:600; line-height:1.25; overflow-wrap:anywhere; }
  .custom-inline { display:flex; align-items:baseline; gap:5px; min-width:0; }
  .custom-inline .custom-metric-label { text-transform:none; }
  .custom-icon { display:flex; align-items:center; justify-content:center; }
  .custom-status { margin-left:0; }
  .custom-warning { color:var(--warning-color); font-size:.76rem; overflow-wrap:anywhere; }
  @container (max-width: 440px) {
    .wrap { padding: min(var(--probulator-card-padding), 12px); }
    .header { align-items:flex-start; flex-wrap:wrap; }
    .header .status { margin-left:auto; }
    .sub { white-space:normal; line-height:1.3; }
    .metric-grid { grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; }
    .summary { grid-template-columns:repeat(2,minmax(0,1fr)); }
    .target-row {
      grid-template-columns:minmax(0,1fr) auto;
      grid-template-areas:
        "info status"
        "latency latency";
      row-gap:6px;
      column-gap:10px;
      align-items:start;
    }
    .target-row .grow { grid-area:info; }
    .target-latency { grid-area:latency; justify-self:start; }
    .target-status { grid-area:status; justify-self:end; }
    .details { grid-template-columns:1fr; row-gap:3px; }
    .details .label { margin-top:7px; font-size:.76rem; }
    .manager-toolbar { grid-template-columns:1fr; }
    .manager-row {
      grid-template-columns:auto minmax(0,1fr) auto;
      grid-template-areas:
        "check info status"
        ". metrics metrics"
        ". actions actions";
      align-items:start;
    }
    .manager-check { grid-area:check; }
    .manager-info { grid-area:info; }
    .manager-metrics { grid-area:metrics; display:block; }
    .manager-row > .pill { grid-area:status; justify-self:end; }
    .manager-actions { grid-area:actions; justify-content:flex-start; }
  }
  @container (max-width: 280px) {
    .metric-grid { grid-template-columns:1fr; }
    .summary { grid-template-columns:1fr; }
    .target-row {
      grid-template-columns:1fr;
      grid-template-areas:
        "info"
        "latency"
        "status";
    }
    .target-status { justify-self:start; }
    .header .status { margin-left:0; width:100%; }
    .minimal { flex-wrap:wrap; }
    .minimal .latency { margin-left:0; width:100%; }
  }
`;

function esc(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function fmtMs(value) {
  const n = Number(value);
  return Number.isFinite(n) ? `${n < 10 ? n.toFixed(1) : Math.round(n)} ms` : "—";
}

function fmtPct(value) {
  const n = Number(value);
  return Number.isFinite(n) ? `${n.toFixed(n >= 99 ? 2 : 1)}%` : "—";
}

function fmtTime(value) {
  if (!value) return "—";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleString();
}

function stateStatus(stateObj) {
  const value = String(stateObj?.attributes?.status || "").toLowerCase();
  if ([
    "online",
    "offline",
    "degraded",
    "probing",
    "unstable",
    "maintenance",
    "dependency_offline",
    "disabled",
  ].includes(value)) return value;
  if (!stateObj) return "probing";
  if (stateObj.state === "on") return "online";
  if (stateObj.state === "off") return "offline";
  return "probing";
}

function frontendVersionWarning(targets) {
  const backend = targets.find((stateObj) => stateObj.attributes?.integration_version)
    ?.attributes?.integration_version;
  if (!backend || backend === PROBULATOR_FRONTEND_VERSION) return "";
  return `<div class="version-warning" role="status">Frontend ${esc(PROBULATOR_FRONTEND_VERSION)} is loaded with backend ${esc(backend)}. Refresh the browser after the integration update.</div>`;
}

function statusLabel(status) {
  return String(status || "unknown").replaceAll("_", " ");
}

function probulatorTargets(hass, config = {}) {
  const requested = Array.isArray(config.entities) && config.entities.length
    ? new Set(config.entities)
    : null;
  const group = String(config.group || "").trim().toLowerCase();
  const targets = Object.values(hass?.states || {})
    .filter((stateObj) => stateObj.entity_id.startsWith("binary_sensor."))
    .filter((stateObj) => stateObj.attributes?.probulator === true)
    .filter((stateObj) => stateObj.attributes?.probulator_kind === "target")
    .filter((stateObj) => !requested || requested.has(stateObj.entity_id))
    .filter((stateObj) => !group || String(stateObj.attributes?.group || "").toLowerCase() === group);

  const byName = (a, b) => String(a.attributes?.target_name || a.attributes?.friendly_name || a.entity_id)
    .localeCompare(String(b.attributes?.target_name || b.attributes?.friendly_name || b.entity_id));
  if (config.sort === "name") return targets.sort(byName);

  const rank = {
    offline: 0,
    dependency_offline: 0,
    unstable: 1,
    degraded: 2,
    maintenance: 3,
    probing: 4,
    disabled: 5,
    online: 6,
  };
  return targets.sort((a, b) => {
    const delta = (rank[stateStatus(a)] ?? 9) - (rank[stateStatus(b)] ?? 9);
    return delta || byName(a, b);
  });
}

function fireMoreInfo(element, entityId) {
  element.dispatchEvent(new CustomEvent("hass-more-info", {
    bubbles: true,
    composed: true,
    detail: { entityId },
  }));
}

function applyInlineTheme(element, config) {
  const map = {
    online_color: "--probulator-online-color",
    degraded_color: "--probulator-degraded-color",
    offline_color: "--probulator-offline-color",
    unstable_color: "--probulator-unstable-color",
    maintenance_color: "--probulator-maintenance-color",
    dependency_color: "--probulator-dependency-color",
    disabled_color: "--probulator-disabled-color",
    unknown_color: "--probulator-unknown-color",
    background: "--probulator-card-background",
    border_radius: "--probulator-card-border-radius",
    metric_font_size: "--probulator-metric-font-size",
    card_padding: "--probulator-card-padding",
    row_gap: "--probulator-row-gap",
    field_gap: "--probulator-field-gap",
  };
  for (const [key, cssVar] of Object.entries(map)) {
    if (config?.[key]) element.style.setProperty(cssVar, config[key]);
    else element.style.removeProperty(cssVar);
  }
}

function fireConfigChanged(element, config) {
  element.dispatchEvent(new CustomEvent("config-changed", {
    bubbles: true,
    composed: true,
    detail: { config },
  }));
}

class ProbulatorFormEditor extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._config = {};
    this._schema = [];
    this._hint = "All fields are optional unless marked required. Changes preview immediately.";
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  setConfig(config) {
    this._config = { ...config };
    this._render();
  }

  configure(schema, labels, hint = null) {
    this._schema = schema;
    this._labels = labels;
    if (hint) this._hint = hint;
    this._render();
  }

  _render() {
    if (!this.shadowRoot || !this._hass || !this._schema.length) return;
    if (!customElements.get("ha-form")) {
      customElements.whenDefined("ha-form").then(() => this._render());
      return;
    }
    this.shadowRoot.innerHTML = `
      <style>
        :host { display:block; padding:8px 0; }
        .hint { color:var(--secondary-text-color); font-size:.82rem; margin:0 0 12px; }
      </style>
      <div class="hint">${esc(this._hint)}</div>
      <ha-form></ha-form>
    `;
    const form = this.shadowRoot.querySelector("ha-form");
    form.hass = this._hass;
    form.data = this._config;
    form.schema = this._schema;
    form.computeLabel = (schema) => this._labels?.[schema.name] || schema.name || "";
    form.addEventListener("value-changed", (event) => {
      this._config = { ...event.detail.value };
      fireConfigChanged(this, this._config);
    });
  }
}

class ProbulatorTargetEditor extends ProbulatorFormEditor {
  setConfig(config) {
    const normalized = { ...config };
    if (normalized.mode === "custom" && layoutRows(normalized, "line", 8).length === 0) {
      normalized.line_1 = "icon, name, spacer, status";
      normalized.line_2 = "target";
      normalized.line_3 = "response:stack, success:stack";
    }
    super.setConfig({
      mode: "normal",
      show_response: true,
      show_average: true,
      show_success: true,
      show_p95: false,
      show_jitter: false,
      show_sparkline: true,
      custom_show_labels: true,
      ...normalized,
    });
  }

  constructor() {
    super();
    this.configure([
      { name: "entity", required: true, selector: { entity: { domain: ["binary_sensor"] } } },
      { name: "mode", selector: { select: { options: ["minimal", "normal", "extended", "custom"], mode: "dropdown" } } },
      { name: "name", selector: { text: {} } },
      { name: "icon", selector: { icon: {} } },
      { name: "show_response", selector: { boolean: {} } },
      { name: "show_average", selector: { boolean: {} } },
      { name: "show_success", selector: { boolean: {} } },
      { name: "show_p95", selector: { boolean: {} } },
      { name: "show_jitter", selector: { boolean: {} } },
      { name: "show_sparkline", selector: { boolean: {} } },
      { name: "line_1", selector: { text: {} } },
      { name: "line_2", selector: { text: {} } },
      { name: "line_3", selector: { text: {} } },
      { name: "line_4", selector: { text: {} } },
      { name: "line_5", selector: { text: {} } },
      { name: "line_6", selector: { text: {} } },
      { name: "line_7", selector: { text: {} } },
      { name: "line_8", selector: { text: {} } },
      { name: "custom_show_labels", selector: { boolean: {} } },
      { name: "custom_labels", selector: { text: {} } },
      { name: "custom_hide_empty", selector: { boolean: {} } },
      { name: "card_padding", selector: { text: {} } },
      { name: "row_gap", selector: { text: {} } },
      { name: "field_gap", selector: { text: {} } },
      { name: "online_color", selector: { text: {} } },
      { name: "degraded_color", selector: { text: {} } },
      { name: "offline_color", selector: { text: {} } },
      { name: "background", selector: { text: {} } },
      { name: "border_radius", selector: { text: {} } },
      { name: "metric_font_size", selector: { text: {} } },
    ], {
      entity: "Target entity",
      mode: "Display mode",
      name: "Display name",
      icon: "Icon",
      show_response: "Show response time",
      show_average: "Show average response time",
      show_success: "Show success rate",
      show_p95: "Show 95th percentile",
      show_jitter: "Show jitter",
      show_sparkline: "Show latency sparkline (Extended)",
      line_1: "Custom line 1",
      line_2: "Custom line 2",
      line_3: "Custom line 3",
      line_4: "Custom line 4",
      line_5: "Custom line 5",
      line_6: "Custom line 6",
      line_7: "Custom line 7",
      line_8: "Custom line 8",
      custom_show_labels: "Show labels in Custom mode",
      custom_labels: "Custom labels (field=Label; field=Label)",
      custom_hide_empty: "Hide fields with no value",
      card_padding: "Card padding (CSS value)",
      row_gap: "Custom row gap (CSS value)",
      field_gap: "Custom field gap (CSS value)",
      online_color: "Online color (CSS value)",
      degraded_color: "Degraded color (CSS value)",
      offline_color: "Offline color (CSS value)",
      background: "Card background (CSS value)",
      border_radius: "Border radius (CSS value)",
      metric_font_size: "Metric font size (CSS value)",
    }, "Custom mode fields: icon, status_dot, name, target, host, port, group, status, underlying_status, quality, monitoring, maintenance, flapping, response, average, min, max, p95, jitter, success, samples, failures, successful_probes, total_probes, consecutive_failures, consecutive_successes, flap_transitions, last_check, checked_ago, last_success, last_failure, status_change, outage, last_outage, outage_count, longest_outage, mean_outage, total_outage, stable_since, probe_interval, thresholds, timeout, retries, attempts, probe_cycle, queue_wait, dependency, maintenance_until, error, probe_type, service, spacer, divider, sparkline. Put comma-separated fields on each Custom line. Add :value, :inline, or :stack to a field to override its presentation, for example response:value or last_check:inline.");
  }
}

class ProbulatorOverviewEditor extends ProbulatorFormEditor {
  setConfig(config) {
    const normalized = { ...config };
    if (normalized.title === "HA Probulator") delete normalized.title;
    super.setConfig({ sort: "status", custom_show_labels: false, ...normalized });
  }

  constructor() {
    super();
    this.configure([
      { name: "title", selector: { text: {} } },
      { name: "group", selector: { text: {} } },
      { name: "sort", selector: { select: { options: ["status", "name"], mode: "dropdown" } } },
      { name: "entities", selector: { entity: { domain: ["binary_sensor"], multiple: true } } },
      { name: "item_line_1", selector: { text: {} } },
      { name: "item_line_2", selector: { text: {} } },
      { name: "item_line_3", selector: { text: {} } },
      { name: "item_line_4", selector: { text: {} } },
      { name: "custom_show_labels", selector: { boolean: {} } },
      { name: "custom_labels", selector: { text: {} } },
      { name: "custom_hide_empty", selector: { boolean: {} } },
      { name: "card_padding", selector: { text: {} } },
      { name: "row_gap", selector: { text: {} } },
      { name: "field_gap", selector: { text: {} } },
      { name: "online_color", selector: { text: {} } },
      { name: "degraded_color", selector: { text: {} } },
      { name: "offline_color", selector: { text: {} } },
      { name: "background", selector: { text: {} } },
      { name: "border_radius", selector: { text: {} } },
    ], {
      title: "Title",
      group: "Group filter",
      sort: "Sort order",
      entities: "Specific targets",
      item_line_1: "Target row line 1",
      item_line_2: "Target row line 2",
      item_line_3: "Target row line 3",
      item_line_4: "Target row line 4",
      custom_show_labels: "Show labels in custom target rows",
      custom_labels: "Custom labels (field=Label; field=Label)",
      custom_hide_empty: "Hide fields with no value",
      card_padding: "Card padding (CSS value)",
      row_gap: "Custom row gap (CSS value)",
      field_gap: "Custom field gap (CSS value)",
      online_color: "Online color (CSS value)",
      degraded_color: "Degraded color (CSS value)",
      offline_color: "Offline color (CSS value)",
      background: "Card background (CSS value)",
      border_radius: "Border radius (CSS value)",
    }, "Overview target rows use the same field keys as the Target card. Leave all Target row lines blank for the built-in compact layout, or define up to four custom lines.");
  }
}

class ProbulatorSummaryEditor extends ProbulatorFormEditor {
  setConfig(config) {
    super.setConfig({ title: "Network status", ...config });
  }

  constructor() {
    super();
    this.configure([
      { name: "title", selector: { text: {} } },
      { name: "group", selector: { text: {} } },
      { name: "entities", selector: { entity: { domain: ["binary_sensor"], multiple: true } } },
      { name: "online_color", selector: { text: {} } },
      { name: "degraded_color", selector: { text: {} } },
      { name: "offline_color", selector: { text: {} } },
      { name: "background", selector: { text: {} } },
      { name: "border_radius", selector: { text: {} } },
    ], {
      title: "Title",
      group: "Group filter",
      entities: "Specific targets",
      online_color: "Online color (CSS value)",
      degraded_color: "Degraded color (CSS value)",
      offline_color: "Offline color (CSS value)",
      background: "Card background (CSS value)",
      border_radius: "Border radius (CSS value)",
    });
  }
}

class ProbulatorManagerEditor extends ProbulatorFormEditor {
  setConfig(config) {
    super.setConfig({
      title: "HA Probulator Manager",
      sort: "status",
      show_actions: true,
      show_bulk_actions: true,
      ...config,
    });
  }

  constructor() {
    super();
    this.configure([
      { name: "title", selector: { text: {} } },
      { name: "group", selector: { text: {} } },
      { name: "sort", selector: { select: { options: ["status", "name"], mode: "dropdown" } } },
      { name: "show_actions", selector: { boolean: {} } },
      { name: "show_bulk_actions", selector: { boolean: {} } },
      { name: "online_color", selector: { text: {} } },
      { name: "degraded_color", selector: { text: {} } },
      { name: "offline_color", selector: { text: {} } },
      { name: "unstable_color", selector: { text: {} } },
      { name: "maintenance_color", selector: { text: {} } },
      { name: "background", selector: { text: {} } },
      { name: "border_radius", selector: { text: {} } },
    ], {
      title: "Title",
      group: "Fixed group filter",
      sort: "Sort order",
      show_actions: "Show target actions",
      show_bulk_actions: "Show multi-select bulk actions",
      online_color: "Online color (CSS value)",
      degraded_color: "Degraded color (CSS value)",
      offline_color: "Offline color (CSS value)",
      unstable_color: "Unstable color (CSS value)",
      maintenance_color: "Maintenance color (CSS value)",
      background: "Card background (CSS value)",
      border_radius: "Border radius (CSS value)",
    });
  }
}


const PROBULATOR_LAYOUT_FIELDS = new Set([
  "icon",
  "status_dot",
  "name",
  "target",
  "host",
  "port",
  "group",
  "status",
  "underlying_status",
  "quality",
  "monitoring",
  "maintenance",
  "flapping",
  "response",
  "average",
  "min",
  "max",
  "p95",
  "jitter",
  "success",
  "samples",
  "failures",
  "successful_probes",
  "total_probes",
  "consecutive_failures",
  "consecutive_successes",
  "flap_transitions",
  "last_check",
  "checked_ago",
  "last_success",
  "last_failure",
  "status_change",
  "outage",
  "last_outage",
  "outage_count",
  "longest_outage",
  "mean_outage",
  "total_outage",
  "stable_since",
  "probe_interval",
  "thresholds",
  "timeout",
  "retries",
  "attempts",
  "probe_cycle",
  "queue_wait",
  "dependency",
  "maintenance_until",
  "error",
  "probe_type",
  "service",
  "spacer",
  "divider",
  "sparkline",
]);

const PROBULATOR_DEFAULT_LABELS = {
  target: "Target",
  host: "Host",
  port: "Port",
  group: "Group",
  status: "Status",
  underlying_status: "Underlying",
  quality: "Quality",
  monitoring: "Monitoring",
  maintenance: "Maintenance",
  flapping: "Flapping",
  response: "Response",
  average: "Average",
  min: "Minimum",
  max: "Maximum",
  p95: "95th percentile",
  jitter: "Jitter",
  success: "Success",
  samples: "Samples",
  failures: "Failed probes",
  successful_probes: "Successful probes",
  total_probes: "Total probes",
  consecutive_failures: "Consecutive failures",
  consecutive_successes: "Consecutive successes",
  flap_transitions: "Flap transitions",
  last_check: "Last check",
  checked_ago: "Checked",
  last_success: "Last success",
  last_failure: "Last failure",
  status_change: "Last status change",
  outage: "Current outage",
  last_outage: "Last outage",
  outage_count: "Outages",
  longest_outage: "Longest outage",
  mean_outage: "Mean outage",
  total_outage: "Total outage",
  stable_since: "Stable since",
  probe_interval: "Probe interval",
  thresholds: "Thresholds",
  timeout: "Timeout",
  retries: "Retries",
  attempts: "Attempts",
  probe_cycle: "Probe cycle",
  queue_wait: "Queue wait",
  dependency: "Dependency",
  maintenance_until: "Maintenance until",
  error: "Last error",
  probe_type: "Probe",
  service: "Service",
};

function parseCustomLabels(value) {
  const labels = {};
  String(value || "").split(";").forEach((entry) => {
    const split = entry.indexOf("=");
    if (split <= 0) return;
    const key = entry.slice(0, split).trim();
    const label = entry.slice(split + 1).trim();
    if (PROBULATOR_LAYOUT_FIELDS.has(key) && label) labels[key] = label;
  });
  return labels;
}

function parseLayoutTokens(value) {
  return String(value || "")
    .split(",")
    .map((raw) => raw.trim().toLowerCase())
    .filter(Boolean)
    .map((raw) => {
      const [key, requestedStyle] = raw.split(":", 2);
      const style = ["value", "inline", "stack"].includes(requestedStyle)
        ? requestedStyle
        : null;
      return { raw, key, style };
    });
}

function layoutRows(config, prefix = "line", count = 8) {
  const rows = [];
  for (let index = 1; index <= count; index += 1) {
    const tokens = parseLayoutTokens(config?.[`${prefix}_${index}`]);
    if (tokens.length) rows.push(tokens);
  }
  return rows;
}

function secondsText(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return "—";
  if (n < 60) return `${Math.round(n)} s`;
  if (n < 3600) return `${Math.floor(n / 60)}m ${Math.round(n % 60)}s`;
  const hours = Math.floor(n / 3600);
  const minutes = Math.floor((n % 3600) / 60);
  return `${hours}h ${minutes}m`;
}

function relativeTime(value) {
  if (!value) return "—";
  const timestamp = new Date(value).getTime();
  if (!Number.isFinite(timestamp)) return "—";
  const seconds = Math.max(0, Math.round((Date.now() - timestamp) / 1000));
  if (seconds < 60) return `${seconds} second${seconds === 1 ? "" : "s"} ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes} minute${minutes === 1 ? "" : "s"} ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} hour${hours === 1 ? "" : "s"} ago`;
  const days = Math.floor(hours / 24);
  return `${days} day${days === 1 ? "" : "s"} ago`;
}

function fieldValue(key, stateObj, config = {}) {
  const a = stateObj?.attributes || {};
  const status = stateStatus(stateObj);
  const name = config.name || a.target_name || a.friendly_name || stateObj?.entity_id || "—";
  const hostPort = a.target || (a.host ? `${a.host}${a.port ? `:${a.port}` : ""}` : "—");

  switch (key) {
    case "name": return name;
    case "target": return hostPort;
    case "host": return a.host || "—";
    case "port": return a.port ?? "—";
    case "group": return a.group || "—";
    case "status": return statusLabel(status);
    case "underlying_status": return statusLabel(a.underlying_status || status);
    case "quality": return statusLabel(a.quality);
    case "monitoring": return a.monitoring_enabled === false ? "Disabled" : "Enabled";
    case "maintenance": return a.maintenance === true ? "On" : "Off";
    case "flapping": return a.flapping === true ? "Yes" : "No";
    case "response": return fmtMs(a.response_time_ms);
    case "average": return fmtMs(a.average_response_time_ms);
    case "min": return fmtMs(a.min_response_time_ms);
    case "max": return fmtMs(a.max_response_time_ms);
    case "p95": return fmtMs(a.p95_response_time_ms);
    case "jitter": return fmtMs(a.jitter_ms);
    case "success": return fmtPct(a.success_rate);
    case "samples": return a.window_samples ?? "—";
    case "failures": return a.failed_probes ?? "—";
    case "successful_probes": return a.successful_probes ?? "—";
    case "total_probes": return a.total_probes ?? "—";
    case "consecutive_failures": return a.consecutive_failures ?? 0;
    case "consecutive_successes": return a.consecutive_successes ?? 0;
    case "flap_transitions": return a.flap_transitions ?? 0;
    case "last_check": return fmtTime(a.last_check);
    case "checked_ago": return relativeTime(a.last_check);
    case "last_success": return fmtTime(a.last_success);
    case "last_failure": return fmtTime(a.last_failure);
    case "status_change": return fmtTime(a.last_status_change);
    case "outage": return secondsText(a.current_outage_duration_seconds);
    case "last_outage": return secondsText(a.last_outage_duration_seconds);
    case "outage_count": return a.outage_count ?? 0;
    case "longest_outage": return secondsText(a.longest_outage_duration_seconds);
    case "mean_outage": return secondsText(a.mean_outage_duration_seconds);
    case "total_outage": return secondsText(a.total_outage_duration_seconds);
    case "stable_since": return fmtTime(a.stable_since);
    case "probe_interval": return a.current_scan_interval != null
      ? `${a.current_scan_interval} s`
      : a.scan_interval != null ? `${a.scan_interval} s` : "—";
    case "thresholds": {
      const warning = Number(a.warning_latency_ms);
      const critical = Number(a.critical_latency_ms);
      return Number.isFinite(warning) && Number.isFinite(critical)
        ? `W ${warning} · C ${critical} ms`
        : "—";
    }
    case "timeout": return a.timeout != null ? `${a.timeout} s` : "—";
    case "retries": return a.retries ?? "—";
    case "attempts": return a.attempts ?? "—";
    case "probe_cycle": return fmtMs(a.probe_cycle_ms);
    case "queue_wait": return fmtMs(a.probe_queue_wait_ms);
    case "dependency": return a.dependency_name
      ? `${a.dependency_name} · ${statusLabel(a.dependency_status)}`
      : "—";
    case "maintenance_until": return fmtTime(a.maintenance_until);
    case "error": return a.last_error || "—";
    case "probe_type": return "TCP";
    case "service": return "TCP Service";
    default: return "—";
  }
}

function renderLayoutField(token, stateObj, config, labels, compact = false) {
  const { key, style } = token;
  const a = stateObj?.attributes || {};
  const status = stateStatus(stateObj);
  const label = labels[key] || PROBULATOR_DEFAULT_LABELS[key] || key;

  if (key === "spacer") return '<span class="custom-spacer" aria-hidden="true"></span>';
  if (key === "divider") return '<span class="custom-divider" aria-hidden="true"></span>';
  if (key === "sparkline") return sparkline(a.latency_history);
  if (key === "icon") {
    const icon = config.icon || a.icon || "mdi:lan-connect";
    return `<span class="custom-field custom-icon"><ha-icon icon="${esc(icon)}"></ha-icon></span>`;
  }
  if (key === "status_dot") {
    return `<span class="custom-field ${status}" aria-label="${esc(statusLabel(status))}"><span class="dot"></span></span>`;
  }

  const value = fieldValue(key, stateObj, config);
  if (
    config.custom_hide_empty === true
    && !["name", "status"].includes(key)
    && (value == null || value === "" || value === "—")
  ) {
    return "";
  }

  if (key === "status" && style !== "value" && style !== "inline" && style !== "stack") {
    return `<span class="custom-field custom-status pill ${status}">${esc(statusLabel(status))}</span>`;
  }
  if (key === "name" && style !== "inline" && style !== "stack") {
    return `<span class="custom-field custom-grow custom-primary">${esc(value)}</span>`;
  }

  const defaultValueOnly = compact || config.custom_show_labels === false;
  const effectiveStyle = style || (
    ["target", "host", "group", "dependency", "error"].includes(key)
      ? (config.custom_show_labels === true && !compact ? "inline" : "value")
      : (defaultValueOnly ? "value" : "stack")
  );

  const valueClass = ["target", "host", "group", "dependency", "error"].includes(key)
    ? "custom-secondary"
    : "custom-metric-value";
  const growClass = ["name", "target", "host", "group", "dependency", "error"].includes(key)
    ? " custom-grow"
    : "";

  if (effectiveStyle === "value") {
    return `<span class="custom-field${growClass} ${valueClass}">${esc(value)}</span>`;
  }
  if (effectiveStyle === "inline") {
    return `<span class="custom-field${growClass} custom-inline"><span class="custom-metric-label">${esc(label)}</span><span class="${valueClass}">${esc(value)}</span></span>`;
  }
  return `<span class="custom-field${growClass} custom-metric"><span class="custom-metric-label">${esc(label)}</span><span class="${valueClass}">${esc(value)}</span></span>`;
}

function renderCustomLayout(stateObj, config, prefix = "line", count = 8, compact = false) {
  const rows = layoutRows(config, prefix, count);
  const labels = parseCustomLabels(config.custom_labels);
  const unknown = new Set();

  const html = rows.map((row) => {
    const fields = row.map((token) => {
      if (!PROBULATOR_LAYOUT_FIELDS.has(token.key)) {
        unknown.add(token.raw);
        return "";
      }
      return renderLayoutField(token, stateObj, config, labels, compact);
    }).join("");
    return fields ? `<div class="custom-line">${fields}</div>` : "";
  }).join("");

  const warning = unknown.size
    ? `<div class="custom-warning">Unknown layout field${unknown.size === 1 ? "" : "s"}: ${esc([...unknown].join(", "))}</div>`
    : "";

  return `<div class="custom-layout">${html}${warning}</div>`;
}

function sparkline(history) {
  const points = Array.isArray(history)
    ? history.map((item) => Number(item?.latency_ms)).filter(Number.isFinite)
    : [];
  if (points.length < 2) return "";
  const width = 100;
  const height = 40;
  const min = Math.min(...points);
  const max = Math.max(...points);
  const span = Math.max(1, max - min);
  const coords = points.map((value, index) => {
    const x = (index / (points.length - 1)) * width;
    const y = height - ((value - min) / span) * (height - 4) - 2;
    return `${x.toFixed(2)},${y.toFixed(2)}`;
  }).join(" ");
  return `<div class="spark"><svg viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" aria-label="Recent response time"><polyline points="${coords}"></polyline></svg></div>`;
}

class ProbulatorCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  static getStubConfig() {
    return {
      mode: "normal",
      show_response: true,
      show_average: true,
      show_success: true,
      show_p95: false,
      show_jitter: false,
      show_sparkline: true,
      custom_show_labels: true,
    };
  }

  static async getConfigElement() {
    return document.createElement("probulator-target-editor");
  }

  setConfig(config) {
    if (!config || !config.entity) throw new Error("HA Probulator card requires an entity");
    const normalized = { ...config };
    if (normalized.mode === "custom" && layoutRows(normalized, "line", 8).length === 0) {
      normalized.line_1 = "icon, name, spacer, status";
      normalized.line_2 = "target";
      normalized.line_3 = "response:stack, success:stack";
    }
    this._config = {
      mode: "normal",
      show_response: true,
      show_average: true,
      show_success: true,
      show_p95: false,
      show_jitter: false,
      show_sparkline: true,
      custom_show_labels: true,
      ...normalized,
    };
    if (!["minimal", "normal", "extended", "custom"].includes(this._config.mode)) {
      throw new Error("mode must be minimal, normal, extended, or custom");
    }
    applyInlineTheme(this, this._config);
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() {
    if (this._config?.mode === "custom") {
      return Math.max(1, layoutRows(this._config, "line", 8).length);
    }
    return this._config?.mode === "extended" ? 5 : this._config?.mode === "minimal" ? 1 : 3;
  }

  getGridOptions() {
    return {
      columns: 6,
      min_columns: 3,
      max_columns: 12,
      rows: "auto",
    };
  }

  _render() {
    if (!this.shadowRoot || !this._config || !this._hass) return;
    const stateObj = this._hass.states[this._config.entity];
    if (!stateObj) {
      this.shadowRoot.innerHTML = `<style>${PROBULATOR_STYLE}</style><ha-card><div class="empty">Entity ${esc(this._config.entity)} was not found.</div></ha-card>`;
      return;
    }

    const a = stateObj.attributes || {};
    const mode = this._config.mode;
    const status = stateStatus(stateObj);
    const name = this._config.name || a.target_name || a.friendly_name || stateObj.entity_id;
    const icon = this._config.icon || a.icon || "mdi:lan-connect";
    const hostPort = a.target || (a.host ? `${a.host}${a.port ? `:${a.port}` : ""}` : "");

    if (mode === "custom") {
      const custom = renderCustomLayout(stateObj, this._config, "line", 8, false);
      this.shadowRoot.innerHTML = `
        <style>${PROBULATOR_STYLE}</style>
        <ha-card>
          <div class="wrap" role="button" tabindex="0">
            ${custom}
          </div>
        </ha-card>`;
    } else if (mode === "minimal") {
      this.shadowRoot.innerHTML = `
        <style>${PROBULATOR_STYLE}</style>
        <ha-card>
          <div class="header minimal ${status}" role="button" tabindex="0">
            <ha-icon icon="${esc(icon)}"></ha-icon>
            <span class="dot"></span>
            <div class="name grow">${esc(name)}</div>
            <div class="latency">${fmtMs(a.response_time_ms)}</div>
          </div>
        </ha-card>`;
    } else {
      const extended = mode === "extended" ? `
        <div class="details">
          <div class="label">Target</div><div class="value">${esc(hostPort || "—")}</div>
          <div class="label">Group</div><div class="value">${esc(a.group || "—")}</div>
          ${a.underlying_status && a.underlying_status !== status ? `<div class="label">Underlying</div><div class="value">${esc(statusLabel(a.underlying_status))}</div>` : ""}
          ${a.dependency_name ? `<div class="label">Depends on</div><div class="value">${esc(a.dependency_name)} · ${esc(statusLabel(a.dependency_status))}</div>` : ""}
          ${a.maintenance_until ? `<div class="label">Maintenance until</div><div class="value">${esc(fmtTime(a.maintenance_until))}</div>` : ""}
          <div class="label">Probe interval</div><div class="value">${esc(a.current_scan_interval ?? a.scan_interval ?? "—")} s</div>
          <div class="label">Minimum</div><div class="value">${fmtMs(a.min_response_time_ms)}</div>
          <div class="label">95th percentile</div><div class="value">${fmtMs(a.p95_response_time_ms)}</div>
          <div class="label">Jitter</div><div class="value">${fmtMs(a.jitter_ms)}</div>
          <div class="label">Maximum</div><div class="value">${fmtMs(a.max_response_time_ms)}</div>
          <div class="label">Failures</div><div class="value">${esc(a.failed_probes ?? "—")} total / ${esc(a.consecutive_failures ?? 0)} consecutive</div>
          <div class="label">Last check</div><div class="value">${esc(fmtTime(a.last_check))}</div>
          <div class="label">Last status change</div><div class="value">${esc(fmtTime(a.last_status_change))}</div>
          ${a.current_outage_duration_seconds != null ? `<div class="label">Current outage</div><div class="value">${esc(Math.round(Number(a.current_outage_duration_seconds)))} s</div>` : ""}
          ${a.stable_since ? `<div class="label">Stable since</div><div class="value">${esc(fmtTime(a.stable_since))}</div>` : ""}
          <div class="label">Outages</div><div class="value">${esc(a.outage_count ?? 0)}${a.longest_outage_duration_seconds != null ? ` · longest ${esc(Math.round(Number(a.longest_outage_duration_seconds)))} s` : ""}</div>
          <div class="label">Last success</div><div class="value">${esc(fmtTime(a.last_success))}</div>
          <div class="label">Last failure</div><div class="value">${esc(fmtTime(a.last_failure))}</div>
          ${a.last_error ? `<div class="label">Last error</div><div class="value">${esc(a.last_error)}</div>` : ""}
        </div>
        ${this._config.show_sparkline !== false ? sparkline(a.latency_history) : ""}
      ` : "";
      this.shadowRoot.innerHTML = `
        <style>${PROBULATOR_STYLE}</style>
        <ha-card>
          <div class="wrap" role="button" tabindex="0">
            <div class="header ${status}">
              <ha-icon icon="${esc(icon)}"></ha-icon>
              <div class="grow">
                <div class="name">${esc(name)}</div>
                <div class="sub">${esc(hostPort)}${a.group ? ` · ${esc(a.group)}` : ""}</div>
              </div>
              <div class="status"><span class="dot"></span>${esc(statusLabel(status))}</div>
            </div>
            <div class="metric-grid">
              ${this._config.show_response !== false ? `<div class="metric"><div class="value">${fmtMs(a.response_time_ms)}</div><div class="label">Response</div></div>` : ""}
              ${this._config.show_average !== false ? `<div class="metric"><div class="value">${fmtMs(a.average_response_time_ms)}</div><div class="label">Average</div></div>` : ""}
              ${this._config.show_success !== false ? `<div class="metric"><div class="value">${fmtPct(a.success_rate)}</div><div class="label">Success</div></div>` : ""}
              ${this._config.show_p95 === true ? `<div class="metric"><div class="value">${fmtMs(a.p95_response_time_ms)}</div><div class="label">95th percentile</div></div>` : ""}
              ${this._config.show_jitter === true ? `<div class="metric"><div class="value">${fmtMs(a.jitter_ms)}</div><div class="label">Jitter</div></div>` : ""}
            </div>
            ${extended}
          </div>
        </ha-card>`;
    }

    const clickable = this.shadowRoot.querySelector('[role="button"]');
    clickable?.addEventListener("click", () => fireMoreInfo(this, stateObj.entity_id));
    clickable?.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        fireMoreInfo(this, stateObj.entity_id);
      }
    });
  }
}

class ProbulatorOverviewCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  static getStubConfig() {
    return { sort: "status" };
  }

  static async getConfigElement() {
    return document.createElement("probulator-overview-editor");
  }

  setConfig(config) {
    const normalized = { ...config };
    if (normalized.title === "HA Probulator") delete normalized.title;
    this._config = { sort: "status", ...normalized };
    applyInlineTheme(this, this._config);
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() {
    const count = probulatorTargets(this._hass, this._config).length;
    return Math.max(1, count + (this._config?.title ? 1 : 0));
  }
  getGridOptions() {
    return {
      columns: "full",
      min_columns: 6,
      rows: "auto",
    };
  }

  _render() {
    if (!this.shadowRoot || !this._hass || !this._config) return;
    const targets = probulatorTargets(this._hass, this._config);
    const rows = targets.map((stateObj) => {
      const a = stateObj.attributes || {};
      const status = stateStatus(stateObj);
      const name = a.target_name || a.friendly_name || stateObj.entity_id;
      const sub = [a.target || (a.host && `${a.host}${a.port ? `:${a.port}` : ""}`), a.group].filter(Boolean).join(" · ");
      const hasCustomLayout = layoutRows(this._config, "item_line", 4).length > 0;
      if (hasCustomLayout) {
        return `
          <div class="target-row custom-target-row" data-entity="${esc(stateObj.entity_id)}" role="button" tabindex="0">
            ${renderCustomLayout(stateObj, this._config, "item_line", 4, false)}
          </div>`;
      }
      return `
        <div class="target-row" data-entity="${esc(stateObj.entity_id)}" role="button" tabindex="0">
          <div class="grow"><div class="target-name">${esc(name)}</div><div class="sub">${esc(sub)}</div></div>
          <div class="target-latency">${fmtMs(a.response_time_ms)}</div>
          <div class="pill target-status ${status}">${esc(statusLabel(status))}</div>
        </div>`;
    }).join("");

    this.shadowRoot.innerHTML = `
      <style>${PROBULATOR_STYLE}</style>
      <ha-card>
        <div class="wrap">
          ${this._config.title ? `<div class="header"><div class="grow"><div class="name">${esc(this._config.title)}</div>${this._config.group ? `<div class="sub">Group: ${esc(this._config.group)}</div>` : ""}</div></div>` : ""}
          <div class="targets">${rows || '<div class="empty">No HA Probulator targets match this card.</div>'}</div>
        </div>
      </ha-card>`;

    this.shadowRoot.querySelectorAll(".target-row").forEach((row) => {
      const entityId = row.dataset.entity;
      row.addEventListener("click", () => fireMoreInfo(this, entityId));
      row.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          fireMoreInfo(this, entityId);
        }
      });
    });
  }
}

class ProbulatorSummaryCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  static getStubConfig() {
    return { title: "Network status" };
  }

  static async getConfigElement() {
    return document.createElement("probulator-summary-editor");
  }

  setConfig(config) {
    this._config = { title: "Network status", ...config };
    applyInlineTheme(this, this._config);
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() { return 3; }
  getGridOptions() {
    return {
      columns: 12,
      min_columns: 6,
      max_columns: 12,
      rows: "auto",
    };
  }

  _render() {
    if (!this.shadowRoot || !this._hass || !this._config) return;
    const targets = probulatorTargets(this._hass, this._config);
    const counts = {
      online: 0,
      degraded: 0,
      unstable: 0,
      offline: 0,
      dependency_offline: 0,
      maintenance: 0,
      disabled: 0,
      probing: 0,
    };
    const latencies = [];
    targets.forEach((stateObj) => {
      counts[stateStatus(stateObj)] += 1;
      const n = Number(stateObj.attributes?.response_time_ms);
      if (Number.isFinite(n)) latencies.push(n);
    });
    const avg = latencies.length ? latencies.reduce((a, b) => a + b, 0) / latencies.length : null;
    const attention = counts.degraded + counts.unstable + counts.dependency_offline;
    const offline = counts.offline;

    this.shadowRoot.innerHTML = `
      <style>${PROBULATOR_STYLE}</style>
      <ha-card>
        <div class="wrap">
          <div class="header"><div class="grow"><div class="name">${esc(this._config.title)}</div>${this._config.group ? `<div class="sub">Group: ${esc(this._config.group)}</div>` : ""}</div></div>
          <div class="summary">
            <div class="summary-box"><div class="n" style="color:var(--probulator-online-color)">${counts.online}</div><div class="l">Online</div></div>
            <div class="summary-box"><div class="n" style="color:var(--probulator-degraded-color)">${attention}</div><div class="l">Needs attention</div></div>
            <div class="summary-box"><div class="n" style="color:var(--probulator-offline-color)">${offline}</div><div class="l">Offline</div></div>
            <div class="summary-box"><div class="n">${fmtMs(avg)}</div><div class="l">Average response</div></div>
          </div>
          <div class="footer">${targets.length} target${targets.length === 1 ? "" : "s"}${counts.probing ? ` · ${counts.probing} probing` : ""}${counts.maintenance ? ` · ${counts.maintenance} maintenance` : ""}${counts.disabled ? ` · ${counts.disabled} disabled` : ""}</div>
        </div>
      </ha-card>`;
  }
}

class ProbulatorManagerCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._search = "";
    this._runtimeGroup = "";
    this._selected = new Set();
  }

  static getStubConfig() {
    return {
      title: "HA Probulator Manager",
      sort: "status",
      show_actions: true,
      show_bulk_actions: true,
    };
  }

  static async getConfigElement() {
    return document.createElement("probulator-manager-editor");
  }

  setConfig(config) {
    this._config = {
      title: "HA Probulator Manager",
      sort: "status",
      show_actions: true,
      ...config,
    };
    this._runtimeGroup = String(this._config.group || "");
    applyInlineTheme(this, this._config);
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() { return 6; }
  getGridOptions() {
    return {
      columns: "full",
      min_columns: 6,
      rows: "auto",
    };
  }

  _applyFilter() {
    const search = this._search.trim().toLowerCase();
    const group = this._runtimeGroup.trim().toLowerCase();
    let visible = 0;
    this.shadowRoot?.querySelectorAll(".manager-row").forEach((row) => {
      const matchesSearch = !search || String(row.dataset.search || "").includes(search);
      const matchesGroup = !group || String(row.dataset.group || "") === group;
      row.hidden = !(matchesSearch && matchesGroup);
      if (!row.hidden) visible += 1;
    });
    const count = this.shadowRoot?.querySelector(".manager-count");
    if (count) count.textContent = `${visible} matching target${visible === 1 ? "" : "s"}`;
  }

  async _runAction(action, targetId) {
    if (!this._hass || !targetId) return;
    if (action === "probe") {
      await this._hass.callService("ha_probulator", "probe", { target_id: targetId });
    } else if (action === "maintenance-on") {
      await this._hass.callService("ha_probulator", "start_maintenance", { target_id: targetId });
    } else if (action === "maintenance-off") {
      await this._hass.callService("ha_probulator", "end_maintenance", { target_id: targetId });
    } else if (action === "monitoring-on") {
      await this._hass.callService("ha_probulator", "set_monitoring", { target_id: targetId, enabled: true });
    } else if (action === "monitoring-off") {
      await this._hass.callService("ha_probulator", "set_monitoring", { target_id: targetId, enabled: false });
    }
  }


  async _runBulkAction(action) {
    if (!this._selected.size) return;
    await Promise.all(
      [...this._selected].map((targetId) => this._runAction(action, targetId))
    );
  }

  _updateBulkState() {
    const count = this.shadowRoot?.querySelector(".manager-bulk-count");
    if (count) {
      count.textContent = `${this._selected.size} selected`;
    }
    this.shadowRoot?.querySelectorAll(".manager-bulk-action").forEach((button) => {
      button.disabled = this._selected.size === 0;
    });
  }

  _selectVisible(select) {
    this.shadowRoot?.querySelectorAll(".manager-row").forEach((row) => {
      if (row.hidden) return;
      const checkbox = row.querySelector(".manager-check");
      const targetId = checkbox?.dataset.target;
      if (!targetId) return;
      checkbox.checked = select;
      if (select) this._selected.add(targetId);
      else this._selected.delete(targetId);
    });
    this._updateBulkState();
  }

  _render() {
    if (!this.shadowRoot || !this._hass || !this._config) return;
    const targets = probulatorTargets(this._hass, { sort: this._config.sort });
    const groups = [...new Set(
      targets.map((stateObj) => String(stateObj.attributes?.group || "").trim()).filter(Boolean)
    )].sort((a, b) => a.localeCompare(b));

    const rows = targets.map((stateObj) => {
      const a = stateObj.attributes || {};
      const status = stateStatus(stateObj);
      const name = a.target_name || a.friendly_name || stateObj.entity_id;
      const search = [name, a.target, a.group, statusLabel(status), a.dependency_name]
        .filter(Boolean).join(" ").toLowerCase();
      const maintenance = a.maintenance === true;
      const monitoring = a.monitoring_enabled !== false;
      const actions = this._config.show_actions === false ? "" : `
        <div class="manager-actions">
          <button class="manager-action" type="button" data-action="probe" data-target="${esc(a.target_id)}">Probe</button>
          <button class="manager-action" type="button" data-action="${maintenance ? "maintenance-off" : "maintenance-on"}" data-target="${esc(a.target_id)}">${maintenance ? "End maintenance" : "Maintenance"}</button>
          <button class="manager-action" type="button" data-action="${monitoring ? "monitoring-off" : "monitoring-on"}" data-target="${esc(a.target_id)}">${monitoring ? "Disable" : "Enable"}</button>
        </div>`;
      const checked = this._selected.has(String(a.target_id || "")) ? "checked" : "";
      return `
        <div class="manager-row" data-search="${esc(search)}" data-group="${esc(String(a.group || "").toLowerCase())}">
          <input class="manager-check" type="checkbox" aria-label="Select ${esc(name)}" data-target="${esc(a.target_id)}" ${checked}>
          <div class="manager-info" data-entity="${esc(stateObj.entity_id)}" role="button" tabindex="0">
            <div class="target-name">${esc(name)}</div>
            <div class="sub">${esc(a.target || "")}${a.group ? ` · ${esc(a.group)}` : ""}${a.dependency_name ? ` · depends on ${esc(a.dependency_name)}` : ""}</div>
          </div>
          <div class="manager-metrics">${fmtMs(a.response_time_ms)}<br>jitter ${fmtMs(a.jitter_ms)}</div>
          <div class="pill ${status}">${esc(statusLabel(status))}</div>
          ${actions}
        </div>`;
    }).join("");

    const groupControl = this._config.group
      ? `<div class="sub">Group: ${esc(this._config.group)}</div>`
      : `<select class="manager-select" aria-label="Filter by group">
          <option value="">All groups</option>
          ${groups.map((group) => `<option value="${esc(group.toLowerCase())}" ${group.toLowerCase() === this._runtimeGroup.toLowerCase() ? "selected" : ""}>${esc(group)}</option>`).join("")}
        </select>`;

    this.shadowRoot.innerHTML = `
      <style>${PROBULATOR_STYLE}</style>
      <ha-card>
        <div class="wrap">
          <div class="header">
            <ha-icon icon="mdi:radar"></ha-icon>
            <div class="grow">
              <div class="name">${esc(this._config.title)}</div>
              <div class="sub">Search, inspect, probe, suppress, or disable targets without leaving the dashboard.</div>
            </div>
          </div>
          ${frontendVersionWarning(targets)}
          <div class="manager-toolbar">
            <input class="manager-input" type="search" aria-label="Search HA Probulator targets" placeholder="Search targets, addresses, groups, states…" value="${esc(this._search)}">
            ${groupControl}
          </div>
          ${this._config.show_bulk_actions === false ? "" : `
          <div class="manager-bulk">
            <span class="manager-bulk-count">0 selected</span>
            <button class="manager-action manager-select-visible" type="button">Select visible</button>
            <button class="manager-action manager-clear-selection" type="button">Clear</button>
            <button class="manager-action manager-bulk-action" type="button" data-action="probe">Probe</button>
            <button class="manager-action manager-bulk-action" type="button" data-action="maintenance-on">Maintenance</button>
            <button class="manager-action manager-bulk-action" type="button" data-action="maintenance-off">End maintenance</button>
            <button class="manager-action manager-bulk-action" type="button" data-action="monitoring-on">Enable</button>
            <button class="manager-action manager-bulk-action" type="button" data-action="monitoring-off">Disable</button>
          </div>`}
          <div class="targets">${rows || '<div class="empty">No HA Probulator targets are available.</div>'}</div>
          <div class="manager-count"></div>
        </div>
      </ha-card>`;

    const search = this.shadowRoot.querySelector(".manager-input");
    search?.addEventListener("input", (event) => {
      this._search = event.target.value || "";
      this._applyFilter();
    });
    const group = this.shadowRoot.querySelector(".manager-select");
    group?.addEventListener("change", (event) => {
      this._runtimeGroup = event.target.value || "";
      this._applyFilter();
    });

    this.shadowRoot.querySelectorAll(".manager-check").forEach((checkbox) => {
      checkbox.addEventListener("change", () => {
        const targetId = checkbox.dataset.target;
        if (!targetId) return;
        if (checkbox.checked) this._selected.add(targetId);
        else this._selected.delete(targetId);
        this._updateBulkState();
      });
    });
    this.shadowRoot.querySelector(".manager-select-visible")?.addEventListener("click", () => {
      this._selectVisible(true);
    });
    this.shadowRoot.querySelector(".manager-clear-selection")?.addEventListener("click", () => {
      this._selected.clear();
      this.shadowRoot.querySelectorAll(".manager-check").forEach((checkbox) => {
        checkbox.checked = false;
      });
      this._updateBulkState();
    });
    this.shadowRoot.querySelectorAll(".manager-bulk-action").forEach((button) => {
      button.addEventListener("click", async () => {
        button.disabled = true;
        try {
          await this._runBulkAction(button.dataset.action);
        } finally {
          this._updateBulkState();
        }
      });
    });

    this.shadowRoot.querySelectorAll(".manager-info").forEach((item) => {
      const entityId = item.dataset.entity;
      item.addEventListener("click", () => fireMoreInfo(this, entityId));
      item.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          fireMoreInfo(this, entityId);
        }
      });
    });

    this.shadowRoot.querySelectorAll(".manager-action").forEach((button) => {
      button.addEventListener("click", async (event) => {
        event.stopPropagation();
        button.disabled = true;
        try {
          await this._runAction(button.dataset.action, button.dataset.target);
        } finally {
          button.disabled = false;
        }
      });
    });

    this._applyFilter();
    this._updateBulkState();
  }
}

if (!customElements.get("probulator-target-editor")) customElements.define("probulator-target-editor", ProbulatorTargetEditor);
if (!customElements.get("probulator-overview-editor")) customElements.define("probulator-overview-editor", ProbulatorOverviewEditor);
if (!customElements.get("probulator-summary-editor")) customElements.define("probulator-summary-editor", ProbulatorSummaryEditor);
if (!customElements.get("probulator-manager-editor")) customElements.define("probulator-manager-editor", ProbulatorManagerEditor);

if (!customElements.get("probulator-card")) customElements.define("probulator-card", ProbulatorCard);
if (!customElements.get("probulator-overview-card")) customElements.define("probulator-overview-card", ProbulatorOverviewCard);
if (!customElements.get("probulator-summary-card")) customElements.define("probulator-summary-card", ProbulatorSummaryCard);
if (!customElements.get("probulator-manager-card")) customElements.define("probulator-manager-card", ProbulatorManagerCard);

window.customCards = window.customCards || [];
const existing = new Set(window.customCards.map((card) => card.type));
if (!existing.has("probulator-card")) {
  window.customCards.push({
    type: "probulator-card",
    name: "HA Probulator Target",
    description: "Reachability, latency, and reliability for one HA Probulator target.",
    preview: true,
    documentationURL: "https://github.com/gigabytegrove/ha-probulator#custom-cards",
    getEntitySuggestion: (hass, entityId) => {
      const stateObj = hass?.states?.[entityId];
      if (stateObj?.attributes?.probulator !== true || stateObj?.attributes?.probulator_kind !== "target") return null;
      return { config: { type: "custom:probulator-card", entity: entityId, mode: "normal" } };
    },
  });
}
if (!existing.has("probulator-overview-card")) {
  window.customCards.push({
    type: "probulator-overview-card",
    name: "HA Probulator Overview",
    description: "List all HA Probulator targets or filter them by group.",
    preview: true,
    documentationURL: "https://github.com/gigabytegrove/ha-probulator#custom-cards",
  });
}
if (!existing.has("probulator-summary-card")) {
  window.customCards.push({
    type: "probulator-summary-card",
    name: "HA Probulator Summary",
    description: "Compact counts and average response time across monitored targets.",
    preview: true,
    documentationURL: "https://github.com/gigabytegrove/ha-probulator#custom-cards",
  });
}

if (!existing.has("probulator-manager-card")) {
  window.customCards.push({
    type: "probulator-manager-card",
    name: "HA Probulator Manager",
    description: "Search and operate HA Probulator targets from one dashboard card.",
    preview: true,
    documentationURL: "https://github.com/gigabytegrove/ha-probulator#custom-cards",
  });
}

console.info(`%c HA Probulator %c cards loaded`, "background:#03a9f4;color:#fff;font-weight:700;padding:2px 5px;border-radius:3px", "");
