---
type: reference
title: Microsoft APM (Agent Package Manager)
description: Microsoft's open-source agent dependency manager — apm.yml manifest, git-based distribution, multi-client targeting, org-wide policy governance. Must-have for Databricks in the MLFlow skills registry plugin architecture.
resource: https://github.com/microsoft/apm
timestamp: 2026-07-23
tags: [skills-registry, apm, microsoft, packaging]
features: [skills-registry]
---

Agent Package Manager. Manifest-driven (`apm.yml` + `apm.lock.yaml`),
git-based distribution (no centralized registry), compiles to 8+ agent
clients. Enterprise features: SBOM export, org-wide policy governance,
drift detection, content security scanning. 3.3K stars, v0.26.0
(Jul 2026), MIT licensed.

Maintained by Daniel Meppiel and Sergio Sisternes (Microsoft).
Explicitly named in MLFlow RFC-0008 (PR #26) as a reference package
manager plugin alongside LOLA.

See [fact-skills-packaging-landscape](/features/skills-registry/knowledge/fact-skills-packaging-landscape.md)
for comparative analysis.
