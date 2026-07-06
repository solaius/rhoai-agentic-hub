---
type: fact
title: Gen AI Studio — what it is and how it's built
description: Prompt engineering, model interaction, and AI asset management surface in RHOAI — Tech Preview in 3.5 EA, GA target 3.6; a federated module riding on OGX (Llama Stack).
timestamp: 2026-07-06
tags: [gen-ai-studio, architecture, ogx]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-review/components/gen-ai-studio-architecture.md (as of 2026-07-05)
---
Gen AI Studio is RHOAI's prompt-engineering/model-interaction/AI-asset-management surface — Playground (multi-model chat), AI Available Assets (AAE — unified view of models/prompts/MCP endpoints/guardrails/vector stores), Observability (chat metrics + tracing), and Configuration Persistence (save/load/share agent configs). It evolved from the original "Prompt Lab" concept aimed at watsonx.ai parity. Current maturity: Tech Preview in RHOAI 3.5 EA, GA target RHOAI 3.6.

Architecturally it's **not standalone** — it's a federated module (Module Federation micro-frontend + Go BFF sidecar, port 8143) inside the ODH Dashboard pod, riding on OGX (Red Hat's Llama Stack Distribution) for models/RAG/shields/agents, MLflow Prompt Registry for prompts, NeMo Guardrails (via TrustyAI Operator, migrating off Llama-Stack-mediated guardrails) for safety, and MCP Gateway for tools (ConfigMap-based today, registry discovery planned).

Owner: Peter Double (Principal PM). Engineering: Team Crimson. Repo: [opendatahub-io/odh-dashboard](https://github.com/opendatahub-io/odh-dashboard) (`packages/gen-ai/`).

Full architecture writeup (system diagram, tech stack, request flow, ADRs, roadmap by theme, open questions): [gen-ai-studio-architecture.md](/features/gen-ai-studio/research/gen-ai-studio-architecture.md).
