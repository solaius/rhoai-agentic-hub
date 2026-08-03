---
title: Agent Interop — strategy
description: Production-readiness layer for agents on RHOAI — OpenShell-anchored sandboxing, identity, policy, and interop. DP Aug 20 (3.5), TP Sep-Nov (3.6), GA early 2027.
timestamp: 2026-08-03
status: current
review_after: 2026-10-03
source: hub.strategy refresh from 65+ knowledge entries, 9-doc research series (01-08 from 2026-07-11/27, 09-competitive from 2026-08-03), strategy repo intake (2026-08-03), Jira snapshot (2026-07-11), profiles/roadmap.md and profiles/strategy.md
---

## The brief

Agent Interop is the production-readiness layer for agents on Red Hat AI.
The bet: **OpenShell-anchored, defense-in-depth sandboxing is the gate
enterprises must pass before any agent reaches production** -- 88% of agent
pilots fail at this gate
([fact-openshell-vs-agent-substrate](/components/agent-interop/knowledge/fact-openshell-vs-agent-substrate.md)).
OpenShell remains the only system covering isolation + behavioral security +
credential management in a single runtime; per-binary policy is unique
([fact-openshell-competitive-landscape](/components/agent-interop/knowledge/fact-openshell-competitive-landscape.md)).

Where we are: Dev Preview shipping Aug 20 in RHOAI 3.5 (Helm-only, docs,
enablement). Upstream Beta gates Sep 15 -- two days before 3.6 EA1 GA
(Sep 17). **Competitive pressure has intensified:** Tigera Lynx shipped fleet
governance at GA (Jun 17); KARS hit v1.0 with encrypted mesh (Jul 1);
OpenShell is absent from the OpenAI Agents SDK ecosystem (7 official
providers, Apr 2026). Adel's 8 strategic rocks (R1-R8) provide the
upstream execution framework
([fact-openshell-strategic-rocks](/components/agent-interop/knowledge/fact-openshell-strategic-rocks.md)).

## What

| Release | Date | Scope | Status |
|---------|------|-------|--------|
| RHOAI 3.5 (DP) | Aug 20 | OpenShell Helm install + docs/enablement; pinned upstream version; enablement blog series; no downstream images, no operator, no SDK | Shipping |
| Upstream Beta | Sep 15 | Multi-tenancy, extensibility, HA on K8s, API stability; 12 upstream gates ([fact-openshell-tp-scope](/components/agent-interop/knowledge/fact-openshell-tp-scope.md)) | Dependency |
| RHOAI 3.6 EA1 (TP) | Sep 17 | UBI10 images via Konflux; operator; Go SDK; SPIFFE identity; governed execution environments (RHAIRFE-2984); OTEL tracing | Planned |
| RHOAI 3.6 EA2 | Oct 15 | Overflow from EA1; items blocked on upstream Beta landing | Planned |
| RHOAI 3.6 GA | Nov 19 | TP feature completion; weekly image builds stabilized | Planned |
| RHOAI 3.7 (GA) | Early 2027 | Full support; disconnected install, multi-arch, pluggable IdP, GitOps policy-as-code, harness gateway sandboxing | Directional |

**Critical timing:** upstream Beta (Sep 15) is 2 days before 3.6 EA1 GA
(Sep 17), with EA1 code freeze Aug 21. Items depending on Beta landing
slip to EA2 or GA if Beta slips.

**Boundaries -- what this is NOT:**

- Pre-deployment agent registry/catalog/discovery -> [agent-registry](/components/agent-registry/)
- Starter-kit templates and catalog UI -> [agent-catalog](/components/agent-catalog/)
- Agent observability/SDLC oversight -> [agent-ops](/components/agent-ops/)
- MCP-level tool traffic governance -> [mcp-gateway](/components/mcp-gateway/)
- AI-native proxy/gateway for all AI traffic -> [ai-gateway](/components/ai-gateway/)
- Deployment is a shared workstream consumed by both catalog and registry, owned by neither (owner, 2026-07-16)

