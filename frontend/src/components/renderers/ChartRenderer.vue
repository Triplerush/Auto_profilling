<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { Chart, registerables } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'

Chart.register(...registerables, zoomPlugin)

const props = defineProps({
  component: { type: Object, required: true },
})

const canvasRef = ref(null)
let chartInstance = null

const PALETTE = [
  '#38bdf8', '#a78bfa', '#34d399', '#fb923c', '#f87171',
  '#facc15', '#818cf8', '#2dd4bf', '#e879f9', '#94a3b8',
]

function buildConfig() {
  const { chart_type, data, config } = props.component
  const type = chart_type === 'histogram' ? 'bar' : chart_type

  const datasets = (data.datasets || []).map((ds, i) => ({
    ...ds,
    backgroundColor: ds.backgroundColor || PALETTE[i % PALETTE.length] + '99',
    borderColor: ds.borderColor || PALETTE[i % PALETTE.length],
    borderWidth: ds.borderWidth || 1,
  }))

  return {
    type,
    data: { labels: data.labels || [], datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: config?.indexAxis || 'x',
      plugins: {
        legend: { labels: { color: '#e2e8f0' } },
        tooltip: { enabled: true },
        zoom: {
          zoom: { wheel: { enabled: true }, pinch: { enabled: true }, mode: 'xy' },
          pan: { enabled: true, mode: 'xy' },
        },
      },
      scales: ['pie', 'doughnut', 'radar'].includes(type) ? {} : {
        x: {
          title: { display: !!config?.x_label, text: config?.x_label || '', color: '#94a3b8' },
          ticks: { color: '#94a3b8' },
          grid: { color: '#334155' },
        },
        y: {
          title: { display: !!config?.y_label, text: config?.y_label || '', color: '#94a3b8' },
          ticks: { color: '#94a3b8' },
          grid: { color: '#334155' },
        },
      },
    },
  }
}

function createChart() {
  if (chartInstance) chartInstance.destroy()
  if (!canvasRef.value) return
  chartInstance = new Chart(canvasRef.value, buildConfig())
}

onMounted(createChart)
onBeforeUnmount(() => { if (chartInstance) chartInstance.destroy() })
watch(() => props.component, createChart, { deep: true })
</script>

<template>
  <div class="glass-card p-6 animate-fade-in">
    <h4 v-if="component.title" class="text-lg font-semibold text-heading mb-4">{{ component.title }}</h4>
    <div class="relative min-h-[300px] max-h-[500px]">
      <canvas ref="canvasRef"></canvas>
    </div>
  </div>
</template>
