import { createApp } from "vue";
import App from "./App.vue";

import SectorTimes from "../dashboard/components/SectorTimes.vue";
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
app.config.globalProperties.$ably = ably;

app.component("SectorTimes", SectorTimes);
app.component("DRSstatus", DRSstatus);
app.component("RaceFlag", RaceFlag);
app.component("PitStatus", PitStatus);

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

app.mount("#rewind-app");
