<template>
  <figure class="highcharts-figure">
    <h2 v-if="in_pit">Pit Lane Limiter</h2>
    <div ref="chartContainer" id="container"></div>

    <!-- Gear overlay circle -->
    <div class="gear-overlay" v-if="currentGear !== null">
      <div
        class="gear-circle"
        :style="{ backgroundColor: gearColors[currentGear] || '#555' }"
      >
        {{ currentGear }}
      </div>
    </div>
  </figure>
</template>

<script>
export default {
  name: "SpeedGauge",
  data() {
    return {
      chart: null,
      currentGear: 0,
      in_pit: false,
      gearColors: {
        1: "#FF5733", // red-orange
        2: "#FF8D1A", // orange
        3: "#FFC300", // yellow
        4: "#28B463", // green
        5: "#3498DB", // blue
        6: "#9B59B6", // purple
        7: "#E74C3C", // red
        8: "#1ABC9C", // teal (8th gear)
      },
    };
  },
  mounted() {
    this.$debug.info("Speed Gauge Component");

    this.initChart();
    if (
      this.$ably &&
      this.$default_ably_channel &&
      this.$telemetry_ably_event
    ) {
      this.subscribeToTelemetry();
    }
  },

  methods: {
    initChart() {
      const Highcharts = this.$Highcharts;
      const pitLaneSpeed = this.$pit_lane_speed || 92;

      // Initialize chart
      this.chart = Highcharts.chart(this.$refs.chartContainer, {
        chart: {
          type: "gauge",
          alignTicks: false,
          plotBackgroundColor: null,
          plotBackgroundImage: null,
          plotBorderWidth: 0,
          plotShadow: false,
        },

        title: { text: "" },

        pane: {
          startAngle: -150,
          endAngle: 150,
        },

        yAxis: [
          {
            min: 0,
            max: 380,
            lineColor: "#2caffe",
            tickColor: "#2caffe",
            minorTickColor: "#2caffe",
            offset: -25,
            lineWidth: 2,
            labels: { distance: -20, rotation: "auto" },
            tickLength: 5,
            minorTickLength: 5,
            endOnTick: false,
            // Add the plot line here
            plotLines: [
              {
                value: 80, // position on the axis
                color: "red", // line color
                width: 2, // line width
                dashStyle: "Dash", // optional: 'Solid', 'Dash', 'Dot', etc.
                zIndex: 5, // make sure it’s above ticks
                label: {
                  align: "right",
                  style: {
                    color: "red",
                    fontWeight: "bold",
                    fontSize: "12px",
                  },
                  rotation: 0,
                  y: -10,
                },
              },
              {
                value: 140, // position on the axis
                color: "#FFD700", // line color
                width: 2, // line width
                dashStyle: "Dash", // optional: 'Solid', 'Dash', 'Dot', etc.
                zIndex: 5, // make sure it’s above ticks
                label: {
                  align: "right",
                  style: {
                    color: "#FFD700",
                    fontWeight: "bold",
                    fontSize: "12px",
                  },
                  rotation: 0,
                  y: -10,
                },
              },
            ],
          },
          {
            min: 0,
            max: 180,
            tickPosition: "outside",
            lineColor: "#d66",
            lineWidth: 2,
            minorTickPosition: "outside",
            tickColor: "#d66",
            minorTickColor: "#d66",
            tickLength: 5,
            minorTickLength: 5,
            labels: { distance: 12, rotation: "auto" },
            offset: -20,
            endOnTick: false,
          },
        ],

        series: [
          {
            name: "Speed",
            data: [0], // start at 0
            dataLabels: {
              format:
                '<span style="color:#2caffe">{y} km/h</span><br/>' +
                '<span style="color:#d66">{custom_mph}</span>',
              backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                  [0, "var(--highcharts-neutral-color-20, #ddd)"],
                  [1, "var(--highcharts-background-color, #fff)"],
                ],
              },
              style: { textOutline: "none" },
              useHTML: false,
            },
            tooltip: { valueSuffix: " km/h" },
          },
        ],
      });
    },

    subscribeToTelemetry() {
      const channel = this.$ably.channels.get(this.$default_ably_channel);

      channel.subscribe(this.$telemetry_ably_event, (message) => {
        const speedKmh = parseFloat(message.data.speed_kmh);

        // Update current gear
        this.currentGear = message.data.gear ?? null;

        this.in_pit = message.data.in_pit;

        if (
          !isNaN(speedKmh) &&
          this.chart &&
          this.chart.series[0].points.length
        ) {
          const point = this.chart.series[0].points[0];
          point.update({
            y: speedKmh,
            custom_mph: (speedKmh * 0.621371).toFixed(0) + " mph",
          });
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

  position: relative; /* Important for overlay positioning */
  display: inline-block; /* So width fits chart */
}

.highcharts-description {
  margin: 0.3rem 10px;
  font-size: 0.9rem;
  color: #666;
}

#container {
  width: 100%;
  height: 400px;
  position: relative;
}

.gear-overlay {
  position: absolute;
  top: calc(50% + 80px); /* 60px below the center */
  left: 50%;
  transform: translateX(-50%); /* horizontally centered */
  font-size: 38px;
  font-weight: bold;
  color: #fff;
  text-shadow: 1px 1px 4px #000;
  pointer-events: none;
}
.gear-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 36px;
  font-weight: bold;
  color: #fff;
  text-shadow: 1px 1px 4px #000;
}
</style>
