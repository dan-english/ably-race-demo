<template>
  <div class="history_wrapper" v-loading="loading">
    <el-select
      v-if="loaded"
      v-model="filter_by"
      placeholder="Filter History By..."
      style="width: 240px; padding-bottom: 46px"
      @change="filterByEvent"
    >
      <el-option
        v-for="item in filter_options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <pre
      v-if="loaded && historyEvents?.length > 0"
      class="line-numbers prism-history"
    ><code ref="codeEl" class="language-json">{{ formattedHistory }}
  </code></pre>
  </div>
</template>

<script>
export default {
  name: "history_events_data",

  data() {
    return {
      filter_by: "",
      loading: true,
      loaded: false,
      historyData: undefined,
      historyEvents: [],

      lapTimeHistoryData: undefined,
      flagStatusHistoryData: undefined,

      filter_options: [
        {
          label: "Race Telemetry",
          value: "telemetry",
        },
        {
          label: "Box Box Status",
          value: "boxbox_status",
        },

        {
          label: "Flag Status",
          value: "flag_status",
        },

        {
          label: "Sector Times",
          value: "sector_time",
        },

        {
          label: "Lap Times",
          value: "lap_time",
          channel: "race-lap-telemetry",
        },
      ],
    };
  },
  computed: {
    formattedHistory() {
      return JSON.stringify(this.historyEvents, null, 2);
    },
  },

  mounted() {
    this.$debug.info("Ably History Data");
    this.loadLargeHistory();
    this.loadLaptimeHistory();
    this.loadFlagStatusHistory();
  },

  methods: {
    filterByEvent(event_name) {
      if (!Array.isArray(this.historyData)) return;

      if (event_name == "lap_time") {
        this.historyEvents = this.lapTimeHistoryData.filter(
          ({ name }) => name === event_name
        );
      } else if (event_name == "flag_status") {
        this.historyEvents = this.flagStatusHistoryData.filter(
          ({ name }) => name === event_name
        );
      } else {
        this.historyEvents = this.historyData.filter(
          ({ name }) => name === event_name
        );
      }

      if (this.historyEvents && this.historyEvents.length > 0) {
        // Initial highlight (optional)
        this.$nextTick(() => {
          // Check if ref exists before highlighting
          if (this.$refs.codeEl) {
            this.$Prism.highlightElement(this.$refs.codeEl);
          }
        });
        this.$emit("history_filter_changed", event_name);
      } else {
        console.log(
          "No data, check persistence configuration in Ably dashboard"
        );
      }
    },

    async loadLargeHistory() {
      this.$debug.log("Loading large history");

      const channel = this.$ably.channels.get(this.$default_ably_channel);

      let all = [];
      let page = await channel.history({
        limit: 110,
        direction: "backwards",
      });

      while (page.items.length && all.length < 200) {
        all.push(...page.items);
        if (!page.hasNext()) break;
        page = await page.next();
      }

      this.historyData = all;
      this.loading = false;
      this.loaded = true;
    },

    async loadLaptimeHistory() {
      this.$debug.log("Loading Laptime history");

      const channel = this.$ably.channels.get(this.$race_lap_ably_channel);

      let all = [];
      let page = await channel.history();

      while (page.items.length && all.length < 200) {
        all.push(...page.items);
        if (!page.hasNext()) break;
        page = await page.next();
      }

      this.lapTimeHistoryData = all;
    },

    async loadFlagStatusHistory() {
      this.$debug.log("Loading Flag Status history");

      const channel = this.$ably.channels.get(this.$race_flag_ably_channel);

      let all = [];
      let page = await channel.history();

      while (page.items.length && all.length < 200) {
        all.push(...page.items);
        if (!page.hasNext()) break;
        page = await page.next();
      }
      this.flagStatusHistoryData = all;
    },
  },
};
</script>
