# Narrative layer & connection axis — design spec (Phase 1)

- **Status:** DRAFT — for section-by-section owner review
- **Date:** 2026-07-08
- **Owner:** Peter Double
- **Amends:** design decision D9 (see `/docs/architecture.md`); adds D12–D16
- **Scope:** structural — the repo's second axis. No new skills; no publishing
  changes. Content seeding is a gated pass at the end.

---

## 1. Problem & goals

The hub's D9 shipped exactly one organizing axis — **feature × type**. It
answers "where do I file this?" and "what do we know about X?" but cannot
answer "how do the pieces connect?" Four owner-identified needs (2026-07-08)
are all symptoms of that one gap:

1. **Narrative** — no home for the story: Adel's agentic strategy 2026, the
   RHAI strategic pillars, how the features together produce customer value
   and business results.
2. **Cross-feature artifacts** — HTML decks and md write-ups that explain the
   narrative or answer questions across features have no correct single-feature
   home, and enablement artifacts are invisible to the index machinery.
3. **Field Q&A** — questions from Sales/SSAs/PMs/customers/partners that the
   repo answers are not captured, deduplicated, or tracked for recurrence.
4. **JTBD** — no mechanism to identify, create, maintain, and track Jobs To Be
   Done for the UX and Documentation teams.

**Goal:** one second axis — a *connection layer* — expressed through three
shared mechanisms (a top-level `narrative/` tree, a `features:` cross-reference
field, new entry types + generated views), such that each need becomes a thin
slice of the same machinery rather than four bolt-ons.

Non-goals (Phase 1): publishing FAQ/JTBD to the pages site; a Slack sweep
assist; JTBD candidate mining; new skills; `features:` on research/strategy
documents.

## 2. Decisions (owner-approved 2026-07-08)

| # | decision |
|---|---|
| D12 | The connection layer is a **top-level `narrative/` tree** — a peer of `features/`, never a pseudo-feature. It reuses the identical five-dir skeleton. "Narrative" (not "strategy" — collides with the per-feature `strategy/` subdir, the `strat.*` Jira skills, and `memory/profiles/strategy.md`; not "portfolio" — Red Hat org overload). |
| D13 | A **`features:` frontmatter field** (OKF local extension per D10) declares which features an entry connects. Values are validated against `features/features.yaml` (unknown id = lint **error**); the indexer renders reverse links. Filing stays two questions — connections are declared, then *generated*, never hand-maintained. |
| D14 | **Type vocabulary extension:** `pillar` and `story` (narrative-only), `qa` and `jtbd` (feature or narrative knowledge), `artifact` (enablement descriptor). New views: `views/narrative-map.md`, `views/faq.md`, `views/jtbd.md`, `views/artifacts.md`. |
| D15 | **Execution status stays in Jira.** `jtbd` tracks the job's truth (`candidate → validated → delivered`, `retired`), never work-in-progress; a `jira:` field points at delivery. Same philosophy as the existing rule that roadmap dates live in one profile. |
| D16 | **Capture-first, publish-later.** FAQ/JTBD views are repo-internal in Phase 1. Curated FAQ/JTBD artifacts may ship via `hub.publish` in Phase 2, pulled by real demand. The Slack sweep assist is Phase 2 at most; capture-at-answer via `hub.capture` is the system of record. |

