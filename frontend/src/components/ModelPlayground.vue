<script setup>
import { ref, reactive } from 'vue'
import { api } from '../api.js'

const props = defineProps({
  model: { type: Object, required: true },
  analysisId: { type: String, required: true },
})

const formValues = reactive(
  Object.fromEntries(
    props.model.input_schema.map(col => [col, props.model.sample_input[col] ?? 0])
  )
)

const loading = ref(false)
const error = ref('')
const result = ref(null)

async function predict() {
  loading.value = true
  error.value = ''
  result.value = null

  try {
    const res = await fetch(api(`/v1/models/${props.analysisId}/predict`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ features: { ...formValues } }),
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      throw new Error(data.detail || `Error ${res.status}`)
    }
    result.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function formatMetricName(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}

function formatMetricValue(value) {
  if (value <= 1) return `${(value * 100).toFixed(1)}%`
  return value.toFixed(2)
}
</script>

<template>
  <div class="glass-card p-6 sm:p-8 animate-fade-in">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-2">
      <div class="w-1 h-6 bg-emerald-500 rounded-full"></div>
      <h3 class="text-xl font-bold text-heading">Probar Modelo</h3>
    </div>
    <p class="text-sm text-muted mb-5 ml-4">
      Ingresa los valores de las features para obtener una prediccion del modelo.
    </p>

    <!-- Model metrics badges -->
    <div class="flex gap-2 flex-wrap mb-6 ml-4">
      <span
        v-for="(value, key) in model.metrics"
        :key="key"
        class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
      >
        {{ formatMetricName(key) }}: {{ formatMetricValue(value) }}
      </span>
      <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-slate-500/10 text-slate-400 border border-slate-500/20">
        {{ model.format.toUpperCase() }}
      </span>
    </div>

    <!-- Form -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
      <div v-for="col in model.input_schema" :key="col" class="flex flex-col gap-1.5">
        <label :for="`field-${col}`" class="text-xs font-medium text-muted truncate" :title="col">
          {{ col }}
        </label>
        <input
          :id="`field-${col}`"
          v-model.number="formValues[col]"
          type="number"
          step="any"
          class="w-full px-3 py-2 rounded-lg text-sm text-heading bg-[var(--bg-card-solid,rgb(30_41_59/0.8))] border border-[var(--border-card)] focus:outline-none focus:ring-2 focus:ring-sky-500/50 focus:border-sky-500/50 transition-colors"
        />
      </div>
    </div>

    <!-- Predict button -->
    <div class="flex items-center gap-4 mb-6">
      <button
        @click="predict"
        :disabled="loading"
        class="inline-flex items-center gap-2 px-6 py-2.5 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg font-semibold text-sm transition-colors cursor-pointer"
      >
        <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        {{ loading ? 'Prediciendo...' : 'Predecir' }}
      </button>

      <button
        @click="Object.assign(formValues, model.sample_input)"
        class="text-xs text-muted hover:text-sky-400 transition-colors cursor-pointer"
      >
        Restaurar valores de ejemplo
      </button>
    </div>

    <!-- Error -->
    <div v-if="error" class="glass-card p-4 border-red-500/30 mb-4">
      <p class="text-sm text-red-400">{{ error }}</p>
    </div>

    <!-- Result -->
    <div v-if="result" class="glass-card p-6 border-emerald-500/20 animate-slide-up">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-1 h-5 bg-emerald-500 rounded-full"></div>
        <h4 class="text-sm font-semibold text-muted uppercase tracking-wider">Resultado</h4>
      </div>

      <div class="flex items-center gap-6 flex-wrap">
        <!-- Prediction -->
        <div class="text-center">
          <p class="text-xs text-muted mb-1">Prediccion</p>
          <p class="text-3xl font-bold text-heading">{{ result.prediction }}</p>
        </div>

        <!-- Confidence bar -->
        <div v-if="result.confidence != null" class="flex-1 min-w-[200px]">
          <div class="flex justify-between text-xs mb-1">
            <span class="text-muted">Confianza</span>
            <span class="text-heading font-semibold">{{ (result.confidence * 100).toFixed(1) }}%</span>
          </div>
          <div class="h-3 rounded-full bg-slate-700/50 overflow-hidden">
            <div
              class="h-full rounded-full transition-all duration-500 ease-out"
              :class="result.confidence > 0.7 ? 'bg-emerald-500' : result.confidence > 0.5 ? 'bg-amber-500' : 'bg-red-500'"
              :style="{ width: `${result.confidence * 100}%` }"
            ></div>
          </div>
        </div>

        <!-- Probability -->
        <div v-if="result.probability != null" class="text-center">
          <p class="text-xs text-muted mb-1">Probabilidad</p>
          <p class="text-lg font-semibold text-heading">{{ (result.probability * 100).toFixed(1) }}%</p>
        </div>
      </div>
    </div>
  </div>
</template>
