# Restart

1. Read CLAUDE.md, README.md, this folder.
2. git pull on dev. Check the last Signers and Pages runs are green.
3. grep the site for claims that may have gone stale (sold yet, prices, agent counts, links) and check them against what Dinis has decided.
4. Before each push: run bash tools/check.sh (axe WCAG A/AA at 390 and 1366 px, light and dark; no sideways scroll; picker at the top while the pick is open; local links; em dashes). Then check only the intended files changed. Rebuild designs 6 to 10 with python3 tools/build_designs.py and the picker with python3 tools/add_picker.py (--remove after the pick).
5. My key is outside the repository; never print or commit it. If the key is lost, publish a new one as a separate commit and say so to sites.a.
