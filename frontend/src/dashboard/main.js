import { createApp } from "vue";
import App from "./App.vue";

import Highcharts from "highcharts";

import HighchartsMore from "highcharts/highcharts-more";
import SolidGauge from "highcharts/modules/solid-gauge";
import HighchartsMap from "highcharts/modules/map";

// Configure Highcharts - Fixed initialization
if (typeof HighchartsMore === "function") {
  HighchartsMore(Highcharts);
} else if (
  HighchartsMore.default &&
  typeof HighchartsMore.default === "function"
) {
  HighchartsMore.default(Highcharts);
}

if (typeof SolidGauge === "function") {
  SolidGauge(Highcharts);
} else if (SolidGauge.default && typeof SolidGauge.default === "function") {
  SolidGauge.default(Highcharts);
}

// Initialize the modules
if (typeof HighchartsMap === "function") {
  HighchartsMap(Highcharts);
} else if (
  HighchartsMap.default &&
  typeof HighchartsMap.default === "function"
) {
  HighchartsMap.default(Highcharts);
}

Highcharts.setOptions({
  time: {
    useUTC: false,
  },
  accessibility: { enabled: false },
  lang: {
    thousandsSep: "",
    locale: "en-GB",
  },
  credits: {
    enabled: true,
    text: "Driven By Ably",
    href: "https://ably.com",
  },
});

import {
  debug,
  initAbly,
  ElementPlus,
  registerAblyConfig,
  registerGlobalComponents,
} from "../shared";

// ----------------------------
// Vue app
// ----------------------------

const ably = initAbly(process.env.VUE_APP_API_KEY);

const app = createApp(App);

app.use(ElementPlus);
app.use(debug);
app.config.globalProperties.$ably = ably;
app.config.globalProperties.$Highcharts = Highcharts;

export function registerLocalComponents(app) {
  const requireLocalComponent = require.context(
    "./components",
    false,
    /[A-Z]\w+\.(vue|js)$/
  );

  requireLocalComponent.keys().forEach((fileName) => {
    const componentConfig = requireLocalComponent(fileName);
    const componentName = fileName.replace(/^\.\/(.*)\.\w+$/, "$1");

    app.component(componentName, componentConfig.default || componentConfig);
  });
}

registerLocalComponents(app);

registerGlobalComponents(app);
registerAblyConfig(app);

app.mount("#dashboard-app");
