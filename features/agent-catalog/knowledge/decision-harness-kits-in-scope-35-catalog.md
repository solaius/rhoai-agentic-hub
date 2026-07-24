---
type: decision
title: Harness kits in scope for 3.5 agent catalog
description: Adel Zaalouk confirmed (~2026-07-11) that all agent kits already in the agentic-starter-kits repo are in scope for 3.5 catalog -- including harness kits (OpenCode, Claude Code, OpenClaw, etc.), not just template kits.
timestamp: 2026-07-23
decided: 2026-07-11
tags: [agent-catalog, 3.5, harness, decision]
---
**Decision**: "Those that are in the starterkits already should be in scope
IMO" -- Adel Zaalouk, responding to Philip Colares Carneiro's question about
whether harness kits (opencode, claude-code, etc.) are in scope for 3.5
catalog.

**Context**: Bill Murdock (AgentDev) opened PR #256 to add harness kits to
the catalog. The question arose because template kits (managed by Tooling
Experience / mpk) and harness kits (managed by AgentDev) had been on separate
tracks. Gage Krumbach noted that catalog inclusion and deployment-list
inclusion are different requirements.

**Implications**: PR #256 must merge for the harness kits to appear. The
agent.yaml minimum required fields for catalog inclusion (per Alessio
Pragliola): `name, displayName, description, framework, labels, logo, env`.
