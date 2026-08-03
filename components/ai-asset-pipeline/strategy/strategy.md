---
title: "AI Asset Pipeline -- strategy"
description: Living strategy for the AI Asset Pipeline -- extend existing model trust pipeline (Konflux, RHTAS, model-metadata-collection) to skills, MCP servers, and agents; single parameterized pipeline with pluggable scan profiles; SLSA L3 provenance as unique moat; 3-phase implementation (skills 3.6, MCP 3.7, agents 3.7+); Adam Bellusci confirmed direction 2026-08-03.
timestamp: 2026-08-03
status: current
review_after: 2026-10-03
source: hub.strategy run 2026-08-03; inputs -- 8 knowledge entries (intake 2026-08-03) + 2-lens research (upstream, architecture) + sibling context (skills-catalog, mcp-catalog, agent-catalog, platform) + roadmap/strategy profiles
---

## The brief

The AI Asset Pipeline extends Red Hat's existing model trust pipeline
(Konflux, RHTAS, ModelCar, model-metadata-collection) to scan, sign,
attest, and OCI-package skills, MCP servers, and agents. **The bet**: a
single parameterized Konflux pipeline with pluggable per-type scan
profiles delivers SLSA L3 provenance for all AI asset types -- a
capability no competitor has
([05-competitive](/components/skills-catalog/research/05-competitive.md)).
Adam Bellusci (AI Hub owner) confirmed extend-not-build-new 2026-08-03
([decision-extend-existing-model-pipeline](/components/ai-asset-pipeline/knowledge/decision-extend-existing-model-pipeline.md)).
**Today**: direction confirmed, research complete, no Jira work planned.
**Top risks**: three competing OCI specs need a Red Hat position, no Jira
scope, epic-sized with no engineering owner. **Next milestone**: create
Jira work under RHAISTRAT-1339 and ship Phase 1 (skills scan + OCI
packaging) targeting 3.6.


## What

### Release train

| Release | Scope | Status |
|---|---|---|
| **3.6** (Phase 1: skills) | `scan-skill` Tekton task (SkillSpector + Snyk agent-scan), `oci-package` task (KitOps `kit pack`), custom in-toto agent-security predicate, Conforma skill policy rules (Rego), model-metadata-collection skill flags (`--skill-index`, `--skill-catalog-output`), parameterized pipeline template with `ASSET_TYPE=skill` path, E2E test | Direction confirmed, no Jira work |
| **3.7** (Phase 2: MCP servers) | `scan-mcp` Tekton task (OWASP MCP Top 10 Semgrep rules, protocol compliance checker), Conforma MCP policy rules, extend MCP metadata enrichment, `ASSET_TYPE=mcp-server` pipeline path | Future |
| **3.7+** (Phase 3: agents) | Agent manifest specification, `scan-agent` composite Tekton task, behavioral testing harness (nightly), agent OCI packaging (Kitfile or OCI Image Index), model-metadata-collection agent provider, Conforma agent policies | Future |

### Boundaries -- what this component is NOT

- **Not a catalog or registry** -- the pipeline sits upstream of both.
  Catalogs ([skills-catalog](/components/skills-catalog/),
  [mcp-catalog](/components/mcp-catalog/),
  [agent-catalog](/components/agent-catalog/)) index trust metadata for
  discovery. Registries track governance state. The pipeline does the
  security work. See
  [fact-ai-asset-pipeline-overview](/components/ai-asset-pipeline/knowledge/fact-ai-asset-pipeline-overview.md).
- **Not a new infrastructure system** -- extends existing Konflux,
  RHTAS/Sigstore, Quay, Conforma, and model-metadata-collection. New
  work is Tekton task definitions and pipeline templates, not platform
  changes.
- **Not model-specific** -- models already flow through this pipeline
  via ModelCar. The extension adds skills, MCP servers, and agents as
  additional asset types.
- **Not a runtime security system** -- pipeline is build-time. Runtime
  security (OpenShell sandboxing, MCP Gateway policy enforcement) is
  owned by other components.


## Why

### The problem

AI assets (skills, MCP servers, agents) enter enterprise environments
with no trust guarantees. 36.8% of public skills have security flaws
(Snyk ToxicSkills), 1,100+ were poisoned on ClawHub (ClawHavoc), 73%
carry elevated safety risk (SkillsBench). MCP servers face tool
poisoning and credential theft (OWASP MCP Top 10). Agents inherit both
risk surfaces. No vendor provides SLSA-grade provenance for non-model
AI assets. See
[fact-skills-supply-chain-security](/components/skills-catalog/knowledge/fact-skills-supply-chain-security.md).

