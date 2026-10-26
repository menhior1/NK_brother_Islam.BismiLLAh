import fs from 'node:fs';
import path from 'node:path';
const langs=['ka','ru','en'];
const dir='./src/data/products';
const files=fs.readdirSync(dir).filter(f=>f.endsWith('.json'));
const problems=[];
const isString=(val)=>typeof val==='string'&&val.trim().length>0;
const validateLocalized=(value,context,required)=>{
 if(!value||typeof value!=='object'){problems.push(`${context} must have translated values`);return;}
 for(const l of langs){
  if(typeof value[l]!=='string')problems.push(`${context}.${l} must be text`);
  else if(required&&!isString(value[l]))problems.push(`${context}.${l} is required for a published product`);
 }
};
for(const file of files){
 const d=JSON.parse(fs.readFileSync(path.join(dir,file),'utf8'));
 for(const field of ['title','description','material','finish','alt','dimensions'])validateLocalized(d[field],`${file}.${field}`,d.published&&['title','description'].includes(field));
 for(const field of ['category','coverImage','published'])if(d[field]===undefined)problems.push(`${file} missing ${field}`);
 for(const img of [d.coverImage,...(d.gallery||[])])if(img?.startsWith('/images/')&&!fs.existsSync(`public${img}`))problems.push(`${file} missing photo ${img}`);
}
const site=JSON.parse(fs.readFileSync('./src/data/site.json','utf8'));
for(const key of ['strapline','heroTitle','heroSubtitle','introEyebrow','introTitle','introDescription','worksEyebrow','worksTitle','aboutEyebrow','aboutTitle','aboutDescription','contactTitle','contactDescription'])validateLocalized(site[key],`site.${key}`,true);
for(const img of [site.heroImage,site.aboutImage])if(img&&!fs.existsSync(`public${img}`))problems.push(`Site missing photo ${img}`);
console.log(`${files.length} products and 3 languages checked. ${problems.length?problems.join('\n'):'All translations and referenced images are valid.'}`);
if(problems.length)process.exit(1);
