---
title: "Skills Catalog research -- architecture refresh"
description: Updates 03-architecture with supply chain pipeline (Konflux CI/CD, three-layer scanning, in-toto attestations), OCI artifact distribution (spec, oras, skillctl), installer architecture (7 methods, strategic position), metadata source-of-truth resolution (SKILL.md frontmatter vs MLflow registry), OpenShell layered sandboxing (deny-by-default + Kata composition), NVIDIA trust pipeline (SkillSpector, skill cards, signed directories), and disconnected delivery (Go git-pull service vs OCI mirror).
timestamp: 2026-07-30
lens: architecture
review_after: 2026-10-30
supersedes_context: "Updates 03-architecture (2026-07-23) with supply chain pipeline, installer architecture, metadata debate, OpenShell integration, and NVIDIA reference impl"
---

# Skills Catalog research -- architecture refresh

Prior research (03-architecture, 2026-07-23) established the hub extension
pattern, BFF reuse, disconnected pipeline, source federation, and trust
tier approach. This document covers what is architecturally new since
then, drawn from the Ann Marie Fred architectural strategy GDoc and
current industry patterns as of 2026-07-30.

## 1. Supply chain build/package/publish pipeline

The GDoc introduces a Konflux CI/CD pipeline to process skills before
they enter the catalog. This is epic-sized work that is not yet planned.

### Konflux pipeline architecture

