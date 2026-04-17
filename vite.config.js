import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/ai-app-lab/',
  build: {
    outDir: 'dist',
    sourcemap: false
  }
})