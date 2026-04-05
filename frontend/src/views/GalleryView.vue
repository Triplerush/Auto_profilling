<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store.js'
import UploadFile from '../components/UploadFile.vue'
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

onMounted(() => {
  store.fetchAnalyses()
  store.fetchNotebooks()
})

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
        <h2 class="text-3xl font-bold text-slate-100">Mis Analisis</h2>
        <p class="text-slate-400 mt-1">Selecciona un analisis para visualizar su dashboard interactivo.</p>
      </div>

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

    <!-- Loading / Error -->
    <div v-if="store.loading" class="flex items-center justify-center py-16">
      <div class="text-slate-400 text-sm">Cargando...</div>
    </div>
    <div v-else-if="store.error" class="glass-card p-8 text-center border-red-500/30">
      <p class="text-red-400">{{ store.error }}</p>
    </div>

    <!-- Analyses Grid -->
    <div v-if="store.analyses.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <div
        v-for="a in store.analyses"
        :key="a.id"
        class="glass-card p-6 hover:border-sky-500/30 transition-all duration-300 hover:-translate-y-1 cursor-pointer group"
        @click="openAnalysis(a.id)"
      >
        <h3 class="text-lg font-semibold text-slate-100 group-hover:text-sky-400 transition-colors mb-2">
          {{ a.title }}
        </h3>
        <p class="text-sm text-slate-400 line-clamp-2 mb-3 leading-relaxed">
          {{ a.description || 'Sin descripcion' }}
        </p>
        <div class="flex items-center gap-2 flex-wrap text-xs mb-3">
          <span v-if="a.author" class="text-slate-300 font-medium">{{ a.author }}</span>
          <span class="text-slate-500">{{ a.created_at.slice(0, 10) }}</span>
          <span class="px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 font-semibold">{{ a.kpi_count }} KPIs</span>
          <span class="px-2 py-0.5 rounded-full bg-violet-500/15 text-violet-400 font-semibold">{{ a.section_count }} secciones</span>
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

    <div v-else-if="!store.loading && !store.error" class="text-center py-16 text-slate-500">
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
            <h3 class="text-base font-semibold text-slate-100 group-hover:text-sky-400 transition-colors mb-1">
              {{ nb.title }}
            </h3>
            <p class="text-sm text-slate-400 line-clamp-2 mb-2">{{ nb.description || 'Sin descripcion' }}</p>
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
