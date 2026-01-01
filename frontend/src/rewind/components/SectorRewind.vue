<template>
  <div class="sectortimes">
    <div
      style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
      "
    >
      <div style="flex: 1"></div>
      <h3 style="margin: 0; flex: 2; text-align: center">
        Sector Times with 30 Second Rewind

        <el-button size="small" type="primary" @click="start_listening"
          >Go</el-button
        >
      </h3>

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
          {{ $default_ably_channel }} <br />
          {{ $telemetry_ably_event }}
        </div>
      </div>
    </div>
  </div>

  <div class="sectortimes">
    <el-table :data="tableData" stripe style="width: 100%">
      <el-table-column prop="lap" label="Lap" width="50px" />
      <el-table-column prop="sector" label="Sector" />
      <el-table-column prop="sector_time_sec" label="Sector Time (sec)" />
      <el-table-column prop="lap_time_sec" label="Lap Time (sec)" />
      <el-table-column prop="position" label="Position" width="100px" />
    </el-table>
  </div>
</template>

<script>
import * as Ably from "ably";
export default {
  name: "SectorRewindTimes",

  mounted() {
    this.$debug.info("Sector Rewind Time Component");
  },
  data() {
    return {
      tableData: [],
    };
  },
  methods: {
    start_listening() {
      if (
        this.$ably &&
        this.$default_ably_channel &&
        this.$sectortime_ably_event
      ) {
        this.subscribeToTelemetry();
      }
    },

    subscribeToTelemetry() {
      const rewindClient = new Ably.Realtime({
        key: this.$ably_api_key,
      });

      const channel = rewindClient.channels.get(this.$default_ably_channel, {
        params: { rewind: "30s" },
      });

      channel.subscribe(this.$sectortime_ably_event, (message) => {
        this.$debug.group(
          `Sector Data Update (rewind): ${this.$sectortime_ably_event}`
        );
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
<style scoped>
.sectortimes {
  margin: 14px;
}

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
