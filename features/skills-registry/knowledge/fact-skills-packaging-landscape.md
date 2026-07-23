---
type: fact
title: Skills packaging landscape — 4 package manager options for MLFlow registry
description: Comparative analysis of APM (Microsoft, must for Databricks), LOLA (Red Hat, must for RH), NPM/NPX (general standard), and OCI artifacts (under discussion) as package manager plugins for the MLFlow skills registry (RFC-0008).
timestamp: 2026-07-23
tags: [skills-registry, packaging, apm, lola, npm, oci, mlflow]
features: [skills-registry, agent-catalog]
source: research session 2026-07-23; GitHub repos, MLFlow RFC PR #26
review_after: 2026-10-23
---

MLFlow RFC-0008 (PR #26, authored by Red Hat's Bill Murdock) defines a
`PackageManagerPlugin` interface: the registry handles governance,
discovery, and tracing; package managers handle harness-specific
installation via plugins registered through Python entrypoints. Four
package managers are under consideration.

## APM — Agent Package Manager (Microsoft)

- **Repo**: https://github.com/microsoft/apm
- **Model**: git-based dependency manager. `apm.yml` manifest declares
  skills, prompts, hooks, MCP servers. `apm.lock.yaml` pins with
  integrity hashes. No centralized registry — pulls from git repos.
- **Multi-client**: compiles to GitHub Copilot, Claude Code, Cursor,
  Codex, Gemini, Windsurf, Kiro, OpenCode.
- **Enterprise**: SBOM export (CycloneDX/SPDX), org-wide policy
  governance (`apm-policy.yml`), drift detection, content security
  scanning. Air-gapped friendly (git-based, no registry dependency).
- **Maturity**: 3.3K stars, 30 contributors, v0.26.0 (Jul 2026). MIT.
- **RFC fit**: explicitly named as reference plugin. Covers the git
  distribution channel natively. No OCI support.
- **Priority**: **must** — Databricks wants APM support.

## LOLA (Red Hat Product Security)

- **Repo**: https://github.com/LobsterTrap/lola
- **Model**: convention-based auto-discovery (no manifest file needed).
  Modules contain `skills/` with SKILL.md files. Federated marketplace
  model — YAML catalogs listing modules. Official marketplace hosted
  under RedHatProductSecurity. `.lola-req` for version constraints.
- **Multi-client**: Claude Code, Copilot CLI/VS Code, Cursor, Gemini
  CLI, OpenCode. Handles path rewriting and format translation per
  assistant.
- **Enterprise**: Apache-2.0, OpenSSF Best Practices badge, SBOM,
  governance doc. No OCI, no content signing, no documented air-gapped
  workflow beyond local paths.
- **Maturity**: 109 stars, 19 contributors, v0.7.0 (Jul 2026). Pre-1.0.
- **RFC fit**: explicitly named as reference plugin alongside APM. The
  RPM-to-DNF analogy: "your skill is the RPM, LOLA is the DNF."
- **Priority**: **must** — Red Hat maintains LOLA and authored RFC-0008.
  Vertically integrated story: MLflow for governance, LOLA for install.

## NPM / NPX (general standard)

- **Model**: registry-backed tarballs, `package.json` manifest, semver,
  scoped packages (`@org/pkg`). `npx` runs without permanent install.
- **Already de facto**: MCP servers distribute via npm (2M+ weekly
  downloads for `@modelcontextprotocol/sdk`). LangChain ships skills
  installable via `npx skills`. 200+ MCP packages on npm.
- **Enterprise**: private registries (Artifactory, Verdaccio, GitHub
  Packages), air-gapped via tarballs or Verdaccio mirror, `npm audit`
  for vulnerability scanning, Sigstore provenance attestations.
- **RFC fit**: clean plugin mapping — `npm install` from local tarball
  or directory, no registry round-trip needed. `package-lock.json`
  maps to `mlflow-skills.lock`.
- **Cons**: not purpose-built for AI skills — no native model
  compatibility or harness requirement metadata. JavaScript-centric.
- **Priority**: **standard inclusion** — massive ecosystem, already the
  MCP transport layer.

## OCI Artifacts (under discussion)

- **Model**: OCI Distribution Spec v1.1. Skills as OCI manifests with
  custom media types, content-addressable layers, semver tags. The
  Agent Skills OCI Artifacts Spec (v0.1.0, ThomasVitale) defines the
  structure.
- **Enterprise**: Red Hat's core competency. Quay.io, OpenShift
  internal registry, Konflux pipelines, cosign/sigstore signing, SBOM
  attachment, `oc-mirror` for disconnected environments. Single
  artifact store for images, models, and skills.
- **RFC fit**: pluggable backend for bundle storage. MLflow resolves
  metadata; OCI distributes. Same governance overlay works across
  air-gapped mirrors.
- **Cons**: more complex than file-based distribution, no native
  "install" concept (needs ORAS/crane tooling), heavier for simple
  skill files, less familiar to data scientists.
- **Priority**: **under discussion** — strongest enterprise/air-gapped
  story but less community momentum than APM/LOLA.

## Strategic view

The plugin architecture means these are **not mutually exclusive**.
RFC-0008 envisions multiple plugins coexisting. The question is which
to ship as supported plugins and in what order:
1. APM + LOLA (must — named in the RFC, sponsor requirements)
2. NPM (standard — already the ecosystem default for MCP)
3. OCI (Red Hat advantage — strongest disconnected/supply-chain story)