[Konflux](https://konflux-ci.dev/) is a Kubernetes-native software factory
built on Tekton. Each build produces:

- **In-toto attestations** via Tekton Chains (SLSA Build L3 compliant)
- **Keyless signing** via Sigstore (no private key management)
- **SBOMs** in industry-standard formats
- **Hermetic builds** with network-isolated build environments

The pipeline is contract-first: `.tekton/` directory in the source repo
defines the build pipeline. On push or PR, Konflux clones, prefetches
dependencies, builds the OCI artifact, generates SBOM, runs scans, and
produces signed provenance attestations. [Conforma](https://conforma.dev/)
then gates artifacts against machine-readable policies derived from
those attestations.

Key architectural insight: Konflux separates the "neutral observer"
(attestation producer) from the "policy enforcer" (Conforma). This maps
to skills: the build pipeline attests what happened; a separate policy
layer decides whether the attestation is acceptable for the catalog.

### Three-layer scanning architecture

The GDoc proposes three scanning layers. Industry equivalents now exist:

| Layer | GDoc term | Industry tool | What it catches |
|---|---|---|---|
| Static analysis | miasma-detect | [SkillSpector](https://github.com/nvidia/skillspector) (64 patterns, 16 categories, AST pass, taint tracking, YARA, OSV.dev CVE lookup) | Vulnerable deps, dangerous code, credential access, data exfiltration paths |
| ML-model scan | Snyk agent-scan | [Snyk Agent Scan](https://github.com/snyk/agent-scan) (15+ risk categories, toxic flow analysis) | Prompt injection, tool poisoning/shadowing, toxic flows, malware payloads, hardcoded secrets |
| LLM-as-reviewer | Prodsec + CodeRabbit | SkillSpector LLM layer (optional second stage) | Hidden instructions, intent mismatches, excessive agency, behavioral threats |

Scale of the problem: Snyk's ToxicSkills study (Feb 2026) scanned 3,984
skills and found 36.8% with at least one security flaw, 13.4% critical,
76 confirmed malicious. SkillSpector's own dataset found prompt injection
in 26.1% of 42,447 skills and likely malicious intent in 5.2%.

### Design implication for RHOAI

The scanning pipeline is a pre-catalog gate, not a catalog runtime
concern. Skills entering the Red Hat catalog image would pass all three
layers during Konflux build. Partner and community skills would require
equivalent scan results before source inclusion. This aligns with the
sync-time compliance gate pattern identified in 03-architecture.

## 2. OCI artifact distribution

A draft specification (v0.1.0, April 2026) by Thomas Vitale proposes
[Agent Skills as OCI Artifacts](https://www.thomasvitale.com/agent-skills-as-oci-artifacts/).
This is the most architecturally significant development since 03.

### Specification structure

Two OCI primitives:

- **Skill Artifact**: OCI Image Manifest with `artifactType:
  application/vnd.agent-skills.skill.v1`. SKILL.md, scripts, and
  resources packaged as content layers.
- **Collection Artifact**: OCI Image Index (same construct as
  multi-platform images) referencing individual Skill digests by name.

Consumer-side: `skills.json` (declarative manifest) + `skills.lock.json`
(pinned to immutable digests, not mutable tags). Mirrors npm's
package.json/package-lock.json pattern.

### Why OCI matters for RHOAI

- **Same infrastructure**: Harbor, Zot, Quay -- the registries already
  serving container images can host skills with zero new infrastructure.
- **Same mirror workflows**: oc-mirror, skopeo copy, crane pull all work
  on OCI artifacts. Disconnected delivery uses existing tooling.
- **Same signing**: Cosign signatures attach via OCI Referrers API as
  referrer artifacts. SBOMs, attestations, and evaluation reports attach
  the same way.
- **No GitHub dependency**: organizations running internal Forgejo,
  GitLab, or Bitbucket need only one API -- OCI distribution spec.

Reference implementations: Arconia CLI (ORAS Java), skills-oci CLI
(ORAS Go, by Mauricio Salatino), [skillctl](https://skillimage.dev/)
(enterprise-grade CLI), and ORAS CLI for low-level workflows. CNCF
Sandbox project [KitOps](https://www.cncf.io/blog/2025/08/27/how-oci-artifacts-will-drive-future-ai-use-cases/)
also packages skills as ModelKits.

### Design implication for RHOAI

OCI distribution is the strategic path for Red Hat. It reuses existing
container supply chain infrastructure (Konflux builds OCI, Quay stores
OCI, oc-mirror mirrors OCI). The catalog image can contain OCI skill
artifacts rather than raw YAML, enabling signature verification at
install time. This converges the "baked YAML" disconnected path with the
"OCI mirror" disconnected path.

## 3. Installer architecture

The GDoc compares 7 installation methods. The strategic position is
"don't prevent any, choose one for RH automation and guarantee via E2E
testing." The landscape has clarified:

| Method | Mechanism | Ecosystem reach | RHOAI fit |
|---|---|---|---|
| git clone + copy | File copy to `.claude/skills/` | Universal | Baseline, always works |
| marketplace.json | Plugin marketplace discovery | Claude Code | Already wired in RHOAI |
| npx skills add | [skills.sh](https://github.com/vercel-labs/skills) CLI | 70+ agents | npm dependency, broad reach |
| Microsoft APM | Agent Package Manager | VS Code/Copilot | Microsoft-specific |
| LOLA | LLM-orchestrated install | Experimental | Not production-ready |
| oras pull | OCI registry pull | Any OCI client | Aligns with OCI strategy |
| MLflow CLI extension | mlflow skills install | MLflow ecosystem | Registry integration path |

The ecosystem grew from 1 registry (Dec 2025) to 8 major marketplaces
by Q2 2026, with npm-style package management as the dominant pattern.
`npx skills add` supports 70+ agents with lockfile-based reproducibility.

### Design implication for RHOAI

Two installation paths serve different personas:
1. **Catalog install** (admin): OCI pull from Quay/mirror -> deploy to
   cluster namespace. This is the RHOAI-managed path.
2. **Developer install** (individual): `npx skills add` or git clone
   for local agent use. RHOAI does not control this path.

The hardest question from 03-architecture remains: where does a
catalog-installed skill land? The agent runtime needs filesystem access
to SKILL.md. If skills run in OpenShell containers, the install target
is the container image or a mounted volume. This is the integration
seam between catalog and runtime.

## 4. Metadata source-of-truth resolution

The GDoc surfaces a debate between Roland Huss (metadata belongs in
Git frontmatter, not split across MLflow) and Ann Marie (MLflow stores
governance data + relationships that frontmatter cannot).

### The two-registry pattern emerging in the ecosystem

The industry is converging on a split that maps to RHOAI's architecture:

| Metadata type | Source of truth | Rationale |
|---|---|---|
| Skill identity (name, description, version, license, author) | SKILL.md frontmatter | Travels with the artifact, no registry dependency |
| Discovery metadata (tags, categories, trust tier) | Catalog source YAML | Admin-curated, catalog-scoped |
| Governance metadata (scan results, approval status, usage analytics, relationships) | MLflow skill registry | Lifecycle state, not intrinsic to the skill |
| Verification metadata (signatures, attestations, SBOMs) | OCI Referrers API | Attached to artifact digest, registry-native |

MLflow [issue #22833](https://github.com/mlflow/mlflow/issues/22833)
proposes a skill registry that "stores metadata and typed source pointers
rather than skill artifacts directly." This matches RHOAI's architecture:
catalog stores/displays, registry governs, neither stores skill content.

### NVIDIA's skill card as a middle layer

NVIDIA skill cards (machine-readable YAML/JSON) sit between frontmatter
and registry: they declare owner, license, use case, output shape,
risks, and mitigations. They are generated as part of the verification
pipeline and travel with the skill, but contain governance-adjacent
data. RHOAI could adopt a similar "enriched metadata" layer that the
catalog displays and the registry indexes.

### Design implication for RHOAI

Roland's concern is valid: splitting metadata creates sync risk. The
resolution is to define a clear ownership boundary. SKILL.md frontmatter
is the canonical identity (name, description, version). The catalog
normalizes from frontmatter + source config. The registry adds lifecycle
state. Neither overwrites the other. Skill cards (if adopted) are build
artifacts, not runtime state.

## 5. OpenShell integration for supply chain mitigation

The GDoc identifies OpenShell as the runtime mitigation: deny-by-default
binaries/CLI, deny-by-default network, masked API keys, isolated
container/VM.

### OpenShell architecture (NVIDIA, Apache 2.0, alpha)

[OpenShell](https://github.com/NVIDIA/openshell) enforces four policy
domains:

1. **Filesystem**: Landlock LSM (kernel-enforced path restrictions)
2. **Network**: HTTP CONNECT proxy with OPA/Rego evaluation, deny-by-default
3. **Process**: Seccomp BPF filters, no privilege escalation
4. **Inference**: Privacy router strips caller credentials, injects
   backend credentials

### Layered composition with OpenShift

Red Hat's own analysis ([Layered sandboxing for AI agents](https://developers.redhat.com/articles/2026/07/16/layered-sandboxing-ai-agents-openshift-and-openshell),
July 2026) shows the two layers are complementary:

- **OpenShell** (application layer): blocks data exfiltration, unauthorized
  API calls, prompt injection network channels. Cannot stop kernel exploits.
- **Kata/sandboxed containers** (hardware layer): blocks container escapes,
  kernel exploits, cross-container corruption. Cannot inspect application
  behavior.

Validated result: each attack succeeded against the layer missing its
protection. Only dual-protected pods stopped both prompt-injection
exfiltration and kernel-level container escape.

### Design implication for RHOAI

Skills in the catalog are inert metadata. The supply chain mitigation
applies at runtime, when an agent loads and executes a skill. The
catalog's role is to surface trust metadata (scan results, signatures,
trust tier) that informs the runtime's OpenShell policy. A skill flagged
as requiring network access should trigger a different OpenShell policy
than a skill that is pure-instruction. This is the catalog-to-runtime
contract.

## 6. Disconnected delivery architecture

03-architecture covered the YAML-baked ConfigMap path. Two new patterns
emerged from the GDoc discussion:

### Ramesh's Go git-pull service

A Go-based service fronting mirrored skill Git repos with git-pull
protocol support (not a full Git server). Purpose: distribute RH and
partner skills out of the box for disconnected environments. Overlay
model: check live source first, fall back to mirrored copy.

Ann Marie's counterpoint: many customers already have internal Git.
This adds infrastructure.

### OCI mirror path (emerging alternative)

If skills are OCI artifacts, disconnected delivery collapses to the
existing oc-mirror workflow. No new service needed. The catalog image
contains OCI skill artifacts; oc-mirror copies them to the disconnected
registry; the catalog service indexes from the local registry.

### Design implication for RHOAI

The Go git-pull service solves a real problem (golden-copy versioning
for disconnected) but adds operational burden. If OCI distribution is
adopted, the same problem is solved by existing tooling. The choice
between these paths should be driven by the OCI artifact decision: if
skills ship as OCI, the git-pull service becomes redundant.

## 7. NVIDIA trust pipeline as reference architecture

The [NVIDIA trust pipeline](https://docs.nvidia.com/skills/agent-skill-trust-pipeline)
is the most mature reference implementation. Six stages:

1. **Authoring**: narrow purpose, clear triggers, explicit permissions
2. **Scanning**: SkillSpector against entire skill directory
3. **Remediation**: resolve high-risk findings or document accepted risk
4. **Documentation**: complete skill card with structured metadata
5. **Signing**: sign directory, publish detached `skill.oms.sig`
6. **Consumer verification**: verify signature before installation

Key design principle: "Scanning asks whether the content appears safe
enough to ship. Signing asks whether the shipped content is the same
content that was reviewed." These are separable concerns.

NVIDIA signs the entire skill directory (SKILL.md, scripts, references,
assets) using the OpenSSF Model Signing standard. Bill Murdock's comment
that NVIDIA signs the "skill/card/eval/benchmark tuple" means the
signature covers the directory containing all four, not a cryptographic
tuple construct.

The NVIDIA verified catalog currently covers 162 skills across 16
product families. The review gate requires: behavior matches description,
permissions are minimal, capabilities are declared and justified, risks
are documented, and signature verifies.

## Key findings

1. **Supply chain pipeline is Konflux-native**: three-layer scanning
   (static + ML-model + LLM) feeds in-toto attestations and cosign
   signatures. This is a pre-catalog build concern, not a runtime concern.
2. **OCI distribution is the strategic convergence point**: same
   registries, same mirrors, same signing, same tooling as containers.
   Eliminates the need for a separate Git-pull service for disconnected.
3. **Installer question partially resolved**: catalog installs via OCI
   pull (admin path); developer installs via npx/git (unmanaged path).
   The hard question remains: where does the installed skill land in the
   agent runtime filesystem?
4. **Metadata split is defensible if boundaries are clear**: frontmatter
   owns identity, catalog owns discovery, registry owns governance,
   OCI Referrers API owns verification artifacts. No layer overwrites
   another.
5. **OpenShell + Kata is the layered runtime mitigation**: catalog
   surfaces trust metadata that informs OpenShell policy selection.
   The catalog-to-runtime contract is the new integration seam.
6. **NVIDIA trust pipeline is the reference to follow**: six-stage
   pipeline with separable scanning and signing concerns. Skill cards
   provide the middle metadata layer between frontmatter and registry.
7. **Disconnected delivery converges with OCI**: if skills are OCI
   artifacts, oc-mirror handles disconnected. The Go git-pull service
   proposal becomes redundant.
