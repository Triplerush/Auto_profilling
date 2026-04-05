<script setup>
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

function cellColor(val) {
  if (val >= 0) {
    const intensity = Math.round(val * 60)
    return `hsl(210, 80%, ${90 - intensity}%)`
  } else {
    const intensity = Math.round(Math.abs(val) * 60)
    return `hsl(0, 70%, ${90 - intensity}%)`
  }
}

function tooltipText(ri, ci, val) {
  return `${props.component.columns[ri]} / ${props.component.columns[ci]}: ${val.toFixed(4)}`
}
</script>

<template>
  <div class="glass-card p-6 animate-fade-in">
    <h4 v-if="component.title" class="text-lg font-semibold text-slate-100 mb-4">{{ component.title }}</h4>

    <ScrollAreaRoot class="w-full" type="hover">
      <ScrollAreaViewport class="w-full">
        <table class="border-collapse text-xs font-mono">
          <thead>
            <tr>
              <th class="px-2 py-1.5 bg-slate-800/50"></th>
              <th
                v-for="(col, i) in component.columns"
                :key="i"
                class="px-2 py-1.5 text-center text-slate-400 font-medium bg-slate-800/50 whitespace-nowrap"
              >
                {{ col }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, ri) in component.matrix" :key="ri">
              <th class="px-2 py-1.5 text-right text-slate-400 font-medium bg-slate-800/50 whitespace-nowrap sticky left-0">
                {{ component.columns[ri] }}
              </th>
              <TooltipRoot v-for="(val, ci) in row" :key="ci">
                <TooltipTrigger as-child>
                  <td
                    :style="{ backgroundColor: cellColor(val) }"
                    class="px-2 py-1.5 text-center text-slate-900 font-semibold border border-slate-700/30 min-w-[3rem] cursor-default"
                  >
                    {{ val.toFixed(2) }}
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
