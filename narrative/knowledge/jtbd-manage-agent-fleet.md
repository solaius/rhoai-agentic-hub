---
type: jtbd
title: "Manage my agent fleet at scale"
description: "When I operate many agents across my organization, I want centralized registry, lifecycle management, and fleet governance, so I can discover shadow agents, enforce policies, and revoke access in seconds."
persona: agentops-admin
status: candidate
timestamp: 2026-07-10
source: narrative/research/02-agentic-requirements-landscape.md
features: [agent-ops, agent-registry]
tags: [narrative, jtbd, fleet, governance, research-gap]
---
**When** I operate many agents across my organization,
**I want to** centrally register, discover, and manage my agent fleet
with lifecycle governance and emergency controls,
**so I can** discover shadow agents, enforce policies fleet-wide, and
revoke agent access in seconds during incidents.

**Evidence (from research):**
- HFS Research: 82% of enterprises have agents their security teams did
  not know existed [research doc 02, source 13]
- Only 47.1% of deployed agents are actively monitored [doc 02, source 16]
- 68% of organizations cannot distinguish human from agent activity in
  logs [doc 02, source 16]
- All hyperscalers (AWS Agent Registry, Google Agent Platform, Microsoft)
  launched fleet management services in 2026 [doc 02, source 22]
- Gartner created the Guardian Agents category specifically for this gap
  — Reviewers, Monitors, and Protectors [doc 02, source 17]

**Gap vs existing JTBDs:** JTBD #6 (Operationalize agents) covers
individual agent production deployment. This JTBD covers the fleet
dimension: what happens when you have 100+ agents, multiple teams, and
need organizational-level visibility and control.

**Pillar:** Agents (Agent Ops theme)
