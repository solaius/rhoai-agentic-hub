# hub.strategy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the `hub.strategy` skill — a gated, prompt-only skill that synthesizes one living strategy document per feature (`features/<id>/strategy/strategy.md`) from the partition's knowledge, research series, and Jira scope — plus its conventions contract and offer hooks, then pilot on agent-catalog.

**Architecture:** Prompt-only skill in the hub.sweep pattern (spec D4): no scripts, no fan-out; context-load → scratchpad draft → inline gate → write/reindex/lint/pathspec-commit. The document contract lives in `conventions/strategy.md` (mirrors `conventions/research.md`); the skill references it rather than embedding the template.

**Tech Stack:** Markdown skill files (`.claude/skills/*/SKILL.md`), hub tooling (`scripts/hub_index.py`, `scripts/hub_lint.py`, pytest suite), git.

**Spec:** `docs/specs/2026-07-16-hub-strategy-skill-design.md` — decisions D1–D4 are settled; do not re-litigate.

## Global Constraints

- This repo is PUBLIC. No customer names, no deal context, nothing Jira does not serve anonymously, in any tracked file.
- SHARED CHECKOUT with concurrent sessions: NEVER `git add -A` or bare `git add .`; stage and commit with explicit pathspecs only; run `git diff --cached --stat` before every commit and confirm only your files are staged.
- Generated files (`features/index.md`, `features/*/index.md`, `features/*/knowledge/index.md`, `memory/index.md`, `views/*`) are never hand-edited; the pre-commit hook re-runs lint + index-freshness and blocks on errors.
- `python scripts/hub_lint.py` must report 0 errors after any tracked write (warnings are expected — there is a pre-existing baseline of ~105).
- Links in tracked content use leading-slash repo-root form: `[x](/conventions/strategy.md)`.
- AGENTS.md has a 150-line CI budget — verify `wc -l` after editing it.
- Commit trailer on every commit: `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- Skill prose style: match the existing hub skills — numbered steps, terse imperative, ALL-CAPS step labels, gate language identical in spirit to hub.jira-sweep/hub.intake.

---

### Task 1: conventions/strategy.md + layout.md pointer

**Files:**
- Create: `conventions/strategy.md`
- Modify: `conventions/layout.md` (the skeleton-contract table row for `strategy/`)

**Interfaces:**
- Produces: the document contract that Task 2's SKILL.md cites as `/conventions/strategy.md`, and the section names Task 5's pilot document must use verbatim: `The brief`, `What`, `Why`, `Where we stand`, `Gaps & risks`, `Jira map` (with `### Candidate jiras`), `Watchlist`, `History`.

- [ ] **Step 1: Create `conventions/strategy.md` with exactly this content**

```markdown
# Strategy document conventions

`features/<id>/strategy/strategy.md` is the feature's ONE living strategy
document — the synthesis a PM plans from. Evidence stays in `knowledge/`
and `research/`; this document cites, it never restates at length.
Producer: `hub.strategy` (gated). Hand-edits are allowed (it is a
document, not a generated file); the next refresh reconciles them and
records the reconciliation in `## History`.

## Shape

ONE file per feature: `strategy/strategy.md`. Current-state, rewritten in
place on refresh (the profile pattern) — never a dated series; the dated
record lives in `research/` and `knowledge/` decisions. Other strategy
artifacts (RFE roadmaps, outcome write-ups) may sit alongside it under
`strategy/`, but `strategy.md` is the entry point and must stand alone.

## Frontmatter

`title` ("<Feature> — strategy") · `description` (one line — feeds the
indexes) · `timestamp` (date of last rewrite) · `status: current` ·
`review_after` (default +60 days — hub.sweep flags staleness) · `source`
(generator note: inputs + date). Linted as warnings only, like research
docs — strategy documents never fail the build.

## The eight sections (fixed order, fixed names)

