# Nicolas Khobelia — Portfolio website

A small, editorial showcase for Nicolas Khobelia's concrete sinks and architectural objects, based on the first approved design concept.

## What's included

- Responsive Astro/TypeScript website: home, collection, individual product pages, studio, contact, thank-you, and 404.
- Tailwind CSS 4 and bespoke editorial styling.
- Two **actual supplied photos** as initial examples — no fictional products, portrait, address or contact details.
- Pages CMS (`.pages.yml`) for Nicolas to add / edit products, upload photographs and edit site copy.
- Build-time WebP resizing using Sharp for every original product photo and new CMS upload.
- Search engine metadata, sitemap, robots.txt, accessible gallery filters, mobile navigation and reduced-motion support.
- Netlify Forms inquiry form, with an optional product field carried to the inquiry page.
- A standalone `offline-preview.html` you can open in a desktop browser **without installing anything**. Preview navigation, collection filters and product pages work, but its inquiry form **does not send messages**.

## Requirements

- Node.js **24** (see `.nvmrc`).
- npm.
- A GitHub repository, Netlify account, and Pages CMS account for live publishing and editing.

## Local development

```bash
npm install
npm run dev
```

Open the local URL displayed by Astro (usually http://localhost:4321).

To test a production build:

```bash
npm run check:content
npm run build
npm run preview
```

`prebuild` automatically creates responsive `.webp` copies in `public/images/optimized`; these files are ignored by Git and regenerated for each deployment. Development mode uses the original photographs.

**Validation note:** the initial project was assembled in an environment without access to the npm registry, so packages could not be installed and the full Astro build could not be run here. The JSON content and Pages CMS YAML were validated, and the independent preview was generated. Run `npm install` / `npm run build` after downloading to confirm in your environment.

## Site organization

```text
.pages.yml                    Pages CMS editor schema
src/content.config.ts        Astro data validation for products
src/data/site.json           Editable studio/home copy
src/data/products/*.json     Editable product records
src/pages/                   Static pages and product routes
src/components/              Header, footer, picture, product card
src/styles/global.css        Layout, design tokens and breakpoints
public/images/products/      Original sample photographs
public/images/uploads/       Where Pages CMS stores new photographs
scripts/optimize-images.mjs  Resizes and compresses images on deployment
public/__forms.html          Netlify Forms registration fallback
netlify.toml                 Production build configuration
```

## Make this project live (in order)

1. **Check permission for both original photographs.** One of the provided images contains a visible **StoneTree Studio** watermark. It has deliberately not been altered or removed. Replace it before publication if Nicolas doesn't have permission to display it as-is.
2. Replace the sample copy and confirm the products' official names, materials and finishes. Dimensions were intentionally left empty because they weren't provided.
3. Create a **private** GitHub repository and upload the project files (ignore `node_modules`, `dist`, and `.astro`).
4. Connect this repository to Netlify (Add new project → Import an existing project). The included `netlify.toml` sets `npm run build`, `dist` and Node 24. The free-tier usage allowance is limited; monitor usage.
5. Deploy once. A temporary `*.netlify.app` URL will be assigned by Netlify.
6. In Netlify, open **Forms**, enable **Form detection**, and trigger a **new deployment**. Verify a genuine test submission from the public contact page and add email notification rules if required.
7. Open [app.pagescms.org](https://app.pagescms.org), sign in with your GitHub access, select the GitHub repository and default branch, and make sure its root `.pages.yml` configuration is recognized.
8. In Pages CMS, configure Nicolas as a collaborator if the service supports that for your account configuration, otherwise authorize a suitable GitHub-based workflow. Have Nicolas try creating a draft product with `published` set to false first.
9. Set a real production domain. Netlify environment variable **`PUBLIC_SITE_URL`** should be the final `https://...` URL (with no trailing slash), then rebuild. If not set, the build attempts the Netlify-provided `URL` environment variable. Set it explicitly when the domain is final to ensure canonical URLs and the sitemap are correct.
10. Edit `src/data/site.json` via Pages CMS with Nicolas's approved wording, real email (if public), and Instagram URL (if desired). The contact form works without a public email.

## How Nicolas will add a product

1. Go to Pages CMS, open **Products**, and select **New**.
2. Add title, shape, description, cover photograph, and optional gallery photos/specifications.
3. Leave **Publicly visible** off while preparing. Switch on when ready.
4. Save the record. Pages CMS commits the changes to GitHub. Netlify rebuilds and publishes the updated site.
5. Image filenames should be descriptive; use photographs Nicolas has permission to publish.

The source file name becomes the URL slug, so a product file such as `oval-concrete-basin.json` is reachable at `/works/oval-concrete-basin/`. If you rename a file, its URL changes; old URLs would require redirects.

## Safety and operational notes

- No accounts, shopping cart, payment processing, separate database, or external API are required for the public site.
- No personal contact details are invented. Inquiries go to the **Netlify dashboard** by default; set up notifications to receive them by email.
- Keep customer inquiries confidential. Set a retention policy and appropriate privacy text before production if required by local law.
- The independent offline preview is for design review only and is **not** the deployable, CMS-connected production output.
- Always inspect the output after CMS additions on desktop and mobile before announcing publication.
