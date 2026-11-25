#!/usr/bin/env node
// Code Apache-2.0, text CC BY 4.0; adapted from an open-source implementation.
// The ABP tools (abp/tools.mjs), Node 18+, no dependencies; they reuse the hook's own decisions.
//   node abp/tools.mjs build                      abp/<role>.md for every role, from abp/policies.json
//   node abp/tools.mjs run-report [--line "..."] [--include-text]  abp/runs/<role>/<run>.json from ~/.abp/log/ and this run's commits;
//     prompts and denied targets as length and keyed hash only, unless the policy logs text and --include-text asks for it (redacted)
//   node abp/tools.mjs report [--since ISO]       the abp agent's hourly review: runs, attempts, breaches, commits outside a grant
import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path'; import { execFileSync } from 'node:child_process'
import { ROOT, ABP, LOG, loadPolicy, whoAmI, grantOf, checkWrite } from '../.claude/hooks/abp.mjs'

const P = loadPolicy(), suf = P.identity?.label_suffix || '', now = () => new Date().toISOString()
const arg = (n, d) => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] ?? d : d }
const git = (...a) => { try { return execFileSync('git', a, { cwd: ROOT, encoding: 'utf8', stdio: 'pipe' }) } catch { return '' } }
const inGrant = (who, f) => checkWrite(who, path.join(ROOT, f), P).decision === 'allow'
// commits as [{sha, subject, files: [...]}], newest first
const commits = (...a) => { const out = []; for (const l of git('log', '--format=@@%h|%s', '--name-only', ...a).split('\n'))
  if (l.startsWith('@@')) { const [sha, ...s] = l.slice(2).split('|'); out.push({ sha, subject: s.join('|'), files: [] }) } else if (l) out.at(-1)?.files.push(l)
  return out }

function build() {
  const code = a => a.map(x => '`' + x + '`').join(', ') || 'none'
  for (const [role, r] of Object.entries(P.roles)) {
    const g = grantOf({ role }, P), agent = role + suf
    const also = [g.subagents && 'sub-agents inside its own run', g.notify_owner && 'push notifications to the owner', g.connectors.length && 'connector tools ' + code(g.connectors)].filter(Boolean)
    fs.writeFileSync(path.join(ABP, `${role}.md`), `---
title: "ABP: ${agent}"
policy: abp/policies.json v${P.version} (sha256:${P._sha})
generated: by node abp/tools.mjs build; never edited by hand
---
# ABP: ${agent}

**Mode: ${P.mode || 'enforce'}.** The grant below is your mandate. A call outside it is logged and reviewed every hour; it is blocked when its rule's breaker is on${P.mode === 'enforce' ? ' (and now, in enforce mode, always)' : ''}. Keep to it as if it were enforced. If it is too tight for a good reason, say so in your status asks: the abp agent proposes a relaxation and ${P.operator} decides.

## Mandate (the grant)

- **Focus:** ${r.focus}.
- **Writes (repository):** ${code(g.writes.map(w => w.replace(/\{role\}/g, role)))}.
- **Writes (outside):** ${code(P.common.writes_outside_repo)} (scratch, the hook's log, memory).
- **Sends to:** ${code(g.send)}.
- **Pushes to:** \`${P.git?.push_branch || 'dev'}\` on \`${P.git?.remote || 'origin'}\`${P.git?.remote_url ? ` (\`${P.git.remote_url}\`)` : ''} only${g.push_remotes.length ? ', also to ' + code(g.push_remotes) : ''}; a dotted worker of this role pushes \`work/<name>\` and its work is reviewed.
${also.length ? `- **Also granted:** ${also.join('; ')}.\n` : ''}- **Never:** ${r.never}.

## Outside the mandate (logged; blocked when the rule's breaker is on)

- Any connector (mcp__ tools) not granted above (R3); new sessions, schedules, wake-ups, environments, workflows (R4).
- Pushing anywhere but \`${P.git?.push_branch || 'dev'}\` on its remote, force-push, deletion, tags, history rewrites, empty commits (R5).
- Writing outside the paths above, or to a protected path: ${P.common.protected.map(p => '`' + p.glob + '`' + (p.owner ? ` (${p.owner})` : '')).join(', ')} (R6).
- Sending anything to a host not listed; GitHub writes (R7). Printing the environment or reading a key (R8). Committing under another name (R9).

## Core rules (every agent)

${P.core.map(c => `- **${c.id}** ${c.rule} *(${c.barrier === 'hook' ? 'held by a hook' : c.barrier === 'review' ? 'checked every hour' : 'a rule, re-anchored at every compaction'})*`).join('\n')}

## Licence to operate

| | |
|---|---|
| Authority and accountable owner | ${P.operator} |
| Licensee | ${agent} (its Claude Code session and its session key) |
| Conditions | this ABP; the repository's CLAUDE.md; its role file |
| Validity | for the session's life, while its run reports are filed |
| Review | every hour by the ${P.kept_by} agent; on any change to its reach |
`)
  }
  console.log(`abp build: ${Object.keys(P.roles).length} ABPs from policy v${P.version} (sha256:${P._sha})`)
}

