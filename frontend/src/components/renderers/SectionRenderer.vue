<script setup>
import { Separator } from 'reka-ui'
import ChartRenderer from './ChartRenderer.vue'
import DataFrameRenderer from './DataFrameRenderer.vue'
import MetricGridRenderer from './MetricGridRenderer.vue'
import CorrelationRenderer from './CorrelationRenderer.vue'
import ConfusionMatrixRenderer from './ConfusionMatrixRenderer.vue'
import TextRenderer from './TextRenderer.vue'
import CodeSnippetRenderer from './CodeSnippetRenderer.vue'

defineProps({
  section: { type: Object, required: true },
  showSeparator: { type: Boolean, default: false },
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
  <div class="animate-slide-up">
    <div class="flex items-center gap-3 mb-5">
      <div class="w-1 h-6 bg-sky-500 rounded-full"></div>
      <h3 class="text-xl font-bold text-heading">{{ section.title }}</h3>
    </div>
    <p v-if="section.description" class="text-sm text-slate-400 mb-5 -mt-2 ml-4">{{ section.description }}</p>

    <div class="space-y-5">
      <template v-for="(comp, i) in section.components" :key="i">
        <component
          v-if="rendererMap[comp.type]"
          :is="rendererMap[comp.type]"
          :component="comp"
          :metrics="comp.type === 'metric_grid' ? comp.metrics : undefined"
        />
        <div v-else-if="comp.type === 'image'" class="glass-card p-5 text-center">
          <h4 v-if="comp.title" class="text-sm font-medium text-slate-200 mb-3">{{ comp.title }}</h4>
          <img :src="comp.src" :alt="comp.alt || comp.title || ''" class="max-w-full h-auto rounded-lg inline-block" />
        </div>
      </template>
    </div>

    <Separator v-if="showSeparator" decorative class="h-px bg-slate-700/50 my-10" />
  </div>
</template>
