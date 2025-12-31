<template>
  <MenuBar active_page="dashboard"></MenuBar>

  <div class="common-layout">
    <el-container class="layout">
      <!-- Left Aside -->
      <el-aside :width="leftWidth + 'px'">
        <LapTimes></LapTimes>
        <SectorTimes></SectorTimes>
      </el-aside>
      <div class="resizer" @mousedown="startResize('left')" />

      <el-main>
        <BoxBox></BoxBox>

        <el-tabs
          v-model="activeName"
          class="demo-tabs"
          @tab-click="handleClick"
        >
          <el-tab-pane label="Race Data Table" name="data_table_view">
            <RaceDataTable></RaceDataTable>
          </el-tab-pane>
          <el-tab-pane label="Tyres" name="tyres">
            <div class="fuel-tyres-wrapper">
              <TyreGauge></TyreGauge>
            </div>
            <div class="gear-wrapper">
              <TyreDeg></TyreDeg>
            </div>
          </el-tab-pane>
          <el-tab-pane label="Fuel" name="fuel">
            <FuelGauge></FuelGauge>
          </el-tab-pane>

          <el-tab-pane label="Sectors" name="sectortimes">
            <SectorTimesBigTable></SectorTimesBigTable>
          </el-tab-pane>

          <el-tab-pane label="Laps" name="laptimes">
            <LapTimesBigTable></LapTimesBigTable>
          </el-tab-pane>
        </el-tabs>
      </el-main>

      <div class="resizer" @mousedown="startResize('right')" />

      <el-aside :width="rightWidth + 'px'" class="right-panel">
        <div class="gear-wrapper">
          <Gear></Gear>
        </div>

        <div class="gear-wrapper">
          <SpeedGauge></SpeedGauge>
        </div>

        <div class="fuel-tyres-wrapper">
          <BasicFuel></BasicFuel>
        </div>
      </el-aside>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      leftWidth: 400,
      rightWidth: 400,
      resizing: null,
      startX: 0,
      startWidth: 0,
      activeName: "data_table_view",
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
        this.leftWidth = Math.max(120, this.startWidth + delta);
      }

      if (this.resizing === "right") {
        this.rightWidth = Math.max(120, this.startWidth - delta);
      }
    },

    stopResize() {
      document.removeEventListener("mousemove", this.onResize);
      document.removeEventListener("mouseup", this.stopResize);
      this.resizing = null;
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
