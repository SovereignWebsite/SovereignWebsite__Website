// Checks the built site before every push: run with  bash tools/check.sh
// For each page in site/, at 390 and 1366 px, light and dark: axe (WCAG A/AA), no sideways scroll,
// the Choose a design picker at the top while the pick is open, no broken local links or images.
// Also: no em dashes in site/. Exit 1 on any failure.
import { createRequire } from 'node:module';
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const { default: AxeBuilder } = await import(process.env.AXE_PATH || '@axe-core/playwright');
const SITE = resolve(dirname(new URL(import.meta.url).pathname), '..', 'site');
const PORT = process.env.PORT || 8765;
const PICK_OPEN = existsSync(join(SITE, 'designs', 'picker.css'));
const files = [];
(function walk(d) { for (const f of readdirSync(d)) { const p = join(d, f); statSync(p).isDirectory() ? walk(p) : p.endsWith('.html') && files.push(p.slice(SITE.length + 1)); } })(SITE);
let fails = 0; const fail = (m) => { fails++; console.log('FAIL', m); };
for (const f of files) {
  const t = readFileSync(join(SITE, f), 'utf8');
  if (t.includes('—')) fail(`${f}: em dash`);
  for (const [, u] of t.matchAll(/(?:href|src)="([^"#?:]+)(?:[#?][^"]*)?"/g)) {
    if (u.startsWith('/') || u.startsWith('mailto')) continue;
    const p = resolve(dirname(join(SITE, f)), u);
    if (!existsSync(p) && !existsSync(join(p, 'index.html'))) fail(`${f}: broken local link ${u}`);
  }
}
// share-check: required on pages that carry share tags or live in for/; counted as a warning elsewhere
const NEED = ['og:title','og:description','og:url','og:type','og:site_name','og:locale','og:image','og:image:width','og:image:height','og:image:alt','twitter:card','twitter:title','twitter:description','twitter:image'];
let noShare = 0;
// width and height of a PNG or JPEG, from its header
function size(b) {
  if (b.readUInt32BE(0) === 0x89504e47) return [b.readUInt32BE(16), b.readUInt32BE(20)];
  for (let i = 2; i < b.length;) { if (b[i] !== 0xff) return [0, 0]; const m = b[i + 1], len = b.readUInt16BE(i + 2);
    if (m >= 0xc0 && m <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(m)) return [b.readUInt16BE(i + 7), b.readUInt16BE(i + 5)]; i += 2 + len; }
  return [0, 0];
}
for (const f of files) {
  const t = readFileSync(join(SITE, f), 'utf8');
  const meta = Object.fromEntries([...t.matchAll(/<meta (?:property|name)="([^"]+)" content="([^"]*)"/g)].map((m) => [m[1], m[2]]));
  const required = f.startsWith('for/') || 'og:title' in meta;
  if (!required) { noShare++; continue; }
  for (const k of NEED) if (!(k in meta)) fail(`${f}: share tag ${k} missing`);
  if (!/^https:\/\//.test(meta['og:url'] || '')) fail(`${f}: og:url not absolute https`);
  if (meta['twitter:card'] !== 'summary_large_image') fail(`${f}: twitter:card not summary_large_image`);
  if (meta['og:image:width'] !== '1200' || meta['og:image:height'] !== '630') fail(`${f}: og:image not 1200 x 630 in its tags`);
  const img = meta['og:image'] || '';
  if (!img.startsWith('https://sovereignwebsite.ai/')) fail(`${f}: og:image not on the site's own host`);
  else { const local = join(SITE, img.replace('https://sovereignwebsite.ai/', '')); if (!existsSync(local)) fail(`${f}: og:image file missing`); else { const [w, h] = size(readFileSync(local)); if (w !== 1200 || h !== 630) fail(`${f}: og:image file is not 1200 x 630`); } }
}
if (noShare) console.log(`warning: ${noShare} pages have no share tags yet`);
const b = await chromium.launch();
for (const f of files) for (const w of [390, 1366]) for (const scheme of ['light', 'dark']) {
  const ctx = await b.newContext({ viewport: { width: w, height: 844 }, colorScheme: scheme }); const p = await ctx.newPage();
  await p.goto(`http://localhost:${PORT}/${f}`);
  const r = await p.evaluate(() => ({ ov: document.documentElement.scrollWidth > innerWidth, top: document.querySelector('.pick-design')?.getBoundingClientRect().top ?? -1 }));
  if (r.ov) fail(`${f} ${w}px ${scheme}: sideways scroll`);
  if (PICK_OPEN && !f.startsWith('for/') && !f.startsWith('abp/') && (r.top < 0 || r.top > 60)) fail(`${f} ${w}px: picker not at the top`);
  const a = await new AxeBuilder({ page: p }).withTags(['wcag2a', 'wcag2aa']).analyze();
  for (const v of a.violations) fail(`${f} ${w}px ${scheme}: axe ${v.id} (${v.nodes.length}) ${v.help}`);
  await ctx.close();
}
await b.close();
console.log(`${files.length} pages checked, ${fails} failures`);
process.exit(fails ? 1 : 0);
