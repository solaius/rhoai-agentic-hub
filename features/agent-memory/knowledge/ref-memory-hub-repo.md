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
Author: Wes Jackson / RH AI Americas. PostgreSQL+pgvector backing (relational/vector/graph), FastMCP server (14 tools), Python SDK + CLI, PatternFly dashboard, OAuth 2.1. Five-tier scope isolation (user/project/role/organizational/enterprise), version history + contradiction detection, curation rules engine, cache-optimized assembly for KV-cache hits. Explicitly a reference/comparison point in the old registry, not an adopted direction — evaluate against [ref-feast-ogx-agent-memory-proposal.md](/features/agent-memory/knowledge/ref-feast-ogx-agent-memory-proposal.md) rather than treat as settled.
