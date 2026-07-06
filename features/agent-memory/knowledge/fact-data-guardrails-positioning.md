---
type: fact
title: "\"Data guardrails\" vs. \"output guardrails\" — a positioning distinction"
description: Jonathan Zarecki's framing for where guardrails fire — before data reaches the LLM (data guardrails) vs. after the LLM generates a response (output guardrails) — proposed as a differentiator when Feast is paired with TrustyAI.
timestamp: 2026-07-06
tags: [agent-memory, guardrails, positioning, feast]
source: ai-asset-registry/docs/knowledge-review/assets/agent-memory-knowledge.md §10.6 (as of 2026-07-05)
review_after: 2026-08-05
---
A framing concept from Jonathan Zarecki's Feast agentic-positioning research, distinguishing two places guardrails can fire:

| Type | When | Examples |
|---|---|---|
| Output guardrails | After the LLM generates a response | NeMo Guardrails, AWS Bedrock, TrustyAI |
| Data guardrails | Before data reaches the LLM — at the retrieval/access layer | Feast, Oracle AI Agent Memory, Veto, Waxell |

Zarecki's argument: Feast (data guardrails) + TrustyAI (output guardrails) together would be a uniquely defensible agentic stack, since no other platform pairs both — Feast offers feature-view-level RBAC (more granular than table/schema level), point-in-time correctness (which Zarecki characterizes as unique among competitors), and a framework-agnostic open-source data-guardrails layer.

This is proposal-stage positioning, not a decision — but it's a plausible lens for the broader registry/governance story beyond agent memory specifically, since the registry-vs-catalog split (see [decision-registry-vs-catalog.md](/features/platform/knowledge/decision-registry-vs-catalog.md)) is itself about where governance sits relative to data/asset flow. See [agent-memory-landscape-research.md](/features/agent-memory/research/agent-memory-landscape-research.md) for the fuller research this framing comes from, and [decision-mcp-gateway-tool-governance-scope.md](/features/mcp-gateway/knowledge/decision-mcp-gateway-tool-governance-scope.md) for a related output-side scope boundary already decided for MCP Gateway.