| # | section | contract |
|---|---|---|
| 1 | `## The brief` | ≤10 lines. What this is, the one-sentence bet, where it stands today, next milestone. The owner's 60-second re-entry. |
| 2 | `## What` | Product shape by release train (table: release → scope → status) + boundaries: what this feature is NOT, with routing to its `related:` siblings. |
| 3 | `## Why` | The problem and the bet stated plainly: jobs served (jtbd/persona links where they exist), market position (wedge vs behind, from research), why now. |
| 4 | `## Where we stand` | Decisions to date (dated, linked), delivery state, in-flight work. |
| 5 | `## Gaps & risks` | Open `question-` entries + research risks + tensions, each with one why-it-matters line. The honest section. |
| 6 | `## Jira map` | Coverage table (strategy element → keys → status), then `### Candidate jiras`: gap → one-line problem statement → suggested project, each ready to hand to `/rfe.create`. Keys/type/status only from Jira; ALL prose in the hub's own words (unauthenticated-probe rule — never probe-withheld text). |
| 7 | `## Watchlist` | Dated external triggers that would change this strategy (upstream merges, freezes, competitor moves), each with "if it fires → what changes". |
| 8 | `## History` | Profile-style dated entries, newest first; every refresh appends one (date, what changed, why, source). Never deleted. |

## Register & rules

- PM working document (owner decision, 2026-07-16): dense, hub-context
  assumed, optimized for the owner's planning and re-entry — not an
  outsider pitch. Public-repo discipline still applies in full.
- Every load-bearing claim links its hub source (leading-slash form).
- Target length: The brief ≤10 lines; the whole document 2–4 pages.
- No customer names, no deal context, ever (restricted-lint enforced).
- Refresh = rewrite the body in place + append one `## History` entry.

## Producers & consumers

- Producer: [hub.strategy](/docs/skills.md). Offered as a follow-up by
  `hub.intake` and `hub.research`; never auto-run.
- Consumers: `hub.sweep` (review_after staleness), `hub.research`
  (sibling standing context), the marketplace review quartet
  (scope/architecture/feasibility/testability reviews), `/rfe.create`
  (candidate jiras).
```

- [ ] **Step 2: Update the skeleton table row in `conventions/layout.md`**

Read the file first; the current row is:

```
| `strategy/`  | strategy docs, RFE roadmaps, outcomes |
```

Replace with:

```
| `strategy/`  | strategy docs, RFE roadmaps, outcomes — `strategy.md` is the living per-feature strategy doc ([strategy.md](/conventions/strategy.md)) |
```

- [ ] **Step 3: Verify lint is clean**

Run: `python scripts/hub_lint.py 2>&1 | tail -1`
Expected: `hub_lint: 0 error(s), <N> warning(s)` — error count MUST be 0; warning count may match the pre-existing baseline (~105).

- [ ] **Step 4: Commit with pathspecs**

```bash
git add conventions/strategy.md conventions/layout.md
git diff --cached --stat   # exactly these 2 files
git commit -m "conventions(strategy): living strategy.md contract + layout pointer

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- conventions/strategy.md conventions/layout.md
```

Do NOT push (Task 5 pushes the batch).

---

### Task 2: the hub.strategy skill

**Files:**
- Create: `.claude/skills/hub.strategy/SKILL.md`

**Interfaces:**
- Consumes: `/conventions/strategy.md` from Task 1 (cited, not embedded).
- Produces: the skill whose name (`hub.strategy`) Tasks 3's hooks and docs rows reference.

- [ ] **Step 1: Create `.claude/skills/hub.strategy/SKILL.md` with exactly this content**

```markdown
---
name: hub.strategy
description: Synthesize or refresh a feature's living strategy document (features/<id>/strategy/strategy.md) from its knowledge, research series, and Jira scope - the WHAT/WHY, gaps and risks, Jira coverage map plus candidate jiras, and watchlist - through the inline gate. Use when the user says "write the strategy for <feature>", "generate the strategy doc", "create the strategy", "refresh the strategy", or after hub.intake / hub.research offer it. One living doc per feature, rewritten in place - never a series.
---

# hub.strategy

Input: a feature id (features/features.yaml). Contract:
/conventions/strategy.md — ONE living document, eight fixed sections, PM
working register, rewritten in place with a ## History entry per refresh.
Spec: /docs/specs/2026-07-16-hub-strategy-skill-design.md.

1. RESOLVE: feature id → features/<id>/strategy/strategy.md. No home in
   features.yaml → offer hub.intake (research needs a home), stop there
   if declined. The file already exists ⇒ this is a REFRESH run.
