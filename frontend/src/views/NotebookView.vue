<script setup>
import { onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store.js'
import NotebookCellRenderer from '../components/NotebookCellRenderer.vue'

const props = defineProps({ id: { type: String, required: true } })
const router = useRouter()

onMounted(() => store.fetchNotebook(props.id))
watch(() => props.id, (newId) => store.fetchNotebook(newId))
</script>

<template>
  <div class="nb-view">
    <button class="back-btn" @click="router.push('/')">&larr; Todos los Notebooks</button>

    <div v-if="store.loading" class="status-msg">Cargando notebook...</div>
    <div v-else-if="store.error" class="status-msg error">{{ store.error }}</div>

    <template v-else-if="store.currentNotebook">
      <div class="nb-header">
        <h2>{{ store.currentNotebook.title }}</h2>
        <span class="nb-filename">{{ store.currentNotebook.filename }}</span>
      </div>

      <div class="cells">
        <NotebookCellRenderer
          v-for="cell in store.currentNotebook.cells"
          :key="cell.index"
          :cell="cell"
        />
      </div>
    </template>
  </div>
</template>

<style scoped>
.nb-view { display: flex; flex-direction: column; gap: 1rem; }
.back-btn {
  align-self: flex-start;
  background: transparent; color: var(--accent); border: 1px solid var(--border);
  border-radius: 6px; padding: 0.4rem 0.85rem; font-size: 0.8rem;
  cursor: pointer; transition: background 0.2s;
}
.back-btn:hover { background: rgba(56, 189, 248, 0.1); }
.status-msg { text-align: center; padding: 3rem; color: var(--text-secondary); }
.status-msg.error { color: var(--danger); }
.nb-header { margin-bottom: 0.5rem; }
.nb-header h2 { font-size: 1.25rem; color: var(--accent); }
.nb-filename { font-size: 0.75rem; color: var(--text-secondary); font-family: monospace; }
.cells { display: flex; flex-direction: column; gap: 0.5rem; }
</style>
