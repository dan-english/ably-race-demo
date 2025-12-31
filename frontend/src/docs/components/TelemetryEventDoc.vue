<template>
  <h1>Telemetry Events</h1>
  <div v-if="!hide">
    Publish to the <span class="event_name">telemetry</span> event on channel
    <span class="channel_name">{{ this.$default_ably_channel }}</span>
  </div>
  <pre
    class="line-numbers"
    data-start="581"
  ><code ref="codeEl" class="language-python ">{{ code }}
  </code></pre>
</template>

<script>
export default {
  name: "telemetry_event_doc",
  props: ["hide_desc"],

  data() {
    return {
      hide: false,

      docActiveEvent: "",
      code: `# --- publish telemetry data ---
await channel.publish(
    "telemetry",
    {
        "timestamp": time.time(),
        "lap": lap,
        "section": section,
        "speed_kmh": round(speed, 1),
        "gear": gear,
        "drs": drs,
        "fuel_kg": round(fuel, 2),
        "in_pit": in_pit,
        "position": position,
        "flag":flag,
        "overtake": ot_text is not None,
        "tyres": tyres,
        "tyre_wear_avg": round(average_tyre_wear(tyres), 2),
        "tyre_wear_worst": round(worst_tyre_wear(tyres), 2),
        "retired": False
    }
)
`.trim(),
    };
  },

  mounted() {
    this.$debug.info_doc("Telemetry Event Doc");
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
