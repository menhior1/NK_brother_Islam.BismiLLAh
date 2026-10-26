import fs from 'node:fs';
import path from 'node:path';
const productPath = './src/data/products';
const products = fs.readdirSync(productPath).filter(f=>f.endsWith('.json'));
let problems = [];
for (const f of products) {
  const d = JSON.parse(fs.readFileSync(path.join(productPath,f),'utf-8'));
  for (const field of ['title','category','coverImage','published']) if (d[field]===undefined) problems.push(`${f} missing ${field}`);
  for (const img of [d.coverImage,...(d.gallery||[])]) if (img && img.startsWith('/images/') && !fs.existsSync(`public${img}`)) problems.push(`${f} missing photo ${img}`);
}
const site = JSON.parse(fs.readFileSync('./src/data/site.json','utf-8'));
for (const img of [site.heroImage, site.aboutImage]) if (img && !fs.existsSync(`public${img}`)) problems.push(`Site missing photo ${img}`);
console.log(`${products.length} products checked. ${problems.length ? problems.join('\n') : 'All referenced images exist.'}`);
if (problems.length) process.exit(1);
