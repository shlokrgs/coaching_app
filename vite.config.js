import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';

export default defineConfig({
  root: 'frontend', // ✅ No './' here
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'frontend/src'),
    },
  },
  css: {
    postcss: path.resolve(__dirname, 'postcss.config.js'), // ✅ Also no './' needed
  },
  build: {
    outDir: path.resolve(__dirname, 'backend/static'), // ✅ Absolute to avoid render issues
    emptyOutDir: true,
  },
  server: {
    port: 3000,
    open: true,
  },
});
