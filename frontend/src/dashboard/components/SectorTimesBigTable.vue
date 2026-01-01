<template>
  <div class="sectortimes">
    <h3>Sector Times</h3>

    <el-table :data="tableData" stripe style="width: 100%">
      <el-table-column prop="lap" label="Lap" width="70px" v-if="show_extra" />
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
import * as Ably from "ably";
export default {
  name: "SectorTimesBigTable",

  data() {
    return {
      show_extra: true,
      tableData: [],
    };
  },
  mounted() {
    this.$debug.info("Sector Time Big Table Component");

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
      const rewindSectorClient = new Ably.Realtime({
        key: this.$ably_api_key,
      });

      const channel = rewindSectorClient.channels.get(
        this.$default_ably_channel,
        {
          params: { rewind: "100s" },
        }
      );

      channel.subscribe(this.$sectortime_ably_event, (message) => {
        this.$debug.group(
          `Sector Data Update Big Table (100s rewind): ${this.$sectortime_ably_event}`
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
