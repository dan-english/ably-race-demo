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
      <h3 style="margin: 0; flex: 1; text-align: center">Sector Times</h3>
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
          {{ $sectortime_ably_event }}
        </div>
      </div>
    </div>
    <p>(rewind 100 seconds)</p>

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
