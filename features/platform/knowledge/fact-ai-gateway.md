---
type: fact
title: AI Gateway / Inference Gateway
description: The unified gateway for all AI traffic (inference, tool calling, A2A, egress) — distinct from MCP Gateway, architecture decided April 2026.
timestamp: 2026-07-06
tags: [platform, ai-gateway, inference]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
Unified, multi-purpose gateway for all AI traffic — inference, egress, agentic/stateful APIs, tool calling, A2A — distinct from MCP Gateway, which handles MCP protocol traffic specifically. Core framework is IPP (Inference Payload Processor), a foundational ext_proc plugin chain within Envoy. Four traffic types: model inference, tool calling/MCP, agent-to-agent (A2A), external provider egress. Red Hat contributes to the industry-wide Open Responses Specification alongside OpenAI, NVIDIA, vLLM, Llama Stack, HuggingFace, AWS, and Databricks.

Status: ~60% detailed as of source capture; follow-up design needed on sub-request routing, Envoy re-entrance, conversation state management, and tenancy strategy. See [decision-ai-gateway-f2f-architecture.md](/features/platform/knowledge/decision-ai-gateway-f2f-architecture.md) for the binding architectural calls, and [ref-ai-gateway-payload-processing-repo.md](/features/platform/knowledge/ref-ai-gateway-payload-processing-repo.md) for the IPP implementation.
