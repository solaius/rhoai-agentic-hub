---
title: "AI Asset Pipeline research -- upstream projects and standards"
description: "Engineering-focused survey of Konflux, model-metadata-collection, KitOps/ModelPack, RHTAS, Conforma, SkillSpector, OCI artifact specs, and Tekton Chains -- extension points for multi-asset AI pipelines"
timestamp: 2026-08-03
lens: upstream
review_after: 2026-11-03
---

# AI Asset Pipeline research -- upstream projects and standards

## 1. Konflux pipeline internals

Konflux is Red Hat's cloud-native software factory built on Tekton. Builds,
tests, and releases are all expressed as PipelineRuns created by
Pipelines-as-Code from `.tekton/` directory definitions.

### Tekton task authoring

Each task is a single YAML file in a flat `task/<name>/` directory. Multiple
version streams use subdirectories (`task/<name>/1.x/`). Tasks are built as
standard **OCI artifacts** (not container images) via the
`tekton-bundle-builder-oci-ta` pipeline. The build reads
`app.kubernetes.io/version` from the Task YAML and sets the
`org.opencontainers.image.version` OCI annotation automatically.

Key extension point: to add a new pipeline type for non-container artifacts,
create a Component pointing at your task directory and select
`tekton-bundle-builder-oci-ta` as the build pipeline. Konflux (via
Pipelines-as-Code) generates `on-pr` and `push` PipelineRun definitions in
`.tekton/`, scoped to the relevant path via CEL expressions:

```yaml
pipelinesascode.tekton.dev/on-cel-expression: |
    event == "pull_request" && target_branch == "main"
    && ("task/echo/***".pathChanged())
```

### Trusted Artifacts for inter-task data sharing

Tasks share files via Trusted Artifacts (ADR-0036) -- archives stored in OCI
registries with checksums. This lets custom tasks participate in build
pipelines without compromising integrity. To author a TA variant, create a
`${task_name}-oci-ta/` directory with a `recipe.yaml` and generate the
variant using `hack/generate-ta-tasks.sh`.

### Release flow

Released bundles are pushed via the `push-tekton-task-bundles-to-external-registry`
managed pipeline. The release process updates a `data-acceptable-bundles` OCI
artifact containing SHA references of trusted tasks, which Conforma consults
for the `trusted_task.trusted` policy check.

