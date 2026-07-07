---
title: AgentOps & MCP Ecosystem — Talk Track (Slides 9-13)
description: Talk track for the RHAI Q2 2026 EBC deck, slides 9-13, covering agentic AI platform architecture and the AgentOps/MCP ecosystem story.
source: ai-asset-registry/agent-ops/talk-track.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# AgentOps & MCP Ecosystem — Talk Track (Slides 9-13)

**Deck:** RHAI Q2 2026 EBC
**Duration:** ~10 minutes (2 min/slide)

---

## Slide 9 — Agentic AI Platform Architecture

- Two personas: AI engineers/developers (left) and platform engineers/admins (right)
- Developer side: tools, models, AI Gateway, agent frameworks, knowledge/memory, safety, agent-to-agent APIs
- Platform side: MCP Gateway, observability, tracing, evaluation, registry, catalog, lifecycle mgmt, identity, security
- Key insight: agentic AI doesn't eliminate platform engineering — it amplifies it
- Every agent-to-tool call, model access, and knowledge retrieval is new surface area to govern, secure, and observe
- That's what RHOAI is purpose-built to address

## Slide 10 — AgentOps: Develop and Deploy Reliably

- Core principle: same cloud-native operational principles (observability, identity, lifecycle, security) repurposed for agentic workloads
- **Observability & tracing:** MLflow 3.10+ and OpenTelemetry — log and visualize full agent execution traces including tool calls and decision points
- **Identity & security:**
  - OAuth 2.0 token exchange for secure delegation (no master API keys passed around)
  - SPIFFE/SPIRE for cryptographic workload identity per agent
  - Kagenti/AuthBridge for agentic auth patterns; agent-to-tool governance via MCP Gateway
- **Evaluation:** Eval Hub + MLflow — systematic agent quality, safety, and accuracy assessment using curated datasets and LLM-as-judge
- **Lifecycle management:** Kagenti — declarative agent deployment via Kubernetes CRs (runtime, identity, trace config)

## Slide 11 — AgentOps Summary

- Unified framework for managing lifecycle, security, and performance of AI agents and tools
- The problem: enterprises build impressive agent demos in a week, production takes months — nobody's solved operational rigor
- **1H 2026:**
  - Agent observability/tracing with MLflow (Dev Preview)
  - Agent deploy & lifecycle management (Dev Preview)
  - SPIFFE/SPIRE for trusted agent identity
  - Agent evaluation with Eval Hub (Tech Preview)
- **2H 2026:**
  - Tracing and lifecycle management GA
  - Sandboxed execution environments for agents — critical for running third-party agents in isolation
  - Agent catalog & registry
- By end of 2026: same level of operational control for agents as any production workload

## Slide 12 — MCP Ecosystem on OpenShift AI

- MCP = Model Context Protocol — open standard for agent-to-tool connectivity ("USB ports for AI agents")
- The problem: ad hoc MCP server deployment, no centralized discovery, security, or governance — doesn't scale beyond PoC
- **MCP Gateway (Tech Preview, 1H):** centralized auth, access control, traffic routing, guardrails for MCP traffic
- **MCP Catalog (Dev Preview, 1H):** searchable discovery of MCP servers, deploy directly, integrated with Gateway from day one
- **Lifecycle Operator (Dev Preview, 1H):** Kubernetes-native deployment and management of MCP servers from catalog
- All consumable from Gen AI Studio — discover, deploy, configure, Gateway handles security automatically
- **2H 2026:** all components to GA + ingestion pipeline (Tech Preview) for packaging/publishing internal MCP servers

## Slide 13 — Gen AI Studio

- Interactive playground tying all capabilities into a single developer surface
- One place to experiment with models, engineer prompts, test RAG, prototype agent behaviors
- **1H 2026:**
  - Prompt engineering & management — version, compare, share prompts across teams
  - Playground UI alignment with Prompt Lab for Watsonx.ai (IBM/Red Hat portfolio consistency)
  - Model/configuration comparison — same prompt against different models side by side
  - MCP Catalog integration — browse, deploy MCP servers, configure agents directly in Studio
  - Surface vector stores
- **2H 2026:**
  - Guardrails integration — test safety policies inline
  - Session tracing — debug and audit from the playground
  - Multimodal support
  - Configuration persistence
  - Deploy playground configs directly as production agents
- The vision: Gen AI Studio = on-ramp from experimentation to production; AgentOps + MCP ecosystem = operational foundation underneath

---

## Presenter Notes

- **Pacing:** trim Slide 10 pillar walkthrough if running long — Slide 11 summary covers the highlights
- **Arc:** big picture (architecture) → operational depth (AgentOps) → two key product areas (MCP, Studio) → how they connect
- **Audience:** enterprise customers/partners at EBC — technically grounded but business-outcome oriented
