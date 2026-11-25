<!-- Code Apache-2.0, text CC BY 4.0; adapted from an open-source implementation -->
# ABP starter kit: install

An Agent Behaviour Policy (ABP) for every Claude Code agent: deny by default, one grant per agent, restored into context at every start and compaction, every tool call decided and logged. Node 18+, no dependencies.

## 0. What the hook is, and is not

**The hook is a guardrail and an audit log, not a security boundary.** It reads the text of each tool call, so anything that runs code can get past it: `bash -c`, `python -c`, `node -e`, a script written and then run, an alias. It keeps an honest agent on its grant and records what every agent tried; it does not stop an agent set on getting round it. The hard boundaries are elsewhere, and come first:

- a separate claude.ai account for the agents, with no connectors (see Connectors below);
- repository permissions: each agent's credentials reach only the repositories it works in;
- branch protection on `main` (and on any branch only a person merges);
- a signed-commit check in CI, against the agents' published keys.

## 1. Copy the files into `<your-repo>`

| Kit file | Goes to |
|---|---|
| `settings.json` | `.claude/settings.json` (merge its `hooks` if you have one) |
| `abp-hook.mjs` | `.claude/hooks/abp.mjs` |
| `abp-tools.mjs` | `abp/tools.mjs` |
| `policies.template.json` | `abp/policies.json` |
| `run-report.schema.json` | `abp/run-report.schema.json` |

Replace the placeholders `<owner>`, `<your-team>`, `<your-repo>` and `<date>`. Commit, and let only the abp agent change `.claude/` and `abp/` from then on (they are protected paths).

## 2. Name your agents

Each agent is a role in `roles`: its focus, the paths it writes, any hosts it sends to, `subagents`, `notify_owner` and the exact `connectors` tools it may use. A dotted name (`dev.search`) with no entry of its own is a worker: its base role's paths only, pushing to `work/dev.search`. The hook knows who a session is from `ABP_ROLE`, or else from the one key label `<role>@<your-team>` in `~/.abp/keys/*/metadata.json`. No label, or two, is unidentified: the core rules hold, and it may write nothing (in observe mode its writes, commits and pushes are logged as attempts; in enforce mode they are blocked).

## 3. Generate each agent's ABP

`node abp/tools.mjs build` writes `abp/<role>.md` for every role; commit them. The SessionStart hook prints the agent's own file back into its context at startup, resume, clear and compact, so a compaction cannot summarise the policy away.

## 4. Start in observe mode

With `"mode": "observe"` a call outside the grant is logged as `observe` and allowed. Pushes are checked for the branch (`git.push_branch`), the remote (`git.remote`, normally `origin`; a role may add `push_remotes`) and that remote's push URL (`git.remote_url`); changing a remote is denied. Run for a few days, read `~/.abp/log/*.jsonl` and the run reports, and widen the grants that are too tight (the owner decides each relaxation; the abp agent proposes them in `proposed_relaxations`, with the evidence).

## 5. Switch breakers on

A breaker blocks one rule even in observe mode: `"breakers": {"rules": {"R5": {"on": true, "since": "...", "why": "...", "by": "<owner>"}}}`. R3 (connectors) ships on. Add others as calibration allows; `"mode": "enforce"` blocks every denial and comes last.

## 6. Run reports

Every agent, before the last commit of a run: `node abp/tools.mjs run-report --line "what this run did"`. It writes `abp/runs/<role>/<run>.json` (schema in `abp/run-report.schema.json`): requests, tool calls by kind, rules executed, attempts outside the grant, and breaches: a commit outside the grant, a compaction not re-anchored, a hook that failed.

A run report never publishes what the owner typed. Each prompt, and each command, path or URL a tool call targeted, is logged and reported as its length and a hash keyed by a per-machine salt (`~/.abp/salt`, made on first use, never committed or read into a conversation), so the owner can match an entry against the local log without the report revealing it. Text is an opt-in that takes two keys: the owner sets `"logging": {"include_text": true}` in the policy, and the agent passes `--include-text`; even then it is redacted (keys, tokens, email addresses) and cut to 240 characters. Keep it off in any public repository.

## 7. The abp agent's hourly review

Every hour the abp agent runs `node abp/tools.mjs report` (the run reports, and every commit's files against its author's grant, as JSON) and writes it up in `abp/reports/<date>-<hour>.md`: breaches, attempts, missing run reports, relaxations proposed. It tightens; the owner relaxes.

## Connectors: keep agents away from your own accounts

- On Claude Code on the web, the connectors (mail, drive, calendar, docs) of the claude.ai account that starts a session attach to that session. An agent started from your account can reach your accounts.
- Run agents on a separate claude.ai account with no connectors. This is a hard boundary; the hooks are policy.
- Block `mcp__` tools by default with the R3 breaker on: only `tools.mcp_allowed` and a role's `connectors` pass; session tools (new sessions, schedules) are denied too.
- For Google, sign in in the browser as an agent account of its own, never through a person's connector.

## What the hooks cannot see

What a script does once started (`bash -c`, `python -c` and the like); shell writes outside the protected paths (caught after the fact by the commit check); a session that does not load this repository's settings; who is really behind a key label.

If the policy cannot be loaded, or the hook fails on a call, it fails closed: only Read, Grep and Glob (and the like) pass; every write, shell command, push, send, connector and sub-agent is blocked. Either way it logs `hook-error`, counted as a breach. The owner fixes `abp/policies.json` to recover. If Node itself is missing, Claude Code runs the tool anyway: that is why the hard boundaries in section 0 come first.
