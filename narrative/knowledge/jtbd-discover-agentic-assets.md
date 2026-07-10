---
type: jtbd
title: "Discover my skills, MCP servers, and agentic assets"
description: "When I'm building agents, I want to discover governed skills, MCP servers, and agentic assets, so I can compose capable agents from validated, approved components."
persona: ai-engineer
status: candidate
timestamp: 2026-07-10
source: ref-agentic-strategy-diagram.md
features: [mcp-catalog, mcp-registry, skills-registry]
tags: [narrative, jtbd, discovery]
---
**When** I'm building or configuring agents,
**I want to** discover governed skills, MCP servers, and agentic assets,
**so I can** compose capable agents from validated, approved components
rather than unvetted tools.

**How RHOAI addresses this:**
- AI Hub as the unified discovery plane for models, MCP servers, agents,
  skills, prompts, and knowledge sources
- MCP Catalog (storefront — discover and deploy RH, partner, community,
  and approved enterprise MCP servers)
- MCP Registry (governance — version, lifecycle, and policy for MCP servers)
- Skills Registry (MLflow-based — register and manage agent skills)
- Validation pipeline — Red Hat tests and benchmarks assets before
  surfacing them (models, MCP servers)

**Pillar:** Agents (AI Hub theme + MCP Ecosystem theme)
