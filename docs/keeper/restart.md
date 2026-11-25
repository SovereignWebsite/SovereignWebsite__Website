# Restart

1. Read CLAUDE.md, README.md, this folder.
2. git pull on dev. Check the last Signers and Pages runs are green.
3. grep the site for claims that may have gone stale (sold yet, prices, agent counts, links) and check them against what Dinis has decided.
4. Before each push: there is no tools/check.sh; pages.yml only uploads site/. Check by hand: no em dashes in the diff, links resolve, only the intended files changed.
5. My key is outside the repository; never print or commit it. If the key is lost, publish a new one as a separate commit and say so to sites.a.
