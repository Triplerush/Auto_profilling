<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store.js'
import { api } from '../api.js'
import MetricGridRenderer from '../components/renderers/MetricGridRenderer.vue'
import SectionRenderer from '../components/renderers/SectionRenderer.vue'

const router = useRouter()
const selectedA = ref(null)
const selectedB = ref(null)
const analysisA = ref(null)
const analysisB = ref(null)
const loading = ref(false)

onMounted(() => {
  if (!store.analyses.length) store.fetchAnalyses()
})

const canCompare = computed(() => selectedA.value && selectedB.value && selectedA.value !== selectedB.value)

async function loadComparison() {
  if (!canCompare.value) return
  loading.value = true
  try {
    const [resA, resB] = await Promise.all([
      fetch(api(`/v1/analyses/${selectedA.value}`)),
      fetch(api(`/v1/analyses/${selectedB.value}`)),
    ])
    if (!resA.ok || !resB.ok) throw new Error('Error al cargar analisis')
    analysisA.value = await resA.json()
    analysisB.value = await resB.json()
  } catch (e) {
    store.error = e.message
  } finally {
    loading.value = false
  }
}

function kpiDiff(kpiA, kpiB) {
  const numA = parseFloat(String(kpiA.value).replace(/[^0-9.\-]/g, ''))
  const numB = parseFloat(String(kpiB.value).replace(/[^0-9.\-]/g, ''))
  if (isNaN(numA) || isNaN(numB)) return null
  const diff = numA - numB
  return diff > 0 ? `+${diff.toFixed(2)}` : diff.toFixed(2)
}

const matchedKpis = computed(() => {
  if (!analysisA.value || !analysisB.value) return []
  return analysisA.value.kpis.map(kpiA => {
    const kpiB = analysisB.value.kpis.find(k => k.label === kpiA.label)
    return { label: kpiA.label, a: kpiA, b: kpiB || null, diff: kpiB ? kpiDiff(kpiA, kpiB) : null }
  })
})
</script>

<template>
  <div class="flex flex-col gap-6 animate-fade-in">
    <!-- Back -->
    <button
      @click="router.push('/')"
      class="inline-flex items-center gap-1.5 text-sm text-muted hover:text-sky-400 transition-colors self-start cursor-pointer"
    >
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
      </svg>
      Volver a Galeria
    </button>

    <!-- Selector -->
    <div class="glass-card p-6">
      <h2 class="text-2xl font-bold text-heading mb-4">Comparar Analisis</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-xs text-muted mb-1.5 font-medium">Analisis A</label>
          <select
            v-model="selectedA"
            class="w-full px-3 py-2.5 rounded-lg text-sm cursor-pointer transition-colors bg-[var(--bg-card-solid)] border border-[var(--border-card)] text-[var(--text-body)] focus:outline-none focus:border-sky-500/50"
          >
            <option :value="null" disabled>Seleccionar...</option>
            <option v-for="a in store.analyses" :key="a.id" :value="a.id">{{ a.title }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs text-muted mb-1.5 font-medium">Analisis B</label>
          <select
            v-model="selectedB"
            class="w-full px-3 py-2.5 rounded-lg text-sm cursor-pointer transition-colors bg-[var(--bg-card-solid)] border border-[var(--border-card)] text-[var(--text-body)] focus:outline-none focus:border-sky-500/50"
          >
            <option :value="null" disabled>Seleccionar...</option>
            <option v-for="a in store.analyses" :key="a.id" :value="a.id">{{ a.title }}</option>
          </select>
        </div>
      </div>
      <button
        @click="loadComparison"
        :disabled="!canCompare || loading"
        class="mt-4 px-5 py-2 bg-sky-500 hover:bg-sky-600 text-white rounded-lg font-semibold text-sm transition-colors cursor-pointer disabled:bg-slate-600 disabled:text-slate-400 disabled:cursor-not-allowed"
      >
        {{ loading ? 'Cargando...' : 'Comparar' }}
      </button>
    </div>

    <!-- Comparison results -->
    <template v-if="analysisA && analysisB">
      <!-- KPI Comparison Table -->
      <div v-if="matchedKpis.length" class="glass-card p-6">
        <h3 class="text-lg font-semibold text-heading mb-4">KPIs Side-by-Side</h3>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr>
                <th class="text-left px-4 py-2.5 text-muted font-medium">KPI</th>
                <th class="text-center px-4 py-2.5 text-sky-400 font-medium">{{ analysisA.metadata.title }}</th>
                <th class="text-center px-4 py-2.5 text-violet-400 font-medium">{{ analysisB.metadata.title }}</th>
                <th class="text-center px-4 py-2.5 text-muted font-medium">Diff</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="kpi in matchedKpis" :key="kpi.label" class="border-t border-[var(--border-card)]">
                <td class="px-4 py-3 text-body font-medium">{{ kpi.label }}</td>
                <td class="px-4 py-3 text-center text-heading font-bold">{{ kpi.a.value }}</td>
                <td class="px-4 py-3 text-center text-heading font-bold">{{ kpi.b?.value ?? '—' }}</td>
                <td class="px-4 py-3 text-center font-mono text-sm"
                  :class="kpi.diff === null ? 'text-faint' : kpi.diff.startsWith('+') ? 'text-emerald-400' : 'text-red-400'"
                >
                  {{ kpi.diff ?? '—' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Side by side sections -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Analysis A -->
        <div class="flex flex-col gap-4">
          <h3 class="text-lg font-semibold text-sky-400 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            {{ analysisA.metadata.title }}
          </h3>
          <SectionRenderer
            v-for="(section, i) in analysisA.sections"
            :key="'a-' + i"
            :section="section"
          />
        </div>

        <!-- Analysis B -->
        <div class="flex flex-col gap-4">
          <h3 class="text-lg font-semibold text-violet-400 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-violet-400"></span>
            {{ analysisB.metadata.title }}
          </h3>
          <SectionRenderer
            v-for="(section, i) in analysisB.sections"
            :key="'b-' + i"
            :section="section"
          />
        </div>
      </div>
    </template>
  </div>
</template>
