import type {APIRoute} from 'astro';
import {publishedProducts} from '../lib/products';
import {languages,route} from '../lib/i18n';
export const GET:APIRoute=async({site})=>{
 const base=site||new URL('https://example.com');
 const products=await publishedProducts();
 const paths=['/','/works/','/about/','/contact/',...products.map(p=>`/works/${p.id}/`)];
 const esc=(v:string)=>v.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
 const urls=paths.flatMap(path=>languages.map(lang=>{
   const loc=esc(new URL(route(lang,path),base).href);
   const alternates=languages.map(l=>`<xhtml:link rel="alternate" hreflang="${l}" href="${esc(new URL(route(l,path),base).href)}" />`).join('');
   const fallback=`<xhtml:link rel="alternate" hreflang="x-default" href="${esc(new URL(route('ka',path),base).href)}" />`;
   return `  <url><loc>${loc}</loc>${alternates}${fallback}</url>`;
 }));
 return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n${urls.join('\n')}\n</urlset>`,{headers:{'Content-Type':'application/xml; charset=utf-8'}});
};
