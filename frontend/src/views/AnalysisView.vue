<script setup>
import { onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store.js'
import MetricGridRenderer from '../components/renderers/MetricGridRenderer.vue'
import SectionRenderer from '../components/renderers/SectionRenderer.vue'

const props = defineProps({ id: { type: String, required: true } })
const router = useRouter()

onMounted(() => store.fetchAnalysis(props.id))
watch(() => props.id, (newId) => store.fetchAnalysis(newId))
</script>

<template>
  <div class="flex flex-col gap-6 animate-fade-in">
    <!-- Back button -->
    <button
      @click="router.push('/')"
      class="inline-flex items-center gap-1.5 text-sm text-slate-400 hover:text-sky-400 transition-colors self-start cursor-pointer"
    >
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
      </svg>
      Todos los Analisis
    </button>

    <!-- Loading / Error -->
    <div v-if="store.loading" class="flex items-center justify-center py-16">
      <div class="text-slate-400 text-sm">Cargando analisis...</div>
    </div>
    <div v-else-if="store.error" class="glass-card p-8 text-center border-red-500/30">
      <p class="text-red-400">{{ store.error }}</p>
    </div>

    <template v-else-if="store.currentAnalysis">
      <!-- Header Card -->
      <div class="glass-card p-8">
        <h2 class="text-3xl font-bold text-slate-100 mb-3">
          {{ store.currentAnalysis.metadata.title }}
        </h2>
        <p v-if="store.currentAnalysis.metadata.description" class="text-slate-300 leading-relaxed mb-4">
          {{ store.currentAnalysis.metadata.description }}
        </p>
        <div class="flex items-center gap-4 flex-wrap text-sm">
          <span v-if="store.currentAnalysis.metadata.author" class="text-slate-300 font-medium">
            {{ store.currentAnalysis.metadata.author }}
          </span>
          <span class="text-slate-500">
            {{ store.currentAnalysis.metadata.created_at.slice(0, 10) }}
          </span>
          <a
            v-if="store.currentAnalysis.metadata.colab_url"
            :href="store.currentAnalysis.metadata.colab_url"
            target="_blank"
            class="inline-flex items-center gap-1 px-3 py-1 rounded-md border border-slate-600 text-sky-400 hover:bg-sky-500/10 transition-colors text-xs"
          >
            Abrir en Colab
          </a>
          <a
            v-if="store.currentAnalysis.metadata.github_url"
            :href="store.currentAnalysis.metadata.github_url"
            target="_blank"
            class="inline-flex items-center gap-1 px-3 py-1 rounded-md border border-slate-600 text-sky-400 hover:bg-sky-500/10 transition-colors text-xs"
          >
            Ver en GitHub
          </a>
        </div>
        <div v-if="store.currentAnalysis.metadata.tags.length" class="flex gap-2 flex-wrap mt-4">
          <span
            v-for="tag in store.currentAnalysis.metadata.tags"
            :key="tag"
            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-sky-500/10 text-sky-400 border border-sky-500/20"
          >
            {{ tag }}
          </span>
        </div>
      </div>

      <!-- KPI Bar -->
      <MetricGridRenderer
        v-if="store.currentAnalysis.kpis.length"
        :metrics="store.currentAnalysis.kpis"
      />

      <!-- Sections -->
      <div class="space-y-2">
        <SectionRenderer
          v-for="(section, i) in store.currentAnalysis.sections"
          :key="i"
          :section="section"
          :show-separator="i < store.currentAnalysis.sections.length - 1"
        />
      </div>
    </template>
  </div>
</template>
