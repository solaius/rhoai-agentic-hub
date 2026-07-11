---
type: fact
title: Agent Interop overview
description: What agent-interop covers — sandboxing (OpenShell), identity (SPIFFE/SPIRE), A2A, agent cards, BYO agent onboarding, discovery, declarative harness config — and current status.
timestamp: 2026-07-11
tags: [agent-interop, openshell, overview]
features: [agent-interop, agent-registry, agent-ops]
review_after: 2026-08-11
source: intake session 2026-07-11; three GDocs, three emails, FAQ
---

Agent Interop is the production-readiness layer for agents on Red Hat AI.
It covers everything between "I have an agent" and "it runs safely in
production": sandboxed execution, cryptographic identity, agent-to-agent
communication, tool governance, and secure onboarding.

Current anchor upstream: **OpenShell** (NVIDIA/OpenShell). The Kagenti
project (previously the planned upstream) is being wound down for
downstream productization; its design concepts inform OpenShell
contributions. See
[decision-openshell-strategic-bet.md](/features/agent-interop/knowledge/decision-openshell-strategic-bet.md).

## Scope

- **Sandboxing**: kernel-level isolation (Landlock LSM, seccomp, network
  namespaces) via OpenShell supervisor model
- **Identity/Security**: SPIFFE/SPIRE zero-trust agent identity, token
  exchange, credential injection without agent exposure
- **A2A Communication**: Agent-to-Agent protocol support, agent card
  discovery
- **BYO Agent**: framework-agnostic onboarding (OpenClaw, LangChain,
  CrewAI, Claude Agents, ADK, Strands, custom)
- **Declarative Harness**: agent configuration and deployment
  abstraction (active design discussion)
- **Discovery**: runtime discovery of agents running on the platform
- **Policy Enforcement**: OPA-based L4/L7 network policy, MCP-aware
  governance, hot-reloadable policies

## Product timeline

- Dev Preview: RHOAI 3.5 (Jul-Aug 2026)
- Tech Preview: RHOAI 3.6 EA (Nov 2026)
- GA: RHOAI 3.7 (early 2027)

## Relationship to other features

Works with the Agent Catalog/Registry/Gateway as part of the Agent
Management Ecosystem. Pre-deployment registry/catalog work is in
[agent-registry](/features/agent-registry/); post-deployment
observability/SDLC oversight in [agent-ops](/features/agent-ops/);
MCP-level tool governance in
[mcp-gateway](/features/mcp-gateway/).

## Key links

- [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell)
- [RHOAI architecture repo](/features/platform/knowledge/ref-opendatahub-architecture-context-repo.md)
- Slack: #forum-openshell, #agentops-leads
- Jira: AgentOps component, agentic/agentic-theme labels
- HATSTRAT-314
