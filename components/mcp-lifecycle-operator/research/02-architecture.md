---
title: MCP Lifecycle Operator — Architecture Research
description: RHOAI module operator integration (DSC -> Module Handler -> MCPLO Controller), Catalog->MCPLO->Gateway->Studio flow, CRD reconciliation loop, security architecture, TLS gap.
timestamp: 2026-07-11
lens: architecture
review_after: 2026-09-11
---

# MCP Lifecycle Operator — Architecture

## Three-Repo Pattern

RHOAI integration involves three repositories:

1. **kubernetes-sigs/mcp-lifecycle-operator** -- upstream SIG Apps
   operator (reconciles MCPServer CRs)
2. **opendatahub-io/mcp-lifecycle-module-operator** -- ODH module
   wrapper (reconciles MCPLifecycleOperator CRs, deploys the MCPLO
   controller)
3. **opendatahub-io/opendatahub-operator** -- parent operator (embeds
   the module handler, manages DSC component lifecycle)

## RHOAI Module Operator Integration

MCPLO integrates via the DSC (DataScienceCluster) CR as the component
`mcplifecycleoperator`. The DSC API (`api/components/v1alpha1/
mcplifecycleoperator_types.go`) defines `DSCMCPLifecycleOperator` with
standard `ManagementSpec` (Managed/Removed toggle) plus
`MCPLifecycleOperatorCommonSpec` (currently empty, placeholder for
future config).

**Module handler config:**

| Field | Value |
|-------|-------|
| ManifestDir | `mcplifecycleoperator` |
| DeploymentName | `mcp-lifecycle-module-operator-controller-manager` |
| ControllerImage | `RELATED_IMAGE_ODH_MCP_LIFECYCLE_MODULE_OPERATOR_IMAGE` |
| RelatedImages | `RELATED_IMAGE_ODH_MCP_LIFECYCLE_OPERATOR_IMAGE` |

Two-tier image pattern: module operator controller (runs in RHOAI
namespace, reconciles MCPLifecycleOperator CRs) and actual MCPLO
controller (the operand that reconciles MCPServer CRs).

**Manifest sources (get_all_manifests.sh):**
- ODH: `opendatahub-io:mcp-lifecycle-module-operator:main@<sha>:config`
- RHOAI: `red-hat-data-services:mcp-lifecycle-module-operator:rhoai-3.5@<sha>:config`

## Reconciliation Chain

```
DataScienceCluster CR
  -> DSC Reconciler (opendatahub-operator)
    -> MCPLifecycleOperator module handler
      -> Checks ManagementState (Managed/Removed)
      -> Deploys kustomize manifests from module-operator/config
      -> Creates MCPLifecycleOperator CR
        -> Module operator reconciles
          -> Deploys actual MCPLO controller
            -> Watches MCPServer CRs
              -> Creates Deployment + Service + NetworkPolicy
```

## Catalog -> MCPLO -> Gateway -> Studio Flow

**Stage 1 -- Discover (MCP Catalog in AI Hub):**
Pre-loaded with curated MCP servers in three tiers: Red Hat (OpenShift,
AAP, Lightspeed), technology partners (Confluent, EDB, IBM, Azure,
Dynatrace), and community (MongoDB, MariaDB). All images built on UBI,
scanned, hosted on quay.io/mcp-servers/. Deploy button disabled when
MCPServer CRD absent.

**Stage 2 -- Deploy (MCPLO):**
User clicks Deploy -> MCPServer CR created -> MCPLO validates (CM/Secret
existence) -> sets Accepted=True -> creates Deployment (Restricted PSS),
Service (ClusterIP, session affinity), NetworkPolicy (ingress on port)
-> waits for readiness -> MCP protocol handshake -> sets Ready=True ->
populates status.address.url.

**Stage 3 -- Connect (MCP Gateway via Connectivity Link):**
Server federation behind single endpoint. MCPServerRegistration targets
HTTPRoute per server. MCPGatewayExtension extends Gateway with MCP
parsing. AuthPolicy attaches for JWT validation (Keycloak). Tool-level
access control, configurable toolPrefix for name collision handling.

**Stage 4 -- Consume (Gen AI Studio / Playground):**
Deployed servers appear in Studio. Users experiment with models + MCP
tools. Llama Stack integration for tool invocation during inference.

