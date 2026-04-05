<script setup>
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  component: { type: Object, required: true },
})

const html = computed(() => marked.parse(props.component.content || ''))
</script>

<template>
  <div class="glass-card p-5 animate-fade-in">
    <div class="prose-dark text-sm leading-relaxed" v-html="html"></div>
  </div>
</template>
