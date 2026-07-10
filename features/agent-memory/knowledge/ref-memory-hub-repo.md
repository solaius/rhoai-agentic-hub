---
type: reference
title: redhat-ai-americas/memory-hub (GitHub)
description: MemoryHub — Red Hat AI Americas' governed agent memory prototype on OpenShift AI (PostgreSQL+pgvector, 14 MCP tools).
resource: https://github.com/redhat-ai-americas/memory-hub
tags: [agent-memory, prototype, github]
timestamp: 2026-07-06
source: ai-asset-registry/docs/knowledge-registry.md §12 (as of 2026-07-05)
review_after: 2026-08-05
---
Author: Wes Jackson / RH AI Americas. PostgreSQL+pgvector backing (relational/vector/graph), FastMCP server (14 tools), Python SDK + CLI, PatternFly dashboard, OAuth 2.1. Five-tier scope isolation (user/project/role/organizational/enterprise), version history + contradiction detection, curation rules engine, cache-optimized assembly for KV-cache hits. Also carries Wes's benchmark research under `research/agent-memory-benchmarks` (shared in the 2026-06-30 sync).

Status (2026-07-10): under active team evaluation as the leading 3.6
governance-layer candidate (Sanjeev leaning MemoryHub as the 3.6 basis —
[1:1 fact](/features/agent-memory/knowledge/fact-agent-memory-1on1-paths-forward-20260630.md));
known gaps are second-order (Claude-Code-centric triggers/hooks, missing
prompt hooks — [07-07 sync](/features/agent-memory/knowledge/fact-agent-memory-team-sync-20260707-transcript.md)).
IP transfer in writing remains a prerequisite. Evaluate alongside the OGX
memory tool interim candidate rather than treat as settled.
