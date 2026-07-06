---
type: decision
title: Registry vs. Catalog separation
description: Registry governs (system of record); Catalog discovers (consumption surface) — MLflow serves the registry role, Kubeflow (Hub) the catalog role.
decided: 2026-04-07
timestamp: 2026-07-06
tags: [platform, registry-vs-catalog, mlflow, kubeflow]
source: ai-asset-registry/docs/knowledge-registry.md §1 (as of 2026-07-05); backend-mapping table from ai-asset-registry/docs/knowledge-review/architecture/system-boundaries.md (as of 2026-07-05)
review_after: 2026-08-05
---
**Context**: MCP servers, agents, models, and other AI asset types each need governance (system-of-record concerns) and discovery (consumption/browsing concerns) — the question was whether these belong in one system or should be split across specialized backends, with MLflow and Kubeflow both in play as candidate backends.

**Decision**: Split the two concerns onto purpose-built backends:
- **Registry = Governance** (system of record): identity, versioning, lifecycle state, policy linkage, lineage, approvals, auditability.
- **Catalog = Discovery** (consumption surface): browsing, searching, filtering, curation — helping users find assets.
- MLflow fills the registry role; Kubeflow (Hub) fills the catalog role. "MLflow is for registries. Kubeflow is for catalogs. We're done." — Adam Bellusci, 2026-04-07 sync.
- Registries are **metadata-first**: the actual asset is stored/run elsewhere; the registry governs metadata and context around it, not the asset payload itself.

**Consequences**: This split is the organizing principle for every asset-type registry (MCP servers, agents, models, prompts, skills, guardrails, knowledge sources) — each adopts the same governance/discovery boundary instead of a bespoke one-off design. It underpins evaluation, observability, gateway integration, lifecycle automation, policy enforcement, supply-chain management, and secure promotion, and enables inner-loop-to-outer-loop workflows (local dev → cluster dev → production).

**Backend mapping per asset type** (point-in-time snapshot, as of 2026-07-05):

| Asset type | Registry backend | Catalog backend |
|---|---|---|
| MCP servers | MLflow | Kubeflow (Hub) |
| Agents | MLflow | Kubeflow (Hub) |
| Models | Kubeflow Hub (fka Model Registry) → MLflow (future) | Kubeflow Hub |
| Prompts | MLflow Prompt Registry | Kubeflow (Hub) |
| Skills | MLflow (prototype) | Kubeflow (Hub) |
| Guardrails | TBD | Kubeflow (Hub) |

Models is the one asset type not yet on the registry side of this split (still Kubeflow-Hub-backed pending the MLflow move — see [fact-model-registry-kubeflow-hub.md](/features/platform/knowledge/fact-model-registry-kubeflow-hub.md)); Skills' "MLflow (prototype)" reflects the Databricks MVP branch state, not a finalized backend choice (see [fact-skills-registry-mvp-analysis.md](/features/skills-registry/knowledge/fact-skills-registry-mvp-analysis.md)). Guardrails backend is still TBD.

See [fact-ai-asset-registries-sync-transcript.md](/features/platform/knowledge/fact-ai-asset-registries-sync-transcript.md) for the meeting this decision came from, and [ref-ai-asset-registries-prd.md](/features/platform/knowledge/ref-ai-asset-registries-prd.md) for the PRD it anchors. Compare [fact-model-registry-kubeflow-hub.md](/features/platform/knowledge/fact-model-registry-kubeflow-hub.md), which shows Kubeflow Hub already living the "catalog" role for models today.
