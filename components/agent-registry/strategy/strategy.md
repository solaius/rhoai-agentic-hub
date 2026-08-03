---
title: Agent Registry — strategy
description: Living strategy for the RHOAI Agent Registry — MLflow-based governed inventory of agents (discover/register/audit), A2A schema, phased delivery (3.5 templates → 3.6 registry → 3.7+ federation), wedge is self-managed/disconnected/governed with a 6-9 month window; dependency immutability is the differentiator no competitor has.
timestamp: 2026-08-03
status: current
review_after: 2026-10-03
source: hub.strategy — synthesized from 13-doc research series (07-16 + 08-03 refreshes), product scoping doc (Adel Zaalouk, 08-03), Jira snapshot (07-16), and knowledge base (63 entries)
---

## The brief

The Agent Registry is a governed inventory of agents: what exists, who
owns it, what it can do, and where it's running. MLflow backend, A2A
Agent Card schema, catalog-as-read-only-view. The bet: **the only
self-managed, disconnected-capable, governed fleet registry with
lineage** — validated by the market gap (no competitor ships this) and
regulation (EU AI Act live Aug 2, mandating the record shape). Two GA
cloud competitors now (Google July 30, Microsoft May 1), AWS imminent.
The window is 6-9 months. Next milestone: RFC-0008 Phase 2 upstream
input (agent entity design), then RHAISTRAT-1436 backend work starting
3.6 EA2 at the earliest.

## What

### Release train

| Release | Scope | Status |
|---------|-------|--------|
| **3.5 (Now)** | Rudimentary agent catalog (starter-kit templates, link-out only); agent metadata schema definition (A2A-based); MLflow MCP Registry ships (RFC-0004, establishing the pattern) | In progress |
| **3.6 EA1** | Agent Catalog TP; deployments view; agent deploy from catalog (OpenShell Go SDK + supported images); registry-view data-source decision needed | Committed |
| **3.6 EA2** | Agent Registry RFC to MLflow upstream; Agent Registry backend in RHOAI (RHAISTRAT-1436: register, search, lifecycle, RBAC); dashboard integration | Work starts at earliest |
| **3.6 GA** | Agent Registry TP; sandboxing UI + runtime connection foundation | Directional |
| **3.7+ (Later)** | Shadow IT visibility (surface unregistered agents); policy enforcement integration; cross-cluster discovery (ARD/A2A); federation; Agent Registry DP (~3.7 EA1 directional) | Future |

### Boundaries

| This component IS | This component IS NOT | See instead |
|---|---|---|
| Governed inventory of agents (definitions + runtime state) | Agent deployment system | agent-catalog (deploy path), agent-interop (OpenShell runtime) |
| Metadata record (A2A schema, MLflow store) | Agent observability platform | MLflow tracing + OpenTelemetry |
| Catalog-as-read-only-RBAC-view of registry | Separate catalog service | [decision](/components/agent-registry/knowledge/decision-agent-catalog-is-registry-view.md) |
| Single-cluster governance (MVP) | Cross-cluster federation (MVP) | 3.7+ roadmap |
| Identity linkage (records SPIFFE/SA refs) | Identity system (issues identities) | agent-interop (SPIFFE/SPIRE, OpenShell) |

## Why

### The jobs

Platform teams cannot answer "how many agents are running, who owns
them, and what can they do?" — 82% of enterprises discovered unknown
agents their security teams didn't know about (Gravitee, HFS, Zenity —
[research/10](/components/agent-registry/research/10-requirements.md)
§2). Shadow agents are the #1 CISO risk for 2026 (Forrester —
[research/12](/components/agent-registry/research/12-requirements-refresh.md)
§1.2). Regulation now mandates the record: EU AI Act (Art. 26/49/50),
OMB M-25-21, NIST GV-1.6/CSA — eight fields converge
([fact-regulatory-record-fields](/components/agent-registry/knowledge/fact-agent-registry-regulatory-record-fields.md)).

