<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store.js'
import { useSEO } from '../composables/useSEO.js'
import UploadFile from '../components/UploadFile.vue'
import SkeletonLoader from '../components/SkeletonLoader.vue'
import {
  CollapsibleRoot,
  CollapsibleTrigger,
  CollapsibleContent,
  DialogRoot,
  DialogTrigger,
  DialogPortal,
  DialogOverlay,
  DialogContent,
  DialogTitle,
  DialogClose,
} from 'reka-ui'

const router = useRouter()
const showLegacy = ref(false)
const activeTag = ref(null)
useSEO({ title: null, description: 'Galeria de analisis interactivos de Data Profiling' })

onMounted(() => {
  store.fetchAnalyses()
  store.fetchNotebooks()
})

const allTags = computed(() => {
  const tags = new Set()
  store.analyses.forEach(a => a.tags?.forEach(t => tags.add(t)))
  return [...tags].sort()
})

const filteredAnalyses = computed(() => {
  if (!activeTag.value) return store.analyses
  return store.analyses.filter(a => a.tags?.includes(activeTag.value))
})

function toggleTag(tag) {
  activeTag.value = activeTag.value === tag ? null : tag
}

function openAnalysis(id) {
  router.push({ name: 'analysis', params: { id } })
}

function openNotebook(id) {
  router.push({ name: 'notebook', params: { id } })
}
</script>