### The bet

**Extend the proven model pipeline, don't build new.** Red Hat already
has SLSA L3 for container images via Konflux. ModelCar packages models
as OCI. RHTAS signs them. model-metadata-collection catalogs them. The
same infrastructure handles skills, MCP servers, and agents with
per-type scan profiles and a shared output contract (OCI + cosign +
in-toto + SBOM).

**SLSA L3 provenance is the moat.** No competitor combines SLSA Level 3
attestation, OCI distribution, open-source governance, and disconnected
delivery for AI assets. JFrog signs but has no SLSA provenance. NVIDIA
scans and signs but has no provenance chain. AWS, Azure, and Google have
no signing for skills at all. See
[05-competitive](/components/skills-catalog/research/05-competitive.md).

### Why now

- EU AI Act Article 50 in effect (August 2, 2026). Traceability and
  provenance support compliance.
- Skills catalog shipping in 3.6 -- without a trust pipeline, the
  catalog has trust badges but no mechanism to earn them.
- NVIDIA and JFrog both shipped trust pipelines in 2026. Red Hat's
  window to lead with SLSA L3 is open but closing.
- The model pipeline infrastructure is mature and proven. Extension
  is incremental, not greenfield.


## Where we stand

### Decisions to date

| Date | Decision | Link |
|---|---|---|
| 2026-08-03 | Extend existing model pipeline to skills, MCP servers, agents (Adam Bellusci) | [decision-extend-existing-model-pipeline](/components/ai-asset-pipeline/knowledge/decision-extend-existing-model-pipeline.md) |

### Delivery state

- **Direction confirmed** by Adam Bellusci (AI Hub owner), 2026-08-03.
- **No Jira work exists.** Epic-sized. Needs Jira scope under
  RHAISTRAT-1339 or a new cross-cutting STRAT.
- **No engineering owner assigned.**
- **Research complete**: upstream + architecture lenses (2026-08-03).
  Implementation path and work items defined at Jira-story granularity.

### Key infrastructure (already exists)

- **Konflux**: Tekton-based, SLSA L3, hermetic builds, 2M+ artifacts.
  See [ref-konflux](/components/ai-asset-pipeline/knowledge/ref-konflux.md).
- **model-metadata-collection**: Go, already multi-asset (models + MCP).
  See [ref-model-metadata-collection](/components/ai-asset-pipeline/knowledge/ref-model-metadata-collection.md).
- **KitOps/ModelPack**: CNCF Sandbox, OCI packaging for AI assets.
  See [ref-kitops-modelpack](/components/ai-asset-pipeline/knowledge/ref-kitops-modelpack.md).
- **Conforma**: policy-as-code, ~40 release policy packages, Rego.
  See [ref-conforma](/components/ai-asset-pipeline/knowledge/ref-conforma.md).
- **SkillSpector**: 68 vuln patterns, SARIF output, pipeline-ready.
  See [ref-nvidia-skillspector](/components/ai-asset-pipeline/knowledge/ref-nvidia-skillspector.md).


## Gaps & risks

### Organizational

- **No Jira work exists** -- the entire pipeline is direction-confirmed
  but unplanned. Needs Jira scope created and engineering owner assigned.
- **No engineering owner** -- Adam Bellusci owns AI Hub and confirmed
  the direction, but the pipeline work needs an engineering lead.

### Technical

- **Three competing OCI specs** -- Thomas Vitale's Agent Skills OCI spec
  (v0.1.0), skillctl/SkillImage (Red Hat ET), and KitOps/ModelPack all
  define different OCI packaging for skills. Red Hat needs a position.
  Research recommends KitOps (CNCF, RH contributes to ModelPack spec)
  but the Vitale spec has cleaner skill-specific media types
  ([01-upstream](/components/ai-asset-pipeline/research/01-upstream.md)).
- **Snyk agent-scan privacy** -- transmits tool descriptions to Snyk
  API. Evaluate for air-gapped deployments where this is unacceptable.
  SkillSpector runs fully offline.
- **Custom in-toto predicate** -- the existing SLSA Provenance and
  Vulnerability predicates don't cover agent-specific scan results.
  Needs `rhoai.redhat.com/attestation/agent-security/v1` defined before
  Phase 1 can ship.

### Timeline

- **Phase 1 (skills) targeting 3.6** is ambitious given no Jira work
  exists. The 7 work items (scan task, OCI packaging, predicate, Conforma
  rules, metadata collection, pipeline template, E2E test) are
  individually medium-sized but need sequencing.
