<script setup>
import { ref, reactive, computed } from 'vue'
import { api } from '../api.js'

const props = defineProps({
  model: { type: Object, required: true },
  analysisId: { type: String, required: true },
})

const recCfg = computed(() => props.model.recommendation || null)
const recEnabled = computed(() => !!recCfg.value?.enabled)

// --- One-hot group detection (existing logic) ---
const groups = computed(() => {
  const candidates = {}
  for (const col of props.model.input_schema) {
    const idx = col.lastIndexOf('_')
    if (idx === -1) continue
    const prefix = col.substring(0, idx)
    const value = col.substring(idx + 1)
    if (!candidates[prefix]) candidates[prefix] = []
    candidates[prefix].push({ col, value })
  }
  const result = {}
  for (const [prefix, members] of Object.entries(candidates)) {
    if (members.length < 2) continue
    const allBinary = members.every(m => {
      const v = props.model.sample_input[m.col]
      return v === 0 || v === 1
    })
    if (allBinary) result[prefix] = members
  }
  return result
})

const groupedCols = computed(() => {
  const set = new Set()
  for (const members of Object.values(groups.value)) {
    for (const m of members) set.add(m.col)
  }
  return set
})

// Field classification: 'group' | 'binary' (single 0/1 flag) | 'log' (*_log → natural input) | 'number'
const fields = computed(() => {
  const seen = new Set()
  const out = []
  for (const col of props.model.input_schema) {
    if (groupedCols.value.has(col)) {
      for (const [prefix, members] of Object.entries(groups.value)) {
        if (members.some(m => m.col === col)) {
          if (!seen.has(prefix)) {
            seen.add(prefix)
            out.push({ kind: 'group', prefix, members })
          }
          break
        }
      }
      continue
    }

    if (col.endsWith('_log')) {
      out.push({ kind: 'log', col, label: col.slice(0, -'_log'.length) })
      continue
    }

    const sample = props.model.sample_input[col]
    if (sample === 0 || sample === 1) {
      out.push({ kind: 'binary', col })
      continue
    }

    out.push({ kind: 'number', col })
  }
  return out
})

// Raw values that get sent to the API (one entry per input_schema column).
const formValues = reactive(
  Object.fromEntries(
    props.model.input_schema.map(col => [col, props.model.sample_input[col] ?? 0])
  )
)

// Natural-value mirror for *_log fields. We keep the log value in `formValues`
// (what the API needs) and the human-readable value here.
const naturalValues = reactive({})
function initNaturalValues() {
  for (const f of fields.value) {
    if (f.kind === 'log') {
      const logVal = props.model.sample_input[f.col] ?? 0
      naturalValues[f.col] = Number(Math.exp(logVal).toFixed(2))
    }
  }
}

function onNaturalChange(col, raw) {
  const n = Number(raw)
  naturalValues[col] = n
  formValues[col] = n > 0 ? Math.log(n) : 0
}

const groupSelection = reactive({})
function initGroupSelection() {
  for (const [prefix, members] of Object.entries(groups.value)) {
    const active = members.find(m => props.model.sample_input[m.col] === 1)
    groupSelection[prefix] = active ? active.col : members[0].col
  }
}

initGroupSelection()
initNaturalValues()

function onGroupChange(prefix, selectedCol) {
  for (const m of groups.value[prefix]) {
    formValues[m.col] = m.col === selectedCol ? 1 : 0
  }
}

function onBinaryChange(col, checked) {
  formValues[col] = checked ? 1 : 0
}

function resetToSample() {
  for (const col of props.model.input_schema) {
    formValues[col] = props.model.sample_input[col] ?? 0
  }
  initGroupSelection()
  initNaturalValues()
}

const loading = ref(false)
const error = ref('')
const result = ref(null)
const recResult = ref(null)

async function submit() {
  loading.value = true
  error.value = ''
  result.value = null
  recResult.value = null

  const path = recEnabled.value
    ? `/v1/models/${props.analysisId}/recommend`
    : `/v1/models/${props.analysisId}/predict`

  try {
    const res = await fetch(api(path), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ features: { ...formValues } }),
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      throw new Error(data.detail || `Error ${res.status}`)
    }
    const data = await res.json()
    if (recEnabled.value) {
      recResult.value = data
    } else {
      result.value = data
    }
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function formatMetricName(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}

const PERCENTAGE_METRICS = new Set([
  'accuracy', 'precision', 'recall',
  'f1', 'f1_macro', 'f1_micro', 'f1_weighted',
  'auc', 'roc_auc', 'pr_auc',
])

