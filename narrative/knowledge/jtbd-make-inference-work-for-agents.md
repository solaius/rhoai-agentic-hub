---
type: jtbd
title: "Make inference work for agents"
description: "When I operate agents at scale, I want inference that's efficient and cost-effective, so agents don't bankrupt my token budget — vLLM, llm-d, self-hosted inference."
persona: platform-engineer
status: candidate
timestamp: 2026-07-10
source: ref-blog-agentic-inference-stack.md
tags: [narrative, jtbd, inference]
---
**When** I operate agents at scale,
**I want to** make inference efficient and cost-effective for agentic
workloads,
**so** agents don't bankrupt my token budget and I maintain control over
cost, sovereignty, and customization.

**How RHOAI addresses this:**
- vLLM inference engine — open-source, supports all major model families
  with agentic-specific optimizations (tool call parsing, chat templates)
- llm-d — disaggregated serving splitting prefill and decode phases for
  independent scaling on different hardware
- Self-hosted inference — $500 GPU processes 30M tokens/day; ROI in 3
  months vs budget-tier API pricing
- Model routing — direct routine tasks to smaller self-hosted models,
  escalate complex tasks to frontier APIs (60-85% cost reduction)
- OGX (formerly Llama Stack) — open API translation across Chat
  Completions, Responses, Messages, Interactions

**The economic case:** Jevons Paradox — per-token costs drop 90% by 2030
but agent-driven consumption rises 24x. Self-hosted inference is a
structural necessity, not just a cost optimization.

**Pillar:** Inference (connects to Agents via the cost paradox)
