---
title: "Operations Lens: Day-2 Operations for OpenShell on RHOAI"
description: Practical operational guide covering gateway administration, credential lifecycle, certificate management, policy lifecycle, upgrades, sandbox lifecycle, warm pools, observability, troubleshooting, and multi-tenancy for OpenShell in production.
timestamp: 2026-07-27
lens: operations
review_after: 2026-09-27
---

# Operations Lens: Day-2 Operations for OpenShell on RHOAI

This document covers the practical day-2 operational model for OpenShell
in production on RHOAI. It extends the existing research series (01-06,
dated 2026-07-11) which covers strategic and architectural depth. This
lens focuses on HOW to operate -- the procedures, tools, failure modes,
and gaps an operations team will encounter.

All content reflects the state of OpenShell as of July 2026 (Helm chart
0.0.85-0.0.91 era, pre-GA). The Helm chart is explicitly marked
**experimental and under active development** by NVIDIA.

---

## 1. Gateway administration

### 1.1 What the gateway is

The gateway is the control plane for OpenShell. All control-plane traffic
between the CLI and sandboxes flows through it. Core responsibilities:

- Provisioning and managing sandboxes (creation, deletion, status)
- Storing provider credentials and delivering them at sandbox startup
- Delivering network and filesystem policies to sandboxes
- Managing inference configuration and routing
- Providing SSH tunnel endpoints for sandbox connectivity
- Minting sandbox JWTs for supervisor authentication

### 1.2 Deployment model

On Kubernetes, the gateway deploys via an OCI-based Helm chart from
`oci://ghcr.io/nvidia/openshell/helm-chart`. Two workload modes:

| Mode | Backend | Use case |
|------|---------|----------|
| StatefulSet (default) | SQLite on PVC | Single-replica evaluation |
| Deployment | External PostgreSQL | Multi-replica production |

Switch to Deployment mode by setting `workload.kind=deployment` and
providing `server.externalDbSecret` pointing to a Secret with a
PostgreSQL URI in the `uri` key.

**RHOAI note**: The DP decision (2026-07-17) confirmed Postgres as the
backend database for dev preview.

### 1.3 Configuration hierarchy

```
Gateway CLI flag > OPENSHELL_* env var > TOML file > built-in default
```

The gateway reads TOML from `--config`, `OPENSHELL_GATEWAY_CONFIG`, or
`$XDG_CONFIG_HOME/openshell/gateway.toml`. The `database_url` setting
is environment-only -- the loader rejects it in TOML files.

Key gateway-wide settings (`[openshell.gateway]`):

| Setting | Default | Purpose |
|---------|---------|---------|
| `bind_address` | `0.0.0.0:8080` | Main listener |
| `health_bind_address` | `0.0.0.0:8081` | Health probes |
| `metrics_bind_address` | `0.0.0.0:9090` | Prometheus metrics |
| `log_level` | `info` | Logging verbosity |
| `sandbox_namespace` | `openshell` | Default sandbox namespace |
| `ssh_session_ttl_secs` | `3600` | SSH session TTL |
| `compute_drivers` | auto-detect | Kubernetes > Podman > Docker |
| `disable_tls` | `false` | Plaintext mode (dev only) |

### 1.4 Health checks

The gateway exposes two health endpoints on the health port:

| Probe | Endpoint | What it checks |
|-------|----------|----------------|
| startup + liveness | `/healthz` | Process liveness |
| readiness | `/readyz` | Database connectivity (background check) |

From the CLI:

```shell
openshell status              # reachability + auth check
openshell status --output json  # machine-readable
openshell gateway info        # compute drivers, driver versions
```

`openshell status` performs two separate checks: a public health RPC
(connectivity + gateway version) and a protected gateway-info query
(credential validation). An expired bearer token shows "Connected" but
"Authentication: Failed".

### 1.5 Scaling and high availability

**Current state**: `replicaCount` defaults to 1. Multi-replica with
StatefulSet requires explicit opt-in via
`workload.allowMultiReplicaStatefulSet`. For production multi-replica,
use Deployment mode with external PostgreSQL.

**Gaps (extends existing knowledge)**:
- **No documented HA pattern.** GitHub issue #1012 ("High-availability
  Kubernetes Support") is open with no resolution.
- **No leader election.** The gateway does not document leader election
  for multi-replica deployments, meaning there is no documented path to
  active-active or active-passive HA.
- **No horizontal pod autoscaler guidance.** No docs on HPA
  configuration, resource requests/limits recommendations, or scaling
  triggers.

**RHOAI implication**: For DP/TP, single-replica with Postgres is
likely sufficient. GA will need an HA story -- this is a gap that needs
upstream engagement or downstream engineering.

### 1.6 gRPC rate limiting

The gateway supports per-client rate limiting:

| Setting | Default | Purpose |
|---------|---------|---------|
| `grpc_rate_limit_requests` | unset | Request count per window |
| `grpc_rate_limit_window_seconds` | unset | Window duration |

Both must be positive to enable. Set either to 0 or omit both to
disable.

---

## 2. Provider and credential lifecycle

### 2.1 Provider model

Providers are first-class entities storing credentials for external
services. The agent process inside a sandbox never sees real credential
values -- an opaque placeholder is used and resolved by the proxy at
network egress.

### 2.2 Credential injection mechanism

