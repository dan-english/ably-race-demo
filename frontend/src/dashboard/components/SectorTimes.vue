<template>
  <div class="sectortimes">
    <h3>Sector Times</h3>

    <el-table :data="tableData" stripe style="width: 100%">
      <el-table-column prop="lap" label="Lap" width="50px" v-if="show_extra" />
      <el-table-column prop="sector" label="Sector" />
      <el-table-column prop="sector_time_sec" label="Sector Time (sec)" />
      <el-table-column
        prop="lap_time_sec"
        label="Lap Time (sec)"
        v-if="show_extra"
      />

      <el-table-column
        prop="position"
        label="Position"
        width="100px"
        v-if="show_extra"
      />
    </el-table>
  </div>
</template>

<script>
export default {
  name: "SectorTimes",
  props: ["show_extra_columns"],

  data() {
    return {
      show_extra: false,
      tableData: [],
    };
  },
  mounted() {
    this.$debug.info("Sector Time Component");

    if (this.show_extra_columns) {
      this.show_extra = true;
    }

    if (
      this.$ably &&
      this.$default_ably_channel &&
      this.$sectortime_ably_event
    ) {
      this.subscribeToTelemetry();
    }
  },
  methods: {
    subscribeToTelemetry() {
      const channel = this.$ably.channels.get(this.$default_ably_channel);

      channel.subscribe(this.$sectortime_ably_event, (message) => {
        this.$debug.group(`Sector Data Update: ${this.$sectortime_ably_event}`);
        this.$debug.info(message.data);
        this.$debug.groupEnd();
        this.tableData.unshift(message.data);
      });

      this.$debug.ably_subscribed(
        this.$default_ably_channel,
        this.$sectortime_ably_event,
        this.$options.name
      );

      //
    },
  },
};
</script>
