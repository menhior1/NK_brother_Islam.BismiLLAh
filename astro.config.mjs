import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: process.env.PUBLIC_SITE_URL || process.env.URL || 'https://example.com',
  output: 'static',
  vite: { plugins: [tailwindcss()] },
  build: { inlineStylesheets: 'auto' },
});