**Sources:** [Konflux task authoring](https://konflux-ci.dev/docs/end-to-end/building-tekton-tasks/), [Pipeline Service architecture](https://konflux-ci.dev/architecture/core/pipeline-service/), [Centralizing pipeline definitions](https://konflux-ci.dev/docs/patterns/centralize-pipeline-definitions/)


## 2. model-metadata-collection architecture

A Go tool (`opendatahub-io/model-metadata-collection`) with two CLIs:
`model-extractor` (pipeline) and `metadata-report` (quality analysis).

### Package layout

```
cmd/model-extractor/      # primary pipeline CLI
cmd/metadata-report/      # read-only reporting CLI
internal/catalog/          # aggregates metadata into YAML catalogs
internal/config/           # CLI flag parsing / config state
internal/enrichment/       # merges data with priority ordering
internal/huggingface/      # HuggingFace API integration
internal/metadata/         # modelcard.md parsing, schema migration
internal/registry/         # OCI manifest fetching, annotation processing
internal/report/           # field completeness statistics
pkg/types/                 # shared type definitions
pkg/utils/                 # utility functions
```

### Pipeline stages

1. **Discovery** -- query HuggingFace collections, produce version-specific
   index YAML under `input/models/collections/`.
2. **Extraction** -- inspect OCI images, extract `modelcard.md` from layers
   via annotation-based detection. Skeleton metadata on failure.
3. **Enrichment** -- merge with strict priority: HuggingFace YAML frontmatter
   > modelcard.md > HuggingFace API > registry defaults.
4. **Catalog generation** -- aggregate individual metadata files; validate
   `model_type` against `generative | predictive | unknown`.
5. **Reporting** -- field-level completeness with provenance tracking.

### MCP server support (already shipped)

MCP catalogs run as a **parallel track**. CLI flags `--mcp-index` and
`--mcp-catalog-output` point to per-tier index files
(`redhat-mcp-servers-index.yaml`, `partner-...`, `community-...`).
Model processing can be suppressed with `--skip-huggingface --skip-enrichment
--skip-catalog`.

### Extension pattern for skills and agents

The MCP track is the architectural precedent. Adding skills/agents requires:

1. Define type schema in `pkg/types/`.
2. Create index YAML format + CLI flags (`--skills-index`, `--agents-index`).
3. Build extraction package under `internal/` for the new source.
4. Add enrichment logic (or extend existing).
5. Add catalog output path and skip flags.
6. Extend reporting for the new asset type.

No formal provider interface exists -- each asset type gets its own internal
package. The pattern is pragmatic copy-and-adapt, not plugin-based.

**Source:** [model-metadata-collection](https://github.com/opendatahub-io/model-metadata-collection)


## 3. KitOps and CNCF ModelPack

KitOps (CNCF project, 240k+ downloads) packages AI/ML assets as OCI
artifacts called ModelKits. It also implements the CNCF ModelPack spec.

### Kitfile

A YAML manifest defining what goes into a ModelKit: models, datasets, code,
docs, prompts, agent skills, MCP server configs. Each becomes a separate OCI
layer with its own SHA-256 digest, enabling selective unpacking.

### OCI media types (ModelKit format)

| Asset | Media type |
|---|---|
| Config (Kitfile) | `application/vnd.kitops.modelkit.config.v1+json` |
| Model | `application/vnd.kitops.modelkit.model.v1.tar` |
| Model part / adaptor | `application/vnd.kitops.modelkit.modelpart.v1.tar` |
| Dataset | `application/vnd.kitops.modelkit.dataset.v1.tar` |
| Code | `application/vnd.kitops.modelkit.code.v1.tar` |
| Docs | `application/vnd.kitops.modelkit.docs.v1.tar` |

The ModelPack format uses CNCF model-spec media types instead. Pack with
`kit pack . --use-model-pack`. Both formats work transparently with Kit
commands (pull, push, unpack, inspect).

### Agent skill installation (v1.13.0)

`kit unpack --as-skill` auto-installs skills for all detected AI tools
(Claude Code, Codex, etc.) on the system.

### Kubernetes compatibility caveat

Custom KitOps media types are silently ignored by Kubernetes ImageVolumes
(1.35+), which expect standard OCI layer types. ModelPack format or standard
media types are needed for direct volume mounting.

### Governance

Contributing companies: Red Hat, PayPal, ANT Group, ByteDance. Two
implementations of ModelPack: KitOps and Modctl. KitOps is the enterprise
implementation.

**Sources:** [KitOps overview](https://kitops.org/docs/overview/), [ModelKit spec](https://kitops.org/docs/modelkit/spec/), [ModelPack integration](https://kitops.org/docs/integrations/modelpack/)


## 4. ModelCar pipeline baseline

ModelCar packages models as OCI container images with a `/models` directory.
The current pipeline:

1. **Source** -- download from HuggingFace using `huggingface-hub` Python
   package.
2. **Build** -- multi-stage Containerfile: stage 1 uses `ubi9/python-311` to
   download model; stage 2 copies only `/models` into `ubi-micro`.
3. **Push** -- `podman push` to Quay.io or `registry.redhat.io`.
4. **Serve** -- KServe with `oci://quay.io/<registry>/<image>:<tag>` URI
   format, or Podman + RHAIS directly.

Validated models ship as pre-built ModelCar images with architecture-specific
configurations. Enabled (non-validated) models have simpler packaging.

The pipeline is currently manual (Containerfile-based). The signing step
(RHTAS) and metadata extraction (model-metadata-collection) are separate
processes, not yet integrated into a single Konflux pipeline.

**Sources:** [Red Hat AI Inference Server ModelCar docs](https://docs.redhat.com/en/documentation/red_hat_ai_inference_server/3.4/html-single/inference_serving_language_models_in_oci-compliant_model_containers/index), [Building ModelCar containers](https://developers.redhat.com/articles/2025/01/30/build-and-deploy-modelcar-container-openshift-ai)


## 5. RHTAS and Sigstore integration

Red Hat Trusted Artifact Signer (RHTAS) is a production deployment of
Sigstore (Fulcio CA + Rekor transparency log + TSA) on OpenShift.

### Keyless signing flow

1. Signer authenticates via OIDC (cluster identity).
2. Fulcio issues a short-lived signing certificate.
3. Cosign signs the artifact using the ephemeral key.
4. Signing event recorded in Rekor transparency log.
5. Certificate and key are discarded -- no key management required.

### Tekton Chains integration

Tekton Chains watches for completed TaskRuns/PipelineRuns and automatically:
- Generates SLSA provenance as in-toto attestations.
- Signs the provenance using the configured signer (RHTAS/Cosign).
- Stores signatures in OCI registries or Rekor.
- Annotates the run with `chains.tekton.dev/signed=true`.

The formatting-signing-uploading pipeline runs automatically with no
pipeline modifications needed. Type hinting via `CHAINS-GIT_COMMIT` and
`CHAINS-GIT_URL` parameters tells Chains about input materials.

### SLSA levels

- Chains alone achieves SLSA Level 2 (authenticated provenance).
- SLSA Level 3 (non-falsifiable provenance) requires SPIFFE/SPIRE integration
  for short-lived certificates backed by workload attestation.

### Model Transparency CLI

`sigstore/model-transparency` provides `model_signing sign` and
`model_signing verify` subcommands for ML models specifically. Creates
Sigstore bundle protobufs (JSON) containing DSSE envelopes. The Go
implementation (`model-transparency-go`) was proposed for donation in
February 2026. A Kubernetes Model Validation Operator (v1.0.1) auto-verifies
signed models before workload execution.

### GA status

RHTAS Operator supports OpenShift 4.16-4.20 (latest update June 2026).
Cosign CLI is the primary signing interface.

**Sources:** [RHTAS product page](https://access.redhat.com/products/red-hat-trusted-artifact-signer/), [RHTAS developer page](https://developers.redhat.com/products/trusted-artifact-signer), [Tekton Chains SLSA provenance](https://tekton.dev/docs/chains/slsa-provenance/), [Model Transparency](https://github.com/sigstore/model-transparency)


## 6. Conforma policy authoring

Conforma (formerly Enterprise Contract) evaluates OPA/Rego policies against
SLSA provenance attestations to gate Konflux releases.

### Policy structure

Policies are organized into **packages** (~40 release packages, ~5 pipeline
packages, ~6 task packages) grouped into **rule collections**: `minimal`,
`slsa3`, `redhat`, `redhat_security`, `github`.

Each rule is Rego code with a metadata annotation block:

```rego
# METADATA
# title: My custom check
# description: Validates X against Y
# custom:
#   short_name: my_check
#   failure_msg: "X did not match expected Y"
#   solution: "Ensure X is configured correctly"
package my_package

deny contains result if {
    # rule logic
    result := {
        "code": "my_package.my_check",
        "msg": "failure message",
    }
}
```

Rules produce `deny` (blocks release) or `warn` (advisory) results.

### Custom built-in functions

Conforma provides Rego builtins beyond standard OPA:

- `ec.oci.blob`, `ec.oci.image_manifest`, `ec.oci.image_referrers` -- OCI
  registry access from within policy evaluation.
- `ec.sigstore.verify_attestation`, `ec.sigstore.verify_image` -- Sigstore
  verification.
- `ec.purl.parse`, `ec.purl.is_valid` -- Package URL parsing.

### EnterpriseContractPolicy CRD

```yaml
apiVersion: appstudio.redhat.com/v1alpha1
kind: EnterpriseContractPolicy
spec:
  publicKey: k8s://openshift-pipelines/public-key
  sources:
    - name: Release policies
      policy:
        - github.com/conforma/policy//policy/release
      data:
        - oci::quay.io/konflux-ci/tekton-catalog/data-acceptable-bundles:latest
      config:
        include: ["*"]
        exclude: ["hermetic_build_task.*"]
```

Policies are bundled as OCI artifacts via conftest and referenced by git URL
or CR name in `IntegrationTestScenario.spec.params.POLICY_CONFIGURATION`.

### Extension for AI assets

To add AI-asset-specific policies (e.g., "skill must pass SkillSpector with
score < 50"), write a Rego package that parses the relevant attestation
predicate, bundle it as OCI, and add it to the policy sources. Conforma's
`ec.oci.*` builtins can fetch artifact metadata directly from registries
during evaluation.

**Sources:** [Conforma policies](https://conforma.dev/docs/policy/index.html), [Release policy](https://conforma.dev/docs/policy/release_policy.html), [Custom config](https://conforma.dev/docs/user-guide/custom-config.html), [Red Hat docs](https://docs.redhat.com/en/documentation/red_hat_advanced_developer_suite_-_software_supply_chain/1.8/html/managing_conforma/proc_creating-an-ec-policy_conforma-rhads)


## 7. SkillSpector internals

NVIDIA's SkillSpector (v2.0.0, Apache 2.0, 5.5k GitHub stars) is a
purpose-built security scanner for AI agent skills.

### Two-stage pipeline

**Stage 1 -- Static analysis** (seconds):
- 68 regex patterns across 17 categories (prompt injection, data
  exfiltration, supply chain, MCP least privilege, MCP tool poisoning, etc.).
- AST behavioral analysis: walks Python AST for `exec()`, `eval()`,
  `subprocess`, `os.system`, `compile`, dynamic `import`/`getattr`.
- Taint tracking: follows data from sources (env vars, file reads) to sinks
  (network calls, exec).
- YARA signatures: malware, webshells, cryptominers, exploit tools.
- Live CVE lookups via OSV.dev (offline fallback).

**Stage 2 -- LLM semantic analysis** (optional, ~87% precision):
- LLM evaluates context and intent, filters false positives.
- Anti-jailbreak protections prevent malicious skills from talking their way
  out of being flagged.
- Providers: OpenAI, Anthropic, NVIDIA, AWS Bedrock, local CLI.

### Risk scoring

Additive: CRITICAL +50, HIGH +25, MEDIUM +10, LOW +5. Executable content
multiplier: 1.3x. Bands: 0-20 SAFE, 21-50 CAUTION, 51-100 DO NOT INSTALL.
Exit code 0 for score <= 50, exit code 1 for score > 50.

### Input/output contract

**Input:** Git repos, URLs, zip files, directories, single files. Per-ingest
cap 100 MiB, per-file 1 MB, zip member cap 10,000.

**Output formats:** Terminal, JSON, Markdown, SARIF (v2.1.0). The SARIF
output is directly consumable by CI/CD pipelines and IDE tooling.

### LangGraph architecture

Orchestrated as a LangGraph workflow with nodes: `resolve_input` ->
`build_context` -> `analyzers` -> `meta_analyzer` -> `report`. Invokable as
a Python API:

```python
from skillspector import graph
result = graph.invoke({
    "input_path": "/path/to/skill",
    "output_format": "sarif",
    "use_llm": False,
})
```

### MCP server mode

SkillSpector can run as an MCP server exposing a `scan_skill` tool via stdio
or HTTP/SSE, turning it into a runtime guardrail rather than an out-of-band
audit step.

### Wrapping as a Tekton task

To wrap SkillSpector as a Konflux Tekton task:

1. Create a container image with Python 3.12+ and SkillSpector installed.
2. Define a Task YAML with `SKILL_PATH` param and `SARIF_OUTPUT` result.
3. Run `skillspector scan $SKILL_PATH --format sarif --output /results/report.sarif`.
4. Use exit code as pass/fail gate. Attach SARIF as an attestation via
   Tekton Chains.
5. Build as OCI bundle via `tekton-bundle-builder-oci-ta`.

**Source:** [SkillSpector](https://github.com/NVIDIA/SkillSpector)


## 8. OCI artifacts for non-container content

### OCI Distribution Spec v1.1

Two key additions enable non-container artifact workflows:

- **`artifactType` field** -- top-level field on manifests denoting custom,
  non-image artifacts. When absent, falls back to `config.mediaType`.
- **Referrers API** -- `GET /v2/<name>/referrers/<digest>` returns an OCI
  Image Index listing all artifacts that reference a given digest via the
  `subject` field. This is how signatures, SBOMs, and attestations link to
  their parent artifacts.

Fallback for older registries: digest tag `sha256-<digest>` mimics the
referrers response. ORAS, Cosign, and Notation handle this transparently.

### Thomas Vitale's Agent Skills OCI Artifacts Spec (v0.1.0, Draft)

Defines packaging, distribution, signing, and tracking for Agent Skills:

| Component | Media type |
|---|---|
| Skill artifact type | `application/vnd.agentskills.skill.v1` |
| Config blob | `application/vnd.agentskills.skill.config.v1+json` |
| Content layer | `application/vnd.agentskills.skill.content.v1.tar+gzip` |
| Collection index | `application/vnd.agentskills.collection.v1` |

Config schema fields: `schemaVersion`, `name`, `version` (SemVer),
`description`, `license` (SPDX), `compatibility`, `allowedTools`,
`metadata`. Exactly one content layer per skill artifact.

Dependency management via `skills.json` (user-edited, declares OCI
references) and `skills.lock.json` (machine-generated, pins exact digests).

Supply chain security: Cosign signing + in-toto attestations attached via
OCI Referrers API.

### skillctl / SkillImage (Red Hat ET)

`skillctl` (`redhat-et/skillimage`) packages skills as **standard OCI
images** (not custom artifact types), enabling `podman pull`, `skopeo copy`,
and Kubernetes ImageVolume mounting (K8s 1.33+ / OpenShift 4.20+) without
init containers. Uses Cosign/Sigstore for signing and supports lifecycle
stages (draft, testing, published, deprecated, archived).

Key difference from the Vitale spec: skillctl uses standard OCI image media
types for Kubernetes compatibility, while the Vitale spec uses custom
artifact types for richer metadata.

### Convergence opportunity

Both approaches are being discussed in CNCF TOC issue #1740 and the
`#initiative-oci-compliant-inner-loop-tooling-and-packaging` CNCF Slack
channel. The Vitale spec, skillctl, ToolHive, and KitOps are all potential
converging implementations.

**Sources:** [OCI v1.1 announcement](https://opencontainers.org/posts/blog/2024-03-13-image-and-distribution-1-1/), [Vitale spec](https://github.com/ThomasVitale/agents-skills-oci-artifacts-spec), [Vitale blog](https://www.thomasvitale.com/agent-skills-as-oci-artifacts/), [skillimage.dev](https://skillimage.dev/), [agentskills discussion](https://github.com/agentskills/agentskills/discussions/292)


## Key findings

1. **Konflux is already OCI-artifact-native.** Tekton tasks are built and
   distributed as OCI bundles. Adding a new pipeline type for skills/agents
   requires creating a Component + task YAML, not modifying Konflux itself.

2. **model-metadata-collection already handles MCP servers.** The Go tool's
   parallel-track architecture (separate index, enrichment, catalog for each
   asset type) is the natural extension point for skills and agents. No
   plugin interface -- copy-and-adapt the MCP pattern.

3. **Three competing OCI packaging specs for skills exist.** The Vitale
   Agent Skills OCI spec (custom artifact types, rich metadata), skillctl
   (standard OCI images, Kubernetes-native), and KitOps (multi-asset
   ModelKit bundles). Red Hat should pick one or contribute to convergence
   via CNCF TOC #1740.

4. **SkillSpector is pipeline-ready.** SARIF output, exit codes, and
   per-ingest caps make it wrappable as a Tekton task. The MCP server mode
   could also serve as a runtime guardrail in the serving layer.

5. **Conforma policies are extensible via Rego.** Custom attestation
   predicates (e.g., SkillSpector scan results, agent capability
   declarations) can be evaluated using `ec.oci.*` builtins. No Conforma
   code changes needed -- just new policy bundles.

6. **Tekton Chains signs anything.** SLSA provenance generation is
   automatic for any TaskRun/PipelineRun. The signing infrastructure
   (RHTAS/Cosign/Rekor) works for any OCI artifact, not just containers.

7. **Model Transparency CLI has a Go implementation.** The
   `model-transparency-go` library and the Model Validation Operator
   provide a Kubernetes-native verification path that could extend to
   non-model assets.

8. **KitOps is the most complete multi-asset packaging solution.** It
   already handles models, datasets, code, prompts, agent skills, and MCP
   server configs in a single versioned artifact. Red Hat is a ModelPack
   contributing company. The `--as-skill` flag (v1.13.0) shows agent
   ecosystem awareness.
