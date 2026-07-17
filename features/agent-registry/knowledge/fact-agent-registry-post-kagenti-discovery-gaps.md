---
type: fact
title: Post-kagenti discovery gaps — enumeration without enrichment
description: Kagenti's removal split agent discovery in two and nobody owns the second half — Sandbox v1beta1 CRs enumerate but carry zero agent semantics; no component fetches/verifies agent cards (verified/identity/trust_domain have no producer); BYO label-discovery is orphaned.
timestamp: 2026-07-16
tags: [agent-registry, discovery, openshell, agent-sandbox]
features: [agent-interop]
---
Kagenti's AgentCard CRD did two jobs: enumerate agents AND carry
verified A2A metadata (card fetch + JWS/SPIFFE-x5c verification). After
the roadmap removal
([fact-kagenti-roadmap-removal](/features/agent-registry/knowledge/fact-kagenti-roadmap-removal.md)),
no single component does both:

1. **Sandbox v1beta1 CRs** (agents.x-k8s.io; v0.5.0 2026-06-24, v0.5.1
   2026-07-09) expose infrastructure fields only — podTemplate, service,
   operatingMode, podIPs, conditions. No skills, protocol, card, or
   verification anywhere.
2. **Agent-card fetch + signature verification has NO successor.** The
   registry schema's `verified`/`identity`/`trust_domain` fields
   currently have no producer; RHAISTRAT-1956 (mutually-authenticated
   metadata sync, paraphrased) is the only vehicle — the long pole for
   any `verified=true` GA claim.
3. **BYO/Mode-1 agents are invisible**: kagenti's label convention
   (`kagenti.io/type=agent` on plain Deployments) lost its owner —
   untracked regression.

Architecture consequence: the registry owns the card/workload join. See
[research/09-architecture](/features/agent-registry/research/09-architecture.md).
