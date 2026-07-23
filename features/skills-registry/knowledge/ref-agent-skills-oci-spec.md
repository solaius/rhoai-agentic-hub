---
type: reference
title: Agent Skills OCI Artifacts Spec (v0.1.0)
description: Draft spec for packaging AI agent skills as OCI artifacts — custom media types, OCI Image Index as collection catalog, skills.json/skills.lock.json for version pinning. v0.1.0, Thomas Vitale.
resource: https://github.com/ThomasVitale/agents-skills-oci-artifacts-spec
timestamp: 2026-07-23
tags: [skills-registry, oci, packaging, spec]
features: [skills-registry]
---

Defines how to package agent skills as OCI manifests: config blob with
structured JSON metadata (extracted from SKILL.md frontmatter — name,
version, license, compatibility, allowed-tools), a single tar+gzip
content layer, custom media types
(`application/vnd.agentskills.skill.v1`), and semver tags. An OCI Image
Index serves as a browsable collection catalog referencing skill
artifacts by digest.

`skills.json` / `skills.lock.json` pair manages version pins and digest
reproducibility (analogous to package.json / package-lock.json).

v0.1.0 draft. Follows established OCI artifact patterns (Helm charts,
Crossplane packages, WASM modules, Sigstore signatures). Would leverage
Red Hat's existing infrastructure (Quay.io, OpenShift internal registry,
oc-mirror for air-gapped, cosign signing).

See [fact-skills-packaging-landscape](/features/skills-registry/knowledge/fact-skills-packaging-landscape.md)
for comparative analysis.
