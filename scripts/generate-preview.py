"""Self-contained OFFLINE design preview; not the deployable Astro build.
Run from repository root: python scripts/generate-preview.py
"""
import base64, json, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
site = json.loads((ROOT/'src/data/site.json').read_text())
products = []
for f in (ROOT/'src/data/products').glob('*.json'):
    p = json.loads(f.read_text()); p['slug'] = f.stem
    if p['published']: products.append(p)
products.sort(key=lambda x:x.get('order',99))
esc = lambda s: html.escape(str(s), quote=True)
def img(path):
    p=ROOT/'public'/path.lstrip('/')
    suffix=p.suffix.lower()
    typ='image/jpeg' if suffix in ('.jpg','.jpeg') else 'image/png'
    return 'data:'+typ+';base64,'+base64.b64encode(p.read_bytes()).decode()
images = {p['coverImage']:img(p['coverImage']) for p in products}
images[site['heroImage']] = img(site['heroImage'])
images[site['aboutImage']] = img(site['aboutImage'])
css=(ROOT/'src/styles/global.css').read_text().replace('@import "tailwindcss";', '')
additional='''
[data-page] { display: none; }
[data-page].active { display: block; }
body:not(.is-home) .site-header { background: var(--paper); color: var(--ink); }
body.is-home .site-header { position: absolute; background: transparent; color: #fff; }
body.is-home .site-header.menu-open { color: var(--ink); }
@media (max-width:760px) { body.is-home .site-header { position: absolute; } }
.preview-banner { position: fixed; z-index: 70; right: 10px; bottom: 10px; background: rgba(246,243,237,.92); border: 1px solid #b5afa4; padding: 9px 13px; font-size: 11px; color: #292c29; box-shadow: 0 7px 35px rgba(0,0,0,.14); }
@media(max-width:480px) { .preview-banner { font-size: 9px; padding: 8px; } }
'''
def productcard(p, i):
    return f'''<a class="product-card {'product-card--offset' if i%2 else ''}" href="#product/{p['slug']}" data-category="{esc(p['category'])}">
  <div class="product-card__photo"><picture><img src="{images[p['coverImage']]}" alt="{esc(p['alt'])}" loading="lazy"></picture></div>
  <div class="product-card__meta"><div><h3>{esc(p['title'])}</h3><p>{esc(p['category'])} basin <span aria-hidden="true">/</span> {esc(p['material'])}</p></div><span class="card-arrow" aria-hidden="true">↗</span></div>
</a>'''
feat=''.join(productcard(p,i) for i,p in enumerate(products))
collection=''.join(productcard(p,i) for i,p in enumerate(products))
filters=''.join(f'<button type="button" class="filter-button {"is-active" if i == 0 else ""}" data-filter="{esc(cat)}" aria-pressed="{str(i==0).lower()}">{esc(cat)}</button>' for i,cat in enumerate(['All']+list(dict.fromkeys(p['category'] for p in products))))
details=''
for p in products:
    spec=''.join(f'<div><dt>{label}</dt><dd>{esc(p[key])}</dd></div>' for label,key in [('Material','material'),('Finish','finish'),('Dimensions','dimensions')] if p.get(key))
    details+=f'''<section data-page="product/{p['slug']}" class="detail-section"><div class="container"><a class="back-link" href="#collection">← &nbsp; Back to collection</a><div class="detail-grid"><div class="detail-media"><picture class="detail-main-image"><img src="{images[p['coverImage']]}" alt="{esc(p['alt'])}" /></picture></div><div class="detail-copy"><p class="eyebrow eyebrow--dark">OBJECT / {esc(p['category'].upper())}</p><h1 class="display-title">{esc(p['title'])}</h1><p class="detail-description">{esc(p['description'])}</p><dl class="spec-list">{spec}</dl><a class="button button--dark" href="#contact?product={p['slug']}">Inquire about this piece <span>↗</span></a><p class="detail-footnote">For availability and custom requests, contact the studio.</p></div></div></div></section>'''

