import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { viteSingleFile } from 'vite-plugin-singlefile';

/**
 * Builds the demo page to a single `index.html` at the package root so it opens
 * from the filesystem with no server (module scripts loaded over file:// are
 * blocked by CORS, so everything has to be inlined).
 */
export default defineConfig({
  root: 'app',
  plugins: [react(), viteSingleFile()],
  build: {
    outDir: '..',
    emptyOutDir: false,
    target: 'es2020',
    cssCodeSplit: false,
    assetsInlineLimit: 100000000,
    reportCompressedSize: true,
  },
});
