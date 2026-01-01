module.exports = {
  devServer: {
    client: {
      overlay: {
        errors: true,
        warnings: false,
        runtimeErrors: (error) => {
          const ignoreErrors = [
            "ResizeObserver loop completed with undelivered notifications.",
            "ResizeObserver loop limit exceeded",
          ];
          if (ignoreErrors.includes(error.message)) {
            return false;
          }
          return true;
        },
      },
    },
  },
  pages: {
    index: {
      entry: "src/main.js", // main app
      template: "public/index.html",
      filename: "index.html",
    },
    dashboard: {
      entry: "src/dashboard/main.js", // dashboard app
      template: "public/dashboard.html",
      filename: "dashboard.html",
    },
    docs: {
      entry: "src/docs/main.js", // docs app
      template: "public/docs.html",
      filename: "docs.html",
    },
    debug: {
      entry: "src/debug/main.js", // debug app
      template: "public/debug.html",
      filename: "debug.html",
    },
    rewind: {
      entry: "src/rewind/main.js", // rewind app
      template: "public/rewind.html",
      filename: "rewind.html",
    },
    history: {
      entry: "src/history/main.js", // history app
      template: "public/history.html",
      filename: "history.html",
    },
  },
  outputDir: "../dist",
  publicPath: "/",
};
