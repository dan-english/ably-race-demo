<template>
  <h1>Sector Times</h1>
  <div v-if="!hide">
    Publish to the <span class="event_name">sector_time</span> event on channel
    <span class="channel_name">{{ this.$default_ably_channel }}</span> with
    completion of each sector with in the lap (18 sections on this circuit)
  </div>

  <div class="prism-tomorrow">
    <pre
      class="line-numbers"
      data-start="623"
    ><code ref="codeEl" class="language-python ">{{ code }}
  </code></pre>
  </div>
</template>

<script>
export default {
  name: "sector_event_doc",
  props: ["hide_desc"],
  data() {
    return {
      hide: false,
      docActiveEvent: "",
      code: `# --- publish sector time after finishing section ---
await channel.publish(
    "sector_time",
    {
        "lap": lap,
        "sector": section,
        "sector_time_sec": round(sector_time, 3),
        "lap_time_sec": round(lap_sim_time, 3),
        "position": position,
    }
 )`.trim(),
    };
  },

  mounted() {
    this.$debug.info_doc("Sector Event Doc");
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
