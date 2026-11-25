#!/usr/bin/env bash
# Run before every push: html-validate, then serves site/ locally and runs tools/check.mjs (share tags, axe, sideways scroll, picker, links, em dashes).
# Installs @axe-core/playwright@4.10.1 into a temporary folder; uses the Playwright already on the machine.
set -euo pipefail
cd "$(dirname "$0")/.."
AX=/tmp/sws-axe; if [ ! -d "$AX/node_modules/@axe-core/playwright" ]; then mkdir -p "$AX"; (cd "$AX" && npm init -y >/dev/null && npm install --silent @axe-core/playwright@4.10.1); fi
echo "html-validate"; npx --yes html-validate@8.24.0 --config tools/htmlvalidate.json "site/**/*.html" 2>&1 | grep -v "npm warn" || true
npx --yes html-validate@8.24.0 --config tools/htmlvalidate.json "site/**/*.html" >/dev/null 2>&1 || { echo "FAIL html-validate"; exit 1; }
PORT=${PORT:-8765}; python3 -m http.server "$PORT" -d site >/dev/null 2>&1 & SRV=$!; trap "kill $SRV 2>/dev/null" EXIT; sleep 1
AXE_PATH="$AX/node_modules/@axe-core/playwright/dist/index.mjs" PORT=$PORT node tools/check.mjs
