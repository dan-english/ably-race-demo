<template>
  <div class="fuelguage">
    <div
      style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
      "
    >
      <div style="flex: 1"></div>
      <h3 style="margin: 0; flex: 1; text-align: center">Fuel Level</h3>
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

    <figure class="highcharts-figure">
      <div ref="chartContainer" id="container"></div>
    </figure>
  </div>
</template>

<script>
export default {
  name: "BasicFuelGauge",
  data() {
    return {
      chart: null,
      fuelMax: 110,
    };
  },
  mounted() {
    this.$debug.info("Basic Fuel Guage Component");

    const Highcharts = this.$Highcharts;

    // Initialize chart
    this.chart = Highcharts.chart(this.$refs.chartContainer, {
      chart: {
        type: "gauge",
        plotBackgroundColor: null,
        plotBackgroundImage: null,
        plotBorderWidth: 0,
        plotShadow: false,
        height: "80%",
      },

      title: { text: undefined },

      pane: {
        startAngle: -90,
        endAngle: 90,
        background: null,
        center: ["50%", "75%"],
        size: "110%",
      },

      yAxis: {
        min: 0,
        max: this.fuelMax,
        tickPixelInterval: 72,
        tickPosition: "inside",
        tickColor: "var(--highcharts-background-color, #FFFFFF)",
        tickLength: 20,
        tickWidth: 2,
        labels: { distance: 20, style: { fontSize: "14px" } },
        lineWidth: 0,
        plotBands: [
          {
            from: 0,
            to: this.fuelMax * 0.25,
            color: "#DF5353",
            thickness: 20,
            borderRadius: "50%",
          }, // red
          {
            from: this.fuelMax * 0.25,
            to: this.fuelMax * 0.5,
            color: "#FFA500",
            thickness: 20,
            borderRadius: "50%",
          }, // orange
          {
            from: this.fuelMax * 0.5,
            to: this.fuelMax * 0.75,
            color: "#FFFF00",
            thickness: 20,
            borderRadius: "50%",
          }, // yellow
          {
            from: this.fuelMax * 0.75,
            to: this.fuelMax,
            color: "#32CD32",
            thickness: 20,
            borderRadius: "50%",
          }, // lime
        ],
      },

      series: [
        {
          name: "Fuel",
          data: [this.fuelMax],
          tooltip: { valueSuffix: " l" },
          dataLabels: {
            format: "{y:.2f} litres",
            borderWidth: 0,
            color: "#333333",
            style: { fontSize: "16px" },
          },
          dial: {
            radius: "80%",
            backgroundColor: "gray",
            baseWidth: 12,
            baseLength: "0%",
            rearLength: "0%",
          },
          pivot: { backgroundColor: "gray", radius: 6 },
        },
      ],
    });

    // Subscribe to telemetry
    this.subscribeToTelemetry();
  },
  methods: {
    subscribeToTelemetry() {
      if (
        !this.$ably ||
        !this.$default_ably_channel ||
        !this.$telemetry_ably_event
      ) {
        console.warn("Ably telemetry not configured");
        return;
      }

      const channel = this.$ably.channels.get(this.$default_ably_channel);

      channel.subscribe(this.$telemetry_ably_event, (message) => {
        const fuelKg = parseFloat(message.data.fuel_kg);

        if (
          !isNaN(fuelKg) &&
          this.chart &&
          this.chart.series[0].points.length
        ) {
          const point = this.chart.series[0].points[0];
          point.update(Math.min(fuelKg, this.fuelMax));
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
  min-width: 310px;
  max-width: 500px;
  margin: 1em auto;
}
</style>
