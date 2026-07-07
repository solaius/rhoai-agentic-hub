# Working here — the daily loop

## The loop
1. Work normally. When a durable item surfaces (decision, date change,
   preference, useful link) → `hub.capture` files it in seconds, gated.
2. New source document/URL/transcript → `hub.file` (creates feature
   partitions on first use).
3. Session end (or "consolidate memory") → `hub.consolidate` sweeps
   `memory/.scratch/`, proposes promotions, you approve/reject each with a
   public-vs-restricted call, one commit.
4. Ship an artifact → `hub.publish` (manifest entry, disclosure confirm,
   CI does the rest).
5. Something from the old repo needed here → `hub.migrate` (reshapes to
   conventions; never edits the old repo).

## Filing by example
| the thing | where it goes |
|---|---|
| "3.5 DP moved to July" | `memory/profiles/roadmap.md` (profile edit + History) |
| gateway authz decision | `features/mcp-gateway/knowledge/decision-…md` |
| new PRD Google Doc | `features/mcp-registry/knowledge/ref-…md` (canonical `resource:`) |
| new stakeholder | `features/platform/knowledge/person-…md` |
| meeting transcript | `features/<f>/work/transcripts/` (gitignored) + a `ref-` entry |
| SKU/pricing detail | `restricted/features/…` — NEVER tracked |

Rules live in `/conventions/` — layout, type vocabulary, entry shapes, memory,
URIs, publishing. When in doubt, read the matching conventions file; it is
short.

## Adding a feature partition
Don't mkdir by hand — file the first piece of content with `hub.file` and
approve its "create partition" proposal (it updates `features/features.yaml`
and creates only the needed subdirectories).

## Keeping it healthy
`python scripts/hub_index.py` regenerates every index/view;
`python scripts/hub_lint.py` checks structure and schemas; CI runs both on
every push plus the test suite and the publish-manifest check.
`views/stale-facts.md` lists what needs a refresh — clear it during
consolidation.

## Further reading
Why it's shaped this way: [/docs/architecture.md](/docs/architecture.md) ·
the gate in depth: [/docs/memory.md](/docs/memory.md) · every skill:
[/docs/skills.md](/docs/skills.md) · shipping pages:
[/docs/publishing.md](/docs/publishing.md) · scripts & CI:
[/docs/tooling.md](/docs/tooling.md) · lineage: [/docs/history.md](/docs/history.md).

## Contributing (peers)
v1 is single-writer (Peter + agents). The contributor path, documented but
dormant: fork/branch → follow the same conventions (CI validates structure
mechanically) → PR; memory promotions in a PR must keep the gate discipline —
propose entries in the PR description, the owner applies them via
hub.capture/consolidate. When multi-writer becomes real, this section gets
promoted into a full CONTRIBUTING.md.