2. PRECONDITIONS: knowledge/index.md must exist — none → hand off to
   hub.intake and stop. Empty research/ → warn that Why/market will be
   thin, offer hub.research first; proceed only on the user's explicit
   OK. No jira: block or work/jira-snapshot.yaml → offer hub.jira-sweep;
   proceeding means the Jira map names the missing scope as its first
   gap.
3. CONTEXT LOAD (read, in order): knowledge/index.md and every
   decision-/question-/fact- entry in the partition; research/
   00-executive-summary.md, then each lens doc; work/jira-snapshot.yaml
   and the partition's Jira ref- entries; memory/profiles/roadmap.md and
   memory/profiles/strategy.md; each related: sibling's overview fact
   (features.yaml). A missing input shrinks the document, never sinks
   the run — name it in Gaps & risks.
4. DRAFT in the session scratchpad per the /conventions/strategy.md
   section contract — no repo writes. Register: PM working doc (dense,
   hub-context assumed; The brief is the owner's 60-second re-entry).
   Every load-bearing claim cites its hub source (leading-slash link).
   PUBLIC repo: no customer names or deal context; Jira keys/type/status
   only, all prose your own words — NEVER probe-withheld text. Candidate
   jiras: one line each — gap → problem statement → suggested project
   (RHAIRFE/RHAISTRAT) — written to hand straight to /rfe.create.
5. GATE: show The brief inline plus one write line —
   `features/<id>/strategy/strategy.md: <description> [new|update]` —
   full document on request. REFRESH runs show a per-section
   what-changed summary (unchanged/updated/new) instead of the full doc,
   plus the proposed History line. Nothing touches the repo before OK.
6. On OK: write the file, run `python scripts/hub_index.py`, then
   `python scripts/hub_lint.py` (0 errors — fix the document, not the
   scripts). Commit: stage the doc plus regenerated indexes/views
   explicitly, NEVER `git add -A` (shared checkout, see
   fact-concurrent-session-git-hygiene); check
   `git diff --cached --stat`, then commit with pathspecs:
   `git commit -m "strat(<id>): strategy doc <new|refresh>" -- <those paths>`
   && `git push`.
7. OFFER, never auto-run: /rfe.create for candidate jiras the user
   approves; the marketplace review quartet (/scope-review,
   /architecture-review, /feasibility-review, /testability-review)
   against the document or its anchor STRAT; hub.publish only on
   explicit ask (publishing is a separate disclosure decision).
```

- [ ] **Step 2: Sanity-check the skill file parses as a hub skill**

Run: `head -5 .claude/skills/hub.strategy/SKILL.md`
Expected: frontmatter opens with `---` then `name: hub.strategy`.
Also verify every internal path it cites exists or is an allowed dangling reference: `ls conventions/strategy.md docs/specs/2026-07-16-hub-strategy-skill-design.md` → both exist (Task 1 ran first).

- [ ] **Step 3: Lint still clean**

Run: `python scripts/hub_lint.py 2>&1 | tail -1`
Expected: `0 error(s)` (skill files are not knowledge entries; no new warnings expected).

- [ ] **Step 4: Commit with pathspecs**

```bash
git add .claude/skills/hub.strategy/SKILL.md
git diff --cached --stat   # exactly this 1 file
git commit -m "skill(hub.strategy): living per-feature strategy doc, gated (spec 2026-07-16)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- .claude/skills/hub.strategy/SKILL.md
```

---

### Task 3: offer hooks + docs rows (intake, research, AGENTS.md, docs/skills.md)

**Files:**
- Modify: `.claude/skills/hub.intake/SKILL.md` (step 6)
- Modify: `.claude/skills/hub.research/SKILL.md` (step 8)
- Modify: `AGENTS.md` (skills table — mind the 150-line budget)
- Modify: `docs/skills.md` (chain bullet + quick-reference row + in-depth paragraph)

**Interfaces:**
- Consumes: the skill name `hub.strategy` and contract path `/conventions/strategy.md` from Tasks 1–2.

**IMPORTANT:** Read each target file before editing — line wrapping in these files is hand-set; match the exact bytes you find, not the wrapping shown here. The quoted "current text" below is semantically exact but MAY wrap differently on disk.

- [ ] **Step 1: hub.intake step 6**

Current step 6 ends: `...scoping gaps → requirements). Never auto-run.`

Append one sentence so the step becomes (re-wrap to match the file's style):

```
6. OFFER RESEARCH: suggest `hub.research <home>` with a lens set fitted
   to what intake revealed (unknown competitive space → competitive;
   heavy technical sources → architecture + upstream; scoping gaps →
   requirements). Never auto-run. Once research has landed (now or
   later), also offer `hub.strategy <home>` — the living strategy doc
   synthesizes it (/conventions/strategy.md).
