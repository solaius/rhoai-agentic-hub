---
type: fact
title: AI Gateway execution risks — Llama Stack bridge and SGLang/vLLM divergence
description: Two execution risks flagged at the AI Gateway F2F beyond the six binding architecture decisions — a dual-track maintenance burden and a possible vLLM ecosystem fork.
timestamp: 2026-07-06
tags: [platform, ai-gateway, risk, llm-d, vllm]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
**Llama Stack bridge risk**: [decision-ai-gateway-f2f-architecture.md](/restricted/features/platform/knowledge/decision-ai-gateway-f2f-architecture.md) GAs Llama Stack as a bridge in 3.5 while planning a gateway-native multi-tenant Responses implementation within ~6 months — this dual-track maintenance creates risk that customers build dependencies on the bridge if the replacement slips. The F2F decided the timeline; an execution plan for actually hitting it is still needed.

**SGLang/vLLM divergence risk**: the vLLM community is considering a Rust-based SGLang router for orchestration, which could diverge from llm-d — a strategic investment area for Red Hat's inference stack. KV cache management is a current llm-d weakness that needs addressing to keep pace.
