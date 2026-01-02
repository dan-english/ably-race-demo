<template>
  <pre><code ref="codeEl" class="language-ini ">{{ code }}
  </code></pre>
</template>

<script>
export default {
  data() {
    return {
      hide: false,

      docActiveEvent: "",
      code: `# --- Channels
  main_channel      = race-telemetry
  race_lap_channel  = race-lap-telemetry
  race_flag_channel = race-flag

# --- Events
(flag) = flag_status

(race-telemetry) = race_status
(race-telemetry) = telemetry
(race-telemetry) = sector_time
(race-telemetry) = boxbox_status

(lap-channel) = lap_time

# --- Ably Channel Message Rules
race-flag = Persist all messages
race-lap-telemetry = Persist all messages
race-telemetry  = Persist all messages


# --- Logic
If fuel below 70 litres force pit flag triggered
If tyre wear greater than 45% force pit flag triggered
Safety car could trigger force pit flag
Enforce speed limit while in pit section
Only overtake while DRS enabled
Flags are randomly generated (yellow could randomly be bumped to safety car)
Flags other than green enforce speed restrictions

# --- Flags
green
yellow
vsc
safety car


`.trim(),
    };
  },
  mounted() {
    this.$debug.info_doc("Intro");
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