11 customer-validated problems (P1-P11) from 10+ enterprise customers
independently confirmed by industry surveys
([research/12](/components/agent-registry/research/12-requirements-refresh.md)
§1). Three end behaviors: **discover** (find what exists), **register**
(make it governed), **audit** (query who/what/where)
([fact-product-scope](/components/agent-registry/knowledge/fact-agent-registry-product-scope.md)).

### The wedge

Nobody ships a self-managed, disconnected, governed fleet registry with
lineage. Every hyperscaler registry is cloud-locked (Google=GCP,
Microsoft=M365/Azure, AWS=Bedrock, IBM=SaaS, Databricks=Unity). All
funded startups ($160M+ across 7 entrants) are SaaS. The open-source
slot is contested (Solo.io agentregistry, CNCF Sandbox pending) but
none has air-gapped support yet.

Gartner's inaugural "Guardian Agents" Market Guide (Feb 2026)
explicitly calls for "independent guardian agent layers that work across
clouds and platforms" — this IS the RHOAI positioning
([research/13](/components/agent-registry/research/13-competitive.md)
§3).

**The differentiator no competitor has**: dependency immutability
enforcement — ensuring that ACTIVE agents' pinned skill/MCP
dependencies cannot be unilaterally deprecated by the owning team. OCI
digest-pinning semantics + negotiated deprecation
([research/12](/components/agent-registry/research/12-requirements-refresh.md)
§3).

### Window

Estimated **6-9 months** (down from 6-12 in July). Time-boxed by:
IBM's eventual on-prem Agentic Control Plane port, Solo.io
agentregistry CNCF Sandbox + air-gapped support, and Microsoft
cross-cloud registry sync maturation
([fact-market-position](/components/agent-registry/knowledge/fact-agent-registry-market-position.md)).

## Where we stand

### Decisions to date

- **2026-08-03** — Agent catalog is a read-only RBAC view of the
  registry, not a separate service
  ([decision](/components/agent-registry/knowledge/decision-agent-catalog-is-registry-view.md))
- **2026-07-16** — Registry work starts 3.6 EA2 at the earliest,
  multi-release path to DP (~3.7 EA1 directional)
  ([roadmap](/memory/profiles/roadmap.md))
- **2026-07-10** — Kagenti removed from roadmap; OpenShell expands to
  cover its capabilities
  ([fact](/components/agent-registry/knowledge/fact-kagenti-roadmap-removal.md))

### Delivery state

