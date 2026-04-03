<script setup>
import ChartRenderer from './ChartRenderer.vue'
import DataFrameRenderer from './DataFrameRenderer.vue'
import MetricGridRenderer from './MetricGridRenderer.vue'
import CorrelationRenderer from './CorrelationRenderer.vue'
import ConfusionMatrixRenderer from './ConfusionMatrixRenderer.vue'
import TextRenderer from './TextRenderer.vue'
import CodeSnippetRenderer from './CodeSnippetRenderer.vue'

defineProps({
  section: { type: Object, required: true },
})

const rendererMap = {
  chart: ChartRenderer,
  dataframe: DataFrameRenderer,
  metric_grid: MetricGridRenderer,
  correlation_matrix: CorrelationRenderer,
  confusion_matrix: ConfusionMatrixRenderer,
  text: TextRenderer,
  code_snippet: CodeSnippetRenderer,
}
</script>

<template>
  <div class="section">
    <h3 class="section-title">{{ section.title }}</h3>
    <p v-if="section.description" class="section-desc">{{ section.description }}</p>
    <div class="section-components">
      <template v-for="(comp, i) in section.components" :key="i">
        <component
          v-if="rendererMap[comp.type]"
          :is="rendererMap[comp.type]"
          :component="comp"
          :metrics="comp.type === 'metric_grid' ? comp.metrics : undefined"
        />
        <div v-else-if="comp.type === 'image'" class="image-wrapper">
          <h4 v-if="comp.title" class="img-title">{{ comp.title }}</h4>
          <img :src="comp.src" :alt="comp.alt || comp.title || ''" class="section-img" />
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.section { margin-bottom: 1.5rem; }
.section-title {
  font-size: 1.1rem;
  color: var(--accent);
  margin-bottom: 0.3rem;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid var(--border);
}
.section-desc {
  font-size: 0.82rem;
  color: var(--text-secondary);
  margin-bottom: 0.75rem;
}
.section-components {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.image-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
  text-align: center;
}
.img-title { font-size: 0.9rem; color: var(--text-primary); margin-bottom: 0.5rem; }
.section-img { max-width: 100%; height: auto; border-radius: 6px; cursor: zoom-in; }
</style>
