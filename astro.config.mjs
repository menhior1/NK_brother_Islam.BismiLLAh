import { defineConfig } from 'astro/config';

// Tailwind is processed by PostCSS (postcss.config.mjs).
// The @tailwindcss/vite plugin currently breaks Astro 6 / Rolldown production builds.
export default defineConfig({
  site: process.env.PUBLIC_SITE_URL || process.env.URL || 'https://example.com',
  output: 'static',
  build: { inlineStylesheets: 'auto' },
});
