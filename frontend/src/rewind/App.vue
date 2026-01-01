<template>
  <MenuBar
    active_page="rewind"
    hide_flag="true"
    hide_drs="true"
    hide_pit="true"
  />

  <div class="common-layout">
    <el-container class="layout two-column">
      <el-aside class="left-pane">
        <SectorRewind />
      </el-aside>

      <el-main class="right-pane">
        <SectorTimes show_extra_columns="true" />
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  computed: {},

  methods: {},
};
</script>
<style scoped>
.layout {
  height: 100vh;
  display: flex;
}

/* Force exact 50/50 */
.left-pane,
.right-pane {
  width: 50%;
  overflow: auto;
}

/* Vertical divider */
.left-pane {
  border-right: 2px solid #e0e0e0;
}

/* Optional: match Element Plus theme on hover */
.left-pane:hover {
  border-right-color: #409eff;
}
</style>
