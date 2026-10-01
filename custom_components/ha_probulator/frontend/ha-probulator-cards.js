const PROBULATOR_STYLE = `
  :host {
    --probulator-online-color: var(--success-color, #43a047);
    --probulator-degraded-color: var(--warning-color, #f9a825);
    --probulator-offline-color: var(--error-color, #d32f2f);
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
  .offline .dot { background:var(--probulator-offline-color); box-shadow:0 0 0 3px color-mix(in srgb, var(--probulator-offline-color) 18%, transparent); }
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
  .pill.offline { color:var(--probulator-offline-color); }
  .summary { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin-top:14px; }
  .summary-box { padding:12px; border-radius:10px; background:color-mix(in srgb, var(--primary-text-color) 5%, transparent); }
  .summary-box .n { font-size:1.35rem; font-weight:700; }
  .summary-box .l { color:var(--secondary-text-color); font-size:.75rem; margin-top:2px; }
  .footer { color:var(--secondary-text-color); font-size:.78rem; margin-top:12px; }
  @media (max-width: 520px) {
    .metric-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
    .summary { grid-template-columns:repeat(2,minmax(0,1fr)); }
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
  if (["online", "offline", "degraded", "probing"].includes(value)) return value;
  if (!stateObj) return "probing";
  if (stateObj.state === "on") return "online";
  if (stateObj.state === "off") return "offline";
  return "probing";
}

function probulatorTargets(hass, config = {}) {
  const requested = Array.isArray(config.entities) && config.entities.length
    ? new Set(config.entities)
    : null;
  const group = String(config.group || "").trim().toLowerCase();
  return Object.values(hass?.states || {})
    .filter((stateObj) => stateObj.entity_id.startsWith("binary_sensor."))
    .filter((stateObj) => stateObj.attributes?.probulator === true)
    .filter((stateObj) => stateObj.attributes?.probulator_kind === "target")
    .filter((stateObj) => !requested || requested.has(stateObj.entity_id))
    .filter((stateObj) => !group || String(stateObj.attributes?.group || "").toLowerCase() === group)
    .sort((a, b) => String(a.attributes?.target_name || a.attributes?.friendly_name || a.entity_id)
      .localeCompare(String(b.attributes?.target_name || b.attributes?.friendly_name || b.entity_id)));
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
    return { mode: "normal" };
  }

  setConfig(config) {
    if (!config || !config.entity) throw new Error("HA Probulator card requires an entity");
    this._config = { mode: "normal", ...config };
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
    const hostPort = a.host ? `${a.host}${a.port ? `:${a.port}` : ""}` : "";

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
          <div class="label">Minimum</div><div class="value">${fmtMs(a.min_response_time_ms)}</div>
          <div class="label">Maximum</div><div class="value">${fmtMs(a.max_response_time_ms)}</div>
          <div class="label">Failures</div><div class="value">${esc(a.failed_probes ?? "—")} total / ${esc(a.consecutive_failures ?? 0)} consecutive</div>
          <div class="label">Last success</div><div class="value">${esc(fmtTime(a.last_success))}</div>
          <div class="label">Last failure</div><div class="value">${esc(fmtTime(a.last_failure))}</div>
          ${a.last_error ? `<div class="label">Last error</div><div class="value">${esc(a.last_error)}</div>` : ""}
        </div>
        ${sparkline(a.latency_history)}
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
              <div class="status"><span class="dot"></span>${esc(status)}</div>
            </div>
            <div class="metric-grid">
              <div class="metric"><div class="value">${fmtMs(a.response_time_ms)}</div><div class="label">Response</div></div>
              <div class="metric"><div class="value">${fmtMs(a.average_response_time_ms)}</div><div class="label">Average</div></div>
              <div class="metric"><div class="value">${fmtPct(a.success_rate)}</div><div class="label">Success</div></div>
            </div>
            ${extended}
          </div>
        </ha-card>`;
    }

    const clickable = this.shadowRoot.querySelector('[role="button"]');
    clickable?.addEventListener("click", () => fireMoreInfo(this, stateObj.entity_id));
    clickable?.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") fireMoreInfo(this, stateObj.entity_id);
    });
  }
}

class ProbulatorOverviewCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  static getStubConfig() {
    return { title: "HA Probulator", mode: "normal" };
  }

  setConfig(config) {
    this._config = { title: "HA Probulator", mode: "normal", ...config };
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
      const sub = [a.host && `${a.host}${a.port ? `:${a.port}` : ""}`, a.group].filter(Boolean).join(" · ");
      return `
        <div class="target-row" data-entity="${esc(stateObj.entity_id)}" role="button" tabindex="0">
          <div class="grow"><div class="target-name">${esc(name)}</div><div class="sub">${esc(sub)}</div></div>
          <div>${fmtMs(a.response_time_ms)}</div>
          <div class="pill ${status}">${esc(status)}</div>
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
        if (event.key === "Enter" || event.key === " ") fireMoreInfo(this, entityId);
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
    const counts = { online: 0, degraded: 0, offline: 0, probing: 0 };
    const latencies = [];
    targets.forEach((stateObj) => {
      counts[stateStatus(stateObj)] += 1;
      const n = Number(stateObj.attributes?.response_time_ms);
      if (Number.isFinite(n)) latencies.push(n);
    });
    const avg = latencies.length ? latencies.reduce((a, b) => a + b, 0) / latencies.length : null;

    this.shadowRoot.innerHTML = `
      <style>${PROBULATOR_STYLE}</style>
      <ha-card>
        <div class="wrap">
          <div class="header"><div class="grow"><div class="name">${esc(this._config.title)}</div>${this._config.group ? `<div class="sub">Group: ${esc(this._config.group)}</div>` : ""}</div></div>
          <div class="summary">
            <div class="summary-box"><div class="n" style="color:var(--probulator-online-color)">${counts.online}</div><div class="l">Online</div></div>
            <div class="summary-box"><div class="n" style="color:var(--probulator-degraded-color)">${counts.degraded}</div><div class="l">Degraded</div></div>
            <div class="summary-box"><div class="n" style="color:var(--probulator-offline-color)">${counts.offline}</div><div class="l">Offline</div></div>
            <div class="summary-box"><div class="n">${fmtMs(avg)}</div><div class="l">Average response</div></div>
          </div>
          <div class="footer">${targets.length} target${targets.length === 1 ? "" : "s"}${counts.probing ? ` · ${counts.probing} still probing` : ""}</div>
        </div>
      </ha-card>`;
  }
}

if (!customElements.get("probulator-card")) customElements.define("probulator-card", ProbulatorCard);
if (!customElements.get("probulator-overview-card")) customElements.define("probulator-overview-card", ProbulatorOverviewCard);
if (!customElements.get("probulator-summary-card")) customElements.define("probulator-summary-card", ProbulatorSummaryCard);

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
      return { type: "custom:probulator-card", entity: entityId, mode: "normal" };
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

console.info(`%c HA Probulator %c cards loaded`, "background:#03a9f4;color:#fff;font-weight:700;padding:2px 5px;border-radius:3px", "");
