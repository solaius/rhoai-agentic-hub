---
title: "Agent Registry research — post-kagenti architecture"
description: The post-kagenti reference architecture for the RHOAI agent registry — Sandbox-CR discovery, the card-verification gap, dual-entity resolution, register-on-deploy, governance mapping, and base-image provenance.
timestamp: 2026-07-16
lens: architecture
review_after: 2026-10-16
---

# Agent Registry research — post-kagenti architecture

> Superseded 2026-07-16 (same day) in one respect by [11-jira-gap](11-jira-gap.md) — RHAISTRAT-1956, named throughout this doc as the only card-verification vehicle, closed between 2026-07-11 and 2026-07-16 with no successor (clone RHAIRFE-2388 still Approved); read "the only vehicle" as "no active vehicle exists". Also: the EA2 backend is tracked after all (RHAISTRAT-1436, unscheduled).
>
> Superseded 2026-07-16 (same day) in a second respect by an owner re-timing (recorded in [/memory/profiles/roadmap.md](/memory/profiles/roadmap.md) History): the roadmap frame used throughout — "Agent Registry TP 3.6 EA1; backend EA2; GAs in 3.6" — is retired. Registry work starts **3.6 EA2 at the earliest**, on a multi-release path to DP (~3.7 EA1 directional, no committed GA); deployment (BFF → Go SDK) is **its own workstream** that catalog and registry both consume. Read §4.3's sequencing table and every "EA1 registry view / EA2 backend" reference through that lens — the §4.3 stopgap warning gets stronger, not weaker (any early registry view now predates its backend by even more).

**Date**: 2026-07-16
**Lens**: architecture
**Replaces the architecture spine of**: [03-kagenti-and-kubernetes](03-kagenti-and-kubernetes.md) (2026-04-24) — see the supersedes section at the end.

Kagenti was removed from the roadmap on 2026-07-10 ([fact-kagenti-roadmap-removal](/features/agent-registry/knowledge/fact-kagenti-roadmap-removal.md)); the platform's agent-runtime bet converged on OpenShell (NVIDIA-origin supervisor-model sandbox) plus the kubernetes-sigs agent-sandbox `Sandbox` CRD. This document rebuilds the registry's integration architecture on what actually exists on a 3.6-era RHOAI cluster, keeping what survives of Varsha Prasad Narsing's [upstream proposal](/features/agent-registry/strategy/upstream-proposal.md) (the `AgentDiscoveryProvider` plugin model, the Agent entity, the ACTIVE/UNHEALTHY/STALE/REMOVED lifecycle) and replacing everything that was kagenti-shaped.

## Platform baseline (ground truth)

