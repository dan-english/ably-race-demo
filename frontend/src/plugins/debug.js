export default {
  install(app) {
    // Read from env (Vue CLI exposes VUE_APP_*)
    const app_debug =
      process.env.VUE_APP_DEBUG === "true" ||
      process.env.VUE_APP_DEBUG === true;

    if (process.env.VUE_APP_DEBUG === undefined) {
      console.error(
        "**** VUE_APP_DEBUG flag not found - please update your .env file ****"
      );
    }

    const debug = {
      //ably specific start
      ably_subscribed: function (channel_name, event_name, component_name) {
        if (app_debug === true) {
          console.log(
            `%c✅ Subscribed To Channel: ${channel_name}:${event_name} (Component: ${component_name})`,
            "color: #384D69; font-size: normal; font-weight: normal;"
          );
        }
      },

      //ably specific end
      flag(color) {
        if (!color) return;

        const normalizedColor = color.toLowerCase().replace(/\s+/g, "");

        const key = Object.keys(window.$flagColors || {}).find(
          (k) => k.replace(/\s+/g, "").toLowerCase() === normalizedColor
        );

        const bgColor = key ? window.$flagColors[key].fill : "white";
        const flagText =
          color.charAt(0).toUpperCase() + color.slice(1) + " Flag";

        console.log(
          `%c${flagText}`,
          `background:${bgColor}; color:black; font-weight:bold; padding:2px 6px; border-radius:4px;`
        );
      },

      //ably specific end
      group(message) {
        if (app_debug === true) {
          console.groupCollapsed(
            "%c" + message,
            "color:#228B22;font-weight:bold;"
          );
        }
      },

      groupEnd() {
        if (app_debug === true) {
          console.groupEnd();
        }
      },

      infoWarn: function (message) {
        if (app_debug === true) {
          if (typeof message == "string") {
            console.info(
              "%c" + "[w] " + message,
              "color: #999900; font-size: normal;font-weight:bold;font-style:italic"
            );
          } else {
            console.info(message);
          }
        }
      },

      infoError: function (message) {
        if (app_debug === true) {
          if (typeof message == "string") {
            console.info(
              "%c" + "[e] " + message,
              "color: red; font-size: normal;font-weight:bold;font-style:italic"
            );
          } else {
            console.info(message);
          }
        }
      },

      msg: function (message) {
        app_debug === true
          ? console.debug(
              "%c" + message,
              "color: green; font-size: normal;font-weight:bold;"
            )
          : undefined;
      },

      log: function (message) {
        if (app_debug === true) {
          if (typeof message == "string") {
            console.log(
              "%c" + message,
              "color: #384D69; font-size: normal;font-weight:normal;"
            );
          } else {
            console.log(message);
          }
        }
      },

      warn: function (message) {
        app_debug === true
          ? console.warn(
              "%c" + message,
              "color: #84D69; font-size: normal;font-weight:bold;"
            )
          : undefined;
      },
      error: function (message) {
        app_debug === true
          ? console.error(
              "%c" + message,
              "color: #384D69; font-size: normal;font-weight:bold;"
            )
          : undefined;
      },
      table: function (dataArray) {
        app_debug === true ? console.table(dataArray) : undefined;
      },

      image: function (t) {
        if (app_debug === true) {
          console.log(
            "%c    ",
            "font-size:300px; background-size: 100% 100%; background:url(" +
              t +
              ") no-repeat;"
          );
        }
      },

      config(data) {
        data.app_debug_enabled = app_debug;

        console.groupCollapsed(
          "%cConfiguration",
          "color:#384D69;font-size: normal;font-weight:bold;"
        );
        console.table(data);

        console.groupEnd();
      },

      info_doc(message) {
        if (app_debug === true) {
          if (typeof message === "string") {
            console.info(
              "%c[i] " + message,
              "color: green; font-weight:bold; font-style:italic;"
            );
          } else {
            console.info(message);
          }
        }
      },

      info(message) {
        if (app_debug === true) {
          if (typeof message === "string") {
            console.info(
              "%c[i] " + message,
              "color: blue; font-weight:bold; font-style:italic;"
            );
          } else {
            console.info(message);
          }
        }
      },
    };

    // Make it available everywhere
    app.config.globalProperties.$debug = debug;
  },
};
