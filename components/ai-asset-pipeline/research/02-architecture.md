---
title: "AI Asset Pipeline research -- architecture and integration patterns"
description: Cross-asset Konflux pipeline architecture for scanning, signing, attesting, and OCI-packaging skills, MCP servers, and agents alongside models -- parameterized single pipeline, pluggable scan profiles (SkillSpector/Snyk/OWASP MCP Top 10), OCI artifact structures per type, Tekton Chains signing, Conforma policy gating, metadata collection extension, disconnected delivery via oc-mirror, 3-phase implementation path.
timestamp: 2026-08-03
lens: architecture
review_after: 2026-11-03
---

# AI Asset Pipeline research -- architecture and integration patterns

Decision confirmed 2026-08-03 by Adam Bellusci: extend the existing model
trust pipeline, not build new. This document designs the pipeline
extension that handles skills, MCP servers, and agents alongside models.
The reader should be able to write Jira stories from the integration
points and contracts defined here.

## 1. Cross-asset pipeline architecture

### Current model pipeline

```
Source repo push → Konflux clone → prefetch deps → buildah OCI image
  → Tekton Chains signs (cosign) + generates in-toto attestation
  → SBOM generation → Conforma policy gate → push to Quay
  → model-metadata-collection extracts/enriches → catalog YAML
```

ModelCar images are standard container images. Tekton Chains observes
the TaskRun, captures IMAGE_URL and IMAGE_DIGEST results, and
automatically generates SLSA provenance attestations at Build L3.

### Extended multi-asset pipeline

```
Source repo push → Konflux clone → asset type detection
  → dispatch to scan profile (Tekton Pipeline selection)
  → type-specific scan tasks (parallel where possible)
  → OCI packaging (kit pack or custom task)
  → Tekton Chains signs + attests
  → Conforma policy gate (type-aware predicates)
  → push to Quay
  → model-metadata-collection extracts/enriches → catalog YAML
```

### Dispatch mechanism

Detection happens at pipeline selection time, not runtime. Each repo
contains a `.tekton/` directory referencing the appropriate pipeline.

**Recommendation**: parameterized single pipeline with `ASSET_TYPE`
enum (`model|skill|mcp-server|agent`). The parameter gates which scan
tasks run via Tekton `when` expressions. This matches Konflux's
existing pattern of a base pipeline with conditional tasks.

### Shared vs type-specific Tekton tasks

| Task | Shared | Type-specific |
|---|---|---|
| `git-clone` | Yes | - |
| `prefetch-dependencies` | Yes | - |
| `oci-package` | Yes (kit pack) | Config varies per type |
| `sbom-generate` | Yes (syft) | - |
| `scan-skill` | - | Skills only |
| `scan-mcp` | - | MCP servers only |
| `scan-agent` | - | Agents only |
| `scan-container` (existing) | - | Containers/models only |
| `metadata-collect` | Yes | Provider selection by type |
| Tekton Chains signing | Yes (automatic) | - |
| Conforma gate | Yes | Policy rules vary per type |

## 2. Pluggable scan profiles

### Common input/output contract

**Inputs** (workspace + params):
- `source` workspace: cloned repository
- `ASSET_TYPE` param: `skill|mcp-server|agent`
- `ARTIFACT_REF` param: OCI reference (for post-package scanning)

**Outputs** (results + workspace):
- `SCAN_OUTPUT` result: JSON summary following Konflux ADR-0030
- `scan-results` workspace: full SARIF files

