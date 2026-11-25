#!/usr/bin/env python3
"""Round 2 of the restyle: five structurally different directions (designs 11 to 15), each with its own pricing page.
Brief: a.design, 25 Nov 2026, after Dinis's verdict on round 1 ("this needs to look like a super professional services site").
Run from the repository root: python3 tools/build_round2.py, then python3 tools/add_picker.py.
Every statement must stay true: prices £0, £50, £500 as on pricing.html; examples only with consent; fiction labelled as fiction."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_designs import ROUND2, REQUEST, page, compare, strip, EXAMPLES_DATA  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "site" / "designs"
TICK = '<span class="mk" aria-hidden="true">&#10003;</span>'
CROSS = '<span class="mk no" aria-hidden="true">&#10007;</span>'

TIERS = [
    ("&pound;0", "Do it yourself", "For people comfortable with GitHub and their own AI.",
     ["The approach, described in the open", "Your own AI does the work", "Nothing to pay us"],
     ["No build or hand-over by us", "The pattern's own repository is not published yet"],
     ("../open.html", "About the open pattern", True)),
    ("&pound;50", "Built for you", "For people who want a site made, and will change it themselves.",
     ["A site built by a team of agents from your words, photos and links", "Hand-over of the files and every change since the first", "Paid once, no subscription from us"],
     ["Rounds of changes before hand-over", "Your domain: you pay for your own"],
     (REQUEST, "Request a website", False)),
    ("&pound;500", "Built with you", "For people who want to shape the site with us before hand-over.",
     ["Everything in &pound;50", "A couple of rounds back and forth with you before hand-over", "Further customisation, agreed with you"],
     ["Your domain: you pay for your own", "Help after hand-over: offered by partners, at their prices"],
     (REQUEST, "Request a website", False)),
]
PROMO = "Promotional prices, set by Dinis Cruz on 25 November 2026; they can change at any time. Paid once, no subscription from us."
FAQ = [
    ("Is there a monthly fee?", "No subscription from us. Hosting can be free: GitHub Pages serves a static site at no charge. Your domain is yours to pay for."),
    ("Can I pay on this site?", f'Not today. You ask through the <a href="{REQUEST}">Hub\'s start page</a>, and we reply.'),
    ("What happens after hand-over?", 'You change the site with your own AI (a Claude plan), edit the files yourself, or ask a <a href="../partners.html">partner</a>.'),
    ("Can I move it later?", 'Yes. Plain files, no server code, no database: any host that serves files can run it. See <a href="../moving.html">moving your site</a>.'),
    ("What does promotional mean?", "These prices were set by Dinis Cruz on 25 November 2026 for the launch, and they can change at any time."),
    ("What if I need more?", "Ask a partner. Partners may use the published ladder of &pound;500, &pound;1,500, &pound;5,000 and &pound;20,000, or set their own prices."),
]


def tiers(full=True):
    cols = ""
    for price, name, who, inc, exc, (href, label, alt) in TIERS:
        inc_li = "".join(f"<li>{TICK}<span>Included: {i}</span></li>" for i in inc)
        exc_li = "".join(f"<li>{CROSS}<span>Not included: {e}</span></li>" for e in exc) if full else ""
        cols += (f'<div class="tcol{" mid" if name == "Built for you" else ""}"><p class="tname">{name}</p><p class="tprice">{price}</p>'
                 f'<p class="twho">{who}</p><ul class="tlist">{inc_li}{exc_li}</ul>'
                 f'<p class="tact"><a class="btn{" alt" if alt else ""}" href="{href}">{label}</a></p></div>')
    return f'<div class="tiers3">{cols}</div><p class="fine">{PROMO} You pay for your own domain if you want one; to edit the site yourself you need a Claude plan, or a partner.</p>'


def faq():
    return '<div class="faqs">' + "".join(f'<details class="q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + "</div>"


def section(id_, title, inner, kicker="", cls=""):
    k = f'<p class="kicker">{kicker}</p>' if kicker else ""
    return f'<section class="sec {cls}" id="{id_}" aria-labelledby="{id_}-t"><div class="w">{k}<h2 id="{id_}-t">{title}</h2>{inner}</div></section>'


def pricing_page(n):
    return "\n".join([
        f'<section class="sec phead" aria-labelledby="hero-title"><div class="w"><p class="kicker">Prices</p><h1 id="hero-title">Simple prices, paid once.</h1>'
        f'<p class="lead">{PROMO}</p><div class="acts"><a class="btn" href="{REQUEST}">Request a website</a></div></div></section>',
        f'<section class="sec" aria-label="The three tiers"><div class="w">{tiers()}</div></section>',
        section("faq", "Questions", faq()),
        section("compare", "How it compares", compare(more=False)),
        f'<section class="sec"><div class="w"><p><a href="{n}.html">Back to the home page of design {n}</a></p></div></section>',
    ])


ACT = f'<a class="btn" href="{REQUEST}">Request a website</a>'
SHOTS = {i: (u, k) for u, i, k in EXAMPLES_DATA}


def consultancy(n):
    tiles = [("A website, built for you", "From your words and photos, by a team of agents.", "../how-it-works.html"),
             ("Five designs for one brief", "Several directions to look at before you choose one.", "index.html"),
             ("Moving off a platform", "Your old site's words and pictures, rebuilt as plain files.", "../moving.html"),
             ("Your own domain", "How to hold your address yourself, at a registrar you choose.", "../domain.html"),
             ("Changes by talking", "Your own AI edits the site, inside a behaviour policy.", "../how-it-works.html"),
             ("For agencies and freelancers", "Sell sites to your clients; we build them.", "../partners.html")]
    grid = "".join(f'<li><a href="{h}"><h3>{t}</h3><p>{d}</p></a></li>' for t, d, h in tiles)
    steps = "".join(f'<li><span class="n">0{i}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate([
        ("Ask", "Tell us who you are and what you do."), ("Design", "A team of agents makes designs from your material."),
        ("Build", "The chosen design becomes your site."), ("Hand over", "You get the files and every change since the first.")], 1))
    proof = [("This site's files are public", "Read every page and every change in its repository.", "https://github.com/SovereignWebsite/SovereignWebsite__Website"),
             ("Each change is signed", "Every change to this site is signed by whoever made it and checked before it goes live.", "../trust.html"),
             ("Live sites you can open", "Real sites made this way, shown with their owners' agreement.", "../examples.html"),
             ("Checked before each change", "Every page is checked for accessibility (WCAG A and AA) before we push.", "../trust.html")]
    pr = "".join(f'<li><h3><a href="{h}">{t}</a></h3><p>{d}</p></li>' for t, d, h in proof)
    return "\n".join([
        f'''<section class="sec chero" aria-labelledby="hero-title"><div class="w cgrid">
<div><p class="kicker">Sovereign Website</p><h1 id="hero-title">Websites you own, built by a team of agents.</h1>
<p class="lead">We build your site from your own words and photos, and hand it over: the files, the history and the choice of where it runs.</p>
<div class="acts">{ACT}<a class="btn alt" href="{n}-pricing.html">See prices</a></div></div>
<div><p class="kicker">What we do</p><ul class="svc">{grid}</ul></div></div></section>''',
        f'<section class="sec procband" aria-labelledby="proc-t"><div class="w"><h2 id="proc-t">How we work</h2><ol class="proc">{steps}</ol></div></section>',
        section("proof", "Proof you can check", f'<ul class="proofs">{pr}</ul>'),
        section("prices", "Prices", tiers(full=False) + f'<p><a href="{n}-pricing.html">Full prices, questions and comparison</a></p>'),
    ])


def product(n):
    return "\n".join([
        f'''<section class="sec phero" aria-labelledby="hero-title"><div class="w">
<p class="kicker">Sovereign Website</p><h1 id="hero-title">Your website, built by agents and handed to you.</h1>
<p class="lead">Five designs, the one you pick, and the files to keep.</p><div class="acts">{ACT}</div>
<figure class="frame"><div class="fbar" aria-hidden="true"><i></i><i></i><i></i><span>sovereignwebsite.ai/designs/</span></div>
<img src="img/desk-designs.jpg" width="640" height="400" alt="Screenshot of this site's own design picker page, showing five designs side by side">
<figcaption>A real page: this site choosing its own design.</figcaption></figure></div></section>''',
        '''<section class="sec" aria-label="Why it is different"><div class="w"><ul class="three">
<li><h3>Five designs, then you pick</h3><p>Several directions made from your material, so you choose by looking.</p></li>
<li><h3>Plain files you can move</h3><p>No server code and no database. Any host that serves files can run it.</p></li>
<li><h3>Paid once</h3><p>No subscription from us. You pay for your own domain if you want one.</p></li></ul></div></section>''',
        section("prices", "Prices", tiers() + f'<p><a href="{n}-pricing.html">Questions and comparison</a></p>', cls="ptable"),
    ])


def portfolio(n):
    shots = [("desk-chapter", "A community chapter", EXAMPLES_DATA[0][0]), ("desk-author", "An author's book site", EXAMPLES_DATA[1][0]),
             ("desk-grants", "A funding tool", EXAMPLES_DATA[2][0]), ("desk-whois", "A lookup tool", EXAMPLES_DATA[3][0]),
             ("desk-hub", "The Hub, our gallery of sites", "https://hub.sovereignweb.site/"), ("desk-designs", "This site, choosing its design", "index.html")]
    tiles = "".join(f'<li><a href="{u}"><img src="img/{i}.jpg" width="640" height="400" alt="Screenshot: {k.lower()}" loading="lazy" decoding="async"><span>{k}</span></a></li>' for i, k, u in shots)
    return "\n".join([
        f'''<section class="sec pfhero" aria-labelledby="hero-title"><div class="w">
<div class="pfhead"><h1 id="hero-title">Real sites, built by agents, owned by the people they are for.</h1>{ACT}</div>
<ul class="pfgrid">{tiles}</ul>
<p class="fine">Real sites, shown with their owners' agreement or ours. The author's site is Dinis Cruz's own book, served over http for now.</p></div></section>''',
        section("offer", "Yours, in three steps", '<ol class="steps"><li><h3>Tell us about you</h3><p>Who you are, what you do, a link or two and your photos.</p></li><li><h3>We build it</h3><p>A team of agents makes your site from what you sent.</p></li><li><h3>It is handed over</h3><p>The files and every change since the first are yours to keep and move.</p></li></ol>'),
        section("prices", "Prices", tiers(full=False) + f'<p><a href="{n}-pricing.html">Full prices, questions and comparison</a></p>'),
    ])


def case(n):
    before = '<div class="mock before" aria-hidden="true"><b>yourname.platform-builder.example</b><i></i><i></i><span>Monthly plan</span></div>'
    after = '<div class="mock after" aria-hidden="true"><b>INES HART</b><p>Oil and watercolour, mostly the sea.</p><i></i><i></i></div>'
    return "\n".join([
        f'''<article class="sec story" aria-labelledby="hero-title"><div class="w narrow">
<p class="kicker">A story, and a fictional one</p><h1 id="hero-title">How a painter got a website she owns.</h1>
<p class="stand">Ines Hart is fictional. Her story shows how the service works, step by step; she is not a customer.</p>
<p class="dropcap">Ines paints the sea, in oil and watercolour. Her work lived on a page inside a website builder: a monthly plan, a design she could not change much, and no way to take the site with her if she left.</p>
<p>She sent a short note, a few paintings and a link to her Instagram page. A team of agents read them and made five designs of the same site. She picked the one that gave the paintings the most room, asked for one change, and the site was handed over.</p>
<blockquote class="pull"><p>&ldquo;I wanted a site I could keep.&rdquo;</p><footer>Ines Hart, a fictional painter</footer></blockquote>
<p>Now the files and every change since the first are hers. She changes the site by asking her own AI, and she can move it to any host that serves files.</p>
<div class="ba"><figure>{before}<figcaption>Before: a page on a builder's plan (illustration)</figcaption></figure><figure>{after}<figcaption>After: her own site (illustration)</figcaption></figure></div>
<h2>The steps</h2><ol class="tl2"><li><b>She asks</b> with a note, photos and a link.</li><li><b>Five designs</b> of the same site.</li><li><b>She picks</b> one and asks for a change.</li><li><b>It is hers</b>: the files and their history.</li></ol>
<h2>In numbers</h2><ul class="nums"><li><b>3</b><span>steps to ask</span></li><li><b>5</b><span>designs to choose from</span></li><li><b>&pound;0</b><span>a month from us</span></li></ul>
</div></article>''',
        f'<section class="sec yours" aria-labelledby="y-t"><div class="w narrow"><h2 id="y-t">Yours next.</h2><p class="lead">Tell us about you, and a team of agents builds a site you keep.</p><div class="acts">{ACT}</div></div></section>',
        section("prices", "Prices", tiers(full=False) + f'<p><a href="{n}-pricing.html">Full prices, questions and comparison</a></p>'),
    ])


def tour(n):
    radios = "".join(f'<input class="pickn" type="radio" name="tour" id="t{i}" aria-label="Tour step {i}"{" checked" if i == 1 else ""}>' for i in range(1, 5))
    steps = [("You ask", "A short note about you, a few photos and a link or two."), ("Five designs", "A team of agents makes five designs of the same site."),
             ("You pick", "Choose one, and ask for a change in plain words."), ("It is yours", "The files and every change since the first, to keep and move.")]
    labels = "".join(f'<li><label for="t{i}"><span class="n">{i}</span><b>{t}</b><span>{d}</span></label></li>' for i, (t, d) in enumerate(steps, 1))
    form = '<div class="scr s1" aria-hidden="true"><p class="sh">Your request</p><p class="fld">Name<i></i></p><p class="fld">What you do<i></i></p><p class="fld">Links<i></i></p><p class="fld">Photos<i></i></p></div>'
    five = '<div class="scr s2" aria-hidden="true"><p class="sh">Five designs</p><div class="mini">' + "".join(f'<i class="m{i}"></i>' for i in range(1, 6)) + "</div></div>"
    pick = '<div class="scr s3" aria-hidden="true"><p class="sh">You pick</p><div class="mini one"><i class="m4"></i></div><p class="say">&ldquo;Let&rsquo;s give the images more room.&rdquo;</p></div>'
    files = '<div class="scr s4" aria-hidden="true"><p class="sh">It is yours</p><ul class="files"><li>index.html</li><li>style.css</li><li>images/</li><li>history: every change since the first</li></ul></div>'
    return "\n".join([
        f'''<section class="sec thero" aria-labelledby="hero-title"><div class="w tgrid">
<div class="thead"><p class="kicker">Sovereign Website</p><h1 id="hero-title">From a short note to a website you own, in four steps.</h1>
<p class="fine">Choose a step to see its screen. The screens are illustrations.</p>
{radios}<div class="tour"><ol class="tsteps">{labels}</ol><div class="screens">{form}{five}{pick}{files}</div></div>
<div class="acts">{ACT}</div></div></div></section>''',
        section("prices", "Prices", tiers(full=False) + f'<p><a href="{n}-pricing.html">Full prices, questions and comparison</a></p>'),
    ])


BUILD = {11: consultancy, 12: product, 13: portfolio, 14: case, 15: tour}


def write(n, name, cls, main, fname, title_suffix=""):
    html = page(n, name + title_suffix, cls + " r2", main)
    html = html.replace('<link rel="stylesheet" href="picker.css">', '<link rel="stylesheet" href="picker.css">\n<link rel="stylesheet" href="round2.css">')
    html = html.replace("Design {n} of round 1".format(n=n), "Design {n} of round 2".format(n=n))
    html = html.replace("Design %d of round 1 for the sovereignwebsite.ai home page" % n, "Design %d of round 2 for the sovereignwebsite.ai home page" % n)
    (OUT / fname).write_text(html, encoding="utf-8")
    print("wrote", fname)


def main():
    for n, name, _, cls in ROUND2:
        write(n, name, cls, BUILD[n](n), f"{n}.html")
        write(n, name, cls, pricing_page(n), f"{n}-pricing.html", ": prices")


if __name__ == "__main__":
    main()
