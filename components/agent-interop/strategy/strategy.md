---
title: Agent Interop — strategy
description: Production-readiness layer for agents on RHOAI — OpenShell-anchored sandboxing, identity, policy, and interop. DP in 3.5, TP in 3.6 EA, GA in 3.7.
timestamp: 2026-07-30
status: current
review_after: 2026-09-30
source: hub.strategy from 60+ knowledge entries, 8-doc research series (2026-07-11 + 2026-07-27), 209-issue Jira snapshot; profiles/roadmap.md and profiles/strategy.md
---

## The brief

Agent Interop is the production-readiness layer for agents on Red Hat AI.
The bet: **OpenShell-anchored, defense-in-depth sandboxing is the gate
enterprises must pass before any agent reaches production** — 88% of agent
pilots fail at this gate
([fact-openshell-vs-agent-substrate](/components/agent-interop/knowledge/fact-openshell-vs-agent-substrate.md)).
Security + compliance differentiation compensates for RHOAI's 12-18 month
time-to-market gap versus Azure/AWS/Google
([00-executive-summary](/components/agent-interop/research/00-executive-summary.md)).

Where we are: Dev Preview shipping in RHOAI 3.5 (Jul-Aug 2026) as Helm-only
with Konflux pipeline setup. OpenShift path is experimental (privileged SCC
required). Next milestone: Tech Preview in 3.6 EA (Nov 2026) with operator,
SPIFFE identity, team-based policy, and observability.

## What

| Release | Scope | Status |
|---------|-------|--------|
| RHOAI 3.5 (DP) | OpenShell Helm install + docs/enablement; Konflux pipeline for images; no operator | Shipping |
| RHOAI 3.6 EA (TP) | Operator lifecycle (RHAISTRAT-1752); SPIFFE identity; team-based policy; observability; single + multi-player | Planned |
| RHOAI 3.6 GA / 3.7 EA | Agent deployment from catalog (OpenShell Go SDK + supported images); service binding; declarative agent onboarding | Planned |
| RHOAI 3.7 (GA) | Full identity, policy, discovery; OpenShell GA | Directional |

**Boundaries — what this is NOT:**

- Pre-deployment agent registry/catalog/discovery → [agent-registry](/components/agent-registry/)
- Starter-kit templates and catalog UI → [agent-catalog](/components/agent-catalog/)
- Agent observability/SDLC oversight → [agent-ops](/components/agent-ops/)
- MCP-level tool traffic governance → [mcp-gateway](/components/mcp-gateway/)
- Deployment is a shared workstream consumed by both catalog and registry, owned by neither (owner, 2026-07-16)

## Why

**The problem.** Enterprise agents need to call tools, fetch data, and interact
with external systems — each action is an unsanctioned network call from a
process running arbitrary LLM-generated code. Standard containers are
explicitly insufficient for this threat model
([05-landscape](/components/agent-interop/research/05-landscape.md)). No
competitor offers kernel-level isolation + hot-reloadable policy + credential
masking in a single product.

**The bet.** OpenShell's supervisor-based architecture (no sidecar injection,
kernel-level Landlock/seccomp/netns isolation, OPA-enforced egress,
credential injection without sandbox exposure) provides the right primitive
([fact-openshell-architecture](/components/agent-interop/knowledge/fact-openshell-architecture.md)).
NVIDIA co-engineering and the kubernetes-sigs/agent-sandbox SIG provide the
upstream foundation
([fact-nvidia-co-engineering-model](/components/agent-interop/knowledge/fact-nvidia-co-engineering-model.md)).

**Why now.** Three converging pressures:
1. **Regulatory**: NIST AI Agent Standards Initiative (Feb 2026), EU AI Act
   high-risk obligations (Aug 2026), FIPS 140-2 sunset (Sep 2026)
2. **Market**: Azure AI Foundry Agent Service GA'd May 2025; AWS Bedrock
   Agents GA'd Mar 2025 — waiting longer widens the gap
3. **Customer**: 88% of agent pilots fail at security; enterprise sandbox
   demand validated across multiple verticals
   ([ref-email-openshell-weekly-jun15](/components/agent-interop/knowledge/ref-email-openshell-weekly-jun15.md))

## Where we stand

