---
type: fact
description: "restricted/ now syncs via git-crypt — tracked encrypted in the public repo, key at ~/.git-crypt-keys/rhoai-agentic-hub.key; a locked checkout shows \\0GITCRYPT headers, misleading missing-var doctor warnings, and bashrc parse noise; fix = git-crypt unlock (doctor detects since dde6574)"
timestamp: 2026-07-16
status: current
---
Resolves backlog #14 (restricted/ cross-machine sync): the answer was
**git-crypt**, not a private mirror. `restricted/**` is tracked in the
public repo as git-crypt ciphertext (`.gitattributes`:
`restricted/** filter=git-crypt`), with `restricted/.env.example`
filter-excluded so it stays readable as the tracked template. The symmetric
key lives OUTSIDE the repo at `~/.git-crypt-keys/rhoai-agentic-hub.key`
(override: `GIT_CRYPT_KEY`). Transcripts stay local everywhere —
`**/transcripts/` is globally gitignored, so `work/transcripts/` never
syncs, by design.

## The locked-checkout failure mode (hit on machine B, 2026-07-16)

A clone that was never `git-crypt unlock`ed looks broken in confusing ways:

- every tracked restricted file starts with the `\0GITCRYPT` magic header
  (diagnose with `head -c 9 <file> | od -c`);
- `restricted/.env` is ciphertext, so the doctor printed misleading
  per-var warnings (JIRA_*/SLACK_* "missing") and `~/.bashrc` spewed a
  binary parse error on EVERY shell invocation;
- doctor section 11 falsely reported "unlocked" because it sampled the
  first `.md` found — an untracked hand-copied plaintext file from the
  pre-git-crypt era.

**Fix**: `git-crypt unlock ~/.git-crypt-keys/rhoai-agentic-hub.key`
(requires a fully clean worktree — even a modified generated index blocks
it). Unlock also writes the smudge/clean filters into local git config with
`required=true`; without that local config, `git add` on a restricted file
would stage PLAINTEXT into the public repo — which is why doctor treats a
missing filter as locked.

Since commit dde6574 the doctor detects both halves: section 4 FAILs loud
on a ciphertext `.env` with the unlock command, and section 11 samples a
TRACKED file + checks the filter config.

Related: [[fact-mcp-tokens-baked-into-claude-config]],
[[fact-doctor-owns-shell-env-wiring]],
[[fact-concurrent-session-git-hygiene]].
