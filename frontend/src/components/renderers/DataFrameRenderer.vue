<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  component: { type: Object, required: true },
})

const searchQuery = ref('')
const sortCol = ref(null)
const sortDir = ref('asc')
const currentPage = ref(0)
const pageSize = props.component.config?.page_size || 10

const columns = computed(() => props.component.data.columns)

const filteredRows = computed(() => {
  let rows = props.component.data.rows
  if (props.component.config?.searchable !== false && searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    rows = rows.filter(row => row.some(cell => String(cell ?? '').toLowerCase().includes(q)))
  }
  if (sortCol.value !== null) {
    const idx = sortCol.value
    rows = [...rows].sort((a, b) => {
      const va = a[idx], vb = b[idx]
      if (va == null) return 1
      if (vb == null) return -1
      if (typeof va === 'number' && typeof vb === 'number') return sortDir.value === 'asc' ? va - vb : vb - va
      return sortDir.value === 'asc'
        ? String(va).localeCompare(String(vb))
        : String(vb).localeCompare(String(va))
    })
  }
  return rows
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredRows.value.length / pageSize)))
const paginatedRows = computed(() => {
  const start = currentPage.value * pageSize
  return filteredRows.value.slice(start, start + pageSize)
})

function toggleSort(idx) {
  if (props.component.config?.sortable === false) return
  if (sortCol.value === idx) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortCol.value = idx
    sortDir.value = 'asc'
  }
  currentPage.value = 0
}

function onSearch() {
  currentPage.value = 0
}
</script>

<template>
  <div class="df-wrapper">
    <h4 v-if="component.title" class="df-title">{{ component.title }}</h4>

    <input
      v-if="component.config?.searchable !== false"
      v-model="searchQuery"
      @input="onSearch"
      class="df-search"
      placeholder="Buscar..."
    />

    <div class="df-table-wrap">
      <table>
        <thead>
          <tr>
            <th
              v-for="(col, idx) in columns"
              :key="idx"
              @click="toggleSort(idx)"
              :class="{ sortable: component.config?.sortable !== false }"
            >
              {{ col }}
              <span v-if="sortCol === idx" class="sort-arrow">{{ sortDir === 'asc' ? '▲' : '▼' }}</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, ri) in paginatedRows" :key="ri">
            <td v-for="(cell, ci) in row" :key="ci">{{ cell ?? '' }}</td>
          </tr>
          <tr v-if="paginatedRows.length === 0">
            <td :colspan="columns.length" class="empty">Sin resultados</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="df-pagination" v-if="totalPages > 1">
      <button :disabled="currentPage === 0" @click="currentPage--">&laquo; Anterior</button>
      <span>{{ currentPage + 1 }} / {{ totalPages }}</span>
      <button :disabled="currentPage >= totalPages - 1" @click="currentPage++">Siguiente &raquo;</button>
    </div>
  </div>
</template>

<style scoped>
.df-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
}
.df-title { font-size: 0.9rem; color: var(--text-primary); margin-bottom: 0.75rem; }
.df-search {
  width: 100%; padding: 0.45rem 0.75rem; margin-bottom: 0.75rem;
  background: var(--bg-dark); border: 1px solid var(--border); border-radius: 6px;
  color: var(--text-primary); font-size: 0.8rem; outline: none;
}
.df-search:focus { border-color: var(--accent); }
.df-table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
th, td { padding: 0.4rem 0.6rem; border: 1px solid var(--border); text-align: left; }
th {
  background: var(--bg-dark); color: var(--text-secondary); font-weight: 500;
  position: sticky; top: 0; white-space: nowrap;
}
th.sortable { cursor: pointer; user-select: none; }
th.sortable:hover { color: var(--accent); }
.sort-arrow { font-size: 0.65rem; margin-left: 0.3rem; }
td { color: var(--text-primary); }
tr:nth-child(even) { background: rgba(15, 23, 42, 0.5); }
.empty { text-align: center; color: var(--text-secondary); padding: 1.5rem; }
.df-pagination {
  display: flex; justify-content: center; align-items: center; gap: 1rem;
  margin-top: 0.75rem; font-size: 0.8rem; color: var(--text-secondary);
}
.df-pagination button {
  padding: 0.3rem 0.75rem; background: var(--bg-dark); border: 1px solid var(--border);
  border-radius: 4px; color: var(--text-secondary); cursor: pointer; font-size: 0.75rem;
}
.df-pagination button:hover:not(:disabled) { border-color: var(--accent); color: var(--accent); }
.df-pagination button:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
