---
type: fact
title: "8-layer agentic inference stack architecture"
description: "The 8-layer architecture from Adel's blog: Agent/Harness → API Translation → Gateway → Guardrails → Disaggregated Serving → Model Server → Inference Engine → Hardware."
timestamp: 2026-06-08
source: ref-blog-agentic-inference-stack.md
tags: [narrative, architecture, inference]
---
From Adel Zaalouk's blog, the agentic inference stack has 8 layers that
must work together (top to bottom):

1. **Agent and Harness** — the agentic application, wrapped in a sandbox
   boundary for code execution security
2. **API Translation** — bridges harness to model server across Chat
   Completions, Responses, Messages, and Interactions APIs. OGX (formerly
   Llama Stack) provides the open implementation layer.
3. **Gateway** — routing, metering, rate limiting, governance (AI Gateway)
4. **Guardrails** — content safety that preserves the agentic API contract
   (NeMo Guardrails); must be agentic-aware (preserve tool definitions,
   tool choice, reasoning parameters)
5. **Disaggregated Serving** — splits prefill and decode phases for
   independent scaling on different hardware (llm-d). Essential for
   agentic workloads mixing short requests with long reasoning chains.
6. **Model Server Configuration** — chat templates, tool call parsers,
   prompt formatting per model family
7. **Inference Engine** — vLLM, the open-source runtime
8. **Hardware** — accelerators (GPUs, etc.)

The API translation layer (2) and model server configuration layer (6)
are where most agentic compatibility work lives. The blog argues open
source wins structurally because layers 2, 3, 4, 5, 6, 7 all require
customization that proprietary APIs don't expose.
