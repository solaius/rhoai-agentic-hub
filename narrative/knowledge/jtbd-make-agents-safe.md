---
type: jtbd
title: "Make agents safe"
description: "When I deploy agents, I want to ensure AI safety with guardrails, red teaming, and sandboxing, so I can prevent harmful or unauthorized agent behavior in production."
persona: platform-engineer
status: candidate
timestamp: 2026-07-10
source: ref-agentic-strategy-diagram.md
features: [agent-ops]
tags: [narrative, jtbd, safety]
---
**When** I deploy agents to production,
**I want to** ensure AI safety with guardrails, red teaming, and sandboxing,
**so I can** prevent harmful or unauthorized agent behavior and meet
compliance requirements.

**How RHOAI addresses this:**
- NeMo Guardrails (GA) — input/output content filtering, orchestration
  engine for guardrail policies
- Red Teaming (GA soon) — stress-test models against jailbreak, prompt
  injection, and adversarial attacks before deployment
- OpenShell sandboxing (coming) — three patterns: whole-process isolation,
  per-session isolation, SDK-level primitives
- Defense in depth: platform SCCs + SELinux → Kata micro-VMs → OpenShell →
  guardrails → red teaming

**Pillar:** Agents (Agent Ops theme)
