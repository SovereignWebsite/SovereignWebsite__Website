#!/usr/bin/env python3
"""Builds round 1 of the restyle, site/designs/6.html to 10.html, from shared parts.

Run from the repository root: python3 tools/build_designs.py
Output is plain static HTML; nothing here runs on the site. Direction from a.design, 25 Nov 2026.
Every statement must stay true: prices as on pricing.html, examples only with consent, North Studio labelled fictional.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "site" / "designs"
REQUEST = "https://hub.sovereignweb.site/start/"

ROUND = [
    (6, "Studio", "The brief itself: calm and expert", "d-studio"),
    (7, "The Brief", "One printable document, the comparison at its centre", "d-brief"),
    (8, "Five Designs", "Dark first; tap a design and the page takes its colours", "d-five"),
    (9, "Ownership", "A timeline of what you hold, each step with its proof", "d-own"),
    (10, "The Hub", "A map of real sites, with room for yours", "d-hub"),
]
EARLIER = [
    (1, "The plain promise", "Chosen on 20 November 2026; the current home page"),
    (2, "The question", "Where is your website, from 0 to 5?"),
    (3, "Under your own roof", "Your files, your domain, your host"),
    (4, "Five designs", "The method as the message"),
    (5, "The model", "The maturity model first"),
]
FAMILY = [
    ("https://sovereignwebsite.ai/", "Sovereign Website"),
    ("https://sovereignwebsite.org/", "Principles"),
    ("https://sovereignwebsite.site/", "Hosted"),
    ("https://hub.sovereignweb.site/", "Hub"),
    ("https://vault.sovereignwebsite.site/", "Vault"),
    ("https://agenticcells.ai/", "AgentiCCells"),
    ("https://riskmandate.ai/", "RiskMandate"),
    ("https://newsroom.sgit.ai/", "Newsroom"),
]
NAV = [("../how-it-works.html", "How it works"), ("../examples.html", "Examples"), ("../pricing.html", "Prices"), ("https://hub.sovereignweb.site/", "Hub")]
LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><rect x="2" y="2" width="28" height="28" rx="7" fill="none" stroke="currentColor" stroke-width="2.5"/><path d="M10 16.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def picker(current):
    def item(n, name, line, now):
        cur = ' aria-current="page"' if now else ""
        here = '<span class="pk-now">You are here</span>' if now else ""
        live = ' <span class="pk-tag">Live</span>' if n == 1 else ""
        return (f'<li><a href="{n}.html"{cur}><img src="thumbs/{n}-phone.jpg" width="195" height="422" alt="" loading="lazy" decoding="async">'
                f'<strong>Design {n}, {name}{live}</strong><span>{line}</span>{here}</a></li>')
    cur_items = "\n".join(item(n, name, line, n == current) for n, name, line, _ in ROUND)
    old_items = "\n".join(item(n, name, line, n == current) for n, name, line in EARLIER)
    return f'''<div class="pickbar"><div class="w">
<details class="pick-design">
  <summary>Choose a design</summary>
  <div class="pk-panel">
    <p class="pk-intro">Round 1 of the restyle: five directions for this site, each with the same words and prices. Dinis Cruz picks one; until then the home page stays as it is. <a href="index.html">All designs</a></p>
    <ul>
{cur_items}
    </ul>
    <details class="pk-old">
      <summary>Earlier designs (5)</summary>
      <ul>
{old_items}
      </ul>
    </details>
    <p><a href="index.html">Compare all designs</a></p>
  </div>
</details>
<span class="fine">Preview: design {current}, {dict((n, nm) for n, nm, _, _ in ROUND)[current]}. The live site uses design 1. <a href="index.html">All designs</a></span>
</div></div>'''


def header():
    fam = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in FAMILY)
    nav = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in NAV)
    return f'''<nav class="fam" aria-label="The Sovereign Website family"><div class="w"><ul>{fam}</ul></div></nav>
<header class="hd"><div class="w">
  <a class="brand" href="../index.html">{LOGO}<span class="bt">Sovereign Website</span></a>
  <nav class="nav" aria-label="Main"><ul>{nav}</ul></nav>
  <details class="menu"><summary>Menu</summary><div class="mpanel">
    <ul>{nav}<li><a href="../open.html">Open pattern</a></li><li><a href="../pt/index.html" lang="pt-PT">Português</a></li></ul>
    <p class="fine">The family</p><ul>{fam}</ul>
  </div></details>
  <a class="btn" href="{REQUEST}"><span>Request<span class="vh-phone">&nbsp;a website</span></span></a>
</div></header>'''


def strip():
    cards = [("n1", "Editorial", "Architecture for modern living."), ("n2", "Warm", "Architecture for contemporary life."),
             ("n3", "Bold", "Architecture for contemporary life."), ("n4", "Immersive", "Architecture for contemporary life."),
             ("n5", "Minimal", "Architecture for contemporary life.")]
    figs = "".join(f'<figure><div class="ph {c}" aria-hidden="true"><b>NORTH STUDIO</b><p>{p}</p><svg width="100" height="60" viewBox="0 0 100 60" aria-hidden="true" focusable="false"><rect x="2" y="16" width="96" height="6" fill="currentColor" opacity=".7"/><rect x="10" y="22" width="66" height="32" fill="currentColor" opacity=".22"/><rect x="38" y="30" width="30" height="24" fill="currentColor" opacity=".5"/><rect x="0" y="54" width="100" height="4" fill="currentColor" opacity=".35"/></svg></div><figcaption>{n}</figcaption></figure>' for c, n, p in cards)
    return f'''<div><div class="ns" tabindex="0" role="region" aria-label="Five designs for North Studio, a fictional studio">{figs}</div>
<p class="nscap">North Studio is a fictional architecture studio, made to show the five designs.</p></div>'''


HERO_WORDS = '<p class="kicker">Sovereign Website</p><h1 id="hero-title">Your website. Built by agents, owned by you.</h1>'
HERO_LINE = '<p class="lead">Tell a team of agents what you want. They build your site and hand it over. You keep the files and every change since the first, and you can move it to any host that serves files.</p>'
HERO_ACTS = f'<div class="acts"><a class="btn" href="{REQUEST}">Request a website</a><a class="btn alt" href="#five">See five designs for one brief</a></div>'

PRICES = '''<div class="prices">
  <div class="pcard"><p class="kicker">As it is</p><p class="amt">&pound;50</p><ul><li>You send us the details.</li><li>We build your site and hand it over as it is.</li><li>After that you make any changes yourself.</li></ul></div>
  <div class="pcard"><p class="kicker">With rounds of changes</p><p class="amt">&pound;500</p><ul><li>The same as &pound;50.</li><li>We go back and forth with you a couple of times before hand-over.</li><li>Any further customisation we agree with you.</li></ul></div>
</div>
<p class="fine">Promotional prices, set by Dinis Cruz on 25 November 2026; they can change at any time. Paid once, no subscription from us. You pay for your own domain if you want one; to edit the site yourself you need a Claude plan, or a partner. <a href="../pricing.html">Every price, with its label</a>.</p>'''

PROMISES = '''<ul class="prom">
  <li><h3>A team builds it</h3><p>An interview about what you want, then a team of agents builds your site from your own photos and words.</p></li>
  <li><h3>You keep the files</h3><p>Its own repository, with every change since the first. Plain files you can copy anywhere.</p></li>
  <li><h3>You change it by talking</h3><p>Your own AI changes the site when you ask, inside a behaviour policy that says what it may touch. Every change can be undone.</p></li>
  <li><h3>You can move it</h3><p>No server code, no database. Any host that serves files can run it.</p></li>
</ul>'''

STEPS = f'''<ol class="steps">
  <li><h3>Tell us about you</h3><p>Who you are, what you do, a link or two, and any photos you want used.</p></li>
  <li><h3>We build it</h3><p>A team of agents makes your site from what you sent.</p></li>
  <li><h3>It is handed over</h3><p>You get the site, and from then on you can change it yourself.</p></li>
</ol>
<div class="acts"><a class="btn" href="{REQUEST}">Request a website</a></div>'''

EXAMPLES_DATA = [
    ("https://london.agentics-foundation.organisation.sovereignweb.site/", "ex-chapter", "A community chapter"),
    ("http://one-human-nine-agents.dinis.author.sovereignweb.site/", "ex-author", "An author's book site"),
    ("https://startup-grants.tool.sovereignweb.site/", "ex-grants", "A funding tool"),
    ("https://whois.tool.sovereignweb.site/", "ex-whois", "A lookup tool"),
]
EXAMPLES = '<ul class="ex">' + "".join(
    f'<li><a href="{u}"><img src="img/{i}.jpg" width="390" height="720" alt="Phone screenshot of {k.lower()}" loading="lazy" decoding="async"><span>{k}</span></a></li>'
    for u, i, k in EXAMPLES_DATA) + '</ul>\n<p class="fine">Real sites, shown with their owners\' agreement or ours. The author\'s site is Dinis Cruz\'s own book, served over http for now.</p>'

DOTS = '<svg width="260" height="180" viewBox="0 0 260 180" role="img" aria-label="Sites gathered in groups">' + "".join(
    f'<circle cx="{x}" cy="{y}" r="7" fill="#8AB0FF"/>' for x, y in [(40, 40), (62, 52), (48, 70), (70, 30), (150, 50), (172, 40), (160, 72), (186, 64), (90, 130), (112, 140), (100, 116), (200, 130), (222, 142), (210, 112)]) + '<circle cx="232" cy="38" r="8" fill="none" stroke="#F3EFE6" stroke-width="2"/></svg>'

HUB = f'''<section class="sec band" aria-labelledby="hub-title"><div class="w hubgrid">
<div><p class="kicker">The Hub</p><h2 id="hub-title">See the sites made so far.</h2>
<p class="lead">In the Hub's own words: &ldquo;Your own website, made for you by an agent team, in five designs. Yours to keep.&rdquo; Each site there shows how it was made and how to start.</p>
<div class="acts"><a class="btn" href="https://hub.sovereignweb.site/">Open the Hub</a></div></div>
<div>{DOTS}</div></div></section>'''

ROWS = [
    ("Who holds the files", "Plain files and their history, which you can copy", "Usually the platform", "Depends on the contract", "Depends on the contract"),
    ("Can you move it elsewhere", "Yes, to any host that serves files", "Usually not, or only part of it", "Usually yes, if you have the files", "Depends on the contract"),
    ("Monthly fee", "None from us", "Yes", "Usually none, unless you agree a retainer", "Depends on the contract"),
    ("Designs you see", "Five, as we work today", "Templates to choose from", "Depends on the designer", "Depends on the agency"),
    ("Who keeps it up to date", "You, by talking to your own AI, or a partner", "You, in the builder's editor", "The designer, if agreed", "The agency, if agreed"),
    ("If you stop paying", "Nothing stops: it was paid once", "Usually the site goes offline", "Usually the site stays where it is hosted", "Depends on the contract"),
]


def compare(n_rows=None, more=True):
    rows = ROWS if n_rows is None else ROWS[:n_rows]
    body = "".join(f'<tr><th scope="row">{r[0]}</th><td class="us">{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>' for r in rows)
    link = '<p><a href="7.html#compare">See the full comparison</a></p>' if more else ""
    return f'''<div class="cmpwrap"><table class="cmp"><caption class="fine" style="caption-side:bottom;text-align:left;padding-top:8px">Kinds of provider, not named companies. &ldquo;Usually&rdquo; means what is common, not true of every provider. For named builders, the Hub keeps a table quoted from their own pages, checked on 23 November 2026: <a href="https://hub.sovereignweb.site/">hub.sovereignweb.site</a>. Swipe sideways on a phone.</caption>
<thead><tr><th scope="col"><span class="fine">Question</span></th><th scope="col">Sovereign Website</th><th scope="col">Website builder subscription</th><th scope="col">Freelance designer</th><th scope="col">Agency</th></tr></thead>
<tbody>{body}</tbody></table></div>{link}'''


def footer():
    fam = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in FAMILY)
    return f'''<footer class="ft"><div class="w">
<div class="cols">
  <div><p><strong>Sovereign Website</strong></p><ul><li><a href="../how-it-works.html">How it works</a></li><li><a href="../pricing.html">Prices</a></li><li><a href="../examples.html">Examples</a></li><li><a href="../open.html">Open pattern</a></li></ul></div>
  <div><p><strong>More</strong></p><ul><li><a href="../moving.html">Moving your site</a></li><li><a href="../domain.html">Your domain</a></li><li><a href="../partners.html">Partners</a></li><li><a href="../trust.html">Trust</a></li><li><a href="../pt/index.html" lang="pt-PT">Português</a></li></ul></div>
  <div><p><strong>The family</strong></p><ul>{fam}</ul></div>
</div>
<p><strong>Where things stand:</strong> the hosted service under this name does not exist yet.</p>
<p class="fine" style="color:inherit">sovereignwebsite.ai is static files: no scripts, no forms, no cookies, no tracking. <a href="index.html">All designs</a>, <a href="../index.html">the current home page</a>.</p>
</div></footer>'''


def page(n, name, cls, main, pre_page=""):
    desc = f"Design {n} of round 1 for the sovereignwebsite.ai home page, {name}: a proposal from the design agent's direction of 25 November 2026, not yet the home page."
    inner = f'''<a class="skip" href="#main">Skip to content</a>
{picker(n)}
{header()}
<main id="main">
{main}
</main>
{footer()}'''
    body = f'{pre_page}<div class="page">\n{inner}\n</div>' if pre_page else inner
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Design {n}, {name}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Dinis Cruz">
<meta name="color-scheme" content="{'dark' if cls == 'd-five' else 'light dark'}">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="round.css">
<link rel="stylesheet" href="picker.css">
<style>@media(max-width:30rem){{.vh-phone{{display:none}}}}</style>
</head>
<body class="rd {cls}">
{body}
</body>
</html>
'''


def sec(id_, title, inner, kicker=""):
    k = f'<p class="kicker">{kicker}</p>' if kicker else ""
    return f'<section class="sec" id="{id_}" aria-labelledby="{id_}-t"><div class="w">{k}<h2 id="{id_}-t">{title}</h2>{inner}</div></section>'


def studio():
    hero = f'<section class="sec" aria-labelledby="hero-title"><div class="w hero-grid"><div>{HERO_WORDS}{HERO_LINE}{HERO_ACTS}</div><div id="five">{strip()}</div></div></section>'
    return "\n".join([hero, sec("prices", "Two prices, paid once", PRICES), sec("promises", "Four plain promises", PROMISES),
                      sec("how", "How it works", STEPS), sec("examples", "Sites like these", EXAMPLES), HUB,
                      sec("compare", "Own it, or rent it", compare(4))])


def brief():
    parts = [("what", "What it is", f'{HERO_LINE}<div id="five">{strip()}</div>'), ("prices", "The prices", PRICES), ("get", "What you get", PROMISES),
             ("how", "How it works", STEPS), ("compare", "How it compares", compare()), ("examples", "Sites like these", EXAMPLES),
             ("hub", "The Hub", '<p class="lead">In the Hub\'s own words: &ldquo;Your own website, made for you by an agent team, in five designs. Yours to keep.&rdquo;</p><p><a href="https://hub.sovereignweb.site/">Open the Hub</a></p>')]
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t, _ in parts)
    secs = "".join(f'<section id="{i}" aria-labelledby="{i}-t"><h2 id="{i}-t"><span class="n">{k + 1}</span>{t}</h2>{c}</section>' for k, (i, t, c) in enumerate(parts))
    return f'''<section class="sec" aria-labelledby="hero-title"><div class="w">{HERO_WORDS}<div class="acts"><a class="btn" href="{REQUEST}">Request a website</a></div></div></section>
<div class="w doc"><nav class="toc" aria-label="Contents"><p class="kicker">Contents</p><ol>{toc}</ol></nav><div>{secs}</div></div>'''


def five():
    cards = [("nd1", "n1", "Editorial", "Architecture for modern living."), ("nd2", "n2", "Warm", "Architecture for contemporary life."),
             ("nd3", "n3", "Bold", "Architecture for contemporary life."), ("nd4", "n4", "Immersive", "Architecture for contemporary life."),
             ("nd5", "n5", "Minimal", "Architecture for contemporary life.")]
    labels = "".join(f'<label for="{i}"><span class="ph {c}"><b>NORTH STUDIO</b><span class="pt">{p}</span><svg width="100" height="60" viewBox="0 0 100 60" aria-hidden="true" focusable="false"><rect x="2" y="16" width="96" height="6" fill="currentColor" opacity=".7"/><rect x="10" y="22" width="66" height="32" fill="currentColor" opacity=".22"/><rect x="38" y="30" width="30" height="24" fill="currentColor" opacity=".5"/><rect x="0" y="54" width="100" height="4" fill="currentColor" opacity=".35"/></svg></span><span>{n}</span></label>' for i, c, n, p in cards)
    hero = f'''<section class="sec" aria-labelledby="hero-title"><div class="w">{HERO_WORDS}{HERO_LINE}{HERO_ACTS}
<div id="five"><p class="fine">Tap a design: the page below takes its colours. North Studio is a fictional architecture studio, made to show the five designs.</p>
<div class="five" tabindex="0" role="region" aria-label="Five designs for North Studio, a fictional studio">{labels}</div></div></div></section>'''
    return "\n".join([hero, sec("prices", "Two prices, paid once", PRICES), sec("promises", "Four plain promises", PROMISES),
                      sec("how", "How it works", STEPS), sec("examples", "Sites like these", EXAMPLES), HUB, sec("compare", "Own it, or rent it", compare(4))])


def ownership():
    tl = '''<ol class="tl">
<li><h3>You ask</h3><p>You tell us who you are, what you do, and send a link or two and any photos.</p><span class="proof">Proof: your request, in writing</span></li>
<li><h3>We build it</h3><p>A team of agents builds the site. Every change is a commit in the site's own repository.</p><span class="proof">Proof: the history, one commit per change</span></li>
<li><h3>It is handed over</h3><p>You get the site: plain files and their whole history.</p><span class="proof">Proof: the files, which you can copy</span></li>
<li><h3>You change it</h3><p>Your own AI changes it when you ask, inside a behaviour policy. Every change can be undone.</p><span class="proof">Proof: your change, in the same history</span></li>
<li><h3>You move it anywhere</h3><p>Any host that serves files can run it. Moving these sites to a second host has not yet been shown; when it is, the proof goes here.</p><span class="proof">Proof: plain files, no server code</span></li>
</ol>'''
    hero = f'<section class="sec" aria-labelledby="hero-title"><div class="w">{HERO_WORDS}<p class="lead">What you hold, from the day you ask to the day you move it, each step with its proof.</p><div class="acts"><a class="btn" href="{REQUEST}">Request a website</a></div>{tl}</div></section>'
    return "\n".join([hero, sec("prices", "Two prices, paid once", PRICES), sec("five", "Five designs for one brief", strip()),
                      sec("compare", "Own it, or rent it", compare(4)), sec("examples", "Sites like these", EXAMPLES), HUB])


def hubmap():
    groups = [("Organisations", [EXAMPLES_DATA[0]]), ("Authors", [EXAMPLES_DATA[1]]), ("Tools", [EXAMPLES_DATA[2], EXAMPLES_DATA[3]])]
    g = "".join(f'<div class="grp"><h3>{t}</h3><ul>' + "".join(f'<li><a href="{u}">{k}</a></li>' for u, _, k in items) + '</ul></div>' for t, items in groups)
    g += f'<div class="grp yours"><h3>Yours could sit here</h3><p>A site for you, made the same way.</p><a class="btn" href="{REQUEST}">Request a website</a></div>'
    hero = f'''<section class="sec" aria-labelledby="hero-title"><div class="w">{HERO_WORDS}<p class="lead">Sites made this way, by kind. Each one is real and shown with its owner's agreement or ours.</p>
<div class="map">{g}</div><p class="fine"><a href="https://hub.sovereignweb.site/">See every site on the Hub</a>.</p></div></section>'''
    return "\n".join([hero, sec("five", "Five designs for one brief", strip()), sec("prices", "Two prices, paid once", PRICES),
                      sec("how", "How it works", STEPS), sec("compare", "Own it, or rent it", compare(4)), HUB])


def main():
    builders = {6: studio, 7: brief, 8: five, 9: ownership, 10: hubmap}
    for n, name, _, cls in ROUND:
        pre = "".join(f'<input class="pickn" type="radio" name="nd" id="nd{i}" aria-label="North Studio design {i}"{" checked" if i == 4 else ""}>' for i in range(1, 6)) if cls == "d-five" else ""
        (OUT / f"{n}.html").write_text(page(n, name, cls, builders[n](), pre), encoding="utf-8")
        print("wrote", n)


if __name__ == "__main__":
    main()