SARIF (Static Analysis Results Interchange Format) is the common output.
All scan profiles produce SARIF v2.1.0. SARIF files go into a workspace
(too large for Tekton's 4096-byte result limit) and are attached to the
OCI artifact as a referrer via `cosign attach`.

### Skills scan profile: `scan-skill`

Three layers, as steps within a single Task:

| Step | Tool | What it catches |
|---|---|---|
| 1. Static analysis | SkillSpector (68 patterns, 17 categories) | Prompt injection, data exfiltration, credential access, memory alteration, tool poisoning |
| 2. ML-model scan | Snyk agent-scan (15+ risk categories) | Toxic flows, malware payloads, hardcoded secrets, tool shadowing |
| 3. LLM reviewer | Custom LLM task (optional, gated) | Hidden instructions, intent mismatches, excessive agency |

LLM reviewer only runs for community/partner skills (cost/latency).

### MCP server scan profile: `scan-mcp`

Maps to OWASP MCP Top 10 (MCP01-MCP10):

| Step | Tool | Coverage |
|---|---|---|
| 1. Static analysis | Semgrep + custom rules | MCP01 (hardcoded tokens), MCP05 (command injection), MCP06 (missing auth), MCP10 (context over-sharing) |
| 2. Protocol compliance | Custom task | Tool schema completeness, transport security, capability declarations |
| 3. Tool poisoning | Snyk agent-scan | MCP03 (injection in tool descriptions), shadow tool detection |

### Agent scan profile: `scan-agent`

Composite: runs skill scans on bundled skills, MCP scans on referenced
servers, plus agent-specific checks (harness config permissions, sandbox
escape patterns, unrestricted tool access).

**Behavioral testing** (nightly, not per-PR): adversarial prompts in
sandboxed environment (Firecracker/gVisor). Too slow for every build;
results cached as attestations.

## 3. OCI artifact structure per asset type

### Skills (Thomas Vitale spec v0.1.0)

```
OCI Image Manifest
  artifactType: application/vnd.agentskills.skill.v1
  config:       application/vnd.agentskills.skill.config.v1+json
                (SKILL.md frontmatter as queryable JSON)
  layers:
    - application/vnd.agentskills.skill.content.v1.tar+gzip
      (SKILL.md + scripts/ + references/ + assets/)
```

Config blob enables registry-side querying without pulling content.

Referrers (attached via cosign/ORAS):
- cosign signature, in-toto attestation, SBOM, scan results (SARIF)

### MCP servers

Already containerized -- the OCI artifact IS the container image, with
MCP-specific annotations:
```
annotations:
  io.rhoai.asset-type: mcp-server
  io.rhoai.mcp.transport: stdio|sse|streamable-http
  io.rhoai.mcp.tools: comma-separated tool names
```

Source-distributed MCP servers: Kitfile with `mcpServers` section.

### Agents (composite)

**3.6 path**: Kitfile ModelKit (flat bundle -- skills + MCP refs +
harness config in one artifact). Ships faster with KitOps today.

**3.7+ path**: OCI Image Index (composition -- each component as
independent digest, recursively verifiable and cacheable).

## 4. Signing and attestation flow

### Tekton Chains

Chains observes TaskRuns, captures IMAGE_URL + IMAGE_DIGEST results,
produces cosign signature + in-toto attestation. Works identically for
container images and non-container OCI artifacts.

### Custom in-toto predicate

The existing SLSA Provenance and Vulnerability predicates don't capture
agent-specific scan results. Define a custom predicate:

```
predicateType: https://rhoai.redhat.com/attestation/agent-security/v1
predicate:
  assetType: skill|mcp-server|agent
  scanLayers:
    - tool: skillspector, version: 1.2.0, result: PASS, findings: 0
    - tool: snyk-agent-scan, version: 0.9.0, result: PASS, findings: 3
  owaspMcpCoverage: [MCP01, MCP03, MCP04, MCP05]
```

### Conforma policy evaluation

Per-type Rego policies evaluate the custom attestation predicate:

```rego
deny[msg] {
  attestation.predicate.scanLayers[_].tool == "skillspector"
  attestation.predicate.scanLayers[_].result != "PASS"
  msg := "SkillSpector scan failed"
}
```

Conforma ships ~40 release policy packages. Adding AI-asset-specific
policies is Rego authoring, not code changes.

## 5. Metadata collection extension

### Current architecture

model-metadata-collection uses flag-based approach (not a provider
interface). Models and MCP servers are separate CLI invocations.

### Extension for skills (3.6)

**Approach**: add `--skill-index` and `--skill-catalog-output` flags
(matches existing MCP pattern, ships faster than refactor).

Skills provider behavior:
1. Read skill-index.yaml (list of OCI refs)
2. Pull OCI manifest, read config blob (SKILL.md frontmatter JSON)
3. Query OCI Referrers API for attestations (scan results)
4. Classify by tags/categories, assign trust tier
5. Generate catalog YAML entry for Kubeflow Hub

### Future refactor (3.7+)

```go
type AssetProvider interface {
    Discover(ctx, config) ([]AssetRef, error)
    Extract(ctx, ref) (*AssetMetadata, error)
    Enrich(ctx, meta) error
    Classify(ctx, meta) error
    ToCatalogEntry(meta) CatalogEntry
}
```

Implementations: ModelProvider, MCPProvider, SkillProvider, AgentProvider.

## 6. Disconnected delivery

### oc-mirror for non-container OCI

oc-mirror v2 (OCP 4.16+) handles non-container OCI artifacts via
`additionalImages`. No model-specific logic to generalize:

```yaml
mirror:
  additionalImages:
    - name: quay.io/rhoai/skills/my-skill:v1.0.0
    - name: quay.io/rhoai/mcp-servers/my-mcp:v2.1.0
```

Cosign signatures and attestations mirror automatically (OCI referrers).
Air-gapped: oc-mirror disk-to-mirror via physical media.

### YAML-baked ConfigMap path

Catalog metadata baked into ConfigMap at build time (existing pattern).
Extend to include skills and MCP metadata in parallel ConfigMaps.

## 7. Integration seams

### Pipeline → Catalog

Pipeline outputs OCI artifact to Quay + triggers model-metadata-collection
(webhook or scheduled). Tool generates catalog YAML. Kubeflow Hub reads
YAML and displays type-specific UI card.

### Pipeline → Registry

model-metadata-collection writes RegisteredModel + ModelVersion +
ModelArtifact to the MLflow registry API. Same flow extends to skills
if the registry tracks non-model assets (decision pending).

### Pipeline → Quay

Standard OCI push via `kit push` or `oras push`. Quay treats all OCI
artifacts equally. Cosign attaches signatures/attestations as referrers.
Quay supports OCI Referrers API (Distribution Spec 1.1).

## 8. Implementation path

### Phase 1: Skills (target 3.6)

| Work item | Effort | Dependencies |
|---|---|---|
| `scan-skill` Tekton task (SkillSpector + Snyk) | M | SkillSpector container image, Snyk token |
| `oci-package` Tekton task (kit pack for skills) | S | KitOps CLI image |
| Agent Security attestation predicate definition | S | None |
| Conforma skill policy rules (Rego) | S | Predicate definition |
| model-metadata-collection: skill flags | M | Catalog YAML schema |
| Pipeline template: `ASSET_TYPE=skill` path | M | All of the above |
| E2E test: skill through full pipeline | M | Pipeline template |

### Phase 2: MCP servers (target 3.7)

| Work item | Effort | Dependencies |
|---|---|---|
| `scan-mcp` Tekton task (OWASP MCP Top 10) | L | Custom Semgrep rules |
| MCP protocol compliance checker | M | MCP spec parser |
| Conforma MCP policy rules | S | scan-mcp output |
| Extend MCP metadata enrichment | S | Partially exists |
| Pipeline template: `ASSET_TYPE=mcp-server` | S | Phase 1 foundation |

### Phase 3: Agents (target 3.7+)

| Work item | Effort | Dependencies |
|---|---|---|
| Agent manifest specification | M | Skills + MCP specs stable |
| `scan-agent` Tekton task (composite) | L | scan-skill, scan-mcp |
| Behavioral testing harness (nightly) | L | Sandbox infrastructure |
| Agent OCI packaging | M | Agent manifest spec |
| model-metadata-collection: agent provider | M | Agent manifest spec |
| Conforma agent policy rules | S | scan-agent output |

## Key findings

1. **Single parameterized pipeline, not per-type**: `ASSET_TYPE` param
   with Tekton `when` expressions gates scan tasks. Less sprawl.
2. **SARIF is the scan output lingua franca**: all layers produce SARIF,
   attached as OCI referrers. Conforma evaluates SARIF-based predicates.
3. **KitOps is the packaging tool**: CNCF Sandbox, `kit pack` in a
   Tekton task handles all asset types via Kitfile.
4. **Custom in-toto predicate needed**: define
   `rhoai.redhat.com/attestation/agent-security/v1` for agent-specific
   scan results.
5. **model-metadata-collection extends via flags first**: `--skill-index`
   matches the existing MCP pattern. Provider interface refactor is 3.7+.
6. **oc-mirror handles non-container OCI natively**: no generalization
   needed. Skills mirror through `additionalImages`.
7. **Behavioral testing is nightly, not per-build**: cache results as
   attestations; Conforma checks recency.
8. **Phase 1 (skills) validates the cross-asset architecture**: reusable
   infrastructure for Phases 2 and 3.
