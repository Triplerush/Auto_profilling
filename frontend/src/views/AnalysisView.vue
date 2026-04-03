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
  <div class="analysis-view">
    <button class="back-btn" @click="router.push('/')">&larr; Todos los Analisis</button>

    <div v-if="store.loading" class="status-msg">Cargando analisis...</div>
    <div v-else-if="store.error" class="status-msg error">{{ store.error }}</div>

    <template v-else-if="store.currentAnalysis">
      <div class="analysis-header">
        <h2>{{ store.currentAnalysis.metadata.title }}</h2>
        <p class="analysis-desc">{{ store.currentAnalysis.metadata.description }}</p>
        <div class="analysis-meta">
          <span v-if="store.currentAnalysis.metadata.author" class="meta-item">
            {{ store.currentAnalysis.metadata.author }}
          </span>
          <span class="meta-item">{{ store.currentAnalysis.metadata.created_at.slice(0, 10) }}</span>
          <a
            v-if="store.currentAnalysis.metadata.colab_url"
            :href="store.currentAnalysis.metadata.colab_url"
            target="_blank"
            class="meta-link"
          >Abrir en Colab</a>
          <a
            v-if="store.currentAnalysis.metadata.github_url"
            :href="store.currentAnalysis.metadata.github_url"
            target="_blank"
            class="meta-link"
          >Ver en GitHub</a>
        </div>
        <div v-if="store.currentAnalysis.metadata.tags.length" class="tags">
          <span v-for="tag in store.currentAnalysis.metadata.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>

      <MetricGridRenderer
        v-if="store.currentAnalysis.kpis.length"
        :metrics="store.currentAnalysis.kpis"
      />

      <SectionRenderer
        v-for="(section, i) in store.currentAnalysis.sections"
        :key="i"
        :section="section"
      />
    </template>
  </div>
</template>

<style scoped>
.analysis-view { display: flex; flex-direction: column; gap: 1.25rem; }
.back-btn {
  align-self: flex-start;
  background: transparent; color: var(--accent); border: 1px solid var(--border);
  border-radius: 6px; padding: 0.4rem 0.85rem; font-size: 0.8rem;
  cursor: pointer; transition: background 0.2s;
}
.back-btn:hover { background: rgba(56, 189, 248, 0.1); }
.status-msg { text-align: center; padding: 3rem; color: var(--text-secondary); }
.status-msg.error { color: var(--danger); }
.analysis-header { margin-bottom: 0.25rem; }
.analysis-header h2 { font-size: 1.35rem; color: var(--accent); }
.analysis-desc { font-size: 0.88rem; color: var(--text-secondary); margin-top: 0.3rem; line-height: 1.5; }
.analysis-meta {
  display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;
  margin-top: 0.5rem; font-size: 0.78rem;
}
.meta-item { color: var(--text-secondary); }
.meta-link {
  color: var(--accent); text-decoration: none; border: 1px solid var(--border);
  padding: 0.2rem 0.5rem; border-radius: 4px;
}
.meta-link:hover { background: rgba(56, 189, 248, 0.1); }
.tags { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-top: 0.5rem; }
.tag {
  font-size: 0.7rem; padding: 0.15rem 0.5rem; border-radius: 4px;
  background: rgba(56, 189, 248, 0.12); color: var(--accent); font-weight: 500;
}
</style>
