---
title: MCP Lifecycle Operator — Requirements Gap Analysis
description: GA requirements mapped to Operator Capability Levels (L1-2 to L3-4). P0 gaps in observability, disconnected catalog, OLS transition, Helm deprecation. P1 in sandbox, governance, entitlements.
timestamp: 2026-07-11
lens: requirements
review_after: 2026-09-11
---

# MCP Lifecycle Operator — Requirements Gap Analysis

## 1. Operator Maturity (RHAISTRAT-1995 / OCPSTRAT-2879)

MCPLO is at Operator Capability Level 1-2. GA requires Level 3-4.

| Level | Required for GA | Status |
|-------|----------------|--------|
| L1: Basic Install | Automated provisioning via CRD | Done |
| L2: Seamless Upgrades | Rolling updates, version transitions | Partial (OCPSTRAT-2879 lists automated rolling updates) |
| L3: Full Lifecycle | Backup, restore, failover, Day 2 ops | Not started |
| L4: Deep Insights | Prometheus metrics, alerts, detailed status | OCPSTRAT-2879 lists ServiceMonitor; metrics added in v0.2.0 |

**RHAISTRAT-1995 specific gaps:**
1. Dependency awareness -- unclear errors when Gateway absent
2. Observability -- no ServiceMonitor, no alerting rules
3. Documentation -- no production patterns, upgrade paths, runbooks
4. Support commitment -- TP/DP support only

**P0 recommendations:**
- Prometheus ServiceMonitor auto-created per MCPServer
- PrometheusRule for alerting (server down > 5 min, handshake failures)
- GatewayAvailable condition with actionable messages
- Operator-level /metrics endpoint (reconcile duration, errors, queue depth)
- Admission webhook for CRD validation
- Conversion webhook planning (v1alpha1 to v1beta1 path)

**P1 recommendations:**
- Expanded conditions (ServerHealthy, GatewayRegistered, ConfigValid)
- Graceful rollout with automatic rollback on handshake failure
- Kubernetes Events for lifecycle milestones

