---
title: "Agent Interop Research: Executive Summary"
description: Living synthesis across competitive, upstream, architecture, requirements, landscape, jira-gap, deployment, and operations lenses for agent interoperability on Red Hat AI.
timestamp: 2026-07-11
updated: 2026-08-03
review_after: 2026-09-11
---

# Agent Interop Research: Executive Summary

This is the living synthesis for the agent-interop research series. It
summarizes findings across six strategic lenses conducted 2026-07-11
and two practical lenses (deployment, operations) added 2026-07-27,
covering agent sandboxing (OpenShell/NVIDIA), identity (SPIFFE/SPIRE),
A2A communication, agent cards, BYO agent onboarding, discovery,
declarative harness configuration, deployment patterns, and day-2
operations.

## Series index

| Doc | Lens | Sources | Date |
|-----|------|---------|------|
| [01-competitive](01-competitive.md) | competitive | 36 | 2026-07-11 |
| [02-upstream](02-upstream.md) | upstream | 55 | 2026-07-11 |
| [03-architecture](03-architecture.md) | architecture | 24 | 2026-07-11 |
| [04-requirements](04-requirements.md) | requirements | ~30 | 2026-07-11 |
| [05-landscape](05-landscape.md) | landscape | 45 | 2026-07-11 |
| [06-jira-gap](06-jira-gap.md) | jira-gap | internal cross-ref | 2026-07-11 |
| [07-deployment](07-deployment.md) | deployment | 30+ | 2026-07-27 |
| [08-operations](08-operations.md) | operations | 40+ | 2026-07-27 |
| [09-competitive](09-competitive.md) | competitive (refresh) | 15+ | 2026-08-03 |

## Key findings

### Strategic position

OpenShell is architecturally differentiated through its hybrid
multi-layer sandboxing (Landlock + seccomp + netns + OPA) combined with
a supervisor-based model. No competitor offers equivalent kernel-level
isolation with hot-reloadable policy for AI agents. The competitive
gap is in **ecosystem and protocols** -- MCP has 78% enterprise adoption
(97M monthly SDK downloads, 10k+ servers) while A2A has 150+ supporting
organizations and production use at Google, Microsoft, AWS, Salesforce.
RHOAI has neither protocol natively today.

### Market timing risk

RHOAI trails on market timing. Azure AI Foundry Agent Service went GA
May 2025, AWS Bedrock Agents GA March 2025, Google rebranded to Gemini
Enterprise April 2026. OpenShell Dev Preview ships Aug 20, 2026; TP
targets Sep-Nov 2026; GA early 2027. The gap means RHOAI must
differentiate on **security, compliance, and hybrid cloud** rather than
time-to-market.

### Competitive landscape has shifted (09-competitive, 2026-08-03)

Three developments since the original competitive lens change the
strategic picture:

1. **Tigera Lynx shipped fleet governance at GA (Jun 17)** -- eBPF
   discovery, Cedar policy, SPIFFE identity, AI-CSPM with compliance
   packs, production bank deployments. Lynx owns the fleet governance
   narrative that OpenShell lacks. The strategy repo's "partner vs.
   competitor" conditional resolved: Lynx shipped first.

2. **KARS hit v1.0 (Jul 1)** -- end-to-end encrypted inter-agent mesh
   (Signal Protocol), per-pod Rust router, 8 framework integrations,
   GitOps-native governance, A2A live, AGT integration. More capable
   than the hub's prior assessment ("starting point"). OpenShell's
   remaining advantage is per-binary depth (process-level vs. pod-level
   enforcement).

3. **OpenAI Agents SDK ships 7 official sandbox providers (Apr 2026)**
   -- Blaxel, Cloudflare, Daytona, E2B, Modal, Runloop, Vercel.
   OpenShell is not among them. Ecosystem visibility gap for the largest
   agent developer audience.

Additionally, checkpoint/restore is now table stakes across the category
(E2B, Daytona, Cloudflare, Vercel, Runloop, Microsandbox, CodeSandbox
all ship it). OpenShell's CAP 972 work is urgent. Daytona went
closed-source (Jun 2026), reducing OSS competitive pressure but
validating commercial value ($1M ARR in <3 months).

OpenShell's core differentiators remain unique and validated: per-binary
policy, L7 TLS MITM, denial intelligence, and the three-layer coverage
(isolation + behavioral + credentials). No competitor has matched this
depth. The 88% security incident rate (BeyondScale 2026) validates the
security-first positioning.

See [09-competitive](09-competitive.md) for the full refresh including
updated threat ranking, net-new competitors, and recommended actions.

### Industry definitions have converged (landscape lens)

The landscape lens establishes that industry definitions for the seven
agent-interop capability areas have largely stabilized by mid-2026:

