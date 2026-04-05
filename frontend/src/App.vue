<script setup>
import { useRouter } from 'vue-router'
import { TooltipProvider } from 'reka-ui'

const router = useRouter()
</script>

<template>
  <TooltipProvider :delay-duration="300" :skip-delay-duration="100">
    <header class="sticky top-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-700/50">
      <div
        class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center gap-3 cursor-pointer select-none"
        @click="router.push('/')"
      >
        <h1 class="text-xl font-bold text-slate-100 hover:text-sky-400 transition-colors">Auto Profiling</h1>
        <p class="text-xs text-slate-500 tracking-wide uppercase">Plataforma Interactiva de Data Profiling</p>
      </div>
    </header>
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-12">
      <router-view />
    </main>
  </TooltipProvider>
</template>
