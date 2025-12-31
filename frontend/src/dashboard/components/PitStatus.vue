<template>
  <img v-if="in_pit" height="50px" src="/pitcog.png" />
</template>

<script>
export default {
  name: "PitStatus",

  data() {
    return {
      in_pit: false,
    };
  },

  mounted() {
    this.$debug.info("Pit Status Component");

    if (
      this.$ably &&
      this.$default_ably_channel &&
      this.$boxbox_status_ably_event
    ) {
      this.subscribeToTelemetry();
    }
  },

  methods: {
    subscribeToTelemetry() {
      const channel = this.$ably.channels.get(this.$default_ably_channel);

      channel.subscribe(this.$boxbox_status_ably_event, (message) => {
        this.in_pit = message.data.in_pit;
      });

      this.$debug.ably_subscribed(
        this.$default_ably_channel,
        this.$boxbox_status_ably_event,
        this.$options.name
      );
    },
  },
};
</script>
