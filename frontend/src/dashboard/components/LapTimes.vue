<template>
  <div class="laptimes">
    <h3>Lap Times</h3>

    <el-table :data="tableData" stripe style="width: 100%">
      <el-table-column prop="lap" label="Lap" width="50px" />
      <el-table-column
        prop="position"
        label="Position"
        width="80px"
        v-if="show_extra"
      />
      <el-table-column prop="lap_time_sec" label="Lap Time (sec)" />
      <el-table-column prop="best_lap_sec" label="Best Lap" v-if="show_extra" />
    </el-table>
  </div>
</template>

<script>
export default {
  name: "LapTimeTable",
  props: ["show_extra_columns", "custom_rewind"],
  data() {
    return {
      show_extra: false,
      tableData: [],
      rewind_count: 2,
    };
  },
  mounted() {
    this.$debug.info("Lap Time Component");

    if (this.show_extra_columns) {
      this.show_extra = true;
    }
    // if (this.custom_rewind) {
    //   this.rewind_count = this.custom_rewind;
    //   console.log("custom rewind to:" + this.custom_rewind);
    // }

    if (this.$ably && this.$race_lap_ably_channel && this.$laptime_ably_event) {
      this.subscribeToTelemetry();
    }
  },
  methods: {
    subscribeToTelemetry() {
      const channel = this.$ably.channels.get(this.$race_lap_ably_channel, {
        params: { rewind: this.rewind_count },
      });

      channel.subscribe(this.$laptime_ably_event, (message) => {
        this.$debug.group(`Lap Data Update: ${this.$laptime_ably_event}`);
        this.$debug.info(message.data);
        this.$debug.groupEnd();
        this.tableData.unshift(message.data);
      });

      this.$debug.ably_subscribed(
        this.$default_ably_channel,
        this.$laptime_ably_event,
        this.$options.name
      );
    },
  },
};
</script>
