---
type: fact
title: "Harness vs framework: manual vs automatic transmission"
description: "Adel's framing: frameworks (LangChain, CrewAI, Strands) = manual transmission with full developer control; harnesses (OpenClaw, Claude Code) = automatic transmission, off-the-shelf agent runtimes."
timestamp: 2026-07-08
source: Power 90 session 2026-07-08
features: [agent-registry]
tags: [narrative, definitions]
---
From the Power 90 (2026-07-08), Adel's positioning for the field:

**Framework = manual transmission:** the developer builds the agent loop,
defines tool schemas, manages state, controls orchestration. Full control
but more effort. Examples: LangChain, LlamaIndex, CrewAI, Strands, ADK,
Autogen.

**Harness = automatic transmission:** off-the-shelf agent runtimes where
you provide MCP servers/skills, models, and a prompt — the harness does
the orchestration. You don't code the agent; you configure it. Examples:
OpenClaw, Claude Code, Cursor.

**Key insight:** ~1,000 frameworks but only ~4 APIs (Chat Completions,
Responses, Messages, Interactions). The industry is standardizing on APIs
more than frameworks. Red Hat's play: capture the API surface with open
implementations and provide the production onboarding path regardless of
framework or harness choice.

Srikanth Tanniru's concise definition from the session chat:
"Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions"
