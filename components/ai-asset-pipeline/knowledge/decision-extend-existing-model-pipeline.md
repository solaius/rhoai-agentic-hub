---
type: decision
title: Extend the existing model trust pipeline to skills, MCP servers, and agents
description: Adam Bellusci (AI Hub owner) confirmed 2026-08-03 -- push additional AI asset types into the existing model pipeline (Konflux, RHTAS, model-metadata-collection), not a new standalone system.
decided: 2026-08-03
timestamp: 2026-08-03
tags: [ai-asset-pipeline, architecture, decision]
components: [ai-asset-pipeline, skills-catalog, mcp-catalog, agent-catalog]
review_after: 2027-02-03
source: Slack conversation with Adam Bellusci 2026-08-03
---

## Context

The skills supply chain threat landscape (36.8% of public skills have
security flaws, 1,100+ poisoned on ClawHub) requires a trust pipeline
for scanning, signing, and attesting skills before they enter the
catalog. The same threats apply to MCP servers and agents.

The question was whether this trust pipeline is a brand-new component or
an extension of what already exists for models.

## Decision

**Extend the existing model trust pipeline.** Adam Bellusci (Senior
Principal Product Manager, AI Hub owner) confirmed that additional asset
types (skills, MCP servers, agents) will be pushed into the existing
pipeline infrastructure:

- **Konflux** provides SLSA L3 builds, Tekton pipelines, signing
- **RHTAS/Sigstore** provides signing and attestation (already used for
  ModelCar images)
- **model-metadata-collection** already handles models AND MCP servers
  (extends to skills and agents)
- **Conforma** provides policy-as-code release gating

Not a new standalone system. The only genuinely new work is per-asset-type
validation Tekton tasks (scan profiles for skills, MCP servers, agents).

## Consequences

- No new infrastructure to deploy -- reuses existing Konflux, Quay,
  Sigstore, Conforma
- The pipeline component (ai-asset-pipeline) tracks the cross-asset
  trust work as a unified workstream
- First implementation targets skills (smallest artifact, most urgent);
  extends to MCP servers and agents
- Jira work belongs under RHAISTRAT-1339 (AI Hub AI Asset Delivery) or
  a new cross-cutting STRAT, not under any single asset type
