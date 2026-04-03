<script setup>
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  component: { type: Object, required: true },
})

const html = computed(() => marked.parse(props.component.content || ''))
</script>

<template>
  <div class="text-wrapper">
    <div class="md-content" v-html="html"></div>
  </div>
</template>

<style scoped>
.text-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
}
.md-content { line-height: 1.6; font-size: 0.9rem; }
.md-content :deep(h1) { font-size: 1.4rem; color: var(--accent); margin: 0.75rem 0 0.5rem; }
.md-content :deep(h2) { font-size: 1.15rem; color: var(--accent); margin: 0.75rem 0 0.4rem; }
.md-content :deep(h3) { font-size: 1rem; color: var(--text-primary); margin: 0.6rem 0 0.3rem; }
.md-content :deep(p) { margin: 0.4rem 0; color: var(--text-secondary); }
.md-content :deep(strong) { color: var(--text-primary); }
.md-content :deep(code) { background: var(--bg-code); padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.82rem; }
.md-content :deep(ul), .md-content :deep(ol) { padding-left: 1.5rem; color: var(--text-secondary); }
.md-content :deep(li) { margin: 0.2rem 0; }
.md-content :deep(blockquote) { border-left: 3px solid var(--accent); padding-left: 1rem; color: var(--text-secondary); margin: 0.5rem 0; }
</style>
