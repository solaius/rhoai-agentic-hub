---
type: fact
title: RHOAI 3.4 agentic capabilities — status snapshot
description: GA/Tech Preview/Dev Preview status for eleven agentic capabilities as of the Agentic AI Messaging Guide (Apr 2026) — a point-in-time snapshot, not a roadmap.
timestamp: 2026-07-06
tags: [platform, rhoai-3.4, capabilities, status]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §10 (as of 2026-07-05)
---
Snapshot as of the Apr 2026 Messaging Guide (see [ref-agentic-messaging-guide.md](/features/platform/knowledge/ref-agentic-messaging-guide.md)) — expect drift by 3.5/3.6, re-verify before reuse:

| Capability | Status | Notes |
|---|---|---|
| Agent traceability via MLflow | GA | Logs every LLM call, tool execution, decision step |
| Governed prompt management (GenAI Studio) | GA | Prompts managed as code; version, test, refine |
| BYOA (LangGraph, CrewAI, OpenClaw) | TP | Framework-agnostic agent operationalization |
| Lifecycle management with Kagenti | TP | Agent discovery and versioning |
| Agent Sandbox | DP | Policy-governed runtime, zero-trust boundaries |
| Identity management (SPIFFE/SPIRE) | DP | Cryptographic agent identities, short-lived tokens |
| MaaS platform (admin UI, token limits, self-service) | GA | Self-service model access for builders |
| External OIDC + model egress via Inference Gateway | TP | Secure routing to cloud-hosted LLMs |
| Inference-aware autoscaling (KV cache pressure) | GA | Handles concurrent multi-agent inference spikes |
| Speculative decoding (2x-3x speedup) | GA | Lowers cost-per-interaction for high-frequency agents |
| Hardware: NVIDIA Blackwell, AMD MI325X day-zero | GA | Consistent agent workloads across silicon/cloud |

GA = generally available, TP = Tech Preview, DP = Dev Preview.
