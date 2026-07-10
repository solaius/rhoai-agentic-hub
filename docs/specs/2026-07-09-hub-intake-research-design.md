# hub.intake + hub.research — design spec

- **Date:** 2026-07-09 · **Owner:** Peter Double · **Status:** approved design,
  pre-implementation
- **Closes:** enhancements backlog #1 (fully) and #27(a) (competitive sweep as
  a research lens). #27(b) (Jira gap analysis) is re-scoped as a future
  `hub.research` mode gated on backlog #2 (Jira hub skills).

## Problem

The highest-frequency PM workflow — learning about something new (upstream
project, DP feature, competitive move) and getting it into the hub as
structured entries — has no guided path. Today: `/deep-research` → manually
split output into typed entries → scaffold a partition by hand → reindex.
Research output has no organization contract, no refresh story, and no hub
awareness (it doesn't read what the hub already knows).

## Decisions made during brainstorming

1. **Research output contract:** numbered series + gated knowledge entries +
   living synthesis. Re-runs refresh `00-executive-summary` and mark
   superseded findings — a living research base per feature.
2. **#27 split:** competitive sweep (domain YAML configs) ships now as a
   `hub.research` lens; Jira gap analysis waits for #2 and becomes a named
   future mode.
3. **Depth:** the skill sizes the topic and proposes quick/standard/deep with
   expected output; the user confirms or overrides before any fan-out.
4. **Intake scope:** one skill for both new-feature onboarding and bulk
   source-adding to existing features; partition creation is step zero when
   needed.
5. **Lens scoping via prompt:** naming lenses in the invocation ("competitive
   research only on mcp-gateway") runs exactly those lenses; naming none gets
   the full sizing proposal with editable lens set.

## Architecture

Two new skills in the `hub.*` namespace (both maintain hub structure through
gates — the operational family, per /docs/skills.md).

### hub.intake — the guided multi-source front door

One flow for onboarding a new feature and for bulk-adding sources to an
existing one. Reuses, never duplicates:

- Source filing follows `hub.file`'s procedure (canonical URIs, ref- entries,
  transcript handling, restricted routing). `hub.file` stays as-is for
  one-off filing.
- Entry-extraction gating follows `hub.consolidate`'s batch pattern.

### hub.research — standalone deep research on a feature or narrative topic

Built around **lenses** as the unit of scoping:

| lens | looks for |
|---|---|
| `landscape` | definitions, state of the art, best practices |
| `upstream` | OSS projects, standards, protocols, relevant repos |
| `architecture` | patterns, reference architectures, build-vs-buy shapes |
| `requirements` | capability expectations, enterprise needs, persona demands |
| `competitive` | competitor moves, analyst coverage — driven by domain YAML configs |
| *(future)* `jira-gap` | "NOT building" analysis — activates when backlog #2 lands |

### Shared convention — conventions/research.md (new)

Pins the series contract so both skills, the linter, and future skills agree:

- Numbering: `00-executive-summary.md` (living synthesis), `01..N` one doc
  per lens/subtopic, `REVIEW-NOTES.md` for human rulings. Refresh runs
  continue existing numbering.
- Research-doc frontmatter: `title`, `description`, `timestamp`, `lens`
  (or `source` for migrated docs), `review_after`.
- Refresh/supersede rules: contradictions get a supersede note in the old
  doc, never deletion; `00` is rewritten each refresh.

The existing `features/agent-memory/research/` series is the reference model
and the richest refresh-test fixture.

### Relationship to the built-in /deep-research

`hub.research` replaces that workflow for hub topics. It may use the same
underlying tools (web search/fetch, parallel agents) but owns its flow:
output organization, gating, and hub context (reading existing entries
first) are the point. `/deep-research` remains for non-hub questions.

## Component flows

### hub.intake (.claude/skills/hub.intake/SKILL.md)

1. **Gather** — topic + sources from the prompt (URLs, GDocs, Slack
   permalinks, Jira/RFE links, transcript files, pasted text). Ask once for
   anything obviously missing.
2. **Route home** — match against `features/features.yaml` and narrative/;
   if nothing fits, propose a new partition (id, title, one-line
   description) exactly as `hub.file` step 1. A new partition also gets a
   starter `fact-<id>-overview.md` (what it is, status, key links).
3. **File sources** — each per `hub.file`'s procedure: canonical URI, ref-
   entry with load-bearing description, transcripts → `work/transcripts/`
   (gitignored), NDA-adjacent → `restricted/`. Jira/RFE links get a ref-
   entry with the URL only until #2 provides field ingestion.
4. **Extract entries** — read the sources; propose typed entries (`fact-`,
   `decision-`, `question-`, `qa-`, `person-`) found inside them.
5. **Batch gate** — one consolidate-style table: every proposed write, one
   line each, public/restricted call per item, approve/edit/reject.
6. **Commit** — reindex, lint (0 errors), single commit
   `intake(<home>): <topic>`.
7. **Offer research** — "run hub.research on this now?" with a suggested
   lens set. Never auto-runs.

### hub.research (.claude/skills/hub.research/SKILL.md)

1. **Context load** — read the home's `knowledge/index.md`, existing
   `research/` series, and open `question-` entries; open questions become
   research inputs.
2. **Size & propose** — fresh vs. refresh, proposed lenses × depth
   (quick/standard/deep), expected output ("standard: 4 docs + entries,
   ~15 sources/lens"). Prompt-scoped lenses land here; user confirms.
   Depth shapes: quick = single agent, 1–2 docs; standard = 3–4 lens
   agents; deep = full lens set including competitive, with adversarial
   source verification.
3. **Fan out** — parallel research agents, one per lens (quick runs a
   single agent, no fan-out). Each agent gets the hub context summary + its
   lens brief; competitive agents also get the matching domain YAML.
4. **Write series** — one numbered doc per lens under `<home>/research/`,
   continuing numbering on refresh; rewrite `00-executive-summary` as the
   living synthesis; supersede notes into contradicted docs.
5. **Propose entries** — decision-ready atoms (facts, refs to key sources,
   new open questions, answers to existing ones) → same batch gate as
   intake.
6. **Commit** — reindex, lint, single commit
   `research(<home>): <lenses> <depth>`.

### Domain configs

`.claude/skills/hub.research/domains/*.yaml`, seeded with `redhat-ai.yaml`
(competitors, search areas, analyst coverage, partner ecosystem — reshaped
from pm-toolkit's research skill). The competitive lens picks a config by
feature match or asks; no matching config means generic competitor search.

## Data flow & gating

| source | tool path | destination rules |
|---|---|---|
| Web (search, blogs, docs, analyst posts) | WebSearch / WebFetch | public — research docs + entries |
| GitHub repos/issues | WebFetch / `gh` | public |
| Google Docs/Drive | Google Drive MCP | judgment call; NDA-adjacent → restricted/ |
| Slack threads | Slack MCP | content summarized into entries; asker/customer identity → restricted/ sibling (hub.capture qa rule) |
| Jira/RFE links | URL only (until #2) | ref- entries, public |
| Customer tracker | rhai-tracker MCP / restricted tracker | read allowed as input; any finding citing it → restricted/, never tracked |
| Transcripts / local files | filesystem | raw → work/transcripts/ (gitignored); extracted entries gated |

**Two-stage gate:**

1. **Plan gate** (before fan-out): lenses, depth, domain config, target
   paths. This is where cost is controlled; the plan is a hard cap.
2. **Write gate** (before any commit): one batch table — every file, one
   line: `path: description [public|restricted] [new|update|supersede]`.
   Research docs gate at line level with full content on request; knowledge
   entries gate as in hub.consolidate. Nothing is written before this gate;
   reject drops the item, edit adjusts it.

**Public-repo discipline (standing rules in both SKILL.md files):**
customer names/deal context never leave restricted/; anything sourced from
the tracker or NDA-marked GDocs routes restricted regardless of how generic
the finding looks; dollar figures and agreement language are never written
to tracked files (they trip the lint heuristics by design).

Research series are tracked files and sync via git; only transcripts and
restricted mirrors stay local (existing contract, unchanged).

## Error handling

- **Partial fan-out failure:** report which lenses completed; write only
  completed docs; record the gap in `00-executive-summary` with the exact
  retry invocation. Never silently pretend coverage.
- **Unreachable sources:** intake still files the ref- entry with a
  `fetch failed` note in the gate line; research notes shrunken source
  lists in the doc's source section.
- **MCP unavailability:** say so, offer the degraded path (paste content),
  point at `hub.doctor check`. No retry loops.
- **Refresh contradictions:** surfaced as pairs in the write gate with a
  proposed supersede — never auto-resolved.
- **Interrupted runs:** nothing touches disk before the write gate; the
  post-gate tail (reindex → lint → commit) is idempotent and re-runnable.
  Lint errors are fixed in the written content, never in the scripts.
- **Runaway scope:** the plan gate's agent/doc counts are a hard cap;
  mid-run discoveries yield a "recommend follow-up run" note, not silent
  expansion.

## Verification & acceptance

**Machine verification:** existing chain unchanged — `hub_lint.py` 0
errors, `hub_index.py --check` clean, `pytest scripts/tests` green. One
code change rides along: the linter learns the research-doc frontmatter
contract for `research/*.md` as **warnings only** (missing
description/timestamp) — the 21 pre-convention agent-memory docs must not
go red.

**Docs in scope:** AGENTS.md skills-table rows (two lines, mind the
150-line CI budget), docs/skills.md sections for both skills + the
intake→research chain, conventions/research.md (new), and
docs/enhancements.md (#1 → Done; #27 rewritten: (a) shipped as the
competitive lens, (b) jira-gap mode gated on #2).

**Acceptance — one live run each:**

1. `hub.intake` on a genuinely new small topic: partition created, 2–3
   sources filed, entries gated, CI green after push.
2. `hub.intake` against an existing feature with new sources (bulk-add
   path).
3. `hub.research` quick run, single lens, on the new partition — series
   born with `00` + one lens doc.
4. `hub.research` scoped run — "competitive only" on an existing feature
   with `redhat-ai.yaml` — verifies prompt scoping + domain configs.
5. Stretch (run early — richest fixture): refresh on
   `features/agent-memory/research/` — numbering continues at 19, `00`
   refresh proposed through the gate.

## Out of scope

- Jira field ingestion and the `jira-gap` lens (backlog #2 / #27(b)).
- Any change to `hub.file`, `hub.capture`, `hub.consolidate` behavior.
- Auto-publishing of research output (publishing stays a per-artifact
  `hub.publish` decision, permanently).
- Embedding/vector search — the partition/type/index system remains the
  retrieval design.
