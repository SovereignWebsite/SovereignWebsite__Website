#!/usr/bin/env python3
"""Builds the Agent Behaviour Policy starter kit pages: site/abp/index.html (the guide) and site/abp/kit/index.html (the files).
Asked for by Dinis Cruz, 25 Nov 2026 (relayed by a.maestro). Live and growing: the files are listed as they arrive.
Run from the repository root: python3 tools/build_abp.py. True statements only; no names, keys or session links in the templates."""
import sys
import hashlib
from html import escape
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_designs import header, footer  # noqa: E402

SITE = Path(__file__).resolve().parent.parent / "site"
GH = "https://github.com/PrompTugal/PrompTugal__News__Website/blob/dev/"
GH_TREE = "https://github.com/PrompTugal/PrompTugal__News__Website/tree/dev/"
RM = "https://riskmandate.ai/"

ABP_AGENT = """You are the ABP agent for this repository. You own the agent behaviour policies and the hooks that enforce them.

- The policies live in one file in this repository. Every agent gets the core rules; anything not granted to an agent is denied.
- Keep the hooks wired: the policy is read again at the start of every session (startup, resume, clear and compact), and every tool call is checked before it runs. Run in observe mode: record what happens, and block only where a rule's breaker is on.
- Generate one behaviour policy per agent from the policy file, and keep them current.
- After each run, write a run report in the agreed schema.
- Every hour, review the run reports and tighten any grant that allowed more than the work needed.
- When a rule seems too tight, write a proposal for the owner, with the evidence. Never relax a policy yourself.
- Never print, store or commit a key, a token or private data."""

SECURITY_AGENT = """You are the security agent for this repository.

- Before work starts, review the plan for risk. After it is done, review the result.
- Review every commit for keys, tokens, contact details and private data.
- When you find a problem, raise a hold on that work and say why, with the evidence.
- Never fix another agent's paths yourself: report to the agent that owns them.
- Never lift a hold yourself: the owner does.
- Never print or copy a secret you find; say where it is, and that it must be rotated."""

KIT = [
    ("INSTALL.md", None, "Install guide", "The seven steps, the connectors advice and what the hooks cannot see. Start here."),
    ("policies.template.json", "abp/policies.json", "policies.json template", "The core rules, deny by default, the R3 connectors breaker on, and example grants for an abp agent, a security agent and a dev agent."),
    ("settings.json", ".claude/settings.json", "Hook wiring", "SessionStart (startup, resume, clear, compact), UserPromptSubmit, PreToolUse and PreCompact."),
    ("abp-hook.mjs", ".claude/hooks/abp.mjs", "The hook", "Re-anchors each agent's ABP at every start and compaction; decides and logs every tool call, in observe mode, blocking only where a rule's breaker is on."),
    ("abp-tools.mjs", "abp/tools.mjs", "Build and report command", "build: one ABP per agent; run-report: each run's report; report: the hourly review."),
    ("run-report.schema.json", "abp/run-report.schema.json", "Run-report schema", "What every run records, so the hourly review has something to read."),
]
LIVE = [
    ("board/abp/README.md", "How the team's policies work", GH),
    ("board/abp/policies.json", "The full policy file (one team, many agents)", GH),
    ("board/abp/security.md", "A generated behaviour policy, for the security agent", GH),
    ("board/abp/reports/", "The hourly reviews", GH_TREE),
    ("board/runs/", "Run reports", GH_TREE),
    ("board/team/security/ROLE.md", "The security agent's role", GH),
    (".claude/settings.json", "The hook wiring", GH),
]
CASES = ["The relayed yes", "A key in a transcript", "An XSS found within the hour", "The email that turned the gate red",
         "A house rule the sub-agent did not know", "Per-session leak-scan allowlists"]

