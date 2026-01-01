<template>
  <div class="">
    <div
      style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
      "
    >
      <div style="flex: 1"></div>
      <h3 style="margin: 0; flex: 1; text-align: center">Tyre Degradation</h3>
      <div style="flex: 1; display: flex; justify-content: flex-end">
        <div
          style="
            padding: 4px 12px;
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 11px;
          "
        >
          {{ $default_ably_channel }} <br />
          {{ $telemetry_ably_event }}
        </div>
      </div>
    </div>

    <div class="tyre-gauges">
      <div v-for="tyre in tyreOrder" :key="tyre" class="tyre-gauge-container">
        <div :id="'container-' + tyre" class="chart-container"></div>
        <div class="tyre-label">{{ tyre }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TyreGauge",
  data() {
    return {
      tyreOrder: ["FL", "FR", "RL", "RR"],
      charts: {},
    };
  },
  mounted() {
    this.$debug.info("Tyre Gauges");

    this.initGauges();

    if (
      this.$ably &&
      this.$default_ably_channel &&
      this.$telemetry_ably_event
    ) {
      this.subscribeToTelemetry();
    }
  },
  beforeUnmount() {
    // destroy all charts
    Object.values(this.charts).forEach((chart) => chart.destroy());
  },
  methods: {
    initGauges() {
      const Highcharts = this.$Highcharts;
      const baseGaugeOptions = {
        chart: { type: "solidgauge" },
        title: null,
        pane: {
          center: ["50%", "75%"],
          size: "120%",
          startAngle: -90,
          endAngle: 90,
          background: { innerRadius: "60%", outerRadius: "100%", shape: "arc" },
        },
        tooltip: { enabled: false },
        yAxis: {
          min: 0,
          max: 100,
          lineWidth: 0,
          tickWidth: 0,
          labels: { enabled: false },
        },
        plotOptions: {
          solidgauge: {
            dataLabels: {
              useHTML: true,
              y: 60,
              borderWidth: 0,
              format:
                '<div style="text-align:center"><span style="font-size:10px">{y:.1f}</span> <span style="font-size:10px;opacity:0.6">%</span></div>',
            },
          },
        },
      };

      this.tyreOrder.forEach((tyre) => {
        this.charts[tyre] = Highcharts.chart(
          "container-" + tyre,
          Highcharts.merge(baseGaugeOptions, {
            yAxis: {
              title: {},
              stops: [
                [0.0, "#55BF3B"],
                [0.25, "#FFD700"], // yellow
                [0.5, "#FFA500"], // orange
                [0.75, "#FF4500"], // orange-red
                [1.0, "#FF0000"], // red
              ],
            },
            series: [{ name: "Tyre Deg", data: [0] }],
          })
        );
      });
    },
    subscribeToTelemetry() {
      const channel = this.$ably.channels.get(this.$default_ably_channel);

      channel.subscribe(this.$telemetry_ably_event, (message) => {
        const tyres = message.data.tyres || {};

        this.tyreOrder.forEach((tyre) => {
          if (tyres[tyre] !== undefined && this.charts[tyre]) {
            const value = Math.min(tyres[tyre], 100);
            this.charts[tyre].series[0].points[0].update(value, true);
          }
        });
      });

      this.$debug.ably_subscribed(
        this.$default_ably_channel,
        this.$telemetry_ably_event,
        this.$options.name
      );
    },
  },
};
</script>

<style scoped>
.tyre-gauges {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 2 columns */
  grid-gap: 20px; /* spacing between gauges */
  justify-items: center;
  align-items: center;
}

.tyre-gauge-container {
  width: 260px;
  position: relative;
}

.chart-container {
  width: 100%;
  height: 220px;
}

.tyre-label {
  text-align: center;
  font-weight: bold;
  margin-top: 5px;
}
</style>
