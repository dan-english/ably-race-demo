<template>
  <svg
    v-if="racing"
    width="50"
    height="30"
    viewBox="0 0 120 120"
    xmlns="http://www.w3.org/2000/svg"
  >
    <!-- Flag pole -->
    <rect x="0" y="0" width="10" height="120" fill="#333" />

    <!-- Waving flag -->
    <path
      id="raceFlag"
      :d="flagPath"
      :fill="$flagColors[currentFlag]?.fill || 'transparent'"
      :stroke="$flagColors[currentFlag]?.stroke || 'transparent'"
      stroke-width="2"
    >
      <animate
        attributeName="d"
        dur="2s"
        repeatCount="indefinite"
        :values="flagAnimationValues"
      />
    </path>
  </svg>
</template>

<script>
export default {
  name: "RaceFlag",

  data() {
    return {
      currentFlag: "transparent",
      racing: false,
      // Base flag path (used for initial display)
      flagPath: "M10 10 Q50 20 100 10 T190 10 L190 70 Q100 80 10 70 Z",
      // Animation values for waving
      flagAnimationValues: `
        M10 10 Q50 20 100 10 T190 10 L190 70 Q100 80 10 70 Z;
        M10 10 Q50 0 100 10 T190 10 L190 70 Q100 60 10 70 Z;
        M10 10 Q50 20 100 10 T190 10 L190 70 Q100 80 10 70 Z
      `,
    };
  },

  mounted() {
    this.$debug.info("Flag Component");

    if (
      this.$ably &&
      this.$default_ably_channel &&
      this.$flag_status_ably_event
    ) {
      this.subscribeToTelemetry();
    }
  },

  methods: {
    subscribeToTelemetry() {
      const channel = this.$ably.channels.get(this.$default_ably_channel);

      channel.subscribe(this.$flag_status_ably_event, (message) => {
        if (!this.racing) this.racing = true;

        let flag = message.data.flag?.toLowerCase().replace(/\s+/g, ""); // normalize string
        // Attempt direct match with global flagColors keys
        const normalizedKey = Object.keys(this.$flagColors).find(
          (key) => key.replace(/\s+/g, "").toLowerCase() === flag
        );

        this.currentFlag = normalizedKey || "grey"; // fallback if unknown
        this.$debug.flag(this.currentFlag);

        this.$emit("flag-change", this.currentFlag);
      });

      this.$debug.ably_subscribed(
        this.$default_ably_channel,
        this.$flag_status_ably_event,
        this.$options.name
      );
    },
  },
};
</script>

<style scoped>
svg {
  display: block;
  margin: 0 auto;
}
</style>
