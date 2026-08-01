---
type: reference
title: AI Gateway Project
description: Master project doc for the AI Gateway — plans, RHOAI 3.6 MaaS scope, long-term Praxis vision, Envoy migration, team roster, meeting notes, status updates, alternatives research. Shane Utt + Christopher Ferreira.
resource: https://docs.google.com/document/d/1Gq6JnyB84-5uk0dG16zQQx4igmbt7wvRX0XGRydThxw
tags: [ai-gateway, praxis, project, planning]
timestamp: 2026-07-31
review_after: 2026-09-30
source: user-provided, fetched via Google Workspace MCP 2026-07-31
---

The all-in-one project document for the AI Gateway effort. Contains
multiple tabs/sections:

- **What/Why/How**: AI-native gateway rationale, medium-term (Envoy +
  Praxis) and long-term (full Praxis) plans
- **RHOAI 3.6 Plan - MaaS Support**: detailed requirements (Responses
  API, Messages API, API translation, credential management, guardrails,
  token rate limiting, GA readiness), implementation architecture
  (ext_proc, BBR, IPP gap coverage), Konflux onboarding
- **Long-Term Plan - AI-Native Proxy - Praxis**: Rust proxy framework
  vision, filter-first extensibility, payload processing, multi-tenancy,
  governance
- **Migration: Envoy -> Praxis**: Istio and Kuadrant migration plans (WIP)
- **Presentations + Demos**: links to slide decks and demo recordings
- **AI Gateway Team**: roster, channels, meeting notes (weekly from
  Jun 2026 onward)
- **Status Updates**: bi-weekly status email template and archives
- **Research**: alternatives considered (Envoy, HAProxy, Ztunnel,
  Linkerd2-proxy, River, Orion, agentgateway, LiteLLM, and more)