At sandbox startup, the proxy replaces each credential with a
placeholder token in the agent's environment. When the agent sends an
HTTP request containing that placeholder, the proxy resolves it to the
real value before forwarding upstream.

Supported injection locations: header values (including Bearer and Basic
auth), query parameter values, and URL path segments. The proxy does NOT
modify request bodies (unless `request_body_credential_rewrite: true` is
set for REST endpoints), cookies, or response content.

Fail-closed: if the proxy detects an unresolvable placeholder, it
rejects the request with HTTP 500 rather than forwarding the raw
placeholder upstream.

### 2.3 Creating and managing providers

```shell
# From environment variables
openshell provider create --name my-claude --type claude --from-existing

# Explicit credential
openshell provider create --name my-api --type generic --credential API_KEY=sk-abc123

# Runtime credentials (gateway-minted, e.g., AWS STS)
openshell provider create --name my-aws --type aws-s3 --runtime-credentials
```

Management commands:

| Command | Purpose |
|---------|---------|
| `openshell provider list` | List all providers (values never shown) |
| `openshell provider get <name>` | Inspect one provider |
| `openshell provider update <name> --from-existing` | Rotate from env |
| `openshell provider update <name> --credential KEY=VALUE` | Explicit rotation |
| `openshell provider delete <name>` | Remove provider |

### 2.4 Credential rotation

Two rotation paths:

**Manual rotation**: `openshell provider update` with new credential
values. Set expiry timestamps with `--credential-expires-at KEY=TIMESTAMP`.
Use `0` to clear expiry.

**Automated refresh**: The gateway can mint tokens for:
- OAuth2 refresh token
- OAuth2 client credentials
- Google service account JWT
- AWS STS AssumeRole (requires `providers_v2_enabled=true`)

```shell
# Configure automated refresh
openshell provider refresh configure my-graph \
  --credential-key MS_GRAPH_ACCESS_TOKEN \
  --strategy oauth2-client-credentials \
  --material tenant_id="$TENANT_ID" \
  --material client_id="$CLIENT_ID" \
  --secret-material-env client_secret=CLIENT_SECRET

# Force immediate rotation
openshell provider refresh rotate my-graph --credential-key MS_GRAPH_ACCESS_TOKEN

# Check refresh status
openshell provider refresh status my-graph
```

The `--secret-material-env` flag reads values from the CLI's own
environment so the secret never appears in the host process table.

**Expired credential behavior**: OpenShell skips expired provider
credentials when building a sandbox provider environment. Running
sandboxes also reject expired credential generations during placeholder
resolution, ensuring stale placeholders fail closed.

### 2.5 External secret store integration

**Gap: No native Vault, cloud KMS, or external-secrets-operator
integration exists.** Credentials are stored in the gateway's database
(SQLite or PostgreSQL). The only external credential mechanisms are:

- Kubernetes Secrets (for the mTLS bundle and provider YAML in Helm
  deployments)
- OAuth2/OIDC token refresh (gateway-managed)
- AWS STS AssumeRole (gateway-managed)
- SPIFFE Workload API for dynamic token grants (via
  `provider_spiffe_workload_api_socket_path`)

For enterprise deployments needing Vault or cloud KMS integration, the
current path is to inject credentials via environment variables or
Kubernetes Secrets into the gateway pod, then register them as providers.

### 2.6 Providers v2

Providers v2 (enabled via `providers_v2_enabled=true`) adds:

- Provider profiles (reusable provider type definitions)
- Network policy composition (providers contribute policy entries
  automatically)
- Runtime attach/detach of providers to running sandboxes
- Provider-scoped endpoint rules (`_provider_*` policy entries)

Key operational difference: with v2, `--from-existing` uses
profile-backed discovery. If no matching profile exists, the command
fails rather than falling back.

**Runtime limitation**: Attaching/detaching providers affects future
process launches. Already-running processes keep the environment they
started with. Long-running processes needing new credentials must be
restarted.

---

## 3. Certificate management

### 3.1 Two provisioning modes

| Mode | Description | Rotation |
|------|-------------|----------|
| Built-in `pkiInitJob` (default) | Pre-install Helm Job generates self-signed CA + certs | Manual (redeploy) |
| cert-manager | cert-manager controller owns TLS lifecycle | Automatic before expiry |

When `certManager.enabled=true`, cert-manager owns TLS certificate
generation even if `pkiInitJob.enabled` remains true.

### 3.2 What gets generated

The chart provisions a complete PKI chain: a self-signed CA, server
certificate (for the gateway listener), and client certificate (for
sandbox supervisor mTLS transport). The mTLS bundle is for transport
security between gateway and supervisors -- not for user authentication.

### 3.3 cert-manager integration

```shell
# Install cert-manager
helm install cert-manager oci://quay.io/jetstack/charts/cert-manager \
  --namespace cert-manager --create-namespace \
  --set crds.enabled=true --wait

# Enable in OpenShell
helm upgrade --install openshell ... --set certManager.enabled=true
```

cert-manager handles automatic renewal before expiry.

### 3.4 JWT signing secret

Even under cert-manager mode, the chart runs a JWT-only initialization
hook because cert-manager cannot create the sandbox JWT signing Secret.
This Secret is separate from TLS certificates and is mounted at
`/etc/openshell-jwt`. Settings:

| Setting | Default | Purpose |
|---------|---------|---------|
| `gateway_jwt.ttl_secs` | 3600 (Helm default) | Sandbox JWT lifetime |
| `gateway_jwt.gateway_id` | `openshell` | Gateway identifier in tokens |

When `ttl_secs` is 0, tokens do not expire -- only for local
single-player gateways. The gateway logs a warning when Kubernetes
uses 0.

### 3.5 CLI-side certificate layout

```
~/.config/openshell/gateways/<name>/
  metadata.json          # endpoint, auth mode
  mtls/
    ca.crt               # CA certificate
    tls.crt              # Client certificate
    tls.key              # Client private key
  oidc_token.json        # OIDC tokens (owner-only perms)
```

Extracting the mTLS bundle from Kubernetes:

```shell
kubectl -n openshell get secret openshell-client-tls \
  -o jsonpath='{.data.ca\.crt}' | base64 -d > ca.crt
# (similarly for tls.crt and tls.key)
```

### 3.6 OIDC changes to the cert story

With OIDC enabled, mTLS remains for transport security but user
authentication shifts to JWT validation. The gateway validates tokens
against the issuer's JWKS endpoint with configurable cache TTL
(`jwks_ttl_secs`, default 3600). Token refresh is handled by the CLI
automatically when a refresh token exists.

**RHOAI implication**: OIDC is the recommended path for multi-user RHOAI
deployments. The cert-manager integration handles transport cert
rotation. User credential rotation is delegated to the IdP
(Keycloak/Entra ID/Okta).

---

## 4. Policy lifecycle

### 4.1 Policy structure

Policies have two categories:

**Static sections** (locked at sandbox creation, require destroy + recreate):
- `filesystem_policy` -- Landlock LSM path restrictions
- `landlock` -- compatibility mode (`best_effort` or `hard_requirement`)
- `process` -- `run_as_user`, `run_as_group`, seccomp

**Dynamic sections** (hot-reloadable on running sandboxes):
- `network_policies` -- named blocks of endpoints, binaries, protocols
- `network_middlewares` -- HTTP request middleware configurations

### 4.2 Creating sandboxes with policies

```shell
# Explicit policy file
openshell sandbox create --policy ./my-policy.yaml -- claude

# Default policy via environment
export OPENSHELL_SANDBOX_POLICY=./my-policy.yaml
openshell sandbox create -- claude
```

### 4.3 Hot-reload mechanics

Dynamic sections update via two commands:

| Command | Behavior |
|---------|----------|
| `openshell policy update` | Incremental merge into `network_policies` |
| `openshell policy set` | Full replacement of all dynamic sections |

When hot-reload changes rules on an active HTTP L7 endpoint, existing
keep-alive tunnels close before forwarding the next parsed request. Most
HTTP clients reconnect automatically.

**Raw streams are connection-scoped and outside L7 live-reload
guarantees.** This covers `tls: skip`, non-HTTP TCP payloads, HTTP
upgrades like WebSocket, and long-lived response streams like SSE.

Multiple flags in one `policy update` command apply as one atomic merge
batch, producing at most one new revision. They succeed or fail
together.

When two updates race, the gateway uses optimistic retry: it fetches the
latest revision, reapplies the full batch, validates, and retries the
write.

### 4.4 Policy versioning and rollback

```shell
# List revisions
openshell policy list <name>

# Inspect a stored revision
openshell policy get <name> --rev <version>

# View base policy (user-authored, without provider entries)
openshell policy get <name> --base > current-policy.yaml

# View full effective policy (base + provider layers)
openshell policy get <name> --full
```

Rollback is manual: retrieve a previous revision with `--rev`, then
apply it with `policy set`.

**Gap: No first-class rollback command exists.** The operator must
manually export a previous revision and re-apply it.

### 4.5 Global policy override

```shell
# Apply one policy to every sandbox
openshell policy set --global --policy ./global-policy.yaml

# Remove global override
openshell policy delete --global
```

While a global policy is active, sandbox-level policy updates are
rejected. This is the enforcement mechanism for fleet-wide compliance
policies.

### 4.6 L7 protocol support

Six protocols are supported in policy rules:

| Protocol | CLI support | YAML-only | Inspection capability |
|----------|-------------|-----------|----------------------|
| `rest` | Yes | -- | HTTP method/path, query params |
| `websocket` | Yes | -- | RFC 6455 upgrade + client text messages |
| `sql` | Yes | -- | -- |
| `graphql` | -- | Yes | Operation type/name/fields |
| `mcp` | -- | Yes | MCP Streamable HTTP methods/tools |
| `json-rpc` | -- | Yes | JSON-RPC 2.0 method matching |

MCP and JSON-RPC require full YAML via `policy set` -- the incremental
update parser does not accept these protocols.

### 4.7 Policy Advisor (RFC 0002)

The Policy Advisor enables agents to request narrow network policy
changes after a denial. It follows an audit2allow-style workflow:

1. Agent makes a request that policy denies
2. OpenShell returns a structured 403 with `agent_guidance` and
   `next_steps`
3. Agent reads the policy advisor skill and submits an `addRule` proposal
   to `http://policy.local/v1/proposals`
4. Gateway stores the proposal as a pending draft chunk and runs the
   policy prover
5. Developer approves or rejects from outside the sandbox

Two approval modes:

