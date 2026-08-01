---
type: fact
title: "Adel's positioning thesis: alongside harness, not instead of"
description: Adel Zaalouk's positioning guidance for RHOAI agent memory — "memory is the new lock-in vector," platform runs alongside harness-native memory, 5 anti-patterns, 3 integration tiers, harness convergence analysis, and the tagline.
timestamp: 2026-07-27
source: https://docs.google.com/document/d/1_tgs89biYBqC5ZnuLC3QbvkNElvJr4yo1D3W84aYTOY
tags: [agent-memory, positioning, strategy]
review_after: 2026-10-27
---

Adel Zaalouk (PM sponsor, agentic strategy) wrote a positioning document
for RHOAI agent memory. Context from Peter: "not gospel, but definitely
could have good ideas and things to be aware of." The novel positioning
elements (distinct from the hub's existing research/strategy):

## Lead framing: memory is the new lock-in vector

Every hyperscaler is building managed memory services that tie customers to
their cloud. Memory is becoming the new lock-in mechanism after model
lock-in. Red Hat's answer: platform memory that runs anywhere, governed by
the customer, not the cloud provider.

## Core stance: alongside harness, not instead of

The platform does NOT replace harness-native memory (MEMORY.md,
.cursorrules, SQLite). Both systems run in parallel during a session. The
harness writes to its native store; the model also calls `memorize` on the
platform. Redundancy is harmless; the platform deduplicates. The
difference shows up when the developer switches machines, switches
harnesses, adds a teammate, or needs rollback.

**Tagline:** "Your harness handles memory for one session on one machine.
The platform handles memory for your fleet, your team, and your compliance
requirements."

## Harness convergence analysis (8 harnesses)

Where harnesses converge (leave alone):
- Static instruction files are table stakes (CLAUDE.md, .cursor/rules/)
- Conversations are ephemeral — no harness persists raw chat as primary memory
- Rules beat memories for teams (version-controlled, deterministic)

Where harnesses diverge (opportunity):
- Client vs. server: Claude Code fully client-side, Devin fully server-side
- Auto vs. approved: Claude Code auto-extracts (drifts after 1-2 months), Cursor requires user approval
- Cross-agent sharing: only Copilot Memory and Devin Knowledge Base share across surfaces

The governance column across all 8 harnesses: **None**. No versioning, no
audit trail, no access control, no rollback, no poisoning defense.

## Three integration tiers

| Tier | Developer effort | Best for |
|------|------------------|----------|
| MCP tools | Connect MCP server (1 command) | Any MCP-capable harness |
| OpenAI-compatible APIs | Add API calls to agent code | Framework agents without MCP |
| Lifecycle hooks | Add config to sandbox definition | Agents in OpenShell sandboxes |

## Five anti-patterns

1. Don't auto-extract everything (Databricks: stale auto-extracted memories become "established precedent")
2. Don't make memory management the primary UX (developers want agents that stop forgetting, not a memory dashboard)
3. Don't fight the harness (Claude Code will keep writing MEMORY.md — let it)
4. Don't skip forgetting (TTL and consolidation are not phase-3 features)
5. Don't gate basic memory behind paid tiers (Mem0 gates graph behind $249/mo — our story: full capability on any deployment)

## Developer journey framing

Adel sketches a 5-day narrative: Day 1 memorize, Day 2 cross-machine
recall, Day 3 colleague joins with different harness and gets project
context, Day 4 bad memory detected and rolled back via dashboard, Day 5
compliance audit answered with full provenance trail.
