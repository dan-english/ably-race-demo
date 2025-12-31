<template>
  <div class="menu-container" :style="{ borderBottomColor: flagBorderColor }">
    <el-menu
      :default-active="activeIndex"
      class="el-menu"
      mode="horizontal"
      @select="handleSelect"
    >
      <el-menu-item index="1">Ably Racing Demo</el-menu-item>
      <el-menu-item index="2">Dashboard</el-menu-item>
      <el-menu-item index="3">Rewind</el-menu-item>
      <el-menu-item index="6">History</el-menu-item>
      <el-menu-item index="4" :disabled="debugTabDisabled">Race</el-menu-item>
      <el-menu-item index="5">Docs</el-menu-item>
    </el-menu>

    <div class="flag-wrapper">
      <PitStatus></PitStatus>
      <RaceFlag @flag-change="onFlagChange"></RaceFlag>
    </div>
  </div>
</template>

<script>
export default {
  name: "MenuBar",
  props: ["active_page"],

  data() {
    return {
      activeIndex: 1,
      currentFlag: "grey",
      debugTabDisabled: true,
      routes: {
        1: "/",
        2: "/dashboard",
        3: "/rewind",
        6: "/history",
        4: "/debug",
        5: "/docs",
      },
    };
  },

  mounted() {
    this.$debug.info("Menu Component");

    if (this.active_page == "docs") {
      this.activeIndex = 5;
    } else if (this.active_page == "rewind") {
      this.activeIndex = 3;
    } else if (this.active_page == "dashboard") {
      this.activeIndex = 2;
    } else if (this.active_page == "debug") {
      this.activeIndex = 4;
    } else if (this.active_page == "history") {
      this.activeIndex = 6;
    }

    this.debugTabDisabled = this.$debug_tab_disabled;
  },

  computed: {
    flagBorderColor() {
      const flag = this.currentFlag?.toLowerCase();
      return (flag && this.$flagColors[flag]?.fill) || "transparent";
    },
  },

  methods: {
    handleSelect(key) {
      const path = this.routes[key];
      if (path) {
        window.location.href = path;
      }
    },

    onFlagChange(flag) {
      this.currentFlag = flag;
    },
  },
};
</script>

<style scoped>
.el-menu {
  flex-grow: 1; /* menu takes remaining space */
  margin: 0;
  border: none;
}

.flag-wrapper {
  display: flex;
  align-items: center;
  margin-right: 10px;
}
</style>
