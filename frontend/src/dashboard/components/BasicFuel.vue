<template>
  <figure class="highcharts-figure">
    <div id="container-fuel-load" class="chart-container"></div>
  </figure>
</template>

<script>
export default {
  name: "BasicFuel",

  data() {
    return {
      chartFuelLoad: null,
      chartTyre: null,
      telemetryLoaded: false,
    };
  },

  mounted() {
    this.$debug.info("Basic Fuel Component");

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
    if (this.chartFuelLoad) this.chartFuelLoad.destroy();
    if (this.chartTyre) this.chartTyre.destroy();
  },

  methods: {
    initGauges() {
      const Highcharts = this.$Highcharts;
      const baseGaugeOptions = {
        chart: { type: "solidgauge" },
        title: null,
        pane: {
          center: ["50%", "85%"],
          size: "140%",
          startAngle: -90,
          endAngle: 90,
          background: { innerRadius: "60%", outerRadius: "100%", shape: "arc" },
        },
        tooltip: { enabled: false },
        yAxis: { lineWidth: 0, tickWidth: 0 },
        plotOptions: {
          solidgauge: { dataLabels: { borderWidth: 0, useHTML: true } },
        },
      };

      // Fuel Load Gauge
      this.chartFuelLoad = Highcharts.chart(
        "container-fuel-load",
        Highcharts.merge(baseGaugeOptions, {
          yAxis: {
            min: 0,
            max: 120,
            title: { text: "Fuel Load" },
            stops: [
              [0.0, "#DF5353"], // low = red
              [0.6, "#DDDF0D"], // mid = yellow
              [1.0, "#55BF3B"], // high = green
            ],
          },
          series: [
            {
              name: "Fuel Load",
              data: [0],
              dataLabels: {
                format:
                  '<div style="text-align:center">' +
                  '<span style="font-size:24px">{y:.1f}</span><br/>' +
                  '<span style="font-size:12px;opacity:0.6">kg</span>' +
                  "</div>",
              },
            },
          ],
        })
      );
    },

    subscribeToTelemetry() {
      const channel = this.$ably.channels.get(this.$default_ably_channel);

      channel.subscribe(this.$telemetry_ably_event, (message) => {
        const data = message.data;

        if (this.chartFuelLoad && data.fuel_kg !== undefined) {
          this.chartFuelLoad.series[0].points[0].update(data.fuel_kg, true);
        }
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
.highcharts-figure {
  width: 350px;
  margin: 0 auto;
}
.chart-container {
  width: 300px;
  height: 200px;
  float: left;
}
@media (max-width: 900px) {
  .chart-container {
    float: none;
    margin: 0 auto;
  }
}
</style>
