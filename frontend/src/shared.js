import debug from "./plugins/debug.js";
import ElementPlus from "element-plus";

import { initAbly } from "./ably";

import "element-plus/dist/index.css";
import "./assets/styles.css";

export const flagColors = {
  yellow: { fill: "#FFD700", stroke: "#FFC300" },
  green: { fill: "#00FF00", stroke: "#00CC00" },
  orange: { fill: "#FFA500", stroke: "#FF8C00" },
  red: { fill: "#FF0000", stroke: "#FF0000" },
  checkered: { fill: "white", stroke: "black" },
  "safety car": { fill: "#FFD700", stroke: "#FFD700" },
  vsc: { fill: "#FFA500", stroke: "#FFA500" },
  grey: { fill: "#ccc", stroke: "#ccc" },
};

export function registerAblyConfig(app) {
  app.config.globalProperties.$ably_api_key = process.env.VUE_APP_API_KEY;

  app.config.globalProperties.$default_ably_channel =
    process.env.VUE_APP_RACE_ABLY_CHANNEL;

  app.config.globalProperties.$race_lap_ably_channel =
    process.env.VUE_APP_RACE_LAP_ABLY_CHANNEL;

  app.config.globalProperties.$race_flag_ably_channel =
    process.env.VUE_APP_RACE_FLAG_ABLY_CHANNEL;

  app.config.globalProperties.$default_ably_weatherchannel =
    process.env.VUE_APP_ABLY_WEATHER_CHANNEL;

  app.config.globalProperties.$laptime_ably_event =
    process.env.VUE_APP_ABLY_LAPTIME_EVENT;

  app.config.globalProperties.$telemetry_ably_event =
    process.env.VUE_APP_ABLY_TELEMETRY_EVENT;

  app.config.globalProperties.$flag_status_ably_event =
    process.env.VUE_APP_ABLY_FLAG_STATUS_EVENT;

  app.config.globalProperties.$boxbox_status_ably_event =
    process.env.VUE_APP_ABLY_BOX_STATUS_EVENT;

  app.config.globalProperties.$pit_lane_speed =
    process.env.VUE_APP_ABLY_PIT_LANE_SPEED;

  app.config.globalProperties.$sectortime_ably_event =
    process.env.VUE_APP_ABLY_SECTORTIME_EVENT;

  app.config.globalProperties.$debug_tab_disabled =
    process.env.VUE_APP_DEBUG_TAB_DISABLED;

  app.config.globalProperties.$flagColors = flagColors;
}

export function registerGlobalComponents(app) {
  const requireComponent = require.context(
    "./components",
    false,
    /[A-Z]\w+\.(vue|js)$/
  );

  requireComponent.keys().forEach((fileName) => {
    const componentConfig = requireComponent(fileName);
    const componentName = fileName.replace(/^\.\/(.*)\.\w+$/, "$1");
    app.component(componentName, componentConfig.default || componentConfig);
    // console.log(componentName);
  });
}

export { debug, initAbly, ElementPlus };