HEAD = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Dinis Cruz">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://sovereignwebsite.ai/{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Sovereign Website">
<meta property="og:locale" content="en_GB">
<meta property="og:image" content="https://sovereignwebsite.ai/abp/og-abp.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Agent Behaviour Policy starter kit: six files for a team of Claude Code agents, free to download.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://sovereignwebsite.ai/abp/og-abp.png">
<link rel="canonical" href="https://sovereignwebsite.ai/{path}">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{up}designs/round.css">
<link rel="stylesheet" href="{up}abp/abp.css">
</head>
<body class="rd abp">
<a class="skip" href="#main">Skip to content</a>
"""


def fix_links(html, up):
    # header() and footer() are written for pages one folder deep (../); adjust for deeper pages
    return html.replace('href="../', f'href="{up}').replace('href="index.html">All designs', f'href="{up}designs/index.html">All designs')


def prompt_block(id_, title, text):
    return (f'<section class="sec" aria-labelledby="{id_}-t"><div class="w"><h2 id="{id_}-t">{title}</h2>'
            f'<p class="fine">Ready to paste as the start of the agent\'s session. Adjust the paths to your repository.</p>'
            f'<pre class="prompt" tabindex="0"><code>{escape(text)}</code></pre></div></section>')


def sha_of(name):
    return hashlib.sha256((SITE / "abp" / "kit" / name).read_bytes()).hexdigest()


def guide():
    kit = "".join(f'<li><h3>{t}</h3><p>{d}</p><p class="fine"><a href="kit/{f}" download>Download {f}</a></p></li>' for f, _, t, d in KIT)
    live = "".join(f'<li><a href="{base}{p}">{escape(p)}</a>: {d}</li>' for p, d, base in LIVE)
    cases = "".join(f"<li>{c}</li>" for c in CASES)
    main = f'''<main id="main">
<section class="sec" aria-labelledby="hero-title"><div class="w">
<p class="kicker">Agent Behaviour Policy</p>
<h1 id="hero-title">A starter kit for agents that keep themselves in bounds.</h1>
<p class="lead">For a team already running Claude Code agents that wants to add two more: an agent that owns the behaviour policies, and a security agent.</p>
<p class="note">Six files, adapted from a team that runs them: <a href="kit/">download the kit</a>, each with its SHA-256 so you can check it. Tested on Node 22 and 24, by the team that wrote it.</p>
</div></section>
<section class="sec" aria-labelledby="what-t"><div class="w"><h2 id="what-t">What an Agent Behaviour Policy is</h2>
<blockquote class="src"><p>&ldquo;An Agent Behaviour Policy describes one AI agent in one deployment: everything it can do (the grant), what you actually authorised (the mandate), the gap between the two (the delta), and what really stands in the way of each thing (the barrier).&rdquo;</p>
<footer>From <a href="{RM}agent-behaviour-policy.html">Agent Behaviour Policies</a>, RiskMandate.</footer></blockquote>
<p>The step above it is a <a href="{RM}licence-to-operate.html">licence to operate</a>: in RiskMandate&rsquo;s words, &ldquo;a named person authorises that policy, for an interval, with conditions and their enforcers.&rdquo;</p></div></section>
<section class="sec" aria-labelledby="kit-t"><div class="w"><h2 id="kit-t">What the kit holds</h2><ul class="kitlist">{kit}</ul>
<p><a href="kit/">The kit page</a> lists every file with where it goes and its SHA-256. Start with INSTALL.md.</p></div></section>
{prompt_block("p1", "Start prompt: the ABP agent", ABP_AGENT)}
{prompt_block("p2", "Start prompt: the security agent", SECURITY_AGENT)}
<section class="sec" id="connectors" aria-labelledby="con-t"><div class="w"><h2 id="con-t">Connectors: keep the agents away from your own accounts</h2>
<p>If you use Claude with connectors such as Gmail, Google Drive or Slack, those connectors belong to your claude.ai account. On Claude Code on the web, the account&rsquo;s connectors are read when a cloud session starts, so agents started on your account can reach your mail, files and messages. Tool permissions for each connector are set for the whole account, at <a href="https://claude.ai/customize/connectors">claude.ai/customize/connectors</a>, not per session or per agent.</p>
<p>What the kit recommends, strongest first:</p>
<ol class="recs">
<li><h3>Separate accounts</h3><p>Run the agents on a separate Claude account with no connectors, such as your team&rsquo;s own agent account, and keep your personal connectors on your own account. This is the only hard boundary.</p></li>
<li><h3>Block connectors in the policy</h3><p>Deny every connector tool by default in policies.json, with that rule&rsquo;s breaker on (blocking) from day one, and allow named tools only. This is defence in depth, not a boundary: it covers only sessions that run the repository&rsquo;s hooks. The live example below has this rule, and its team reports running it in observe mode for now.</p></li>
<li><h3>Sign in to Google in the browser</h3><p>Where a website needs Google, it signs in in the browser as the agent account, through Google&rsquo;s own APIs for Drive and Chat, never through a person&rsquo;s Claude connector.</p></li>
</ol></div></section>
<section class="sec" aria-labelledby="live-t"><div class="w"><h2 id="live-t">A live example</h2>
<p>One team runs this today, in public: the PrompTugal news site&rsquo;s agents. Their files, on GitHub:</p><ul>{live}</ul>
<p class="fine">These links will move to the ABP agent&rsquo;s own site, abp.agents.sovereignweb.site, once it is up.</p></div></section>
<section class="sec" aria-labelledby="why-t"><div class="w"><h2 id="why-t">Why it matters: case studies</h2>
<p>Six published case studies from that team, each a real incident and what the policies did:</p><ul>{cases}</ul>
<p><a href="{GH}board/abp/case-studies/README.md">Read them on GitHub</a>.</p></div></section>
<section class="sec" aria-labelledby="lic-t"><div class="w"><h2 id="lic-t">Licence</h2>
<p>The templates are adapted from the PrompTugal news site&rsquo;s repository, whose code is under Apache-2.0 and whose text is under CC BY 4.0. What is adapted here keeps those licences.</p></div></section>
</main>'''
    return main


def kitpage():
    rows = "".join(f'<tr><th scope="row"><a href="{f}" download>{f}</a></th><td>{t}</td><td>{("<code>" + dst + "</code>") if dst else "read first"}</td><td><code class="sha">{sha_of(f)}</code></td></tr>' for f, dst, t, _ in KIT)
    return f'''<main id="main"><section class="sec" aria-labelledby="hero-title"><div class="w">
<p class="kicker">Agent Behaviour Policy starter kit</p><h1 id="hero-title">The files</h1>
<p class="lead">Six files. Copy each to where it goes, replace the placeholders, then follow <a href="INSTALL.md">INSTALL.md</a>. The <a href="../">guide</a> has the two start prompts and a live example.</p>
<p class="fine swipe">Swipe sideways for more.</p>
<div class="cmpwrap"><table class="cmp kit"><thead><tr><th scope="col">File</th><th scope="col">What it is</th><th scope="col">Goes to</th><th scope="col">SHA-256</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="fine">Check a file with <code>sha256sum &lt;file&gt;</code> (or <code>shasum -a 256</code>). Tested on Node 22 and 24, by the team that wrote it. Code under Apache-2.0, text under CC BY 4.0, adapted from the PrompTugal news site&rsquo;s repository.</p>
</div></section></main>'''


def write(rel, title, desc, main):
    up = "../" * (rel.count("/"))
    html = HEAD.format(title=title, desc=desc, path=rel.replace("index.html", ""), up=up) + fix_links(header(), up) + "\n" + main + "\n" + fix_links(footer(), up) + "\n</body>\n</html>\n"
    out = SITE / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", rel)


def main():
    write("abp/index.html", "Agent Behaviour Policy starter kit: Sovereign Website",
          "A starter kit for a team of Claude Code agents: add an agent that owns the behaviour policies, and a security agent.", guide())
    write("abp/kit/index.html", "The kit files: Agent Behaviour Policy starter kit",
          "The files of the Agent Behaviour Policy starter kit, listed as they are prepared.", kitpage())


if __name__ == "__main__":
    main()
