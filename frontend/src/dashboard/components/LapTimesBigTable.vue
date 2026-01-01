<template>
  <div class="laptimes">
    <h3>Lap Times</h3>

    <el-table :data="tableData" stripe style="width: 100%">
      <el-table-column prop="lap" label="Lap" width="70px" />
      <el-table-column prop="position" label="Position" width="100px" />
      <el-table-column prop="lap_time_sec" label="Lap Time (sec)" />
      <el-table-column prop="best_lap_sec" label="Best Lap" />
    </el-table>
  </div>
</template>

<script>
import * as Ably from "ably";

export default {
  name: "LapTimeBigTable",
  data() {
    return {
      tableData: [],
      rewind_count: 20,
    };
  },
  mounted() {
    this.$debug.info("Lap Time Big Table Component");

    if (this.$ably && this.$race_lap_ably_channel && this.$laptime_ably_event) {
      this.subscribeToTelemetry();
    }
  },
  methods: {
    subscribeToTelemetry() {
      const rewindLapClient = new Ably.Realtime({
        key: this.$ably_api_key,
      });

      const channel = rewindLapClient.channels.get(
        this.$race_lap_ably_channel,
        {
          params: { rewind: this.rewind_count },
        }
      );

      channel.subscribe(this.$laptime_ably_event, (message) => {
        this.$debug.group(
          `Lap Data Update Big Table: ${this.$laptime_ably_event}`
        );
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
