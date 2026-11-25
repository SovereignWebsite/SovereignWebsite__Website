#!/usr/bin/env python3
"""Builds the sector pages, site/for/<kind>.html: one short page per kind of person, made to be the link in an email.
First screen answers: what is this, what does it cost, what do I do. Under 2,500 px on a phone.
Run from the repository root: python3 tools/build_sectors.py  (then python3 tools/add_picker.py while the pick is open).
Every statement must stay true; the sample is fictional and labelled so; prices as on pricing.html."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_designs import header, footer, REQUEST, LOGO  # noqa: F401  (same header and footer as round 1)

OUT = Path(__file__).resolve().parent.parent / "site" / "for"
BASE = "https://sovereignwebsite.ai/for/"

SECTORS = {
    "profile": dict(
        kicker="For professionals", title="A profile of your own",
        h1="A profile of your own.",
        line="Your story, your work and how to reach you, on a site whose files you keep and can move.",
        share="A profile site of your own, built by a team of agents. £50 or £500, paid once.",
        sample=("Sam Rivers", "Product designer", ["About", "Work", "Experience", "Contact"],
                "I design tools that people use every day. Ten years in product teams, from start-ups to public services."),
        needs="Your history in your own words (a CV is a fine start), a photo, and the links you want shown.",
    ),
    "artist": dict(
        kicker="For artists", title="A website for your work",
        h1="A website of your own, for your work.",
        line="Your pictures and your words, made into a site you keep, with no subscription from us.",
        share="A website for your art, built by a team of agents. £50 or £500, paid once.",
        sample=("Ines Hart", "Painter", ["Work", "About", "Shows", "Contact"],
                "Oil and watercolour, mostly the sea. New paintings every season."),
        needs="Your pictures (links or files), a few lines about you, and links you want shown, such as an Instagram page or a shop.",
    ),
}

GET = '''<ul class="prom">
  <li><h3>Built for you</h3><p>A team of agents builds your site from your own words and photos.</p></li>
  <li><h3>Yours to keep</h3><p>The files and every change since the first, which you can copy and move to any host that serves files.</p></li>
  <li><h3>Paid once</h3><p>No subscription from us. You pay for your own domain if you want one.</p></li>
</ul>'''


def sample(name, role, nav, blurb):
    links = "".join(f"<span>{n}</span>" for n in nav)
    return f'''<figure class="sample"><div class="phone" aria-hidden="true">
<div class="s-top"><b>{name}</b><div class="s-nav">{links}</div></div>
<div class="s-hero"><svg width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="currentColor" opacity=".18"/><circle cx="32" cy="25" r="11" fill="currentColor" opacity=".45"/><rect x="14" y="40" width="36" height="18" rx="9" fill="currentColor" opacity=".45"/></svg>
<p class="s-name">{name}</p><p class="s-role">{role}</p></div>
<p class="s-blurb">{blurb}</p>
<div class="s-grid"><i></i><i></i><i></i><i></i></div>
</div><figcaption>A fictional example: {name} is not a real person.</figcaption></figure>'''


def page(kind, d):
    url = f"{BASE}{kind}.html"
    img = f"{BASE}og-{kind}.png"
    title = f"{d['title']}: Sovereign Website"
    body = f'''<a class="skip" href="#main">Skip to content</a>
{header()}
<main id="main">
<section class="sec sector" aria-labelledby="hero-title"><div class="w sgrid">
<div><p class="kicker">{d['kicker']}</p><h1 id="hero-title">{d['h1']}</h1>
<p class="lead">{d['line']}</p>
<p class="priceline"><strong>&pound;50 or &pound;500</strong>, promotional, paid once. &pound;50: we build it and hand it over as it is. &pound;500: a couple of rounds of changes with you first. <a href="../pricing.html">Prices</a></p>
<div class="acts"><a class="btn" href="{REQUEST}">Yes, I would like one</a></div></div>
{sample(*d['sample'])}
</div></section>
<section class="sec" aria-labelledby="get-t"><div class="w"><h2 id="get-t">What you get</h2>{GET}
<p class="fine">What we need from you: {d['needs']}</p></div></section>
<section class="sec" aria-labelledby="how-t"><div class="w"><h2 id="how-t">How it works</h2>
<ol class="steps short"><li><h3>Tell us about you</h3></li><li><h3>We build it</h3></li><li><h3>It is handed over, and you can change it yourself</h3></li></ol>
<div class="acts"><a class="btn" href="{REQUEST}">Yes, I would like one</a></div>
<p class="fine">Questions? Ask on the <a href="{REQUEST}">Hub's start page</a>, or read <a href="../how-it-works.html">how it works</a>.</p></div></section>
</main>
<footer class="ft ft-short"><div class="w">
<p><a href="../index.html">Sovereign Website</a> &middot; <a href="../how-it-works.html">How it works</a> &middot; <a href="../pricing.html">Prices</a> &middot; <a href="../examples.html">Examples</a> &middot; <a href="https://hub.sovereignweb.site/">Hub</a> &middot; <a href="../trust.html">Trust</a></p>
<p class="fine" style="color:inherit"><strong>Where things stand:</strong> the hosted service under this name does not exist yet. Static files: no scripts, no forms, no cookies, no tracking.</p>
</div></footer>'''
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{d['share']}">
<meta name="author" content="Dinis Cruz">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{d['share']}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Sovereign Website">
<meta property="og:locale" content="en_GB">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{d['h1']} Sovereign Website, £50 or £500.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{d['share']}">
<meta name="twitter:image" content="{img}">
<link rel="canonical" href="{url}">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../designs/round.css">
<link rel="stylesheet" href="sector.css">
</head>
<body class="rd">
{body}
</body>
</html>
'''


def share_card(kind, d):
    """HTML for the 1200 x 630 share image, rendered to og-<kind>.png by tools/build_sectors_images.mjs."""
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;width:1200px;height:630px;background:#FAF7F0;color:#14213D;font-family:system-ui,sans-serif;display:flex;flex-direction:column;justify-content:center;padding:0 90px;box-sizing:border-box}}
.k{{font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#1D4ED8;font-size:26px}}
h1{{font:600 84px/1.05 "Iowan Old Style",Palatino,Georgia,serif;margin:22px 0 26px;max-width:960px}}
p{{font-size:34px;color:#4A5568;margin:0}}.b{{margin-top:40px;font-weight:700;font-size:30px;display:flex;align-items:center;gap:14px}}
.b svg{{width:40px;height:40px}}</style></head><body>
<div class="k">{d['kicker']}</div><h1>{d['h1']}</h1><p>&pound;50 or &pound;500, paid once. Built by agents, owned by you.</p>
<div class="b">{LOGO}Sovereign Website</div></body></html>'''


def main():
    OUT.mkdir(exist_ok=True)
    for kind, d in SECTORS.items():
        (OUT / f"{kind}.html").write_text(page(kind, d), encoding="utf-8")
        (OUT.parent.parent / "tools" / "out").mkdir(exist_ok=True)
        (OUT.parent.parent / "tools" / "out" / f"og-{kind}.html").write_text(share_card(kind, d), encoding="utf-8")
        print("wrote", kind)


if __name__ == "__main__":
    main()
