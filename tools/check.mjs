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
const b = await chromium.launch();
for (const f of files) for (const w of [390, 1366]) for (const scheme of ['light', 'dark']) {
  const ctx = await b.newContext({ viewport: { width: w, height: 844 }, colorScheme: scheme }); const p = await ctx.newPage();
  await p.goto(`http://localhost:${PORT}/${f}`);
  const r = await p.evaluate(() => ({ ov: document.documentElement.scrollWidth > innerWidth, top: document.querySelector('.pick-design')?.getBoundingClientRect().top ?? -1 }));
  if (r.ov) fail(`${f} ${w}px ${scheme}: sideways scroll`);
  if (PICK_OPEN && (r.top < 0 || r.top > 60)) fail(`${f} ${w}px: picker not at the top`);
  const a = await new AxeBuilder({ page: p }).withTags(['wcag2a', 'wcag2aa']).analyze();
  for (const v of a.violations) fail(`${f} ${w}px ${scheme}: axe ${v.id} (${v.nodes.length}) ${v.help}`);
  await ctx.close();
}
await b.close();
console.log(`${files.length} pages checked, ${fails} failures`);
process.exit(fails ? 1 : 0);
