<template>
  <MenuBar
    active_page="docs"
    hide_flag="true"
    hide_drs="true"
    hide_pit="true"
  ></MenuBar>

  <div class="common-layout">
    <el-container class="layout">
      <!-- Left Aside -->
      <el-aside :width="leftWidth + 'px'">
        <AblyDocsTable @doc_event_changed="onEventChange"></AblyDocsTable>
      </el-aside>
      <div class="resizer" @mousedown="startResize('left')" />

      <el-main>
        <SectorEventDoc v-if="sectoreventdoc"></SectorEventDoc>
        <LapEventDoc v-if="lapeventdoc"></LapEventDoc>
        <BoxEventDoc v-if="boxeventdoc"></BoxEventDoc>
        <FlagEventDoc v-if="flageventdoc"></FlagEventDoc>
        <TelemetryEventDoc v-if="telemetrydoc"></TelemetryEventDoc>
        <IntroDoc v-if="introdoc"></IntroDoc>
        <ConfigDoc v-if="configdoc"></ConfigDoc>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      leftWidth: 250,
      maxLeftWidth: 250,

      resizing: null,
      startX: 0,
      startWidth: 0,
      activeName: "intro",

      sectoreventdoc: false,
      lapeventdoc: false,
      boxeventdoc: false,
      flageventdoc: false,
      telemetrydoc: false,
      configdoc: false,
      introdoc: true,
    };
  },

  methods: {
    handleClick() {},
    startResize(side) {
      this.resizing = side;
      this.startX = event.clientX;
      this.startWidth = side === "left" ? this.leftWidth : this.rightWidth;

      document.addEventListener("mousemove", this.onResize);
      document.addEventListener("mouseup", this.stopResize);
    },

    onResize(event) {
      const delta = event.clientX - this.startX;

      if (this.resizing === "left") {
        const newWidth = this.startWidth + delta;

        this.leftWidth = Math.min(this.maxLeftWidth, Math.max(120, newWidth));
      }

      if (this.resizing === "right") {
        const newWidth = this.startWidth - delta;

        this.rightWidth = Math.max(120, newWidth);
      }
    },

    stopResize() {
      document.removeEventListener("mousemove", this.onResize);
      document.removeEventListener("mouseup", this.stopResize);
      this.resizing = null;
    },

    onEventChange(event_channel) {
      const stateMap = {
        sector_time: "sectoreventdoc",
        lap_time: "lapeventdoc",
        boxbox_status: "boxeventdoc",
        flag_status: "flageventdoc",
        telemetry: "telemetrydoc",
        introdoc: "introdoc",
        configdoc: "configdoc",
      };
      // Reset all flags
      for (const key of Object.values(stateMap)) {
        this[key] = false;
      }

      // Enable only the relevant one
      if (stateMap[event_channel]) {
        this[stateMap[event_channel]] = true;
        this.activeName = this[stateMap[event_channel]];
      }
    },
  },
};
</script>

<style scoped>
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 20px; /* vertical spacing */
}

/* Center the gear horizontally */
.gear-wrapper {
  display: flex;
  justify-content: center;
  padding-top: 10px;
}

/* FuelAndTyres stays full width */
.fuel-tyres-wrapper {
  width: 100%;
}

.layout {
  height: 100vh;
}

/* Drag handle */

.resizer {
  width: 6px;
  cursor: col-resize;
  background-color: transparent;

  /* 👇 THIS IS THE IMPORTANT PART */
  height: 100%;
  align-self: stretch;
  position: relative;
}

.resizer::after {
  content: "";
  position: absolute;
  left: 2px;
  top: 0;
  bottom: 0; /* full height line */
  width: 2px;
  background-color: #ccc;
}

/* Hover feedback */
.resizer:hover::after {
  background-color: #409eff;
}
</style>
