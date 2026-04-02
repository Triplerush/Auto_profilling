import { reactive } from 'vue'

export const store = reactive({
  notebooks: [],
  currentNotebook: null,
  loading: false,
  error: '',

  async fetchNotebooks() {
    this.loading = true
    this.error = ''
    try {
      const res = await fetch('/v1/notebooks')
      if (!res.ok) throw new Error('Error al cargar notebooks')
      const data = await res.json()
      this.notebooks = data.notebooks
    } catch (e) {
      this.error = e.message
    } finally {
      this.loading = false
    }
  },

  async fetchNotebook(id) {
    this.loading = true
    this.error = ''
    this.currentNotebook = null
    try {
      const res = await fetch(`/v1/notebooks/${id}`)
      if (!res.ok) throw new Error('Notebook no encontrado')
      this.currentNotebook = await res.json()
    } catch (e) {
      this.error = e.message
    } finally {
      this.loading = false
    }
  },
})
