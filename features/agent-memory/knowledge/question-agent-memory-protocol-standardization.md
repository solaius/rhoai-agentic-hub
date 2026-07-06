---
type: question
title: Should Red Hat pursue a memory interoperability protocol, or stay watch-only?
description: MCP (tools) and A2A (agent-to-agent) are adopted standards; no equivalent exists for agent memory — Feast's research flags this as a high-risk, adoption-dependent option worth only watching for now.
status: open
timestamp: 2026-07-06
tags: [agent-memory, protocol, standards]
source: ai-asset-registry/docs/knowledge-review/assets/agent-memory-knowledge.md §10.4, §10.5 (as of 2026-07-05)
---
MCP standardized agent-tool interaction and A2A (1.0.0, March 2026, Linux Foundation governed, 150+ orgs in production) standardized agent-to-agent — but no adopted standard exists for agent-to-memory interaction. The two attempts so far are thin: A2M (draft v0.1, single author, MIT license, zero adoption) and Engram/PLUR (a YAML memory-unit format, v2.1, ~1.4K weekly npm downloads).

Feast's own research (see [ref-feast-in-agentic-ai-era.md](/features/agent-memory/knowledge/ref-feast-in-agentic-ai-era.md) and the fuller writeup in [agent-memory-landscape-research.md](/features/agent-memory/research/agent-memory-landscape-research.md)) explicitly frames "define the memory protocol" as its highest-risk, longest-timeline strategic option (6-12 months, adoption-dependent) and recommends watch-only for now rather than investing.

Open question: does that calculus change as the agent memory team's own architecture work (RHAISTRAT-1345, see [ref-rhaistrat-1345-outcome.md](/features/agent-memory/knowledge/ref-rhaistrat-1345-outcome.md)) matures, or does Red Hat let the ecosystem consolidate first before committing either way?
