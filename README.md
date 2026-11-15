# Nicolas Khobelia — multilingual portfolio

Astro + Tailwind CSS 4 (PostCSS) + Pages CMS + Netlify. Georgian is the default, Russian and English have distinct static URLs.

## Site languages / URLs

| Georgian (default) | Russian | English |
|---|---|---|
| `/` | `/ru/` | `/en/` |
| `/works/` | `/ru/works/` | `/en/works/` |
| `/works/round-concrete-basin/` | `/ru/works/round-concrete-basin/` | `/en/works/round-concrete-basin/` |
| `/about/` | `/ru/about/` | `/en/about/` |
| `/contact/` | `/ru/contact/` | `/en/contact/` |

Language switching preserves the active page or product route. Static HTML uses appropriate `lang`, `canonical`, `hreflang`, OG locale, localized meta descriptions, and multilingual sitemap entries.

## Editing content

Pages CMS (https://app.pagescms.org) reads `.pages.yml`. Each product includes Georgian, Russian and English values for title, description, material, finish, dimensions, and image description. The site file includes three-language homepage, studio, and contact copy. Product gallery images remain shared across languages. Check all translations before switching **Published** on. The content validation script rejects missing published product titles and descriptions in any language.

New products require a stable Latin `slug`, e.g. `oval-concrete-basin`. The product's filename defines its public URL.

## Development

Requires Node.js 24.

```bash
npm ci
npm run check:content
npm run dev
npm run build
npm run preview
```

Netlify uses `npm run build`, the `dist` output, and Node 24. Tailwind uses PostCSS rather than `@tailwindcss/vite` to avoid Astro 6 / Rolldown compatibility errors.

## Contact and publishing

Netlify Forms receives a shared `inquiry` form with a language field; success pages use the selected locale. Verify that Netlify form detection is enabled, redeploy and test real submissions separately in all three languages before public launch. Confirm rights to both source photos (one has a visible third-party watermark), replace placeholder copy as needed, and confirm public email / Instagram.

### Caveat

The previously generated `offline-preview.html` (if present) is an older English-only design demonstration; it does not reflect this multilingual implementation. Review the actual Netlify preview for all three locales.


## Contact and search visibility

- Contact form replaced with editable phone numbers +995551937757 and +79697936686; all three languages display click-to-call links.
- Each language has search-specific homepage title and description. Product pages emit factual Product structured data; homepages identify Nicolas via Person structured data. Canonical URLs, alternate language tags, sitemap and robots.txt are retained.
- Enter the canonical production address in Netlify's PUBLIC_SITE_URL environment variable and redeploy. For the current Netlify URL, use https://nk-portf.netlify.app unless a custom domain is chosen.
- Verify the public site in Google Search Console and submit /sitemap.xml. Indexing is at Google's discretion, never guaranteed.