- **MLflow upstream**: RFC-0008 (Skill Registry Phase 1) is the live
  upstream conversation (PR #26, draft). Agent entity deferred to Phase
  2 — Red Hat needs to author Phase 2 input. The RFC-0008 author is
  also the RHAISTRAT-1436 assignee — upstream/downstream share an
  author
  ([fact](/components/agent-registry/knowledge/fact-mlflow-rfc-0008-skills-phase1.md)).
- **Varsha's proposal branch** is dormant (no commits since 2026-04-23).
  The `AgentDiscoveryProvider` plugin interface survives; the kagenti
  reference plugin does not. Needs re-baselining onto Sandbox/OpenShell
  ([fact](/components/agent-registry/knowledge/fact-agent-registry.md)).
- **Enumeration and enrichment have split**: Sandbox CRs enumerate
  workloads but carry zero agent semantics. No component fetches or
  verifies A2A agent cards. `verified`/`identity`/`trust_domain` have no
  producer
  ([fact](/components/agent-registry/knowledge/fact-agent-registry-post-kagenti-discovery-gaps.md)).
- **Product scope defined** (Adel Zaalouk, 2026-08-03): three end
  behaviors, seven exclusions, phased delivery, A2A schema, catalog-as-view
  ([ref](/components/agent-registry/knowledge/ref-agent-registry-scoping-gdoc.md)).

## Gaps & risks

### Open questions (from knowledge base)

| Question | Evidence state | Why it matters |
|----------|---------------|----------------|
| [Agent versioning for non-deterministic systems](/components/agent-registry/knowledge/question-agent-versioning-nondeterministic.md) | Four-layer model + eval-gated promotion (12 §2) | Schema must version code/prompt/model/tools independently; SemVer alone fails |
| [Dependency permanence](/components/agent-registry/knowledge/question-agent-dependency-permanence.md) | OCI digest-pinning + negotiated deprecation (12 §3); no competitor solves this | Differentiator — enforce immutable dependencies for ACTIVE agents |
| [Visibility scoping](/components/agent-registry/knowledge/question-agent-visibility-scoping.md) | Three-tier (public/restricted/private) + Bazel deprecation-visibility (12 §4) | Multi-tenant discovery boundaries; default should be restricted |
| [Backend dual-entity model](/components/agent-registry/knowledge/question-agent-registry-backend-dual-entity.md) | RHAISTRAT-1436 is single-entity; research recommends dual (AgentVersion + instance) | Schema-freeze-sensitive — cheap before EA2, breaking after |
| [Pre/post-deployment relationship](/components/agent-registry/knowledge/question-agent-registry-pre-deployment-relationship.md) | Regulators need both "approved" and "running" views (10 §1.2) | Drives the dual-entity architecture |
| [EA1 registry-view data source](/components/agent-registry/knowledge/question-registry-view-ea1-data-source.md) | Registry TP lands before its own backend; stopgap collapses the two-view model | Product decision needed before EA1 build |
| [BYO agent discovery post-kagenti](/components/agent-registry/knowledge/question-byo-agent-discovery-labels.md) | Only vehicle (RHAISTRAT-1955) targets the removed substrate | BYO/Mode-1 agents invisible without this |

### Risks

1. **1436 schema freezes before design input lands.** The backend schema
   is single-entity with no runtime states, no SUSPENDED, no
   `version_ref`, no risk-tier/log-refs/retention. The shared author
   with RFC-0008 is the channel — but the schema freeze date is
   unconfirmed.
2. **Card-verification vehicle closed with no successor.** RHAISTRAT-1956
   Closed (Won't Do), entire card chain (1956, 1213, 1599) closed.
   `verified=true` has zero paths. The most urgent re-file.
3. **Solo.io CNCF Sandbox decision** may land before RHOAI ships.
   agentgateway already has air-gapped docs; agentregistry following
   would weaken the disconnected differentiator.
4. **Microsoft cross-cloud sync** could mature from preview to GA,
   weakening RHOAI's multi-cloud governance claim.
5. **Missing requirements in the product scope**: NHI identity lifecycle,
   inter-agent boundary testing, eval status as metadata, cost
   attribution tags, context/grounding declaration — eight gap
   requirements surfaced by research but not in P1-P11.

## Jira map

### Coverage

| Strategy element | Key(s) | Type | Status |
|---|---|---|---|
| Unified governance (umbrella) | RHAISTRAT-1355 | Outcome | In Progress |
| Agent Hub UI (registry + deployments views) | RHAISTRAT-1697 | Outcome | In Progress |
| Deployments view (running instances) | RHAISTRAT-1758 | Feature | In Progress (3.5 GA) |
| Deploy from catalog | RHAISTRAT-1742 | Feature | In Progress (3.6 EA1) |
| Registry backend (MLflow-native) | RHAISTRAT-1436 | Feature | New (unscheduled) |
| Agent lifecycle management (registration CR) | RHAISTRAT-1955 | Feature | New (stranded on kagenti) |
| Agent metadata extraction | RHAISTRAT-1956 | Feature | **Closed** (Won't Do) |
| Runtime contract (agent obligations) | RHAISTRAT-2019 | Feature | New |
| Registry UI | RHAIRFE-1313 | Feature Request | Stakeholder review |
| Agent metadata extraction (demand side) | RHAIRFE-2388 | Feature Request | Approved |
| Agentic base images | RHAIRFE-2443 | Feature Request | Approved |

### Candidate jiras

Gap → problem statement → suggested project, ready for `/rfe.create`.

1. **Card-verification successor** — no component fetches or verifies
   A2A agent cards post-kagenti; `verified=true` has zero paths; the
   registry needs a card-fetch + JWS-verification loop as a first-class
   enrichment service → RHAISTRAT (Feature under RHAISTRAT-1355)

2. **Dual-entity / runtime-state schema input** — RHAISTRAT-1436's schema
   is single-entity with one lifecycle; regulators require both
   "approved" and "running" views; instance states
   (ACTIVE/UNHEALTHY/STALE/REMOVED + SUSPENDED) and `version_ref` join
   are needed before the EA2 schema freeze → RHAISTRAT (schema input to
   RHAISTRAT-1436)

3. **Shadow-agent inventory + adopt-into-governance** — 82% of orgs
   discover unknown agents; zero Jira work covers unlinked-instance
   records or the adopt-into-governance flow; the registry needs an
   unregistered-workload reconciler → RHAIRFE (Feature Request)

4. **Regulatory record completion** — the eight-field record mandated by
   EU AI Act/NIST/CSA is partially covered (owner, compliance tags) but
   missing risk-classification, log/audit-trail refs, identity/
   permissions linkage, and retention commitment (≥6 months on removed
   records) → RHAISTRAT (schema input to RHAISTRAT-1436)

5. **Dependency immutability enforcement** — no existing registry
   prevents cascading breaks from dependency deprecation; RHOAI can
   differentiate with OCI-style digest-pinning + negotiated deprecation;
   agent registration records should declare skill/MCP dependencies at
   exact versions → RHAIRFE (Feature Request)

6. **Visibility scoping** — multi-tenant discovery needs three-tier
   visibility (public/restricted/private) with Bazel-style
   deprecation-visibility interaction; default should be restricted
   (workspace-scoped), "no list-all path" at the data-access layer →
   RHAIRFE (Feature Request)

## Watchlist

| Trigger | Expected | If it fires → what changes |
|---------|----------|---------------------------|
| AWS Agent Registry GA | Post-Aug-6 namespace migration; likely re:Invent (Nov/Dec) or sooner | Three GA cloud competitors; removes "preview-only" caveat from competitive comparisons |
| Solo.io agentregistry CNCF Sandbox decision | Board review may have occurred; decision pending | OSS legitimacy; if accepted, becomes the default K8s-native registry |
| Solo.io agentregistry air-gapped docs | Unknown | Directly erodes the disconnected differentiator |
| IBM Agentic Control Plane on OpenShift | Think 2027 plausible (Q2) | Closes IBM's on-prem gap; strongest validation of the market but most direct competition |
| Microsoft cross-cloud sync GA | Unknown (preview now) | De facto multi-cloud governance overlay if it matures |
| Google ARD adoption beyond Google | Next 6 months | If adopted, becomes the federated discovery standard RHOAI must support |
| NIST SP 800-53 agent overlays | Q4 2026 target | Creates explicit procurement requirements for agent registries |
| MLflow RFC-0008 Phase 1 review concludes | Unknown | Window for Phase 2 agent-entity input closes |
| Forrester ADP Wave | Q4 2026 | Analyst positioning for agent development platforms |
| RHAISTRAT-1436 EA2 schema freeze | Unconfirmed | Last moment for dual-entity, runtime states, regulatory fields |

## History

- 2026-08-03 — **Creation** — first strategy document, synthesized from
  13-doc research series (April 2026 original + July 16 refresh + August
  3 requirements + competitive refreshes), product scoping doc (Adel
  Zaalouk), Jira snapshot, and 63 knowledge entries. Replaces the
  placeholder strategy-status.md.
