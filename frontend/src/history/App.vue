<template>
  <MenuBar active_page="history"></MenuBar>

  <div class="common-layout">
    <el-container class="layout">
      <el-aside :width="leftWidth + 'px'"><!-- no left nav--> </el-aside>

      <div class="resizer" @mousedown="startResize('left')" />

      <el-main>
        <HistoryData
          @history_filter_changed="filter_changed"
          :filter_option="activeName"
        ></HistoryData>
      </el-main>

      <div class="resizer" @mousedown="startResize('right')" />

      <el-aside :width="rightWidth + 'px'" class="right-panel">
        <SectorEventDoc v-if="sectoreventdoc" hide_desc="1"></SectorEventDoc>
        <LapEventDoc v-if="lapeventdoc" hide_desc="1"></LapEventDoc>
        <BoxEventDoc v-if="boxeventdoc" hide_desc="1"></BoxEventDoc>
        <FlagEventDoc v-if="flageventdoc" hide_desc="1"></FlagEventDoc>
        <TelemetryEventDoc
          v-if="telemetrydoc"
          hide_desc="1"
        ></TelemetryEventDoc>
      </el-aside>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      leftWidth: 1,
      maxLeftWidth: 1,
      rightWidth: 500,
      resizing: null,
      startX: 0,
      startWidth: 0,
      activeName: "intro",

      sectoreventdoc: false,
      lapeventdoc: false,
      boxeventdoc: false,
      flageventdoc: false,
      telemetrydoc: false,
    };
  },

  methods: {
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

    filter_changed(new_filter) {
      console.log("docs frame shoudl show: " + new_filter);

      const stateMap = {
        sector_time: "sectoreventdoc",
        lap_time: "lapeventdoc",
        boxbox_status: "boxeventdoc",
        flag_status: "flageventdoc",
        telemetry: "telemetrydoc",
      };
      // Reset all flags
      for (const key of Object.values(stateMap)) {
        this[key] = false;
      }

      // Enable only the relevant one
      if (stateMap[new_filter]) {
        this[stateMap[new_filter]] = true;
        this.activeName = this[stateMap[new_filter]];
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
