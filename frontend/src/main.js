import { createApp } from "vue";
import App from "./App.vue";

import {
  debug,
  initAbly,
  ElementPlus,
  registerAblyConfig,
  registerGlobalComponents,
} from "./shared";

// ----------------------------
// Vue app
// ----------------------------

const ably = initAbly(process.env.VUE_APP_API_KEY);

const app = createApp(App);

app.use(ElementPlus);

app.use(debug);
app.config.globalProperties.$ably = ably;

registerGlobalComponents(app);
registerAblyConfig(app);

app.mount("#app");
