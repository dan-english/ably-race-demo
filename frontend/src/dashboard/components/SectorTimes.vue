<template>
  <div class="">
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
          v-if="show_extra"
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
    <el-table :data="tableData" stripe style="width: 100%" height="350">
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