content=f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nicolas Khobelia | Interactive design preview</title><meta name="description" content="Interactive local preview of the Nicolas Khobelia portfolio design"><style>{css}\n{additional}</style></head>
<body class="is-home"><a class="skip-link" href="#main-content">Skip to content</a>
<header class="site-header"><a class="brand" href="#home"><span class="brand-mark">NK</span><span class="brand-name">NICOLAS<br>KHOBELIA</span></a><button class="menu-toggle" aria-controls="primary-nav" aria-expanded="false" aria-label="Open navigation"><span></span><span></span></button><nav id="primary-nav" class="primary-nav" aria-label="Main navigation"><a href="#home">Home</a><a href="#collection">Collection</a><a href="#studio">The studio</a><a href="#contact">Contact</a></nav></header>
<main id="main-content">
<div data-page="home" class="active">
 <section class="hero"><picture class="hero-image"><img src="{images[site['heroImage']]}" alt="Round concrete basin with black tap"></picture><div class="hero-shade"></div><div class="container hero-content"><div class="hero-copy"><p class="eyebrow hero-eyebrow"><span class="eyebrow-rule"></span>{esc(site['strapline'])}</p><h1>{esc(site['heroTitle'])}</h1><p class="hero-description">{esc(site['heroSubtitle'])}</p><a class="button button--light" href="#collection">Explore collection <span>↗</span></a></div><div class="hero-index">01<span class="hero-index-rule"></span>02</div></div><a class="hero-scroll" href="#intro-anchor">SCROLL TO EXPLORE <span>↓</span></a></section>
 <section class="intro-section section-pad" id="intro-anchor"><div class="container intro-grid"><p class="eyebrow eyebrow--dark">{esc(site['introEyebrow'])}<span class="tiny-square"></span></p><div><h2 class="display-title intro-title">{esc(site['introTitle'])}</h2><p class="intro-body">{esc(site['introDescription'])}</p></div></div></section>
 <section class="works-section section-pad"><div class="container"><div class="section-heading"><div><p class="eyebrow eyebrow--dark">{esc(site['worksEyebrow'])}</p><h2 class="display-title">{esc(site['worksTitle'])}</h2></div><a class="text-link" href="#collection">All works <span>↗</span></a></div><div class="product-grid">{feat}</div></div></section>
 <section class="studio-split"><div class="studio-split__image"><picture><img src="{images[site['aboutImage']]}" alt="Oval concrete basin"></picture></div><div class="studio-split__copy"><div><p class="eyebrow eyebrow--dark">{esc(site['aboutEyebrow'])}</p><h2 class="display-title">{esc(site['aboutTitle'])}</h2><p>{esc(site['aboutDescription'])}</p><a class="text-link" href="#studio">Meet the maker <span>↗</span></a></div><span class="studio-split__number">NK — 001</span></div></section>
 <section class="end-cta section-pad"><div class="container end-cta__inner"><p class="eyebrow">HAVE A PROJECT IN MIND?</p><h2 class="display-title">Beautiful objects<br><em>begin with a conversation.</em></h2><a class="button button--outline-light" href="#contact">Get in touch <span>↗</span></a></div></section>
