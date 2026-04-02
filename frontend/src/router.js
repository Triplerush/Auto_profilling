import { createRouter, createWebHistory } from 'vue-router'
import GalleryView from './views/GalleryView.vue'
import NotebookView from './views/NotebookView.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'gallery', component: GalleryView },
    { path: '/notebook/:id', name: 'notebook', component: NotebookView, props: true },
  ],
})
