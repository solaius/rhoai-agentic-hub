---
type: decision
title: MCP servers and agents are the top-priority asset types for RHOAI 3.5
description: A 2026-03-19 meeting decision setting MCP servers and agent registries as the highest-priority asset types for the 3.5 registry work, ahead of prompts/models/skills/guardrails.
decided: 2026-03-19
timestamp: 2026-07-06
tags: [platform, prioritization, mcp-registry, agent-registry]
source: ai-asset-registry/docs/knowledge-review/decisions/key-decisions.md (as of 2026-07-05)
review_after: 2026-08-05
---
**Context**: With multiple AI asset types in scope for the broader registry effort (MCP servers, agents, models, prompts, skills, guardrails, knowledge sources), the 2026-03-19 meeting needed to pick where to start.

**Decision**: MCP servers and agents are the highest-priority asset types for RHOAI 3.5 — ahead of models (already served by Kubeflow Hub), prompts (already served by MLflow Prompt Registry), skills (pending upstream Databricks work), and guardrails. Rationale given: growing enterprise demand for MCP governance, and a need for agent registries specifically to prevent "agent sprawl."

**Consequences**: This is the prioritization that the hub's own partition structure now reflects in practice — `mcp-registry` and `agent-registry` are both active, populated partitions with concrete 3.5-targeted work, while `skills-registry` is smaller/upstream-dependent and other asset types (models, prompts, guardrails) don't have dedicated partitions at all. See [fact-registry-proposal-discussion-transcript.md](/features/platform/knowledge/fact-registry-proposal-discussion-transcript.md) for the same 2026-03-19 meeting's other topic (Databricks upstream process, plugin architecture) — that entry doesn't cover this prioritization call, so this is a separate decision from the same session, not a duplicate.
