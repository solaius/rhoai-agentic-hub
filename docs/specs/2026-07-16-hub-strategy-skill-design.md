# hub.strategy — per-feature strategy document skill — design spec

- **Date:** 2026-07-16 · **Owner:** Peter Double · **Status:** approved
  design, pre-implementation
- **Fills:** the empty `strategy/` leg of the feature skeleton contract
  (/conventions/layout.md — "strategy docs, RFE roadmaps, outcomes"), which
  no skill populates today (every generated feature index carries a dangling
  `strategy/` link).
- **Pilot:** agent-catalog — the most fully provisioned partition (intake,
  5-lens research series, Jira scope + snapshot + strategic refs, all landed
  2026-07-16).

## Problem

The hub accumulates knowledge (typed entries), evidence (research series),
and Jira state (sweeps) per feature, but nothing synthesizes them into the
document a PM actually plans from: what we're building and why, where it
stands, what's missing, and which gaps should become Jira items. That
synthesis exists today only in Peter's head and scattered across decisions,
research summaries, and profiles. Each new feature re-derives it ad hoc;
returning to a feature after weeks means re-reading everything.

## Decisions already made (brainstorm, 2026-07-16 — do not re-litigate)

- **D1 — Shape:** ONE living document, `features/<id>/strategy/strategy.md`,
  rewritten in place on refresh with a `## History` section (profile
  pattern). No dated series, no companion files.
- **D2 — Jira section:** BOTH halves — a coverage map (existing
  STRAT/RFE/ENG keys → which strategy element they deliver) AND gap-derived
  candidate jiras, each a one-line problem statement ready to hand to
  `/rfe.create`. Uncovered gaps and unhomed jiras both surface.
- **D3 — Audience:** PM working document. Dense, hub-context assumed,
  optimized for the owner's planning and 60-second re-entry — NOT an
  outsider pitch. Public-repo discipline still applies in full (no customer
  names, no deal context, nothing Jira won't serve anonymously).
- **D4 — Architecture:** prompt-only skill (hub.sweep pattern). No fan-out,
  no new scripts. Strategy synthesis wants one mind holding all inputs;
  the heavy lifting (research, sweep) already happened upstream.

## The document contract (`conventions/strategy.md`)

`features/<id>/strategy/strategy.md` (narrative/ may adopt the same shape
later for the strategy spine; out of scope now).

Frontmatter: `title` ("<Feature> — strategy") · `description` (one line for
the indexes) · `timestamp` · `status: current` · `review_after`
(+60 days default — hub.sweep flags staleness) · `source` (generator note:
inputs + date).

Eight sections, fixed order, fixed names:

| # | Section | Contract |
|---|---|---|
| 1 | **The brief** | ≤10 lines. What this is, the one-sentence bet, where it stands today, next milestone. The owner's 60-second re-entry. |
| 2 | **What** | Product shape by release train (table: release → scope → status) + boundaries: what this feature is NOT, with routing to `related:` siblings. |
| 3 | **Why** | The problem and the bet stated plainly: jobs served (jtbd/persona links where they exist), market position (wedge vs behind, from research), why now. |
| 4 | **Where we stand** | Decisions to date (dated, linked), delivery state, in-flight work. |
| 5 | **Gaps & risks** | Open `question-` entries + research risks + tensions, each with one why-it-matters line. The honest section. |
| 6 | **Jira map** | Coverage table (strategy element → keys → status) then `### Candidate jiras` (gap → one-line problem statement → suggested project). Keys and status only from Jira; all prose is the hub's own words (unauthenticated-probe rule). |
| 7 | **Watchlist** | Dated external triggers that would change this strategy (upstream merges, freezes, competitor moves), each with "if it fires → what changes". |
| 8 | **History** | Profile-style dated entries, newest first; every refresh appends one. |

Rules: every load-bearing claim links its hub source (leading-slash form —
the strategy doc CITES knowledge/research, it never restates evidence at
length); target length 2–4 pages beyond The brief; rewrite-in-place on
refresh (the doc is current-state; research/ holds the dated record);
no customer names or deal context ever (restricted-lint enforced).

## The skill (`.claude/skills/hub.strategy/SKILL.md`)

Prompt-only. Flow:

1. **RESOLVE:** feature id from features/features.yaml (no home → offer
   hub.intake, stop). Existing `strategy/strategy.md` ⇒ REFRESH run.
2. **PRECONDITIONS:** knowledge/index.md must exist. Empty `research/` →
   warn that the Why/market sections will be thin, offer `hub.research`
   first; proceed only on explicit user OK. No `jira:` block/snapshot →
   same pattern with `hub.jira-sweep` (section 6 then marks Jira scope
   itself as a gap).
3. **CONTEXT LOAD:** knowledge index + every decision-/question-/fact- in
   the partition; research `00-executive-summary.md` + lens docs; Jira
   snapshot + jira ref- entries; memory/profiles/roadmap.md +
   strategy.md; `related:` siblings' overview facts. (Same standing-context
   discipline as hub.research.)
4. **DRAFT** in the session scratchpad per conventions/strategy.md — no
   repo writes.
5. **GATE:** show The brief inline + one write line
   (`strategy/strategy.md [new|update]`), full document on request.
   REFRESH runs show a what-changed summary instead of the full doc.
   Nothing touches the repo before OK.
6. **On OK:** write, `python scripts/hub_index.py`, `python
   scripts/hub_lint.py` (0 errors), commit with pathspecs
   (`strat(<id>): strategy doc <new|refresh>` — NEVER `git add -A`), push.
7. **OFFER, never auto-run:** `/rfe.create` for approved candidate jiras;
   the marketplace review quartet (`/scope-review`, `/architecture-review`,
   `/feasibility-review`, `/testability-review`) against the doc or its
   anchor STRAT; `hub.publish` only on explicit ask.

## Wiring

- `conventions/strategy.md` — the contract above; add a row/link in
  conventions/layout.md's skeleton table pointing at it.
- `hub.intake` step 6 — after offering hub.research, add: research already
  landed (or lands later) → offer `hub.strategy <home>`.
- `hub.research` follow-ups step — add `hub.strategy` to the offered
  follow-ups once a series exists.
- AGENTS.md skills table + docs/skills.md — one row each.
- Lint/indexer: expected to need NO changes — strategy/ files get the same
  warning-only frontmatter treatment as research docs, and the generated
  feature index already links the `strategy/` directory (writing the first
  strategy.md turns the dangling link live). VERIFY both behaviors during
  implementation; fix content-side, not scripts, unless the indexer
  genuinely ignores strategy/.

## Pilot

Immediately after the skill lands: `hub.strategy agent-catalog`, through
its own gate. Success looks like: The brief reads true in 60 seconds; the
Jira map reconciles all 6 strategic refs + RHAIRFE-2443; candidate jiras
include at least the known unhomed gaps (e.g. Sandbox-naming
reconciliation, upstream customProperties divergence check, owner-metadata
capture at deploy time); Watchlist carries the research follow-up triggers
(Go SDK PR series, AIPCC ADR, Forrester ADP Wave, MLflow RFC-0008).

## Out of scope / deferred

- narrative/strategy/ (the cross-feature strategy spine) — same template
  may apply later; not now.
- Auto-refresh cadence (cron/loop) — manual invocation + review_after
  staleness flagging only.
- Publishing strategy docs to the internal hub sites — hub.publish remains
  a separate, explicit decision.
- Script-assisted data pack (`hub_strategy.py`) — only if generated docs
  drift from their sources in practice.
