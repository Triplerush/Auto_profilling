<script setup>
import { computed } from 'vue'
import {
  TooltipRoot,
  TooltipTrigger,
  TooltipPortal,
  TooltipContent,
  TooltipArrow,
  ScrollAreaRoot,
  ScrollAreaViewport,
  ScrollAreaScrollbar,
  ScrollAreaThumb,
} from 'reka-ui'

const props = defineProps({
  component: { type: Object, required: true },
})

const rowTotals = computed(() =>
  props.component.matrix.map(row => row.reduce((a, b) => a + b, 0))
)

function cellBg(ri, ci, val) {
  const total = rowTotals.value[ri] || 1
  const pct = val / total
  if (ri === ci) {
    return `rgba(34, 197, 94, ${0.15 + pct * 0.5})`
  }
  return val > 0 ? `rgba(239, 68, 68, ${0.1 + pct * 0.4})` : 'transparent'
}

function tooltipText(ri, ci, val) {
  const total = rowTotals.value[ri] || 1
  const pct = ((val / total) * 100).toFixed(1)
  return `Real: ${props.component.labels[ri]}, Pred: ${props.component.labels[ci]} — ${val} (${pct}%)`
}
</script>

<template>
  <div class="glass-card p-6 animate-fade-in">
    <h4 v-if="component.title" class="text-lg font-semibold text-slate-100 mb-4">{{ component.title }}</h4>

    <ScrollAreaRoot class="w-full" type="hover">
      <ScrollAreaViewport class="w-full">
        <table class="border-collapse text-sm">
          <thead>
            <tr>
              <th class="px-3 py-2 text-xs text-slate-500 italic bg-slate-800/50">Real \ Pred</th>
              <th
                v-for="(label, i) in component.labels"
                :key="i"
                class="px-3 py-2 text-center text-slate-300 font-medium bg-slate-800/50 whitespace-nowrap"
              >
                {{ label }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, ri) in component.matrix" :key="ri">
              <th class="px-3 py-2 text-right text-slate-300 font-medium bg-slate-800/50 whitespace-nowrap sticky left-0">
                {{ component.labels[ri] }}
              </th>
              <TooltipRoot v-for="(val, ci) in row" :key="ci">
                <TooltipTrigger as-child>
                  <td
                    :style="{ backgroundColor: cellBg(ri, ci, val) }"
                    :class="[
                      'px-3 py-2.5 text-center border border-slate-700/30 min-w-[4.5rem] cursor-default',
                      ri === ci ? 'ring-2 ring-sky-500/40 ring-inset' : ''
                    ]"
                  >
                    <span class="block font-bold text-slate-100">{{ val }}</span>
                    <span class="block text-xs text-slate-400">{{ ((val / (rowTotals[ri] || 1)) * 100).toFixed(1) }}%</span>
                  </td>
                </TooltipTrigger>
                <TooltipPortal>
                  <TooltipContent class="tooltip-content" :side-offset="5" side="top">
                    {{ tooltipText(ri, ci, val) }}
                    <TooltipArrow class="tooltip-arrow" />
                  </TooltipContent>
                </TooltipPortal>
              </TooltipRoot>
            </tr>
          </tbody>
        </table>
      </ScrollAreaViewport>
      <ScrollAreaScrollbar orientation="horizontal" class="scrollbar-track">
        <ScrollAreaThumb class="scrollbar-thumb" />
      </ScrollAreaScrollbar>
    </ScrollAreaRoot>
  </div>
</template>
