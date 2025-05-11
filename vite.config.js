import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';

export default defineConfig({
  root: 'frontend',
  base: '/static/', // ✅ Ensures asset paths are prefixed correctly
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'frontend/src'),
    },
  },
  css: {
    postcss: path.resolve(__dirname, 'postcss.config.js'),
  },
  build: {
    outDir: path.resolve(__dirname, 'backend/static'), // ✅ Outputs build to FastAPI's static dir
    emptyOutDir: true,
  },
  server: {
    port: 3000,
    open: true,
  },
});
