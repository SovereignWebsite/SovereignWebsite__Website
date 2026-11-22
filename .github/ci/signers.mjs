// Who signed each new commit. Seeded by SovereignWebsite__Factory (incident 2026-11-22__pushed-before-key-published:
// a site went live from commits signed by a key not yet published; nothing refused it).
// Dinis Cruz, 22 Nov 2026, in factory.d's session: "Yes to the sign check. Yes to the org apply to the sites already there."
//
// Usage: node .github/ci/signers.mjs <before> <after>     (a push's range; before all zeros: just <after>)
// For each new commit (merges skipped):
//   - with an Agent: trailer: it must carry a git SSH signature by that agent's live key in the Factory's
//     team/keys.json (fetched from its dev branch now, so a key not yet published fails), and its Claude-Session:
//     must be the session published with that key;
//   - without one: a person's commit (an owner editing on GitHub, or the Factory's own seeding). It must be signed
//     and verified by GitHub (asked through the API with the workflow's token); it is listed in the summary;
//   - "Owner override: <quote>, <where>" in the message lets a commit through that would otherwise fail; it is listed.
// Exit 1 on any refusal, so the deploy that follows does not run. Prints no secret. Needs git and ssh-keygen.
import { execFileSync, spawnSync } from 'node:child_process';
import { writeFileSync, appendFileSync, mkdtempSync, rmSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

export const KEYS_URL = 'https://raw.githubusercontent.com/SovereignWebsite/SovereignWebsite__Factory/dev/team/keys.json';
const AGENT = /^[a-z0-9]+(?:[.-][a-z0-9]+)*@[a-z0-9.-]+$/i;
const live = (k) => k.status !== 'superseded' && k.status !== 'retired';
const lines = (s) => (s ? s.split('\n').map((x) => x.trim()).filter(Boolean) : []);

// keys: the Factory's team/keys.json entries. personVerified(sha): { verified, login } from GitHub, for commits with no Agent:.
export async function checkSigners({ cwd = process.cwd(), before, after, keys, personVerified }) {
  const git = (...a) => execFileSync('git', a, { cwd, encoding: 'utf8' }).trim();
  // A push that creates the branch (before all zeros) checks its whole history; a force push whose old head is gone checks only the new head.
  const known = (r) => { try { git('rev-parse', '--verify', '--quiet', `${r}^{commit}`); return true; } catch { return false; } };
  const range = before && !/^0+$/.test(before) ? (known(before) ? `${before}..${after}` : `${after}^!`) : after;
  const commits = lines(git('rev-list', '--no-merges', range));
  const dir = mkdtempSync(join(tmpdir(), 'signers-'));
  try {
    const signers = [], sessionOf = new Map();
    for (const k of keys.filter(live)) {
      const pem = k.bundle?.sign ?? k.public_key?.sign;
      if (!k.agent || !AGENT.test(k.agent) || !pem) continue;
      try {
        const f = join(dir, `${signers.length}.pem`); writeFileSync(f, pem);
        const ssh = execFileSync('ssh-keygen', ['-i', '-m', 'PKCS8', '-f', f], { encoding: 'utf8' }).trim().split(' ').slice(0, 2).join(' ');
        signers.push(`${k.agent} namespaces="git" ${ssh}`);
        if (!sessionOf.has(k.agent)) sessionOf.set(k.agent, new Set());
        if (k.session) sessionOf.get(k.agent).add(k.session);
      } catch { /* an unreadable key verifies nothing */ }
    }
    const allowed = join(dir, 'allowed_signers'); writeFileSync(allowed, signers.join('\n') + '\n');
    const ok = [], people = [], overrides = [], refused = [];
    for (const c of commits) {
      const short = c.slice(0, 7), subject = git('log', '-1', '--format=%s', c), body = git('log', '-1', '--format=%B', c);
      const agents = lines(git('log', '-1', '--format=%(trailers:key=Agent,valueonly)', c));
      const sessions = lines(git('log', '-1', '--format=%(trailers:key=Claude-Session,valueonly)', c));
      const override = (body.match(/^Owner override:\s*(.+)$/m) || [])[1];
      let why = null;
      if (agents.length) {
        const v = spawnSync('git', ['-c', 'gpg.format=ssh', '-c', 'gpg.ssh.program=ssh-keygen', '-c', `gpg.ssh.allowedSignersFile=${allowed}`, 'verify-commit', c], { cwd, encoding: 'utf8' });
        const principal = (`${v.stdout}\n${v.stderr}`.match(/Good "git" signature for (\S+)/) || [])[1];
        if (v.status !== 0) why = `Agent: ${agents.join(', ')}, but not signed by a key published in the Factory's team/keys.json`;
        else if (agents.length !== 1 || agents[0] !== principal) why = `signed by ${principal}, Agent: ${agents.join(', ')}`;
        else if (sessions.length !== 1 || !(sessionOf.get(principal) || new Set()).has(sessions[0])) why = `Claude-Session: missing or not the session published with ${principal}'s key`;
        else { ok.push(`${short} ${principal}`); continue; }
      } else {
        const p = await personVerified(c);
        if (p?.verified) { people.push(`${short} by ${p.login || 'unknown'}: ${subject}`); continue; }
        why = 'no Agent: trailer and not a commit GitHub verified';
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
  if (r.refused.length) l.push('\nNot deployed. Publish the agent\'s key in the Factory first (team/keys.json), or record the owner\'s override in the commit message: "Owner override: <their words>, <where>".');
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
      return { verified: j.commit?.verification?.verified === true, login: j.author?.login || j.commit?.author?.name };
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
