---
type: question
title: Agent memory governance layer — Feast (which proposal) vs. MemoryHub vs. other?
description: Two separate Feast-based proposals (Zarecki's Feast+OGX, Manganiello's Unified Platform) and MemoryHub all cover overlapping governance-layer territory for RHAISTRAT-1345 — none is the current direction.
status: open
timestamp: 2026-07-06
tags: [agent-memory, feast, memoryhub, governance]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
Three proposals overlap on the same problem (a governed memory layer: scope tiers, audit, provenance, PII/contradiction handling) and none is the settled direction:
- Jonathan Zarecki's Feast+OGX proposal — [ref-feast-ogx-agent-memory-proposal.md](/features/agent-memory/knowledge/ref-feast-ogx-agent-memory-proposal.md)
- Umberto Manganiello's Unified Platform (3-phase Feast) proposal — [ref-unified-platform-agentic-memory-infrastructure.md](/features/agent-memory/knowledge/ref-unified-platform-agentic-memory-infrastructure.md)
- Wes Jackson's MemoryHub — [ref-memory-hub-repo.md](/features/agent-memory/knowledge/ref-memory-hub-repo.md)

Open questions: if MemoryHub's IP/copyright blocker is resolved, should the Feast team's Write-loop phase adopt MemoryHub's curation engine rather than building Mem0 integration from scratch — or should all three remain separate options evaluated at the July 2026 architecture review? Do Zarecki's and Manganiello's Feast proposals themselves need to converge before that review?

Update 2026-07-10: the 2026-07-07 sync effectively ruled **Feast out as
the interim memory path** — its own maintainer (Francisco Arceo) called a
feature store the wrong fit ("just because it can doesn't mean it
should"), and the interim slot now belongs to the OGX memory tool +
MemoryHub pair ([sync fact](/features/agent-memory/knowledge/fact-agent-memory-team-sync-20260707-transcript.md)).
Zarecki's presentation may still happen; the question stays open until
Sanjeev's architecture doc lands the governance-layer choice.