**Decisions to date:**
- 2026-07-17: [Postgres as DP backend DB](/components/agent-interop/knowledge/decision-openshell-dp-postgres.md)
- 2026-07-17: [Base image dual path (Hummingbird + UBI/RHEL)](/components/agent-interop/knowledge/decision-openshell-base-image-dual-path.md)
- 2026-07-17: [GPU and confidential computing deferred past Oct/Nov](/components/agent-interop/knowledge/decision-openshell-defer-gpu-cc.md)
- 2026-07-11: Convergence onto OpenShell ([ref-email-openshell-convergence](/components/agent-interop/knowledge/ref-email-openshell-convergence.md))

**Delivery state:**
- Helm chart v0.0.85+ deploys on vanilla K8s and OpenShift (experimental)
- Sidecar topology (Topology B) now ships as a Helm value — not theoretical
- Layered sandboxing (OpenShell + Kata) validated on OpenShift 4.21
  ([ref-rh-developer-layered-sandboxing](/components/agent-interop/knowledge/ref-rh-developer-layered-sandboxing.md))
- Agent Sandbox SIG CRDs at v1beta1; API still changing fast
  ([ref-agent-sandbox-sig](/components/agent-interop/knowledge/ref-agent-sandbox-sig.md))

**In-flight:**
- NVIDIA co-engineering MVP scope-lock (Product/Consulting/Eco-system Eng/AI Eng)
- Konflux pipeline setup for downstream images
- Weekly OpenShell reports coordinating convergence

## Gaps & risks

**Critical (deployment blockers):**

