<template>
  <div>
    <svg
      id="drsIndicator"
      width="60"
      height="30"
      viewBox="0 0 200 100"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <!-- Glow filter for ON state -->
        <filter id="glow">
          <feGaussianBlur stdDeviation="2.5" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      <!-- Border box -->
      <rect
        id="drsBox"
        x="10"
        y="10"
        width="180"
        height="80"
        :fill="drs_enabled ? '#000000' : 'transparent'"
        :stroke="drs_enabled ? '#00ff00' : '#666'"
        :stroke-width="drs_enabled ? '4' : '3'"
        rx="8"
      />

      <!-- DRS Text -->
      <text
        id="drsText"
        x="100"
        y="65"
        text-anchor="middle"
        font-size="48"
        font-weight="bold"
        font-family="Arial, sans-serif"
        :fill="drs_enabled ? '#00ff00' : '#666'"
        :filter="drs_enabled ? 'url(#glow)' : 'none'"
      >
        DRS
      </text>
    </svg>
  </div>
</template>

<script>
export default {
  name: "DRSstatus",

  data() {
    return {
      drs_enabled: false,
      racing: false,
    };
  },

  mounted() {
    this.$debug.info("DRS Status Component");

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
        this.drs_enabled = message.data.drs || false;

        this.$debug.info(`DRS: ${this.drs_enabled}`);
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
svg {
  display: block;
  margin: 0 auto;
}
</style>
