import { createApp } from "vue";
import App from "./App.vue";

import Prism from "prismjs";
import "prismjs/themes/prism-tomorrow.css";

import "prismjs/components/prism-python";
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-json";
import "prismjs/components/prism-ini";
import "prismjs/components/prism-yaml";

import "prismjs/plugins/line-numbers/prism-line-numbers.js";
import "prismjs/plugins/line-numbers/prism-line-numbers.css";

import BoxEventDoc from "../docs/components/BoxEventDoc.vue";
import FlagEventDoc from "../docs/components/FlagEventDoc.vue";
import SectorEventDoc from "../docs/components/SectorEventDoc.vue";
import TelemetryEventDoc from "../docs/components/TelemetryEventDoc.vue";
import LapEventDoc from "../docs/components/LapEventDoc.vue";

import DRSstatus from "../dashboard/components/DRSstatus.vue";
import PitStatus from "../dashboard/components/PitStatus.vue";
import RaceFlag from "../dashboard/components/RaceFlag.vue";

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
app.config.globalProperties.$Prism = Prism;
app.config.globalProperties.$ably = ably;

app.component("DRSstatus", DRSstatus);
app.component("RaceFlag", RaceFlag);
app.component("PitStatus", PitStatus);

app.component("BoxEventDoc", BoxEventDoc);
app.component("FlagEventDoc", FlagEventDoc);
app.component("SectorEventDoc", SectorEventDoc);
app.component("TelemetryEventDoc", TelemetryEventDoc);
app.component("LapEventDoc", LapEventDoc);

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
app.mount("#history-app");
