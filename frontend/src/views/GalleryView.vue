<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store.js'
import UploadFile from '../components/UploadFile.vue'

const router = useRouter()
const showUpload = ref(false)
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

function onUploaded() {
  showUpload.value = false
  store.fetchAnalyses()
  store.fetchNotebooks()
}
</script>

<template>
  <div class="gallery">
    <div class="gallery-header">
      <div>
        <h2>Mis Analisis</h2>
        <p>Selecciona un analisis para visualizar su dashboard interactivo.</p>
      </div>
      <button class="btn" @click="showUpload = !showUpload">
        {{ showUpload ? 'Cancelar' : 'Subir Archivo' }}
      </button>
    </div>

    <UploadFile v-if="showUpload" @uploaded="onUploaded" />

    <div v-if="store.loading" class="status-msg">Cargando...</div>
    <div v-else-if="store.error" class="status-msg error">{{ store.error }}</div>

    <!-- Analyses (primary) -->
    <div v-if="store.analyses.length" class="grid">
      <div
        v-for="a in store.analyses"
        :key="a.id"
        class="analysis-card"
        @click="openAnalysis(a.id)"
      >
        <h3 class="card-title">{{ a.title }}</h3>
        <p class="card-desc">{{ a.description || 'Sin descripcion' }}</p>
        <div class="card-meta">
          <span v-if="a.author" class="meta-author">{{ a.author }}</span>
          <span class="meta-date">{{ a.created_at.slice(0, 10) }}</span>
          <span class="badge kpi">{{ a.kpi_count }} KPIs</span>
          <span class="badge section">{{ a.section_count }} secciones</span>
        </div>
        <div v-if="a.tags.length" class="card-tags">
          <span v-for="tag in a.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>
    </div>

    <div v-else-if="!store.loading && !store.error" class="status-msg">
      No hay analisis disponibles. Exporta un Data Contract desde tu notebook o sube un archivo <code>.json</code>.
    </div>

    <!-- Legacy notebooks (secondary) -->
    <div v-if="store.notebooks.length" class="legacy-section">
      <button class="legacy-toggle" @click="showLegacy = !showLegacy">
        {{ showLegacy ? '▾' : '▸' }} Notebooks legacy ({{ store.notebooks.length }})
      </button>
      <div v-if="showLegacy" class="grid legacy-grid">
        <div
          v-for="nb in store.notebooks"
          :key="nb.id"
          class="nb-card"
          @click="openNotebook(nb.id)"
        >
          <h3 class="card-title">{{ nb.title }}</h3>
          <p class="card-desc">{{ nb.description || 'Sin descripcion' }}</p>
          <div class="card-meta">
            <span class="badge code">{{ nb.code_cells }} code</span>
            <span class="badge md">{{ nb.markdown_cells }} md</span>
          </div>
          <div class="nb-file">{{ nb.filename }}</div>
        </div>
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
.analysis-card, .nb-card {
  background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px;
  padding: 1.25rem; cursor: pointer; transition: border-color 0.2s, transform 0.15s;
}
.analysis-card:hover, .nb-card:hover { border-color: var(--accent); transform: translateY(-2px); }
.card-title { font-size: 1rem; color: var(--text-primary); margin-bottom: 0.4rem; }
.card-desc {
  font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
  margin-bottom: 0.75rem;
}
.card-meta { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; margin-bottom: 0.5rem; }
.meta-author { font-size: 0.75rem; color: var(--text-primary); font-weight: 500; }
.meta-date { font-size: 0.72rem; color: var(--text-secondary); }
.badge {
  font-size: 0.68rem; padding: 0.15rem 0.45rem; border-radius: 4px; font-weight: 600;
}
.badge.kpi { background: rgba(34, 197, 94, 0.15); color: var(--success); }
.badge.section { background: rgba(167, 139, 250, 0.15); color: var(--purple); }
.badge.code { background: rgba(56, 189, 248, 0.15); color: var(--accent); }
.badge.md { background: rgba(167, 139, 250, 0.15); color: var(--purple); }
.card-tags { display: flex; gap: 0.3rem; flex-wrap: wrap; }
.tag {
  font-size: 0.65rem; padding: 0.12rem 0.4rem; border-radius: 4px;
  background: rgba(56, 189, 248, 0.1); color: var(--accent);
}
.nb-file { font-size: 0.7rem; color: var(--text-secondary); font-family: monospace; }
.legacy-section { margin-top: 0.5rem; }
.legacy-toggle {
  background: transparent; border: none; color: var(--text-secondary);
  font-size: 0.82rem; cursor: pointer; padding: 0.3rem 0;
}
.legacy-toggle:hover { color: var(--accent); }
.legacy-grid { margin-top: 0.75rem; }
</style>
