<template>
  <MenuBar active_page="debug"></MenuBar>

  <div class="common-layout">
    <el-container class="layout">
      <el-main>
        <StartRace></StartRace>
      </el-main>
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
        this.leftWidth = Math.max(120, this.startWidth + delta);
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