function runReport() {
  const who = arg('--role') ? { role: arg('--role'), agent: arg('--role') + suf, how: '--role' } : whoAmI(P)
  if (!who.role) { console.error(`abp run-report: this session is unidentified (${who.how}); pass --role`); return process.exitCode = 1 }
  const stF = path.join(os.homedir(), '.abp/state.json'); let st = {}; try { st = JSON.parse(fs.readFileSync(stF, 'utf8')) } catch {}
  const evs = []
  try { for (const f of fs.readdirSync(LOG)) for (const l of fs.readFileSync(path.join(LOG, f), 'utf8').split('\n')) try {
    const e = JSON.parse(l); if (e.t > (st[who.role] || '') && (!e.agent || e.agent === who.agent)) evs.push({ ...e, s: f }) } catch {} } catch {}
  evs.sort((a, b) => a.t < b.t ? -1 : 1)
  const ev = k => evs.filter(e => e.ev === k), tools = ev('tool'), att = tools.filter(e => e.decision !== 'allow'), cnt = (o, k) => { if (k) o[k] = (o[k] || 0) + 1; return o }
  const started = evs[0]?.t || st[who.role] || now(), ended = now(), breaches = []
  const mine = commits(`--since=${started}`, '-n', '200').filter(c => c.subject.startsWith(who.agent + ':'))
  for (const c of mine) for (const f of c.files) if (!inGrant(who, f)) breaches.push({ kind: 'write-outside-grant', what: `${c.sha} wrote ${f}`, rule: 'R6' })
  const comp = ev('compact').length, re = ev('session-start').filter(e => e.source === 'compact').length
  if (re < comp) breaches.push({ kind: 'not-re-anchored', what: `${comp} compaction(s), ${re} re-anchor(s): the policy may have been lost`, rule: 'R1' })
  for (const e of ev('hook-error')) breaches.push({ kind: 'hook-error', what: `the hook failed (${e.blocked ? 'closed' : 'open'}) on ${e.tool || e.mode}: ${e.error}`, rule: 'R2' })
  const run = started.replace(/:/g, '-').replace(/\.\d+/, ''), rq = ev('prompt'), inm = tools.length - att.length
  const TX = process.argv.includes('--include-text') && P.logging?.include_text === true   // two keys: the owner's policy and this flag
  if (process.argv.includes('--include-text') && !TX) console.error('abp run-report: the policy does not log text (logging.include_text); lengths and hashes only')
  const rep = { $schema: '../../run-report.schema.json', agent: who.agent, run, started, ended, line: arg('--line', ''), policy: { version: P.version, sha256: P._sha },
    text_included: TX, sessions: new Set(evs.map(e => e.s)).size, requests: rq.map(e => ({ t: e.t, chars: e.chars, sha256: e.sha, ...TX && { head: e.head } })),
    session_events: ev('session-start').map(e => ({ t: e.t, source: e.source || 'unknown' })), compactions: { count: comp, re_anchored: re },
    tool_calls: { total: tools.length, by_kind: tools.reduce((o, e) => cnt(o, e.kind || e.tool), {}) },
    policies_executed: tools.reduce((o, e) => cnt(o, e.rule), {}), policies_instrumented: P.core.filter(c => c.barrier === 'hook').map(c => c.id),
    mandate: { actions: inm, commits: mine.map(c => ({ sha: c.sha, subject: c.subject.slice(0, 160), files: c.files.length })) },
    reach: { attempts: att.length, blocked: att.filter(e => e.decision === 'deny').length, observed: att.filter(e => e.decision === 'observe').length,
      denied: att.map(e => ({ t: e.t, tool: e.tool, rule: e.rule, kind: e.kind, target_chars: e.target_chars, target_sha256: e.target_sha, ...TX && { what: e.reason, target: e.target } })) },
    breaches, counts: { requests: rq.length, tool_calls: tools.length, in_mandate: inm, out_of_mandate: att.length, attempts: att.length, breaches: breaches.length } }
  const dir = path.join(ABP, 'runs', who.role); fs.mkdirSync(dir, { recursive: true }); fs.writeFileSync(path.join(dir, `${run}.json`), JSON.stringify(rep, null, 1) + '\n')
  st[who.role] = ended; fs.mkdirSync(path.dirname(stF), { recursive: true }); fs.writeFileSync(stF, JSON.stringify(st))
  console.log(`abp run-report: abp/runs/${who.role}/${run}.json: ${tools.length} tool calls, ${inm} in mandate, ${att.length} attempts, ${breaches.length} breaches`)
}

