<template>
  <el-table
    :data="tableData"
    stripe
    style="width: 100%"
    highlight-current-row
    :row-key="getRowKey"
    :current-row-key="currentRowKey"
    @row-click="handleRowClick"
  >
    <el-table-column prop="event" label="" />
  </el-table>
</template>
<script>
export default {
  name: "docs_events_table",
  data() {
    return {
      currentRowKey: "introdoc",

      tableData: [
        { event: "Intro", channel: "introdoc" },

        { event: "Telemetry", channel: "telemetry" },
        { event: "Sectors", channel: "sector_time" },
        { event: "Laps", channel: "lap_time" },
        { event: "Pitting", channel: "boxbox_status" },
        { event: "Flag", channel: "flag_status" },
        { event: "Config", channel: "configdoc" },
      ],
    };
  },
  mounted() {
    this.$debug.info("Ably Events ");
  },
  methods: {
    getRowKey(row) {
      return row.channel;
    },
    handleRowClick(row) {
      this.currentRowKey = row.channel;

      this.$emit("doc_event_changed", this.currentRowKey);
    },
  },
};
</script>
