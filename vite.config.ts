import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'url'

import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  root: '.',
  base: '/static/',
  build: {
    manifest: 'manifest.json',
    outDir: './static',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: './frontend/main.ts',
        styles: './frontend/styles.css',
      },
    },
  },
  plugins: [
    vue({
      include: [/\.vue$/],
    }),
    tailwindcss(),
  ],
  server: {
    cors: true,
    // allowedHosts: [
    //   '.optimism.buri-frog.ts.net',
    //   '.optimism',
    //   '.entropy.buri-frog.ts.net',
    //   '.entropy',
    // ],
    port: 3333,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./frontend', import.meta.url)),
    },
    extensions: ['.html', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue', '.md'],
  },
})
