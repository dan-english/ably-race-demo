<template>
  <div class="laptimes">
    <div
      style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
      "
    >
      <div style="flex: 1"></div>
      <h3 style="margin: 0; flex: 1; text-align: center">Lap Times</h3>
      <div style="flex: 1; display: flex; justify-content: flex-end">
        <div
          style="
            padding: 4px 12px;
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 11px;
          "
        >
          {{ $race_lap_ably_channel }} <br />
          {{ $laptime_ably_event }}
        </div>
      </div>
    </div>
    <p>(rewind 20 messages)</p>

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

<style scoped>
h3 {
  margin-bottom: 0px;
}
p {
  margin: 2px;
  padding-bottom: 10px;
  border-bottom: 1px solid #696969;
  font-size: 12px;
  font-style: italic;
  color: #696969;
}
</style>
