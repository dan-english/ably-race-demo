<template>
  <div class="sectortimes">
    <h3>
      Sector Times with Rewind
      <el-button size="small" type="primary" @click="start_listening"
        >Go</el-button
      >
    </h3>
    <sub><b>30 second rewind</b></sub>
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
  margin: 21px;
}
h3 {
  margin-bottom: 13px;
}
</style>
