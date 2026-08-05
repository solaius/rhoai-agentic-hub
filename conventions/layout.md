# Layout conventions

## Vocabulary: components and features

- A **component** is an item in `components/` — a thing that exists in
  RHOAI (MCP Gateway, Agent Catalog, ...). Partitions under
  `components/` are component partitions.
- A **feature** is functionality added to a component (what a RHAISTRAT
  Feature ticket describes). The hub does not model features
  structurally; the word is reserved for that meaning.
- Components map loosely to **Jira components** — not 1:1 (the catalogs
  and registries land in the "AI Hub" Jira component). The mapping
  lives in `components/components.yaml` as `jira_component:`.
- Components have (or can create) **Jira labels** — always lowercase
  (e.g. `mcp-catalog`), stored as `jira_labels:`; lint enforces case.
- Jira issue types keep their own names: `Feature` and `Feature Request`
  in JQL, `ref_types:`, and prose always mean the Jira issue types.

## The filing questions
Every addition answers: **which home — `narrative/` (story-shaped) or which
component? which type?**
- Component list = `components/components.yaml` (the routing table; `components/index.md` is generated from it).
- Types = [type-vocabulary.md](/conventions/type-vocabulary.md).
- Working context vs domain knowledge boundary = [memory.md](/conventions/memory.md).

## Component skeleton contract
Every `components/<id>/` contains exactly these subdirectories (created on first
use, never pre-created empty):

| dir | holds |
|---|---|
| `knowledge/` | typed entries only, plus generated `index.md` |
| `research/`  | deep documents (numbered series optional) |
| `strategy/`  | strategy docs, RFE roadmaps, outcomes — `strategy.md` is the living per-component strategy doc ([strategy.md](/conventions/strategy.md)) |
| `enablement/`| one subdirectory per artifact (deck, hub site, blog) |
| `prototype/` | one subdirectory per prototype holding `prototype.yaml` (v2: fork branch + preview URL); generated pages live in the UXD fork, not this repo |
| `work/`      | active drafts, RFE pipeline artifacts, `transcripts/` (gitignored), `jira-snapshot.yaml` (machine-written by hub.jira-sweep; tracked), `triage-log.yaml` (machine-written by hub.jira-triage; tracked; carries no Jira prose by design, so it needs no redaction in this PUBLIC repo) |

Anything else directly under a component is a lint **error**. `platform/` is the
cross-cutting pseudo-component (releases, people, personas, SKUs, org process —
story/strategy content lives in /narrative/).

### Prototype structure

Each `prototype/<slug>/` holds exactly one file, `prototype.yaml`:

- required: `title`, `description`, `status` (active | superseded |
  archived), `components` (list of component ids), `source_repo`,
  `branch` (fork branch, usually = slug), `base` (e.g. `upstream/3.6`),
  `preview_url` (`<pages_base_url>/branch-<branch>/`), `current` (a key
  of `versions`), `versions` (map `vN -> {timestamp, commit, summary}`;
  `commit` is a fork sha, or `static` on migrated static-era entries)
- optional: `snapshots` (map `vN -> {branch, preview_url}` for frozen
  side-by-side branches), `mr_url` (set when upstreamed)

The React pages themselves live in the UXD fork
(`conventions/prototype-fork.yaml` points at it), one branch per
prototype based off `upstream/3.6`. Cross-component prototypes keep their
metadata in `narrative/prototype/<slug>/`.

## Component families
`related:` in `components/components.yaml` declares a component's boundary
siblings — e.g. the agent family (agent-registry · agent-interop ·
agent-catalog) and the mcp family (mcp-gateway · mcp-catalog ·
mcp-lifecycle-operator · mcp-registry · mcp-ecosystem). Closed vocabulary:
ids must exist in the routing table (lint error), no self-reference, and
keep it symmetric (the linter warns on one-way links). Consumers: the
generated component index (Related line), `hub.research` (siblings are
standing context in every lens brief), `hub.sweep` (boundary-drift
candidates). This is partition-level wiring; per-entry spread is still the
`components:` list.

## The narrative layer
`narrative/` is a peer of `components/` holding the connective story — pillars,
cross-component stories, the strategy spine, cross-component artifacts. Same
five-dir skeleton and rules as a component. Route here only when content would
be *wrong* under any single component; otherwise pick the primary component and
declare the spread with `components:` (see
[type-vocabulary.md](/conventions/type-vocabulary.md)). `pillar-` / `story-`
entries live only here.

## Generated files — never hand-edit
`components/index.md`, `components/*/index.md`, `components/*/knowledge/index.md`,
`narrative/index.md`, `narrative/knowledge/index.md`, `memory/index.md`,
`views/*` — regenerate with `python scripts/hub_index.py`.
CI fails when they are stale.

## Links
Leading-slash repo-root form: `[text](/components/mcp-registry/knowledge/x.md)`.
Dangling links are allowed (they mark not-yet-written knowledge); the linter
warns only.

## restricted/
Gitignored, local-only. Mirrors this layout (`restricted/components/...`,
`restricted/memory/...`). Same conventions apply; the linter checks it locally
when present.
