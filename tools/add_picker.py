#!/usr/bin/env python3
"""Puts the "Choose a design" picker at the top of every page while the pick is open (Dinis's standing rule).
Idempotent: the block sits between <!-- picker:start --> and <!-- picker:end -->; run again to refresh, or with --remove after the pick.
Designs 6 to 10 get their picker from tools/build_designs.py and are skipped here."""
import re, sys
from pathlib import Path
SITE = Path(__file__).resolve().parent.parent / "site"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_designs import ROUND, ROUND2, CURRENT, older

def block(prefix, current):
    def item(n, name, line):
        cur = ' aria-current="page"' if n == current else ""
        here = '<span class="pk-now">You are here</span>' if n == current else ""
        live = ' <span class="pk-tag">Live</span>' if n == 1 else ""
        return (f'<li><a href="{prefix}designs/{n}.html"{cur}><img src="{prefix}designs/thumbs/{n}-phone.jpg" width="195" height="422" alt="" loading="lazy" decoding="async">'
                f'<strong>Design {n}, {name}{live}</strong><span>{line}</span>{here}</a></li>')
    cur_items = "\n".join(item(n, nm, ln) for n, nm, ln, _ in CURRENT)
    old_items = "\n".join(item(n, nm, ln) for n, nm, ln in older())
    names = {**{n: nm for n, nm, _, _ in CURRENT}, **{n: nm for n, nm, _ in older()}}
    line = (f'Preview: design {current}, {names[current]}. The live site uses design 1.' if current else 'Round 2 of the restyle is open for picking. The live site uses design 1.')
    return f'''<!-- picker:start -->
<div class="pickbar-top"><details class="pick-design">
  <summary>Choose a design</summary>
  <div class="pk-panel">
    <p class="pk-intro">Round 2 of the restyle: five structurally different directions for this site, each with the same words and prices. Dinis Cruz picks one; until then the home page stays as it is. <a href="{prefix}designs/index.html">All designs</a></p>
    <ul>
{cur_items}
    </ul>
    <details class="pk-old">
      <summary>Earlier designs ({len(older())})</summary>
      <ul>
{old_items}
      </ul>
    </details>
    <p><a href="{prefix}designs/index.html">Compare all designs</a></p>
  </div>
</details> <span class="pk-line">{line} <a href="{prefix}designs/index.html">All designs</a></span></div>
<!-- picker:end -->'''

remove = "--remove" in sys.argv
for f in sorted(SITE.rglob("*.html")):
    rel = f.relative_to(SITE)
    if rel.parts[0] == "designs" and rel.stem.split("-")[0] in {str(n) for n, *_ in ROUND + ROUND2}:
        continue
    if rel.parts[0] in ("for", "abp"):  # sector pages are emailed links, not part of the pick (a.design, 25 Nov)
        continue
    s = f.read_text(encoding="utf-8")
    s = re.sub(r"<!-- picker:start -->.*?<!-- picker:end -->\n?", "", s, flags=re.S)
    prefix = "../" * (len(rel.parts) - 1)
    css = f'<link rel="stylesheet" href="{prefix}designs/picker.css">'
    s = s.replace(css + "\n", "")
    if not remove:
        current = int(rel.stem) if rel.parts[0] == "designs" and rel.stem.isdigit() else None
        s = re.sub(r"(<body[^>]*>\n?)", lambda m: m.group(1) + block(prefix, current) + "\n", s, count=1)
        s = s.replace("</head>", css + "\n</head>", 1)
    f.write_text(s, encoding="utf-8")
    print(("removed " if remove else "picker ") + str(rel))
