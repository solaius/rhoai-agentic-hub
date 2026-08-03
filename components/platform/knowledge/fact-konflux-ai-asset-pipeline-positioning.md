---
type: fact
title: Konflux AI asset supply chain pipeline is shared platform infrastructure
description: The Konflux pipeline for scanning, signing, attesting, and OCI-packaging AI assets (skills, MCP servers, agents) is shared platform infra upstream of both catalog and registry -- not a feature of either; artifact-type-aware scan profiles, shared output contract; first target skills, extend to MCP+agents; belongs under RHAISTRAT-1339 or new cross-cutting STRAT.
timestamp: 2026-08-02
tags: [platform, konflux, supply-chain, skills-catalog, mcp-catalog, agent-catalog, architecture]
components: [platform, ai-asset-pipeline, skills-catalog, mcp-catalog, agent-catalog]
review_after: 2026-11-02
source: session analysis 2026-08-02, synthesized from Ann Marie Fred architectural strategy GDoc + competitive/architecture research
---

The Konflux AI asset supply chain pipeline is **shared platform
infrastructure**, not a catalog or registry feature. It sits upstream
of both:

```
Git repo (asset source)
  → Konflux pipeline (scan, sign, attest, package as OCI)
      → Catalog (indexes trust metadata for discovery)
      → Registry (tracks governance state, relationships, usage)
      → Quay/oc-mirror (distributes the artifact, disconnected)
```

The catalog doesn't scan or sign -- it displays trust status. The
registry doesn't scan or sign -- it records governance decisions. The
pipeline does the actual security work. Neither owns it; both consume
its outputs.

## Cross-asset architecture

The same pipeline applies to all three AI asset types with
artifact-type-specific scan profiles:

| Artifact | Scan profile | Threat focus |
|---|---|---|
| Skills | SkillSpector patterns (68 vuln, 17 categories) | NL malware, prompt injection, memory alteration |
| MCP servers | OWASP MCP Top 10 | Tool poisoning, credential theft, unauthorized network |
| Agents | Composite (skills + MCP + harness-specific) | All of the above plus harness risks |

**Shared output contract**: every artifact type produces OCI artifact +
cosign signature + in-toto attestation + SBOM. Catalog, registry, and
Quay all consume these the same way.

**Build as one shared artifact-type-aware pipeline**, not three separate
pipelines. Same Tekton infrastructure, pluggable scan task per type.

## Implementation path

First implementation targets **skills** (smallest artifact, most urgent
threat data -- 36.8% of public skills have security flaws). Extends to
MCP servers and agents once the shared infrastructure is proven.

## Organizational home

Belongs under **RHAISTRAT-1339** (AI Hub AI Asset Delivery for Agentic
Solutions -- the umbrella Outcome) or as a **new cross-cutting
RHAISTRAT** for AI asset supply chain security. Does not belong under
any single asset type's STRAT.

**Update 2026-08-03**: Adam Bellusci (AI Hub owner) confirmed
extend-existing-pipeline direction. Now tracked as the
[ai-asset-pipeline](/components/ai-asset-pipeline/) component. See
[decision-extend-existing-model-pipeline](/components/ai-asset-pipeline/knowledge/decision-extend-existing-model-pipeline.md).

**Current gap**: this work is not yet planned in Jira. Epic-sized. See
[fact-skills-supply-chain-security](/components/skills-catalog/knowledge/fact-skills-supply-chain-security.md)
for the threat landscape and mitigation plan detail.
