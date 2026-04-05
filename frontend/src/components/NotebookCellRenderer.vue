<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import {
  CollapsibleRoot,
  CollapsibleTrigger,
  CollapsibleContent,
} from 'reka-ui'

const props = defineProps({
  cell: { type: Object, required: true },
})

const renderedMarkdown = computed(() => {
  if (props.cell.cell_type !== 'markdown') return ''
  return marked.parse(props.cell.source)
})
</script>

<template>
  <!-- Markdown Cell -->
  <div v-if="cell.cell_type === 'markdown'" class="glass-card p-5">
    <div class="prose-dark text-sm leading-relaxed" v-html="renderedMarkdown"></div>
  </div>

  <!-- Code Cell -->
  <div v-else-if="cell.cell_type === 'code'" class="glass-card overflow-hidden border-l-[3px] border-l-sky-500">
    <CollapsibleRoot>
      <CollapsibleTrigger
        class="flex items-center gap-2 w-full px-4 py-3 text-sm text-slate-400 hover:bg-sky-500/5 transition-colors cursor-pointer select-none"
      >
        <svg class="w-4 h-4 text-slate-500 transition-transform duration-200 [[data-state=open]_&]:rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
        </svg>
        <span v-if="cell.execution_count" class="text-sky-400 font-mono font-semibold text-xs">[{{ cell.execution_count }}]</span>
        <span class="text-xs">Codigo fuente</span>
        <span class="ml-auto px-2 py-0.5 rounded-full text-xs font-mono bg-sky-500/20 text-sky-400">code</span>
      </CollapsibleTrigger>

      <CollapsibleContent>
        <pre class="bg-slate-950 px-5 py-4 m-0 overflow-x-auto text-sm font-mono leading-relaxed text-slate-300 border-t border-slate-700/50"><code>{{ cell.source }}</code></pre>
      </CollapsibleContent>
    </CollapsibleRoot>

    <div v-if="cell.outputs.length > 0" class="border-t border-slate-700/50">
      <template v-for="(out, i) in cell.outputs" :key="i">
        <!-- Text output -->
        <pre v-if="out.output_type === 'text'" class="px-5 py-3 m-0 text-sm leading-relaxed text-slate-400 bg-slate-900/50 overflow-x-auto whitespace-pre-wrap break-words">{{ out.content }}</pre>

        <!-- HTML / DataFrame -->
        <div v-else-if="out.output_type === 'html'" class="px-5 py-3 overflow-x-auto text-sm prose-dark" v-html="out.content"></div>

        <!-- Image -->
        <div v-else-if="out.output_type === 'image'" class="p-4 text-center bg-slate-900/50">
          <img
            v-if="out.attrs?.mime_type === 'image/svg+xml'"
            :src="'data:image/svg+xml;utf8,' + encodeURIComponent(out.content)"
            alt="Output grafico"
            class="max-w-full h-auto rounded-lg inline-block"
          />
          <img v-else :src="out.content" alt="Output grafico" class="max-w-full h-auto rounded-lg inline-block" />
        </div>

        <!-- Error -->
        <pre v-else-if="out.output_type === 'error'" class="px-5 py-3 m-0 text-sm leading-snug text-red-400 bg-red-500/5 overflow-x-auto whitespace-pre-wrap">{{ out.content }}</pre>
      </template>
    </div>
  </div>
</template>
