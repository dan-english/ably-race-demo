import { createApp } from "vue";
import App from "./App.vue";

import Prism from "prismjs";
import "prismjs/themes/prism-tomorrow.css";
import "prismjs/components/prism-python";
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-css";
import "prismjs/components/prism-markup";
import "prismjs/components/prism-json";
import "prismjs/components/prism-bash";
import "prismjs/components/prism-ini";
import "prismjs/components/prism-yaml";

import "prismjs/plugins/line-numbers/prism-line-numbers.js";
import "prismjs/plugins/line-numbers/prism-line-numbers.css";

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

app.config.globalProperties.$Prism = Prism;

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
app.mount("#docs-app");
