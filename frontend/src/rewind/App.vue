<template>
  <MenuBar active_page="rewind"></MenuBar>

  <div class="common-layout">
    <el-container class="layout">
      <el-aside :width="leftWidth + 'px'">
        <SectorRewind></SectorRewind>
      </el-aside>

      <div class="resizer" @mousedown="startResize('left')" />

      <el-main>
        <SectorTimes show_extra_columns="true"></SectorTimes>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      //   leftWidth: 600,

      rightWidth: 0,
      resizing: null,
      startX: 0,
      startWidth: 0,
      activeName: "intro",

      sectoreventdoc: false,
      lapeventdoc: false,
      boxeventdoc: false,
      flageventdoc: false,
      telemetrydoc: false,
      introdoc: true,
    };
  },
  computed: {
    leftWidth() {
      return Math.floor(window.innerWidth * 0.5); // 60% of viewport
    },
    maxLeftWidth() {
      return Math.floor(window.innerWidth * 0.5); // 60% of viewport
    },
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
  padding-top: 20px;
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