- **Agent interoperability** is now crisply defined as the capability
  allowing diverse agents to discover, communicate, delegate, and
  operate as a cohesive system without custom integration -- distinct
  from point-to-point integration.
- **Sandboxing** has a clear three-tier baseline (microVM / user-space
  kernel / hardened container), with the VM boundary as the 2026
  consensus for untrusted code. Standard containers are explicitly
  insufficient.
- **Identity** has converged on SPIFFE as the workload identity
  substrate, with a two-layer model (SPIFFE + OAuth/JWT delegation) as
  the reference architecture. The intent layer above identity remains
  the open frontier.
- **A2A** reached v1.0 ratification and ACP has merged into it, leaving
  two complementary protocols (A2A horizontal + MCP vertical) rather
  than three competing ones.
- **Agent cards** have a well-defined specification and discovery
  mechanism (`/.well-known/agent-card.json`), plus the Agentic Resource
  Discovery (ARD) specification from Microsoft for federated catalogs.
- **BYO agent onboarding** is recognized as a distinct enterprise
  capability with converging best practices around self-service
  onboarding with governance guardrails.
- **Declarative configuration** has CRD consensus (Agent Sandbox SIG +
  kagent patterns), with the remaining debate on abstraction level
  (Kubernetes-first vs. platform-agnostic).

### Governance frameworks have converged

Three governance frameworks (OWASP Agentic Top 10, Microsoft Agent
Governance Toolkit, NIST AI Agent Standards Initiative) now overlap on
largely the same control set. Microsoft's AGT is notable as the first
toolkit to address all 10 OWASP agentic risks with deterministic,
sub-millisecond policy enforcement. Design principle: "instead of
asking an agent to behave, make it incapable of misbehaving."

### FIPS path exists

The Rust FIPS blocker has a viable resolution path. AWS-LC holds FIPS
140-3 certificate #4816, and aws-lc-rs provides a ring-compatible Rust
wrapper. OpenShell issue #900 proposes switching from ring to aws-lc-rs.
The SSH layer remains a gap (no FIPS-validated Rust SSH implementation
yet). FIPS 140-2 sunset on September 21, 2026 adds urgency -- in-process
CMVP status is not a valid compliance state.

### Identity architecture is the hardest unsolved problem

SPIFFE provides the right substrate (cryptographic, ephemeral, no static
secrets), but current implementations struggle with agent-specific
challenges: dynamic registration of ephemeral agents, per-instance
identity granularity, and the "intent layer" gap (SPIFFE answers "who"
but not "why"). The strongest documented architecture is the Red Hat
three-layer model (SPIFFE transport + AuthBridge/Keycloak application
layer + lifecycle management), published at next.redhat.com June 2026.
The IETF AIMS standard (March 2026) and NIST NCCoE concept paper
(February 2026) validate this direction.

### Multi-tenancy is the enterprise gate

88% of agent pilots never reach production, primarily due to
infrastructure gaps: isolation, governance, compliance, and data
residency. Multi-tenancy is the single largest unresolved architectural
question for both OpenShell and RHOAI. The recommended model is
namespace-level tenant boundaries + OpenShell per-agent sandboxing +
shared gateway with tenant-scoped policy + optional vCluster Private
Nodes for regulated workloads. The "unconditional rewrite" pattern
(proxy always substitutes correct tenant ID, never validates and
rejects) is architecturally stronger than conditional validation.

### Declarative config consensus

The 2026 Kubernetes ecosystem has converged: declarative CRD patterns
beat SDK-first for production agent management. Agent Sandbox SIG
provides the CRD standard (Sandbox/SandboxTemplate/SandboxClaim/
SandboxWarmPool). kagent (CNCF Sandbox) adds Agent/Session/Tool CRDs
with GitOps-native workflows. OpenShell should adopt a layered CRD
approach: agent-sandbox-compatible core CR that OpenShell's operator
reconciles, with OpenShell-specific policy and driver config in
associated ConfigMaps.

### Regulatory pressure accelerating

NIST launched the AI Agent Standards Initiative (February 2026). The
June 2, 2026 executive order mandates Binding Operational Directives for
civilian federal agencies. SP 800-53 control overlays for agent systems
are in development. The EU AI Act entered full enforcement early 2026.
The Colorado AI Act becomes enforceable June 2026, and EU AI Act
high-risk obligations start August 2026. Organizations in regulated
industries should plan for existing sector regulations to cover AI agent
deployments within 12-18 months.

### Jira coverage gaps are wider than expected (jira-gap lens)

The jira-gap lens cross-references the 209-issue Jira snapshot against
research findings from all five lenses. Of 31 research-identified
capabilities, only 14 have confirmed Jira tracking, 3 have partial
coverage, and **14 have no confirmed RHAISTRAT feature**.

