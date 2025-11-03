import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// Dynamically import visualizer only if available (dev environment)
const plugins = [react()];
try {
  const { visualizer } = await import('rollup-plugin-visualizer');
  plugins.push(
    visualizer({
      filename: './dist/stats.html',
      open: false,
      gzipSize: true,
      brotliSize: true,
    }) as any
  );
} catch (e) {
  // Visualizer not available (production build), skip it
}

export default defineConfig({
  plugins,
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    // Production build optimizations
    target: 'esnext',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.logs in production
        drop_debugger: true,
      },
    },
    rollupOptions: {
      output: {
        // Manual chunk splitting for better caching
        manualChunks: {
          // React core
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          // Data fetching
          'query-vendor': ['@tanstack/react-query', 'axios'],
          // Charts library (largest dependency)
          'charts-vendor': ['recharts'],
          // Icons
          'icons-vendor': ['lucide-react'],
        },
      },
    },
    // Increase chunk size warning limit since we have charts
    chunkSizeWarningLimit: 600,
    sourcemap: false, // Disable sourcemaps for smaller build
  },
})
