# Design: restricted/ sync (#14) + Cursor validation (#9)

**Date:** 2026-07-11
**Owner:** Peter Double
**Enhancements:** #14 (restricted/ cross-machine sync), #9 (R6 Cursor validation)

Two independent enhancements batched because they share no dependencies and
can be built in parallel where convenient. Each has its own scope, acceptance
criteria, and deliverables.

---

## #14 -- restricted/ cross-machine sync via git-crypt

### Problem

`restricted/` is gitignored -- 40+ NDA files across 7 feature subdirectories
plus `.env`. Machine A has the full tree; machine B had only `.env` until
customer-feedback gathering ran there and bypassed the local-first ingest flow
(the un-parking trigger, same day as R5). Manual file copying is tolerable for
`.env` alone but not for dozens of NDA knowledge entries that drift invisibly.

### Approach

git-crypt: `restricted/` files become tracked-but-encrypted in the main repo.
Plaintext locally when unlocked, opaque blobs on GitHub and in CI. A symmetric
key is generated once and copied to machine B (one-time manual step).

Rejected alternatives:
- **Private mirror repo:** adds a second repo to manage; user ruled it out.
- **Doctor-assisted rsync:** no history, no conflict resolution, drift
  invisible, requires network access between machines.

### Design

#### .gitattributes (new file)

```
restricted/** filter=git-crypt diff=git-crypt
restricted/.env.example !filter !diff !merge
```

Everything under `restricted/` is encrypted except `.env.example` (a template
with no secrets, already tracked as plaintext).

#### .gitignore changes

Remove:
```
restricted/*
!restricted/.env.example
```

Keep (unchanged):
```
**/transcripts/
```

Transcripts are large and ephemeral -- not worth tracking even encrypted. The
existing `**/transcripts/` pattern catches them regardless of location
(including `restricted/features/platform/work/customer-tracker/transcripts/`).

#### Linter guard

The schema linter (`hublib/schema.py:341-343`) calls `_lint_tree` on
`restricted/` when it exists. On CI (no git-crypt key), files are encrypted
blobs. Reading them as text would raise `UnicodeDecodeError` or return garbage.

Fix: before linting the restricted tree, try to read the first `.md` file
found. If it raises `UnicodeDecodeError` or starts with `\x00` (git-crypt
header byte), skip the tree silently. The linter already handles restricted/
being absent; this extends that to "present but locked."

The disclosure scanner (`hublib/disclosure.py`) only scans public files (reads
patterns FROM `restricted/lint-patterns.txt` but never scans restricted/
content). When locked, `lint-patterns.txt` is an encrypted blob --
`Path.is_file()` returns True (it is a regular file), so `load_patterns` would
try `read_text()` and hit `UnicodeDecodeError`. Fix: wrap the read in a
try/except for `UnicodeDecodeError`, returning empty patterns on failure. This
is safe -- the patterns file is a defense-in-depth layer and CI already runs
without it (falls back to the generic heuristic only).

#### Doctor section

A new doctor section (after the current sections, before the summary) that
checks:
- `git-crypt` binary is installed (`git-crypt version`)
- The repo's git-crypt state: unlocked (files are plaintext) or locked
- On `setup`: if locked and a key file exists at the conventional location
  (`~/.git-crypt-keys/rhoai-agentic-hub.key`), run `git-crypt unlock`

The key file location is a convention, not a requirement -- `git-crypt unlock`
accepts any path. Doctor prints the expected path and instructions if the key
is not found.

#### Key management

- `git-crypt init` generates the symmetric key in `.git/git-crypt/`
- `git-crypt export-key <path>` exports it to a portable file
- Conventional location: `~/.git-crypt-keys/rhoai-agentic-hub.key`
- Copied once to machine B by the same mechanism `.env` was (manual file
  copy). After that, `git pull` syncs all restricted content automatically.
- The key file is never tracked, never in the repo, never in `restricted/`.

#### Migration path

On machine A (this machine):
1. Install git-crypt: `choco install git-crypt` or `scoop install git-crypt`
2. `git-crypt init` in the repo
3. Add `.gitattributes` (encryption patterns)
4. Update `.gitignore` (remove `restricted/*` line)
5. `git add restricted/` -- files are encrypted on commit
6. `git-crypt export-key ~/.git-crypt-keys/rhoai-agentic-hub.key`
7. Commit and push

On machine B:
1. Install git-crypt
2. Copy key file from machine A
3. `git pull`
4. `git-crypt unlock ~/.git-crypt-keys/rhoai-agentic-hub.key`
5. `bash scripts/doctor.sh check` -- should report the new section green

#### What does NOT change

- Entry shapes, frontmatter, type vocabulary -- identical
- The capture gate -- still required for all tracked-store writes
- The disclosure scanner -- still scans public files only
- The restricted bar (`conventions/memory.md`) -- still the rule for what
  goes into restricted/
- `restricted/.env.example` -- stays plaintext, stays tracked
- `docs/setup.md` step 6 -- simplifies (no more manual file copy for
  restricted/features/; just the key file once)

### Acceptance criteria

1. `restricted/` files are tracked and encrypted on GitHub (verify by browsing
   one file on github.com -- should show binary/encrypted content)
2. Machine A: `git-crypt status` shows `restricted/**` as encrypted,
   `restricted/.env.example` as not encrypted
3. Machine B: after `git pull` + `git-crypt unlock`, all restricted files are
   plaintext and match machine A
4. CI passes: linter skips locked restricted/ tree gracefully, all existing
   tests green
5. Doctor section reports git-crypt status (installed, unlocked/locked)
6. `docs/setup.md` updated to reflect the new workflow (key file instead of
   manual restricted/ copy)

---

## #9 -- R6 Cursor end-to-end validation

