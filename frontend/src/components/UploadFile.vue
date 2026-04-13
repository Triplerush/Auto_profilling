<script setup>
import { ref } from 'vue'
import { api } from '../api.js'

const emit = defineEmits(['uploaded'])

const selectedFile = ref(null)
const fileName = ref('')
const uploading = ref(false)
const error = ref('')
const dragover = ref(false)

const VALID_EXTENSIONS = ['.json', '.ipynb']

function handleFile(file) {
  const ext = file.name.substring(file.name.lastIndexOf('.'))
  if (!VALID_EXTENSIONS.includes(ext)) {
    error.value = 'Solo se aceptan archivos .json o .ipynb'
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

  const isJson = selectedFile.value.name.endsWith('.json')
  const url = api(isJson ? '/v1/analyses/upload' : '/v1/notebooks/upload')

  try {
    const res = await fetch(url, { method: 'POST', body: form })
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
  <div class="flex flex-col gap-4">
    <div
      :class="[
        'border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors',
        dragover
          ? 'border-sky-500 bg-sky-500/5'
          : 'border-slate-600 hover:border-sky-500/50'
      ]"
      @click="$refs.fileInput.click()"
      @dragover.prevent="dragover = true"
      @dragleave="dragover = false"
      @drop.prevent="onDrop"
    >
      <div class="text-4xl text-slate-500 mb-3">+</div>
      <p class="text-slate-400 text-sm">
        Arrastra un archivo <strong class="text-sky-400">.json</strong> o <strong class="text-sky-400">.ipynb</strong> aqui o haz clic para seleccionar
      </p>
      <p class="text-xs text-slate-500 mt-2">Data Contract JSON o Jupyter Notebook</p>
      <input ref="fileInput" type="file" accept=".json,.ipynb" @change="onFileChange" class="hidden" />
    </div>

    <div v-if="fileName" class="text-sm text-sky-400">{{ fileName }}</div>
    <div v-if="error" class="text-sm text-red-400">{{ error }}</div>

    <button
      :disabled="!selectedFile || uploading"
      @click="submit"
      class="self-end px-5 py-2 bg-sky-500 hover:bg-sky-600 text-white rounded-lg font-semibold text-sm transition-colors cursor-pointer disabled:bg-slate-600 disabled:text-slate-400 disabled:cursor-not-allowed"
    >
      {{ uploading ? 'Subiendo...' : 'Subir' }}
    </button>
  </div>
</template>
