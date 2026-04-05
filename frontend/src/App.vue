<script setup>
import { useRouter } from 'vue-router'
import { TooltipProvider } from 'reka-ui'
import { useTheme } from './composables/useTheme.js'

const router = useRouter()
const { theme, toggleTheme } = useTheme()
</script>

<template>
  <TooltipProvider :delay-duration="300" :skip-delay-duration="100">
    <header class="sticky top-0 z-50 backdrop-blur-md border-b transition-colors duration-300"
      :class="theme === 'dark' ? 'bg-slate-900/80 border-slate-700/50' : 'bg-white/90 border-slate-300/50 shadow-sm'"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center gap-3">
        <div class="flex items-center gap-3 cursor-pointer select-none flex-1" @click="router.push('/')">
          <h1 class="text-xl font-bold hover:text-sky-400 transition-colors"
            :class="theme === 'dark' ? 'text-slate-100' : 'text-slate-900'"
          >Auto Profiling</h1>
          <p class="text-xs tracking-wide uppercase hidden sm:block"
            :class="theme === 'dark' ? 'text-slate-500' : 'text-slate-400'"
          >Plataforma Interactiva de Data Profiling</p>
        </div>
        <button
          @click="toggleTheme"
          class="p-2 rounded-lg transition-colors cursor-pointer"
          :class="theme === 'dark'
            ? 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            : 'text-slate-500 hover:text-slate-700 hover:bg-slate-100'"
          :aria-label="theme === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'"
        >
          <!-- Sun icon (shown in dark mode) -->
          <svg v-if="theme === 'dark'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <!-- Moon icon (shown in light mode) -->
          <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
        </button>
      </div>
    </header>
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-12">
      <router-view v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </router-view>
    </main>
  </TooltipProvider>
</template>