```

- [ ] **Step 2: hub.research step 8**

Current: `8. Offer follow-ups the run surfaced (a deeper lens pass, hub.intake for an adjacent topic) — never auto-run them.`

Replace with:

```
8. Offer follow-ups the run surfaced (a deeper lens pass, hub.intake for
   an adjacent topic, `hub.strategy <home>` now that a series exists —
   the strategy doc consumes it) — never auto-run them.
```

- [ ] **Step 3: AGENTS.md skills-table row**

Insert directly after the `hub.research` row:

```
| hub.strategy | synthesize/refresh the feature's living strategy doc (strategy/strategy.md) from knowledge + research + jira -- gated |
```

Then run: `wc -l AGENTS.md` — expected ≤ 150. If over budget, shorten THIS row (not others) until under.

- [ ] **Step 4: docs/skills.md — three edits**

(a) Chain bullet, inserted directly after the `**Research:**` bullet:

```
- **Strategy:** `hub.strategy <feature>` → the ONE living
  `strategy/strategy.md` (eight-section contract:
  [/conventions/strategy.md](/conventions/strategy.md)) synthesized from
  knowledge + research + the Jira snapshot; refresh rewrites in place +
  `## History`. Offered by intake and research; its candidate jiras feed
  `/rfe.create`.
```

(b) Quick-reference table row, inserted directly after the `hub.research` row:

```
| `hub.strategy` | write/refresh a feature's living strategy doc | brief shown inline + write gate | `strategy/strategy.md`, reindex + commit |
```

(c) In-depth paragraph, inserted directly after the `**hub.research**` paragraph block (before `**hub.jira-sweep**`):

```
**`hub.strategy`** — the synthesis layer: one living strategy document per
feature (`strategy/strategy.md`, contract in
[/conventions/strategy.md](/conventions/strategy.md)) built from the
partition's knowledge entries, research series, Jira snapshot + refs,
memory profiles, and `related:` siblings. PM working register — dense,
60-second re-entry brief, honest gaps section, Jira coverage map plus
gap-derived candidate jiras ready for `/rfe.create`. Rewritten in place on
refresh with a `## History` entry; preconditions nudge toward
`hub.research` / `hub.jira-sweep` first when those inputs are missing.
```

- [ ] **Step 5: Lint + verify budgets**

Run: `python scripts/hub_lint.py 2>&1 | tail -1` → `0 error(s)`.
Run: `wc -l AGENTS.md` → ≤ 150.

- [ ] **Step 6: Commit with pathspecs**

```bash
git add .claude/skills/hub.intake/SKILL.md .claude/skills/hub.research/SKILL.md AGENTS.md docs/skills.md
git diff --cached --stat   # exactly these 4 files
git commit -m "wire(hub.strategy): intake/research offers, AGENTS + skills-guide rows

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- .claude/skills/hub.intake/SKILL.md .claude/skills/hub.research/SKILL.md AGENTS.md docs/skills.md
```

---

### Task 4: verify lint/indexer treatment of strategy/ (report-only)

**Files:**
- Create/Modify: NONE in the repo. Scratch work only, under the session scratchpad directory. This task produces a REPORT.

**Interfaces:**
- Consumes: nothing from other tasks (read-only investigation; can run in parallel with Tasks 1–3).
- Produces: a written verdict the pilot (Task 5) relies on: (a) how `hub_lint.py` treats `features/<id>/strategy/*.md` frontmatter (expected: same generic warning-only treatment as research docs — grep already shows the linter has NO special-casing for either); (b) whether `hub_index.py` enumerates strategy/ files in the generated feature index or only links the directory; (c) whether the existing pytest suite stays green untouched.

- [ ] **Step 1: Read the relevant script behavior**

Read `scripts/hub_lint.py` and `scripts/hub_index.py` (plus `scripts/hublib/` if logic lives there): find where feature-subdirectory markdown is discovered, what frontmatter rules apply outside `knowledge/`, and how `features/<id>/index.md` renders the five skeleton links. Cite exact line numbers in the report.

- [ ] **Step 2: Empirical check in an isolated root**

The test suite (`scripts/tests/`) shows how to build a temp hub root (e.g. `test_disclosure.py` writes files under `tmp_path` and points the tool at it). Using the same mechanism (`--root` flag or test helper — whichever the scripts actually support), build a minimal fake hub in the SCRATCHPAD containing `features/x/strategy/strategy.md` with the Task-1 frontmatter shape, run lint + index against it, and record: errors? warnings? does the generated feature index list the file?

- [ ] **Step 3: Pytest regression**

Run: `python -m pytest scripts/tests -v 2>&1 | tail -3`
Expected: all pass (no scripts were changed by this plan; any failure is pre-existing — report it, do not fix scripts).

- [ ] **Step 4: Report**

Return the verdict (a/b/c) with line citations. If (a) or (b) reveals the linter ERRORS on strategy docs or the indexer breaks on them, STOP and report — the fix belongs in the plan owner's hands (content-side fix per the spec; scripts only change if the indexer genuinely ignores strategy/).

No commit — this task writes nothing to the repo.

---

### Task 5: pilot — hub.strategy agent-catalog (MAIN SESSION ONLY)

**Files:**
- Create: `features/agent-catalog/strategy/strategy.md` (through the skill's own gate)
- Modify: `memory/log.md` (one shipped-skill log line under today's heading)

**Interfaces:**
- Consumes: everything — the skill (Task 2), the contract (Task 1), Task 4's verdict.

**This task runs in the MAIN SESSION, not a subagent** — it requires the owner's gate approvals and his read of The brief.

- [ ] **Step 1: Push the implementation batch**

```bash
git push
```

- [ ] **Step 2: Invoke `hub.strategy agent-catalog`** (the Skill tool) and follow its flow end-to-end: context load → draft → gate (show The brief) → on OK write/reindex/lint/commit/push.

- [ ] **Step 3: Check pilot success criteria from the spec**

- The brief reads true in 60 seconds (owner's call at the gate).
- Jira map reconciles all 6 strategic refs (RHAISTRAT-1740/1697/1742/1758/1349/1792) + RHAIRFE-2443.
- Candidate jiras include the known unhomed gaps: Sandbox-naming reconciliation, upstream customProperties divergence check, owner-metadata capture at deploy time.
- Watchlist carries: OpenShell Go SDK PR series, AIPCC ADR (MR 224), Forrester ADP Wave (Q4 2026), MLflow RFC-0008.
- The dangling `/features/agent-catalog/strategy/` link warning disappears from lint output (or Task 4 explained why not).

- [ ] **Step 4: Log the shipped skill**

Append under `## 2026-07-16` in `memory/log.md` (create nothing — the heading exists):

```
- **Creation** -- hub.strategy shipped (spec + plan 2026-07-16): living per-feature strategy doc (conventions/strategy.md, 8 sections), offered by intake/research, piloted on agent-catalog (first strategy/ leg filled in the hub).
```

Then: `python scripts/hub_index.py`, lint (0 errors), commit `mem: log hub.strategy shipped` with pathspecs (`memory/log.md memory/index.md`), push.

---

## Self-review notes (done at plan time)

- Spec coverage: D1–D4 → Tasks 1–2; wiring → Task 3; verify item → Task 4; pilot + success criteria → Task 5. Out-of-scope list untouched. ✓
- No placeholders: full file contents embedded for every create; edits quote current text with a read-first instruction because wrapping is hand-set. ✓
- Name consistency: `hub.strategy`, `strategy/strategy.md`, `/conventions/strategy.md`, section names, and the `strat(<id>):` commit prefix are identical across tasks. ✓
