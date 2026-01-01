<template>
  <div class="race_data_table">
    <el-table :data="tableData" stripe style="width: 100%" height="750">
      <el-table-column prop="lap" label="Lap" width="70" />
      <el-table-column prop="position" label="Position" width="90" />
      <el-table-column prop="section" label="Section" />
      <el-table-column prop="speed_kmh" label="Speed (km/h)" width="90" />
      <el-table-column prop="gear" label="Gear" width="60" />

      <!-- DRS column with color -->
      <el-table-column label="DRS" width="80">
        <template #default="{ row }">
          <span
            :style="{ color: row.drs ? 'green' : 'red', fontWeight: 'bold' }"
          >
            {{ row.drs ? "ON" : "OFF" }}
          </span>
        </template>
      </el-table-column>

      <!-- Fuel column with conditional color -->
      <el-table-column label="Fuel (kg)" width="100">
        <template #default="{ row }">
          <span
            :style="{
              color: row.fuel_kg < 50 ? 'red' : 'black',
              fontWeight: row.fuel_kg < 50 ? 'bold' : 'normal',
            }"
          >
            {{ (row.fuel_kg ?? 0).toFixed(2) }}
          </span>
        </template>
      </el-table-column>

      <el-table-column label="Tyres" width="180">
        <template #default="{ row }">
          <div v-if="row.tyres" class="tyre-grid">
            <span
              class="tyre-status"
              :style="{ backgroundColor: tyreColor(row.tyres.FL) }"
            >
              FL {{ row.tyres.FL.toFixed(0) }}%
            </span>
            <span
              class="tyre-status"
              :style="{ backgroundColor: tyreColor(row.tyres.FR) }"
            >
              FR {{ row.tyres.FR.toFixed(0) }}%
            </span>
            <span
              class="tyre-status"
              :style="{ backgroundColor: tyreColor(row.tyres.RL) }"
            >
              RL {{ row.tyres.RL.toFixed(0) }}%
            </span>
            <span
              class="tyre-status"
              :style="{ backgroundColor: tyreColor(row.tyres.RR) }"
            >
              RR {{ row.tyres.RR.toFixed(0) }}%
            </span>
          </div>
        </template>
      </el-table-column>

      <!-- In Pit column with color -->
      <el-table-column label="In Pit" width="80">
        <template #default="{ row }">
          <span
            :style="{
              color: row.in_pit ? 'orange' : 'black',
              fontWeight: row.in_pit ? 'bold' : 'normal',
            }"
          >
            {{ row.in_pit ? "IN PIT" : "NO" }}
          </span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "RaceDataTable",
  props: [],
  mounted() {
    this.$debug.info("Race Data Table");

    if (
      this.$ably &&
      this.$default_ably_channel &&
      this.$telemetry_ably_event
    ) {
      this.subscribeToTelemetry();
    }
  },
  data() {
    return {
      tableData: [],
      debug: false,
    };
  },

  methods: {
    subscribeToTelemetry() {
      const channel = this.$ably.channels.get(this.$default_ably_channel);

      channel.subscribe(this.$telemetry_ably_event, (message) => {
        // prepend new data to table
        this.tableData.unshift(message.data);

        // Trim excess items beyond 50 in-place
        if (this.tableData.length > 50) {
          this.tableData.splice(50); // removes all items after index 49
        }
      });

      this.$debug.ably_subscribed(
        this.$default_ably_channel,
        this.$telemetry_ably_event,
        this.$options.name
      );
      //
    },
    tyreColor(wear) {
      if (wear < 30) return "#28B463"; // green
      if (wear < 60) return "#F1C40F"; // yellow
      return "#E74C3C"; // red
    },
  },
};
</script>
<style scoped>
.tyre-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2px; /* slightly smaller gap */
  text-align: center;
}

.tyre-status {
  padding: 1px 3px; /* smaller padding */
  border-radius: 3px;
  color: white;
  font-weight: bold;
  font-size: 0.7rem; /* smaller font */
}
</style>
