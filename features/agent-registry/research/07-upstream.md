---
title: "Agent Registry research — upstream refresh"
description: July 2026 state of everything the registry builds on — MLflow's RFC-0008 stream, Unity Catalog agents, A2A 1.0 + the new ARD federation spec, agent-sandbox v1beta1/OpenShell discovery surfaces, and the agentic-ci base-image upstream — with corrections to the April series.
timestamp: 2026-07-16
lens: upstream
review_after: 2026-10-16
---

# Agent Registry research — upstream refresh (July 2026)

The April series was written into a world where no one had proposed a registry
upstream, kagenti was the Kubernetes discovery partner, and Databricks had no
agent asset type. All three of those premises have moved. The upstream picture
as of 2026-07-16: **MLflow now has a formal RFC pipeline and the first registry
RFC (skills, not agents) is a Red Hat-authored draft**; **Databricks made
agents a governable Unity Catalog asset in June**; **A2A shipped 1.0.1 and the
discovery-standard race produced ARD**, a Google/Microsoft federation spec that
wraps AgentCards and MCP server cards; and **the Kubernetes discovery substrate
is now Sandbox CRs + the OpenShell gateway**, with kagenti off the RHOAI path
(though publicly the upstream project is rebranding, not dying). Detail per
area below; corrections to the existing series at the end.

## 1. MLflow: the registry conversation moved into a formal RFC stream

### RFC-0008 — what it actually is

The "MLflow RFC-0008" the fresh agent-catalog research flagged is **not an
agent registry**. [mlflow/rfcs PR #26 — "RFC-0008: MVP Skill Registry (Phase
1)"](https://github.com/mlflow/rfcs/pull/26) is a **draft opened 2026-07-14 by
jwm4 (Bill Murdock)**, proposing a governed, **metadata-first** registry for
AI agent **skills and skill bundles**: versioning, **lifecycle stages**,
aliases, typed source pointers (Git repos, OCI registries, ZIP archives, MLflow
artifacts) instead of storing artifacts directly, installation delegated to
package-manager plugins, and `mlflow.skill_context()` tracing integration. As
of 2026-07-16 it has **no assigned reviewers and no review activity** — last
commit 2026-07-14. Subagents, hooks, and MCP-server cross-references are
**explicitly deferred to a Phase 2 RFC** that extends bundles toward
agent-shaped entities (scope narrowed from a broader proposal, PR #10, per
discussion with Databricks maintainers — see the sibling
[agent-catalog upstream doc](/features/agent-catalog/research/02-upstream.md),
which covers the RFC-0004 MCP Registry precedent and the phase-split).

