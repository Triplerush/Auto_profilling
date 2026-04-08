import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/v1/models': 'http://localhost:8001',
      '/v1': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
    },
  },
})
