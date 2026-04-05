<script setup>
defineProps({
  variant: { type: String, default: 'card' }, // 'card', 'text', 'kpi', 'chart'
  count: { type: Number, default: 1 },
})
</script>

<template>
  <!-- Card skeleton (gallery) -->
  <template v-if="variant === 'card'">
    <div v-for="n in count" :key="n" class="glass-card p-6 animate-pulse">
      <div class="h-5 bg-slate-700/50 rounded w-3/4 mb-3"></div>
      <div class="h-3 bg-slate-700/30 rounded w-full mb-2"></div>
      <div class="h-3 bg-slate-700/30 rounded w-2/3 mb-4"></div>
      <div class="flex gap-2">
        <div class="h-5 bg-slate-700/30 rounded-full w-16"></div>
        <div class="h-5 bg-slate-700/30 rounded-full w-20"></div>
        <div class="h-5 bg-slate-700/30 rounded-full w-14"></div>
      </div>
    </div>
  </template>

  <!-- Header skeleton (analysis detail) -->
  <template v-else-if="variant === 'header'">
    <div class="glass-card p-8 animate-pulse">
      <div class="h-8 bg-slate-700/50 rounded w-2/3 mb-4"></div>
      <div class="h-4 bg-slate-700/30 rounded w-full mb-2"></div>
      <div class="h-4 bg-slate-700/30 rounded w-4/5 mb-5"></div>
      <div class="flex gap-3">
        <div class="h-4 bg-slate-700/30 rounded w-24"></div>
        <div class="h-4 bg-slate-700/30 rounded w-20"></div>
      </div>
    </div>
  </template>

  <!-- KPI skeleton -->
  <template v-else-if="variant === 'kpi'">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <div v-for="n in count" :key="n" class="glass-card p-5 border-l-4 border-l-slate-700/50 animate-pulse">
        <div class="h-3 bg-slate-700/30 rounded w-20 mb-2"></div>
        <div class="h-7 bg-slate-700/50 rounded w-16"></div>
      </div>
    </div>
  </template>

  <!-- Chart skeleton -->
  <template v-else-if="variant === 'chart'">
    <div v-for="n in count" :key="n" class="glass-card p-6 animate-pulse">
      <div class="h-5 bg-slate-700/50 rounded w-1/3 mb-4"></div>
      <div class="h-[300px] bg-slate-700/20 rounded-lg flex items-end justify-around px-8 pb-4 gap-3">
        <div class="bg-slate-700/30 rounded-t w-full" style="height: 60%"></div>
        <div class="bg-slate-700/30 rounded-t w-full" style="height: 80%"></div>
        <div class="bg-slate-700/30 rounded-t w-full" style="height: 45%"></div>
        <div class="bg-slate-700/30 rounded-t w-full" style="height: 70%"></div>
        <div class="bg-slate-700/30 rounded-t w-full" style="height: 55%"></div>
        <div class="bg-slate-700/30 rounded-t w-full" style="height: 90%"></div>
      </div>
    </div>
  </template>

  <!-- Text line skeleton -->
  <template v-else-if="variant === 'text'">
    <div class="animate-pulse space-y-2">
      <div v-for="n in count" :key="n" class="h-3 bg-slate-700/30 rounded" :style="{ width: (70 + Math.random() * 30) + '%' }"></div>
    </div>
  </template>
</template>