The feeder issue is load-bearing for our positioning: [mlflow/mlflow
#22833 — "[FR] Add skill registry primitives for governed skill metadata and
versioning"](https://github.com/mlflow/mlflow/issues/22833) was opened
**2026-04-23 by jwm4 and is assigned to him**, with motivation naming
lifecycle management (draft/published/deprecated/retired), security-scan
tracking, **federated discovery**, and skill grouping — enterprise framing
that references RHOAI needs. The upstream registry stream is now being
**authored from our side of the fence**, not merely lobbied for: the April
playbook ("get Corey Zumar to invite a design") has effectively been executed,
one entity type earlier than we planned.

Two design deltas from what the April series predicted matter for the future
agent phase:

- **Metadata-first, not artifact-storing.** RFC-0008 stores metadata + typed
  source pointers; the B-Step62 MVP stored SKILL.md artifacts in the artifact
  store. This matches the RHOAI "metadata-first, plugin-based" strategy
  exactly — the strategy and the upstream draft are now the same shape.
- **Lifecycle stages upstream.** The April analysis (05 §6.4) held that
  lifecycle states were strictly downstream territory. RFC-0008 puts lifecycle
  stages in the upstream core. If that survives review, the downstream
  governance delta for RHOAI shrinks — and the same concession is likely
  available to a future agent entity.

### Varsha's proposal is dormant and kagenti-coupled

The [spike/gateway branch](https://github.com/varshaprasad96/mlflow/commits/spike/gateway)
has had **no commits since 2026-04-23**, and that final commit is titled
*"Integrate kagenti AgentCard into agent registry proposal"* — i.e., the last
motion on the post-deployment Agent entity draft **deepened its dependency on
the component RHOAI has since dropped**. The core design (Agent entity,
`mlflow.agent_discovery` entry points with POLL/WATCH/WEBHOOK,
ACTIVE/UNHEALTHY/STALE/REMOVED lifecycle) remains sound and
plugin-agnostic by construction, but the reference plugin narrative
(kagenti AgentCard CRs as source of truth, MLflowReconciler push) must be
re-baselined onto agent-sandbox `Sandbox` CRs and/or the OpenShell gateway
before any upstream submission. Given RFC-0008's Phase 2 will approach agents
from the pre-deployment side (bundles → agent-shaped entities), the natural
upstream play is to land the post-deployment discovery design as the
**runtime-discovery companion to Phase 2**, not as a standalone RFC racing it.

### MLflow 3.12–3.14: agent investment went to observability and gateway governance, not registry

Three releases since the April series, none touching a registry namespace
([release index](https://mlflow.org/releases/)):

- [MLflow 3.12.0](https://mlflow.org/releases/3.12.0/) (2026-05-05): tracing
  attachments for multimodal spans; **coding-agent tracing extended beyond
  Claude Code to Codex, Gemini, and Qwen**; gateway guardrails.
- [MLflow 3.13.0](https://mlflow.org/releases/3.13.0/) (2026-05-29): **full
  RBAC with admin UI**, trace archival, **one-click coding-agent onboarding to
  the AI Gateway** (Claude Code / Codex / Gemini CLI — tracing, budgets,
  guardrails), Hermes Agent support, **official Helm chart** for Kubernetes.
- [MLflow 3.14.0](https://mlflow.org/releases/) (2026-06-17): **`mlflow agent
  setup`** one-command onboarding that delegates instrumentation to the coding
  agent itself; durable (write-ahead-log) Claude Code tracing; trace review
  queues; `@mlflow.test` pytest integration.

The `mlflow.agents` namespace is **unchanged** — still invoke-only, no
`register_agent()`/`search_agents()`, no `agents:/` URI scheme, no AgentCard
support. The pattern across 3.12–3.14 is clear: MLflow is treating agents
(especially coding-agent harnesses) as **things to observe and govern at the
gateway**, not yet things to register. That leaves the registry primitive gap
exactly where the April analysis put it — but the entity-registry track now
runs through the mlflow/rfcs queue, at skills-first sequencing.

One infrastructure change directly benefits any future registry:
**multi-workspace support** shipped in
[MLflow 3.10.0](https://mlflow.org/releases/3.10.0/) (Matt Prahl a lead
contributor), and mprahl released a **Kubernetes-backed WorkspaceProvider and
K8s authorization plugin** (2026-04-08) — see
[Workspaces docs](https://mlflow.org/docs/latest/self-hosting/workspaces/).
Workspaces + RBAC (3.13) + Helm chart mean the self-hosted MLflow that RHOAI
embeds now has a real tenancy/permission substrate for a registry to scope
against.

### Databricks: the "they build it first" risk landed — in Unity Catalog

At Data + AI Summit 2026 (June), Databricks announced that through **Unity AI
Gateway** organizations can *"register and govern Databricks-hosted and
external models, MCP services, agents, and skills alongside your data"* with
unified access control, lineage, and auditing —
[What's new with Unity Catalog, DAIS 2026](https://www.databricks.com/blog/whats-new-unity-catalog-data-ai-summit-2026);
[Agent Bricks at DAIS 2026](https://www.databricks.com/blog/agent-bricks-dais-2026)
positions Agent Bricks as the full agent platform on top. The April claim
that "Unity Catalog does not have a dedicated Agent asset type" is now false.
Two readings for us: (a) Databricks has validated agent-as-registered-asset at
the governance layer, which normalizes the concept an OSS MLflow agent entity
would formalize; (b) their incentive to accept an OSS agent registry RFC may
*rise* (OSS primitive → UC governance mapping, the exact Model Registry
pattern) — but the differentiated governance now ships in their proprietary
layer first. The emphasis in public material is runtime governance
(gateway/telemetry) rather than registration mechanics; no OSS-side agent
entity accompanied the announcement.

## 2. A2A 1.0, ARD, and the discovery-standard race

### A2A: 1.0.1 current; extensions are now the registry-relevant surface

[a2aproject/A2A](https://github.com/a2aproject/A2A) is at **v1.0.1
(2026-05-28)**. The registry-schema payload of 1.0 is unchanged from the April
analysis (JWS-signed cards with RFC 8785 canonicalization,
`/.well-known/agent-card.json`, multi-tenancy, `supportedInterfaces`
bindings), with two post-April notes:

- **Dual-version advertising**: AgentCards can declare v0.3 and v1.0 support
  simultaneously for backward compatibility
  ([What's new in v1](https://github.com/a2aproject/A2A/blob/main/docs/whats-new-v1.md)) —
  a registry schema should store protocol version per interface, not per agent.
- **Official extensions**: the `extensions` field now has four published
  official extensions — **Secure Passport, Timestamp, Traceability, and Agent
  Gateway Protocol** ([spec](https://a2a-protocol.org/latest/specification/)).
  Traceability and Agent Gateway Protocol in particular are metadata a
  registry should capture and filter on (observability contract, gateway
  routing capability).

### A2A's own registry effort is stuck; that vacuum is being filled elsewhere

[A2A Discussion #741 — "Agent Registry - Proposal"](https://github.com/a2aproject/A2A/discussions/741)
(opened June 2025 by a maintainer, active through **2026-05-22**) proposes a
centralized catalog + OAuth2 entitlements model, but the thread has settled
into an unresolved architectural split: **catalog federation** (central,
sync-based, staleness-prone) versus **peer federation** (sovereign registries,
mTLS/SPIFFE), with W3C DCAT/JSON-LD and **xRegistry** floated as neutral
foundations and the latest activity on verifiable credentials and compliance
attestations. No spec output yet. Practical read: A2A defines the *card*, not
the *registry* — the registry/federation layer is being standardized outside
the A2A project.

### ARD — the new federated discovery spec to track

On **2026-06-17**, Google and Microsoft (with Cisco, Databricks, GitHub,
GoDaddy, Hugging Face, NVIDIA, Salesforce, ServiceNow, Snowflake) announced
the **Agentic Resource Discovery (ARD) specification**
([Google announcement](https://developers.googleblog.com/announcing-the-agentic-resource-discovery-specification/),
[Microsoft](https://commandline.microsoft.com/agentic-resource-discovery-specification-ard/),
[spec](https://agenticresourcediscovery.org/spec/) — v0.9 Draft, dated
2026-05-28, Apache-2.0). Mechanics that matter for our registry:

- **Publication**: a machine-readable catalog at
  `/.well-known/ai-catalog.json` under the publisher's own domain; discovery
  also via robots.txt `agentmap` directives, HTML link tags, and DNS SVCB
  records.
- **Envelope, not schema**: media-type-driven — it *wraps*
  `application/a2a-agent-card+json` and `application/mcp-server-card+json`
  (plus `ai-catalog+json` bundles and `ai-registry+json` search endpoints)
  rather than defining a competing agent description. Artifact schemas stay
  with their protocols.
- **Identity**: domain-anchored URNs (`urn:air:<publisher>:<namespace>:<name>`)
  with the domain as trust anchor; optional `trustManifest` carrying SPIFFE
  IDs / DIDs for zero-trust cross-checks; metadata for domain verification,
  signature algorithms, and revocation URLs.
- **Federation**: registry-to-registry over plain HTTP with three modes —
  `auto` (upstream fan-out), `referrals` (return registry pointers), `none`.
- **Adoption**: early use in GitHub Copilot's Agent Finder; otherwise low so
  far ([launch coverage](https://content.fans/news/microsoft-google-launch-ai-agent-discovery-specification-github-ships-agent-finder),
  [Snowflake](https://www.snowflake.com/en/blog/agentic-resource-discovery-specification/),
  [Hugging Face](https://huggingface.co/blog/agentic-resource-discovery-launch)).

**Is ARD becoming the federated discovery standard?** Too early to call — v0.9
"Proposal" status, four weeks old, thin adoption. But it is the only candidate
with Google *and* Microsoft plus the major registry operators (GitHub, Hugging
Face) and Databricks/NVIDIA behind it, and it answers exactly the federation
question A2A #741 deadlocked on and that issue #22833 lists as a skill-registry
motivation. Cheap hedges for us: keep registry identifiers mappable to
domain-anchored URNs, store cards in their native media types, and treat
"expose an `ai-catalog.json` / `ai-registry` search endpoint" as a candidate
registry feature rather than inventing a bespoke federation API.

### MCP-side registry standardization

The [official MCP Registry](https://registry.modelcontextprotocol.io/)
([modelcontextprotocol/registry](https://github.com/modelcontextprotocol/registry))
remains **preview** as of July 2026 — launched 2025-09-08, API frozen at v0.1
since October 2025, GA "later" with possible breaking changes/data resets
still on the table ([about page](https://modelcontextprotocol.io/registry/about)).
Its explicit design center is **subregistry consumption** — Anthropic, GitHub,
PulseMCP, Docker Hub, Microsoft-type downstream registries that add curation,
ratings, security scanning, and *enterprise internal registries* over the
shared metadata layer. That is the same upstream-primitive/downstream-
governance split our MLflow strategy assumes, now normalized in the
neighboring registry. The **registry-as-MCP-server** pattern also has an
MLflow-specific existence proof:
[B-Step62/mcp-server-mlflow](https://github.com/B-Step62/mcp-server-mlflow)
exposes the MLflow Prompt Registry to agents as an MCP server — the obvious
low-cost discovery surface to replicate for a future agent/skills registry.
Note ARD's `mcp-server-card+json` media type makes MCP registry entries
federable through the same ARD layer as agents — one federation story for both
registries.

## 3. Kubernetes: the discovery substrate after kagenti

### agent-sandbox went v1beta1 — what a discovery plugin can read

[kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox)
**v0.5.0 (June 2026) graduated the core and extension APIs
(`agents.x-k8s.io`, `extensions.agents.x-k8s.io`) from v1alpha1 to v1beta1**;
v0.5.1 (July 2026) is current
([releases](https://github.com/kubernetes-sigs/agent-sandbox/releases);
[Kubernetes blog intro, 2026-03-20](https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/)).
Registry-relevant surface of the v1beta1 `Sandbox` CRD:

| CRD surface | Registry mapping |
|---|---|
| `spec.operatingMode` (`Running`/`Suspended`, replaces `spec.replicas`) | ACTIVE vs suspended lifecycle input |
| `spec.service` bool (auto-provisioned headless Service) | stable DNS endpoint → `url` field |
| `status.podIPs` (now exposed end-to-end) | direct endpoint fallback |
| `status.labelselector`, pod labels/annotations | `metadata` map, source filters |
| Conditions: `Suspended`, `Finished` (`PodSucceeded`/`PodFailed`) | UNHEALTHY/REMOVED transitions |
| Pod template (image, resources) | image provenance cross-ref to catalog entry |

The critical *limitation*: the Sandbox CRD is **workload-shaped, not
agent-shaped**. It tells a discovery plugin *where and whether* something runs
— it carries no AgentCard, no skills, no protocol declaration (upstream kind
is `Sandbox`; there is no `AgentSandbox` kind — see sibling verification). The
"what is this agent" half must come from the catalog entry that deployed it or
from fetching `/.well-known/agent-card.json` off the service endpoint. This is
precisely the gap kagenti's AgentCard CRD used to fill, and nothing on the
OpenShell path currently replaces it — the strongest single argument for the
registry owning that join. RHOAI 3.5's dashboard listing of Sandbox CRs is a
discovery *prototype* of exactly this plugin.

### OpenShell: what the gateway exposes

[NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell)'s **gateway is the
control plane** — it owns API access, state, policy and settings delivery,
provider/inference configuration, and relay coordination, and every compute
driver (local, Docker, Kubernetes-via-agent-sandbox) exposes the same gateway
API ([How OpenShell works](https://docs.nvidia.com/openshell/about/how-it-works),
[Manage gateways](https://docs.nvidia.com/openshell/sandboxes/manage-gateways)).
A registry discovery provider pointed at a gateway could enumerate:

- **Sandboxes** — CRUD + status monitoring (the agent-process inventory);
- **Sessions/relays** — authenticated CLI-to-sandbox connections over mTLS;
- **Providers** — model/credential bindings, with auto-discovery of
  recognized agents (Claude, Codex, OpenCode, Copilot) from the environment;
- **Policies** — per-sandbox static sections (`filesystem_policy`, `landlock`,
  `process`, locked at creation) plus hot-reloadable `network_policies`
  ([policy docs](https://docs.nvidia.com/openshell/sandboxes/policies)) —
  governance metadata no Kubernetes-level view has.

That makes the gateway a *richer* discovery source than raw Sandbox CRs
(policy + provider context), at the cost of depending on an alpha (v0.0.x,
"single-player mode") API. The **Go SDK the 3.6 deploy path builds on is
still pre-merge**: [PR #2271](https://github.com/NVIDIA/OpenShell/pull/2271)
(Part A of six: foundation, types, sandbox client) remained open in review as
of 2026-07-16, and an earlier three-part draft series (#2225–#2227) was closed
in favor of the six-PR decomposition — none merged. Depth on the SDK series
and the rhuss prototype: sibling
[agent-catalog upstream §3](/features/agent-catalog/research/02-upstream.md).

### kagent and the Solo.io "agentregistry" — a registry competitor surfaces in CNCF

[kagent](https://kagent.dev/) (CNCF Sandbox since 2025-05-22,
[CNCF page](https://www.cncf.io/projects/kagent/)) defines **agents as
Kubernetes CRDs** with native MCP/A2A/OpenAI-compatible endpoints and
OTel/Prometheus observability — its CRDs are themselves a declarative agent
inventory a discovery plugin could list, and it remains the most mature
K8s-native agent runtime in CNCF.

More directly registry-adjacent:
[cncf/sandbox#477](https://github.com/cncf/sandbox/issues/477) is a **pending
CNCF Sandbox application (filed 2026-03-25 by Solo.io, review scheduled
2026-09-22) for "agentregistry"**
([agentregistry-dev/agentregistry](https://github.com/agentregistry-dev/agentregistry)
— Go, Apache-2.0, first commit 2025-10-29, v0.3.2, ~29 contributors): "a
cloud-native registry for discovering, curating, and deploying **MCP servers,
agents, and skills**" with governance, K8s-native deployment, and kagent
integration. That is a near-exact scope overlap with the RHOAI registry+catalog
pair, arriving through CNCF rather than MLflow/Kubeflow. Young project, but if
accepted in September it becomes the CNCF-blessed noun for this space — worth
a standing watch and a deliberate positioning statement (our differentiators:
MLflow lineage/eval/tracing integration and the Kubeflow catalog join).

### kagenti: what is publicly true

Publicly, the [kagenti org](https://github.com/kagenti) is **not archived and
shows no wind-down notice** as of 2026-07-16: kagenti/kagenti released v0.6.1
(2026-06-25), weekly org reports continue, copyright headers moved from IBM
Corp. to Kagenti, and the project site states **"Kagenti is becoming Rosso"**
— a rebrand, with several org repos (adk, agentic-control-plane,
plugins-adapter) archived along the way
([org](https://github.com/kagenti), [project page](https://kagenti.github.io/.github/);
sibling doc's verification pass concurs). The accurate statement for our docs:
**kagenti is off the RHOAI roadmap and out of the registry's discovery
architecture; upstream, the project continues under a new name**. Claims that
the org is being wound down should not be made publicly — what's observable is
roadmap removal on our side plus rebranding and partial repo archival
upstream. Its durable ideas (AgentCard-as-CR, SPIFFE/Keycloak identity, the
Kuadrant-hosted MCP gateway) remain unreplaced on the OpenShell path.

## 4. Base-image upstreams

### opendatahub-io/agentic-ci — the public tip of the agent-image work

[opendatahub-io/agentic-ci](https://github.com/opendatahub-io/agentic-ci) is
real and active (Apache-2.0, Python, ~454 commits, **53 releases**, 5 open
PRs): a pip-installable harness for **running AI coding agents in sandboxed CI
environments** with streaming output and telemetry. Registry/base-image
relevant specifics:

- **Harnesses**: Claude Code and OpenCode runners.
- **Isolation backends**: local, Podman (default), and **OpenShell** (network
  policies, Landlock filesystem control, endpoint restrictions) — the same
  substrate stack as the product runtime direction.
- **Images**: pre-built runner/sandbox/CI images published to
  **`quay.io/aipcc/agentic-ci/`**, rebuilt daily, dependency-managed via
  Renovate. The AIPCC quay namespace publishing coding-agent runner images is
  the clearest *public* signal that the shared agent-base-image work
  (RHAIRFE-2443; the AIPCC base-image ADR) has a build pipeline behind it.
  The ADR's open questions (UBI version, product ID) are internal — tracked
  by key only here.

### Adjacent public signal: the Emerging Tech bootc track

Red Hat's Emerging Technologies blog published
["Building a hardened, image-based foundation for AI agents"](https://www.redhat.com/en/blog/building-hardened-image-based-foundation-ai-agents)
(2026-04-28, Sally O'Malley): **fedora-bootc** immutable host images for agent
fleets — read-only root, rootless Podman, Quadlet-managed services, secrets
injected post-boot — demonstrated with OpenClaw, with OpenShell recommended
for production sandboxing. This is a *host-image* track distinct from the
AIPCC *container-base-image* (UBI/Konflux) track; the two are complementary
(bootc host runs the UBI-based agent containers) but their coexistence is
exactly why the UBI-version/product-ID questions in the ADR need settling —
there are now two public-ish Red Hat shapes for "the thing an agent runs on."

### Harness packaging norms (provenance angle only)

None of the major harness vendors publish supported OCI base images: Claude
Code is proprietary, distributed via npm + native installer; Codex CLI is an
Apache-2.0 Rust binary; OpenCode ships near-daily via install script/npm;
Goose ships channel installers under AAIF governance; OpenClaw and pi
self-update by design (full table and licensing depth: sibling
[agent-catalog upstream §6](/features/agent-catalog/research/02-upstream.md)
— not repeated here). Provenance consequence for the base-image effort: there
is **no upstream image to inherit** — pinning, SBOM, signature, and rebuild
cadence all land on the Konflux/AIPCC pipeline, and every harness's
self-update mechanism must be disabled or redirected in the image build. The
ecosystem norm is converging on *govern the harness at a gateway* (MLflow
3.13/3.14 one-click coding-agent onboarding; Unity AI Gateway coding-agent
governance) rather than *bless the harness binary* — the base-image + registry
pair is how RHOAI does both.

## Supersedes / corrections to the existing series

1. **05-mlflow-upstream.md §5.1 / §8.1** — *"No agent registry proposals
   exist upstream; the namespace is unoccupied; the window is open."* →
   Superseded. The registry conversation now runs through
   [mlflow/rfcs](https://github.com/mlflow/rfcs): RFC-0008 (skills, Phase 1)
   is a Red Hat-authored draft (PR #26, 2026-07-14; feeder issue #22833,
   jwm4, 2026-04-23), with agent-shaped entities deferred to Phase 2. The play
   is no longer "claim the empty namespace," it is "author/shape Phase 2 and
   attach the post-deployment discovery design to it."
2. **05-mlflow-upstream.md §3.3** — *Skills Registry = B-Step62 MVP,
   artifact-storing, dedicated tables, "what Databricks will accept."* →
   Superseded as design-of-record: RFC-0008 is **metadata-first with typed
   source pointers** and package-manager-plugin installation; the MVP's
   contribution survives as the dedicated-entity-table precedent.
3. **05-mlflow-upstream.md §6.4** — *"Lifecycle states are not included
   upstream — Draft/Published/Deprecated/Archived are RHOAI extensions."* →
   Partially superseded: RFC-0008 proposes **lifecycle stages in the upstream
   core** (draft/published/deprecated/retired framing in #22833). If accepted,
   the downstream governance delta shrinks and the same is negotiable for a
   future agent entity.
4. **05-mlflow-upstream.md §4.3** — *"Unity Catalog does not have a dedicated
   'Agent' asset type."* → Superseded at DAIS 2026 (June): agents, skills,
   and MCP services are registrable/governable in Unity Catalog via Unity AI
   Gateway. The §8.2 risk "Databricks builds it first" materialized — in the
   proprietary layer, with no OSS entity attached.
5. **05-mlflow-upstream.md §2.6** — *mlflow.agents is thin (invoke-only).* →
   Still true through 3.14.0 (2026-06-17), and worth restating: three releases
   of agent investment went to coding-agent observability and gateway
   governance, zero to registry APIs.
6. **05-mlflow-upstream.md §6.2/§6.5 and strategy/upstream-proposal.md** —
   *kagenti as the reference Kubernetes discovery provider; "MLflow plugin
   reads reconciled AgentCard CRs."* → Stale. Varsha's branch is dormant
   (last commit 2026-04-23, and it *added* kagenti AgentCard integration);
   the reference-plugin story must be re-baselined on agent-sandbox v1beta1
   `Sandbox` CRs and/or the OpenShell gateway API before submission.
7. **03-kagenti-and-kubernetes.md (whole document)** — kagenti as the
   registry's Kubernetes discovery layer → superseded by the OpenShell +
   agent-sandbox direction. Also correct the framing of kagenti's status:
   publicly the upstream org is active and rebranding to "Rosso" (v0.6.1,
   2026-06-25), not archived — removal is an RHOAI-roadmap fact, not an
   upstream-death fact. The unreplaced remainder (AgentCard-as-CR,
   SPIFFE/Keycloak identity) is now a registry requirement, not a kagenti
   feature.
8. **02-standards-and-protocols.md §2.6** — *"A2A reached v1.0 early 2026."*
   → Current release is **v1.0.1 (2026-05-28)**; add the four official
   extensions (Secure Passport, Timestamp, Traceability, Agent Gateway
   Protocol) and dual v0.3/v1.0 card advertising to the registry schema
   considerations.
9. **02-standards-and-protocols.md §6 (implicit)** — *no federated discovery
   standard existed; registry federation unaddressed.* → **ARD v0.9**
   (Google/Microsoft + 9, announced 2026-06-17) now covers publication
   (`/.well-known/ai-catalog.json`), domain-anchored URNs, and
   registry-to-registry federation, wrapping A2A cards and MCP server cards.
   A2A's own registry effort (Discussion #741) remains deadlocked on
   central-vs-peer federation.
10. **04-agent-management-landscape.md** — add three entrants since April:
    Unity Catalog agent governance (Databricks, June), Solo.io's
    **agentregistry** CNCF Sandbox application (#477, review 2026-09-22), and
    the ARD coalition. The competitive frame is no longer only hyperscaler
    agent platforms — it now includes CNCF-native registries and a federation
    spec.
