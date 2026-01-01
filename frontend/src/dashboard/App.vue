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
            <TyreGauge></TyreGauge>

            <div class="gear-wrapper">
              <TyreDeg></TyreDeg>
            </div>
          </el-tab-pane>
          <el-tab-pane label="Fuel" name="fuel">
            <FuelGauge></FuelGauge>
          </el-tab-pane>

          <el-tab-pane label="Laps" name="laptimes">
            <LapTimesBigTable></LapTimesBigTable>
          </el-tab-pane>

          <el-tab-pane label="Sectors" name="sectortimes">
            <SectorTimesBigTable></SectorTimesBigTable>
          </el-tab-pane>
        </el-tabs>
      </el-main>

      <div class="resizer" @mousedown="startResize('right')" />

      <el-aside :width="rightWidth + 'px'" class="right-panel">
        <div class="right-panel-content">
          <div class="gear-wrapper">
            <Gear></Gear>
          </div>

          <div class="gear-wrapper">
            <SpeedGauge></SpeedGauge>
          </div>

          <div class="fuel-tyres-wrapper">
            <BasicFuel></BasicFuel>
          </div>
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
      isMobile: false,
      rafPending: false,
    };
  },
  mounted() {
    this.checkMobile();
    window.addEventListener("resize", this.checkMobile);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
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
      // Use requestAnimationFrame to throttle resize updates
      if (!this.rafPending) {
        this.rafPending = true;
        requestAnimationFrame(() => {
          const delta = event.clientX - this.startX;

          if (this.resizing === "left") {
            this.leftWidth = Math.max(120, this.startWidth + delta);
          }

          if (this.resizing === "right") {
            this.rightWidth = Math.max(120, this.startWidth - delta);
          }

          this.rafPending = false;
        });
      }
    },

    stopResize() {
      document.removeEventListener("mousemove", this.onResize);
      document.removeEventListener("mouseup", this.stopResize);
      this.resizing = null;
      this.rafPending = false;
    },
    checkMobile() {
      this.isMobile = window.innerWidth < 768;
    },
  },
};
</script>

<style scoped>
/* Hover feedback */
.resizer:hover::after {
  background-color: #409eff;
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

.layout {
  height: 100vh;
}

/* Right panel centering */
.right-panel {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.right-panel-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  padding: 10px;
  gap: 20px;
}

.gear-wrapper,
.fuel-tyres-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 100%;
}

/* Mobile: stack everything vertically */
@media (max-width: 767px) {
  .layout {
    flex-direction: column;
    height: auto; /* allow content to dictate total height */
  }

  /* Make all aside and main full width */
  el-aside,
  el-main {
    width: 100% !important;
    min-width: auto !important;
  }

  /* Left panel (LapTimes + SectorTimes) */
  el-aside:first-of-type {
    order: 1;
  }

  /* Center panel (BoxBox + tabs) */
  el-main {
    order: 2;
    flex: 1 0 auto; /* allow it to grow */
    display: flex;
    flex-direction: column;
    min-height: 400px; /* ensures some usable height for tabs */
  }

  /* Right panel (Gear + Speed + Fuel) */
  el-aside:last-of-type {
    order: 3;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
  }

  /* Make gear/fuel blocks full width on mobile */
  .gear-wrapper,
  .fuel-tyres-wrapper {
    width: 100%;
    padding: 5px 0;
  }

  /* Hide resizers */
  .resizer {
    display: none;
  }

  /* Tabs scrollable */
  .demo-tabs :deep(.el-tabs__header) {
    overflow-x: auto;
    white-space: nowrap;
  }

  .demo-tabs :deep(el-tabs__item) {
    min-width: 120px;
    font-size: 16px;
    padding: 10px 15px;
  }

  .demo-tabs :deep(.el-tabs__active-bar) {
    width: auto !important;
  }
}
</style>
