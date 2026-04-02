<script setup>
import { computed } from 'vue'
import { marked } from 'marked'

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
  <div v-if="cell.cell_type === 'markdown'" class="cell cell-md">
    <div class="md-content" v-html="renderedMarkdown"></div>
  </div>

  <!-- Code Cell -->
  <div v-else-if="cell.cell_type === 'code'" class="cell cell-code">
    <details class="code-source">
      <summary class="code-toggle">
        <span class="exec-badge" v-if="cell.execution_count">[{{ cell.execution_count }}]</span>
        Codigo fuente
      </summary>
      <pre class="source-pre"><code>{{ cell.source }}</code></pre>
    </details>

    <div v-if="cell.outputs.length > 0" class="outputs">
      <template v-for="(out, i) in cell.outputs" :key="i">
        <!-- Text output -->
        <pre v-if="out.output_type === 'text'" class="output-text">{{ out.content }}</pre>

        <!-- HTML / DataFrame -->
        <div v-else-if="out.output_type === 'html'" class="output-html" v-html="out.content"></div>

        <!-- Image -->
        <div v-else-if="out.output_type === 'image'" class="output-image">
          <img
            v-if="out.attrs?.mime_type === 'image/svg+xml'"
            :src="'data:image/svg+xml;utf8,' + encodeURIComponent(out.content)"
            alt="Output grafico"
          />
          <img v-else :src="out.content" alt="Output grafico" />
        </div>

        <!-- Error -->
        <pre v-else-if="out.output_type === 'error'" class="output-error">{{ out.content }}</pre>
      </template>
    </div>
  </div>
</template>

<style scoped>
.cell {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}

/* ─── Markdown ─── */
.cell-md { padding: 1.25rem 1.5rem; }
.md-content { line-height: 1.6; font-size: 0.9rem; }
.md-content :deep(h1) { font-size: 1.4rem; color: var(--accent); margin: 0.75rem 0 0.5rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }
.md-content :deep(h2) { font-size: 1.15rem; color: var(--accent); margin: 0.75rem 0 0.4rem; }
.md-content :deep(h3) { font-size: 1rem; color: var(--text-primary); margin: 0.6rem 0 0.3rem; }
.md-content :deep(p) { margin: 0.4rem 0; color: var(--text-secondary); }
.md-content :deep(strong) { color: var(--text-primary); }
.md-content :deep(code) { background: var(--bg-code); padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.82rem; }
.md-content :deep(ul), .md-content :deep(ol) { padding-left: 1.5rem; color: var(--text-secondary); }
.md-content :deep(li) { margin: 0.2rem 0; }
.md-content :deep(table) { width: 100%; border-collapse: collapse; margin: 0.5rem 0; font-size: 0.82rem; }
.md-content :deep(th), .md-content :deep(td) { padding: 0.4rem 0.6rem; border: 1px solid var(--border); text-align: left; }
.md-content :deep(th) { background: var(--bg-dark); color: var(--text-secondary); font-weight: 500; }
.md-content :deep(blockquote) { border-left: 3px solid var(--accent); padding-left: 1rem; color: var(--text-secondary); margin: 0.5rem 0; }

/* ─── Code ─── */
.cell-code { border-left: 3px solid var(--accent); }
.code-source { }
.code-toggle {
  display: block; padding: 0.6rem 1rem; font-size: 0.78rem; color: var(--text-secondary);
  cursor: pointer; user-select: none; transition: background 0.15s;
}
.code-toggle:hover { background: rgba(56, 189, 248, 0.05); }
.exec-badge {
  color: var(--accent); font-family: monospace; font-weight: 600; margin-right: 0.4rem;
}
.source-pre {
  background: var(--bg-code); padding: 1rem 1.25rem; margin: 0;
  overflow-x: auto; font-size: 0.8rem; line-height: 1.5; color: #c9d1d9;
  border-top: 1px solid var(--border);
}

/* ─── Outputs ─── */
.outputs { border-top: 1px solid var(--border); }
.output-text {
  padding: 0.75rem 1.25rem; margin: 0;
  font-size: 0.8rem; line-height: 1.5; color: var(--text-secondary);
  background: var(--bg-dark); overflow-x: auto; white-space: pre-wrap; word-break: break-word;
}
.output-html {
  padding: 0.75rem 1.25rem; overflow-x: auto; font-size: 0.82rem;
}
.output-html :deep(table) { width: 100%; border-collapse: collapse; }
.output-html :deep(th), .output-html :deep(td) {
  padding: 0.35rem 0.6rem; border: 1px solid var(--border); text-align: left; font-size: 0.78rem;
}
.output-html :deep(th) { background: var(--bg-dark); color: var(--text-secondary); font-weight: 500; }
.output-html :deep(td) { color: var(--text-primary); }
.output-html :deep(tr:nth-child(even)) { background: rgba(15, 23, 42, 0.5); }
.output-image { padding: 1rem; text-align: center; background: var(--bg-dark); }
.output-image img { max-width: 100%; height: auto; border-radius: 6px; }
.output-error {
  padding: 0.75rem 1.25rem; margin: 0;
  font-size: 0.78rem; line-height: 1.4; color: var(--danger);
  background: rgba(239, 68, 68, 0.05); overflow-x: auto; white-space: pre-wrap;
}
</style>
