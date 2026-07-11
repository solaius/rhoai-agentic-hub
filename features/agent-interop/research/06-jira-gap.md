---
title: "Jira Gap Analysis: Research Findings vs. Active Work Items"
description: Cross-reference of agent-interop research findings (lenses 01-05) and knowledge entries against the 209-issue Jira snapshot to identify capability gaps with no tracking, open questions without Jira coverage, and RFE candidates.
timestamp: 2026-07-11
lens: jira-gap
review_after: 2026-09-11
---

# Jira Gap Analysis: Research Findings vs. Active Work Items

## Method

This analysis cross-references the capability areas identified across
five research lenses (competitive, upstream, architecture, requirements,
landscape) and the agent-interop knowledge base against the Jira
snapshot (209 issues swept 2026-07-11 via JQL covering RHOAIENG
component=AgentOps and RHAISTRAT/RHOAIENG labels agentic/agentic-theme).

Jira issue summaries are not available in the public snapshot (null for
disclosure reasons). Coverage determination relies on:
- 15 ref- entries in `features/agent-interop/knowledge/` that link
  specific RHAISTRAT keys to capability areas
- Explicit Jira key references within the research documents
- The capability gaps fact (`fact-openshell-capability-gaps.md`)
- The 5 open question files

The snapshot contains 96 RHAISTRAT issues (Features, Outcomes,
Initiatives) and 113 RHOAIENG issues (Epics, Stories, Tasks, Sub-tasks,
Vulnerabilities, Bugs). Of the 96 RHAISTRAT issues, 15 have ref-
entries providing capability mapping.

## 1. Research-identified capabilities: coverage matrix

### Capabilities with confirmed Jira coverage

These capabilities have tracked RHAISTRAT features with ref- entries
confirming their scope:

| Capability | Jira key(s) | Status | Research lens |
|-----------|-------------|--------|---------------|
| Agent sandboxing (OpenShell integration) | RHAISTRAT-1751, -1585 | Closed (decomposed to children) | competitive, upstream, architecture |
| A2A protocol support | RHAISTRAT-1356 | In Progress | competitive, upstream, landscape |
| BYO agent / runtime compatibility | RHAISTRAT-1349 | In Progress | competitive, requirements, landscape |
| Agent authorization / policy enforcement | RHAISTRAT-1730 | New | architecture, requirements |
| Agent safety enforcement (tool calls) | RHAISTRAT-1269 | New | requirements, landscape |
| Agent governance / registry | RHAISTRAT-1355 | In Progress | competitive, landscape |
| Agent Hub UI / discovery views | RHAISTRAT-1697 | In Progress | requirements |
| BYOA AgentOps journey | RHAISTRAT-1211 | In Progress | requirements, landscape |
| Agent lifecycle management | RHAISTRAT-1955 | New | upstream, architecture |
| Agent metadata extraction | RHAISTRAT-1956 | New | architecture |
| Agent deployments view | RHAISTRAT-1758 | In Progress | requirements |
| Agent runtime contract | RHAISTRAT-2019 | New | architecture |
| OpenShell operator (OLM) | RHAISTRAT-1752 | New | upstream, architecture |
| Kagenti/OpenShell coexistence | RHAISTRAT-1753 | Closed (spike, superseded) | architecture |

**Assessment**: 14 capability areas have confirmed Jira tracking. The
core agent platform work (sandboxing, BYO, A2A, registry, lifecycle,
authorization, safety) is represented.

### Capabilities with NO confirmed Jira coverage

These capabilities were identified as significant across multiple
research lenses but have no known RHAISTRAT feature tracking them. Some
may be covered by the 81 RHAISTRAT issues without ref- entries, but
this cannot be confirmed without summaries.

#### Critical gaps (P0 -- deployment blockers)