<template>
  <div class="flex flex-col gap-6 animate-fade-in">
    <!-- Header -->
    <div class="flex justify-between items-start flex-wrap gap-4">
      <div>
        <h2 class="text-3xl font-bold text-heading">Mis Analisis</h2>
        <p class="text-muted mt-1">Selecciona un analisis para visualizar su dashboard interactivo.</p>
      </div>

      <div class="flex items-center gap-2">
        <button
          v-if="store.analyses.length >= 2"
          @click="router.push('/compare')"
          class="inline-flex items-center gap-2 px-4 py-2.5 border border-slate-600 hover:border-sky-500/50 text-muted hover:text-sky-400 rounded-lg font-medium text-sm transition-colors cursor-pointer"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
          </svg>
          Comparar
        </button>

      <DialogRoot>
        <DialogTrigger
          class="inline-flex items-center gap-2 px-5 py-2.5 bg-sky-500 hover:bg-sky-600 text-white rounded-lg font-semibold text-sm transition-colors cursor-pointer"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          Subir Archivo
        </DialogTrigger>
        <DialogPortal>
          <DialogOverlay class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 animate-fade-in" />
          <DialogContent class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-lg animate-scale-in">
            <div class="glass-card p-6">
              <div class="flex items-center justify-between mb-4">
                <DialogTitle class="text-lg font-semibold text-slate-100">Subir Archivo</DialogTitle>
                <DialogClose class="text-slate-400 hover:text-slate-200 transition-colors cursor-pointer p-1">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </DialogClose>
              </div>
              <UploadFile @uploaded="store.fetchAnalyses(); store.fetchNotebooks()" />
            </div>
          </DialogContent>
        </DialogPortal>
      </DialogRoot>
      </div>
    </div>

    <!-- Tag filters -->
    <div v-if="allTags.length && !store.loading" class="flex items-center gap-2 flex-wrap">
      <span class="text-xs text-slate-500 mr-1">Filtrar:</span>
      <button
        v-for="tag in allTags"
        :key="tag"
        @click="toggleTag(tag)"
        :class="[
          'px-3 py-1 rounded-full text-xs font-medium transition-all duration-200 cursor-pointer border',
          activeTag === tag
            ? 'bg-sky-500 text-white border-sky-500'
            : 'bg-sky-500/10 text-sky-400 border-sky-500/20 hover:bg-sky-500/20'
        ]"
      >
        {{ tag }}
      </button>
      <button
        v-if="activeTag"
        @click="activeTag = null"
        class="px-2 py-1 text-xs text-slate-500 hover:text-slate-300 transition-colors cursor-pointer"
      >
        Limpiar
      </button>
    </div>

    <!-- Loading skeletons -->
    <div v-if="store.loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <SkeletonLoader variant="card" :count="6" />
    </div>

    <!-- Error -->
    <div v-else-if="store.error" class="glass-card p-8 text-center border-red-500/30">
      <p class="text-red-400">{{ store.error }}</p>
    </div>

    <!-- Analyses Grid -->
    <div v-else-if="filteredAnalyses.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <div
        v-for="a in filteredAnalyses"
        :key="a.id"
        class="glass-card p-6 hover:border-sky-500/30 transition-all duration-300 hover:-translate-y-1 cursor-pointer group"
        @click="openAnalysis(a.id)"
      >
        <h3 class="text-lg font-semibold text-heading group-hover:text-sky-400 transition-colors mb-2">
          {{ a.title }}
        </h3>
        <p class="text-sm text-muted line-clamp-2 mb-3 leading-relaxed">
          {{ a.description || 'Sin descripcion' }}
        </p>
        <div class="flex items-center gap-2 flex-wrap text-xs mb-3">
          <span v-if="a.author" class="text-slate-300 font-medium">{{ a.author }}</span>
          <span class="text-slate-500">{{ a.created_at.slice(0, 10) }}</span>
          <span class="px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 font-semibold">{{ a.kpi_count }} KPIs</span>
          <span class="px-2 py-0.5 rounded-full bg-violet-500/15 text-violet-400 font-semibold">{{ a.section_count }} secciones</span>
          <span v-if="a.has_model" class="px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 font-semibold">Modelo</span>
        </div>
        <div v-if="a.tags.length" class="flex gap-2 flex-wrap">
          <span
            v-for="tag in a.tags"
            :key="tag"
            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-sky-500/10 text-sky-400 border border-sky-500/20"
          >
            {{ tag }}
          </span>
        </div>
      </div>
    </div>

    <div v-else-if="!store.loading && !store.error && activeTag && store.analyses.length" class="text-center py-12 text-slate-500">
      <p>No hay analisis con el tag <span class="text-sky-400">"{{ activeTag }}"</span>.</p>
    </div>

    <div v-else-if="!store.loading && !store.error && !store.analyses.length" class="text-center py-16 text-slate-500">
      <p>No hay analisis disponibles.</p>
      <p class="text-sm mt-1">Exporta un Data Contract desde tu notebook o sube un archivo <code class="bg-slate-700/50 text-sky-300 px-1.5 py-0.5 rounded text-sm">.json</code>.</p>
    </div>

    <!-- Legacy Notebooks -->
    <CollapsibleRoot v-if="store.notebooks.length" v-model:open="showLegacy" class="mt-2">
      <CollapsibleTrigger class="flex items-center gap-2 text-sm text-slate-500 hover:text-sky-400 transition-colors cursor-pointer select-none py-1">
        <svg
          :class="['w-4 h-4 transition-transform duration-200', showLegacy ? 'rotate-90' : '']"
          fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
        </svg>
        Notebooks legacy ({{ store.notebooks.length }})
      </CollapsibleTrigger>

      <CollapsibleContent>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mt-4">
          <div
            v-for="nb in store.notebooks"
            :key="nb.id"
            class="glass-card p-5 hover:border-sky-500/30 transition-all duration-200 hover:-translate-y-0.5 cursor-pointer group"
            @click="openNotebook(nb.id)"
          >
            <h3 class="text-base font-semibold text-heading group-hover:text-sky-400 transition-colors mb-1">
              {{ nb.title }}
            </h3>
            <p class="text-sm text-muted line-clamp-2 mb-2">{{ nb.description || 'Sin descripcion' }}</p>
            <div class="flex items-center gap-2 text-xs mb-2">
              <span class="px-2 py-0.5 rounded-full bg-sky-500/15 text-sky-400 font-semibold">{{ nb.code_cells }} code</span>
              <span class="px-2 py-0.5 rounded-full bg-violet-500/15 text-violet-400 font-semibold">{{ nb.markdown_cells }} md</span>
            </div>
            <div class="text-xs text-slate-500 font-mono">{{ nb.filename }}</div>
          </div>
        </div>
      </CollapsibleContent>
    </CollapsibleRoot>
  </div>
</template>