function report() {
  const since = arg('--since', new Date(Date.now() - 3600e3).toISOString()), findings = [], runs = [], agents = {}
  const dir = path.join(ABP, 'runs')
  for (const r of fs.existsSync(dir) ? fs.readdirSync(dir) : []) for (const f of fs.readdirSync(path.join(dir, r))) try {
    const j = JSON.parse(fs.readFileSync(path.join(dir, r, f), 'utf8')); if (j.ended >= since) runs.push(j) } catch {}
  for (const c of commits(`--since=${since}`)) {
    const m = new RegExp(`^([a-z][a-z0-9.-]*)${suf.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}:`).exec(c.subject)
    if (!m) { findings.push({ sev: 'attempt', what: `${c.sha} names no agent in its subject` }); continue }
    const who = { role: m[1], agent: m[1] + suf }, a = agents[who.agent] ||= { commits: 0, outside: [] }
    a.commits++; for (const f of c.files) if (!inGrant(who, f)) a.outside.push(`${c.sha} ${f}`)
  }
  const reported = new Set(runs.map(r => r.agent))
  for (const [agent, a] of Object.entries(agents)) {
    if (a.outside.length) findings.push({ sev: 'breach', what: `${agent}: ${a.outside.length} file(s) outside its grant: ${a.outside.slice(0, 6).join(', ')}` })
    if (!reported.has(agent)) findings.push({ sev: 'breach', what: `${agent}: ${a.commits} commit(s) and no run report (R10)` })
  }
  for (const r of runs) for (const b of r.breaches || []) findings.push({ sev: 'breach', what: `${r.agent} (run ${r.run}): ${b.what}` })
  const sum = k => runs.reduce((n, r) => n + (r.counts?.[k] || 0), 0)
  const out = { since, until: now(), counts: { runs: runs.length, agents_committing: Object.keys(agents).length, in_mandate: sum('in_mandate'), attempts: sum('attempts'), breaches: findings.filter(f => f.sev === 'breach').length },
    findings, attempts: runs.flatMap(r => (r.reach?.denied || []).map(d => ({ agent: r.agent, ...d }))) }
  console.log(JSON.stringify(out, null, 1))
}

const cmd = process.argv[2]
if (cmd === 'build') build(); else if (cmd === 'run-report') runReport(); else if (cmd === 'report') report()
else { console.error('usage: node abp/tools.mjs build | run-report [--line "..."] [--role R] [--include-text] | report [--since ISO]'); process.exitCode = 2 }
