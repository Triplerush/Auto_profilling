<script setup>
import { onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store.js'
import NotebookCellRenderer from '../components/NotebookCellRenderer.vue'
import SkeletonLoader from '../components/SkeletonLoader.vue'
import { useSEO } from '../composables/useSEO.js'

const props = defineProps({ id: { type: String, required: true } })
const router = useRouter()
const { update: updateSEO } = useSEO({})

onMounted(() => store.fetchNotebook(props.id))
watch(() => props.id, (newId) => store.fetchNotebook(newId))
watch(() => store.currentNotebook, (nb) => {
  if (nb) updateSEO(nb.title, `Notebook: ${nb.filename}`)
})
</script>

<template>
  <div class="flex flex-col gap-4 animate-fade-in">
    <!-- Back button -->
    <button
      @click="router.push('/')"
      class="inline-flex items-center gap-1.5 text-sm text-slate-400 hover:text-sky-400 transition-colors self-start cursor-pointer"
    >
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
      </svg>
      Todos los Notebooks
    </button>

    <!-- Loading skeletons -->
    <template v-if="store.loading">
      <SkeletonLoader variant="header" />
      <SkeletonLoader variant="card" :count="3" />
    </template>

    <!-- Error -->
    <div v-else-if="store.error" class="glass-card p-8 text-center border-red-500/30">
      <p class="text-red-400">{{ store.error }}</p>
    </div>

    <template v-else-if="store.currentNotebook">
      <!-- Header -->
      <div class="glass-card p-6 mb-2">
        <h2 class="text-2xl font-bold text-heading mb-1">{{ store.currentNotebook.title }}</h2>
        <span class="text-xs text-slate-500 font-mono">{{ store.currentNotebook.filename }}</span>
      </div>

      <!-- Cells -->
      <div class="flex flex-col gap-3">
        <NotebookCellRenderer
          v-for="cell in store.currentNotebook.cells"
          :key="cell.index"
          :cell="cell"
        />
      </div>
    </template>
  </div>
</template>
