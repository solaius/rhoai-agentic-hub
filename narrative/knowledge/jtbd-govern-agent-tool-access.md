---
type: jtbd
title: "Govern agent tool and model access"
description: "When I manage a fleet of agents, I want to govern which tools and models each agent can access, so I can enforce least-privilege and audit agent actions — MCP Gateway, AI Gateway, SPIFFE."
persona: agentops-admin
status: candidate
timestamp: 2026-07-10
source: ref-power-90-agentic-ai-20260708.md
features: [mcp-gateway, agent-ops]
tags: [narrative, jtbd, governance, access-control]
---
**When** I manage a fleet of agents,
**I want to** govern which tools and models each agent can access,
**so I can** enforce least-privilege, rate-limit token usage per team, and
audit every agent action.

**How RHOAI addresses this:**
- Three governance layers (from Adel's Power 90 presentation):
  1. **Model access layer** — does this agent have access to these models?
  2. **Tool access layer** — can this agent use this specific MCP server/tool?
  3. **Identity layer** — does this agent have the right credentials and
     "on behalf of" delegation for external services?
- MCP Gateway — authentication/authorization proxy for MCP servers; session
  management, tool-level access control, URL whitelisting
- AI Gateway (converging with ODX) — model routing, rate limiting, cost
  tracking, governance across inference endpoints
- SPIFFE/SPIRE — cryptographic workload identity, short-lived tokens
  rotated every minute, integrated via agent runtime (no code changes)
- On-behalf-of delegation — agents act with delegated human identity for
  accountability

**Pillar:** Agents (Agent Ops theme + MCP Ecosystem theme)
