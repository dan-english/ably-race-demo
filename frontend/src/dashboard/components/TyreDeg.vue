<template>
  <div class="tyre-grid">
    <div v-for="tyre in tyres" :key="tyre.key" class="tyre-cell">
      <div class="tyre-label">{{ tyre.key }}</div>

      <div class="tyre-bar-background">
        <div
          class="tyre-bar-fill"
          :style="{
            height: tyrePercentage(tyre.value) + '%',
            backgroundColor: tyreColor(tyre.value),
          }"
        ></div>
      </div>

      <div class="tyre-value">{{ tyre.value.toFixed(1) }}%</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TyreWearGauge",

  data() {
    return {
      tyreMap: {
        FL: 0,
        FR: 0,
        RL: 0,
        RR: 0,
      },
    };
  },

  computed: {
    // Explicit layout order: FL FR / RL RR
    tyres() {
      return [
        { key: "FL", value: this.tyreMap.FL },
        { key: "FR", value: this.tyreMap.FR },
        { key: "RL", value: this.tyreMap.RL },
        { key: "RR", value: this.tyreMap.RR },
      ];
    },
  },

  mounted() {
    if (
      this.$ably &&
      this.$default_ably_channel &&
      this.$telemetry_ably_event
    ) {
      this.subscribeToTelemetry();
    }
  },

  methods: {
    tyrePercentage(wear) {
      return Math.max(0, 100 - wear);
    },

    tyreColor(wear) {
      if (wear < 30) return "#28B463";
      if (wear < 60) return "#F1C40F";
      return "#E74C3C";
    },

    subscribeToTelemetry() {
      const channel = this.$ably.channels.get(this.$default_ably_channel);

      channel.subscribe(this.$telemetry_ably_event, (message) => {
        const t = message.data.tyres;
        if (!t) return;

        this.tyreMap.FL = t.FL ?? this.tyreMap.FL;
        this.tyreMap.FR = t.FR ?? this.tyreMap.FR;
        this.tyreMap.RL = t.RL ?? this.tyreMap.RL;
        this.tyreMap.RR = t.RR ?? this.tyreMap.RR;
      });
    },
  },
};
</script>

<style scoped>
.tyre-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px 16px;

  min-height: 180px; /* 🔑 ensures visibility */
}

.tyre-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50px;
}

.tyre-label {
  font-size: 12px;
  margin-bottom: 4px;
  color: #ccc;
}

.tyre-bar-background {
  width: 100%;
  height: 140px;
  background: #222;
  border: 2px solid #555;
  border-radius: 6px;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
}

.tyre-bar-fill {
  width: 100%;
  transition: height 1s cubic-bezier(0.25, 0.8, 0.25, 1), background-color 0.5s;
}

.tyre-value {
  margin-top: 4px;
  font-size: 11px;
  color: #fff;
}
</style>
