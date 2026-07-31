---
type: decision
title: Converge on Praxis as the AI data plane
description: Binding decision to replace Envoy's AI application layer with Praxis — one router, one policy plane, one configuration authority for AI traffic. IPP, OGX agentic runtime, ITS orchestration, and Semantic Router capabilities converge into Praxis filters.
timestamp: 2026-07-30
decided: 2026-07-30
tags: [ai-gateway, praxis, architecture, envoy]
review_after: 2026-10-30
source: "Red Hat AI Gateway: Architecture & Direction GDoc (Jason Greene, 2026-07-30)"
---

## Context

Multiple components inspect or route the same AI request with partial
context and independent configuration. Envoy provides no substrate
where business logic composes: native C++ filters require maintaining
a 500K+ line codebase, Wasm carries real overhead, ext_proc adds
per-message gRPC round trips, Lua is not production-grade. Each
capability became a component beside the proxy, and components beside
the proxy cannot share request context, identity, ordering, or
configuration. The committed roadmap (Responses with server-side
agentic orchestration under MaaS policy, fallback routing, native
Anthropic Messages, whole-session enforcement, agent governance) is
structurally inexpressible on the current stack.

## Decision

Converge on Praxis as the single AI data plane:

- **One router, one policy plane, one configuration authority** for
  the AI plane. A request traverses the gateway once.
- **Praxis** owns the AI request lifecycle: identity, model resolution,
  entitlements, API translation, guardrails, credential injection,
  routing, and the agentic loop (Responses state, inference rounds,
  tool execution, fan-out).
- **llm-d EPP** remains the placement authority for in-cluster pods.
- **Everything else is terminal**: resource services, scorers, tool
  servers, model backends serve requests but do not route, resolve
  models, or hold provider configuration.
- **IPP** retires; its plugins become Praxis filters.
- **OGX** trends internal-only behind Praxis, then decommissions.
- **ITS** orchestration converges into Praxis fan-out primitives.
- **Envoy remains the front door for 3.6** (TLS, non-AI traffic);
  replacement in subsequent releases via Istio deploying Praxis as
  the gateway data-plane image.

## Consequences

- Every loop iteration, tool call, and fan-out candidate traverses
  the policy pipeline (auth, quotas, metering, audit).
- New capabilities ship as filters, not new stacks.
- OSSM 3.4 (Envoy 1.38) becomes a prerequisite for 3.6.
- The Kuadrant and Istio migration tracks are decoupled from the AI
  layer move and land in subsequent releases.
- Rust becomes the primary language for data-plane development.
