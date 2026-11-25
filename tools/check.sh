#!/usr/bin/env bash
# Run before every push: serves site/ locally and runs tools/check.mjs (axe, sideways scroll, picker, links, em dashes).
# Installs @axe-core/playwright@4.10.1 into a temporary folder; uses the Playwright already on the machine.
set -euo pipefail
cd "$(dirname "$0")/.."
AX=/tmp/sws-axe; if [ ! -d "$AX/node_modules/@axe-core/playwright" ]; then mkdir -p "$AX"; (cd "$AX" && npm init -y >/dev/null && npm install --silent @axe-core/playwright@4.10.1); fi
PORT=${PORT:-8765}; python3 -m http.server "$PORT" -d site >/dev/null 2>&1 & SRV=$!; trap "kill $SRV 2>/dev/null" EXIT; sleep 1
AXE_PATH="$AX/node_modules/@axe-core/playwright/dist/index.mjs" PORT=$PORT node tools/check.mjs
