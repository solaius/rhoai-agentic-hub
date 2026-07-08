# History & lineage

This repo is the intentionally-designed successor to
[ai-asset-registry](https://github.com/solaius/ai-asset-registry) — the
organically-grown repo where the same PM work lived from 2026-02 through
2026-07. Rather than refactor in place, the hub was chartered, designed,
built, and then seeded by migrating the old repo's full text content through
gated review batches. The old repo remains as a read-only archive.

## Timeline

| date | event |
|---|---|
| 2026-07-05 | Charter written and approved (mission, five problems, three pillars, memory goals B→A→C) |
| 2026-07-05 | Design spec approved — the eleven design decisions D1–D11 (see [/docs/architecture.md](/docs/architecture.md)) |
| 2026-07-05 → 06 | Core built task-by-task from the implementation plan (subagent-driven, reviewed per task) — layout, conventions, memory system, `hub.*` skills, scripts, CI, publishing → tagged **`v0.1-core`** |
| 2026-07-06 | **R2** — the old repo's `docs/knowledge-registry.md` monolith (1,105 lines, 13 topic sections) decomposed in 4 gated batches into typed entries across the feature partitions |
| 2026-07-06 | **Batch 5** — `knowledge-review/` parity pass (most files proven already covered; deltas and documents brought over) |
| 2026-07-06 | **Batch 6** — workspace document parity: the old repo's research/strategy/work documents (agent-memory research series, agent-registry, skills-registry, …) → **full text parity** with the old repo |
| 2026-07-06 | **R3** — the per-machine `~/.claude` project memory seeded into `memory/facts/` |
| 2026-07-06 | **R4 wave 1** — `presentation-create` ported (reviewed-and-adapted, not lift-and-shift); first artifact published: the MCP Registry catalog deck |
| 2026-07-06 | **R4 wave 2** — `blog-create` + `blog-mockup` ported (blog guide co-located as a skill reference) |
| 2026-07-06 | **R4 wave 3** — customer-feedback suite ported; tracker data model moved to `restricted/`; rhai-tracker doctor section added |
| 2026-07-08 | **R4 wave 4** — Slack + Google Workspace MCP setup ported: doctor sections 8–9 (Claude-config write, podman runtime), `restricted/.env` sourcing, [/docs/mcp-servers.md](/docs/mcp-servers.md) |

## Where the full records live

The founding documents and the complete migration audit trail are in the old
repo (public, so these links resolve for anyone):

| record | location |
|---|---|
| Vision & direction charter | [docs/superpowers/specs/2026-07-05-rhoai-agentic-hub-charter.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/superpowers/specs/2026-07-05-rhoai-agentic-hub-charter.md) |
| Design spec (D1–D11, full text) | [docs/superpowers/specs/2026-07-05-rhoai-agentic-hub-design.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/superpowers/specs/2026-07-05-rhoai-agentic-hub-design.md) |
| Implementation plan | [docs/superpowers/plans/2026-07-05-rhoai-agentic-hub-build.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/superpowers/plans/2026-07-05-rhoai-agentic-hub-build.md) |
| Migration report — every batch, ruling, count, and verification | [docs/migration/2026-07-06-hub-migration-report.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/migration/2026-07-06-hub-migration-report.md) |

For headline numbers (files migrated, entries per partition, what was
dropped and why), trust the migration report over any figure quoted
elsewhere — it is the audit trail.

## Relationship to the old repo

- **Read-only source material.** New work happens here; the old repo is
  never edited (its one post-migration change was retiring a dead proposal
  and adding the migration report).
- **Migrate on touch (D6).** Remaining old-repo content — chiefly the HTML
  enablement sites (MCP Gateway Knowledge Hub, presentation decks) — comes
  over via `hub.migrate` the first time work actually touches it, not in a
  bulk copy.
- **Legacy URLs stay live.** The old repo's GitHub Pages site
  (`solaius.github.io/ai-asset-registry/`) has been shared widely and keeps
  serving; artifacts move to the hub's pages site individually, when
  migrated and republished.
- **Names differ deliberately in one place:** the old repo's embedded
  customer names in skill texts were left as-is (owner ruling); the hub's
  copies are scrubbed, with customer data confined to `restricted/`.

## Known parked items

Deliberately deferred, in rough priority order:

- `hub.refresh-site` (successor to the old repo's knowledge-hub-create /
  update-hub skills) — port at the next piece of hub-site work.
- `rice-strats` skill port — the rubric it needs is already here at
  `features/platform/strategy/rice-scoring-rubric.md`.
- Remaining old-repo-doctor coverage: `~/.bashrc` shell-env wiring (so
  `JIRA_*` reaches every shell, keeping the deliberate exclusion of
  LLM-provider credentials) and the Jira/Slack connectivity probes — needed
  the first time Jira-using skills (`rfe.*`, `rice-strats`) run on a
  hub-only machine, where nothing else exports `JIRA_*` into the shell.
  (The doctor itself now sources `restricted/.env` — with the same LLM-cred
  exclusion — for its own run, and the Slack-MCP/podman sections were
  ported in R4 wave 4; only the `~/.bashrc` wiring and probes remain.)
- Old-repo HTML enablement artifacts — migrate on touch, per D6.
- Two open content flags, tracked in the entries themselves: the
  security-pipeline schema future-vs-superseded note, and two inferred
  source links on §10 strategy facts.

## What `v0.1-core` marks

The tag (`hub core: layout, conventions, memory system, skills, CI,
publishing`) is the last commit of the *built system* before any content
migration — useful as the clean baseline if you ever want to see the
machinery without the content, or to fork the pattern for another hub
(the eventual `rhoai-atlas` template idea from the charter).
