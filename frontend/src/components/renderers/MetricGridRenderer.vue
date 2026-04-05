<script setup>
import {
  TooltipRoot,
  TooltipTrigger,
  TooltipPortal,
  TooltipContent,
  TooltipArrow,
} from 'reka-ui'

defineProps({
  metrics: { type: Array, required: true },
})

function severityBorder(severity) {
  switch (severity) {
    case 'critical': return 'border-l-red-500'
    case 'warning': return 'border-l-amber-500'
    case 'info': return 'border-l-sky-500'
    default: return 'border-l-emerald-500'
  }
}
</script>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 animate-slide-up">
    <TooltipRoot v-for="(m, i) in metrics" :key="i">
      <TooltipTrigger as-child>
        <div
          :class="[
            'glass-card p-5 border-l-4 hover:border-sky-500/30 transition-all duration-200 hover:-translate-y-0.5 cursor-default',
            severityBorder(m.severity)
          ]"
        >
          <div class="text-sm text-muted font-medium mb-1">{{ m.label }}</div>
          <div class="text-2xl font-bold text-heading">{{ m.value }}</div>
          <div v-if="m.description" class="text-xs text-slate-500 mt-2 line-clamp-2">{{ m.description }}</div>
        </div>
      </TooltipTrigger>
      <TooltipPortal v-if="m.description">
        <TooltipContent class="tooltip-content max-w-xs" :side-offset="5">
          {{ m.description }}
          <TooltipArrow class="tooltip-arrow" />
        </TooltipContent>
      </TooltipPortal>
    </TooltipRoot>
  </div>
</template>
