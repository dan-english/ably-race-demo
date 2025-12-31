<template>
  <h1>Lap Times</h1>
  <div v-if="!hide">
    Publish to the <span class="event_name">lap_time</span> event on channel
    <span class="channel_name">{{ this.$race_lap_ably_channel }}</span>
  </div>
  <pre
    class="line-numbers"
    data-start="644"
  ><code ref="codeEl" class="language-python ">{{ code }}
  </code></pre>
</template>

<script>
export default {
  name: "lap_event_doc",
  props: ["hide_desc"],

  data() {
    return {
      hide: false,

      docActiveEvent: "",
      code: `# --- publish lap time after finishing lap ---
await lap_channel.publish(
    "lap_time",
    {
        "lap": lap,
        "lap_time_sec": round(lap_sim_time, 3),
        "best_lap_sec": round(best_lap, 3),
        "position": position,
    }
)
`.trim(),
    };
  },

  mounted() {
    this.$debug.info_doc("Lap Event Doc");
    if (this.hide_desc) {
      this.hide = this.hide_desc;
    }
    // Highlight the code block
    if (this.$refs.codeEl) {
      this.$Prism.highlightElement(this.$refs.codeEl);
    }
  },

  methods: {},
};
</script>
