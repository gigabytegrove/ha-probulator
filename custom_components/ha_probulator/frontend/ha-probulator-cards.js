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
    display: block;
  }
  ha-card {
    overflow: hidden;
    background: var(--probulator-card-background);
    border-radius: var(--probulator-card-border-radius);
  }
  .wrap { padding: 16px; }
  .header { display:flex; align-items:center; gap:10px; min-width:0; }
  .grow { flex:1; min-width:0; }
  .name { font-weight:600; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .sub { color:var(--secondary-text-color); font-size:.82rem; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
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
  .metric .value { font-size:var(--probulator-metric-font-size); font-weight:600; line-height:1.2; overflow:hidden; text-overflow:ellipsis; }
  .metric .label { margin-top:2px; color:var(--secondary-text-color); font-size:.75rem; }
  .details { display:grid; grid-template-columns:max-content 1fr; column-gap:12px; row-gap:7px; margin-top:16px; font-size:.84rem; }
  .details .label { color:var(--secondary-text-color); }
  .details .value { min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .minimal { padding:12px 14px; }
  .minimal .latency { margin-left:auto; font-weight:600; }
  .spark { height:44px; margin-top:14px; width:100%; }
  .spark svg { display:block; width:100%; height:44px; overflow:visible; }
  .spark polyline { fill:none; stroke:var(--primary-color); stroke-width:2; vector-effect:non-scaling-stroke; }
  .empty { color:var(--secondary-text-color); padding:18px; }
  .targets { display:grid; gap:10px; }
  .target-row { display:grid; grid-template-columns:minmax(0,1fr) auto auto; gap:12px; align-items:center; padding:10px 0; border-top:1px solid var(--divider-color); cursor:pointer; }
  .target-row:first-child { border-top:0; }
  .target-name { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .pill { border-radius:999px; padding:3px 8px; font-size:.76rem; text-transform:capitalize; background:color-mix(in srgb, var(--secondary-text-color) 10%, transparent); }
  .pill.online { color:var(--probulator-online-color); }
  .pill.degraded { color:var(--probulator-degraded-color); }
  .pill.offline, .pill.dependency_offline { color:var(--probulator-offline-color); }
  .pill.unstable { color:var(--probulator-unstable-color); }
  .pill.maintenance { color:var(--probulator-maintenance-color); }
  .pill.disabled { color:var(--probulator-disabled-color); }
  .manager-toolbar { display:grid; grid-template-columns:minmax(0,1fr) minmax(140px,220px); gap:10px; margin:14px 0; }
  .manager-input, .manager-select { box-sizing:border-box; width:100%; min-height:40px; border:1px solid var(--divider-color); border-radius:10px; background:var(--card-background-color); color:var(--primary-text-color); padding:8px 10px; font:inherit; }
  .manager-row { display:grid; grid-template-columns:minmax(0,1.5fr) minmax(90px,.6fr) minmax(78px,.5fr) minmax(170px,.9fr); gap:12px; align-items:center; padding:11px 0; border-top:1px solid var(--divider-color); }
  .manager-row[hidden] { display:none; }
  .manager-metrics { color:var(--secondary-text-color); font-size:.8rem; line-height:1.45; }
  .manager-actions { display:flex; justify-content:flex-end; gap:6px; flex-wrap:wrap; }
  .manager-action { border:1px solid var(--divider-color); border-radius:9px; background:transparent; color:var(--primary-text-color); cursor:pointer; padding:6px 8px; font:inherit; font-size:.76rem; }
  .manager-action:hover { background:color-mix(in srgb, var(--primary-color) 10%, transparent); }
  .manager-action:focus-visible { outline:2px solid var(--primary-color); outline-offset:2px; }
  .manager-info { cursor:pointer; min-width:0; }
  .manager-info:focus-visible { outline:2px solid var(--primary-color); outline-offset:3px; border-radius:4px; }
  .manager-count { color:var(--secondary-text-color); font-size:.78rem; margin-top:10px; }
  .summary { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin-top:14px; }
  .summary-box { padding:12px; border-radius:10px; background:color-mix(in srgb, var(--primary-text-color) 5%, transparent); }
  .summary-box .n { font-size:1.35rem; font-weight:700; }
  .summary-box .l { color:var(--secondary-text-color); font-size:.75rem; margin-top:2px; }
  .footer { color:var(--secondary-text-color); font-size:.78rem; margin-top:12px; }
  @media (max-width: 520px) {
    .metric-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
    .summary { grid-template-columns:repeat(2,minmax(0,1fr)); }
    .manager-toolbar { grid-template-columns:1fr; }
    .manager-row { grid-template-columns:minmax(0,1fr) auto; }
    .manager-metrics { display:none; }
    .manager-actions { grid-column:1 / -1; justify-content:flex-start; }
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
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  setConfig(config) {
    this._config = { ...config };
    this._render();
  }

  configure(schema, labels) {
    this._schema = schema;
    this._labels = labels;
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
      <div class="hint">All fields are optional unless marked required. Changes preview immediately.</div>
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
    super.setConfig({
      mode: "normal",
      show_response: true,
      show_average: true,
      show_success: true,
      show_p95: false,
      show_jitter: false,
      show_sparkline: true,
      ...config,
    });
  }

  constructor() {
    super();
    this.configure([
      { name: "entity", required: true, selector: { entity: { domain: ["binary_sensor"] } } },
      { name: "mode", selector: { select: { options: ["minimal", "normal", "extended"], mode: "dropdown" } } },
      { name: "name", selector: { text: {} } },
      { name: "icon", selector: { icon: {} } },
      { name: "show_response", selector: { boolean: {} } },
      { name: "show_average", selector: { boolean: {} } },
      { name: "show_success", selector: { boolean: {} } },
      { name: "show_p95", selector: { boolean: {} } },
      { name: "show_jitter", selector: { boolean: {} } },
      { name: "show_sparkline", selector: { boolean: {} } },
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
      online_color: "Online color (CSS value)",
      degraded_color: "Degraded color (CSS value)",
      offline_color: "Offline color (CSS value)",
      background: "Card background (CSS value)",
      border_radius: "Border radius (CSS value)",
      metric_font_size: "Metric font size (CSS value)",
    });
  }
}

class ProbulatorOverviewEditor extends ProbulatorFormEditor {
  setConfig(config) {
    super.setConfig({ title: "HA Probulator", sort: "status", ...config });
  }

  constructor() {
    super();
    this.configure([
      { name: "title", selector: { text: {} } },
      { name: "group", selector: { text: {} } },
      { name: "sort", selector: { select: { options: ["status", "name"], mode: "dropdown" } } },
      { name: "entities", selector: { entity: { domain: ["binary_sensor"], multiple: true } } },
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
      online_color: "Online color (CSS value)",
      degraded_color: "Degraded color (CSS value)",
      offline_color: "Offline color (CSS value)",
      background: "Card background (CSS value)",
      border_radius: "Border radius (CSS value)",
    });
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
    };
  }

  static async getConfigElement() {
    return document.createElement("probulator-target-editor");
  }

  setConfig(config) {
    if (!config || !config.entity) throw new Error("HA Probulator card requires an entity");
    this._config = {
      mode: "normal",
      show_response: true,
      show_average: true,
      show_success: true,
      show_p95: false,
      show_jitter: false,
      show_sparkline: true,
      ...config,
    };
    if (!["minimal", "normal", "extended"].includes(this._config.mode)) {
      throw new Error("mode must be minimal, normal, or extended");
    }
    applyInlineTheme(this, this._config);
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() {
    return this._config?.mode === "extended" ? 5 : this._config?.mode === "minimal" ? 1 : 3;
  }

  getGridOptions() {
    return { columns: 6, rows: this._config?.mode === "extended" ? 5 : this._config?.mode === "minimal" ? 1 : 3 };
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

    if (mode === "minimal") {
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
    return { title: "HA Probulator", sort: "status" };
  }

  static async getConfigElement() {
    return document.createElement("probulator-overview-editor");
  }

  setConfig(config) {
    this._config = { title: "HA Probulator", sort: "status", ...config };
    applyInlineTheme(this, this._config);
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() { return 4; }
  getGridOptions() { return { columns: 12, rows: 4 }; }

  _render() {
    if (!this.shadowRoot || !this._hass || !this._config) return;
    const targets = probulatorTargets(this._hass, this._config);
    const rows = targets.map((stateObj) => {
      const a = stateObj.attributes || {};
      const status = stateStatus(stateObj);
      const name = a.target_name || a.friendly_name || stateObj.entity_id;
      const sub = [a.target || (a.host && `${a.host}${a.port ? `:${a.port}` : ""}`), a.group].filter(Boolean).join(" · ");
      return `
        <div class="target-row" data-entity="${esc(stateObj.entity_id)}" role="button" tabindex="0">
          <div class="grow"><div class="target-name">${esc(name)}</div><div class="sub">${esc(sub)}</div></div>
          <div>${fmtMs(a.response_time_ms)}</div>
          <div class="pill ${status}">${esc(statusLabel(status))}</div>
        </div>`;
    }).join("");

    this.shadowRoot.innerHTML = `
      <style>${PROBULATOR_STYLE}</style>
      <ha-card>
        <div class="wrap">
          <div class="header"><div class="grow"><div class="name">${esc(this._config.title)}</div>${this._config.group ? `<div class="sub">Group: ${esc(this._config.group)}</div>` : ""}</div></div>
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
  getGridOptions() { return { columns: 12, rows: 3 }; }

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
  }

  static getStubConfig() {
    return {
      title: "HA Probulator Manager",
      sort: "status",
      show_actions: true,
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
  getGridOptions() { return { columns: 12, rows: 6 }; }

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
      return `
        <div class="manager-row" data-search="${esc(search)}" data-group="${esc(String(a.group || "").toLowerCase())}">
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
          <div class="manager-toolbar">
            <input class="manager-input" type="search" aria-label="Search HA Probulator targets" placeholder="Search targets, addresses, groups, states…" value="${esc(this._search)}">
            ${groupControl}
          </div>
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
