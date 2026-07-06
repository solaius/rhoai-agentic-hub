# Layout conventions

## The two filing questions
Every addition answers: **which feature? which type?**
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
| `strategy/`  | strategy docs, RFE roadmaps, outcomes |
| `enablement/`| one subdirectory per artifact (deck, hub site, blog) |
| `work/`      | active drafts, RFE pipeline artifacts, `transcripts/` (gitignored) |

Anything else directly under a feature is a lint **error**. `platform/` is the
cross-cutting pseudo-feature (releases, people, personas, SKUs, org strategy).

## Generated files — never hand-edit
`features/index.md`, `features/*/index.md`, `features/*/knowledge/index.md`,
`memory/index.md`, `views/*` — regenerate with `python scripts/hub_index.py`.
CI fails when they are stale.

## Links
Leading-slash repo-root form: `[text](/features/mcp-registry/knowledge/x.md)`.
Dangling links are allowed (they mark not-yet-written knowledge); the linter
warns only.

## restricted/
Gitignored, local-only. Mirrors this layout (`restricted/features/...`,
`restricted/memory/...`). Same conventions apply; the linter checks it locally
when present.
