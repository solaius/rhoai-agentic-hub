---
type: fact
title: AI Gateway 3.6 scope and delivery plan
description: 3.6 engineering goal — Praxis replaces IPP and provides Responses support, both aiming GA quality; Messages API, API translation, guardrails, credential management; ext_proc attachment over OSSM 3.4; EA1/EA2 verification gates; TP as fallback.
timestamp: 2026-07-31
tags: [ai-gateway, praxis, release, 3.6]
review_after: 2026-09-15
source: Architecture & Direction GDoc (2026-07-30) + AI Gateway Project GDoc 3.6 Plan tab
---

## 3.6 committed

- Praxis productization: downstream repo (opendatahub-io/praxis-extproc),
  Konflux onboarding, FIPS migration start
- IPP plugin parity and conformance gates; EA1/EA2 verification milestones
- Messages passthrough carry-forward (new owner: Praxis)
- Tech Preview as the named fallback if GA gates fail
- Praxis configuration/deployment managed by existing MaaS controllers
  replacing IPP deployment

## 3.6 target (gated on parity/conformance)

- Praxis replaces IPP behind the same API contracts
- OpenAI Responses API + server-side agentic loop orchestration
- Anthropic Messages API support (translation + passthrough)
- Multi-provider API translation (OpenAI, Anthropic, Bedrock, Vertex AI)
- Runtime APIs move to Praxis; resource APIs run OGX-behind-Praxis
- All traffic attaches over ext_proc (OSSM 3.4, Envoy 1.38)
- AI guardrails (NeMo/TrustyAI integration)
- Provider credential injection and management (API key, GCP WI,
  AWS SigV4, Azure AD)

## Key risks and gates

- Konflux pipeline for Rust/praxis-extproc is the single largest
  delivery risk (AIPCC supporting)
- FIPS compliance for Rust binary
- IPP parity conformance suite must pass
- Conversation-state continuity across 3.5 to 3.6 engine swap is an
  explicit open line item
- Support designation (GA vs TP with support exceptions) under review
  with BU and Engineering

## Key owners

- Responses + Agentic Loop: Sebastien Han (AAET Agentic API)
- Messages API + API Translation: Francisco Arceo (AAET Agentic API)
- Guardrails: Christina Xu (Platform AI Safety)
- Token Rate Limiting: Eguzki Astiz Lezaun (Kuadrant)
- Deployment/lifecycle: Jamie Land + Shane Utt
