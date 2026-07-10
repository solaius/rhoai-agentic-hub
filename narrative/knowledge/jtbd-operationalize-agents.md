---
type: jtbd
title: "Operationalize agents"
description: "When I move from prototype to production, I want to operationalize my agents with identity, access control, and lifecycle management, so I can trust them in enterprise environments."
persona: platform-engineer
status: candidate
timestamp: 2026-07-10
source: ref-agentic-strategy-diagram.md
features: [agent-ops, agent-registry]
tags: [narrative, jtbd, operations, lifecycle]
---
**When** I move agents from prototype to production,
**I want to** operationalize them with identity, access control, and
lifecycle management,
**so I can** trust them in enterprise environments and scale the agent
fleet with confidence.

**How RHOAI addresses this:**
- Agent Registry (MLflow-based) — governed asset record with versions,
  approval workflows, catalog for reuse
- SPIFFE/SPIRE identity — short-lived, auto-rotated credentials for agents
  (no hardcoded secrets); agent runtime manages identity injection
- Agent Sandbox (workload orchestration) — secure onboarding flow for
  agents onto the platform
- "From Metal to Agents" — reuse all platform primitives (SCCs, SELinux,
  network policies, Kata containers) extended for agentic workloads

**This is the overarching JTBD** — the other JTBDs (make safe, evaluate,
discover, etc.) are capabilities that compose into this outcome. The
agentic strategy's north star: "Your Agent. Our Platform. Production-Ready."

**Pillar:** Agents (the umbrella goal)
