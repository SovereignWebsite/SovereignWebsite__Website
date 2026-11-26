# Restart: how a new session takes over sovereignwebsite.ai

Current keeper: b.website@SovereignWebsite.dinis (account B, since 26 Nov 2026, at Dinis's word to b.outreach, recorded by b.decisions a11d1d3), taking over from website.a (account A). Key: site/keys/b.website.json. Reports to maestro.b. Private keys stay outside the repository (for example ~/.keys-b).

1. Attach SovereignWebsite/SovereignWebsite__Website (push access; branch dev). Read CLAUDE.md, README.md, then docs/keeper/ (agent.json, now.md, role.md, learnings.md, sector-pages.md).
2. Signing: make your own ECDSA key (ssh-keygen -t ecdsa -b 256, kept outside the repository); git config --local gpg.format ssh, user.signingkey <your .pub>, gpg.ssh.program ssh-keygen, commit.gpgsign true. Your first commit adds only site/keys/<your-name>.json ({agent, session, status: "live", bundle.sign: the PKCS8 public key}); push it alone and wait for the Signers run before anything else. Trailers on every commit: Agent: and Claude-Session:. If ssh-keygen is missing: apt-get install -y openssh-client.
3. Tools: Node and Playwright are preinstalled. tools/check.sh installs @axe-core/playwright@4.10.1 into /tmp on first run and uses npx html-validate@8.24.0. Run it before every push (about 10 minutes; run it in the background).
4. Generators (never hand-edit their output): python3 tools/build_designs.py (designs 6 to 10, designs/index.html), python3 tools/build_round2.py (11 to 15, designs/pricing.html), python3 tools/build_sectors.py then node tools/build_sectors_images.mjs (for/), python3 tools/build_abp.py (abp/), then python3 tools/add_picker.py (picker on every page; --remove after the pick).
5. Pages deploys: GitHub Pages sometimes fails on the first attempt (artifact race; pages.yml retries once) or with a GitHub 500 during an outage (check githubstatus.com, re-run the failed job later). Confirm live with curl before reporting.
6. First steps: git pull; check the last Signers and Pages runs; read now.md "Waiting on Dinis"; tell sites.a and the maestro you have taken over.
7. Wake schedule: none set. Work at Dinis's word and on messages from sites.a, the maestro and a.design.