The three most critical gaps -- **FIPS 140-3 compliance, privileged SCC
elimination, and multi-tenancy** -- have upstream OpenShell issues but
NO downstream RHAISTRAT ensuring Red Hat-specific requirements are met
(FIPS build pipeline, SCC testing, RHOAI namespace model). These are
the three capabilities that block enterprise deployment.

The identity stack is the widest gap: SPIFFE provisioning, token
exchange/AuthBridge, and intent-based authorization span four research
lenses but only authorization (RHAISTRAT-1730) has tracking. MCP at the
agent layer (distinct from MCP Gateway) is also untracked despite 78%
enterprise adoption.

The lens recommends 13 RFEs: 3 for immediate filing (FIPS, SCC,
multi-tenancy), 5 for next planning cycle (SPIFFE identity, AuthBridge,
MCP agent layer, CRD design, service binding), and 5 for roadmap
backlog. See [06-jira-gap](06-jira-gap.md) for the full coverage matrix
and RFE specifications.

### Deployment is achievable but fragile (deployment lens, 2026-07-27)

The deployment lens (07) maps OpenShell's three topologies to concrete
environments with prerequisites, Helm values, and operational profiles.
Nine findings extend strategic-lens knowledge:

- **Sidecar topology (B) is shipping.** The Helm chart exposes
  `supervisor.topology=sidecar` with strict/relaxed sub-modes. This was
  described as future in the architecture lens but is now a configurable
  Helm value.
- **User namespace support is implemented**
  (`server.enableUserNamespaces=true`). On K8s 1.33+ this maps container
  UID 0 to an unprivileged host UID, creating a concrete path to
  eliminating the privileged SCC -- not just a theoretical mitigation.
  OpenShift support is a work in progress.
- **Layered sandboxing validated on OpenShift 4.21.** Red Hat Developer
  article (Jul 2026) confirms OpenShell + Kata dual protection stops
  both application-layer and kernel-level attacks. Neither layer
  interferes with the other.