| Mode | Clean proposals | Proposals with findings |
|------|-----------------|------------------------|
| `manual` (default) | Draft inbox for human review | Draft inbox |
| `auto` (opt-in) | Auto-approved, hot-reload | Still pending for human review |

Auto-approval requires all three conditions: effective mode is `auto`,
prover delta is empty, and no security notes.

The policy prover checks four formal categories:
- `link_local_reach` -- rule reaches link-local or metadata endpoints
- `l7_bypass_credentialed` -- binary bypasses L7 inspection on a
  credentialed host
- `credential_reach_expansion` -- binary gains credentialed reach to new
  host:port
- `capability_expansion` -- new HTTP method on existing credentialed
  reach

Every auto-approval emits a `CONFIG:APPROVED` event with
`auto=true` for full audit trail.

### 4.8 Compliance policy templates

**Gap: No pre-built compliance policy templates exist (SOC2, HIPAA,
FedRAMP).** This was identified as gap G14 in the jira-gap lens (06).
The Policy Advisor provides the mechanism, but no reference compliance
policies ship with OpenShell. This is a white space opportunity for
RHOAI (identified in the executive summary as opportunity #3).

---

## 5. Upgrade paths

### 5.1 Helm chart upgrades

```shell
helm upgrade --install openshell \
  oci://ghcr.io/nvidia/openshell/helm-chart \
  --version <version> \
  --namespace openshell \
  --values my-values.yaml
```

Key behaviors during upgrade:
- PKI secrets generated on first install persist across upgrades
  (pre-install hooks are idempotent)
- Existing sandboxes keep running during the upgrade and remain
  manageable after gateway restart
- After upgrading Agent Sandbox (controller + CRD rollout), restart the
  OpenShell gateway to re-detect API versions

### 5.2 Breaking change risk

**The Helm chart is explicitly marked experimental.** Templates, values,
and defaults can change between releases. There is:

- **No documented migration guide** between chart versions
- **No changelog with breaking change annotations** in the chart itself
- **No CRD version migration documentation** for the Agent Sandbox SIG
  CRDs
- **No compatibility matrix** between OpenShell chart versions and Agent
  Sandbox controller versions

**RHOAI implication**: For the DP-to-TP-to-GA path, Red Hat needs to
track and document breaking changes, provide migration guides, and
potentially backport stability patches. The current upstream release
cadence is rapid (0.0.x with no semver stability guarantees).

### 5.3 Agent Sandbox CRD versioning

The Agent Sandbox SIG ships v1beta1 CRDs (Sandbox, SandboxTemplate,
SandboxClaim, SandboxWarmPool). OpenShell detects and caches the served
Sandbox API version at gateway startup. After a CRD version change,
restart the gateway.

**Gap: No documented CRD migration path exists for v1beta1 to v1.**
When the Agent Sandbox SIG promotes to v1, there will be a CRD
migration required. The timeline is not public.

### 5.4 Rollback

**Gap: No documented rollback procedure exists.** `helm rollback` should
work for chart-level rollback, but database schema changes (if any) are
not documented. For the SQLite backend, the PVC may contain schema
changes that are not backward-compatible. For PostgreSQL, no migration
tooling is documented.

---

## 6. Sandbox lifecycle

### 6.1 Lifecycle phases

| Phase | Description |
|-------|-------------|
| Provisioning | Runtime setup, credential injection, policy application |
| Ready | Sandbox running, agent active, isolation enforced |
| Error | Provisioning or execution failure |
| Deleting | Teardown, resource release, credential purge |

### 6.2 Creation

```shell
# Basic
openshell sandbox create -- claude

# With resources
openshell sandbox create --cpu 2 --memory 4Gi -- claude

# With GPU
openshell sandbox create --gpu 2 -- claude

# With providers, policy, labels, env vars, uploads
openshell sandbox create \
  --provider my-claude \
  --policy ./policy.yaml \
  --label env=dev \
  --env DEBUG=1 \
  --upload ./src:/workspace/src \
  -- claude
```

CPU values follow Kubernetes-style quantities (e.g., `500m`, `2.5`).
Memory uses byte quantities (`512Mi`, `4Gi`). On Kubernetes, these
set both request and limit.

### 6.3 Monitoring and status

```shell
# List all sandboxes
openshell sandbox list
openshell sandbox list --selector env=dev   # filter by label

# Detailed info (policy source, revision, active policy)
openshell sandbox get my-sandbox
openshell sandbox get my-sandbox --output json

# Policy-only output
openshell sandbox get my-sandbox --policy-only

# Log streaming
openshell logs my-sandbox --tail --source sandbox --level warn --since 5m

# Real-time TUI dashboard
openshell term
```

The TUI (`openshell term`) displays three panels: Gateways,
Providers/Global Settings, and Sandboxes. It shows blocked connections
(`action=deny`) and proxy activity in real time.

### 6.4 Deletion and cleanup

```shell
openshell sandbox delete my-sandbox
```

Deletion stops all processes, releases resources, and purges injected
credentials.

**Gap: No automated garbage collection exists.** There is no mechanism
to automatically clean up idle sandboxes, no TTL-based expiration, and
no orphan detection. Sandbox cleanup is entirely manual via
`sandbox delete`.

**RHOAI implication**: For multi-tenant production deployments,
automated cleanup will be essential. This should be part of the operator
or a sidecar controller. The SandboxWarmPool provides pre-provisioning
but not cleanup.

### 6.5 Resource limits and quotas

Per-sandbox CPU, memory, and GPU limits are set at creation time. On
Kubernetes, these translate directly to pod resource requests/limits.

**Gap: No namespace-level or tenant-level quota enforcement exists
within OpenShell.** Kubernetes ResourceQuotas apply at the namespace
level, but OpenShell provides no quota management layer on top. There is
no per-user sandbox count limit, no aggregate resource cap, and no
cost attribution.

### 6.6 File transfer

```shell
# Upload (respects .gitignore by default)
openshell sandbox upload my-sandbox ./src /sandbox/src

# Download (restricted to /sandbox, symlink escape protection)
openshell sandbox download my-sandbox /sandbox/output ./local
```

### 6.7 Service forwarding and port forwarding

```shell
# Expose a service through the gateway
openshell service expose my-sandbox 8080

# Port-forward a local port
openshell forward start 8000 my-sandbox
openshell forward start 8000 my-sandbox -d  # background
```

---

## 7. Warm pools

### 7.1 Agent Sandbox SIG warm pool model

The SandboxWarmPool CRD (kubernetes-sigs/agent-sandbox) pre-provisions a
pool of ready sandbox pods. When a new sandbox is needed, a
SandboxClaim requests a ready Sandbox from the pool. If a warm pod
exists, ownership is transferred in under 100 milliseconds. The pool
then replenishes.

### 7.2 Controller tuning parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `--sandbox-warm-pool-concurrent-workers` | 1 | Max concurrent reconciles |
| `--sandbox-warm-pool-max-batch-size` | 300 | Max sandboxes per create/delete batch |
| `--kube-api-qps` | -1 (no limit) | API client QPS |
| `--kube-api-burst` | 10 | API client burst |

### 7.3 OpenShell integration status

**Significant active work, not yet shipped.** GitHub issues show a
multi-issue warm pool effort:

- #1447: Warm pool support for OpenShell sandboxes (open)
- #2157: Warm-pool provisioning for Kubernetes sandboxes (open)
- #2460: SandboxClaims for matching warm pools (open)
- #1892: Warm-pooled sandboxes via agent-sandbox extension CRDs (open)
- #1879: Warm-pooled sandboxes for the Kubernetes compute driver (open)
- #2199: Warm Pool Feasibility Study (closed -- study completed)

The feasibility study (#2199) has been completed, suggesting the
architecture is understood. The implementation issues are open and
active.

**RHOAI implication**: Warm pool support is critical for production
agent workloads with latency requirements. The jira-gap lens flagged
this as gap G17 (medium severity). There is no RHAISTRAT tracking
downstream integration. If warm pool support ships upstream before
RHOAI 3.7, it should be included in the GA scope.

### 7.4 Cold start characteristics

**Gap: No published cold start metrics exist.** The warm pool goal is
sub-100ms assignment. Without warm pools, sandbox creation time depends
on:
- Image pull time (mitigated by `IfNotPresent` policy and pre-pulling)
- Pod scheduling time
- Supervisor bootstrap time (namespace setup, Landlock, seccomp)
- Credential injection and policy application

No benchmarks or SLA targets are published for any of these phases.

---

## 8. Monitoring and observability

### 8.1 Logging architecture

OpenShell produces a unified log stream combining two formats:

**Standard tracing** (Rust `tracing` framework):
```
2026-04-01T03:28:39.160Z INFO openshell_sandbox: Starting sandbox
```

**OCSF structured events** (seven event classes):
```
2026-04-01T04:04:32.118Z OCSF NET:OPEN [INFO] ALLOWED /usr/bin/curl(58) -> api.github.com:443 [policy:github_api engine:opa]
```

| Event class | Class UID | Covers |
|-------------|-----------|--------|
| Network Activity (`NET:`) | 4001 | TCP tunnels, DNS, SSRF blocks |
| HTTP Activity (`HTTP:`) | 4002 | HTTP requests, L7 enforcement |
| SSH Activity (`SSH:`) | 4007 | Handshakes, channels |
| Process Activity (`PROC:`) | 1007 | Process start/exit/timeout |
| Detection Finding (`FINDING:`) | 2004 | Nonce replay, bypass detection |
| Device Config State Change (`CONFIG:`) | 5019 | Policy load/reload, Landlock |
| Application Lifecycle (`LIFECYCLE:`) | 6002 | Supervisor start, SSH ready |

Severity tiers: `[INFO]`, `[LOW]`, `[MED]`, `[HIGH]`, `[CRIT]`,
`[FATAL]`.

### 8.2 Log access methods

| Method | Source | Completeness | Persistence |
|--------|--------|-------------|-------------|
| CLI (`openshell logs`) | Gateway gRPC buffer | May drop under load | In-memory only |
| TUI (`openshell term`) | Gateway gRPC buffer | Same as CLI | In-memory only |
| Filesystem (`/var/log/openshell.*.log`) | Sandbox-local files | Complete record | On sandbox disk |
| OCSF JSON export | Structured JSONL files | Structured subset | On sandbox disk |

**Important**: The gateway maintains a bounded buffer of recent log
lines per sandbox. This buffer is NOT persisted to disk and is lost on
gateway restart. The in-sandbox files are the complete record. The gRPC
push channel drops events rather than blocking.

Log files rotate daily, retaining the three most recent files.

### 8.3 OCSF JSON export

Enable structured OCSF JSONL export for SIEM integration:

```shell
# Global enable
openshell settings set --global --key ocsf_json_enabled --value true

# Per-sandbox enable
openshell settings set my-sandbox --key ocsf_json_enabled --value true
```

Changes activate on the next poll cycle (default: every 10 seconds),
no restart needed. Output: `/var/log/openshell-ocsf.YYYY-MM-DD.log`
inside the sandbox, OCSF v1.7.0 compliant.

SIEM integration:

| Tool | Method |
|------|--------|
| Splunk | Splunk OCSF Add-on (Splunkbase) |
| Amazon Security Lake | OCSF is the native schema |
| Elastic | Filebeat with OCSF field mappings |
| Custom | `jq`, Python, or any JSON tooling |

### 8.4 Metrics

The gateway config exposes a `metrics_bind_address` (default
`0.0.0.0:9090`) for Prometheus scraping.

**Gap: Metrics instrumentation is minimal and actively being developed.**
Key GitHub issues:

- #909: "feat(server): metrics instrumentation" (open)
- #1270: "feat(observability): add gateway OTLP traces and initial Kube
  monitoring surface" (closed -- some work shipped)
- #1119: "feat: pre-register prometheus metrics at startup so /metrics
  is never empty" (closed -- shipped)

The `/metrics` endpoint exists and is pre-registered, but the breadth
of emitted metrics is not documented. No Grafana dashboards ship with
OpenShell. No alerting rules are published.

**RHOAI implication**: For TP/GA, RHOAI will need to build or curate
Grafana dashboards and Prometheus alerting rules. The upstream metrics
surface is still evolving. This should be tracked as a downstream
engineering task.

### 8.5 OpenTelemetry integration

**Partially implemented, actively tracked.**

- #1758: "Add OpenTelemetry trace correlation across gateway activity"
  (open)
- #1818: "Add optional OpenTelemetry tracing hooks to the Python SDK"
  (open)
- #1055: "Enterprise Observability" (open -- umbrella issue)
- #1922: "feat(observability): investigate portable sandbox log
  collection" (open)

The capability gaps fact (from the existing knowledge base) notes that
Kagenti auto-wired MLflow experiments + RBAC, while OpenShell can set
OTEL env vars but has nothing built-in. This remains accurate.

**RHOAI implication**: The jira-gap lens identified MLflow/OTEL tracing
integration as gap G10 (medium severity). No RHAISTRAT exists for this.
RHOAI should file a downstream tracking feature for observability
integration.

### 8.6 Filtering and analysis patterns

Useful `grep` patterns for OCSF log files inside sandboxes:

| Goal | Pattern |
|------|---------|
| All denied connections | `grep "DENIED\|BLOCKED"` |
| All network events | `grep "OCSF NET:"` |
| L7 enforcement decisions | `grep "OCSF HTTP:"` |
| Security findings | `grep "OCSF FINDING:"` |
| Policy changes | `grep "OCSF CONFIG:"` |
| Medium severity and above | `grep "\[MED\]\|\[HIGH\]\|\[CRIT\]\|\[FATAL\]"` |

For OCSF JSON, extract denied connections:
```shell
cat /var/log/openshell-ocsf.*.log | jq -c 'select(.action == "Denied")'
```

---

## 9. Troubleshooting patterns

### 9.1 Diagnostic commands

| Command | Purpose |
|---------|---------|
| `openshell status` | Gateway reachability + auth check |
| `openshell status -g <name>` | Check a non-active gateway |
| `openshell gateway info` | Runtime details, compute drivers |
| `openshell doctor check` | Docker environment diagnostics |
| `openshell logs <name> --tail --source sandbox` | Stream sandbox logs |
| `openshell term` | Real-time TUI dashboard |
| `openshell sandbox get <name>` | Sandbox policy source + revision |

### 9.2 Gateway connectivity failures

**"Connected" but "Authentication: Failed"**: Expired bearer token.
Fix: `openshell gateway login <name>`.

**"Authorization: Unverified"**: Older gateway lacking capability query.
Not a failure -- informational.

**Kubernetes gateway not reachable**:
```shell
kubectl -n openshell get deployment,statefulset,pods
kubectl -n openshell logs deployment/openshell -c openshell-gateway --tail=100
kubectl -n openshell get events --sort-by=.lastTimestamp
```

### 9.3 Sandbox startup failures

| Driver | Diagnostic focus |
|--------|-----------------|
| Docker | Daemon health, image availability, gateway logs |
| Podman | Socket availability, rootless networking, image availability |
| Kubernetes | Events and sandbox pods in `server.sandboxNamespace` |
| MicroVM | VM driver logs, rootfs availability |

### 9.4 Policy denial debugging

Monitor denials showing host, port, binary, and reason:

```shell
openshell logs <name> --tail --source sandbox
```

Denial reasons:
- `no matching policy` -- OPA found no allow rule
- `resolves to always-blocked address` -- loopback/link-local
- `resolves to <ip> which is not in allowed_ips` -- IP outside allowlist
- `DNS resolution failed` -- resolution failure
- `port <n> is a blocked control-plane port` -- etcd/K8s API/kubelet
- `request-target contains an encoded '/'` -- encoded slash rejected
- `l7 deny` -- L7 policy rule denial

Proxy error response bodies contain machine-readable codes:
`policy_denied`, `middleware_denied`, `middleware_failed`,
`ssrf_denied`, `upstream_unreachable`.

### 9.5 Landlock failures

Landlock events in logs:
- `CONFIG:LOADED` with `[abi:v2 compat:BestEffort ro:4 rw:2]` -- normal
- `CONFIG:*` with `[MED]` -- inaccessible path in best-effort mode
  (degraded isolation)
- Detection Finding at `[HIGH]` -- Landlock unavailable (pre-5.13
  kernel)

In `hard_requirement` mode, inaccessible paths cause sandbox startup
failure.

### 9.6 FIPS-related failures

**Extends existing knowledge**: OpenShell is Rust (rustls + ring). No
FIPS path exists today. aws-lc-rs proposed (OpenShell #900). If a
regulated customer deploys OpenShell and requires FIPS-validated crypto,
there is no workaround -- it simply does not work. The SSH layer has no
FIPS-validated Rust implementation at all.

FIPS 140-2 sunsets September 21, 2026. In-process CMVP status is not a
valid compliance state.

### 9.7 Network namespace issues

OpenShell uses dedicated Linux network namespaces per sandbox. All
traffic routes through a veth pair to the host-side proxy at
`10.200.0.1`. If network namespace setup fails:
- Check that the container runtime supports network namespaces
- On Kubernetes sidecar topology, verify `shareProcessNamespace: true`
- Check seccomp phase ordering -- namespace entry requires privileged
  helpers before seccomp locks down `setns`

### 9.8 Common mistakes (from security best practices)

| Mistake | Impact | Fix |
|---------|--------|-----|
| Omitting `protocol` on REST endpoints | L4-only enforcement | Add `protocol: rest` with rules |
| Using `access: full` | Allows all methods/paths | Use `read-only` or explicit rules |
| Broad binary globs (`/**`) | Any binary reaches endpoint | Scope to specific directories |
| Adding inference provider hosts to `network_policies` | Bypasses credential isolation | Always use `inference.local` |
| Jumping to `enforce` without `audit` | Breaks agent workflows | Audit first, enforce after validation |

---

## 10. Multi-tenancy operations

### 10.1 Current state

**Multi-tenancy is not implemented.** This is the single largest
unresolved architectural question (confirmed by the executive summary
and the jira-gap lens as critical gap G3).

The current access control model has exactly two roles:
- `openshell-admin` -- administrative access
- `openshell-user` -- standard user access

There is no per-user sandbox isolation, no per-tenant namespace
scoping, no tenant onboarding/offboarding workflow, and no per-tenant
quota enforcement.

### 10.2 Upstream tracking

- OpenShell #1722: "Multi-tenant deployments" (open)
- OpenShell #1145: "Multi-tenant support roadmap?" (open)
- OpenShell #1795: "Support creating sandbox CRs in a configurable
  target namespace" (open)
- OpenShell #2385: "feat(proxy): namespace- or cluster-shared proxy
  placement" (open, draft RFC)
- OpenShell #2485/#2484: "feat(helm): split gateway and workspace
  namespace charts" (open)

The Helm chart split (#2485) is a prerequisite for namespace-level
tenant isolation -- it separates the gateway chart from the workspace
(sandbox) chart so each tenant namespace can have its own workspace
chart installation.

### 10.3 Recommended operational model (from architecture lens)

The architecture lens recommended: namespace-level tenant boundaries +
OpenShell per-agent sandboxing + shared gateway with tenant-scoped
policy + optional vCluster Private Nodes for regulated workloads. The
"unconditional rewrite" pattern (proxy always substitutes correct
tenant ID) is architecturally stronger than conditional validation.

### 10.4 What operations would need

When multi-tenancy lands, the operational model would require:

- **Tenant provisioning**: Namespace creation, RBAC, network policies,
  resource quotas, provider credentials per tenant
- **Tenant isolation**: Sandbox namespace scoping, policy namespace
  scoping, log isolation
- **Per-tenant quotas**: Sandbox count limits, aggregate CPU/memory/GPU
  caps, storage limits
- **Tenant onboarding/offboarding**: Automated provisioning of all the
  above, credential rotation on offboarding, data cleanup
- **Cost attribution**: Per-tenant resource consumption tracking for
  chargeback

None of these capabilities exist today.

### 10.5 Interim workaround

For DP/TP, the only path to tenant-like isolation is deploying separate
OpenShell gateway instances per tenant, each in its own namespace with
its own RBAC and network policies. This is operationally expensive but
provides hard isolation.

---

## 11. Operational gaps summary

The following operational gaps are significant for RHOAI productization:

| Gap | Severity | Upstream tracking | RHAISTRAT |
|-----|----------|-------------------|-----------|
| No HA / leader election | High | #1012 | None |
| No Vault / external secret store integration | High | None | None |
| No automated sandbox garbage collection | High | None | None |
| No compliance policy templates | Medium | None | None (G14) |
| No Grafana dashboards or alerting rules | Medium | #909 | None |
| No OTEL auto-wiring | Medium | #1758, #1818 | None (G10) |
| No published cold start metrics | Medium | None | None |
| No documented rollback procedure | Medium | None | None |
| No CRD migration guide (v1beta1 to v1) | Medium | None | None |
| No multi-tenancy | Critical | #1722 | None (G3) |
| FIPS not available | Critical | #900 | None (G1) |
| Warm pool not integrated | Medium | #1447 et al. | None (G17) |
| No documented upgrade breaking changes | Medium | None | None |

**New finding (extends existing knowledge)**: The HA gap (#1012) and
the lack of automated garbage collection were not identified in the
prior research series. The HA gap is particularly concerning for
production deployments where the gateway is a single point of failure.

---

## Sources

### NVIDIA OpenShell documentation (GitHub raw, fetched 2026-07-27)
- [docs/sandboxes/manage-gateways.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/sandboxes/manage-gateways.mdx) -- gateway management
- [docs/sandboxes/manage-providers.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/sandboxes/manage-providers.mdx) -- provider management
- [docs/sandboxes/manage-sandboxes.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/sandboxes/manage-sandboxes.mdx) -- sandbox lifecycle
- [docs/sandboxes/policies.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/sandboxes/policies.mdx) -- policy management
- [docs/sandboxes/policy-advisor.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/sandboxes/policy-advisor.mdx) -- Policy Advisor (RFC 0002)
- [docs/sandboxes/providers-v2.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/sandboxes/providers-v2.mdx) -- Providers v2
- [docs/observability/logging.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/observability/logging.mdx) -- logging architecture
- [docs/observability/accessing-logs.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/observability/accessing-logs.mdx) -- log access
- [docs/observability/ocsf-json-export.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/observability/ocsf-json-export.mdx) -- OCSF export
- [docs/reference/gateway-auth.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/reference/gateway-auth.mdx) -- gateway authentication
- [docs/reference/gateway-config.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/reference/gateway-config.mdx) -- gateway configuration
- [docs/reference/support-matrix.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/reference/support-matrix.mdx) -- support matrix
- [docs/security/best-practices.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/security/best-practices.mdx) -- security best practices
- [docs/kubernetes/setup.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/kubernetes/setup.mdx) -- Kubernetes deployment
- [docs/kubernetes/topology.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/kubernetes/topology.mdx) -- sandbox topology
- [docs/kubernetes/managing-certificates.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/kubernetes/managing-certificates.mdx) -- certificate management
- [docs/kubernetes/access-control.mdx](https://github.com/NVIDIA/OpenShell/blob/main/docs/kubernetes/access-control.mdx) -- access control

### OpenShell GitHub issues (searched 2026-07-27)
- [#909](https://github.com/NVIDIA/OpenShell/issues/909) -- metrics instrumentation
- [#1012](https://github.com/NVIDIA/OpenShell/issues/1012) -- HA Kubernetes support
- [#1055](https://github.com/NVIDIA/OpenShell/issues/1055) -- enterprise observability
- [#1145](https://github.com/NVIDIA/OpenShell/issues/1145) -- multi-tenant support roadmap
- [#1270](https://github.com/NVIDIA/OpenShell/issues/1270) -- OTLP traces + Kube monitoring
- [#1447](https://github.com/NVIDIA/OpenShell/issues/1447) -- warm pool support
- [#1722](https://github.com/NVIDIA/OpenShell/issues/1722) -- multi-tenant deployments
- [#1758](https://github.com/NVIDIA/OpenShell/issues/1758) -- OTEL trace correlation
- [#1795](https://github.com/NVIDIA/OpenShell/issues/1795) -- configurable target namespace
- [#1818](https://github.com/NVIDIA/OpenShell/issues/1818) -- OTEL Python SDK hooks
- [#1879](https://github.com/NVIDIA/OpenShell/issues/1879) -- warm-pooled K8s sandboxes
- [#1892](https://github.com/NVIDIA/OpenShell/issues/1892) -- warm pool via extension CRDs
- [#1922](https://github.com/NVIDIA/OpenShell/issues/1922) -- portable sandbox log collection
- [#2157](https://github.com/NVIDIA/OpenShell/issues/2157) -- warm-pool provisioning
- [#2199](https://github.com/NVIDIA/OpenShell/issues/2199) -- warm pool feasibility study
- [#2385](https://github.com/NVIDIA/OpenShell/issues/2385) -- shared proxy placement RFC
- [#2460](https://github.com/NVIDIA/OpenShell/issues/2460) -- SandboxClaims for warm pools
- [#2485](https://github.com/NVIDIA/OpenShell/issues/2485) -- Helm chart namespace split

### Agent Sandbox SIG
- [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox) -- repository
- [Agent Sandbox configuration docs](https://github.com/kubernetes-sigs/agent-sandbox/blob/main/docs/configuration.md) -- controller tuning
- [Agent Sandbox documentation site](https://agent-sandbox.sigs.k8s.io/docs/) -- official docs

### Hub knowledge base (read 2026-07-27)
- `/components/agent-interop/knowledge/fact-openshell-architecture.md`
- `/components/agent-interop/knowledge/fact-openshell-capability-gaps.md`
- `/components/agent-interop/knowledge/fact-openshell-openshift-deployment.md`
- `/components/agent-interop/knowledge/fact-openshell-product-timeline.md`
- `/components/agent-interop/knowledge/decision-openshell-dp-postgres.md`
- `/components/agent-interop/knowledge/decision-openshell-base-image-dual-path.md`
- `/components/agent-interop/research/00-executive-summary.md`
- `/components/agent-interop/research/06-jira-gap.md`
