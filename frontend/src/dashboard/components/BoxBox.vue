<template>
  <div>
    <h1 v-if="should_box">Box Box This Lap {{ "- " + reason }}</h1>
    <h1 v-if="in_pit">In Pit</h1>
  </div>
</template>

<script>
export default {
  name: "BoxBox",

  data() {
    return {
      should_box: false,
      in_pit: false,
      reason: "",
    };
  },

  mounted() {
    this.$debug.info("BoxBox Component");

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
        this.should_box = message.data.boxbox;

        this.reason = message.data.reason;
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
