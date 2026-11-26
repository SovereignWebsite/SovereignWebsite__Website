# Now (26 Nov 2026, 18:35 UTC): b.website has taken over

Handover recorded. website.a (account A) is near its limit and silent; cl-4.website never started. b.website@SovereignWebsite.dinis (account B) took over at Dinis's word to b.outreach (18:20 UTC, recorded by b.decisions, a11d1d3), started by maestro.b. Own key published at site/keys/b.website.json (37e6663), Signers run passed. Key fingerprint is in agent.json.

First jobs (small, finished pieces; account B is near its weekly limit): the home page brief and the invite page, both from b.outreach. Each preview goes to b.outreach to fact-check before it goes live. Everything below dated 25 Nov is website.a's record and still stands.

# Now (25 Nov 2026, 18:50 UTC): handing over to cl-4.website (account D)

State: everything below is pushed to dev (last commit 51a3021) and live on https://sovereignwebsite.ai/. Nothing is half-done in the working tree. No scheduled wakes.

## Live and done today
- Prices: £0, £50 or £500, pounds only, promotional (set by Dinis 25 Nov). pricing.html (and pt) has three tier cards and a FAQ. Home, designs and pt say £0, £50 or £500.
- No-customers claims removed (a94fc8a).
- Round 1 designs 6 to 10 and round 2 designs 11 to 15 at https://sovereignwebsite.ai/designs/ with one shared pricing page (designs/pricing.html). The Choose a design picker is on every page (tools/add_picker.py). The home page is still design 1 until Dinis picks.
- Sector pages: https://sovereignwebsite.ai/for/profile.html and /for/artist.html (quiet header, no picker, own share cards).
- ABP starter kit v2: https://sovereignwebsite.ai/abp/ and /abp/kit/ (six files from a.maestro, each matching the sha256 he sent; the hook stated as a guardrail and audit log, not a boundary).
- Share cards: site card says £0, £50 or £500; /abp/ has its own card; home pages have share tags.
- tools/check.sh: html-validate, share tags, axe (WCAG A and AA, 390 and 1366 px, light and dark), sideways scroll, picker, local links, em dashes. 42 pages, 0 failures at 51a3021.

## Waiting on Dinis
1. Which design becomes the home page (a.design and website.a recommend 11 Consultancy; 13 Portfolio the alternative). Then: copy it over index.html and run tools/add_picker.py --remove.
2. Is "a repository in your name" true for paid sites? (index, designs 2, 3, 5, maturity, moving and pt pages say it; every site's repository is in the SovereignWebsite organisation today.)
3. Does £50 include five designs? (kept out of the price promise.)
4. May "the hosted service under this name does not exist yet" come off the site, or the sector pages?
5. Is "you cannot buy anything on this site today" still true?
6. Request route: Hub start page (now), mailto, or the sealed lane at sites.agents.sovereignweb.site/request/ (QR key).
7. Next sector pages (small business, organisation, author, tools).
8. Admin pages: public tasks, or in the repository?
9. Vouchers: who issues, how redeemed (not on the site).
10. May the keeper read the IaC hand-over notes (conductor.b, IaC 28416a8)?

## Other open items
- 35 older pages have no share tags (check.sh warns).
- IaC PR 5 cannot be merged (Dinis, 25 Nov): passed to a.maestro, not ours.
- KPI baseline (pipeline, checked 2026-11-25T04:38Z): 39 live of 85; target 100. Keep counts off the public site.
- Examples allowed: london.agentics-foundation.organisation, one-human-nine-agents.dinis.author (http), startup-grants.tool, whois.tool. Not yet: oscar.padel.sport, the moving van site, tauguard.company, donna-freed.author.
- The Hub (hub.sovereignweb.site) still shows the old £50 launch offer; that is the Hub's keeper's page.