## Why

**The problem.** Enterprise agents need to call tools, fetch data, and interact
with external systems -- each action is an unsanctioned network call from a
process running arbitrary LLM-generated code. Standard containers are
explicitly insufficient for this threat model
([00-executive-summary](/components/agent-interop/research/00-executive-summary.md)).

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
   Agents GA'd Mar 2025; Tigera Lynx shipped fleet governance Jun 2026;
   KARS v1.0 Jul 2026 -- the market is not waiting
3. **Customer**: 88% of agent pilots fail at security; 88% of orgs reported
   AI agent security incidents (BeyondScale 2026)

**Competitive position (updated Aug 2026).**
([09-competitive](/components/agent-interop/research/09-competitive.md))

OpenShell's core differentiators remain unique and validated: per-binary
policy (OPA/Rego + `/proc` + SHA-256 TOFU), L7 TLS MITM inspection,
denial intelligence, credential-free inference routing. No competitor
has matched this depth. However:

- **Lynx owns fleet governance.** Tigera shipped the discovery/auth/policy/
  audit layer OpenShell lacks -- eBPF auto-discovery, Cedar policy, AI-CSPM
  with compliance packs, production at global banks. NVIDIA's own launch
  says "requires an integrated ecosystem." If Red Hat doesn't build fleet
  governance, Lynx becomes the default pairing -- a third-party dependency.
- **KARS is no longer "the starting point."** v1.0 ships encrypted
  inter-agent mesh (Signal Protocol), per-pod Rust router, 8 framework
  integrations, GitOps governance, A2A live, AGT integration. MIT-licensed.
  OpenShell's remaining edge is per-binary depth (process vs. pod boundary).
- **OpenAI SDK ecosystem absence.** 7 official sandbox providers; OpenShell
  is not among them. Invisible to the largest agent developer audience.

## Where we stand

**Decisions to date:**
- 2026-07-28: Dev Preview scope locked -- architect sign-off narrows 3.5 DP
  to pinned upstream version, docs, blogs. Konflux/operator are TP.
- 2026-07-28: gVisor dropped -- weaker isolation than Kata, no Red Hat
  operator. QEMU confirmed as preferred hypervisor.
- 2026-07-28: Three sandboxing layers defined -- Layer 1 (OpenShift Sandbox
  Containers, GA), Layer 2 (Agent Sandbox, TP), Layer 3 (OpenShell, software).
- 2026-07-17: [Postgres as DP backend DB](/components/agent-interop/knowledge/decision-openshell-dp-postgres.md)
- 2026-07-17: [Base image dual path (Hummingbird + UBI/RHEL)](/components/agent-interop/knowledge/decision-openshell-base-image-dual-path.md)
- 2026-07-17: [GPU and confidential computing deferred past Oct/Nov](/components/agent-interop/knowledge/decision-openshell-defer-gpu-cc.md)
- 2026-07-11: Convergence onto OpenShell ([ref-email-openshell-convergence](/components/agent-interop/knowledge/ref-email-openshell-convergence.md))

**Delivery state:**
- Helm chart v0.0.90 deploys on vanilla K8s and OpenShift (experimental)
- Sidecar topology (Topology B) ships as a Helm value
- Layered sandboxing (OpenShell + Kata) validated on OpenShift 4.21
  ([ref-rh-developer-layered-sandboxing](/components/agent-interop/knowledge/ref-rh-developer-layered-sandboxing.md))
