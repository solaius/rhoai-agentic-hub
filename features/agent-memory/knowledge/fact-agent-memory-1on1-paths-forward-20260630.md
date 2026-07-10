---
type: fact
title: "Agent memory 1:1 — paths forward (Peter × Sanjeev, 2026-06-30)"
description: Standalone-service architecture position (decoupled from OGX AND AI Gateway), multi-backend requirement, substrate/intelligence/governance layering, and the revised phasing — 3.6 DP → 3.7 TP (Feb 2027) → 3.8 GA (Summit 2027).
tags: [agent-memory, architecture, roadmap, meeting]
timestamp: 2026-07-10
source: meeting transcript 2026-06-30 (work/transcripts/, local); participants Peter Double, Sanjeev Rampal
---

30-min 1:1 on architecture direction and release phasing. Key positions:

- **Standalone service**: Sanjeev's strong position — agent memory should be
  its own service, "not entirely coupled to either OGX or a gateway"
  (gateways are network devices; memory is a database/server-side
  function). Peter agrees. Coexistence with those layers stays possible;
  dependence does not.
- **Multi-backend, not "the Postgres+pgvector solution"**: support multiple
  memory structures — vector DB + file system minimum, extensible (graph);
  "agent memory as a service" naming preferred.
- **Candidates-per-layer framing** (Peter's gap-analysis deck): raw
  substrate / memory intelligence (LLM extraction — Mem0 partial fit) /
  governance & scope (MemoryHub strongest: six tiers, most features;
  [Sanjeev](/features/agent-memory/knowledge/person-sanjeev-rampal.md)
  leaning MemoryHub as the 3.6 basis). Feast enters as a candidate (in
  product, RBAC built in, independent of OGX, MCP server coming;
  [Zarecki](/features/agent-memory/knowledge/person-jonathan-zarecki.md)
  to present).
- **Phasing revised**: 3.6 = **DP deliberately, not TP** (freedom to swap
  parts — "get-out-of-jail" flexibility; TP carries support/docs/sales
  obligations); 3.7 (Feb 2027) = TP, sets up a Red Hat Summit 2027 demo;
  3.8 (Summit drop) = GA target. Supersedes the research series' earlier
  "3.7+ GA" sketch.
- **Org constraint**: leadership's 12-month priority list (8 topics)
  excludes agent memory — "not a 2026 topic, a 2027 topic." Response:
  scope basics, file specific RFEs (target: week of 2026-07-07), lean on
  the few real customer asks for prioritization.
- **MemoryHub IP**: Wes is willing; Peter requires the transfer in
  writing/license before productization.
- **ODH single-vendor tension**: AI projects land in Open Data Hub (SKU
  pressure) → implicitly single-vendor open source; community strategy
  unresolved.
