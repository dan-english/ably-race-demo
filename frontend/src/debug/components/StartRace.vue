<template>
  <div>
    <el-button @click="runScript" type="primary" :loading="isRunning">
      {{ isRunning ? "Running..." : "Start Race" }}
    </el-button>

    <div v-if="result" class="result">
      <h3>Result:</h3>
      <pre>{{ result }}</pre>
    </div>

    <div v-if="error" class="error">
      <h3>Error:</h3>
      <pre>{{ error }}</pre>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isRunning: false,
      result: null,
      error: null,
    };
  },

  methods: {
    async runScript() {
      this.isRunning = true;
      this.result = null;
      this.error = null;

      try {
        const response = await fetch("/api/run-script", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();
        console.log(data);

        if (data.success) {
          this.result = data.output;
        } else {
          this.error = data.error;
        }
      } catch (err) {
        this.error = `Failed to connect: ${err.message}`;
        console.log(err.message);
      } finally {
        this.isRunning = false;
      }
    },
  },
};
</script>

<style scoped>
.run-button {
  padding: 0.75rem 1.5rem;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.run-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.result,
.error {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 4px;
}

.result {
  background: #f0f9ff;
  border: 1px solid #0ea5e9;
}

.error {
  background: #fef2f2;
  border: 1px solid #ef4444;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