| # | Capability | Research evidence | Gap severity |
|---|-----------|------------------|-------------|
| G1 | **FIPS 140-3 compliance (Rust path)** | Requirements lens: aws-lc-rs path exists (OpenShell #900), FIPS 140-2 sunsets Sep 21 2026, SSH layer has no solution. No RHAISTRAT filed. Only upstream tracking. | CRITICAL -- regulated customer blocker, hard deadline |
| G2 | **Privileged SCC elimination** | Requirements lens: CAP_SYS_ADMIN is enterprise deployment blocker on OpenShift. Topology B mitigation path exists. No RHAISTRAT filed. Only upstream OpenShell #899, #1959. | CRITICAL -- OpenShift deployment blocker |
| G3 | **Multi-tenancy model** | Architecture + requirements lenses: namespace + per-agent sandbox + shared gateway recommended. No RHAISTRAT filed. Only upstream OpenShell #1722. | CRITICAL -- production scale blocker |

#### High gaps (P1 -- enterprise readiness)

| # | Capability | Research evidence | Gap severity |
|---|-----------|------------------|-------------|
| G4 | **SPIFFE/SPIRE identity integration** | All five lenses converge: SPIFFE is the identity substrate. RHAISTRAT-1730 covers authorization but NOT identity provisioning (SVID issuance, dynamic registration, rotation). The identity layer beneath authorization is untracked. | HIGH -- zero-trust foundation |
| G5 | **Token exchange / AuthBridge** | Architecture lens: Red Hat three-layer model documented (SPIFFE + AuthBridge/Keycloak + lifecycle). Capability gaps fact: "token exchange" listed as high-severity gap. No RHAISTRAT. | HIGH -- delegation chain requirement |
| G6 | **MCP protocol support (agent layer)** | Competitive lens: 78% enterprise MCP adoption, 97M monthly SDK downloads. RHOAI has no native MCP at the agent layer (MCP Gateway is separate feature area for tool traffic governance, not agent-to-tool protocol). | HIGH -- ecosystem gap |
| G7 | **Declarative CRD design** | Architecture + requirements + landscape lenses: CRD consensus clear (Agent Sandbox + kagent patterns). RHAISTRAT-2019 covers runtime contract, RHAISTRAT-1752 covers operator, but no feature for the CRD schema design itself. | HIGH -- platform engineer expectation |
| G8 | **Service binding (LLM endpoints)** | Capability gaps fact: medium-severity gap. Kagenti auto-injected LLM endpoints and MCP gateway URLs; OpenShell requires manual provider YAML. No RHAISTRAT. | HIGH -- developer experience |

#### Medium gaps (P2 -- competitive differentiation)

| # | Capability | Research evidence | Gap severity |
|---|-----------|------------------|-------------|
| G9 | **Agent mesh / hybrid cloud agent communication** | Architecture lens: white space opportunity #2. Solo.io agent mesh pattern documented. No competitor offers true on-prem-to-cloud agent communication. No RHAISTRAT. | MEDIUM -- differentiator |
| G10 | **MLflow/OTEL tracing integration** | Capability gaps fact: medium-severity gap. Kagenti auto-wired MLflow experiments + RBAC; OpenShell can set env vars but nothing built-in. No RHAISTRAT. | MEDIUM -- observability |
| G11 | **Non-sandboxed agent tracking** | Capability gaps fact: medium-severity gap. Kagenti's AgentRuntime CR attached to any pod; OpenShell requires every agent in a sandbox. No RHAISTRAT. | MEDIUM -- enterprise reality |
| G12 | **Shadow agent discovery** | Landscape lens: "highest-risk agents are the ones not in any inventory." 62% of organizations experimenting, 80% report risky behavior. No RHAISTRAT. | MEDIUM -- governance gap |
| G13 | **Intent-based authorization** | Landscape lens: "SPIFFE answers WHO but not WHY." First-mover opportunity, no standard exists. No RHAISTRAT. | MEDIUM -- future differentiator |
| G14 | **SOC2/HIPAA/FedRAMP compliance templates** | Requirements lens: "policy-as-code for agents" is white space #3. Git-versioned OPA policies with compliance templates. No RHAISTRAT. | MEDIUM -- regulated industries |
| G15 | **Agent cost optimization / FinOps** | Competitive lens: white space opportunity #4. Requirements lens: P2 for platform engineers. No RHAISTRAT. | MEDIUM -- enterprise scale |
| G16 | **Third-party security audit** | Competitive lens: "no third-party security audit or production references in regulated industries." No RHAISTRAT. | MEDIUM -- trust signal |
| G17 | **Warm pool integration (RHOAI)** | Upstream lens: Agent Sandbox SIG provides SandboxWarmPool CRD. No RHAISTRAT for RHOAI-side integration. | MEDIUM -- cold start elimination |

## 2. Open questions: Jira tracking status

| Open question | RHAISTRAT tracking | Upstream tracking | Assessment |
|--------------|-------------------|------------------|------------|
| Rust FIPS path | **NONE** | OpenShell #900 | GAP -- critical compliance deadline (Sep 2026). Needs RHAISTRAT for downstream build pipeline, FIPS feature flag, and SSH gap mitigation. |
| Privileged SCC | **NONE** | OpenShell #899, #1959 | GAP -- deployment blocker. Needs RHAISTRAT for Topology B qualification on OpenShift, SCC compatibility testing. |
| Multi-tenancy | **NONE** | OpenShell #1722 | GAP -- production gate. Needs RHAISTRAT for namespace model design, tenant-scoped gateway config, RBAC model. |
| Declarative config | **PARTIAL** -- RHAISTRAT-2019 (runtime contract), RHAISTRAT-1752 (operator) | OpenShell #1719 | PARTIAL -- CRD schema design and Agent Sandbox SIG compatibility not tracked. |
| SKU / product home | **NONE** | N/A | GAP -- internal decision. Needs RHAISTRAT or internal tracking for packaging decision (RHOAI umbrella vs separate operator vs Red Hat AI SKU). |

**Finding**: All five open questions have either no Jira tracking (3) or
only partial tracking (1) on the Red Hat side. Upstream OpenShell issues
exist for three of them but there is no downstream RHAISTRAT ensuring
Red Hat-specific requirements are addressed (FIPS build pipeline, SCC
testing, namespace model for RHOAI multi-user).

## 3. Enterprise requirements coverage

Cross-referencing the requirements lens (04-requirements.md)
persona-driven priority matrix against confirmed Jira coverage:

### Platform engineer requirements

| Requirement | Priority | Jira coverage | Gap? |
|------------|----------|--------------|------|
| Declarative agent deployment (CRD/GitOps) | P0 | Partial (RHAISTRAT-2019, -1752) | YES -- CRD schema gap |
| Multi-tenancy with namespace isolation | P0 | None | YES -- G3 |
| No privileged containers (restricted SCC) | P0 | None | YES -- G2 |
| Warm pools for cold-start elimination | P1 | None (upstream only) | YES -- G17 |
| Operator lifecycle (OLM/OperatorHub) | P1 | RHAISTRAT-1752 | No |
| Cost attribution per tenant/agent | P2 | None | YES -- G15 |

### ML/AI engineer requirements

| Requirement | Priority | Jira coverage | Gap? |
|------------|----------|--------------|------|
| BYO framework support | P0 | RHAISTRAT-1349 | No |
| Debugging in sandbox | P0 | OpenShell native | No |
| Service binding for LLM endpoints | P1 | None | YES -- G8 |
| MLflow/OTEL tracing integration | P1 | None | YES -- G10 |
| Starter kits / quickstart templates | P2 | RHAISTRAT-1697 | No |

### Security / compliance requirements

| Requirement | Priority | Jira coverage | Gap? |
|------------|----------|--------------|------|
| FIPS 140-3 validated crypto | P0 | None | YES -- G1 |
| Audit trail (full delegation chain) | P0 | Partial (RHAISTRAT-1730 authorization, not audit) | PARTIAL |
| Least-privilege (no static credentials) | P0 | OpenShell native | No |
| FedRAMP-ready deployment | P1 | None | YES -- G14 |
| SOC2/HIPAA compliance templates | P1 | None | YES -- G14 |
| Third-party security audit | P2 | None | YES -- G16 |

### Enterprise architect requirements

| Requirement | Priority | Jira coverage | Gap? |
|------------|----------|--------------|------|
| Keycloak/LDAP identity integration | P0 | None (architecture documented, no RHAISTRAT) | YES -- G5 |
| Hybrid cloud agent communication | P0 | None | YES -- G9 |
| A2A/MCP protocol support | P1 | RHAISTRAT-1356 (A2A only) | PARTIAL -- G6 (MCP gap) |
| Agent registry and discovery | P1 | RHAISTRAT-1355, -1697 | No |
| Agent cost optimization / FinOps | P2 | None | YES -- G15 |

**Summary**: Of 22 persona-driven requirements identified in the
requirements lens, 8 have confirmed Jira coverage, 3 have partial
coverage, and **11 have no confirmed Jira tracking**.

## 4. Competitive gap assessment

The competitive lens (01-competitive.md) identifies five areas where
"OpenShell/RHOAI is behind." Jira coverage for each:

| Competitive gap | Jira coverage | Assessment |
|----------------|--------------|------------|
| MCP ecosystem (78% enterprise adoption) | None at agent layer | GAP -- G6. MCP Gateway (separate feature) covers tool traffic but not agent-to-tool protocol integration in OpenShell |
| A2A protocol (150+ orgs) | RHAISTRAT-1356 | COVERED but early stage (In Progress) |
| Market timing (12-18 months behind) | N/A (not a feature) | Structural -- mitigate through differentiation |
| Security audit gaps | None | GAP -- G16 |
| Agent discovery mechanism | RHAISTRAT-1355, -1697 | COVERED |

The competitive lens identifies six white space opportunities. Jira
coverage:

| White space | Jira coverage | Assessment |
|------------|--------------|------------|
| SPIFFE-native agent identity | None | GAP -- G4 |
| Hybrid cloud agent mesh | None | GAP -- G9 |
| Policy-as-code for agent governance | Partial (RHAISTRAT-1730 covers authorization, not Git-versioned OPA templates) | PARTIAL |
| Agent cost optimization / FinOps | None | GAP -- G15 |
| Regulated industry focus (compliance templates) | None | GAP -- G14 |
| Universal BYO agent onboarding | RHAISTRAT-1349, -1211 | COVERED |

## 5. Upstream dependency tracking

Research lenses 02 (upstream) and 03 (architecture) identify critical
upstream dependencies. Several have no downstream tracking for
Red Hat-specific integration requirements:

| Upstream dependency | Upstream status | RHAISTRAT tracking | Gap |
|-------------------|----------------|-------------------|-----|
| Agent Sandbox SIG v1beta1 | Active, v1beta1 Jun 2026 | None | Need feature for RHOAI integration |
| kagent CNCF Sandbox | Active, GitOps-native | None | Evaluate for CRD adoption |
| Envoy AI Gateway v1.0 | GA Jun 2026 | None (MCP Gateway feature covers AI Gateway) | Covered in mcp-gateway feature |
| OpenShell FIPS (aws-lc-rs) | Proposed (#900) | None | GAP -- G1 |
| OpenShell privileged SCC | Open (#899) | None | GAP -- G2 |
| OpenShell multi-tenancy | Discussion (#1722) | None | GAP -- G3 |
| OpenShell Kubernetes operator | Discussion (#1719) | RHAISTRAT-1752 | COVERED |
| SPIFFE/SPIRE agent extensions | CNCF Graduated | None | GAP -- G4 |
| IETF AIMS agent identity | Published Mar 2026 | None | Track for compliance alignment |
| Microsoft ARD specification | Active (2026) | None | Monitor for discovery standard |

## 6. Recommended RFEs to close gaps

### Tier 1: file immediately (critical gaps, blocking deployment)

| # | RFE title | Covers gap | Rationale |
|---|----------|-----------|-----------|
| R1 | **FIPS 140-3 compliance for OpenShell on RHOAI** | G1 | Hard deadline Sep 21 2026. Scope: downstream FIPS build pipeline (aws-lc-rs), feature flag integration, SSH gap mitigation plan, CMVP timeline tracking. |
| R2 | **Restricted SCC compatibility for OpenShell sandboxes** | G2 | Enterprise deployment blocker. Scope: Topology B (gVisor/Kata boundary) qualification on OpenShift, SCC compatibility test suite, documentation of supported topologies. |
| R3 | **Multi-tenancy model for agent sandboxes** | G3 | Production scale blocker. Scope: namespace-level tenant boundaries, tenant-scoped gateway policy, RBAC model, data isolation pattern, noisy-neighbor quotas. Reference OpenShell #1722. |

### Tier 2: file for next planning cycle (high gaps, enterprise readiness)

| # | RFE title | Covers gap | Rationale |
|---|----------|-----------|-----------|
| R4 | **SPIFFE identity provisioning for agent workloads** | G4 | Zero-trust foundation. Scope: SVID issuance for agent pods, dynamic registration for ephemeral agents, integration with Keycloak for delegation chain. Distinct from RHAISTRAT-1730 authorization. |
| R5 | **Token exchange and delegation chain for agents (AuthBridge)** | G5 | Enterprise identity requirement. Scope: Envoy ext-proc AuthBridge for RFC 8693 token exchange, Keycloak Federated Client Authentication, nested `act` claims. |
| R6 | **MCP protocol support at the agent layer** | G6 | 78% enterprise adoption. Scope: MCP client/server support in OpenShell sandbox, MCP-aware routing in gateway, integration with MCP Lifecycle Operator. Distinct from MCP Gateway feature (tool traffic governance). |
| R7 | **Agent CRD design aligned with Agent Sandbox SIG** | G7 | Platform engineer expectation. Scope: evaluate layered CRD approach (Agent Sandbox v1beta1 core + OpenShell extensions), GitOps compatibility, Template/Claim/Instance separation. |
| R8 | **Service binding for LLM endpoints in agent sandboxes** | G8 | Developer experience. Scope: automatic injection of LLM provider endpoints and MCP gateway URLs into agent sandbox environment. Replaces manual provider YAML. |

### Tier 3: file for roadmap backlog (medium gaps, differentiation)

| # | RFE title | Covers gap | Rationale |
|---|----------|-----------|-----------|
| R9 | **MLflow/OTEL tracing integration for agent workloads** | G10 | Observability. Scope: auto-wire MLflow experiments, OTEL trace propagation across agent-to-agent calls, correlation trace IDs with tenant metadata. |
| R10 | **Agent warm pool integration on RHOAI** | G17 | Cold start elimination. Scope: SandboxWarmPool CRD integration, pre-provisioned sandbox pools, millisecond assignment. |
| R11 | **Shadow agent discovery and inventory** | G12 | Governance gap. Scope: discover unregistered agent workloads in cluster, security posture assessment, onboarding pathway. |
| R12 | **Compliance template library for agent governance** | G14 | Regulated industries. Scope: pre-built OPA policy sets for SOC2, HIPAA, FedRAMP mapped to agent controls, Git-versioned and auditable. |
| R13 | **Non-sandboxed agent tracking** | G11 | Enterprise reality. Scope: register and govern agent workloads that do not run in OpenShell sandboxes (pre-existing deployments, lightweight agents). |

### RFEs NOT recommended (monitor only)

| Capability | Reason |
|-----------|--------|
| Intent-based authorization (G13) | No standard exists. Monitor IETF/NIST. Too early for RFE. |
| Agent cost optimization / FinOps (G15) | P2 priority. Depends on multi-tenancy (R3). File after G3 resolved. |
| Third-party security audit (G16) | Procurement decision, not a feature. Track as action item. |
| Hybrid cloud agent mesh (G9) | White space but depends on A2A + identity (R4, R5). File after foundation in place. |
| Microsoft ARD tracking | Standards monitoring, not a feature. |

## 7. Summary statistics

| Metric | Count |
|--------|-------|
| Total Jira issues in snapshot | 209 |
| RHAISTRAT issues with ref- entries (capability-mapped) | 15 |
| Research-identified capabilities | 31 |
| Capabilities with confirmed Jira coverage | 14 |
| Capabilities with partial coverage | 3 |
| Capabilities with NO confirmed coverage | 14 |
| Open questions (5) with Jira tracking | 1 partial, 4 none |
| Persona-driven P0 requirements without Jira | 5 of 9 |
| Recommended RFEs: Tier 1 (file immediately) | 3 |
| Recommended RFEs: Tier 2 (next planning cycle) | 5 |
| Recommended RFEs: Tier 3 (roadmap backlog) | 5 |
| Total recommended RFEs | 13 |

## 8. Key findings

1. **The three critical gaps (FIPS, privileged SCC, multi-tenancy) have
   NO downstream Jira tracking.** All three have upstream OpenShell
   issues but no RHAISTRAT ensuring Red Hat-specific requirements
   (FIPS build pipeline, SCC testing, RHOAI namespace model) are
   addressed. These are the highest-risk gaps.

2. **The identity stack is the widest gap.** SPIFFE provisioning, token
   exchange, AuthBridge, and intent-based authorization span four
   research lenses but only authorization (RHAISTRAT-1730) has tracking.
   The three other identity capabilities are untracked. The research
   identifies this as "the hardest unsolved problem."

3. **MCP at the agent layer is untracked.** MCP Gateway (separate
   feature area) covers tool traffic governance, but MCP protocol
   support within agent sandboxes -- enabling agents to act as MCP
   clients/servers -- has no RHAISTRAT. This matters because MCP has
   78% enterprise adoption.

4. **5 of 9 P0 persona requirements have no Jira.** The requirements
   lens identified 9 P0 (non-negotiable) requirements across four
   personas. Five of them -- declarative CRD, multi-tenancy,
   restricted SCC, FIPS, and Keycloak identity -- have no confirmed
   RHAISTRAT.

5. **81 RHAISTRAT issues lack ref- entries.** The snapshot contains 96
   RHAISTRAT issues but only 15 have ref- entries mapping them to
   capabilities. Some of the 81 unmapped issues may cover identified
   gaps. A sweep to create ref- entries for the remaining issues would
   improve coverage visibility. Priority: the 28 issues created in
   June-July 2026 (RHAISTRAT-1993 through RHAISTRAT-2220).

## Sources

- Jira snapshot: `/features/agent-interop/work/jira-snapshot.yaml`
  (209 issues, swept 2026-07-11)
- Research series: 01-competitive through 05-landscape (2026-07-11)
- Knowledge base: 15 ref- entries, 5 open questions, 1 capability
  gaps fact
- No external sources -- this lens is internal cross-reference only
