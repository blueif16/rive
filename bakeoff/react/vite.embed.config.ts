import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/** Component-only bundle with React externalised — used for weight reporting. */
export default defineConfig({
  root: 'app',
  plugins: [react()],
  build: {
    outDir: '../dist-embed',
    emptyOutDir: true,
    target: 'es2020',
    cssCodeSplit: false,
    lib: {
      entry: 'embed.ts',
      formats: ['es'],
      fileName: () => 'figure.js',
    },
    rollupOptions: {
      external: ['react', 'react-dom', 'react/jsx-runtime'],
    },
  },
});
