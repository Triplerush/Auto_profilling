<script setup>
import { ref } from 'vue'

const props = defineProps({
  component: { type: Object, required: true },
})

const copied = ref(false)

async function copyCode() {
  await navigator.clipboard.writeText(props.component.code)
  copied.value = true
  setTimeout(() => { copied.value = false }, 1500)
}
</script>

<template>
  <div class="code-wrapper">
    <div class="code-header">
      <h4 v-if="component.title" class="code-title">{{ component.title }}</h4>
      <span class="code-lang">{{ component.language || 'python' }}</span>
      <button class="copy-btn" @click="copyCode">{{ copied ? 'Copiado!' : 'Copiar' }}</button>
    </div>
    <pre class="code-block"><code>{{ component.code }}</code></pre>
  </div>
</template>

<style scoped>
.code-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}
.code-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid var(--border);
}
.code-title { font-size: 0.85rem; color: var(--text-primary); flex: 1; }
.code-lang { font-size: 0.7rem; color: var(--text-secondary); background: var(--bg-dark); padding: 0.15rem 0.5rem; border-radius: 4px; }
.copy-btn {
  font-size: 0.72rem; padding: 0.2rem 0.6rem;
  background: transparent; border: 1px solid var(--border); border-radius: 4px;
  color: var(--text-secondary); cursor: pointer;
}
.copy-btn:hover { border-color: var(--accent); color: var(--accent); }
.code-block {
  background: var(--bg-code);
  padding: 1rem 1.25rem;
  margin: 0;
  overflow-x: auto;
  font-size: 0.8rem;
  line-height: 1.5;
  color: #c9d1d9;
}
</style>
