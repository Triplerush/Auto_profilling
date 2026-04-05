<script setup>
import { ref } from 'vue'
import {
  TooltipRoot,
  TooltipTrigger,
  TooltipPortal,
  TooltipContent,
  TooltipArrow,
} from 'reka-ui'

const props = defineProps({
  component: { type: Object, required: true },
})

const copied = ref(false)

async function copyCode() {
  await navigator.clipboard.writeText(props.component.code)
  copied.value = true
  setTimeout(() => { copied.value = false }, 1500)
}
</script>

<template>
  <div class="glass-card overflow-hidden animate-fade-in">
    <div class="flex items-center gap-3 px-4 py-2.5 bg-slate-700/30 border-b border-slate-700/50">
      <h4 v-if="component.title" class="text-sm font-medium text-slate-200 flex-1">{{ component.title }}</h4>
      <span class="text-xs font-mono px-2 py-0.5 rounded bg-slate-900/50 text-sky-400">
        {{ component.language || 'python' }}
      </span>
      <TooltipRoot>
        <TooltipTrigger as-child>
          <button
            @click="copyCode"
            class="text-xs px-2.5 py-1 rounded border border-slate-600 text-slate-400 hover:border-sky-500/50 hover:text-sky-400 transition-colors cursor-pointer"
          >
            {{ copied ? 'Copiado!' : 'Copiar' }}
          </button>
        </TooltipTrigger>
        <TooltipPortal>
          <TooltipContent class="tooltip-content" :side-offset="5">
            {{ copied ? 'Copiado al portapapeles' : 'Copiar codigo' }}
            <TooltipArrow class="tooltip-arrow" />
          </TooltipContent>
        </TooltipPortal>
      </TooltipRoot>
    </div>
    <pre class="bg-slate-950 p-4 overflow-x-auto text-sm font-mono leading-relaxed text-slate-300 m-0"><code>{{ component.code }}</code></pre>
  </div>
</template>
