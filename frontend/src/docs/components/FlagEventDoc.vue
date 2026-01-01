<template>
  <h1>Flag Status</h1>

  <div v-if="!hide">
    Publish to the <span class="event_name">flag_status</span> event on channel
    <span class="channel_name">{{ this.$race_flag_ably_channel }}</span>
  </div>
  <pre
    class="line-numbers"
    data-start="423"
  ><code ref="codeEl" class="language-python ">{{ code }}
  </code></pre>

  <pre><code ref="codeE2"  class="language-ini">"flag_status" could be one of
- green
- yellow
- vsc
- safety car
</code></pre>

  <pre
    class="line-numbers"
    data-start="434"
  ><code ref="codeE3"  class="language-ini">{{ listen_code }}</code></pre>
</template>

<script>
export default {
  name: "flag_event_doc",
  props: ["hide_desc"],

  data() {
    return {
      hide: false,

      listen_code: `subscribeToTelemetry() {
const channel = this.$ably.channels.get(this.$race_flag_ably_channel, {
  params: { rewind: 1 },
});
channel.subscribe(this.$flag_status_ably_event, (message) => {
  if (!this.racing) this.racing = true;
  let flag = message.data.flag?.toLowerCase().replace(/\\s+/g, "");
  const normalizedKey = Object.keys(this.$flagColors).find(
    (key) => key.replace(/\\s+/g, "").toLowerCase() === flag
  );
  this.currentFlag = normalizedKey || "grey";
});},`.trim(),

      code: `# --- publish flag only on change ---
if flag != prev_flag:
    await flag_channel.publish(
        "flag_status",
        {
            "flag": flag
        }
    )
    prev_flag = flag
`.trim(),
    };
  },

  mounted() {
    this.$debug.info_doc("Flag Event Doc");
    if (this.hide_desc) {
      this.hide = this.hide_desc;
    }

    Object.keys(this.$refs).forEach((refKey) => {
      if (refKey.startsWith("code") && this.$refs[refKey]) {
        this.$Prism.highlightElement(this.$refs[refKey]);
      }
    });
  },

  methods: {},
};
</script>
