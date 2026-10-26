import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

// CMS uploads land in public/images/uploads; build generates responsive WebP
// versions. Keep the originals; only optimized output is ignored in Git.
const root = path.resolve('public/images');
const output = path.join(root, 'optimized');
const widths = [480, 960, 1440];
async function process(dir) {
  for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
    if (entry.name === 'optimized') continue;
    const filename = path.join(dir, entry.name);
    if (entry.isDirectory()) { await process(filename); continue; }
    if (!/\.(jpe?g|png|webp|avif)$/i.test(entry.name)) continue;
    const rel = path.relative(root, filename).replace(/\\/g, '/');
    const stem = rel.replace(/\.(jpe?g|png|webp|avif)$/i, '');
    for (const width of widths) {
      const dest = path.join(output, `${stem}-${width}.webp`);
      await fs.mkdir(path.dirname(dest), { recursive: true });
      await sharp(filename).rotate().resize({ width, withoutEnlargement: false })
        .webp({ quality: 79, effort: 4 }).toFile(dest);
    }
    console.log(`Processed ${rel}`);
  }
}
await fs.rm(output, { recursive: true, force: true });
await process(root);