Reference: [Operator SDK Capability Levels](https://sdk.operatorframework.io/docs/overview/operator-capabilities/),
[CNCF Operator White Paper](https://tag-app-delivery.cncf.io/whitepapers/operator/)

## 2. Disconnected Catalog Delivery

**Current state:** MCPLO images via RHOAI offline bundle. MCP server
catalog has no offline delivery mechanism.

**Gap:** No declarative catalog manifest, no oc-mirror integration for
MCP server images, no offline browse-and-deploy experience.

**P0 recommendations:**
- MCP Server Catalog as OCI artifact (follows OLM File-Based Catalog
  pattern) -- package metadata (names, descriptions, image refs, tool
  manifests) as OCI artifact for mirroring
- oc-mirror support via ImageSetConfiguration additionalImages
- Offline catalog UI reading from local/mirrored catalog source

**P1 recommendations:**
- IDMS generation for cluster-side image redirect
- Incremental catalog updates (delta mirrors)

Reference: [oc-mirror v2 docs](https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/html/disconnected_environments/installing-mirroring-disconnected),
[Flux CD OCI artifacts](https://fluxcd.io/flux/cheatsheets/oci-artifacts/)

## 3. OLS Transition

**Current state:** OLS uses internal OCP MCP server. Productized MCPLO
means OLS will ask users to install via MCPLO.

**Gaps:**
1. Subscription cliff -- today OLS works with just OCP; after transition,
   needs RHOAI (at least limited entitlement)
2. Installation complexity increase (0 steps to 3)
3. Version coupling (OLS releases coupled to RHOAI operator)
4. No rollback if external MCP server has issues

**P0 recommendations:**
- Transparent fallback -- OLS detects MCPLO-managed server, uses it if
  available, continues with internal implementation if not
- Zero-config for OCP users -- single-click "Enable MCP servers" in
  console, not multi-step RHOAI operator installation

**P1 recommendations:**
- Documented migration path with validation and rollback steps
- Clear deprecation timeline for OLS internal MCP server

## 4. Code Mode / Agent Sandbox (OCPSTRAT-2879)

OCPSTRAT-2879 requires integration with Agent Sandbox for
network-isolated code execution.

**Gaps:**
- MCPServer CRD has no sandbox requirement field
- No sandbox provisioning trigger on MCPServer deploy
- Network policy coordination (MCPLO NetworkPolicy vs sandbox networking)
- Security model gap (PSS necessary but insufficient for code execution)

**P0 recommendation:**
- MCPServer CRD sandbox annotation
  (spec.runtime.sandbox: {enabled: true, profile: "code-execution"})

**P1 recommendations:**
- SandboxReady condition in MCPServer status
- Pre-built OPA policy library for MCP server security profiles

Reference: [NSA MCP Security Guidance (June 2026)](https://media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF),
[CSA MCP Security Crisis (May 2026)](https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-security-crisis-20260504-csa-styled/)

## 5. Helm Deprecation Path

Standalone Helm chart deprecated after MCPLO reaches TP.

**Gaps:** No migration guide, no migration tooling, no deprecation
notice, no resource adoption mechanism.

**P0 (for TP):**
- Configuration mapping document (Helm values -> MCPServer CRD spec)
- Deprecation notice in Chart.yaml

**P1 (for GA):**
- Migration script (reads Helm release, generates MCPServer YAML)
- Resource adoption (MCPLO adopts existing Helm-created resources)
- Coexistence documentation

Reference: [Hazelcast Helm-to-Operator migration](https://docs.hazelcast.com/operator/5.15/migrating-from-helm),
[Redpanda migration](https://docs.redpanda.com/current/migrate/kubernetes/helm-to-operator/)

## 6. RHOAI Limited Entitlement Clarity

**Gaps:** No telemetry for entitlement tracking, unclear capability
gating, no self-service entitlement check, RHCL BU transition
uncertainty.

**P0:** Entitlement-aware operator behavior with clear error messages
**P1:** Usage metering for subscription compliance, customer-facing
entitlement matrix

## 7. Multi-Cluster

**Gaps:** No cross-cluster discovery, no RHACM integration, no federated
catalog, no cross-cluster Gateway routing.

**P1:** RHACM OperatorPolicy docs for fleet MCPLO deployment (no MCPLO
changes needed), MCPServer ConfigurationPolicy for CRD replication
**P2:** Cross-cluster service discovery via MCP Registry, MCP Gateway
federation

Reference: [RHACM OperatorPolicy](https://developers.redhat.com/articles/2024/08/08/getting-started-operatorpolicy)

## 8. Enterprise Governance

**Gaps:** No approval workflows, no MCPLO-specific audit events, no
image allowlist policy, no tool-level policy, no OPA/Gatekeeper
templates, no version pinning, no SBOM generation.

**P0:** Audit logging documentation, OPA Gatekeeper constraint
templates (image allowlist, required labels, namespace restrictions),
image signature verification docs
**P1:** Operator-emitted Events for lifecycle transitions, version
pinning spec field, pre-built Gatekeeper policy library
**P2:** Approval workflow integration (ServiceNow/Jira), SBOM
generation, tool-level access control, compliance dashboard

Reference: [OPA Gatekeeper enterprise guide](https://support.tools/post/enterprise-opa-gatekeeper-kubernetes-policy-management-2025/),
[Kubernetes audit docs](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/)

## Priority Matrix

| Area | GA Readiness | Key Blocker | Priority |
|------|-------------|-------------|----------|
| Operator maturity (L3-4) | Partial | Missing observability | P0 |
| Disconnected catalog | Not started | No OCI artifact pattern | P0 |
| OLS transition | Not started | Subscription cliff | P0 |
| Helm deprecation | Not started | No migration guide | P0 (TP) / P1 (GA) |
| Agent Sandbox | Design phase | OpenShell not stable | P1 |
| Entitlement clarity | Partial | RHCL BU transition | P1 |
| Enterprise governance | Minimal | Missing audit/policy | P1 |
| Multi-cluster | Not started | Needs RHACM docs only | P2 |