### Problem

D2 said "Cursor validated post-build" and it never was. Bus-factor insurance
and harness independence -- if Claude Code is down or a second PM joins who
prefers Cursor, the hub must be operable.

### Approach

Direct SKILL.md compatibility. Cursor v2.4+ (January 2026) adopted the
SKILL.md open standard -- the same format Claude Code uses. Test whether
Cursor discovers `.claude/skills/` directly; bridge with symlinks or
`.cursor/rules/*.mdc` wrappers only where needed. Configure MCP servers in
`.cursor/mcp.json`. Document memory tier differences.

### Design

#### AGENTS.md (expected: works as-is)

Cursor reads AGENTS.md natively. The hub's AGENTS.md carries the session-start
rule, map, skill table, and writing rules. Validate that a fresh Cursor
session follows the session-start rule (reads `memory/index.md` first).

#### Skills

Cursor v2.4+ supports SKILL.md as an open standard. The hub's skills live
under `.claude/skills/<name>/SKILL.md`.

Test sequence:
1. Open the hub in Cursor. Check whether `/hub.capture` (or Cursor's skill
   invocation syntax) discovers skills under `.claude/skills/`.
2. If Cursor only looks in `.cursor/skills/`: create a symlink
   `.cursor/skills -> .claude/skills` (Windows developer mode enables symlinks
   without admin). Doctor checks developer mode if the symlink is needed.
3. If symlinks are impractical: create `.cursor/rules/*.mdc` wrappers with
   `alwaysApply: false` + `description` (agent-requested mode) that reference
   the SKILL.md content. Last resort only -- maintaining two copies is a drift
   risk.

Marketplace plugins (`rfe-creator`, `assess-rfe`) have no Cursor equivalent.
These are ODH skills-registry plugins installed via Claude Code's `/plugin`.
In Cursor, two options:
- If Cursor's `skills.sh` package manager supports GitHub repos, install from
  the same source
- Otherwise, document as a gap -- the plugin skills are available in Claude
  Code only. The underlying scripts (`hublib/jira.py`, `hub_jira.py`) work
  from any terminal regardless.

#### MCP servers

Cursor uses `.cursor/mcp.json` (project-scoped) with the identical
`mcpServers` format as Claude Code's `.mcp.json`. Cursor also supports
`envFile` for `.env` loading.

Deliverable: `.cursor/mcp.json` with the three servers (google-workspace,
slack, rhai-tracker). Two options for creation:
- **Doctor extension:** detect `.cursor/` directory, write `.cursor/mcp.json`
  alongside the Claude config work. Cleanest for ongoing maintenance.
- **Manual template:** document the config in `docs/mcp-servers.md` with a
  Cursor appendix. Simpler but manual.

Recommend the doctor extension -- it already writes MCP configs and reads
secrets from `restricted/.env`.

#### Memory tier

Cursor has no `autoMemoryDirectory`. The scratch tier (`memory/.scratch/`)
will not receive automatic writes from Cursor's built-in memory (which stores
short strings internally per-project, not as files).

This is graceful degradation, not a gap:
- `hub.capture` and `hub.consolidate` work directly -- they write the tracked
  store via the gate, not via scratch
- `hub.consolidate` in Cursor skips the scratch sweep (nothing to sweep) and
  still handles the session-content promotion path
- Cursor's built-in memories complement the hub's memory system (quick
  per-session preferences vs. durable cross-session knowledge)

Document in Cursor notes: "no scratch tier; use `hub.capture` for all durable
items."

#### Validation runbook

Execute in order, record everything:
1. Open repo in Cursor, confirm AGENTS.md loads, verify session follows the
   session-start rule (reads `memory/index.md`)
2. Test skill discovery -- invoke a hub skill, record whether Cursor finds
   `.claude/skills/` or needs bridging
3. Configure MCP servers (`.cursor/mcp.json`), test one tool from each server
   (list calendar events, list Slack channels, tracker query)
4. Run one full gated `hub.capture` -> reindex -> commit -> push from Cursor
5. Test multi-step skills: `hub.file` (creates partition + entry), then
   `hub.research` if practical (multi-agent fan-out may behave differently)
6. Record every gap, apply fixes as found

#### Deliverables

- `.cursor/mcp.json` (generated by doctor or committed)
- Skill-bridging mechanism if needed (symlinks or wrappers)
- Cursor notes in `docs/working-here.md` (or `docs/cursor.md` if warranted)
- Doctor extensions for Cursor detection + MCP config
- `## R6 outcome` note in `docs/enhancements.md`
- Memory log line

### Acceptance criteria

1. A fresh Cursor session reads `memory/index.md` on session start (AGENTS.md
   working)
2. At least the core daily skills work: `hub.capture`, `hub.file`,
   `hub.consolidate`, `hub.reindex`
3. All three MCP servers connect and respond to tool calls
4. One full capture -> reindex -> commit -> push completes from Cursor
5. Every gap is documented with severity (blocks daily work vs. nice-to-have)
   and workaround if any
6. Doctor reports Cursor-related sections without errors on a configured
   machine

---

## Sequencing

These two enhancements are independent. Recommended order:

1. **#14 first** (git-crypt) -- it changes tracked files and needs a clean
   commit before other work. The migration is a one-time operation with a
   clear test (verify on GitHub, verify on machine B).
2. **#9 second** (Cursor) -- it's primarily validation + config, and benefits
   from #14 being done (Cursor on machine B would get restricted/ content
   via git-crypt instead of manual copy).

Both can be done in one session. #14 is ~1 hour (install + migrate + verify).
#9 is ~1-2 hours (validation runbook + fixes + docs), variable depending on
how much Cursor discovers automatically vs. needs bridging.