function formatMetricValue(value, key) {
  if (typeof value !== 'number') return String(value)
  if (PERCENTAGE_METRICS.has(String(key).toLowerCase())) {
    return `${(value * 100).toFixed(1)}%`
  }
  return value.toFixed(3)
}

function humanizeBinary(col) {
  return col.replace(/^is_/, '').replace(/_/g, ' ')
}
</script>

<template>
  <div class="glass-card p-6 sm:p-8 animate-fade-in">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-2">
      <div class="w-1 h-6 bg-emerald-500 rounded-full"></div>
      <h3 class="text-xl font-bold text-heading">
        {{ recEnabled ? (recCfg.label || 'Recomendaciones') : 'Probar Modelo' }}
      </h3>
    </div>
    <p class="text-sm text-muted mb-5 ml-4">
      <template v-if="recEnabled">
        Marca tus preferencias y obten las mejores recomendaciones del catalogo segun el modelo.
      </template>
      <template v-else>
        Ingresa los valores de las features para obtener una prediccion del modelo.
      </template>
    </p>

    <!-- Model metrics badges -->
    <div class="flex gap-2 flex-wrap mb-6 ml-4">
      <span
        v-for="(value, key) in model.metrics"
        :key="key"
        class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
      >
        {{ formatMetricName(key) }}: {{ formatMetricValue(value, key) }}
      </span>
      <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-slate-500/10 text-slate-400 border border-slate-500/20">
        {{ model.format.toUpperCase() }}
      </span>
    </div>

    <!-- Form -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
      <template v-for="field in fields" :key="field.kind === 'group' ? `g:${field.prefix}` : `${field.kind}:${field.col}`">
        <!-- Grouped One-Hot columns rendered as a single select -->
        <div v-if="field.kind === 'group'" class="flex flex-col gap-1.5">
          <label :for="`field-${field.prefix}`" class="text-xs font-medium text-muted truncate" :title="field.prefix">
            {{ field.prefix }}
          </label>
          <select
            :id="`field-${field.prefix}`"
            :value="groupSelection[field.prefix]"
            @change="onGroupChange(field.prefix, $event.target.value)"
            class="w-full px-3 py-2 rounded-lg text-sm text-heading bg-[var(--bg-card-solid,rgb(30_41_59/0.8))] border border-[var(--border-card)] focus:outline-none focus:ring-2 focus:ring-sky-500/50 focus:border-sky-500/50 transition-colors"
          >
            <option v-for="m in field.members" :key="m.col" :value="m.col">
              {{ m.value }}
            </option>
          </select>
        </div>

        <!-- Single binary flag rendered as a checkbox -->
        <div v-else-if="field.kind === 'binary'" class="flex flex-col gap-1.5">
          <label :for="`field-${field.col}`" class="text-xs font-medium text-muted truncate" :title="field.col">
            {{ field.col }}
          </label>
          <label
            :for="`field-${field.col}`"
            class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm bg-[var(--bg-card-solid,rgb(30_41_59/0.8))] border border-[var(--border-card)] cursor-pointer hover:border-sky-500/50 transition-colors"
          >
            <input
              :id="`field-${field.col}`"
              type="checkbox"
              :checked="formValues[field.col] === 1"
              @change="onBinaryChange(field.col, $event.target.checked)"
              class="w-4 h-4 accent-emerald-500 cursor-pointer"
            />
            <span class="text-heading capitalize">{{ humanizeBinary(field.col) }}</span>
          </label>
        </div>

        <!-- *_log column rendered as natural value (we send Math.log of it) -->
        <div v-else-if="field.kind === 'log'" class="flex flex-col gap-1.5">
          <label :for="`field-${field.col}`" class="text-xs font-medium text-muted truncate flex items-center gap-1" :title="field.col">
            {{ field.label }}
            <span class="text-[10px] text-muted/70 normal-case">(valor natural)</span>
          </label>
          <input
            :id="`field-${field.col}`"
            type="number"
            min="0"
            step="any"
            :value="naturalValues[field.col]"
            @input="onNaturalChange(field.col, $event.target.value)"
            class="w-full px-3 py-2 rounded-lg text-sm text-heading bg-[var(--bg-card-solid,rgb(30_41_59/0.8))] border border-[var(--border-card)] focus:outline-none focus:ring-2 focus:ring-sky-500/50 focus:border-sky-500/50 transition-colors"
          />
        </div>

        <!-- Default: continuous numeric input -->
        <div v-else class="flex flex-col gap-1.5">
          <label :for="`field-${field.col}`" class="text-xs font-medium text-muted truncate" :title="field.col">
            {{ field.col }}
          </label>
          <input
            :id="`field-${field.col}`"
            v-model.number="formValues[field.col]"
            type="number"
            step="any"
            class="w-full px-3 py-2 rounded-lg text-sm text-heading bg-[var(--bg-card-solid,rgb(30_41_59/0.8))] border border-[var(--border-card)] focus:outline-none focus:ring-2 focus:ring-sky-500/50 focus:border-sky-500/50 transition-colors"
          />
        </div>
      </template>
    </div>

    <!-- Submit -->
    <div class="flex items-center gap-4 mb-6">
      <button
        @click="submit"
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
        {{ loading ? (recEnabled ? 'Buscando...' : 'Prediciendo...') : (recEnabled ? 'Recomendar' : 'Predecir') }}
      </button>

      <button
        @click="resetToSample"
        class="text-xs text-muted hover:text-sky-400 transition-colors cursor-pointer"
      >
        Restaurar valores de ejemplo
      </button>
    </div>

    <!-- Error -->
    <div v-if="error" class="glass-card p-4 border-red-500/30 mb-4">
      <p class="text-sm text-red-400">{{ error }}</p>
    </div>

    <!-- Recommendation result -->
    <div v-if="recResult" class="glass-card p-6 border-emerald-500/20 animate-slide-up">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-1 h-5 bg-emerald-500 rounded-full"></div>
        <h4 class="text-sm font-semibold text-muted uppercase tracking-wider">{{ recResult.label || 'Recomendaciones' }}</h4>
      </div>

      <div class="flex items-baseline gap-2 mb-4">
        <span class="text-xs text-muted">Rating predicho para tu seleccion:</span>
        <span class="text-2xl font-bold text-emerald-400">{{ recResult.predicted_rating?.toFixed?.(2) ?? recResult.predicted_rating }}</span>
        <span class="text-xs text-muted">/ 10</span>
      </div>

      <div v-if="recResult.user_categories && Object.keys(recResult.user_categories).length" class="flex flex-wrap gap-1.5 mb-4">
        <span
          v-for="(value, key) in recResult.user_categories"
          :key="key"
          class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs bg-sky-500/10 text-sky-400 border border-sky-500/20"
        >
          <span class="text-muted/80">{{ key }}:</span> {{ value }}
        </span>
      </div>

      <div class="space-y-2">
        <div
          v-for="(item, idx) in recResult.items"
          :key="idx"
          class="flex items-center gap-3 p-3 rounded-lg bg-[var(--bg-card-solid,rgb(30_41_59/0.6))] border border-[var(--border-card)] hover:border-emerald-500/30 transition-colors"
        >
          <span class="text-xl font-bold text-emerald-400 w-6 text-center">{{ idx + 1 }}</span>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold text-heading truncate">{{ item.title }}</p>
            <div class="flex flex-wrap gap-1.5 mt-1">
              <span v-if="item.type" class="text-[10px] px-2 py-0.5 rounded-full bg-slate-500/15 text-slate-300">{{ item.type }}</span>
              <span v-if="item.genre" class="text-[10px] px-2 py-0.5 rounded-full bg-purple-500/15 text-purple-300">{{ item.genre }}</span>
              <span v-if="item.platform" class="text-[10px] px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-300">{{ item.platform }}</span>
              <span v-if="item.country" class="text-[10px] px-2 py-0.5 rounded-full bg-sky-500/15 text-sky-300">{{ item.country }}</span>
              <span v-if="item.language" class="text-[10px] px-2 py-0.5 rounded-full bg-pink-500/15 text-pink-300">{{ item.language }}</span>
            </div>
          </div>
          <div class="text-right shrink-0">
            <p class="text-lg font-bold text-heading">{{ item[recResult.rating_field]?.toFixed?.(1) ?? item[recResult.rating_field] }}</p>
            <p class="text-[10px] text-muted">{{ item.match_count }}/{{ Object.keys(recResult.user_categories || {}).length }} match</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Predict result (legacy path for non-recommend models) -->
    <div v-else-if="result" class="glass-card p-6 border-emerald-500/20 animate-slide-up">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-1 h-5 bg-emerald-500 rounded-full"></div>
        <h4 class="text-sm font-semibold text-muted uppercase tracking-wider">Resultado</h4>
      </div>

      <div class="flex items-center gap-6 flex-wrap">
        <div class="text-center">
          <p class="text-xs text-muted mb-1">Prediccion</p>
          <p class="text-3xl font-bold text-heading">{{ result.prediction }}</p>
        </div>

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

        <div v-if="result.probability != null" class="text-center">
          <p class="text-xs text-muted mb-1">Probabilidad</p>
          <p class="text-lg font-semibold text-heading">{{ (result.probability * 100).toFixed(1) }}%</p>
        </div>
      </div>
    </div>
  </div>
</template>
