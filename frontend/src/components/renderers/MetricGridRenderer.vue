<script setup>
defineProps({
  metrics: { type: Array, required: true },
})

function severityColor(severity) {
  switch (severity) {
    case 'warning': return 'var(--warning)'
    case 'critical': return 'var(--danger)'
    default: return 'var(--success)'
  }
}
</script>

<template>
  <div class="metrics-grid">
    <div
      v-for="(m, i) in metrics"
      :key="i"
      class="metric-card"
      :style="{ borderLeftColor: severityColor(m.severity) }"
    >
      <div class="metric-value">{{ m.value }}</div>
      <div class="metric-label">{{ m.label }}</div>
      <div v-if="m.description" class="metric-desc">{{ m.description }}</div>
    </div>
  </div>
</template>

<style scoped>
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 0.75rem;
}
.metric-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--success);
  border-radius: 8px;
  padding: 0.85rem 1rem;
}
.metric-value {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-primary);
}
.metric-label {
  font-size: 0.78rem;
  color: var(--text-secondary);
  margin-top: 0.15rem;
}
.metric-desc {
  font-size: 0.7rem;
  color: var(--text-secondary);
  margin-top: 0.3rem;
  opacity: 0.7;
}
</style>
