// Renders tools/out/og-<kind>.html to site/for/og-<kind>.png at 1200 x 630 (the share image). Run after build_sectors.py.
import { createRequire } from 'node:module'; import { readdirSync } from 'node:fs'; import { resolve, dirname } from 'node:path';
const require = createRequire(import.meta.url); const { chromium } = require('playwright');
const root = resolve(dirname(new URL(import.meta.url).pathname), '..');
const b = await chromium.launch();
for (const f of readdirSync(`${root}/tools/out`).filter((f) => f.startsWith('og-') && f.endsWith('.html'))) {
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await p.goto(`file://${root}/tools/out/${f}`);
  await p.screenshot({ path: `${root}/site/for/${f.replace('.html', '.png')}` }); console.log('image', f); await p.close();
}
await b.close();