</div>
<div data-page="collection"><section class="page-hero page-hero--collection"><div class="container"><p class="eyebrow eyebrow--dark">THE COLLECTION / 001</p><div class="page-hero__row"><h1 class="display-title">The collection<span class="heading-period">.</span></h1><p>A study in form, material and texture. Each piece brings its own quiet character into a space.</p></div></div></section><section class="collection-section"><div class="container"><div class="collection-toolbar"><div class="filters" role="group" aria-label="Filter by shape">{filters}</div><span class="collection-count">{len(products):02d} OBJECTS</span></div><div class="product-grid collection-grid">{collection}</div><p class="filter-empty" hidden>No objects in this category yet.</p></div></section></div>
<div data-page="studio"><section class="about-page-section"><div class="container about-page-grid"><div class="about-page-text"><p class="eyebrow eyebrow--dark">ABOUT NICOLAS / THE STUDIO</p><h1 class="display-title">{esc(site['aboutTitle'])}</h1><p class="lead">{esc(site['aboutDescription'])}</p><p>From rounded silhouettes to subtle surface textures, the work explores how a practical object can become a distinctive part of an interior.</p><a class="text-link" href="#contact">Start a conversation <span>↗</span></a></div><div class="about-page-media"><picture><img src="{images[site['aboutImage']]}" alt="Oval concrete basin"></picture></div></div></section><section class="about-statement"><div class="container"><p class="eyebrow eyebrow--dark">A SIMPLE IDEA</p><h2 class="display-title">Texture, proportion,<br><em>and a sense of place.</em></h2></div></section></div>
<div data-page="contact"><section class="contact-section"><div class="container contact-grid"><div class="contact-intro"><p class="eyebrow eyebrow--dark">CONTACT THE STUDIO</p><h1 class="display-title">{esc(site['contactTitle'])}</h1><p class="lead">{esc(site['contactDescription'])}</p></div><form class="inquiry-form" id="demo-inquiry"><div class="form-row"><label for="demo-name">YOUR NAME *</label><input id="demo-name" name="name" placeholder="Name" minlength="2" required></div><div class="form-row"><label for="demo-email">EMAIL ADDRESS *</label><input id="demo-email" type="email" name="email" placeholder="Email" required></div><div class="form-row"><label for="demo-subject">SUBJECT</label><select id="demo-subject" name="subject"><option>Product inquiry</option><option>Custom project</option><option>General question</option></select></div><p id="demo-product" class="product-note" hidden></p><div class="form-row"><label for="demo-message">YOUR MESSAGE *</label><textarea id="demo-message" name="message" placeholder="Tell us about your project or the piece you're interested in…" rows="6" required minlength="10"></textarea></div><button class="button button--dark" type="submit">Send inquiry <span>↗</span></button><p class="form-privacy">Preview only — messages are not sent from this offline file.</p></form></div></section></div>
{details}
</main>
<footer class="site-footer"><div class="container footer-top"><a class="footer-brand" href="#home">Nicolas Khobelia<span>Objects with character.</span></a><div class="footer-links"><a href="#collection">Collection</a><a href="#studio">Studio</a><a href="#contact">Contact</a></div></div><div class="container footer-bottom"><span>© 2026 Nicolas Khobelia</span><span>Designed with restraint.</span></div></footer>
<div class="preview-banner" aria-label="Preview status">DESIGN PREVIEW · NOT LIVE</div>
<script>
(function(){{
 const pages=[...document.querySelectorAll('[data-page]')];
 const header=document.querySelector('.site-header');
 const menu=document.querySelector('.menu-toggle');
 function openMenu(open){{ header.classList.toggle('menu-open',open); document.body.classList.toggle('nav-open',open); menu.setAttribute('aria-expanded',String(open)); menu.setAttribute('aria-label',open?'Close navigation':'Open navigation'); }}
 menu.addEventListener('click',()=>openMenu(!header.classList.contains('menu-open')));
 document.querySelectorAll('.primary-nav a').forEach(a=>a.addEventListener('click',()=>openMenu(false)));
 function route(){{
  let raw=decodeURIComponent(location.hash.slice(1)||'home');
  let [slug,search]=raw.split('?');
  if(!pages.some(p=>p.dataset.page===slug)) slug='home';
  pages.forEach(p=>p.classList.toggle('active',p.dataset.page===slug));
  document.body.classList.toggle('is-home',slug==='home');
  const selected=new URLSearchParams(search||'').get('product');
  const note=document.querySelector('#demo-product');
  const obj={json.dumps({p['slug']: p['title'] for p in products})};
  if(selected && obj[selected]){{ note.hidden=false; note.textContent='Regarding: '+obj[selected]; }} else note.hidden=true;
  openMenu(false);
  window.scrollTo({{top:0,behavior:'instant'}});
 }}
 window.addEventListener('hashchange',route);route();
 const buttons=document.querySelectorAll('.filter-button');
 const cards=document.querySelectorAll('.collection-grid .product-card');
 buttons.forEach(button=>button.addEventListener('click',()=>{{
   const category=button.dataset.filter;let visible=0;
   buttons.forEach(btn=>{{btn.classList.toggle('is-active',btn===button);btn.setAttribute('aria-pressed',String(btn===button));}});
   cards.forEach(card=>{{const show=category==='All'||card.dataset.category===category;card.hidden=!show;if(show)visible++;}});
   document.querySelector('.collection-count').textContent=String(visible).padStart(2,'0')+' OBJECTS';
   document.querySelector('.filter-empty').hidden=visible!==0;
 }}));
 document.querySelector('#demo-inquiry').addEventListener('submit',(e)=>{{e.preventDefault();alert('Design preview only. Your message has not been sent. The deployed site will use Netlify Forms.');}});
}})();
</script></body></html>'''
output = ROOT / 'offline-preview.html'
output.write_text(content)
print(f'Wrote {output} ({output.stat().st_size:,} bytes)')
