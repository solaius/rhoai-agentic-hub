# Research series conventions

`research/` directories (feature or narrative skeleton) hold deep
documents — the numbered-series contract below. Typed atoms (facts, refs,
questions) belong in `knowledge/`, not here; research runs propose them
separately through the gate.

## The series

- `00-executive-summary.md` — the living synthesis. Rewritten on every
  refresh; lists every doc in the series; records lens gaps with the exact
  retry invocation ("competitive lens not run — retry with
  `hub.research <home> competitive`").
- `01..N` — one doc per lens or subtopic, filename `NN-<slug>.md`.
  Numbering never restarts; refresh runs continue where the series left
  off.
- `REVIEW-NOTES.md` — human rulings on the series (what is DECIDED vs
  EXPLORATORY). Written by the owner, never by research runs. No
  frontmatter required.

## Frontmatter (research docs)

`title` · `description` (one line, written for someone deciding whether
to open it) · `timestamp` (ISO date) · `lens`
(`landscape|upstream|architecture|requirements|competitive|jira-gap` —
omit for pre-convention or migrated docs; `source:` marks migrated
provenance) ·
`review_after` (ISO date). The linter checks `description` and
`timestamp` as **warnings only** — research docs never fail the build.
`index.md` and `REVIEW-NOTES.md` are exempt.

## Refresh & supersede

- A refresh rewrites `00-executive-summary.md` and appends new numbered
  docs; it never deletes.
- A finding contradicted by newer research gets a supersede note **in the
  old doc** — a blockquote directly under its H1:
  `> Superseded <YYYY-MM-DD> by [NN-slug](NN-slug.md) — <one line why>.`
  The old doc keeps its place in the series.
- Conflicts between new findings and existing knowledge entries are
  surfaced at the write gate, never auto-resolved.

## Producers

`hub.research` (primary), `hub.intake` (offers the kickoff),
`hub.migrate` (imports old-repo series; `source:` marks provenance).
The reference series:
[agent-memory research](/features/agent-memory/research/00-executive-summary.md).
