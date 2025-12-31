<template>
  <h1>Config</h1>

  <pre><code ref="codeEl"  class="language-ini">

VUE_APP_DEBUG=true
VUE_APP_API_KEY=_YOUR_UNIQUE_KEY_
VUE_APP_RACE_ABLY_CHANNEL=race-telemetry
# A dedicated channel just for lap times/data
VUE_APP_RACE_LAP_ABLY_CHANNEL=race-lap-telemetry
VUE_APP_ABLY_LAPTIME_EVENT=lap_time
VUE_APP_ABLY_SECTORTIME_EVENT=sector_time
VUE_APP_ABLY_TELEMETRY_EVENT=telemetry
VUE_APP_ABLY_FLAG_STATUS_EVENT=flag_status
VUE_APP_ABLY_BOX_STATUS_EVENT=boxbox_status

VUE_APP_ABLY_PIT_LANE_SPEED=80
VUE_APP_ABLY_WEATHER_CHANNEL=weather
VUE_APP_DEBUG_TAB_DISABLED=true




</code></pre>

  <div>Telemetry Events - main channel - event-name: 'telemetry'</div>
</template>

<script>
export default {
  name: "config_doc",

  data() {
    return {
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
    this.$debug.info_doc("Config Doc");

    // Highlight the code block
    if (this.$refs.codeEl) {
      this.$Prism.highlightElement(this.$refs.codeEl);
    }
  },

  methods: {},
};
</script>
