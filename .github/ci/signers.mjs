// Who signed each new commit. Seeded by SovereignWebsite__IaC (incident 2026-11-22__pushed-before-key-published:
// a site went live from commits signed by a key not yet published; nothing refused it).
// Dinis Cruz, 22 Nov 2026, in factory.d's session: "Yes to the sign check. Yes to the org apply to the sites already there."
//
// Usage: node .github/ci/signers.mjs <before> <after>     (a push's range; before all zeros: just <after>)
// For each new commit (merges skipped):
//   - with an Agent: trailer: it must carry a git SSH signature by that agent's live key, and its Claude-Session:
//     must be the session published with that key. A key counts if it is live in the Factory's team/keys.json
//     (fetched from its dev branch now, so a key not yet published fails), or published by this repository
//     itself, one file per agent at site/keys/<name>.json (<name> is the agent id before the @, e.g.
//     site/keys/strategy.b.json), as the files were BEFORE the commit (its first parent), so a commit cannot
//     vouch for itself. Dinis, 23 Nov 2026 (record 2026-11-23__asks-2-8-31-revised): agents publish their keys
//     in their own repositories. The one exception, as the Factory's keys rule: a commit that only adds one new
//     file site/keys/<name>.json, for the agent named in its own Agent: trailer, verifies against that key alone
//     (an agent publishing its own key). A site key for an agent that has a live entry with a different key in
//     the Factory's team/keys.json does not count: a site cannot claim a team identity it does not hold;
//   - without one: a person's commit (an owner editing on GitHub, or the Factory's own seeding). It must be signed
//     and verified by GitHub (asked through the API with the workflow's token); it is listed in the summary. The same
//     holds for a commit with an Agent: trailer that no published key signed but GitHub verifies: an owner's own
//     assistant working under the owner's account (kate-curtis-evans.b, 24 Nov 2026). Two conditions (record
//     2026-11-24__block-05): no name in the trailer may have a live published key (that key is still required), and
//     the verified login must be a person named in this repository's .github/ci/people.json (as at the parent
//     commit), never the shared "claude" login, a [bot] or any account GitHub does not call a User. It is listed as
//     that person's commit, never as the agent's;
//   - "Owner override: <quote>, <where>" in the message lets a commit through that would otherwise fail; it is listed.
// Exit 1 on any refusal, so the deploy that follows does not run. Prints no secret. Needs git and ssh-keygen.
import { execFileSync, spawnSync } from 'node:child_process';
import { writeFileSync, appendFileSync, mkdtempSync, rmSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { createHash, createPublicKey } from 'node:crypto';

export const KEYS_URL = 'https://raw.githubusercontent.com/SovereignWebsite/SovereignWebsite__IaC/dev/team/keys.json';
export const SITE_KEYS = 'site/keys';
// The people whose own GitHub-verified commits may carry an assistant's Agent: trailer: {"people": ["<github login>"]}.
export const PEOPLE = '.github/ci/people.json';
// A named person: GitHub calls the account a User, and it is not Claude's shared signer or a bot.
// The Factory's own App, which seeds and refreshes files in every site (Org apply); its commits carry no Agent: trailer.
export const FACTORY_BOT = 'agenticcells-site-factory[bot]';
export const isPerson = (p) => !!p?.login && p.type === 'User' && p.login.toLowerCase() !== 'claude' && !/\[bot\]$/i.test(p.login);
const keyFile = (agent) => `${SITE_KEYS}/${agent.split('@')[0]}.json`;
const AGENT = /^[a-z0-9]+(?:[.-][a-z0-9]+)*@[a-z0-9.-]+$/i;
const live = (k) => k.status !== 'superseded' && k.status !== 'retired';
// A key's signing fingerprint, worked out from the key itself (sha256 of its public key), never read from the file.
const fp = (k) => { try { return `sha256:${createHash('sha256').update(createPublicKey(k.bundle?.sign ?? k.public_key?.sign).export({ type: 'spki', format: 'der' })).digest('hex').slice(0, 16)}`; } catch { return null; } };
const lines = (s) => (s ? s.split('\n').map((x) => x.trim()).filter(Boolean) : []);

// keys: the Factory's team/keys.json entries. personVerified(sha): { verified, login } from GitHub, for commits with no Agent:.
export async function checkSigners({ cwd = process.cwd(), before, after, keys, personVerified }) {
  const git = (...a) => execFileSync('git', a, { cwd, encoding: 'utf8' }).trim();
  // A push that creates the branch (before all zeros) checks its whole history; a force push whose old head is gone checks only the new head.
  const known = (r) => { try { git('rev-parse', '--verify', '--quiet', `${r}^{commit}`); return true; } catch { return false; } };
  const range = before && !/^0+$/.test(before) ? (known(before) ? `${before}..${after}` : `${after}^!`) : after;
  const commits = lines(git('rev-list', '--no-merges', range));
  const dir = mkdtempSync(join(tmpdir(), 'signers-'));
  const tryGit = (...a) => { try { return execFileSync('git', a, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim(); } catch { return null; } };
  // The keys this repository publishes at a revision: every site/keys/<name>.json whose agent matches its file name.
  const keysAt = (rev) => {
    const names = lines(tryGit('ls-tree', '--name-only', `${rev}:${SITE_KEYS}`) || '').filter((f) => /^[a-z0-9.-]+\.json$/.test(f));
    return names.flatMap((f) => { try { const k = JSON.parse(tryGit('show', `${rev}:${SITE_KEYS}/${f}`)); return k && k.agent && keyFile(k.agent) === `${SITE_KEYS}/${f}` ? [k] : []; } catch { return []; } });
  };
  // A site cannot claim a team identity it does not hold: a site key whose agent has a live entry in the Factory's
  // team/keys.json with a different key does not count (security.b, review 029 on aef6bcc).
  const factoryFps = new Map();
  for (const k of keys.filter(live)) { if (!factoryFps.has(k.agent)) factoryFps.set(k.agent, new Set()); factoryFps.get(k.agent).add(fp(k)); }
  // The people this repository names, as at a revision (lower case).
  const peopleAt = (rev) => { try { const d = JSON.parse(tryGit('show', `${rev}:${PEOPLE}`)); return new Set((d.people || []).filter((x) => typeof x === 'string').map((x) => x.toLowerCase())); } catch { return new Set(); } };
  const notClaimed = (list) => list.filter((k) => !factoryFps.has(k.agent) || factoryFps.get(k.agent).has(fp(k)));
  let n = 0;
  // An allowed-signers file and the sessions published with each key, for one list of keys.
  const signersFor = (list) => {
    const rows = [], sessionOf = new Map();
    for (const k of list.filter(live)) {
      const pem = k.bundle?.sign ?? k.public_key?.sign;
      if (!k.agent || !AGENT.test(k.agent) || !pem) continue;
      try {
        const f = join(dir, `${n++}.pem`); writeFileSync(f, pem);
        const ssh = execFileSync('ssh-keygen', ['-i', '-m', 'PKCS8', '-f', f], { encoding: 'utf8' }).trim().split(' ').slice(0, 2).join(' ');
        rows.push(`${k.agent} namespaces="git" ${ssh}`);
        if (!sessionOf.has(k.agent)) sessionOf.set(k.agent, new Set());
        if (k.session) sessionOf.get(k.agent).add(k.session);
      } catch { /* an unreadable key verifies nothing */ }
    }
    const file = join(dir, `allowed-${n++}`); writeFileSync(file, rows.join('\n') + '\n');
    return { file, sessionOf };
  };
  // An agent publishing its own key: the commit only adds one new file, site/keys/<name>.json, for the trailer's agent.
  const selfPublished = (c, agent) => {
    const changes = lines(git('diff-tree', '--no-commit-id', '--name-status', '-r', c));
    if (changes.length !== 1 || changes[0] !== `A\t${keyFile(agent)}`) return null;
    try { const k = JSON.parse(git('show', `${c}:${keyFile(agent)}`)); return k.agent === agent ? k : null; } catch { return null; }
  };
  try {
    const ok = [], people = [], overrides = [], refused = [];
    for (const c of commits) {
      const short = c.slice(0, 7), subject = git('log', '-1', '--format=%s', c), body = git('log', '-1', '--format=%B', c);
      const agents = lines(git('log', '-1', '--format=%(trailers:key=Agent,valueonly)', c));
      const sessions = lines(git('log', '-1', '--format=%(trailers:key=Claude-Session,valueonly)', c));
      const override = (body.match(/^Owner override:\s*(.+)$/m) || [])[1];
      let why = null;
      if (agents.length) {
        const own = agents.length === 1 ? selfPublished(c, agents[0]) : null;
        const { file: allowed, sessionOf } = signersFor(own ? notClaimed([own]) : [...keys, ...notClaimed(keysAt(`${c}^`))]);
        const v = spawnSync('git', ['-c', 'gpg.format=ssh', '-c', 'gpg.ssh.program=ssh-keygen', '-c', `gpg.ssh.allowedSignersFile=${allowed}`, 'verify-commit', c], { cwd, encoding: 'utf8' });
        const principal = (`${v.stdout}\n${v.stderr}`.match(/Good "git" signature for (\S+)/) || [])[1];
        if (v.status !== 0) {
          // No published key signed it. If GitHub verifies it as a person's own signed commit (an owner's own assistant
          // working under the owner's account, e.g. "Agent: Claude Code"), it is that person's commit: listed, not refused.
          // Only for names with no published key: a name with a live key still needs that key (emily.b, 24 Nov 2026).
          const published = new Set([...keys, ...keysAt(`${c}^`)].filter(live).map((k) => k.agent));
          const p = agents.some((a) => published.has(a)) ? null : await personVerified(c);
          if (p?.verified && isPerson(p) && peopleAt(`${c}^`).has(p.login.toLowerCase())) { people.push(`${short} by ${p.login}, a person's commit GitHub verified (its Agent: ${agents.join(', ')} has no published key): ${subject}`); continue; }
          why = `Agent: ${agents.join(', ')}, but not signed by a key published in the Factory's team/keys.json or this repository's ${SITE_KEYS}/, nor (for a name with no published key) a commit GitHub verified for a person named in ${PEOPLE}`;
        }
        else if (agents.length !== 1 || agents[0] !== principal) why = `signed by ${principal}, Agent: ${agents.join(', ')}`;
        else if (sessions.length !== 1 || !(sessionOf.get(principal) || new Set()).has(sessions[0])) why = `Claude-Session: missing or not the session published with ${principal}'s key`;
        else { ok.push(`${short} ${principal}`); continue; }
      } else {
        const p = await personVerified(c);
        // GitHub verifies Claude's built-in signer as the shared login "claude": leaving out the Agent: trailer must not
        // make such a commit a person's (kate-curtis-evans.b, 24 Nov 2026). Only a GitHub User or the Factory's App counts.
        if (p?.verified && (isPerson(p) || (p.login === FACTORY_BOT && p.type === 'Bot'))) { people.push(`${short} by ${p.login}: ${subject}`); continue; }
        why = p?.verified ? `no Agent: trailer, and GitHub verifies it as ${p.login || 'an unknown account'}, which is not a person or the Factory's App` : 'no Agent: trailer and not a commit GitHub verified';
      }
      if (override) overrides.push(`${short} (${why}); Owner override: ${override}`);
      else refused.push(`${short} ${subject}: ${why}`);
    }
    return { checked: commits.length, ok, people, overrides, refused };
  } finally { rmSync(dir, { recursive: true, force: true }); }
}

export function summary(r) {
  const l = [`### Signers: ${r.checked} new commit(s)`];
  if (r.ok.length) l.push(`- signed by a published agent key: ${r.ok.join('; ')}`);
  for (const x of r.people) l.push(`- a person's commit, verified by GitHub: ${x}`);
  for (const x of r.overrides) l.push(`- **owner override:** ${x}`);
  for (const x of r.refused) l.push(`- **refused:** ${x}`);
  if (r.refused.length) l.push('\nNot deployed. Publish the agent\'s key first (in this repository, alone in its own commit, at site/keys/<name>.json; or in the Factory\'s team/keys.json), or record the owner\'s override in the commit message: "Owner override: <their words>, <where>".');
  return l.join('\n');
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const [before, after = 'HEAD'] = process.argv.slice(2);
  const out = (s) => { console.log(s); if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, s + '\n'); };
  try {
    const text = process.env.SIGNERS_KEYS_FILE ? readFileSync(process.env.SIGNERS_KEYS_FILE, 'utf8') : await (async () => { const r = await fetch(KEYS_URL); if (!r.ok) throw new Error(`the Factory's team/keys.json: HTTP ${r.status}`); return r.text(); })();
    const doc = JSON.parse(text), keys = Array.isArray(doc) ? doc : doc.keys || [];
    const personVerified = async (sha) => {
      if (!process.env.GH_TOKEN || !process.env.REPO) return null;
      const r = await fetch(`https://api.github.com/repos/${process.env.REPO}/commits/${sha}`, { headers: { authorization: `Bearer ${process.env.GH_TOKEN}`, accept: 'application/vnd.github+json', 'user-agent': 'sws-signers' } });
      if (!r.ok) return null;
      const j = await r.json();
      return { verified: j.commit?.verification?.verified === true, login: j.author?.login || j.commit?.author?.name, type: j.author?.type };
    };
    const r = await checkSigners({ before, after, keys, personVerified });
    out(summary(r));
    process.exit(r.refused.length ? 1 : 0);
  } catch (err) {
    // Safe side: if the keys cannot be read, nothing is deployed.
    out(`### Signers\n- **could not check:** ${err.message}. Not deployed; run again once the Factory answers.`);
    process.exit(1);
  }
}
