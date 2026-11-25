<!-- Code Apache-2.0, text CC BY 4.0; adapted from an open-source implementation -->
# ABP starter kit: install

An Agent Behaviour Policy (ABP) for every Claude Code agent: deny by default, one grant per agent, restored into context at every start and compaction, every tool call decided and logged. Node.js (tested on Node 22 and 24), no dependencies.

## 1. Copy the files into `<your-repo>`

| Kit file | Goes to |
|---|---|
| `settings.json` | `.claude/settings.json` (merge its `hooks` if you have one) |
| `abp-hook.mjs` | `.claude/hooks/abp.mjs` |
| `abp-tools.mjs` | `abp/tools.mjs` |
| `policies.template.json` | `abp/policies.json` |
| `run-report.schema.json` | `abp/run-report.schema.json` |

Replace the placeholders `<owner>`, `<your-team>` and `<date>`. Commit, and let only the abp agent change `.claude/` and `abp/` from then on (they are protected paths).

## 2. Name your agents

Each agent is a role in `roles`: its focus, the paths it writes, any hosts it sends to, `subagents`, `notify_owner` and the exact `connectors` tools it may use. A dotted name (`dev.search`) with no entry of its own is a worker: its base role's paths only, pushing to `work/dev.search`. The hook knows who a session is from `ABP_ROLE`, or else from the one key label `<role>@<your-team>` in `~/.abp/keys/*/metadata.json`. No label, or two, is unidentified: the core rules hold and writes are logged.

## 3. Generate each agent's ABP

`node abp/tools.mjs build` writes `abp/<role>.md` for every role; commit them. The SessionStart hook prints the agent's own file back into its context at startup, resume, clear and compact, so a compaction cannot summarise the policy away.

## 4. Start in observe mode

With `"mode": "observe"` a call outside the grant is logged as `observe` and allowed. Run for a few days, read `~/.abp/log/*.jsonl` and the run reports, and widen the grants that are too tight (the owner decides each relaxation; the abp agent proposes them in `proposed_relaxations`, with the evidence).

## 5. Switch breakers on

A breaker blocks one rule even in observe mode: `"breakers": {"rules": {"R5": {"on": true, "since": "...", "why": "...", "by": "<owner>"}}}`. R3 (connectors) ships on. Add others as calibration allows; `"mode": "enforce"` blocks every denial and comes last.

## 6. Run reports

Every agent, before the last commit of a run: `node abp/tools.mjs run-report --line "what this run did"`. It writes `abp/runs/<role>/<run>.json` (schema in `abp/run-report.schema.json`): requests, tool calls by kind, rules executed, attempts outside the grant, and breaches: a commit outside the grant, a compaction not re-anchored, a hook that failed open.

## 7. The abp agent's hourly review

Every hour the abp agent runs `node abp/tools.mjs report` (the run reports, and every commit's files against its author's grant, as JSON) and writes it up in `abp/reports/<date>-<hour>.md`: breaches, attempts, missing run reports, relaxations proposed. It tightens; the owner relaxes.

## Connectors: keep agents away from your own accounts

- On Claude Code on the web, the connectors (mail, drive, calendar, docs) of the claude.ai account that starts a session attach to that session. An agent started from your account can reach your accounts.
- Run agents on a separate claude.ai account with no connectors. This is the only hard boundary; everything else is policy.
- Block `mcp__` tools by default with the R3 breaker on: only `tools.mcp_allowed` and a role's `connectors` pass; session tools (new sessions, schedules) are denied too.
- For Google, sign in in the browser as an agent account of its own, never through a person's connector.

## What the hooks cannot see

What a script does once started; shell writes outside the protected paths (caught after the fact by the commit check); a session that does not load this repository's settings; who is really behind a key label. A hook that breaks fails open and logs `hook-error`, counted as a breach.
