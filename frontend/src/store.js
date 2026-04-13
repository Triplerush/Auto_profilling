import { reactive } from 'vue'
import { api } from './api.js'

export const store = reactive({
  // Analyses (Data Contract)
  analyses: [],
  currentAnalysis: null,

  // Legacy notebooks
  notebooks: [],
  currentNotebook: null,

  loading: false,
  error: '',

  async fetchAnalyses() {
    this.loading = true
    this.error = ''
    try {
      const res = await fetch(api('/v1/analyses'))
      if (!res.ok) throw new Error('Error al cargar analisis')
      const data = await res.json()
      this.analyses = data.analyses
    } catch (e) {
      this.error = e.message
    } finally {
      this.loading = false
    }
  },

  async fetchAnalysis(id) {
    this.loading = true
    this.error = ''
    this.currentAnalysis = null
    try {
      const res = await fetch(api(`/v1/analyses/${id}`))
      if (!res.ok) throw new Error('Analisis no encontrado')
      this.currentAnalysis = await res.json()
    } catch (e) {
      this.error = e.message
    } finally {
      this.loading = false
    }
  },

  async fetchNotebooks() {
    try {
      const res = await fetch(api('/v1/notebooks'))
      if (!res.ok) return
      const data = await res.json()
      this.notebooks = data.notebooks
    } catch {
      // Legacy endpoint may not be critical
    }
  },

  async fetchNotebook(id) {
    this.loading = true
    this.error = ''
    this.currentNotebook = null
    try {
      const res = await fetch(api(`/v1/notebooks/${id}`))
      if (!res.ok) throw new Error('Notebook no encontrado')
      this.currentNotebook = await res.json()
    } catch (e) {
      this.error = e.message
    } finally {
      this.loading = false
    }
  },
})
