---
type: decision
title: "ODH-ADR-ML-0001: consolidate AI asset registries on MLflow (formal ADR)"
description: The formal, approved Architecture Decision Record ratifying MLflow as the unified registry backend for all AI asset types — the same conclusion as decision-registry-vs-catalog.md, reached through ODH's ADR process.
decided: 2026-05-24
timestamp: 2026-07-06
tags: [platform, adr, mlflow, registry-vs-catalog]
source: ai-asset-registry/docs/knowledge-review/components/gen-ai-studio-architecture.md §12 (as of 2026-07-05)
review_after: 2026-08-05
---
**Context**: [decision-registry-vs-catalog.md](/features/platform/knowledge/decision-registry-vs-catalog.md) captures the registry-vs-catalog split as it emerged from an April 2026 sync ("MLflow is for registries. Kubeflow is for catalogs. We're done." — Adam Bellusci). Separately, and later, the same conclusion went through ODH's formal Architecture Decision Record process.

**Decision**: **ODH-ADR-ML-0001** ("Consolidate AI Asset Registries on MLflow"), authored by Edson Tirelli, approved 2026-05-24: MLflow is the unified registry backend for all AI asset types (models, prompts, skills, MCP servers, agents, guardrails, knowledge sources). Key principles: registry-catalog separation (MLflow = registry, AI Hub = catalog); a federated plugin model per asset type; upstream-first development. A companion ADR, **ODH-ADR-ML-0002** ("Shared Workspace for Cross-Namespace Resource Sharing," also approved 2026-05-24), establishes a shared global MLflow workspace enabling cross-namespace resource sharing — e.g., prompt sharing into Gen AI Studio ([RHAISTRAT-1750](https://redhat.atlassian.net/browse/RHAISTRAT-1750)).

Both ADRs live in [opendatahub-io/architecture-decision-records](https://github.com/opendatahub-io/architecture-decision-records/tree/main/architecture-decision-records/mlflow).

**Consequences**: Formalizes, via ODH's own governance process, the same registry/catalog boundary already decided informally — this doesn't change the substance of [decision-registry-vs-catalog.md](/features/platform/knowledge/decision-registry-vs-catalog.md), but it's a more citable, dated, authored source for the same call, and confirms the plugin/federation model applies uniformly across asset types (not just MCP). Gen AI Studio's AI Assets view is the first concrete consumer, consolidating all asset types through MLflow APIs — see [gen-ai-studio-architecture.md](/features/gen-ai-studio/research/gen-ai-studio-architecture.md).
