<template>
  <h1>Box Box Status</h1>

  <div v-if="!hide">
    Publish to the <span class="event_name">boxbox_status</span> event on
    channel
    <span class="channel_name">{{ this.$default_ably_channel }}</span>
  </div>

  <pre
    class="line-numbers"
    data-start="402"
  ><code ref="codeEl" class="language-python ">{{ code }}
  </code></pre>

  <pre
    class="line-numbers"
    data-start="428"
  ><code ref="codeE2" class="language-python ">{{ code_pitreason }}
  </code></pre>
</template>

<script>
export default {
  name: "box_event_doc",
  props: ["hide_desc"],

  data() {
    return {
      hide: false,
      docActiveEvent: "",
      code_pitreason: `# --- publish boxbox status---
await channel.publish(
    "boxbox_status",
    {
      "boxbox": True,
      "in_pit":False,
      "reason":"Tyres"
    }
)`,

      code: `# --- publish boxbox status---
await channel.publish(
    "boxbox_status",
    {
        "boxbox": False,
        "in_pit": False,
        "approaching_pit" : False,
        "total_pit_time": pit_total_time
    }
)
`.trim(),
    };
  },

  mounted() {
    this.$debug.info_doc("Box Event Doc");
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