Standing context: the **`architecture/rhoai-3.5-ea.2`** snapshot in [opendatahub-io/architecture-context](https://github.com/opendatahub-io/architecture-context) (generated 2026-06-22, 65 components), per [ref-opendatahub-architecture-context-repo](/features/platform/knowledge/ref-opendatahub-architecture-context-repo.md). The sibling catalog architecture doc ([agent-catalog/research/03-architecture](/features/agent-catalog/research/03-architecture.md), 2026-07-16) established the dashboard/BFF topology from the same snapshot; this doc adds the MLflow-side detail.

What matters for the registry, from the snapshot:

- **MLflow** ships as a stateless containerized service managed by the platform operator: PostgreSQL backend, workspace-scoped RBAC (plus kube-rbac-proxy TokenReview at the sidecar), REST `/api/2.0|3.0/mlflow/*`, OTLP trace ingestion at `v1/traces`, an AI Gateway subsystem proxying LLM providers, and a Huey task queue for async jobs — Varsha's proposal assumed exactly this Huey/poll + background-watch + webhook substrate, and it is present ([architecture-context mlflow.md, rhoai-3.5-ea.2](https://github.com/opendatahub-io/architecture-context/blob/main/architecture/rhoai-3.5-ea.2/mlflow.md), 2026-06-22).
- **Dashboard** is a module-federation host with per-asset BFF sidecars, including an **agent-ops BFF (port 8843)**; the RHOAI 3.5 agents table discovers agents by **listing Sandbox CRs, read-only** (no deploy in 3.5, decision 2026-07-09). The 3.6 deploy path is dashboard BFF → **OpenShell Go SDK**.
- **The snapshot still documents kagenti** (`agents-operator.md`: AgentCard/AgentRuntime CRDs, AuthBridge, SPIFFE, JWS-signed cards, MLflow auto-discovery and tracking env-var injection, and — notably — support for `agents.x-k8s.io/Sandbox` workloads). Treat that component doc as design-concept reference only; the capabilities it describes are precisely the ones whose loss Section 1.4 inventories.
- **OpenShell Kubernetes support is explicitly experimental** — "the Kubernetes deployment path is under active development. Expect rough edges and breaking changes" ([NVIDIA/OpenShell README](https://github.com/NVIDIA/OpenShell), fetched 2026-07-16); the hub's interop entries additionally record privileged-SCC and TLS-disabled caveats ([interop 00-executive-summary](/features/agent-interop/research/00-executive-summary.md)). The Go SDK the deploy path depends on is a six-PR series whose first PR — foundation plus a functional **sandbox client only**, all other clients stubbed `Unimplemented` — is open as of 2026-07-16 ([NVIDIA/OpenShell#2271](https://github.com/NVIDIA/OpenShell/pull/2271), opened 2026-07-14).

Roadmap frame: Agent Catalog TP + Agent Registry TP in 3.6 EA1; Agent Registry backend 3.6 EA2; GAs in 3.6. Strategy invariant: registry = governance (MLflow), catalog = discovery (kubeflow/hub); metadata-first, plugin-based.

## 1. Discovery sources on a 3.6-era cluster

What can an MLflow `AgentDiscoveryProvider` actually read? Four sources, with very different information content. The key structural finding: **enumeration and enrichment have split**. Kagenti's AgentCard CRD was both (it enumerated agents *and* carried their full A2A metadata, pre-verified). Nothing on a post-kagenti cluster does both.

### 1.1 Sandbox CRs — enumeration, no agent semantics

The `Sandbox` kind (`agents.x-k8s.io/v1beta1` — **not** "AgentSandbox"; v1beta1 landed June 2026, current release v0.5.1, 2026-07-09) is what the dashboard's 3.5 agents table already lists, filtered on the `openshell.ai/managed-by` label. Its full field surface ([Agent Sandbox API reference](https://agent-sandbox.sigs.k8s.io/docs/api/); [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox)):

| Where | Fields |
|---|---|
| `spec` | `podTemplate`, `volumeClaimTemplates`, `service` (bool — auto headless Service), `shutdownTime`, `shutdownPolicy` (default Retain), `operatingMode` (Running/Suspended) |
| `status` | `serviceFQDN`, `service`, `conditions`, `selector`, `podIPs`, `nodeName` |

Read that list carefully: **there is no agent metadata anywhere in it**. No name-as-agent, no skills, no protocol, no card, no verification status. A Sandbox CR tells the registry that *an isolated stateful workload exists*, what image it runs (`spec.podTemplate.spec.containers[].image`), where to reach it (`status.serviceFQDN`), and whether it is up (`status.conditions`) or suspended (`spec.operatingMode`). Everything the registry's data model calls agent semantics — `protocol`, `skills`, `securitySchemes`, `verified` — must come from somewhere else. The upstream SIG is deliberate about this: agent-sandbox is a workload-isolation API, not an agent-introspection API.

**Capability mapping**: native `list` → `POLL`; native Kubernetes watch → `WATCH` (the natural fit — the plugin inherits etcd consistency and controller reconciliation for free); or a sync controller pushes CR state at the registry → `WEBHOOK` (Section 3). Liveness derivation is clean: CR exists + conditions ready → candidate ACTIVE; `operatingMode: Suspended` → a state Varsha's model doesn't have (see 4.3); CR deleted → STALE → REMOVED after grace.

### 1.2 OpenShell gateway state — lifecycle truth, SDK-gated

The OpenShell gateway is the control-plane API and authentication boundary: it holds sandbox lifecycle state and metadata, active (hot-reloadable) policy configurations, provider credential bundles, and audit logs of policy decisions ([NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell)). For agents deployed the platform way, the gateway knows things the Sandbox CR does not: session state, policy in force, egress denials — the raw material for a *behavioral* health signal rather than a pod-liveness one.

But access is gRPC via the Go SDK, and as of 2026-07-16 only the sandbox client of that SDK is functional ([#2271](https://github.com/NVIDIA/OpenShell/pull/2271) — policy, service, gateway clients are PRs D–E of the series). **Capability mapping**: `POLL` only, realistically, and not before the SDK series completes; no watch/streaming surface is exposed yet. Treat gateway state as a *future enrichment source* (policy posture, audit-derived health), not as the discovery backbone. Building the registry's discovery on the gateway would also couple it to a single runtime — the same mistake as building it on kagenti.

### 1.3 A2A agent cards — enrichment, currently orphaned

The A2A 1.0 spec (ratified; ACP merged into it) defines the AgentCard — identity, provider, capabilities, skills, interfaces, security schemes — discovered at the well-known path and optionally **JWS-signed**, with canonicalization, signature format, and verification procedures specified (spec §8, §8.4; extended authenticated card via `capabilities.extendedAgentCard`) ([A2A specification 1.0](https://a2a-protocol.org/latest/specification/)). The platform's container contract guarantees the endpoint exists on supported harnesses: port 8000, `/.well-known/agent-card.json` ([fact-agent-catalog-starter-kits](/features/agent-catalog/knowledge/fact-agent-catalog-starter-kits.md)); the agent runtime contract work (RHAISTRAT-2019, paraphrased) formalizes it.

This is where the actual agent semantics live — and **nobody on the post-kagenti cluster fetches it**. Combining 1.1 + 1.3 is the recovery path: enumerate via Sandbox CRs, then HTTP GET the card at `status.serviceFQDN`, verify signatures, and merge. **Capability mapping**: `POLL` (HTTP fetch on a schedule or on CR-change trigger); no watch; cards are enrichment keyed to an enumeration source, never an enumeration source themselves (you cannot list well-known URLs you don't know about).

### 1.4 Static/deploy-time registration — the seed

The catalog's `agent.yaml` plus the user's declared configuration (binding output — RHAIRFE-2310/2309, paraphrased) is the richest metadata the platform will ever have about an agent, available at the exact moment of deployment, before the pod even starts. **Capability mapping**: `WEBHOOK` — the deploy path POSTs a registration. This is the "register on deploy" half of Section 3. Varsha's static-file plugin also survives trivially for air-gapped/manual inventory.

### 1.5 Summary table

| Source | Yields | POLL | WATCH | WEBHOOK | Status (2026-07) |
|---|---|---|---|---|---|
| Sandbox CRs (`agents.x-k8s.io/v1beta1`) | existence, image digest, endpoint FQDN, conditions, suspend state, labels | yes | **yes — natural fit** | via sync controller | shipping; dashboard 3.5 lists them |
| OpenShell gateway (gRPC/Go SDK) | lifecycle state, policy posture, audit/health | eventually | no surface yet | no | SDK PR A only; experimental k8s |
| A2A agent card (`/.well-known/agent-card.json`) | full agent semantics, JWS signatures | yes (enrichment) | no | no | endpoint contractually present; **no fetcher exists** |
| Deploy-time registration (catalog + binding) | declared config, owner, version identity | n/a | n/a | **yes — richest** | 3.6 EA1 deploy path |

### 1.6 What kagenti provided that now has NO equivalent

Doc 03 built on six kagenti capabilities. Their post-kagenti status:

1. **Automatic card fetch and in-cluster caching** (`status.agentCardJSON`) — **gone, no equivalent**. The registry plugin (or a new controller) must own the fetch. Until something does, every discovered agent is semantics-blind.
2. **JWS verification bound to SPIFFE x5c** (the `status.verified` bit, end-to-end pod-identity→metadata trust chain) — **gone, no equivalent**. The registry schema's `verified` / `identity` / `trust_domain` fields ([upstream-proposal](/features/agent-registry/strategy/upstream-proposal.md)) currently have **no producer**. The Red Hat three-layer identity model (SPIFFE transport + AuthBridge/Keycloak application layer + lifecycle, next.redhat.com June 2026, per [interop 00-executive-summary](/features/agent-interop/research/00-executive-summary.md)) supplies workload identity and the mTLS channel for a mutually-authenticated fetch — but no component signs cards or verifies signatures. RHAISTRAT-1956 (agent metadata extraction — mutually-authenticated capability sync, paraphrased) is the Jira-side vehicle; it is now the *only* path to a `verified=true` agent record.
3. **Label-based BYO auto-discovery** (`kagenti.io/type: agent` on arbitrary Deployments/StatefulSets) — **gone**. Sandbox-CR discovery only sees sandbox-shaped workloads. A Mode-1/BYO agent running as a plain Deployment ([fact-agent-deployment-modes](/features/agent-catalog/knowledge/fact-agent-deployment-modes.md)) is invisible unless a new label convention is established. This is a real regression in discovery coverage, currently untracked.
4. **MLflowReconciler push** — **gone as code, alive as pattern**: ODH ADR #142 rebuilds it for MCP servers (Section 3.2).
5. **Verification-keyed network policy** — moved to OpenShell's policy engine, but keyed to policy config, not to card verification. Registry-relevant only as future gateway enrichment.
6. **MLflow tracking env-var injection / AgentRuntime config** — was an agents-operator behavior per the snapshot; must now be re-implemented in the deploy path (binding) or OpenShell driver config. Registry-relevant because trace linkage (Section 2) depends on it.

Gaps 1–3 compound into the headline: **on a post-kagenti cluster the registry can know that agents exist, but not what they are or whether to trust them, unless the registry-side machinery does the work kagenti used to do.**

## 2. Dual-entity resolution: record vs instance

### 2.1 The two patterns

- **Pattern A — one entity, lifecycle stages.** A single Agent record moves through "defined → approved → deployed → running". Simple, but it cannot represent the actual cardinalities: one version, N instances (scale-out, multi-cluster); one instance surviving several governance changes; instances with no governed record (out-of-band deploys).
- **Pattern B — separate entities with references.** Pre-deployment `RegisteredAgent` + `AgentVersion` (the MCP two-tier pattern, [fact-mcp-registry-data-model-proposal](/features/mcp-registry/knowledge/fact-mcp-registry-data-model-proposal.md)) and post-deployment `Agent` instance records (Varsha's entity, unchanged), joined by a hard reference `instance.version_ref → AgentVersion`. Varsha's schema already reserves the seam: its `version` field is "informational" — the design move is to promote it to a first-class foreign reference, nullable for discovered-but-unlinked instances.

Pattern B is the recommendation, and it is what the platform's own Jira shape already implies: RHAISTRAT-1697 (registry view — all *registered* agents) and RHAISTRAT-1758 (deployments view — *running instances* from sandbox runtime CRs) are explicitly distinct surfaces (paraphrased). Two views, two entities.

### 2.2 MLflow mechanics: LoggedModel as the version hub

MLflow 3 already has the version-side entity. A **LoggedModel** "acts as a metadata hub, linking a conceptual application version to its specific external code (e.g., a Git commit), configurations, and associated MLflow entities like traces and evaluation results"; `mlflow.create_external_model()` creates version records for agents whose code/weights don't live in MLflow, and `mlflow.set_active_model()` auto-links execution traces to the version ([MLflow: Version Tracking for Agents and LLMs](https://mlflow.org/docs/latest/genai/version-tracking/); [LoggedModel data model](https://mlflow.org/docs/latest/genai/data-model/logged-model)). Registered-model versions link back to the LoggedModel/run that produced them ([MLflow Model Registry](https://mlflow.org/docs/latest/ml/model-registry/)).

Concretely for the agent registry plugin: `AgentVersion` should either *be* a LoggedModel specialization (plugin-architecture route) or carry `logged_model_id`. Then the lineage chain closes end-to-end: **instance → AgentVersion → LoggedModel → git commit + traces + eval runs** — and because the deploy path injects MLflow tracing env vars (gap 6 above, when re-implemented), production traces from a running instance land on the same version record its governance state lives on. That is the registry's differentiated answer to "which definition is this instance based on, and how is it behaving?" (Emilio Garcia's question from doc 06, finally with mechanics).

### 2.3 What AWS and Databricks do

- **AWS Agent Registry** (preview 2026-04-09) is record-centric: it stores agents, tools, MCP servers, and skills "as a structured record", versioned, with an approval workflow (draft → pending approval → discoverable) and deprecation — while *running* agents are AgentCore runtime's concern. Registration is manual (console/SDK/API) or by **pointing the registry at an MCP or A2A endpoint, which it ingests automatically** ([AWS blog](https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/), 2026-04). So AWS also splits record from runtime — and its endpoint-ingestion is exactly the card-fetch enrichment of Section 1.3, validating that the *registry side* owns the fetch.
- **Databricks** is version-centric: the LoggedModel is the agent version; deployment is tracked through registered-model aliases and deployment jobs rather than a separate instance entity ([Databricks version concepts](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/version-concepts)). Databricks can get away without an instance entity because it owns the serving plane; RHOAI cannot — Kubernetes deployments happen outside the platform's front door (GitOps), which is precisely why Varsha's instance entity plus discovery exists.

Neither vendor exposes "Register" as an end-user catalog verb — registration is a side-effect or an ingestion — consistent with the sibling catalog finding ([question-agent-catalog-register-vs-deploy](/features/agent-catalog/knowledge/question-agent-catalog-register-vs-deploy.md)).

### 2.4 The join keys

How does a discovered instance find its AgentVersion? In order of strength:

1. **Stamped identity (platform path)**: the deploy path writes registry IDs (`registry.opendatahub.io/agent-version-id`, or similar) as **annotations on the Sandbox CR** at creation. Reconciliation becomes a lookup. Zero ambiguity; costs one line in the deploy flow. This should be a hard requirement of the 3.6 deploy path.
2. **Image digest**: `spec.podTemplate.spec.containers[].image` by digest matches the AgentVersion's recorded image. Necessary but not sufficient — Mode-2 agents share harness images and differ only in configuration ([fact-agent-deployment-modes](/features/agent-catalog/knowledge/fact-agent-deployment-modes.md)), so digest narrows to the harness, not the version. Digest + declared-config hash is the workable composite.
3. **Card identity**: fetched agent card name/provider/version claims, ideally signature-verified. Weakest (self-asserted unless signed), but the only key available for fully out-of-band BYO agents.

Instances that match nothing get registered as **unlinked instances** (`version_ref = null`) — visible to governance as shadow inventory rather than invisible. That single nullable field is what turns the GitOps objection into a feature (Section 3.3).

## 3. Register-on-deploy, end-to-end

### 3.1 The flow

The recommendation, matching the sibling catalog research's governance evidence ("Deploy always registers, reconcile the rest", 2026-07-16) and the ODH ADR #142 direction:

```
        PLATFORM PATH (register on deploy)                     OUT-OF-BAND PATH (reconcile)
┌──────────────┐  1. browse/deploy  ┌────────────────┐
│ Agent Catalog │──────────────────▶│ dashboard BFF   │        GitOps / oc apply / other
│ (kubeflow/hub)│                   │ + binding       │                  │
└──────────────┘                    └───┬────────┬────┘                  │
                                        │        │ 2. Go SDK            │
                        3. register     │        ▼                      ▼
                        version+instance│   ┌───────────┐        ┌───────────────┐
                        (sync, gated on │   │ OpenShell │ creates│  Sandbox CR   │
                        approval track) │   │  gateway  │───┐    │ (no registry  │
                                        │   └───────────┘   │    │  annotations) │
                                        ▼                   ▼    └───────┬───────┘
                              ┌──────────────────┐   ┌─────────────┐     │
                              │  MLflow Agent    │   │ Sandbox CR  │     │
                              │  Registry        │   │ + registry  │     │
                              │                  │   │ annotations │     │
                              │  RegisteredAgent │   └──────┬──────┘     │
                              │  └ AgentVersion ─┼┐         │ pod        │
                              │     └ Agent      ││         ▼            │
                              │      (instance) ─┼┼──┐ ┌───────────┐     │
                              └──▲────────▲──────┘│  │ │ agent pod │     │
                                 │        │       │  │ │ :8000     │     │
                     5. webhook  │        │ 6. enrich│ │ /.well-   │     │
                        push     │        │ card fetch│ known/     │     │
                                 │        │ + verify │ agent-card  │     │
                            ┌────┴────────┴────┐ (mTLS, RHAISTRAT-1956)  │
                            │  registry sync   │◀── 4. watch Sandbox CRs │
                            │  controller      │◀────────────────────────┘
                            │ (ADR #142 pattern│    adopt unannotated CRs
                            │  generalized)    │    → unlinked instance
                            └────────┬─────────┘
                                     │ read surfaces
              ┌──────────────────────┴──────────────────────┐
              ▼                                             ▼
   Registry view (RHAISTRAT-1697)              Deployments view (RHAISTRAT-1758)
   all registered agents — MLflow              running instances — Sandbox CRs
                                               via agent-ops BFF :8843
```

Steps: (1) user deploys from the catalog detail page; (2) BFF resolves binding and calls the OpenShell Go SDK, **stamping registry annotations on the Sandbox CR**; (3) the BFF registers synchronously — creating/confirming the AgentVersion and creating the Agent instance record with `version_ref` set; (4) the sync controller watches Sandbox CRs cluster-wide, catching both paths — for annotated CRs it confirms/heals the instance record; for unannotated CRs (GitOps) it creates unlinked instances; (5) CR state changes push to the MLflow webhook (`WEBHOOK` capability); (6) an enrichment loop fetches and verifies agent cards over mutually-authenticated channels, filling skills/protocol/`verified`.

Division of labor, upstream vs downstream: **upstream MLflow** keeps the generic `AgentDiscoveryProvider` (POLL/WATCH/WEBHOOK) and the webhook endpoint — nothing Sandbox- or OpenShell-specific (doc 03 §3.2's vendor-neutrality argument survives intact; only the reference plugin changes from AgentCard CRDs to Sandbox CRs). **Downstream ODH** ships the sync controller, following the MCP precedent, so one mechanism family serves both asset types.

### 3.2 Where ODH ADR #142 actually stands

Checked 2026-07-16: [opendatahub-io/architecture-decision-records PR #142](https://github.com/opendatahub-io/architecture-decision-records/pull/142) is **ODH-ADR-ML-0003 — "MCP Deployments Automatic Sync to MCP Registry"** (author dkuc, opened 2026-06-26, **still an open PR**, one approval, active review on security and failure handling). It decides: "Introduce a Kubernetes controller that watches `MCPServer` custom resources (managed by the MCP Lifecycle Operator) and automatically synchronizes their state into the MLflow MCP Server Registry", living in the model-registry-operator repo, extracting `status.serverInfo` and `status.address.url`, writing to MLflow over REST with projected ServiceAccount tokens, cleaning up via finalizers.

Two consequences for agents:

- **The pattern is decided-in-principle, MCP-scoped in fact.** The agent equivalent (watch `Sandbox` CRs, sync to the agent registry) is an extension nobody has written down as an ADR yet. It should be, before the EA2 backend lands.
- **The agent version is harder than the MCP version.** `MCPServer.status.serverInfo` gives the MCP controller real metadata to sync; the Sandbox CR has *no* equivalent (Section 1.1). The agent sync controller either syncs infrastructure-only records (thin but honest) or takes on the card fetch (fatter controller, kagenti-redux). Recommended split: controller syncs existence/liveness/annotations only; card enrichment stays a registry-side loop under RHAISTRAT-1956 — keeps the controller dumb and the trust logic (signature verification, mTLS) in one place.

One more Jira-shaped input: RHAISTRAT-1955 (agent lifecycle management — a single CR to register an agent, paraphrased) suggests a declarative registration CR. That is *compatible* with this architecture, not competing: a registration CR is a fourth discovery source (GitOps users register by committing the CR; the same sync controller reconciles it), and it answers Andrew Ballantyne's objection on its own terms — GitOps flows get a GitOps-native registration path instead of a policed front door.

### 3.3 The GitOps objection, resolved by asymmetry

Ballantyne's point — flows through the registry can't be forced, `oc apply` can't be policed — is correct and the architecture concedes it. The resolution is asymmetric guarantees: the **platform path guarantees** registration (deploy always registers, synchronously, with full metadata); the **out-of-band path guarantees only detection** (reconciled within a watch interval, as an unlinked instance with thin metadata). Governance sees a complete inventory; only platform-path records are *rich*. EU-AI-Act-flavored accountability requirements (per the sibling requirements research) are met by the inventory being complete, not by every record being born through the front door.

## 4. Governance mapping: four tracks × four runtime states

### 4.1 The two machines don't map — and shouldn't

The MCP Registry's four independent governance tracks ([fact-mcp-registry-data-model-proposal](/features/mcp-registry/knowledge/fact-mcp-registry-data-model-proposal.md)) apply to the **AgentVersion**; Varsha's runtime states apply to the **Agent instance**:

| Governance (AgentVersion) | Runtime (Agent instance) |
|---|---|
| Lifecycle: Draft → Candidate → Published → Deprecated → Retired | ACTIVE |
| Approval: Draft → Pending → Approved → Rejected → Revoked | UNHEALTHY |
| Verification: Unverified → Verified | STALE |
| Certification: None → Candidate → Certified → Expired → Revoked | REMOVED |

There is **no clean state-to-state mapping, and that is the design**, not a defect (doc 06 §3.2's independence argument survives and strengthens). Governance answers "should this exist?"; runtime answers "does it, and is it well?". A Deprecated version legitimately has ACTIVE instances; an UNHEALTHY instance of a Certified version stays Certified.

What connects them is **join points**, not mappings:

1. **Deploy gate** (governance → runtime): the platform deploy path refuses versions that aren't `lifecycle=Published ∧ approval=Approved` (the MCP invariant, reused verbatim). This is enforcement at the only point the platform controls — the front door — consistent with 3.3.
2. **Impact surfacing** (governance → runtime): Deprecate/Revoke a version ⇒ registry flags its ACTIVE instances; a signal, never a kill switch.
3. **Retire safety** (runtime → governance): a version with zero non-REMOVED instances is safely retirable — the runtime side finally gives the governance side real evidence for the Retired transition, something the MCP registry (with its `is_deployed` boolean only) cannot do.
4. **Terminology hazard**: the governance **Verification track** (a curation judgment on the record) and the runtime **`verified` field** (a cryptographic property of a fetched card, per instance) are different facts that share a word. Rename one in the schema (`verification_status` vs `card_attested`) before the EA2 backend freezes names.

### 4.2 What doesn't map at all

- **STALE** has no governance analog — it's a discovery-plumbing state (source stopped reporting), invisible to the four tracks by design.
- **Certification** has no runtime signal — it's organizational, though base-image attestation (Section 5) can become *evidence* feeding it.
- **`operatingMode: Suspended`** (Sandbox v1beta1) has no home in Varsha's four states: a suspended agent is not ACTIVE, not UNHEALTHY (deliberate), not STALE (still reported). The upstream proposal needs a fifth state (SUSPENDED/PAUSED) or a sub-state — a concrete, new upstream-RFC edit driven by the sandbox convergence.

### 4.3 Sequencing against real releases

| Release | Governance side | Runtime side | Gap to watch |
|---|---|---|---|
| 3.5 (now) | MCP Registry DP (four tracks debut) | dashboard agents table lists Sandbox CRs, read-only | none — deliberately disconnected |
| 3.6 EA1 | MCP Registry DP→TP; **Agent Catalog TP + Agent Registry TP** | deploy path (BFF → Go SDK) | **registry TP lands before its own backend** — if the EA1 registry view is fed from Sandbox CRs as a stopgap, it becomes a second deployments view and the 1697/1758 distinction collapses on arrival. The EA1 registry view should be fed from deploy-time registrations (even file/ConfigMap-backed) or explicitly labeled a preview of the deployments view. |
| 3.6 EA2 | **Agent Registry backend (MLflow)** | sync controller + enrichment loop realistic here | ADR-for-agents (the #142 extension) must be merged before this or the controller ships without a decision record |
| 3.6 GA | four tracks + workspace RBAC on agents | full flow of Section 3.1 | verification producer (RHAISTRAT-1956) is the long pole for any `verified=true` GA claim |

**Workspace RBAC**: the MLflow component already enforces workspace-scoped RBAC (platform baseline), so AgentVersion records inherit workspace scoping for free. Discovered instances arrive namespace-scoped, not workspace-scoped — the namespace↔workspace mapping for reconciled instances is an unowned design point (the MCP controller sidesteps it because MCPLO deployments are platform-initiated; unannotated GitOps Sandboxes are not).

## 5. Base images in the registry architecture

RHAIRFE-2443 (paraphrased) proposes shared agentic base images: UBI-minimal base layer + per-harness layer, built in Konflux with signed SBOMs, multi-arch, automated CVE patching ([fact-agentic-base-images](/features/agent-registry/knowledge/fact-agentic-base-images.md)). Konflux's attestation machinery is concrete: **SLSA provenance produced by Tekton Chains** under the **in-toto attestation framework**, signed and attached with **cosign** (`cosign download attestation $IMAGE` retrieves it), carrying full PipelineRun build metadata ([Konflux attestations](https://konflux-ci.dev/docs/metadata/attestations/)).

Where this plugs into registry records:

1. **AgentVersion stores the image by digest**, never by tag, with the attestation references alongside. Registration-time verification (cosign verify against Red Hat's key/identity) is a cheap, automatable check — and the natural *evidence input* to the Certification track (4.2): "Certified" for a Red-Hat-built agent can mean, mechanically, "provenance verified back to a Konflux pipeline".
2. **The provenance chain layers**: base image (RHAIRFE-2443, AIPCC-built) → harness image (supported-images program, catalog side) → AgentVersion (registry record referencing the harness digest + declared config) → instance (Sandbox CR whose `podTemplate` image digest is observable). The registry is the only component positioned to answer the cross-layer query that motivates the whole chain: **"a CVE landed in the UBI base — which running agents are affected?"** — walk digest → versions → non-REMOVED instances. Neither the catalog (no runtime knowledge) nor the cluster (no version knowledge) can answer it.
3. **CVE rebuilds create a versioning question**: automated patching produces new digests for the "same" harness. If AgentVersion pins a digest, every rebuild forces a version bump (governance churn); if it pins a tag, the CVE query above breaks. Recommended: version identity = (harness image *line* + declared config), with the digest recorded per-instance at deploy/discovery time — instances carry the digest they actually run, versions carry the line. This keeps governance stable across patch rebuilds while preserving the audit query.
4. **Relationship to registered versions**: base images are *not* registry entities themselves — they are supply-chain metadata *on* AgentVersions (a `base_image` field derivable from the harness image's provenance). Registering base images as first-class assets would duplicate what Konflux/Quay already govern. Metadata-first, again.

## 6. Synthesis: the recommended reference architecture in one paragraph

Enumerate from **Sandbox CRs** (WATCH — the only universal, runtime-agnostic signal on the cluster); seed rich records from **deploy-time registration** (WEBHOOK — the platform path stamps registry annotations on the CR it creates and registers synchronously, gated on the approval track); reconcile everything else into **unlinked instances** via an ADR-#142-style **sync controller** (the MCP precedent generalized, kept metadata-dumb); enrich and establish trust through a registry-side **card fetch + JWS verification loop** over mutually-authenticated channels (RHAISTRAT-1956 — the reincarnation of the only kagenti capability with no other successor); keep **two entities** (AgentVersion under four governance tracks; Agent instance under runtime states + a new SUSPENDED) joined by `version_ref` with image-digest+config-hash as the fallback join key; and hold **OpenShell gateway state** in reserve as a future health/policy enrichment source once the Go SDK series completes — never as the discovery backbone.

## Supersedes / corrections to the existing series

**Doc 03 — [03-kagenti-and-kubernetes](03-kagenti-and-kubernetes.md) (2026-04-24) — architecture spine superseded in full:**

- §1–2 *"kagenti is the primary integration partner"; kagenti "planned for inclusion in RHOAI in H2 2026"* → **False as of 2026-07-10**: kagenti removed from the roadmap, org winding down; the runtime bet is OpenShell + kubernetes-sigs agent-sandbox. Sections stand as historical reference only.
- §2.2–2.3 AgentCard CRD as discovery source of truth (auto-fetch of cards, `status.agentCardJSON`, JWS verification, label-based discovery) → **No replacement exists**; this doc's §1.6 is the gap inventory. Discovery source of truth is now the `Sandbox` CR (`agents.x-k8s.io/v1beta1`) — which carries no agent metadata.
- §2.4 SPIFFE/SPIRE via kagenti sidecars → superseded by the three-layer identity model (SPIFFE + AuthBridge/Keycloak + lifecycle) per the interop series; the registry's trust fields keep their shape but their producer is unbuilt (RHAISTRAT-1956).
- §3 Option A/B/C integration architectures against AgentCard CRDs, and the MLflowReconciler push → superseded by §3.1 of this doc: watch Sandbox CRs + deploy-time webhook + ADR-#142-pattern sync controller. Varsha's abstract interface (`AgentDiscoveryProvider`, POLL/WATCH/WEBHOOK, entry points) **survives unchanged** — only the reference plugin's substrate changes.
- §5 *"Agent-sandbox is a runtime concern that the registry does not directly integrate with"* → **Inverted.** Sandbox CRs are now the registry's primary Kubernetes discovery source. Also stale: "version 0.4.2, ~1,900 stars" (April) → v1beta1 API, v0.5.1 (2026-07-09).
- §4 kagent as secondary discovery source → deprioritized, not disproven; a kagent plugin remains possible under the same interface but is nobody's plan of record.
- §6 Kubernetes-native patterns (label-based discovery §6.1) → partially superseded: the label convention lost its owner with kagenti; §6.2–6.5 (CRD-as-metadata, operator reconciliation, K8s-as-one-source, plugin-per-platform) **reaffirmed** and load-bearing in this doc.

**Doc 06 — [06-rhoai-context](06-rhoai-context.md) (2026-04-24) — corrections:**

- §6.5 "Kagenti Operator… deployment primitive for agents on K8s; RHOAI 3.5 Tech Preview" → superseded: the deployment primitive is OpenShell (SDK-driven, 3.6) atop Sandbox CRs; no kagenti TP.
- §4.2 "MCP and Agent registry co-priority for 3.5" → overtaken by events: agent registry is 3.6 (TP EA1, backend EA2); MCP Registry carried 3.5 (DP).
- §7.1 dual-entity open question → answered in recommendation form by §2 of this doc (separate entities, hard reference, unlinked-instance state, LoggedModel as version hub).
- §7.3 kagenti integration depth → **moot**; replaced by the OpenShell/sandbox integration questions in this doc (§1.2, §4.3).
- §3.2's dual-state-machine framing → reaffirmed and extended (join points, SUSPENDED gap, verification-name collision).

**Strategy doc — [upstream-proposal](/features/agent-registry/strategy/upstream-proposal.md) (Varsha, 2026-02-16):** remains the upstream anchor, but its "Reference Plugin: Kubernetes with kagenti" section describes a dead substrate; the upstream RFC's reference implementation must be rewritten against Sandbox CRs + card fetch, and the state model needs a SUSPENDED addition (§4.2). The core interface, entity, and capability model survive.

## Sources

1. [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox) — v1beta1, v0.5.1 (2026-07-09); fetched 2026-07-16
2. [Agent Sandbox API reference](https://agent-sandbox.sigs.k8s.io/docs/api/) — Sandbox/SandboxTemplate/SandboxClaim/SandboxWarmPool v1beta1 fields; fetched 2026-07-16
3. [opendatahub-io/architecture-decision-records PR #142](https://github.com/opendatahub-io/architecture-decision-records/pull/142) — ODH-ADR-ML-0003, MCPServer→MLflow sync controller (dkuc, 2026-06-26, open); fetched 2026-07-16
4. [NVIDIA/OpenShell PR #2271](https://github.com/NVIDIA/OpenShell/pull/2271) — Go SDK PR A of six (rhuss, 2026-07-14, open; sandbox client only); fetched 2026-07-16
5. [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell) — gateway state model, experimental Kubernetes support; fetched 2026-07-16
6. [A2A protocol specification v1.0](https://a2a-protocol.org/latest/specification/) — AgentCard, §8 discovery, §8.4 card signing/verification; fetched 2026-07-16
7. [AWS Agent Registry preview](https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/) — 2026-04-09; fetched 2026-07-16
8. [MLflow: Version Tracking for Agents and LLMs](https://mlflow.org/docs/latest/genai/version-tracking/) — LoggedModel, `create_external_model`, `set_active_model`
9. [MLflow: LoggedModel data model](https://mlflow.org/docs/latest/genai/data-model/logged-model)
10. [MLflow Model Registry](https://mlflow.org/docs/latest/ml/model-registry/) — version↔LoggedModel lineage
11. [Databricks: version tracking concepts](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/version-concepts) — version-centric agent model
12. [Konflux attestations](https://konflux-ci.dev/docs/metadata/attestations/) — SLSA provenance via Tekton Chains, in-toto, cosign; fetched 2026-07-16
13. [architecture-context rhoai-3.5-ea.2 mlflow.md](https://github.com/opendatahub-io/architecture-context/blob/main/architecture/rhoai-3.5-ea.2/mlflow.md) — MLflow component ground truth (2026-06-22 snapshot); fetched 2026-07-16
14. [kubeflow/hub](https://github.com/kubeflow/hub) — catalog backend (via sibling doc, verified 2026-07-16)
15. [kagenti/kagenti-operator](https://github.com/kagenti/kagenti-operator) — historical reference for the gap inventory (per doc 03)
16. Local hub: [upstream-proposal](/features/agent-registry/strategy/upstream-proposal.md) · [fact-kagenti-roadmap-removal](/features/agent-registry/knowledge/fact-kagenti-roadmap-removal.md) · [fact-agentic-base-images](/features/agent-registry/knowledge/fact-agentic-base-images.md) · [fact-mcp-registry-data-model-proposal](/features/mcp-registry/knowledge/fact-mcp-registry-data-model-proposal.md) · [fact-agent-deployment-modes](/features/agent-catalog/knowledge/fact-agent-deployment-modes.md) · [question-agent-catalog-register-vs-deploy](/features/agent-catalog/knowledge/question-agent-catalog-register-vs-deploy.md) · [agent-catalog/research/03-architecture](/features/agent-catalog/research/03-architecture.md) · [agent-interop/research/00-executive-summary](/features/agent-interop/research/00-executive-summary.md) · [fact-openshell-architecture](/features/agent-interop/knowledge/fact-openshell-architecture.md)

Jira (keys, paraphrased): RHAISTRAT-1355, -1697, -1758, -1955, -1956, -2019; RHAIRFE-2443, -2309, -2310.
