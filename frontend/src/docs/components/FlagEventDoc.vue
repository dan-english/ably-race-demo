<template>
  <h1>Flag Status</h1>

  <div v-if="!hide">
    Publish to the <span class="event_name">flag_status</span> event on channel
    <span class="channel_name">{{ this.$default_ably_channel }}</span>
  </div>
  <pre
    class="line-numbers"
    data-start="417"
  ><code ref="codeEl" class="language-python ">{{ code }}
  </code></pre>

  <pre><code ref="codeE2"  class="language-ini">"flag_status" could be one of
- green
- yellow
- vsc
- safety car
</code></pre>
</template>

<script>
export default {
  name: "flag_event_doc",
  props: ["hide_desc"],

  data() {
    return {
      hide: false,

      code: `# --- publish flag only on change ---
if flag != prev_flag:
    await channel.publish(
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
    // Highlight the code block
    if (this.$refs.codeEl) {
      this.$Prism.highlightElement(this.$refs.codeEl);
    }
    if (this.$refs.codeE2) {
      this.$Prism.highlightElement(this.$refs.codeE2);
    }
  },

  methods: {},
};
</script>