## MCPServer CRD Reconciliation Loop

1. **Fetch** MCPServer resource (not found -> clean up metrics, return)
2. **validateConfig()** -- check storage mounts, envFrom, env valueFrom
   for CM/Secret existence. NotFound/BadRequest -> permanent
   ValidationError (Accepted=False, no requeue). Transient errors ->
   exponential backoff.
3. **reconcileDeployment()** -- build pod template with security
   defaults, apply config hash annotation (drives rolling updates on
   Secret/CM changes), create or update via server-side apply.
4. **reconcileService()** -- ClusterIP, port "mcp", session affinity
   per stateless flag.
5. **reconcileNetworkPolicy()** -- ingress-only on configured TCP port,
   no source restrictions.
6. **reconcileReadyCondition()** -- check deployment status
   (ScaledToZero/Initializing/DeploymentUnavailable).
7. **MCP Protocol Handshake** (when deployment available) -- connect via
   StreamableClientTransport (HTTP, 10s timeout), send Initialize
   request, extract server info + capabilities, populate
   status.serverInfo. Auth errors (401/403) treated as reachable.
   Failure: exponential backoff 10s->20s->...->2min cap, max 10
   retries (MCPHandshakeRetriesExhausted).

**Watch triggers:** MCPServer changes (generation, annotation, label),
owned Deployments/Services/NetworkPolicies, referenced ConfigMaps and
Secrets via field indexers.

## Security Architecture

**Pod Security Standards (Restricted by default):**
- AllowPrivilegeEscalation: false
- ReadOnlyRootFilesystem: true
- RunAsNonRoot: true
- Capabilities: Drop ALL
- SeccompProfile: RuntimeDefault

Users can override via spec.runtime.security.securityContext.

**RBAC model:** Operator manages Deployments/Services/NetworkPolicies,
reads ConfigMaps/Secrets. Per-server ServiceAccount via
spec.runtime.security.serviceAccountName. Default: namespace default SA.

**NetworkPolicy:** Ingress-only on configured port, no source
restrictions, no egress restrictions. Gap: production environments
need additional source-scoped policies.

**Ownership/drift:** ownerReferences on child resources, drift
detection via semantic deep comparison, orphaned resource adoption.

## TLS Gap

Current status.address.url shows http:// (not https://). MCP server
traffic is unencrypted within the cluster. MCP Gateway handles TLS
termination at ingress. RHOAIENG-72309 ("Central TLS Profile
consistency") addresses this: module operator passes TLS config to
MCPLO, MCPLO handles TLS from env. The MCPLifecycleOperatorCommonSpec
(currently empty) is the likely vehicle for TLS profile configuration.
PR #257 upstream adds TLS env propagation.

## Disconnected Architecture

No MCPLO-specific disconnected docs found. Based on RHOAI patterns:
operator images via RELATED_IMAGE_* in OLM CSV (oc adm catalog mirror),
MCP server images need manual mirroring, MCPServer CR supports arbitrary
image references, catalog UI is static content (no internet needed to
browse). Key gap: no declarative catalog manifest for offline delivery.

## Maturity Status (RHOAI 3.4, May 2026)

| Component | Maturity |
|-----------|----------|
| MCP Lifecycle Operator | Developer Preview (v0.1.0) |
| MCP Catalog | Developer Preview |
| MCP Gateway | Technology Preview |
| MCPServer CRD | Alpha (v1alpha1) |

Sources: [kubernetes-sigs/mcp-lifecycle-operator](https://github.com/kubernetes-sigs/mcp-lifecycle-operator),
[opendatahub-io/opendatahub-operator](https://github.com/opendatahub-io/opendatahub-operator),
[Red Hat MCPLO blog](https://www.redhat.com/en/blog/manage-mcp-servers-red-hat-openshift-mcp-lifecycle-operator),
[Red Hat MCP Catalog blog](https://www.redhat.com/en/blog/mcp-catalog-here-discover-deploy-and-connect-red-hat-openshift-ai),
[Red Hat MCP Gateway blog](https://www.redhat.com/en/blog/control-your-ai-agent-traffic-scale-model-context-protocol-gateway-red-hat-openshift-now-technology-preview),
[Kuadrant/mcp-gateway](https://github.com/Kuadrant/mcp-gateway)