- Agent Sandbox SIG CRDs at v1beta1; API still changing fast
- UBI10 images (4 images, Gateway/Supervisor/Sandbox/CLI) via Konflux in progress (EPIC AIPCC-28137)
- Upstream progress on 4 at-risk items: credential storage drivers (#2454),
  warm pools (#2460), blackbox images (#2476), HA (#2489) all have open PRs

**In-flight:**
- NVIDIA co-engineering MVP scope-lock
- Konflux pipeline for downstream images (weekly cadence)
- Strategy repo
  ([ref-openshell-strategy-gitlab-repo](/components/agent-interop/knowledge/ref-openshell-strategy-gitlab-repo.md))
  as continual source for rocks, competitive positioning, and TP scope

## Gaps & risks

**Critical (deployment blockers):**

| Gap | Why it matters | Tracking |
|-----|---------------|----------|
| [Privileged SCC on OpenShift](/components/agent-interop/knowledge/question-openshell-privileged-scc.md) | Enterprise red flag; 3 mitigation paths (sidecar, user namespaces K8s 1.33+, layered Kata) but none production-validated on OCP | OpenShell #899, #1959; no RHAISTRAT |
| [No FIPS path](/components/agent-interop/knowledge/question-openshell-rust-fips.md) | Rustls + ring not FIPS-validated; FIPS 140-2 sunsets Sep 2026. Phase 1 design specified (aws-lc-rs), SSH gap remains | OpenShell #900; no RHAISTRAT |
| [Multi-tenancy not implemented](/components/agent-interop/knowledge/question-openshell-multi-tenancy.md) | No per-tenant scoping/quotas/isolation. Workspaces PR merging but full implementation targeting Beta | OpenShell #1722; no RHAISTRAT |
| [Gateway HA / leader election](/components/agent-interop/knowledge/question-openshell-gateway-ha.md) | Single point of failure; multi-replica works but no guarantees. Assignee (TaylorMutch) leaving -- handoff risk | OpenShell #1012, PR #2489; no RHAISTRAT |
| **Upstream Beta timing** | Beta Sep 15 is 2 days before EA1 GA Sep 17; code freeze Aug 21. Any Beta slip cascades to EA2/GA | 12 upstream gates ([fact-openshell-tp-scope](/components/agent-interop/knowledge/fact-openshell-tp-scope.md)) |

**High (competitive and enterprise readiness):**

| Gap | Why it matters |
|-----|---------------|
| **Fleet governance gap** | Lynx shipped fleet governance at GA (Jun 17) that OpenShell lacks -- eBPF discovery, Cedar policy, AI-CSPM, compliance packs. If RH doesn't build this, Lynx becomes a third-party dependency in the RHOAI stack ([09-competitive](/components/agent-interop/research/09-competitive.md)) |
| **OpenAI SDK ecosystem absence** | Not among 7 official sandbox providers. Invisible to the largest agent developer audience. Architecturally compatible but no integration exists |
| **Checkpoint/restore** | Table stakes across the category (E2B, Cloudflare, Vercel, Runloop, Microsandbox, CodeSandbox all ship it). OpenShell has nothing; CAP 972 needs urgent Red Hat input |
| [SKU / product home decision](/components/agent-interop/knowledge/question-openshell-sku-product-home.md) | RHOAI component vs separate operator vs OCP component -- affects cadence, ownership, entitlement |
| [SPIFFE identity provisioning](/components/agent-interop/research/06-jira-gap.md) (G4) | Authorization tracked (RHAISTRAT-1730) but identity provisioning (SVID issuance, dynamic registration) is not |
| [No Vault/KMS integration](/components/agent-interop/research/08-operations.md) | Credential rotation manual or OAuth2-only |
| [No official air-gap path](/components/agent-interop/research/07-deployment.md) | Practical approach works but undocumented |
| [Declarative config path](/components/agent-interop/knowledge/question-openshell-declarative-agent-config.md) | No CRD or K8s-native declarative path today |

**Tensions:**
- **Speed vs safety**: OpenShift experimental status vs customer demand for sandboxing now
- **Upstream vs downstream**: NVIDIA controls the Rust codebase, release cadence, and architecture decisions; Red Hat influence depends on contribution weight
- **Support boundary**: harness binaries are "validated, not supported" ([fact-harness-support-boundary](/components/agent-interop/knowledge/fact-harness-support-boundary.md)) -- customers may not understand the distinction
- **Fleet governance: build vs partner**: building fleet governance into OpenShell is slower but owned; partnering with Tigera (Lynx) is faster but creates a dependency. Strategy decision.

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
| Governed execution environments | RHAIRFE-2984 | New |

TP-scope RFEs ([fact-openshell-tp-scope](/components/agent-interop/knowledge/fact-openshell-tp-scope.md)):

| Deliverable | RFE | Needs STRAT |
|-------------|-----|-------------|
| UBI10 container images | RHAIRFE-2443 / RHAISTRAT-2067 | No |
| Build pipeline + telemetry removal | RHAIRFE-2679 | No |
| OpenShell operator | RHAIRFE-2572 / RHAISTRAT-1752 | No |
| Go SDK | RHAIRFE-2623 | **Yes** |
| Identity: SPIFFE token exchange | RHAIRFE-2567 | **Yes** |
| Identity: inbound caller auth | RHAIRFE-2568 | **Yes** |
| Identity: protocol-aware policy | RHAIRFE-2569 | **Yes** |
| OTEL tracing | RHAIRFE-794 | No |
| Declarative agent deployment | RHAIRFE-2310 / RHAISTRAT-2148 | No |
| Governed execution envs | RHAIRFE-2984 | **Yes** |
| Warm pools (cold start) | RHAIRFE-2678 | No |

Snapshot: 209 issues (96 RHAISTRAT, 113 RHOAIENG), swept 2026-07-11.
15 of 96 RHAISTRAT issues have ref- entries; 81 remain unmapped.

### Candidate jiras

**Tier 1 -- file immediately (critical gaps, no downstream tracking):**

1. **FIPS 140-3 compliance for OpenShell on RHOAI** -- Regulated customers
   cannot deploy without FIPS-validated crypto. Downstream build pipeline
   (aws-lc-rs), feature flag, SSH gap mitigation, CMVP tracking.
   -> RHAIRFE or RHAISTRAT

2. **Restricted SCC compatibility for OpenShell sandboxes** -- Privileged SCC
   is an enterprise deployment blocker on OpenShift. Topology B + user
   namespaces + Kata layered sandboxing qualification, SCC test suite.
   -> RHAIRFE or RHAISTRAT

3. **Multi-tenancy model for agent sandboxes** -- Production scale requires
   per-tenant namespace boundaries, quotas, gateway policy scoping, RBAC.
   -> RHAISTRAT

4. **Gateway HA for production deployments** -- Single point of failure.
   Leader election, active-passive/active-active, HPA. Assignee leaving
   compounds urgency.
   -> RHAIRFE or RHAISTRAT

**Tier 2 -- next planning cycle:**

5. **SPIFFE identity provisioning for agent workloads** -- Zero-trust
   foundation. SVID issuance, dynamic registration, Keycloak delegation.
   Distinct from RHAISTRAT-1730 (authorization).
   -> RHAISTRAT

6. **Service binding for LLM endpoints in agent sandboxes** -- Replace manual
   provider YAML with automatic injection. Developer experience gap.
   -> RHAIRFE

7. **Air-gap deployment guide for OpenShell** -- No official disconnected
   path. Image/chart mirroring, internal model endpoints.
   -> RHAIRFE

**Tier 3 -- competitive response (new from 09-competitive):**

8. **OpenAI Agents SDK sandbox provider integration** -- OpenShell not in the
   7 official providers. Architecturally compatible (harness/compute
   separation maps to supervisor/proxy). High visibility, moderate effort.
   -> RHAIRFE

9. **Checkpoint/restore for sandbox state** -- Table stakes across the
   category. Every major competitor ships snapshot/checkpoint. CAP 972
   is the upstream proposal; needs urgent Red Hat input before it merges
   without alignment.
   -> RHAIRFE (downstream) + upstream CAP 972 comment

10. **Fleet governance positioning decision** -- Lynx shipped fleet governance
    that OpenShell lacks. Build into OpenShell (slower, owned) vs partner
    with Tigera (faster, dependency). Not an RFE -- a strategy decision
    that gates whether RFEs follow.
    -> Decision doc, then RHAISTRAT if "build"

## Watchlist

| Date | Trigger | If it fires -> |
|------|---------|----------------|
| Aug 20 2026 | RHOAI 3.5 GA (DP ships) | DP scope locked; field feedback begins; enablement blog series goes live |
| Aug 21 2026 | 3.6 EA1 code freeze | Operator (RHAISTRAT-1752) must be ready; any TP scope not committed by this date slips to EA2 |
| Sep 15 2026 | OpenShell upstream Beta | Critical gate for TP. If it slips, dependent EA1 deliverables cascade to EA2/GA. Two-day margin to EA1 GA |
| Sep 21 2026 | FIPS 140-2 sunset | In-process CMVP is not valid compliance; aws-lc-rs migration becomes urgent blocker |
| Oct 3 2026 | GTC Berlin | NVIDIA OpenShell presentation; competitive visibility moment |
| Nov 19 2026 | RHOAI 3.6 GA | TP feature completion; weekly image builds stabilized |
| Ongoing | Tigera Lynx enterprise adoption | If Lynx becomes the default fleet governance layer for OpenShell, RH needs a position on that stack composition |
| Ongoing | KARS adoption trajectory | v1.0 with encrypted mesh + AGT integration. If enterprises adopt KARS for governance + Agent Sandbox for isolation, OpenShell's value narrows to "deeper inspection" |
| Ongoing | CAP 972 (suspend/resume) | Checkpoint/restore proposal; Red Hat input needed before it merges without alignment. Competing with CAP 970 |
| Ongoing | OASIS attestation standard | NVIDIA wants Red Hat compatible; if it publishes without alignment, identity model (R3b) may need rework |
| Ongoing | OpenAI Agents SDK provider ecosystem | An integration would give OpenShell visibility where agents are built |
| Ongoing | Agent Sandbox SIG v1beta1 -> v1 | CRD breaking changes could require OpenShell rework |
| Ongoing | NVIDIA OpenShell release cadence | Upstream velocity controls downstream; weekly image build acceleration in progress |

## History

- 2026-08-03 -- **Refresh** -- strategy repo intake (11-competitor landscape,
  8 rocks R1-R8, TP scope with 12 upstream beta gates + 11 downstream
  deliverables) + competitive research refresh (09-competitive: Lynx GA
  fleet governance gap, KARS v1.0 elevated threat, OpenAI SDK ecosystem
  absence, checkpoint/restore table stakes). Concrete dates throughout
  (Aug 20 DP, Sep 15 Beta, Sep 17 EA1, Oct 15 EA2, Nov 19 GA). 4 new
  gaps added (fleet governance, OpenAI SDK, checkpoint/restore, Beta
  timing). 3 new candidate jiras (Tier 3 competitive response). 5 new
  watchlist triggers. Sources: gitlab.cee.redhat.com/azaalouk/
  openshell-strategy (Jul 28), web search competitive sweep (Aug 3).
- 2026-07-30 -- **Creation** -- initial strategy doc from 60+ knowledge
  entries, 8-doc research series (lenses 01-06 from 2026-07-11, 07-08
  from 2026-07-27), 209-issue Jira snapshot (2026-07-11), roadmap and
  strategy profiles. Covers full scope: sandboxing, identity, A2A,
  declarative config, deployment, operations. Four critical gaps
  identified (SCC, FIPS, multi-tenancy, gateway HA); 7 candidate jiras
  drafted. OpenShell GDoc intake + deployment/operations research run
  same session.
