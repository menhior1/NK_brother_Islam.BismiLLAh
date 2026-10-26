import type { APIRoute } from 'astro';
import { publishedProducts } from '../lib/products';
export const GET: APIRoute = async ({ site }) => {
  const base = site || new URL('https://example.com');
  const products = await publishedProducts();
  const paths = ['/', '/works/', '/about/', '/contact/', ...products.map(p => `/works/${p.id}/`)];
  const escapeXml = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${paths.map(path => `  <url><loc>${escapeXml(new URL(path, base).href)}</loc></url>`).join('\n')}\n</urlset>`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
