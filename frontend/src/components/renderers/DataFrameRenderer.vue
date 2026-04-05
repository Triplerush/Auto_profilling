<script setup>
import { ref, computed } from 'vue'
import {
  ScrollAreaRoot,
  ScrollAreaViewport,
  ScrollAreaScrollbar,
  ScrollAreaThumb,
} from 'reka-ui'
import {
  PaginationRoot,
  PaginationList,
  PaginationListItem,
  PaginationPrev,
  PaginationNext,
  PaginationEllipsis,
} from 'reka-ui'

const props = defineProps({
  component: { type: Object, required: true },
})

const searchQuery = ref('')
const sortCol = ref(null)
const sortDir = ref('asc')
const currentPage = ref(1)
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
  const start = (currentPage.value - 1) * pageSize
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
  currentPage.value = 1
}

function onSearch() {
  currentPage.value = 1
}
</script>

<template>
  <div class="glass-card overflow-hidden animate-fade-in">
    <h4 v-if="component.title" class="text-lg font-semibold text-slate-100 px-5 pt-5 pb-2">{{ component.title }}</h4>

    <input
      v-if="component.config?.searchable !== false"
      v-model="searchQuery"
      @input="onSearch"
      class="w-full bg-slate-900/50 border-b border-slate-700/50 px-5 py-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500/50 transition-colors"
      placeholder="Buscar..."
    />

    <ScrollAreaRoot class="w-full" type="hover">
      <ScrollAreaViewport class="w-full">
        <table class="w-full text-sm">
          <thead>
            <tr>
              <th
                v-for="(col, idx) in columns"
                :key="idx"
                @click="toggleSort(idx)"
                :class="[
                  'bg-slate-700/30 text-slate-300 font-medium text-left px-4 py-3 whitespace-nowrap sticky top-0',
                  component.config?.sortable !== false ? 'cursor-pointer hover:text-sky-400 transition-colors select-none' : ''
                ]"
              >
                {{ col }}
                <span v-if="sortCol === idx" class="text-sky-400 ml-1 text-xs">{{ sortDir === 'asc' ? '▲' : '▼' }}</span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(row, ri) in paginatedRows"
              :key="ri"
              class="border-t border-slate-700/30 hover:bg-slate-700/20 transition-colors even:bg-slate-800/30"
            >
              <td v-for="(cell, ci) in row" :key="ci" class="px-4 py-2.5 text-slate-300">
                {{ cell ?? '' }}
              </td>
            </tr>
            <tr v-if="paginatedRows.length === 0">
              <td :colspan="columns.length" class="text-center text-slate-500 py-8">Sin resultados</td>
            </tr>
          </tbody>
        </table>
      </ScrollAreaViewport>
      <ScrollAreaScrollbar orientation="horizontal" class="scrollbar-track">
        <ScrollAreaThumb class="scrollbar-thumb" />
      </ScrollAreaScrollbar>
    </ScrollAreaRoot>

    <div v-if="totalPages > 1" class="flex items-center justify-between px-5 py-3 border-t border-slate-700/50">
      <span class="text-xs text-slate-500">{{ filteredRows.length }} filas</span>
      <PaginationRoot
        :total="filteredRows.length"
        :items-per-page="pageSize"
        :page="currentPage"
        :sibling-count="1"
        show-edges
        @update:page="currentPage = $event"
      >
        <PaginationList v-slot="{ items }" class="flex items-center gap-1">
          <PaginationPrev class="px-2.5 py-1.5 rounded-md text-sm text-slate-400 hover:text-slate-200 hover:bg-slate-700/50 transition-colors disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer">
            &laquo;
          </PaginationPrev>

          <template v-for="(item, index) in items" :key="index">
            <PaginationListItem
              v-if="item.type === 'page'"
              :value="item.value"
              :class="[
                'px-3 py-1.5 rounded-md text-sm transition-colors cursor-pointer',
                item.value === currentPage
                  ? 'bg-sky-500 text-white font-medium'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
              ]"
            >
              {{ item.value }}
            </PaginationListItem>
            <PaginationEllipsis v-else :index="index" class="px-2 text-slate-500">
              ...
            </PaginationEllipsis>
          </template>

          <PaginationNext class="px-2.5 py-1.5 rounded-md text-sm text-slate-400 hover:text-slate-200 hover:bg-slate-700/50 transition-colors disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer">
            &raquo;
          </PaginationNext>
        </PaginationList>
      </PaginationRoot>
    </div>
  </div>
</template>
