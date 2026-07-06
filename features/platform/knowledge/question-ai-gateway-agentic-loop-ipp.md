---
type: question
title: Agentic loop microservice x IPP plugin framework integration
description: How the new tool-invocation/inference-cycle "agentic loop" microservice should integrate with the broader IPP plugin framework, given different plugin orderings per context.
status: open
timestamp: 2026-07-06
tags: [platform, ai-gateway, ipp, responses-api]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
The F2F introduced a new "agentic loop" microservice for the tool-invocation/inference cycle (decision 2 in [decision-ai-gateway-f2f-architecture.md](/restricted/features/platform/knowledge/decision-ai-gateway-f2f-architecture.md)), part of re-architecting the Responses API. Different IPP plugin orderings are needed depending on context (outer gateway vs. inner loop) — designed in concept, not yet implemented.
