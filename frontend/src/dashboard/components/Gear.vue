<template>
  <svg :width="size" :height="size" viewBox="0 0 200 200" class="gear-knob">
    <!-- Outer circle -->
    <circle
      cx="100"
      cy="100"
      r="95"
      :fill="inPit ? '#FFD700' : '#222'"
      :stroke="outerCircleStrokeColor"
      stroke-width="4"
    ></circle>

    <!-- Gear numbers around the circle -->
    <g v-for="n in 8" :key="n">
      <circle
        :cx="positions[n].x"
        :cy="positions[n].y"
        r="20"
        :fill="activeGear === n ? gearColors[n] : '#555'"
      />
      <text
        :x="positions[n].x"
        :y="positions[n].y + 6"
        text-anchor="middle"
        font-size="16"
        font-weight="bold"
        fill="white"
      >
        {{ n }}
      </text>
    </g>

    <!-- Center label -->
    <text
      x="100"
      y="105"
      text-anchor="middle"
      font-size="24"
      font-weight="bold"
      fill="#fff"
    >
      Gear
    </text>
  </svg>
</template>

<script>
export default {
  name: "GearShifter",

  props: {
    size: {
      type: Number,
      default: 200,
    },
  },

  data() {
    return {
      activeGear: null,
      inPit: false,
      flag: "",
      flagColors: {
        yellow: "#FFD700",
        green: "#28B463",
        red: "#E74C3C",
        "safety car": "#FFD700",
      },
      gearColors: {
        1: "#FF5733", // red-orange
        2: "#FF8D1A", // orange
        3: "#FFC300", // yellow
        4: "#28B463", // green
        5: "#3498DB", // blue
        6: "#9B59B6", // purple
        7: "#E74C3C", // red
        8: "#1ABC9C", // teal (8th gear)
      },
      positions: {
        1: { x: 100, y: 35 },
        2: { x: 145, y: 60 },
        3: { x: 165, y: 105 },
        4: { x: 145, y: 150 },
        5: { x: 100, y: 168 },
        6: { x: 55, y: 150 },
        7: { x: 35, y: 105 },
        8: { x: 55, y: 60 },
      },
    };
  },

  mounted() {
    this.$debug.info("Gear Component");

    if (
      this.$ably &&
      this.$default_ably_channel &&
      this.$telemetry_ably_event
    ) {
      this.subscribeToTelemetry();
    }
  },
  computed: {
    normalizedFlag() {
      if (!this.flag) return "";
      return String(this.flag).toLowerCase().trim();
    },

    outerCircleStrokeColor() {
      return this.flagColors[this.normalizedFlag] || "#555"; // default stroke
    },
    gearColor() {
      return this.gearColors[this.activeGear] ?? "#555";
    },
  },
  methods: {
    subscribeToTelemetry() {
      const channel = this.$ably.channels.get(this.$default_ably_channel);
      channel.subscribe(this.$telemetry_ably_event, (message) => {
        const data = message.data;

        // Update gear if valid
        if (data.gear >= 1 && data.gear <= 8) {
          this.activeGear = data.gear;
        }

        // Update pit status
        this.inPit = !!data.in_pit;
        this.flag = data.flag;
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
.gear-knob {
  display: block;
  margin: 0 auto;
}
</style>
