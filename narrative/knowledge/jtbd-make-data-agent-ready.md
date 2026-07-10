---
type: jtbd
title: "Make my data agent-ready"
description: "When I deploy agents that need enterprise knowledge, I want my data to be discoverable, fresh, and governed, so agents produce grounded answers instead of hallucinations."
persona: platform-engineer
status: candidate
timestamp: 2026-07-10
source: narrative/research/02-agentic-requirements-landscape.md
tags: [narrative, jtbd, data, rag, research-gap]
---
**When** I deploy agents that need enterprise knowledge,
**I want to** make my data discoverable, fresh, and governed for agent
consumption,
**so** agents produce grounded, accurate answers instead of
hallucinations and I can trust their outputs.

**Evidence (from research):**
- 52% of enterprises cite data quality as the biggest production blocker
  [doc 02, source 3]
- 60% of RAG failures trace to freshness and consistency, not retrieval
  quality [doc 02, source 23]
- 48% cite data searchability and 47% cite data reusability as challenges
  [doc 02, source 5]
- McKinsey: 58% of teams deploying standard RAG identified "multi-step
  reasoning over heterogeneous data sources" as their top limitation
  within 6 months [doc 02, source 23]
- Deloitte: three fundamental data obstacles — legacy integration, data
  architecture constraints, and data discoverability [doc 02, source 5]

**Gap vs existing JTBDs:** No current JTBD addresses the data/context
layer that agents depend on. This sits at the intersection of the Data
pillar and the Agents pillar — the knowledge graph, context engineering,
and data governance prerequisite for agents that produce trustworthy
outputs.

**Pillar:** Data × Agents (the intersection)
