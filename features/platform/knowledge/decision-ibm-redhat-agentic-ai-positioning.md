---
type: decision
title: IBM/Red Hat joint positioning for agentic AI (customer-facing only)
description: Division of labor for joint IBM/Red Hat customer conversations on agentic AI — does not change Red Hat's product roadmap.
decided: 2026-04-14
timestamp: 2026-07-06
tags: [platform, ibm, positioning, messaging]
source: ai-asset-registry/docs/knowledge-registry.md §10, §13 (as of 2026-07-05)
review_after: 2026-08-05
---
**Context**: From the 2026-04-14 Agentic AI pod. IBM and Red Hat needed aligned messaging for joint customer conversations, given overlapping agentic capabilities (Red Hat AI vs. watsonx).

**Decision**: For joint-customer-conversation contexts only: Red Hat owns agent runtime, lifecycle management, and Agent Ops (observability, evaluations, security); IBM owns agent building, control plane, and watsonx Orchestrate (no-code/GUI, local/business users). Red Hat AI Enterprise will be first-class in the watsonx portfolio — IBM properties (Orchestrate, Govern) depend on Red Hat AI Enterprise, not wx.ai/CP4D. Red Hat stays the course on MCP Gateway, Agent Ops, and evaluations/traces with MLflow — none of this changes. Tushar Katarki's framing: "Let the best solution win" — overlaps are inevitable in AI; customer choice is the answer.

**Consequences**: Risk that field sellers misinterpret this as "Red Hat doesn't do agents" (Noel O'Connor) or that IBM owning "AI Governance"/"gateway" language in joint slides causes long-term seller-enablement problems (Jennifer Vargas). Mitigation: FAQ attached to Power Hour, agentic messaging review by Joe, reinforcement in podcast/webinars.
