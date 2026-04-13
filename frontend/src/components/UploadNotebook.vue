<script setup>
import { ref } from 'vue'
import { api } from '../api.js'

const emit = defineEmits(['uploaded'])

const selectedFile = ref(null)
const fileName = ref('')
const uploading = ref(false)
const error = ref('')
const dragover = ref(false)

function handleFile(file) {
  if (!file.name.endsWith('.ipynb')) {
    error.value = 'Solo se aceptan archivos .ipynb'
    return
  }
  error.value = ''
  selectedFile.value = file
  fileName.value = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`
}

function onDrop(e) {
  dragover.value = false
  if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0])
}

function onFileChange(e) {
  if (e.target.files.length) handleFile(e.target.files[0])
}

async function submit() {
  if (!selectedFile.value) return
  uploading.value = true
  error.value = ''

  const form = new FormData()
  form.append('file', selectedFile.value)

  try {
    const res = await fetch(api('/v1/notebooks/upload'), { method: 'POST', body: form })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || 'Error al subir')
    }
    selectedFile.value = null
    fileName.value = ''
    emit('uploaded')
  } catch (e) {
    error.value = e.message
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <div class="upload-card">
    <div
      class="drop-zone"
      :class="{ dragover }"
      @click="$refs.fileInput.click()"
      @dragover.prevent="dragover = true"
      @dragleave="dragover = false"
      @drop.prevent="onDrop"
    >
      <p>Arrastra un archivo <strong>.ipynb</strong> aqui o haz clic para seleccionar</p>
      <input ref="fileInput" type="file" accept=".ipynb" @change="onFileChange" />
    </div>
    <div v-if="fileName" class="file-name">{{ fileName }}</div>
    <div v-if="error" class="error">{{ error }}</div>
    <button class="btn" :disabled="!selectedFile || uploading" @click="submit">
      {{ uploading ? 'Subiendo...' : 'Subir' }}
    </button>
  </div>
</template>

<style scoped>
.upload-card {
  background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 1.25rem;
  display: flex; flex-direction: column; gap: 0.75rem;
}
.drop-zone {
  border: 2px dashed #475569; border-radius: 10px; padding: 2rem 1rem;
  text-align: center; cursor: pointer; transition: border-color 0.2s, background 0.2s;
}
.drop-zone:hover, .drop-zone.dragover { border-color: var(--accent); background: rgba(56, 189, 248, 0.05); }
.drop-zone p { color: var(--text-secondary); font-size: 0.85rem; }
.drop-zone strong { color: var(--accent); }
input[type="file"] { display: none; }
.file-name { color: var(--accent); font-size: 0.82rem; }
.error { color: var(--danger); font-size: 0.82rem; }
.btn {
  align-self: flex-end; padding: 0.45rem 1.25rem; background: var(--accent); color: var(--bg-dark);
  border: none; border-radius: 6px; font-weight: 600; font-size: 0.82rem; cursor: pointer;
  transition: background 0.2s;
}
.btn:hover { background: var(--accent-hover); }
.btn:disabled { background: #475569; color: var(--text-secondary); cursor: not-allowed; }
</style>
