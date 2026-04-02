<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store.js'
import UploadNotebook from '../components/UploadNotebook.vue'

const router = useRouter()
const showUpload = ref(false)

onMounted(() => {
  store.fetchNotebooks()
})

function openNotebook(id) {
  router.push({ name: 'notebook', params: { id } })
}

function onUploaded() {
  showUpload.value = false
  store.fetchNotebooks()
}
</script>

<template>
  <div class="gallery">
    <div class="gallery-header">
      <div>
        <h2>Mis Notebooks</h2>
        <p>Selecciona un notebook para visualizar su analisis.</p>
      </div>
      <button class="btn" @click="showUpload = !showUpload">
        {{ showUpload ? 'Cancelar' : 'Subir Notebook' }}
      </button>
    </div>

    <UploadNotebook v-if="showUpload" @uploaded="onUploaded" />

    <div v-if="store.loading" class="status-msg">Cargando notebooks...</div>
    <div v-else-if="store.error" class="status-msg error">{{ store.error }}</div>
    <div v-else-if="store.notebooks.length === 0" class="status-msg">
      No hay notebooks disponibles. Sube uno o coloca archivos <code>.ipynb</code> en la carpeta de notebooks.
    </div>

    <div v-else class="grid">
      <div
        v-for="nb in store.notebooks"
        :key="nb.id"
        class="nb-card"
        @click="openNotebook(nb.id)"
      >
        <h3 class="nb-title">{{ nb.title }}</h3>
        <p class="nb-desc">{{ nb.description || 'Sin descripcion' }}</p>
        <div class="nb-meta">
          <span class="badge code">{{ nb.code_cells }} code</span>
          <span class="badge md">{{ nb.markdown_cells }} markdown</span>
          <span v-if="nb.has_images" class="badge img">graficos</span>
          <span v-if="nb.has_dataframes" class="badge df">tablas</span>
        </div>
        <div class="nb-file">{{ nb.filename }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gallery { display: flex; flex-direction: column; gap: 1.25rem; }
.gallery-header {
  display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;
}
.gallery-header h2 { font-size: 1.3rem; color: var(--accent); }
.gallery-header p { font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.2rem; }
.btn {
  padding: 0.5rem 1.25rem; background: var(--accent); color: var(--bg-dark);
  border: none; border-radius: 8px; font-weight: 600; font-size: 0.85rem;
  cursor: pointer; transition: background 0.2s;
}
.btn:hover { background: var(--accent-hover); }
.status-msg {
  text-align: center; padding: 3rem; color: var(--text-secondary); font-size: 0.9rem;
}
.status-msg.error { color: var(--danger); }
.status-msg code {
  background: var(--bg-code); padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.8rem;
}
.grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem;
}
.nb-card {
  background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px;
  padding: 1.25rem; cursor: pointer; transition: border-color 0.2s, transform 0.15s;
}
.nb-card:hover { border-color: var(--accent); transform: translateY(-2px); }
.nb-title { font-size: 1rem; color: var(--text-primary); margin-bottom: 0.4rem; }
.nb-desc {
  font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
  margin-bottom: 0.75rem;
}
.nb-meta { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 0.5rem; }
.badge {
  font-size: 0.68rem; padding: 0.15rem 0.45rem; border-radius: 4px; font-weight: 600;
}
.badge.code { background: rgba(56, 189, 248, 0.15); color: var(--accent); }
.badge.md { background: rgba(167, 139, 250, 0.15); color: var(--purple); }
.badge.img { background: rgba(52, 211, 153, 0.15); color: var(--green); }
.badge.df { background: rgba(251, 146, 60, 0.15); color: #fb923c; }
.nb-file { font-size: 0.7rem; color: var(--text-secondary); font-family: monospace; }
</style>
