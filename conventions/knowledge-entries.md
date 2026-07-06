# Knowledge entry conventions

Files are `<prefix><slug>.md` per the prefix table in
[type-vocabulary.md](/conventions/type-vocabulary.md), lower-kebab-case slugs.

Skeleton (a `reference`, the most common type):

    ---
    type: reference
    title: MCP Registry 3.5 PRD
    description: PRD for Dev Preview — scope, personas, MVP cut
    resource: https://docs.google.com/document/d/<id>
    tags: [prd, dev-preview]
    timestamp: 2026-07-05
    ---
    Why it matters, what's inside, what to read first.

Rules:
- One entry = one thing with standalone value. Start coarse; split a file only
  when its parts change at different rates.
- `description` is load-bearing: indexes, views, and agent routing read it.
- Bodies are short prose; link out (`resource`, citations) rather than copy in.
- Superseding: set `status: superseded` + `superseded_by:` on the old entry;
  write the new one; never delete.
- OKF v0.1 conformance (pinned as of 2026-07-05): frontmatter with `type` on
  every entry; `index.md`/`log.md` reserved; extension keys above are
  documented producer extensions per spec §4.1.
