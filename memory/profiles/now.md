---
type: profile
description: "Now: R2 COMPLETE (monolith fully decomposed, batches 1–4 + R3 seed) — 9 partitions — hub build at M1, memory system live"
timestamp: 2026-07-06
status: current
valid_from: 2026-07-06
review_after: 2026-07-20
---
- R2 is now complete: the old repo's monolith (`docs/knowledge-registry.md`)
  is fully decomposed across all 4 batches, and R3 (the `~/.claude` memory
  seed) is done. That monolith is now historical source material only —
  no more knowledge lives there that isn't also in this hub.
- Next: `docs/knowledge-review/` and workspace content (mcps/, agents/,
  agent-memory/, skills/, ai-assets/ presentations/transcripts/blog drafts)
  migrate on-touch, not as a scheduled batch. R4 (content-skill ports —
  presentation-create, blog-*, knowledge-hub-create, customer-feedback-*,
  rice-strats) is pull-driven, per real demand. Runbooks R5 (cross-machine
  continuity test) and R6 (Cursor end-to-end) run when ready.

## History
- 2026-07-06 — **Update** — superseded: "Hub build reached M1: memory
  system live — doctor configured on this machine, capture + consolidate
  skills landed. R2 batch 3 applied (monolith §5–§8) — 18 new + 7 edits +
  roadmap profile refreshed; next: batch 4 (§9–§11+§13 + R3), which
  completes R2." (source: R2 batch 4 apply)
- 2026-07-06 — **Update** — superseded: "R2 batch 2 applied (monolith
  §1+§2+§4) — 4 new entries + 4 edits; asset-registry partition removed
  (dead proposal; Kubeflow Hub entries moved to platform); 9 partitions;
  next: §5–§11+§13 and R3 seed." (source: R2 batch 3 apply)
- 2026-07-06 — **Update** — superseded: "R2 batch 1 applied: monolith
  §3+§12 migrated — 85 entries across 9 new partitions (mcp-gateway,
  mcp-registry, mcp-ecosystem, agent-registry, asset-registry, platform,
  agent-memory, agent-ops, gen-ai-studio). Next: §1/§2/§4, then the
  remaining monolith sections, then the ~/.claude seed (R3)." (source: R2
  batch 2 apply)
- 2026-07-06 — **Update** — superseded: "Daily PM work moves here at M1
  (memory live). Migrate-on-touch from the old repo; monolith decomposition
  is the M3 runbook." (source: R2 batch 1 apply)
- 2026-07-06 — **Update** — superseded: "Building rhoai-agentic-hub per the
  implementation plan in ai-asset-registry/docs/superpowers/plans/2026-07-05-rhoai-agentic-hub-build.md."
  (source: T12 consolidation smoke)
- 2026-07-05 — **Creation** at hub seed.
