---
title: "Skills Catalog research -- architecture and integration patterns"
description: Extend kubeflow/hub as 4th catalog type (proven pattern, lower risk) vs standalone Go+PostgreSQL; BFF pattern reuse (10th sidecar); disconnected pipeline (YAML-baked, ConfigMap, oc-mirror); source federation (YAML/Git/ARD); metadata normalization; trust tiers as labels; catalog-to-registry BFF orchestration; NVIDIA/npm/skills.sh reference architectures.
timestamp: 2026-07-23
lens: architecture
review_after: 2026-10-23
---

# Skills Catalog research -- architecture and integration patterns

## 1. RHOAI platform baseline

All RHOAI catalogs run on kubeflow/hub: Go REST server, PostgreSQL,
pluggable CatalogSourceProvider, BFF module in odh-dashboard. Three
asset types shipped (models, MCP servers, agents). Adding skills would
be the fourth, following the identical pattern.

### What a catalog surface consists of

OpenAPI-first Go REST server -> PostgreSQL (ML-Metadata ER model) ->
CatalogSourceProvider plugins -> BFF -> React/PatternFly 6 module.

The BFF pattern in odh-dashboard uses Webpack Module Federation with
per-asset-type BFF sidecars (currently 9). A skills-catalog-ui would
be the 10th. Read-only, simpler than agent-ops.

## 2. Build new vs extend hub

RHAISTRAT-1780 proposes a new standalone Go + PostgreSQL service. The
alternative: extend kubeflow/hub as the 4th asset type.

**Hub extension advantages**: reuses existing PostgreSQL schema,
REST framework, source aggregation pipeline, BFF integration, and
operator reconciliation. Avoids a new Deployment, Service, StatefulSet.
The MCP catalog and agent catalog both followed this extend-hub path.

**Standalone advantages**: team autonomy, performance isolation.

**Assessment**: the current direction (Git-backed, YAML-source,
read-only) is architecturally identical to the existing catalogs.
Extending kubeflow/hub is the lower-risk, lower-effort path. If a
separate service is chosen, the API contract should follow hub's
OpenAPI conventions.

## 3. Disconnected architecture

The existing pipeline: source repos (GitHub) -> image build
(Konflux/OSBS) bakes YAML into container image -> deployment mounts as
ConfigMap -> catalog service indexes at startup -> oc-mirror v2 for
air-gapped mirroring.

ConfigMap-based offline import: cluster admins create ConfigMap with
sources.yaml pointing to local YAML files. No internet required.

The `skills-metadata-collection` repo/image would follow the
`model-metadata-collection` pattern exactly.

**Design choice**: skill content (SKILL.md files + scripts) should be
bundled into the catalog image for disconnected, not just metadata.
"Stale-but-mirrored beats fresh-but-fetching" (agent-catalog research).

## 4. Source federation

| Source | Type | Connectivity | Priority |
|---|---|---|---|
| Red Hat skills | YAML (baked) | Disconnected-safe | Day 1 |
| Partner skills | YAML or Git-polled | Variable | Day 1 |
| Org-approved | Admin ConfigMap | Disconnected-safe | Day 1 |
| Community | Remote API | Connected-only | Post-GA |
| ARD-discoverable | ARD registry query | Connected-only | Future |

Pull model (catalog fetches from sources) follows the existing hub
pattern. No push/ingest API needed for MVP.

**Metadata normalization**: SKILL.md frontmatter, NVIDIA skill cards,
MLflow skill versions, and ARD descriptors all have different schemas.
A normalizing adapter per source type maps to hub's internal
representation (name, description, version, source URL, labels, trust
tier, customProperties).

## 5. Trust tier implementation

Trust tiers are **metadata labels**, not RBAC roles. They influence UI
presentation and admin decisions. Implementation: `trustTier` label on
catalog source configuration, inherited by all skills from that source.

Cryptographic verification for Red Hat-provided and partner-verified
follows existing image-signing patterns (cosign/Sigstore, OMS for
NVIDIA).

Future installation-permission gating would be enforced in the BFF
layer via SubjectAccessReview, not in the catalog backend.

NVIDIA's sync-time compliance gate pattern should be adopted: before a
skill enters the build-time YAML, CI validates metadata completeness,
license, and (eventually) security scan results. Build pipeline concern,
not catalog runtime.

## 6. Catalog-to-registry integration

BFF orchestration, not new protocol. BFF translates catalog skill
metadata into an MLflow `register_skill()` call. Version tracking via
`.mlflow_skill_info` sidecar. User-initiated pull only, no automated
sync.

Installation features location remains the hardest open question. If
catalog ships before registry, catalog needs its own install path. If
both ship, the unified path (catalog -> register -> install) adds
friction. Needs its own STRAT.

## 7. Ecosystem reference architectures

**NVIDIA**: source-of-truth in product repos, daily sync to aggregated
catalog, compliance gates at sync time. Distribution via npx.

**skills.sh**: metadata-only indexing (no artifacts), npm as identity
layer. Scale model (669K+) with thin infrastructure. Poor security.

**npm**: metadata separated from artifacts early. CouchDB for metadata,
CDN for tarballs. Incremental replication for mirrors.

**ARD**: federated pre-invocation discovery. Two primitives:
ai-catalog.json + registry API. Future catalog source type.

**JFrog**: scan-verify-sign on upload. Promotion model with increasing
security gates. NVIDIA partnership.

## Key findings

1. **Extend kubeflow/hub** -- same pattern, lower risk, proven.
2. **BFF pattern directly reusable** -- 10th sidecar, read-only.
3. **Disconnected pipeline is the same pipeline** -- YAML, ConfigMap,
   oc-mirror.
4. **Metadata normalization is the real work**.
5. **Trust tiers are labels, not RBAC**.
6. **Adopt NVIDIA's sync-time compliance gate pattern**.
7. **Catalog-to-registry is BFF orchestration**.
8. **Installation location is the hardest open question**.
9. **Metadata-only indexing enables scale; curation enables trust**.
