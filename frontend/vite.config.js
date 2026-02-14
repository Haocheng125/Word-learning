import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 4000,
    proxy: {
      '/api': {
        target: 'http://backend:5000',
        changeOrigin: true
      },
      '/admin': {
        target: 'http://backend:5000',
        changeOrigin: true
      }
    }
  }
})
