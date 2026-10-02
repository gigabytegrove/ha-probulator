import { pathToFileURL } from "node:url";
import { resolve } from "node:path";

const registry = new Map();

class ShadowRootStub {
  innerHTML = "";
  querySelector() {
    return {
      addEventListener() {},
      style: { setProperty() {}, removeProperty() {} },
    };
  }
  querySelectorAll() {
    return [];
  }
}

globalThis.HTMLElement = class {
  constructor() {
    this.style = { setProperty() {}, removeProperty() {} };
  }
  attachShadow() {
    this.shadowRoot = new ShadowRootStub();
    return this.shadowRoot;
  }
  dispatchEvent() {
    return true;
  }
};

globalThis.CustomEvent = class {
  constructor(type, init = {}) {
    this.type = type;
    this.detail = init.detail;
  }
};

registry.set("ha-form", class {});
globalThis.customElements = {
  define(name, ctor) {
    if (registry.has(name)) throw new Error(`duplicate custom element: ${name}`);
    registry.set(name, ctor);
  },
  get(name) {
    return registry.get(name);
  },
  whenDefined(name) {
    if (!registry.has(name)) throw new Error(`undefined custom element: ${name}`);
    return Promise.resolve();
  },
};

globalThis.document = {
  createElement(name) {
    return { tagName: name };
  },
};
globalThis.window = { customCards: [] };

await import(pathToFileURL(resolve("custom_components/ha_probulator/frontend/ha-probulator-cards.js")).href);

const expectedElements = [
  "probulator-card",
  "probulator-overview-card",
  "probulator-summary-card",
  "probulator-manager-card",
  "probulator-target-editor",
  "probulator-overview-editor",
  "probulator-summary-editor",
  "probulator-manager-editor",
];

for (const name of expectedElements) {
  if (!registry.has(name)) {
    throw new Error(`missing custom element registration: ${name}`);
  }
}

const registeredCards = new Set(window.customCards.map((card) => card.type));
for (const type of [
  "probulator-card",
  "probulator-overview-card",
  "probulator-summary-card",
  "probulator-manager-card",
]) {
  if (!registeredCards.has(type)) {
    throw new Error(`missing custom card registration: ${type}`);
  }
}

const TargetCard = registry.get("probulator-card");
const targetStub = TargetCard.getStubConfig();
if (
  targetStub.mode !== "normal"
  || targetStub.show_sparkline !== true
  || targetStub.show_jitter !== false
) {
  throw new Error("unexpected target card stub defaults");
}

for (const [cardName, editorName] of [
  ["probulator-card", "probulator-target-editor"],
  ["probulator-overview-card", "probulator-overview-editor"],
  ["probulator-summary-card", "probulator-summary-editor"],
  ["probulator-manager-card", "probulator-manager-editor"],
]) {
  const Card = registry.get(cardName);
  const editor = await Card.getConfigElement();
  if (editor.tagName !== editorName) {
    throw new Error(`${cardName} returned ${editor.tagName}, expected ${editorName}`);
  }
}

const target = new TargetCard();
target.setConfig({ entity: "binary_sensor.example", mode: "normal" });

target.hass = {
  states: {
    "binary_sensor.example": {
      entity_id: "binary_sensor.example",
      state: "on",
      attributes: {
        probulator: true,
        probulator_kind: "target",
        target_name: '<img src=x onerror="alert(1)">',
        target: "<script>alert(1)</script>",
        status: "online",
        response_time_ms: 5,
      },
    },
  },
};
if (
  target.shadowRoot.innerHTML.includes("<img src=x")
  || target.shadowRoot.innerHTML.includes("<script>alert")
) {
  throw new Error("target card rendered unescaped target-controlled HTML");
}
if (!target.shadowRoot.innerHTML.includes("&lt;img")) {
  throw new Error("target card did not visibly escape hostile target text");
}


const OverviewCard = registry.get("probulator-overview-card");
const overviewStub = OverviewCard.getStubConfig();
if ("title" in overviewStub) {
  throw new Error("overview card still injects a default title");
}
const overview = new OverviewCard();
overview.setConfig({ title: "HA Probulator", sort: "status" });
overview.hass = {
  states: {
    "binary_sensor.dns_1": {
      entity_id: "binary_sensor.dns_1",
      state: "on",
      attributes: {
        probulator: true,
        probulator_kind: "target",
        target_name: "DNS 1",
        target: "192.168.0.2:53",
        status: "online",
        response_time_ms: 1.7,
      },
    },
  },
};
if (overview.shadowRoot.innerHTML.includes(">HA Probulator<")) {
  throw new Error("legacy overview title was not suppressed");
}
const overviewGrid = overview.getGridOptions();
if (
  overviewGrid.rows !== "auto"
  || overviewGrid.columns !== "full"
  || overviewGrid.min_columns !== 6
) {
  throw new Error("overview card is not using responsive full-width grid sizing");
}

const targetGrid = target.getGridOptions();
if (
  targetGrid.rows !== "auto"
  || targetGrid.columns !== 6
  || targetGrid.min_columns !== 3
  || targetGrid.max_columns !== 12
) {
  throw new Error("target card is not exposing a flexible grid width range");
}

const ManagerCard = registry.get("probulator-manager-card");
const managerStub = ManagerCard.getStubConfig();
if (managerStub.show_bulk_actions !== true) {
  throw new Error("manager card bulk actions are not enabled by default");
}
const manager = new ManagerCard();
manager.setConfig({ title: "Manager", show_actions: true, show_bulk_actions: true });
const managerGrid = manager.getGridOptions();
if (
  managerGrid.rows !== "auto"
  || managerGrid.columns !== "full"
  || managerGrid.min_columns !== 6
) {
  throw new Error("manager card is not using responsive full-width grid sizing");
}

const SummaryCard = registry.get("probulator-summary-card");
const summary = new SummaryCard();
summary.setConfig({ title: "Summary" });
const summaryGrid = summary.getGridOptions();
if (
  summaryGrid.rows !== "auto"
  || summaryGrid.columns !== 12
  || summaryGrid.min_columns !== 6
  || summaryGrid.max_columns !== 12
) {
  throw new Error("summary card is not exposing a flexible grid width range");
}

let invalidModeRejected = false;
try {
  target.setConfig({ entity: "binary_sensor.example", mode: "not-a-mode" });
} catch {
  invalidModeRejected = true;
}
if (!invalidModeRejected) {
  throw new Error("target card accepted an invalid mode");
}

console.log("HA Probulator frontend smoke test passed");
