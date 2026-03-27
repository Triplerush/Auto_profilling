<script setup>
import { ref } from 'vue'

const emit = defineEmits(['success', 'error'])

const selectedFile = ref(null)
const fileName = ref('')
const processing = ref(false)
const progress = ref(0)
const progressText = ref('')
const dragover = ref(false)

function handleFile(file) {
  if (!file.name.endsWith('.csv')) {
    emit('error', 'Solo se aceptan archivos .csv')
    return
  }
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

  processing.value = true
  progress.value = 30
  progressText.value = 'Subiendo archivo...'

  const form = new FormData()
  form.append('file', selectedFile.value)

  try {
    progress.value = 60
    progressText.value = 'Procesando profiling y limpieza...'

    const res = await fetch('/v1/profiling/process', { method: 'POST', body: form })

    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || 'Error al procesar')
    }

    progress.value = 100
    progressText.value = 'Completado'

    const data = await res.json()
    emit('success', data)
  } catch (e) {
    emit('error', e.message)
  } finally {
    setTimeout(() => {
      processing.value = false
      progress.value = 0
    }, 1500)
  }
}
</script>

<template>
  <div class="card">
    <div
      class="upload-zone"
      :class="{ dragover }"
      @click="$refs.fileInput.click()"
      @dragover.prevent="dragover = true"
      @dragleave="dragover = false"
      @drop.prevent="onDrop"
    >
      <div class="icon">&#128206;</div>
      <p>Arrastra tu archivo CSV aqui o haz clic para seleccionar</p>
      <input ref="fileInput" type="file" accept=".csv" @change="onFileChange" />
    </div>

    <div v-if="fileName" class="file-name">{{ fileName }}</div>

    <div v-if="processing" class="progress">
      <div class="progress-bar">
        <div class="fill" :style="{ width: progress + '%' }"></div>
      </div>
      <p>{{ progressText }}</p>
    </div>

    <div class="actions">
      <button class="btn" :disabled="!selectedFile || processing" @click="submit">
        Procesar archivo
      </button>
    </div>
  </div>
</template>

<style scoped>
.card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 1.5rem;
}
.upload-zone {
  border: 2px dashed #475569;
  border-radius: 12px;
  padding: 3rem 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.upload-zone:hover, .upload-zone.dragover {
  border-color: #38bdf8;
  background: rgba(56, 189, 248, 0.05);
}
.upload-zone p { color: #94a3b8; margin-top: 0.5rem; font-size: 0.9rem; }
.upload-zone .icon { font-size: 2.5rem; }
input[type="file"] { display: none; }
.file-name { margin-top: 0.75rem; color: #38bdf8; font-size: 0.85rem; }
.progress { margin-top: 1rem; }
.progress-bar { height: 6px; background: #334155; border-radius: 3px; overflow: hidden; }
.progress-bar .fill {
  height: 100%;
  background: #38bdf8;
  transition: width 0.3s;
  border-radius: 3px;
}
.progress p { font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem; }
.actions { margin-top: 1rem; text-align: center; }
.btn {
  display: inline-block;
  padding: 0.65rem 1.5rem;
  background: #38bdf8;
  color: #0f172a;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn:hover { background: #7dd3fc; }
.btn:disabled { background: #475569; color: #94a3b8; cursor: not-allowed; }
</style>
