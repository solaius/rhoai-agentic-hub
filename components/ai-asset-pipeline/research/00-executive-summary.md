---
title: "AI Asset Pipeline research -- executive summary"
description: Living synthesis of the 2-lens first run (upstream + architecture, 2026-08-03) -- extend existing model pipeline via parameterized Konflux template with per-type scan profiles; KitOps for OCI packaging; custom in-toto predicate for agent security; SARIF as scan lingua franca; oc-mirror handles disconnected natively; 3-phase implementation (skills 3.6, MCP 3.7, agents 3.7+).
timestamp: 2026-08-03
review_after: 2026-11-03
---

# AI Asset Pipeline research -- executive summary

First research run: **standard, 2 lenses, 2026-08-03**, all completed.

## The series

| Doc | Lens | One line |
|---|---|---|
| [01-upstream](/components/ai-asset-pipeline/research/01-upstream.md) | upstream | Konflux Tekton task authoring, model-metadata-collection Go architecture, KitOps/ModelPack OCI spec, ModelCar baseline, RHTAS/Sigstore, Conforma policy authoring, SkillSpector internals, OCI Distribution Spec v1.1 |
| [02-architecture](/components/ai-asset-pipeline/research/02-architecture.md) | architecture | Single parameterized pipeline, pluggable scan profiles (skills/MCP/agents), OCI artifact structures per type, Tekton Chains signing, custom in-toto predicate, Conforma policy patterns, metadata collection extension, disconnected delivery, 3-phase implementation path |

## What the sweep establishes

**1. The existing pipeline extends cleanly -- no infrastructure
changes needed.** Konflux already builds non-container OCI artifacts
(Tekton task bundles are built and signed this way today). Adding
skills, MCP servers, and agents as new artifact types requires new
Tekton task definitions and pipeline templates, not Konflux platform
changes. The same Tekton Chains signing, Conforma gating, and Quay
storage work identically for all OCI artifact types (01).

**2. Single parameterized pipeline beats per-type pipelines.** Use an
`ASSET_TYPE` enum parameter (`model|skill|mcp-server|agent`) with
Tekton `when` expressions to gate type-specific scan tasks. This
matches Konflux's existing conditional-task pattern and avoids pipeline
definition sprawl. All types share git-clone, prefetch, OCI-package,
SBOM-generate, Chains signing, and Conforma gating (02).

**3. KitOps is the packaging tool.** CNCF Sandbox project, Red Hat
contributes to the ModelPack spec. `kit pack` in a Tekton task handles
all asset types through the Kitfile manifest. v1.12+ has native skill
detection. For skills specifically, the Thomas Vitale OCI spec (v0.1.0)
defines the artifact type and media types. Three competing OCI specs
exist (Vitale, skillctl/SkillImage from RH ET, KitOps) -- Red Hat
needs a position (01).

**4. SARIF is the scan output lingua franca.** All three scan layers
(SkillSpector static, Snyk ML-model, LLM reviewer) produce SARIF
v2.1.0. SARIF files attach to OCI artifacts as referrers via cosign.
Conforma evaluates SARIF-based attestation predicates. This is a
clean, standards-based chain from scan to policy gate (02).

**5. A custom in-toto predicate is needed.** The existing SLSA
Provenance and Vulnerability predicates don't capture agent-specific
scan results (SkillSpector categories, OWASP MCP coverage, toxic
flows). Define `rhoai.redhat.com/attestation/agent-security/v1` with
per-layer scan results and OWASP coverage (02).

**6. model-metadata-collection extends via flags first.** The Go tool
has no provider interface -- it uses flag-based invocation. Adding
`--skill-index` and `--skill-catalog-output` flags matches the existing
MCP server pattern and ships faster. Provider interface refactor is 3.7+
when agent support lands (01, 02).

**7. oc-mirror handles non-container OCI natively.** No model-specific
logic to generalize. Skills as OCI artifacts mirror through the same
`additionalImages` path in ImageSetConfiguration. Cosign signatures and
attestations travel automatically as OCI referrers. Air-gapped delivery
works via disk-to-mirror without modification (02).

**8. Three-phase implementation path.** Phase 1 (skills, 3.6): smallest
artifact, most urgent threat data, most mature tooling. Phase 2 (MCP
servers, 3.7): extends existing MCP metadata support, adds OWASP MCP
Top 10 scanning. Phase 3 (agents, 3.7+): composite scanning, agent
manifest spec. Each phase produces reusable infrastructure (attestation
predicates, Conforma patterns, metadata collection providers) for the
next (02).

**9. SkillSpector is pipeline-ready.** NVIDIA's scanner has SARIF
output, exit codes for CI gating, and a container image. Wrapping it as
a Tekton task is straightforward. The two-stage architecture (fast
static + optional LLM) maps to Tekton task steps. MCP scanning mode
exists but is less mature (01).

**10. Conforma policies are extensible without code changes.** ~40
existing release policy packages, all in Rego. Adding AI-asset-specific
policies (require SkillSpector PASS, require OWASP MCP coverage) is
Rego authoring against the custom attestation predicate (01, 02).

## Recommended follow-ups (not auto-run)

- **competitive lens** -- how do other vendors (JFrog, NVIDIA, AWS,
  Google) architect their AI asset trust pipelines? Feature matrix.
  Retry: `hub.research ai-asset-pipeline competitive`.
- **requirements lens** -- enterprise requirements for the pipeline:
  what do customers need? What do regulated industries demand? Retry:
  `hub.research ai-asset-pipeline requirements`.
- **hub.strategy ai-asset-pipeline** -- the living strategy doc
  synthesizes this research + knowledge into the WHAT/WHY, gaps and
  risks, and implementation roadmap.