Platform re-home (part of D12's seeding): `platform` sheds its story-shaped
content to `narrative/` and its description narrows to components + org
reference data. Personas, people/stakeholder map, releases/SKUs, AI Gateway /
AI Hub UI knowledge **stay** in `platform`.

## 3. The `narrative/` layer

```
narrative/
  index.md            (generated)
  knowledge/          typed entries: pillar-, story-, plus the standard
                      vocabulary (decision/fact/ref/question/person, qa, jtbd)
                      + generated index.md
  research/           deep documents about the story (created on first use)
  strategy/           the strategy spine (e.g., agentic strategy 2026 material)
  enablement/         cross-feature artifacts, one subdirectory per artifact
  work/               drafts, transcripts/ (gitignored)
```

Rules (mirror the feature skeleton contract exactly):
- Subdirectories created on first use, never pre-created empty; anything else
  directly under `narrative/` is a lint **error**; only `index.md` as a file.
- `restricted/narrative/…` mirrors it (same shapes, local-only), like
  `restricted/features/…` today.

**Routing rule change** — the filing question gains one word:

> **Which home — `narrative/` or which feature? Which type?**

Route to `narrative/` when the subject is the *connective story itself*
(pillars, cross-feature value chains, strategy spine, artifacts about the big
picture). Route to a feature when there is a primary feature, even if others
are touched — then declare the spread with `features:`. When in doubt: a
primary feature exists more often than not; `narrative/` is for content that
would be *wrong* under any single feature.

## 4. The `features:` cross-reference field

- **Where allowed (Phase 1):** any knowledge entry (`features/*/knowledge/`,
  `narrative/knowledge/`) and `artifact.md` descriptors. Not memory files.
  Research/strategy documents: Phase 2.
- **Shape:** YAML list of feature ids from `features/features.yaml`.
- **Lint:** must be a list; every id must exist in the routing table —
  unknown id is an **error** (the feature list is closed; this is not the
  dangling-link case). An entry may list its own feature; the indexer dedupes.
- **Rendering:** each feature's generated `index.md` gains a **Connections**
  section — stories that include it, cross-feature artifacts and qa/jtbd
  entries (from other homes) that reference it. `views/*` below do the
  cross-cutting rollups.

## 5. New entry types — contracts

### 5.1 `pillar` (prefix `pillar-`) — `narrative/knowledge/` only

A strategic pillar (RHAI strategic pillars; the agentic-strategy pillars).

```yaml
type: pillar
description: one line — what this pillar is
timestamp: 2026-07-08
status: current          # standard current|superseded lifecycle
source: <provenance — doc/meeting>   # optional
```

Body: what the pillar means, what "good" looks like, the business result it
drives. No extra required fields.

### 5.2 `story` (prefix `story-`) — `narrative/knowledge/` only

A connective narrative: how a set of features together produce a customer
outcome / business result.

```yaml
type: story
description: one line — the story's claim
timestamp: 2026-07-08
features: [mcp-registry, mcp-gateway, mcp-ecosystem]   # REQUIRED, non-empty
pillar: /narrative/knowledge/pillar-<slug>.md          # optional; dangling → warning
status: current
```

Body: the narrative arc — situation, how the features compose, the customer
value, the business result, links to per-feature entries. Guidance (not
enforced): a story listing only one feature is usually a feature doc in
disguise — expect ≥2.

### 5.3 `qa` (prefix `qa-`) — any `knowledge/` (feature primary-home, or narrative for cross-feature)

A field question with our canonical answer. Distinct from `question-`
(**our** open product questions, tracked to resolution) — `qa-` is **the
field's** questions, answered, tracked for reuse and recurrence.

```yaml
type: qa
description: the question, compressed to one line
timestamp: 2026-07-08          # first captured
status: answered               # open|answered (question-style enum)
asks:                          # REQUIRED, ≥1 — the recurrence record
  - date: 2026-07-08
    by: customer               # customer|partner|sales|ssa|pm|eng|exec|other
    context: "RHOAI roadmap call"      # optional; public-safe wording only
features: [mcp-registry, mcp-gateway]  # optional spread
source: https://redhat-internal.slack.com/archives/…   # optional permalink
review_after: 2026-10-08       # optional; answers age as the product moves
```

Body sections: `## Question` (as asked, cleaned), `## Answer` (canonical,
citing the backing entries), `## Gaps` (optional — what we couldn't answer;
RFE/RICE evidence).

Rules:
- **Recurrence = append to `asks:`**, never a duplicate entry. Capture flow
  must search existing `qa-` entries first (see §8 skills).
- **Restricted bar extension:** asker *identities* (customer/partner names,
  deal context) go to the `restricted/` sibling entry; the public entry keeps
  only the role bucket. (Codify in `conventions/memory.md`'s gate list.)

### 5.4 `jtbd` (prefix `jtbd-`) — any `knowledge/` (feature primary-home, or narrative for cross-feature)

```yaml
type: jtbd
description: the job in one line
timestamp: 2026-07-08
persona: ai-engineer            # REQUIRED; free string v1 (see open Q4)
status: candidate               # candidate|validated|delivered|retired (own enum)
features: [agent-registry, agent-memory]   # optional
evidence:                       # optional; repo-root links or URLs
  - /features/mcp-registry/knowledge/qa-<slug>.md
jira: RHAIRFE-1234              # optional; where delivery is tracked
consumers: [ux, docs]           # optional; who uses this JTBD
review_after: 2026-10-08        # optional staleness
```

Body sections: `## Job` — "When *[situation]*, I want to *[motivation]*, so I
can *[outcome]*." — then `## Context & friction`, `## Success signals`,
`## Related` (links).

Status semantics (D15): `candidate` = identified from evidence, unvalidated ·
`validated` = confirmed with users/UX or strong recurring evidence ·
`delivered` = product/docs demonstrably serve the job (link proof) ·
`retired` = no longer worth tracking. **No in-progress state** — `jira:`
points at execution.

### 5.5 `artifact` (fixed filename `artifact.md`) — inside any `enablement/<slug>/`

Makes decks/write-ups first-class and discoverable (today enablement is
invisible to indexes).

```yaml
type: artifact
title: MCP Registry & Catalog
description: what this artifact is and who it's for
timestamp: 2026-07-08
features: [mcp-registry]        # optional; spread for cross-feature artifacts
source: <origin — old-repo path, GDoc, etc.>   # optional
```

Rules: exactly `artifact.md`, only inside an enablement slug directory (both
`features/*/enablement/` and `narrative/enablement/`); other files in the
slug dir stay unlinted (self-contained artifacts keep their assets). Publish
state is **derived** — the indexer cross-references `publish/manifest.yaml`;
it is never stored in the descriptor. Descriptors are recommended, not
required (missing ones are listed as "no descriptor" in the view, not
errors) — future migrations (e.g., the old repo's HTML sets) add one per
artifact at migration time.

## 6. Generated views & index changes

| view | derived from | shape |
|---|---|---|
| `views/narrative-map.md` | pillar + story entries | pillars → their stories → the features each story connects (links); trailing sections: stories without a pillar, pillars without stories (flagged, not errors) |
| `views/faq.md` | `qa` entries | sections: **Unanswered** (`status: open`, newest first) · **Most asked** (`len(asks) ≥ 2`, sorted desc) · **By feature** (all, grouped) — titled "FAQ" (audience-facing name; entries stay `qa-`) |
| `views/jtbd.md` | `jtbd` entries | grouped by status, then feature; per row: persona, evidence count (0-evidence flagged), jira link if present |
| `views/artifacts.md` | `artifact.md` descriptors + enablement dirs | every artifact across features + narrative; publish dest (from manifest) or "unpublished"; descriptor-less dirs listed as such |

Also:
- `narrative/index.md` and `narrative/knowledge/index.md` generated exactly
  like a feature's.
- Every `features/<id>/index.md` gains a **Connections** section (stories,
  cross-referencing artifacts/qa/jtbd), derived from `features:` fields.
- `views/stale-facts.md` picks up `qa`/`jtbd` entries via the existing
  `review_after` mechanics (no new staleness machinery).

## 7. Contract changes — the build checklist

**`scripts/hublib/schema.py`**
1. `KNOWLEDGE_TYPES` += `qa`, `jtbd`. New `NARRATIVE_TYPES = KNOWLEDGE_TYPES ∪ {pillar, story}`.
2. `PREFIX_TO_TYPE` += `pillar-`, `story-`, `qa-`, `jtbd-`.
3. `TYPE_EXTRA_REQUIRED` += `story → (features,)`, `qa → (status, asks)`, `jtbd → (persona, status)`.
4. Per-type status enums (generalize the existing `question` carve-out):
   `question`/`qa` → `open|answered`; `jtbd` → `candidate|validated|delivered|retired`;
   default → `current|superseded`.
5. `asks:` shape validation — non-empty list; each item a mapping with `date`
   (ISO) and `by` (enum above); `context` optional.
6. `features:` validation — list of ids present in `features/features.yaml`
   (schema gains a features.yaml loader); unknown id = **error**. Applies to
   knowledge entries and `artifact.md`.
7. `_lint_tree` lints `narrative/` (same skeleton contract; knowledge typed
   against `NARRATIVE_TYPES`; `pillar`/`story` automatically invalid under
   `features/` since they're absent from `KNOWLEDGE_TYPES`).
8. `artifact.md` lint: allowed only at `*/enablement/<slug>/artifact.md`,
   type must be `artifact`; no other enablement files are linted.
9. `restricted/narrative/` linted when present (extend the existing
   restricted `_lint_tree` call).
10. `story.pillar:` dangling target → **warning** (link philosophy).

**`scripts/hublib/indexer.py`**
11. Load narrative entries + artifact descriptors; generate `narrative/index.md`,
    `narrative/knowledge/index.md`, the four new views, and the per-feature
    Connections sections. Manifest cross-reference for publish state.
12. Convergence preserved (generate twice → no diff); `--check` covers the new
    generated files automatically.

**Tests (`scripts/tests/`)** — required per repo rule (regression test with any
behavior change):
13. Schema: happy + sad path per new type (missing required fields, bad enums,
    bad `asks` shape, unknown `features:` id, pillar/story under `features/`,
    stray file under `narrative/`, misplaced `artifact.md`).
14. Indexer: each new view renders from fixtures; Connections backlinks;
    convergence; descriptor-less enablement dir listed.

**Conventions & docs**
15. `conventions/layout.md` — filing questions updated; `narrative/` section.
16. `conventions/type-vocabulary.md` — new rows; the `question-` vs `qa-`
    distinction note; `artifact` descriptor; per-type status enums.
17. `conventions/memory.md` — restricted-bar bullet: qa asker identities.
18. `docs/architecture.md` — anatomy row, filing questions, views table,
    D12–D16 appended to the decisions table.
19. `AGENTS.md` — map row for `narrative/`, one-line routing update (within
    the 150-line budget); `README.md` layout paragraph; `docs/working-here.md`
    daily-loop mention of qa capture.

**Skills (SKILL.md text only — zero new skills in Phase 1)**
20. `hub.capture` — classifier gains: story-shaped → narrative; field question
    → qa flow (**dedupe first**: search existing `qa-`; match → append to
    `asks:` + offer answer refresh; else new entry; Slack permalink → `source:`;
    restricted call for asker identity); job-shaped → `jtbd` candidate.
21. `hub.file` — same routing extension (narrative as a destination; partition
    creation logic untouched).
22. `hub.consolidate` — sweep classifications gain qa/jtbd/story.
23. `hub.migrate` — narrative as a routing target for story-shaped old-repo
    content; artifact migrations add `artifact.md` descriptors.

## 8. Seed content & platform re-home (gated apply, end of Phase 1)

All through the normal capture/migrate gates, batch-style with owner rulings:

1. **Pillars:** create `pillar-` entries from (a) the agentic-strategy four
   pillars (superseding `features/platform/knowledge/fact-agentic-ai-four-pillars.md`
   with a `superseded_by` pointer — never deleted) and (b) the RHAI strategic
   pillars — **source needed from owner** (open Q1).
2. **Re-home from `platform` → `narrative/knowledge/`:**
   `ref-agentic-ai-strategy-2026.md`, `fact-agentic-ai-messaging-position.md`
   (batch-2 precedent: move, swap tags, repoint inbound links).
3. **`platform` description narrowed** in `features/features.yaml` to
   components + org reference (AI Gateway, AI Hub UI, releases, people,
   personas, SKUs).
4. **Seed stories (2–3, owner edits at gate):** proposed — "Governed MCP
   access end-to-end" (mcp-registry + mcp-gateway + mcp-ecosystem); "The agent
   lifecycle: build → run → operate" (agent-registry + agent-memory +
   agent-ops + gen-ai-studio). Owner may add a third at review.
5. **Artifact descriptor backfill:** one `artifact.md` for the existing
   `features/mcp-registry/enablement/mcp-registry-catalog-deck/`.
6. First `qa-` and `jtbd-` entries arrive through real use, not seeding.

## 9. Phase 2 (recorded, deliberately deferred)

- Curated FAQ page and JTBD catalog published via `hub.publish` (per-audience;
  manifest already supports `audience: internal`), pulled by real demand
  (~20+ answered qa entries, or UX/Docs asking for a URL).
- Slack sweep assist for qa capture (inherits xoxc/xoxd token brittleness —
  assist, never system of record).
- JTBD candidate mining from qa recurrence + the customer tracker (hook into
  `customer-feedback-refresh`).
- `features:` honored on research/strategy documents.
- qa "Gaps" → RFE/RICE evidence hook (`rice-strats` port can cite `asks` counts).
- Persona vocabulary tightening (closed list) if free-string drifts.

## 10. Acceptance criteria

- `python -m pytest scripts/tests -q` green including the new schema/indexer
  tests; `hub_lint.py` 0 errors on the seeded repo; `hub_index.py --check`
  0 stale; generation convergence holds.
- `views/narrative-map.md` renders pillars → stories → features from the seed
  content; `views/faq.md` / `views/jtbd.md` / `views/artifacts.md` render
  (empty-state sections allowed); every feature index shows a Connections
  section when it has any.
- Budgets hold (`AGENTS.md` ≤ 150, `memory/index.md` ≤ 200); CI (`validate`,
  `publish`) green; no new skills; publishing manifest untouched.
- Seed batch applied with owner rulings recorded (migration-report style).

## 11. Open questions for review

1. **RHAI strategic pillars** — what is the canonical source (doc/link/list)?
   Needed before the pillar seed; the agentic-strategy pillars are already in
   the hub.
2. **`decision-registry-vs-catalog.md`** — cross-cutting doctrine; re-home to
   `narrative/` now, or leave in `platform` and move on-touch? (Default:
   leave; minimize Phase 1 moves.)
3. **`asks[].by` buckets** — proposed `customer|partner|sales|ssa|pm|eng|exec|other`;
   confirm these match how you'd want recurrence sliced.
4. **Persona values** — free string in v1 (default), or locked to the
   personas set from day one?
5. **Third seed story** — want one for the studio/skills side (e.g.,
   "from prompt to governed asset"), or start with two?

---

*After approval: implementation plan (task breakdown per the repo's
spec → plan → build workflow), then build with section approvals. This spec
document moves to `status: APPROVED` with rulings inlined.*