- **No official air-gap deployment path exists** (NemoClaw #2218).
  Practical approach (image/chart/manifest mirroring + internal model
  endpoints) works but is undocumented.
- **Gateway API GRPCRoute is the ingress standard**, not K8s Ingress
  resources or OpenShift Routes. Envoy Gateway OIDC must NOT be
  enabled alongside OpenShell OIDC (browser-redirect vs bearer-token
  conflict).
- **FIPS Phase 1 design specified** (OpenShell #900): feature-flagged
  aws-lc-rs backend, algorithm restrictions, SSH validation gap deferred
  to Phase 2. Build toolchain impact: CMake + Go required.
- **RHOAI integration path**: DP = Helm only, TP = operator for lifecycle,
  GA = DSC integration. Separate OLM operator is viable (parallels
  cert-manager/Serverless prerequisite pattern).

### Day-2 operations are immature (operations lens, 2026-07-27)

The operations lens (08) surveys the entire day-2 surface. The gateway
is functional for evaluation but has significant gaps for production:

- **No HA / leader election** (GitHub #1012 open). The gateway is a
  single point of failure. Multi-replica with external Postgres works
  but has no documented HA pattern.
- **No automated sandbox garbage collection.** Orphaned sandboxes must
  be cleaned up manually. No TTL-based cleanup or per-tenant quotas.
- **Gateway log buffer is in-memory only** -- lost on restart. OCSF
  v1.7.0 structured logging with SIEM export is well-designed but the
  persistence gap is an operational surprise.
- **Warm pool feasibility study completed** (#2199) but not yet
  integrated. Six+ upstream issues track the implementation. Cold start
  benchmarks not published.
- **No Vault/KMS integration** for provider credentials. Rotation is
  manual (`provider update`) or automated for OAuth2/Google/AWS STS
  only.
- **No compliance policy templates.** OPA policy authoring, hot-reload,
  and Policy Advisor (RFC 0002) are well-documented, but no SOC2/HIPAA/
  FedRAMP template library exists.
- **OTEL not auto-wired** (#1758, #1818 open). Prometheus metrics
  endpoint exists but instrumentation is minimal (#909 open).

The operational gaps summary (08 section 11) identifies 12 gaps, 3
critical (HA, multi-tenancy, FIPS) and 4 high (Vault integration,
garbage collection, compliance templates, Grafana dashboards).

## Open question status updates

| Question | Research finding | New status |
|----------|-----------------|------------|
| Rust FIPS path | aws-lc-rs provides FIPS 140-3 path; OpenShell #900 proposes it; SSH gap remains. Phase 1 design specified with feature flag. | partial-answer |
| Privileged SCC | Three concrete paths: Topology B (gVisor/Kata), user namespaces (K8s 1.33+, `enableUserNamespaces=true`), sidecar relaxed mode. OpenShell #899 tracks restricted SCC specifically. Layered sandboxing (OpenShell+Kata) validated on OCP 4.21. | open (multiple mitigation paths confirmed) |
| Multi-tenancy | Three models (silo/pool/bridge); namespace + per-agent sandbox + shared gateway recommended; no implementation yet. Helm chart namespace split (#2485) is prerequisite. Interim: separate gateways per tenant. | open |
| Declarative config | CRD consensus clear (Agent Sandbox + kagent patterns); layered approach recommended | open (direction clarified) |
| SKU decision | No new external data; separate OLM operator (paralleling cert-manager) is viable alternative to DSC component. Internal decision. | open |

## White space opportunities

1. **SPIFFE-native agent identity**: No competitor offers SPIFFE-as-a-service for agent SVIDs
2. **Hybrid cloud agent mesh**: No competitor offers true on-prem-to-cloud agent-to-agent communication
3. **Policy-as-code for agents**: Git-versioned OPA policies with compliance templates (SOC2, HIPAA, FedRAMP)
4. **Regulated industry focus**: Banking at 47% production deployment; compliance-first agent templates
5. **Universal BYO onboarding**: Agent onboarding across MCP, A2A, and all major frameworks with automated security scanning
6. **Intent-based authorization**: the "why" layer above SPIFFE identity has no standard -- first mover advantage
7. **Shadow agent discovery**: ~~enterprise shadow agent inventory tooling is a recognized gap with no mature solution~~ **Partially closed**: Tigera Lynx ships eBPF-powered shadow agent discovery and quarantine at GA (Jun 2026). OpenShell would need to match or partner.
8. **OpenAI SDK provider integration**: OpenShell as an official sandbox provider for the OpenAI Agents SDK -- architecturally compatible, high visibility, moderate effort

## Recommended follow-ups

- ~~**jira-gap lens**~~: DONE (2026-07-11) -- see
  [06-jira-gap](06-jira-gap.md). Found 14 capability gaps, 13 RFEs
  recommended, 3 critical (FIPS, SCC, multi-tenancy).
- **File Tier 1 RFEs**: FIPS 140-3 compliance, restricted SCC
  compatibility, and multi-tenancy model need RHAISTRAT features
  immediately -- all three are deployment blockers with no downstream
  tracking.
- **Ref- sweep for unmapped RHAISTRAT issues**: 81 of 96 RHAISTRAT
  issues lack ref- entries. Priority: the 28 issues created Jun-Jul
  2026 (RHAISTRAT-1993 through RHAISTRAT-2220) may cover some gaps.
- **Deeper competitive on IBM**: watsonx Orchestrate "agentic control plane"
  positioning warrants dedicated analysis (ACP merged into A2A changes
  the dynamic)
- **Agent mesh architecture deep dive**: Solo.io agent mesh pattern +
  Envoy AI Gateway v1.0 composition
- **FIPS implementation tracking**: Monitor OpenShell #900 progress and
  aws-lc-rs CMVP status quarterly
- **Microsoft AGT integration assessment**: evaluate AGT execution rings
  model as reference for OpenShell governance layer
- **ARD specification tracking**: Microsoft's Agentic Resource Discovery
  may become the federated discovery standard
- ~~**deployment lens**~~: DONE (2026-07-27) -- see
  [07-deployment](07-deployment.md). 9 new findings: sidecar topology
  shipping, user namespace SCC path, layered sandboxing validated, no
  air-gap path, GRPCRoute ingress standard.
- ~~**operations lens**~~: DONE (2026-07-27) -- see
  [08-operations](08-operations.md). 12 operational gaps identified,
  3 critical. HA gap (#1012) and lack of garbage collection are net-new
  findings not in the prior series.
- **HA architecture for gateway**: upstream engagement needed (OpenShell
  #1012) -- single point of failure is a GA blocker
- **Air-gap deployment guide**: no official path exists -- downstream
  engineering needed for RHOAI disconnected installs
- **Warm pool integration tracking**: feasibility study complete
  (#2199), implementation in progress across 6+ upstream issues
- ~~**competitive refresh**~~: DONE (2026-08-03) -- see
  [09-competitive](09-competitive.md). Key findings: Lynx GA (fleet
  governance gap), KARS v1.0 (elevated threat), OpenAI SDK ecosystem
  gap, checkpoint/restore now table stakes.
- **Fleet governance build-vs-partner decision**: Lynx owns the
  narrative; decide whether to build fleet governance into OpenShell
  or partner with Tigera. Strategy decision, not engineering.
- **OpenAI SDK provider integration**: propose OpenShell as an official
  sandbox provider for the OpenAI Agents SDK
- **CAP 972 checkpoint/restore**: urgent Red Hat input needed before
  upstream proposal merges without alignment
- **KARS field positioning update**: "starting point" no longer
  accurate; differentiate on per-binary depth and compliance
