<script setup>
import { ref } from 'vue'

const props = defineProps({
  component: { type: Object, required: true },
})

const tooltip = ref({ show: false, text: '', x: 0, y: 0 })

function cellColor(val) {
  if (val >= 0) {
    const intensity = Math.round(val * 60)
    return `hsl(210, 80%, ${90 - intensity}%)`
  } else {
    const intensity = Math.round(Math.abs(val) * 60)
    return `hsl(0, 70%, ${90 - intensity}%)`
  }
}

function showTooltip(e, row, col, val) {
  tooltip.value = {
    show: true,
    text: `${props.component.columns[row]} / ${props.component.columns[col]}: ${val.toFixed(4)}`,
    x: e.clientX,
    y: e.clientY,
  }
}

function hideTooltip() {
  tooltip.value.show = false
}
</script>

<template>
  <div class="corr-wrapper">
    <h4 v-if="component.title" class="corr-title">{{ component.title }}</h4>
    <div class="corr-scroll">
      <table class="corr-table">
        <thead>
          <tr>
            <th></th>
            <th v-for="(col, i) in component.columns" :key="i" class="col-label">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, ri) in component.matrix" :key="ri">
            <th class="row-label">{{ component.columns[ri] }}</th>
            <td
              v-for="(val, ci) in row"
              :key="ci"
              :style="{ backgroundColor: cellColor(val) }"
              class="corr-cell"
              @mouseenter="showTooltip($event, ri, ci, val)"
              @mouseleave="hideTooltip"
            >
              {{ val.toFixed(2) }}
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
.corr-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
  position: relative;
}
.corr-title { font-size: 0.9rem; color: var(--text-primary); margin-bottom: 0.75rem; }
.corr-scroll { overflow-x: auto; }
.corr-table { border-collapse: collapse; font-size: 0.75rem; }
.corr-table th, .corr-table td { padding: 0.35rem 0.5rem; text-align: center; }
.col-label { color: var(--text-secondary); font-weight: 500; white-space: nowrap; }
.row-label { color: var(--text-secondary); font-weight: 500; text-align: right; white-space: nowrap; }
.corr-cell { color: #1e293b; font-weight: 600; cursor: default; min-width: 3rem; }
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
