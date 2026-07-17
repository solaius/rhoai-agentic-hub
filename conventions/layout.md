# Layout conventions

## The filing questions
Every addition answers: **which home — `narrative/` (story-shaped) or which
feature? which type?**
- Feature list = `features/features.yaml` (the routing table; `features/index.md` is generated from it).
- Types = [type-vocabulary.md](/conventions/type-vocabulary.md).
- Working context vs domain knowledge boundary = [memory.md](/conventions/memory.md).

## Feature skeleton contract
Every `features/<id>/` contains exactly these subdirectories (created on first
use, never pre-created empty):

| dir | holds |
|---|---|
| `knowledge/` | typed entries only, plus generated `index.md` |
| `research/`  | deep documents (numbered series optional) |
| `strategy/`  | strategy docs, RFE roadmaps, outcomes — `strategy.md` is the living per-feature strategy doc ([strategy.md](/conventions/strategy.md)) |
| `enablement/`| one subdirectory per artifact (deck, hub site, blog) |
| `work/`      | active drafts, RFE pipeline artifacts, `transcripts/` (gitignored), `jira-snapshot.yaml` (machine-written by hub.jira-sweep; tracked), `triage-log.yaml` (machine-written by hub.jira-triage; tracked; carries no Jira prose by design, so it needs no redaction in this PUBLIC repo) |

Anything else directly under a feature is a lint **error**. `platform/` is the
cross-cutting pseudo-feature (releases, people, personas, SKUs, org process —
story/strategy content lives in /narrative/).

## Feature families
`related:` in `features/features.yaml` declares a feature's boundary
siblings — e.g. the agent family (agent-registry · agent-interop ·
agent-catalog) and the mcp family (mcp-gateway · mcp-catalog ·
mcp-lifecycle-operator · mcp-registry · mcp-ecosystem). Closed vocabulary:
ids must exist in the routing table (lint error), no self-reference, and
keep it symmetric (the linter warns on one-way links). Consumers: the
generated feature index (Related line), `hub.research` (siblings are
standing context in every lens brief), `hub.sweep` (boundary-drift
candidates). This is partition-level wiring; per-entry spread is still the
`features:` list.

## The narrative layer
`narrative/` is a peer of `features/` holding the connective story — pillars,
cross-feature stories, the strategy spine, cross-feature artifacts. Same
five-dir skeleton and rules as a feature. Route here only when content would
be *wrong* under any single feature; otherwise pick the primary feature and
declare the spread with `features:` (see
[type-vocabulary.md](/conventions/type-vocabulary.md)). `pillar-` / `story-`
entries live only here.

## Generated files — never hand-edit
`features/index.md`, `features/*/index.md`, `features/*/knowledge/index.md`,
`narrative/index.md`, `narrative/knowledge/index.md`, `memory/index.md`,
`views/*` — regenerate with `python scripts/hub_index.py`.
CI fails when they are stale.

## Links
Leading-slash repo-root form: `[text](/features/mcp-registry/knowledge/x.md)`.
Dangling links are allowed (they mark not-yet-written knowledge); the linter
warns only.

## restricted/
Gitignored, local-only. Mirrors this layout (`restricted/features/...`,
`restricted/memory/...`). Same conventions apply; the linter checks it locally
when present.
