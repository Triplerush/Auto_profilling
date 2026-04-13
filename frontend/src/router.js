import { createRouter, createWebHistory } from 'vue-router'
import GalleryView from './views/GalleryView.vue'
import NotebookView from './views/NotebookView.vue'
import AnalysisView from './views/AnalysisView.vue'
import CompareView from './views/CompareView.vue'

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'gallery', component: GalleryView },
    { path: '/analysis/:id', name: 'analysis', component: AnalysisView, props: true },
    { path: '/notebook/:id', name: 'notebook', component: NotebookView, props: true },
    { path: '/compare', name: 'compare', component: CompareView },
  ],
})
