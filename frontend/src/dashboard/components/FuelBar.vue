<template>
  <div class="fuel-gauge-wrapper">
    <div class="fuel-bar-background">
      <div
        class="fuel-bar-fill"
        :style="{
          height: fuelPercentage + '%',
          backgroundColor: fuelColor,
        }"
      ></div>
      <div class="fuel-bar-overlay">
        <span>{{ fuel_kg.toFixed(1) }} kg</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FuelBar",
  data() {
    return {
      fuel_kg: 100,
      maxFuel: 100,
    };
  },
  computed: {
    fuelPercentage() {
      return Math.min(100, (this.fuel_kg / this.maxFuel) * 100);
    },
    fuelColor() {
      if (this.fuelPercentage > 50) return "#28B463"; // green
      if (this.fuelPercentage > 25) return "#F1C40F"; // yellow
      return "#E74C3C"; // red
    },
  },
  mounted() {
    this.$debug.info("Fuel Bar Component");

    if (
      this.$ably &&
      this.$default_ably_channel &&
      this.$telemetry_ably_event
    ) {
      this.subscribeToTelemetry();
    }
  },
  methods: {
    subscribeToTelemetry() {
      const channel = this.$ably.channels.get(this.$default_ably_channel);

      channel.subscribe(this.$telemetry_ably_event, (message) => {
        const data = message.data;
        if (data.fuel_kg != null) {
          this.fuel_kg = data.fuel_kg;
        }
      });

      this.$debug.ably_subscribed(
        this.$default_ably_channel,
        this.$telemetry_ably_event,
        this.$options.name
      );
    },
  },
};
</script>

<style scoped>
.fuel-gauge-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 60px;
}

.fuel-bar-background {
  position: relative;
  width: 100%;
  height: 250px;
  border: 2px solid #555;
  border-radius: 6px;
  background-color: #222;
  overflow: hidden;
  display: flex;
  align-items: flex-end; /* fill grows/shrinks from bottom */
}

.fuel-bar-fill {
  width: 100%;
  transition: height 1s cubic-bezier(0.25, 0.8, 0.25, 1), background-color 0.5s;
  /* cubic-bezier for smoother shrink effect */
}

.fuel-bar-overlay {
  position: absolute;
  top: 50%;
  width: 100%;
  text-align: center;
  font-weight: bold;
  color: #fff;
  text-shadow: 1px 1px 4px #000;
  pointer-events: none;
  transform: translateY(-50%);
}
</style>