| Gap | Why it matters | Tracking |
|-----|---------------|----------|
| [Privileged SCC on OpenShift](/components/agent-interop/knowledge/question-openshell-privileged-scc.md) | Enterprise customers flag as red flag; 3 mitigation paths identified (sidecar, user namespaces K8s 1.33+, layered Kata) but none production-validated on OCP yet | OpenShell #899, #1959; no RHAISTRAT |
| [No FIPS path](/components/agent-interop/knowledge/question-openshell-rust-fips.md) | Rustls + ring not FIPS-validated; FIPS 140-2 sunsets Sep 2026; blocks regulated customers. Phase 1 design specified (aws-lc-rs), SSH gap remains | OpenShell #900; no RHAISTRAT |
| [Multi-tenancy not implemented](/components/agent-interop/knowledge/question-openshell-multi-tenancy.md) | No per-tenant namespace scoping, quotas, or isolation. Recommended model exists but no implementation. Helm namespace split (#2485) is prerequisite | OpenShell #1722; no RHAISTRAT |
| [Gateway HA / leader election](/components/agent-interop/knowledge/question-openshell-gateway-ha.md) | Gateway is single point of failure; no documented HA, leader election, or HPA guidance. Multi-replica works but without guarantees | OpenShell #1012; no RHAISTRAT |

**High (enterprise readiness):**

| Gap | Why it matters |
|-----|---------------|
| [SKU / product home decision](/components/agent-interop/knowledge/question-openshell-sku-product-home.md) | RHOAI component vs separate operator vs OCP component — affects release cadence, engineering ownership, and entitlement model |
| [SPIFFE identity provisioning](/components/agent-interop/research/06-jira-gap.md) (G4) | RHAISTRAT-1730 covers authorization but NOT identity provisioning (SVID issuance, dynamic registration); the zero-trust foundation beneath authorization is untracked |
| [No Vault/KMS integration](/components/agent-interop/research/08-operations.md) | Provider credentials rotation is manual or OAuth2-only; no external secret store integration |
| [No official air-gap path](/components/agent-interop/research/07-deployment.md) | Practical approach works but is undocumented (NemoClaw #2218) |
| [Declarative config path](/components/agent-interop/knowledge/question-openshell-declarative-agent-config.md) | No CRD or K8s-native declarative path today; CRD consensus exists but design untracked |

**Tensions:**
- **Speed vs safety**: OpenShift experimental status vs customer demand for sandboxing now
- **Upstream vs downstream**: NVIDIA controls the Rust codebase, release cadence, and architecture decisions; Red Hat influence depends on contribution weight and co-engineering relationship
- **Support boundary**: harness binaries are "validated, not supported" ([fact-harness-support-boundary](/components/agent-interop/knowledge/fact-harness-support-boundary.md)) — customers may not understand the distinction

## Jira map

### Coverage (from ref- entries and [06-jira-gap](/components/agent-interop/research/06-jira-gap.md))

| Strategy element | Key(s) | Status |
|-----------------|--------|--------|
| OpenShell sandboxing integration | RHAISTRAT-1751, -1585 | Closed (decomposed) |
| OpenShell operator / OLM | RHAISTRAT-1752 | New |
| A2A protocol | RHAISTRAT-1356 | In Progress |
| BYO agent runtime compat | RHAISTRAT-1349 | In Progress |
| Agent authorization / policy | RHAISTRAT-1730 | New |
| Agent safety enforcement | RHAISTRAT-1269 | New |
| Agent lifecycle management | RHAISTRAT-1955 | New |
| Agent runtime contract | RHAISTRAT-2019 | New |
| Agent Hub UI / discovery | RHAISTRAT-1697 | In Progress |
| BYOA AgentOps journey | RHAISTRAT-1211 | In Progress |

Snapshot: 209 issues (96 RHAISTRAT, 113 RHOAIENG), swept 2026-07-11.
15 of 96 RHAISTRAT issues have ref- entries; 81 remain unmapped.

### Candidate jiras

**Tier 1 — file immediately (critical gaps, no downstream tracking):**

1. **FIPS 140-3 compliance for OpenShell on RHOAI** — Regulated customers
   cannot deploy without FIPS-validated crypto. Downstream build pipeline
   (aws-lc-rs), feature flag, SSH gap mitigation, CMVP tracking.
   → RHAIRFE or RHAISTRAT

2. **Restricted SCC compatibility for OpenShell sandboxes** — Privileged SCC
   is an enterprise deployment blocker on OpenShift. Topology B + user
   namespaces + Kata layered sandboxing qualification, SCC test suite.
   → RHAIRFE or RHAISTRAT

3. **Multi-tenancy model for agent sandboxes** — Production scale requires
   per-tenant namespace boundaries, quotas, gateway policy scoping, RBAC.
   No implementation exists. Helm namespace split is prerequisite.
   → RHAISTRAT

4. **Gateway HA for production deployments** — Gateway is single point of
   failure. Leader election, active-passive/active-active pattern, HPA
   guidance. Upstream engagement (#1012) or downstream engineering.
   → RHAIRFE or RHAISTRAT

**Tier 2 — next planning cycle:**

5. **SPIFFE identity provisioning for agent workloads** — Zero-trust
   foundation. SVID issuance, dynamic registration, Keycloak delegation
   chain. Distinct from RHAISTRAT-1730 (authorization).
   → RHAISTRAT

6. **Service binding for LLM endpoints in agent sandboxes** — Replace manual
   provider YAML with automatic injection of model endpoints, MCP gateway
   URLs. Developer experience gap from Kagenti.
   → RHAIRFE

7. **Air-gap deployment guide for OpenShell** — No official disconnected
   deployment path. Image/chart mirroring, internal model endpoints,
   operator catalog integration.
   → RHAIRFE

## Watchlist

| Date | Trigger | If it fires → |
|------|---------|---------------|
| Sep 21 2026 | FIPS 140-2 sunset | In-process CMVP is not valid compliance; aws-lc-rs migration becomes urgent blocker, not nice-to-have |
| Aug 2 2026 | EU AI Act high-risk obligations start | Agent transparency requirements become enforceable; eight-field agent record becomes table stakes ([fact-agent-registry-regulatory-record-fields](/components/agent-registry/knowledge/fact-agent-registry-regulatory-record-fields.md)) |
| Oct 23 2026 | RHOAI 3.6 code freeze | Operator (RHAISTRAT-1752) must be ready; TP scope locked |
| Ongoing | Agent Sandbox SIG v1beta1 → v1 | CRD breaking changes could require OpenShell rework; no migration guide exists |
| Ongoing | OpenShell #1012 (HA) resolution | If NVIDIA declines, downstream engineering needed for GA |
| Ongoing | NVIDIA OpenShell release cadence | Upstream velocity directly controls what Red Hat can downstream; weekly image build acceleration in progress |
| Ongoing | Microsoft ARD specification | May become the federated agent discovery standard; early adoption could be differentiating |

## History

- 2026-07-30 — **Creation** — initial strategy doc from 60+ knowledge
  entries, 8-doc research series (lenses 01-06 from 2026-07-11, 07-08
  from 2026-07-27), 209-issue Jira snapshot (2026-07-11), roadmap and
  strategy profiles. Covers full scope: sandboxing, identity, A2A,
  declarative config, deployment, operations. Four critical gaps
  identified (SCC, FIPS, multi-tenancy, gateway HA); 7 candidate jiras
  drafted. OpenShell GDoc intake + deployment/operations research run
  same session.