- **Behavioral testing for agents (Phase 3)** requires sandbox
  infrastructure that may not exist yet. Nightly cadence with cached
  attestations is the pragmatic approach.

### Missing inputs

- No Jira scope stored. Run `hub.jira-sweep ai-asset-pipeline` once
  Jira work is created.
- No competitive or requirements research for the pipeline specifically
  (covered partially by skills-catalog research 05/07).


## Jira map

**No Jira scope stored for ai-asset-pipeline.** The following key is
known from the decision:

| Element | Key | Type | Status |
|---|---|---|---|
| AI Hub AI Asset Delivery (umbrella) | RHAISTRAT-1339 | Outcome | In Progress |

**First gap**: no Jira work exists for the pipeline itself. Create work
under RHAISTRAT-1339 or a new cross-cutting STRAT.

### Candidate jiras

| Gap | Problem statement | Suggested project |
|---|---|---|
| No skills scan Tekton task | Konflux has no agent-skills scanning stage; wrapping SkillSpector + Snyk agent-scan as a Tekton task closes the most visible competitive gap | RHAISTRAT (new Feature under 1339) |
| No OCI packaging task for skills | Skills need to be packaged as OCI artifacts (KitOps `kit pack`) for signing, mirroring, and disconnected delivery | RHAISTRAT (new Feature under 1339) |
| No custom in-toto predicate for AI assets | The existing SLSA and Vulnerability predicates don't capture agent-specific scan results; define `rhoai.redhat.com/attestation/agent-security/v1` | RHAISTRAT (new, cross-cutting) |
| No Conforma policies for AI assets | No Rego policies exist to gate AI assets through the release pipeline based on scan results | RHAISTRAT (new, under 1339) |
| model-metadata-collection: no skills provider | The Go tool handles models and MCP servers but not skills; needs `--skill-index` and `--skill-catalog-output` flags | RHOAIENG (new, under existing metadata-collection work) |
| No MCP server scan task (Phase 2) | OWASP MCP Top 10 checks need a Tekton task for Phase 2; custom Semgrep rules + protocol compliance checker | RHAISTRAT (new, 3.7) |
| No agent composite scan task (Phase 3) | Agent scanning requires composite skill + MCP + harness checks; agent manifest spec is a prerequisite | RHAISTRAT (new, 3.7+) |
| Three competing OCI specs -- no Red Hat position | Vitale spec, skillctl/SkillImage (RH ET), and KitOps define different OCI packaging; need a decision to align engineering work | RHAISTRAT (ADR, under 1339) |


## Watchlist

| Date | Trigger | If it fires, what changes |
|---|---|---|
| 2026-08 | RHAISTRAT-1339 scope planning | If pipeline work is scoped under 1339: Jira scope can be stored and engineering owner assigned. If deferred: pipeline remains a gap in the catalog's trust story. |
| 2026-08 | KitOps v1.14+ / ModelPack spec v1.0 | If ModelPack reaches v1.0 with full skill support: adopt as the standard OCI format. If stalls: evaluate Vitale spec or skillctl as alternatives. |
| 2026-09 | SkillSpector maturity / tagged release | If NVIDIA ships a production release: integrate as-is. If it remains minimal commits: evaluate forking or building a Red Hat equivalent. |
| 2026-09 | Snyk agent-scan air-gapped mode | If Snyk ships offline mode: viable for disconnected. If remains API-dependent: SkillSpector-only for air-gapped, Snyk for connected. |
| 2026-10-23 | RHOAI 3.6 code freeze | Hard deadline for Phase 1 (skills). If Jira work is not created by September: Phase 1 misses 3.6. |
| Ongoing | NVIDIA/JFrog trust pipeline evolution | If either ships SLSA L3: Red Hat loses the provenance moat. If they stay at signing-only: moat holds. |
| Ongoing | OWASP MCP Top 10 tooling | If scanning tools emerge for MCP: accelerates Phase 2. If nothing: custom Semgrep rules are the only path. |


## History

- 2026-08-03 -- **Creation** -- first strategy doc for ai-asset-pipeline. Synthesized from intake (8 entries: overview, decision, 5 refs, person) + 2-lens research (upstream, architecture). Key positions: extend existing model pipeline (Adam Bellusci confirmed), single parameterized Konflux pipeline, KitOps for OCI packaging, SARIF as scan lingua franca, custom in-toto predicate, 3-phase implementation (skills 3.6, MCP 3.7, agents 3.7+). 8 candidate jiras, no Jira scope stored.
