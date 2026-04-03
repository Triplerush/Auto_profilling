<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  component: { type: Object, required: true },
})

const tooltip = ref({ show: false, text: '', x: 0, y: 0 })

const rowTotals = computed(() =>
  props.component.matrix.map(row => row.reduce((a, b) => a + b, 0))
)

function cellBg(ri, ci, val) {
  const total = rowTotals.value[ri] || 1
  const pct = val / total
  if (ri === ci) {
    return `rgba(34, 197, 94, ${0.15 + pct * 0.5})`
  }
  return val > 0 ? `rgba(239, 68, 68, ${0.1 + pct * 0.4})` : 'transparent'
}

function showTooltip(e, ri, ci, val) {
  const total = rowTotals.value[ri] || 1
  const pct = ((val / total) * 100).toFixed(1)
  tooltip.value = {
    show: true,
    text: `Real: ${props.component.labels[ri]}, Pred: ${props.component.labels[ci]} — ${val} (${pct}%)`,
    x: e.clientX,
    y: e.clientY,
  }
}

function hideTooltip() {
  tooltip.value.show = false
}
</script>

<template>
  <div class="cm-wrapper">
    <h4 v-if="component.title" class="cm-title">{{ component.title }}</h4>
    <div class="cm-scroll">
      <table class="cm-table">
        <thead>
          <tr>
            <th class="corner">Real \ Pred</th>
            <th v-for="(label, i) in component.labels" :key="i">{{ label }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, ri) in component.matrix" :key="ri">
            <th class="row-label">{{ component.labels[ri] }}</th>
            <td
              v-for="(val, ci) in row"
              :key="ci"
              :style="{ backgroundColor: cellBg(ri, ci, val) }"
              class="cm-cell"
              @mouseenter="showTooltip($event, ri, ci, val)"
              @mouseleave="hideTooltip"
            >
              <span class="cm-count">{{ val }}</span>
              <span class="cm-pct">{{ ((val / (rowTotals[ri] || 1)) * 100).toFixed(1) }}%</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="tooltip.show" class="tooltip" :style="{ left: tooltip.x + 12 + 'px', top: tooltip.y - 8 + 'px' }">
      {{ tooltip.text }}
    </div>
  </div>
</template>

<style scoped>
.cm-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
  position: relative;
}
.cm-title { font-size: 0.9rem; color: var(--text-primary); margin-bottom: 0.75rem; }
.cm-scroll { overflow-x: auto; }
.cm-table { border-collapse: collapse; font-size: 0.82rem; }
.cm-table th, .cm-table td { padding: 0.5rem 0.75rem; text-align: center; border: 1px solid var(--border); }
.corner { color: var(--text-secondary); font-size: 0.7rem; font-style: italic; }
.cm-table thead th { background: var(--bg-dark); color: var(--text-secondary); font-weight: 500; }
.row-label { background: var(--bg-dark); color: var(--text-secondary); font-weight: 500; text-align: right; }
.cm-cell { cursor: default; min-width: 4.5rem; }
.cm-count { display: block; font-weight: 700; color: var(--text-primary); }
.cm-pct { display: block; font-size: 0.68rem; color: var(--text-secondary); }
.tooltip {
  position: fixed;
  background: var(--bg-dark);
  color: var(--text-primary);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.3rem 0.6rem;
  font-size: 0.75rem;
  pointer-events: none;
  z-index: 100;
  white-space: nowrap;
}
</style>
