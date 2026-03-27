<script setup>
import UploadCard from './components/UploadCard.vue'
import ResultsCard from './components/ResultsCard.vue'
import { ref } from 'vue'

const results = ref(null)
const error = ref('')

function onResults(data) {
  error.value = ''
  results.value = data
}

function onError(msg) {
  results.value = null
  error.value = msg
}
</script>

<template>
  <header>
    <h1>Auto Profiling</h1>
    <p>Data Profiling y Limpieza Automatizada de CSV</p>
  </header>
  <main>
    <UploadCard @success="onResults" @error="onError" />
    <div v-if="error" class="error-box">{{ error }}</div>
    <ResultsCard v-if="results" :data="results" />
  </main>
</template>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #0f172a;
  color: #e2e8f0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}
header {
  width: 100%;
  padding: 1.5rem 2rem;
  background: #1e293b;
  border-bottom: 1px solid #334155;
  text-align: center;
}
header h1 { font-size: 1.5rem; color: #38bdf8; }
header p { font-size: 0.85rem; color: #94a3b8; margin-top: 0.25rem; }
main {
  width: 100%;
  max-width: 800px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.error-box {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid #ef4444;
  border-radius: 8px;
  padding: 1rem;
  color: #fca5a5;
  font-size: 0.85rem;
}
</style>
