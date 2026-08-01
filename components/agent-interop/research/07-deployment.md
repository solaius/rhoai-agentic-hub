---
title: "Deployment Lens: OpenShell on RHOAI"
description: Practical deployment patterns for OpenShell across environments — topologies, prerequisites, Helm configuration, OpenShift SCC constraints, RHOAI operator integration, air-gap/FIPS considerations, ingress strategies, and multi-cluster patterns.
timestamp: 2026-07-27
lens: deployment
review_after: 2026-09-27
---

# Deployment Lens: OpenShell on RHOAI

This lens covers the practical HOW of deploying OpenShell. It extends the
architecture (03) and requirements (04) lenses with operationally-focused
detail: what gets installed, in what order, with what configuration, across
which environments.

## 1. Deployment topologies in practice

OpenShell supports three deployment topologies defined by the crate
decomposition (RFC #1305). Each maps to different environments and
threat models.

### Topology A: Combined (single container)

The status quo. The `openshell-sandbox` binary bundles proxy, runtime,
and composition glue into one container. The agent container carries
Linux capabilities needed by the supervisor for network namespace setup,
Landlock, privilege drop, and network policy enforcement.

**When to use:** Developer workstations, evaluation clusters, single-user
setups. The simplest path with the fewest moving parts.

**Prerequisites:** The agent container needs CAP_SYS_ADMIN, CAP_NET_ADMIN,
CAP_SYS_PTRACE, CAP_SYSLOG, and `runAsUser: 0`. On OpenShift, this
means the privileged SCC.

**Helm value:** `supervisor.topology=combined` (default)

**Operational profile:** One pod per sandbox. The supervisor owns all
enforcement (filesystem, process, network, inference) in-process.
Gateway manages lifecycle via Agent Sandbox CRDs.

### Topology B: Sidecar (proxy + runtime split)

Network enforcement runs in a dedicated sidecar container; the process
supervisor runs as a low-capability wrapper in the agent container.
The sidecar topology is enabled by the crate decomposition, which
separates `openshell-proxy` (~12k lines, 70% of codebase) from
`openshell-runtime` (~4k lines).

**When to use:** Shared clusters, enterprise environments where elevated
privileges are unacceptable, environments with VM-boundary isolation
(Kata/gVisor RuntimeClass). The proxy sidecar runs in the pod's root
network namespace and does NOT need elevated privileges; the agent runs
inside its own network namespace with Landlock/seccomp.

**New finding (extends existing knowledge):** The Helm chart now exposes
`supervisor.topology=sidecar` with two sub-modes:
- `supervisor.sidecar.processBinaryAwareNetworkPolicy=true` (default):
  strict mode, sidecar runs as UID 0 for /proc inspection capabilities,
  enforces binary-identity-bound network policy
- `supervisor.sidecar.processBinaryAwareNetworkPolicy=false`: relaxed
  mode, sidecar runs as `proxyUid` (default 1337), drops extra /proc
  inspection capabilities. Network policy enforcement without
  process/binary matching.

Both modes use `shareProcessNamespace: true` so the sidecar can resolve
process identity through `/proc/<entrypoint-pid>`.

**Networking detail:** Kubernetes mode always creates a nested network
namespace. The agent cannot reach the sidecar at 127.0.0.1 directly --
all traffic routes through the supervisor proxy via the veth pair
(10.200.0.2 -> 10.200.0.1:3128). The supervisor runs in the pod's root
network namespace and CAN reach the sidecar at 127.0.0.1.

**Key implication for SCC elimination:** In sidecar topology with
Kata/gVisor RuntimeClass, the proxy runs outside the gVisor sandbox
without elevated privileges. This is the path to eliminating the
privileged SCC requirement on OpenShift (see Section 6).

### Topology C: Standalone egress filter (proxy only)

`openshell-proxy` deployed as a standalone container with no runtime
component. Acts purely as a network policy enforcement point.

**When to use:** When agents are deployed via other mechanisms (direct
pod deployment, existing orchestrators) but need egress filtering,
credential injection, and L7 inspection. Also useful for non-Kubernetes
environments that want proxy-only enforcement.

**Prerequisites:** The proxy needs no elevated privileges -- it operates
purely at the network layer.

### Topology comparison

| Aspect | A (Combined) | B (Sidecar) | C (Proxy only) |
|--------|-------------|-------------|----------------|
| Elevated privileges | Required (CAP_SYS_ADMIN etc.) | Optional (relaxed sidecar mode) | None |
| Filesystem isolation | Landlock | Landlock + VM boundary | None |
| Network policy | In-process OPA | Sidecar OPA | Standalone OPA |
| Process isolation | seccomp + privilege drop | seccomp + VM boundary | None |
| Inference routing | Yes | Yes | Yes |
| Credential injection | Yes | Yes | Yes |
| OpenShift SCC | Privileged | Restricted (with Kata) | Restricted |
| Complexity | Low | Medium | Low |
| Pod count per agent | 1 | 1 (multi-container) | 1 (sidecar to existing pod) |

## 2. Environment variations

### 2.1 Vanilla Kubernetes (reference path)

The cleanest deployment path. Follows the Helm chart defaults without
platform-specific overrides.

**Minimum requirements:**
- Kubernetes 1.29+
- Helm 3.x
- Agent Sandbox controller and CRDs installed
- glibc 2.28+ on nodes (Ubuntu 20.04+, RHEL 8+, Rocky 8+, Amazon Linux 2023+, Fedora 32+)
- Linux kernel 5.13+ for Landlock LSM (recommended), 3.17+ for seccomp (required)

**Gateway workload:** StatefulSet by default (SQLite backend). Switch to
Deployment with `workload.kind=deployment` when using external PostgreSQL
(`server.externalDbSecret`).

**Namespace:** Dedicated `openshell` namespace. Sandbox pods created in
the release namespace by default, configurable via
`server.sandboxNamespace`.

### 2.2 OpenShift

**Status: Experimental. Not for production.**

OpenShift's SCC admission controller rejects the chart's default pod
security settings. Three adjustments are required:

1. **Pre-create namespace:** `oc create ns openshell`
2. **Grant privileged SCC to sandbox service account:**
   `oc adm policy add-scc-to-user privileged -z openshell-sandbox -n openshell`
3. **Helm overrides:**
   - `podSecurityContext.fsGroup=null` (let SCC assign)
   - `securityContext.runAsUser=null` (let SCC assign)
   - `server.disableTls=true` (simplified evaluation path)

**OpenShift-specific issue:** OpenShell sets up sandbox nftables rules as
individual commands. On OpenShift nodes lacking optional conntrack or
packet log expressions, those optional rules can fail without rolling
back the required proxy bypass reject rules.

**Layered sandboxing (new finding, extends architecture lens):** A Red Hat
Developer article (Jul 2026) validates the dual-protection topology:
OpenShell inside Kata micro-VM. Tested on OpenShift 4.21 against two
attack classes:
- Prompt injection exfiltration: OpenShell proxy blocks (Kata alone: leaked)
- Kernel exploit CVE-2026-31431: Kata VM boundary blocks (OpenShell alone: host compromised)
- Both layers together: both attacks blocked. Neither layer interferes
  with the other. OpenShell does not need to know it runs inside a VM.

This validates Topology B as the production path for OpenShift.

### 2.3 Local development (Podman/Docker)

The simplest path. The install script auto-detects the platform and
starts a local gateway:

```
curl -LsSf https://raw.githubusercontent.com/NVIDIA/OpenShell/main/install.sh | sh
```

**Compute drivers:**
| Driver | Requirements | Best for |
|--------|-------------|----------|
| Docker | Docker Desktop or Engine 28.0+ | macOS, Windows WSL2, Linux |
| Podman | Podman 5.x, cgroups v2, rootless networking | Linux workstations avoiding rootful Docker |
| MicroVM | Hypervisor.framework (macOS), KVM (Linux) | VM-level isolation on desktop |

**Gateway:** Listens on `https://127.0.0.1:17670` with auto-generated
mTLS. Config at `~/.config/openshell/gateway.toml`. Client bundle at
`~/.config/openshell/gateways/openshell/mtls/`.

**Lifecycle:** Managed via systemd user services (Linux) or Homebrew
services (macOS). `sudo loginctl enable-linger $USER` for persistence
after logout on Linux.

**Snap:** Also available via `sudo snap install openshell`. Docker plug
requires manual connection: `sudo snap connect openshell:docker docker:docker-daemon`.

### 2.4 Air-gapped / disconnected environments

**No official air-gap documentation exists.** This is a recognized gap
(NemoClaw #2218 explicitly calls it out). Based on the Kubernetes setup
documentation, the following images and manifests must be mirrored:

**Images to mirror:**
- `ghcr.io/nvidia/openshell/gateway:<version>` (amd64 + arm64)
- `ghcr.io/nvidia/openshell/supervisor:<version>`
- `ghcr.io/nvidia/openshell-community/sandboxes/base:latest` (or custom sandbox images)
- `registry.k8s.io/agent-sandbox/agent-sandbox-controller:<version>`
- Any agent images (Claude Code, OpenCode, Codex, or custom)

**Manifests to mirror:**
- Agent Sandbox controller manifest (from kubernetes-sigs/agent-sandbox releases)
- OpenShell Helm chart OCI artifact (`oci://ghcr.io/nvidia/openshell/helm-chart`)

**Helm configuration for disconnected:**
```yaml
image:
  repository: internal-registry.example.com/openshell/gateway
imagePullSecrets:
  - name: regcred
server:
  sandboxImage: internal-registry.example.com/openshell/sandboxes/base:latest
  sandboxImagePullSecrets:
    - name: regcred
supervisor:
  image:
    repository: internal-registry.example.com/openshell/supervisor
```

**Inference routing in air-gap:** The `inference.local` pattern becomes
critical. Agents call `https://inference.local`, and the gateway routes
to an internal model endpoint. Use an OpenAI-compatible provider pointing
at an internal vLLM/Ollama instance:
```
openshell provider create --name internal-llm --type openai \
  --credential OPENAI_API_KEY=empty-if-not-required \
  --config OPENAI_BASE_URL=http://vllm.internal:8000/v1
```

Use `host.openshell.internal` or the host's LAN IP for host-local model
servers. Avoid 127.0.0.1 since the request originates from the gateway,
not the shell.

## 3. Prerequisite stack (dependency chain)

The deployment dependency chain, bottom to top:

```
1. Kubernetes cluster (1.29+) with RBAC
   |
2. Agent Sandbox controller + CRDs
   |  kubectl apply -f .../agent-sandbox/.../manifest.yaml
   |  Creates: agent-sandbox-system namespace, sandboxes.agents.x-k8s.io CRD,
   |           controller deployment
   |  CRDs: Sandbox, SandboxClaim, SandboxTemplate, SandboxWarmPool (v1beta1)
   |
3. [Optional] cert-manager (if not using built-in PKI bootstrap)
   |
4. [Optional] Kubernetes Gateway API + controller (e.g., Envoy Gateway)
   |  Only needed for external access without port-forwarding
   |
5. OpenShell namespace
   |  kubectl create namespace openshell
   |  [OpenShift only] oc adm policy add-scc-to-user privileged -z openshell-sandbox -n openshell
   |
6. OpenShell Helm chart
   |  helm install openshell oci://ghcr.io/nvidia/openshell/helm-chart --version <version>
   |  Creates: Gateway StatefulSet/Deployment, ServiceAccounts (openshell, openshell-sandbox),
   |           Role/RoleBinding, ClusterRole/ClusterRoleBinding, Services,
   |           PKI secrets (pre-install hook), NetworkPolicy
   |
7. CLI installation + gateway registration
   |  openshell gateway add https://... --name <name>
   |
8. Provider configuration
   |  openshell provider create --name <name> --type <type> ...
   |
9. Inference route configuration
   |  openshell inference set --provider <name> --model <model>
   |
10. Sandbox creation
    openshell sandbox create -- claude
```

**Agent Sandbox upgrade note:** When Agent Sandbox is upgraded in place,
the OpenShell gateway MUST be restarted because it caches the detected
Sandbox API versions at startup. Existing sandboxes keep running during
the upgrade.

### Red Hat-specific prerequisite path (OpenShift)

Two options for Agent Sandbox:
- **Option 1 (recommended):** Red Hat build of Agent Sandbox v0.9.0
  (OpenShift Sandboxed Containers 1.12). Installs via OperatorHub.
- **Option 2:** Upstream kubernetes-sigs/agent-sandbox manifests
  (requires manual image mirroring on OpenShift).

## 4. RHOAI integration path

### Current state (Dev Preview, RHOAI 3.5)

OpenShell is NOT yet integrated as a DSC-managed component. The Dev
Preview ships documentation and enablement with Konflux pipeline setup
for images. Users deploy OpenShell independently via the Helm chart.

### Target state (RHAISTRAT-1752: Productize OpenShell Operator)

RHAISTRAT-1752 covers the full productization path:
- **Midstream/downstream build pipeline:** Konflux-based builds
- **Base images:** Dual path -- both Hummingbird and UBI/RHEL (decision
  2026-07-17, pursuing both, no exclusive bet)
- **OLM/OperatorHub packaging:** Separate OLM-based operator
- **DSC-managed component integration:** Integration with rhods-operator
  as a DSC-managed component
- **CVE scanning:** Standard Red Hat vulnerability management
- **Support lifecycle:** Aligned with RHOAI release cadence

### DSC integration pattern

The RHOAI DataScienceCluster CR manages components via `managementState`
(Managed/Removed). As of RHOAI 3.3, the DSC includes ~15 components
(kserve, modelregistry, trustyai, etc.). OpenShell would follow the same
pattern:

```yaml
spec:
  components:
    openshell:
      managementState: Managed
```

However, the SKU decision (question-openshell-sku-product-home.md) is
still open. Multiple delivery vehicles are under consideration:

| Option | Pros | Cons |
|--------|------|------|
| RHOAI umbrella operator (DSC component) | Unified management, single install | Hefty process, operator coupling, RHOAI refactoring in progress |
| Separate OLM operator | Less coupling, upstream-friendly | Separate lifecycle, additional install step |
| Red Hat AI SKU | Different footprint for personal agent use | New product, separate support |
| OCP component | Broad availability | Release cadence mismatch |

Roland Huss noted separate operator is viable and avoids RHOAI coupling.
Ann Marie noted it could be an optional prerequisite operator. The
separate-operator path parallels how cert-manager and Serverless are
prerequisites for RHOAI but not DSC-managed.

### Operator timeline

| Milestone | Target | Operator state |
|-----------|--------|---------------|
| RHOAI 3.5 (DP) | Jul-Aug 2026 | No operator. Helm chart only. |
| RHOAI 3.6 (TP) | Nov 2026 | Operator for lifecycle management. |
| RHOAI 3.7 (GA) | Early 2027 | Full operator with DSC integration. |

### Integration with MCP Lifecycle Operator

The MCP Lifecycle Operator (agent-catalog feature) manages MCP server
lifecycle. In the RHOAI 3.6 timeframe, agent-catalog deploys agents via
the OpenShell Go SDK and supported harness images. The integration point
is the sandbox creation API -- the catalog operator would call the
OpenShell gateway to create sandboxes for agent deployments, with
OpenShell handling isolation and the catalog handling discovery and
deployment specification.

### Database backend decision

**New finding (not in architecture lens):** The Dev Preview uses Postgres
as the backend database (decision 2026-07-17). This aligns with the Helm
chart's `server.externalDbSecret` path for external PostgreSQL, enabling
multi-replica Deployments. The default SQLite backend is for evaluation
only.

## 5. Helm configuration patterns

### Complete values reference (key categories)

The Helm chart exposes ~80 configurable values. The most deployment-relevant:

#### Workload and scaling

| Value | Default | Notes |
|-------|---------|-------|
| `workload.kind` | `statefulset` | Use `deployment` with external DB |
| `replicaCount` | `1` | >1 requires `server.externalDbSecret` |
| `resources` | `{}` | Set CPU/memory requests and limits |
| `terminationGracePeriodSeconds` | `5` | Gateway pod termination grace |

#### Security context (OpenShift-critical)

| Value | Default | Notes |
|-------|---------|-------|
| `podSecurityContext.fsGroup` | `1000` | Set to `null` on OpenShift |
| `securityContext.runAsUser` | `1000` | Set to `null` on OpenShift |
| `securityContext.runAsNonRoot` | `true` | Standard non-root |
| `securityContext.allowPrivilegeEscalation` | `false` | Standard |
| `securityContext.capabilities.drop` | `["ALL"]` | Drop all capabilities |
| `server.appArmorProfile` | `Unconfined` | RuntimeDefault may block supervisor |
| `server.enableUserNamespaces` | `false` | K8s 1.33+ user namespace isolation |

#### Authentication

| Value | Default | Notes |
|-------|---------|-------|
| `server.oidc.issuer` | `""` | OIDC issuer URL; empty disables |
| `server.oidc.audience` | `openshell-cli` | Expected JWT audience |
| `server.oidc.rolesClaim` | `""` | Path to roles in JWT (e.g., `realm_access.roles`) |
| `server.oidc.adminRole` | `""` | Admin role name |
| `server.oidc.userRole` | `""` | Standard user role name |
| `server.auth.allowUnauthenticatedUsers` | `false` | UNSAFE: skip auth checks |

#### TLS and PKI

| Value | Default | Notes |
|-------|---------|-------|
| `server.disableTls` | `false` | Plaintext HTTP; only behind trusted transport |
| `pkiInitJob.enabled` | `true` | Auto-generate mTLS and JWT secrets |
| `pkiInitJob.serverDnsNames` | `[]` | Extra DNS SANs for server cert |
| `certManager.enabled` | `false` | Use cert-manager instead of PKI job |

#### Sandbox configuration

| Value | Default | Notes |
|-------|---------|-------|
| `server.sandboxImage` | `ghcr.io/.../base:latest` | Default sandbox container image |
| `server.sandboxNamespace` | `""` | Defaults to release namespace |
| `server.defaultRuntimeClassName` | `""` | RuntimeClass for sandbox pods (Kata, gVisor) |
| `server.workspaceDefaultStorageSize` | `""` | Default PVC size (built-in 2Gi) |
| `supervisor.topology` | `combined` | `combined` or `sidecar` |
| `supervisor.sideloadMethod` | `""` | Auto-detects: `image-volume` (K8s 1.35+) or `init-container` |

#### Networking and ingress

| Value | Default | Notes |
|-------|---------|-------|
| `service.type` | `ClusterIP` | Service type |
| `service.port` | `8080` | Gateway gRPC/HTTP port |
| `service.healthPort` | `8081` | Health check port |
| `service.metricsPort` | `9090` | Prometheus metrics port |
| `grpcRoute.enabled` | `false` | Create Gateway API GRPCRoute |
| `networkPolicy.enabled` | `true` | SSH ingress restriction on sandbox pods |

#### SPIFFE integration

| Value | Default | Notes |
|-------|---------|-------|
| `server.providerTokenGrants.spiffe.enabled` | `false` | Mount SPIFFE socket into sandboxes |
| `server.providerTokenGrants.spiffe.workloadApiSocketPath` | `/spiffe-workload-api/spire-agent.sock` | SPIFFE socket path |

### CI overlay files

The chart ships tested configuration overlays in `ci/`:
- `values-gateway.yaml` -- gateway-only
- `values-cert-manager.yaml` -- cert-manager integration
- `values-keycloak.yaml` -- Keycloak OIDC
- `values-high-availability.yaml` -- multi-replica + external PostgreSQL
- `values-spire.yaml` -- SPIFFE/SPIRE provider token grants
- `values-spire-stack.yaml` -- SPIRE hardened chart for local dev

These serve as tested reference configurations for each integration
pattern.

## 6. Air-gap and FIPS considerations

### Air-gapped deployment

**Gap confirmed:** No official air-gap documentation or deployment path
exists (NemoClaw #2218). The practical approach requires:

1. **Image mirroring:** All container images (gateway, supervisor,
   sandbox base, agent sandbox controller, agent images) must be
   mirrored to an internal registry.
2. **Helm chart mirroring:** The OCI Helm chart artifact must be pulled
   and pushed to an internal OCI registry.
3. **Agent Sandbox manifest:** The controller manifest must be downloaded
   and modified to reference internal image repositories.
4. **Inference routing:** All LLM endpoints must be internal (vLLM,
   Ollama, TGI, or similar running on internal infrastructure).
5. **Policy configuration:** Egress policies are deny-by-default, which
   actually simplifies air-gap -- only internal endpoints need
   allowlisting.

**Red Hat downstream consideration:** The RHOAI operator handles
disconnected installs via operator catalog mirroring and
ImageContentSourcePolicy/ImageDigestMirrorSet. When OpenShell becomes
an OLM operator, it would inherit this pattern.

### FIPS compliance

**Status: Active development. No FIPS build available today.**

The FIPS gap analysis (OpenShell #900) identifies three crypto
subsystems:

| Subsystem | Current library | FIPS status | Phase 1 replacement |
|-----------|----------------|-------------|-------------------|
| TLS | rustls + ring 0.17 | Not validated | aws-lc-rs (CMVP #4631) |
| SSH | russh 0.57 + mixed backends | Not validated | Algorithm restriction only |
| PKI | rcgen + ring | Not validated | aws-lc-rs |

**Phase 1 approach (feature-flagged):** A workspace-level `fips` Cargo
feature flag that:
- Switches crypto backend from ring to aws-lc-rs
- Restricts TLS to FIPS-approved cipher suites (AES-GCM only, no
  ChaCha20, no X25519)
- Restricts SSH to FIPS-approved algorithms (ECDSA-P256 host keys, no
  Ed25519)
- Replaces HMAC implementation with aws-lc-rs HMAC-SHA256

**Phase 2 (deferred):** Full SSH transport validation. Currently, Phase 1
restricts SSH to FIPS-approved *algorithms* but the underlying russh
implementations remain non-validated modules. The SSH transport operates
within the cluster's mTLS boundary (gateway-to-sandbox), providing
defense-in-depth rather than the primary trust boundary.

**Build complexity:** aws-lc-rs FIPS builds require CMake + Go in the
build toolchain. Cross-compilation from macOS to linux/amd64 for FIPS
container builds may require remote builds.

**Base image complication:** The current base image is Ubuntu Noble, not
UBI, so no FIPS OpenSSL is present. The dual base-image path decision
(pursuing both Hummingbird and UBI/RHEL) is relevant here -- the UBI
path would provide FIPS OpenSSL for system-level crypto, while the
Rust-level FIPS flag handles OpenShell's own crypto.

**Concrete symptom on OpenShift:** On FIPS-enabled clusters, after adding
an egress policy for github.com, `curl -L https://github.com` inside the
sandbox returns `curl: (35) Insufficient randomness`. This is suspected
to be a FIPS-related problem in the base container image, not in
OpenShell's Rust crypto stack. The base image issue is orthogonal to the
aws-lc-rs migration.

**FIPS 140-2 sunset:** September 21, 2026. In-process CMVP applications
are not a valid compliance state after this date. This adds urgency to
the aws-lc-rs migration, which targets FIPS 140-3 (CMVP #4631).

### User namespaces: the privileged SCC elimination path

**New finding (extends question-openshell-privileged-scc.md):** The Helm
chart now supports `server.enableUserNamespaces=true`, which sets
`hostUsers: false` on sandbox pods.

On Kubernetes 1.33+ (user namespaces beta, on by default), this maps
container UID 0 to an unprivileged host UID, making capabilities like
CAP_SYS_ADMIN namespaced to container-local resources only.

**Requirements:**
- Kubernetes 1.33+ (beta through 1.35, GA in 1.36+)
- containerd 2.0+ or CRI-O 1.25+
- Linux kernel 5.12+ for ID-mapped mounts

**OpenShift status:** OpenShift support for user namespaces is a work in
progress. The feature was previously rejected for OpenShell because K8s
user namespace support was alpha, not available on OpenShift, and the
seccomp filter blocks CLONE_NEWUSER. The K8s 1.33 beta promotion
changes this calculus.

**GPU caveat:** "NVIDIA device plugin compatibility with user namespaces
is unverified." OpenShell logs a warning when both GPU and user
namespaces are active. Recommendation: enable on non-GPU clusters for
stronger host isolation, test GPU workloads separately.

**Pod Security Standards relaxation:** When `hostUsers: false`, baseline
and restricted Pod Security Standards allow `runAsNonRoot: false` and
any `runAsUser`/`runAsGroup` value. Baseline namespaces can also set
any `capabilities.add`. This means the restricted SCC could
theoretically work with user namespaces.

**Related issue:** OpenShell #899 tracks restricted SCC support
specifically.

## 7. Ingress strategies

### Port-forwarding (development only)

```
kubectl -n openshell port-forward svc/openshell 8080:8080
openshell gateway add https://127.0.0.1:8080 --local --name k8s
```

mTLS client bundle extracted from `openshell-client-tls` secret.
Server cert SANs include localhost and 127.0.0.1. NOT for shared
environments.

### Kubernetes Gateway API (recommended for external access)

OpenShell uses GRPCRoute resources with a Gateway API controller.
Tested with Envoy Gateway (v1.8.1).

**Architecture:** Client -> HTTPS -> Envoy Gateway (terminates TLS)
-> plaintext -> OpenShell gateway pod.

**Key constraint:** Envoy Gateway OIDC SecurityPolicy must NOT be
enabled. The OIDC flow relies on browser redirects and cookies, which
do not work with the OpenShell CLI or headless agents. OpenShell
validates OIDC bearer tokens itself in gRPC authorization metadata.

**Helm values for external access:**
```yaml
grpcRoute:
  enabled: true
  hostnames: ["openshell.example.com"]
  gateway:
    create: true
    className: eg
    listener:
      protocol: HTTPS
      port: 443
      tls:
        certificateRefs:
          - name: openshell-tls-cert
server:
  disableTls: true    # Envoy terminates TLS
  oidc:
    issuer: https://keycloak.example.com/realms/openshell
    audience: openshell-cli
```

**TLS certificate provisioning:** Options include manual creation,
cert-manager issuance, or reusing the chart's `openshell-server-tls`
secret if its SANs cover the external hostname. Cross-namespace
references require a ReferenceGrant.

**Load balancing:** Handled by the Kubernetes LoadBalancer service
created by Envoy Gateway when the Gateway resource is provisioned.

### OpenShift Routes

The OpenShift documentation references an "Ingress guide" for external
exposure but does not provide inline detail. Given that the ingress
strategy uses Kubernetes Gateway API (not Ingress resources), OpenShift
Routes are not the native path. The Envoy Gateway pattern works on
OpenShift but requires installing Envoy Gateway separately (not
included in base OpenShift).

**Alternative:** OpenShift's built-in HAProxy Ingress Controller could
potentially be configured for gRPC passthrough, but this is not
documented or tested by NVIDIA.

### Service mesh integration

No documented integration with Istio or OpenShift Service Mesh.
OpenShell's internal mTLS (gateway-to-supervisor) operates independently.
The gateway's GRPCRoute approach uses Gateway API, which is the standard
Istio ingress pattern, so coexistence is straightforward but not
explicitly tested.

### Sandbox service forwarding

The gateway routes browser traffic to sandbox loopback ports via
`openshell service expose`. Local gateways use
`http://<sandbox>.openshell.localhost:<port>/` URLs. Custom HTTPS
domains require adding a wildcard DNS SAN to the gateway certificate
via `--server-san` or `OPENSHELL_SERVER_SAN`.

### Headless / CI authentication

For headless agents and CI pipelines, the CLI obtains tokens via the
OAuth2 client-credentials grant (no browser required). Set
`OPENSHELL_OIDC_CLIENT_SECRET` as an environment variable.
Interactive users get Authorization Code + PKCE browser flow by default.

## 8. Multi-cluster and hybrid patterns

### Current state: no documented multi-cluster support

OpenShell is fundamentally a single-cluster deployment. The gateway
manages sandboxes on one compute driver (one cluster). There is no
built-in federation, cross-cluster sandbox migration, or multi-cluster
gateway mesh.

### Multi-gateway pattern

The CLI supports registering multiple gateways:
```
openshell gateway add https://cluster-a.example.com --name prod-a
openshell gateway add https://cluster-b.example.com --name prod-b
openshell gateway select prod-a
```

Users switch between clusters manually. The active gateway resolution
order: `-g` flag -> `OPENSHELL_GATEWAY` env var -> persisted default.

System administrators can seed read-only gateway entries for
package-managed setups at `/etc/openshell` (configurable via
`OPENSHELL_SYSTEM_GATEWAY_DIR`), enabling pre-configured gateway
lists for enterprise environments.

### Multi-tenancy (open gap)

Multi-tenancy remains an open question (OpenShell #1722). Neither
OpenShell nor Kagenti implemented multi-tenancy. Key sub-questions:
tenant model, isolation boundaries, namespace strategy, shared gateway
configuration per namespace/team.

The RHOAI recommendation from the executive summary is:
namespace-level tenant boundaries + OpenShell per-agent sandboxing +
shared gateway with tenant-scoped policy + optional vCluster Private
Nodes for regulated workloads.

### Hybrid cloud considerations

For hybrid deployments (on-prem + cloud), the practical pattern is
separate gateway instances per environment, with users registered
against multiple gateways. The inference routing architecture supports
this -- each gateway can point at different model endpoints (on-prem
vLLM vs. cloud API), and the credential injection pattern means agents
do not need environment-specific configuration.

The "unconditional rewrite" pattern for multi-tenancy (proxy always
substitutes correct tenant ID) extends naturally to hybrid: the proxy
rewrites provider credentials based on the gateway's configuration,
not the agent's environment.

## Key findings that extend existing knowledge

1. **Sidecar topology is real and configurable** (Topology B). The Helm
   chart exposes `supervisor.topology=sidecar` with strict/relaxed
   modes. This was described as future in the architecture lens but is
   now a shipping Helm value.

2. **User namespace support is implemented** in the Helm chart
   (`server.enableUserNamespaces=true`). Combined with K8s 1.33+ user
   namespace support, this is a concrete path to eliminating the
   privileged SCC -- not just a theoretical mitigation.

3. **Layered sandboxing validated on OpenShift 4.21.** The dual
   OpenShell + Kata topology stops both application-layer and
   kernel-level attacks. Published in Red Hat Developer (Jul 2026).

4. **The Postgres backend decision** (Jul 2026) aligns the Dev Preview
   with the Helm chart's external database path, enabling multi-replica
   deployments from day one.

5. **OpenShell #899 tracks restricted SCC support** specifically, beyond
   the general privileged SCC question. The user namespace path and
   sidecar topology are both enablers.

6. **FIPS Phase 1 design is specified** (OpenShell #900) with
   feature-flagged aws-lc-rs backend, algorithm restrictions, and
   explicit documentation of the SSH validation gap. Build toolchain
   impact (CMake + Go) is identified.

7. **No official air-gap deployment path exists.** The practical
   approach (image/chart mirroring + internal model endpoints) works
   but is undocumented.

8. **Gateway API GRPCRoute is the ingress standard,** not Kubernetes
   Ingress resources. This is important for OpenShift, where Routes are
   the default but GRPCRoute with Envoy Gateway is the documented path.

9. **Envoy Gateway OIDC must NOT be enabled** alongside OpenShell OIDC.
   OpenShell validates bearer tokens in gRPC metadata; Envoy's OIDC
   relies on browser redirects incompatible with CLI/headless agents.

## Sources

### NVIDIA OpenShell documentation
- [OpenShell overview](https://docs.nvidia.com/openshell/latest)
- [Quickstart](https://docs.nvidia.com/openshell/latest/get-started/quickstart)
- [Installation](https://docs.nvidia.com/openshell/latest/about/installation)
- [Gateways and Sandboxes](https://docs.nvidia.com/openshell/latest/sandboxes/manage-gateways)
- [Kubernetes setup](https://docs.nvidia.com/openshell/kubernetes/setup)
- [OpenShift](https://docs.nvidia.com/openshell/kubernetes/openshift)
- [Ingress](https://docs.nvidia.com/openshell/kubernetes/ingress)
- [Access control](https://docs.nvidia.com/openshell/kubernetes/access-control)
- [Inference routing](https://docs.nvidia.com/openshell/latest/sandboxes/inference-routing)
- [Security best practices](https://docs.nvidia.com/openshell/latest/security/best-practices)
- [Support matrix](https://docs.nvidia.com/openshell/reference/support-matrix)
- [Default policy](https://docs.nvidia.com/openshell/latest/reference/default-policy)

### GitHub
- [OpenShell Helm chart README](https://github.com/NVIDIA/OpenShell/blob/main/deploy/helm/openshell/README.md)
- [OpenShell #900: FIPS 140-3 compliance path](https://github.com/NVIDIA/OpenShell/issues/900)
- [OpenShell #899: Restricted SCC support](https://github.com/NVIDIA/OpenShell/issues/899)
- [OpenShell #1305: Crate decomposition](https://github.com/NVIDIA/OpenShell/issues/1305)
- [OpenShell #981: Split supervisor and agent pods](https://github.com/NVIDIA/OpenShell/issues/981)
- [OpenShell #1722: Multi-tenancy requirements](https://github.com/NVIDIA/OpenShell/issues/1722)
- [OpenShell #1959: Sandbox user elimination](https://github.com/NVIDIA/OpenShell/issues/1959)
- [NemoClaw #2218: Air-gapped deployment](https://github.com/NVIDIA/NemoClaw/issues/2218)
- [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox)

### Red Hat
- [Layered sandboxing for AI agents: OpenShift and OpenShell](https://developers.redhat.com/articles/2026/07/16/layered-sandboxing-ai-agents-openshift-and-openshell) (Jul 2026)
- [Red Hat build of Agent Sandbox docs](https://docs.redhat.com/en/documentation/openshift_sandboxed_containers/1.12/html/deploying_red_hat_build_of_agent_sandbox/index)
- [opendatahub-io/opendatahub-operator](https://github.com/opendatahub-io/opendatahub-operator) (DSC integration patterns)

### Hub knowledge entries (not repeated, extended)
- fact-openshell-architecture.md -- Topology A/B/C definitions
- fact-openshell-openshift-deployment.md -- Helm install, SCC, mTLS/OIDC
- question-openshell-privileged-scc.md -- Elevated privilege requirements
- question-openshell-rust-fips.md -- FIPS compliance gap
- question-openshell-sku-product-home.md -- SKU/delivery vehicle decision
- question-openshell-multi-tenancy.md -- Multi-tenancy gap
- ref-rhaistrat-1752-openshell-operator.md -- Operator productization
- decision-openshell-dp-postgres.md -- Postgres backend for DP
- decision-openshell-base-image-dual-path.md -- Hummingbird + UBI/RHEL
- 00-executive-summary.md -- Strategic synthesis across lenses 01-06
