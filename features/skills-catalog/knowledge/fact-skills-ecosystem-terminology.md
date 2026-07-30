---
type: fact
title: Skills ecosystem terminology -- precision definitions for RH context
description: Agreed definitions for skills ecosystem terms as used across RH teams -- Agent Skill, Plugin, Marketplace, Skill Bundle, Skill Card, Skill Signature, Installed Skill, Code/Artifact Repository, Package Manager; avoids ambiguity in cross-team discussions.
timestamp: 2026-07-30
tags: [skills-catalog, skills-registry, terminology, definitions]
features: [skills-catalog, skills-registry]
review_after: 2026-12-30
source: Ann Marie Fred architectural strategy GDoc (July 2026) -- "Naming is hard" section
---

Definitions as used in the RHOAI skills architecture. The area is
evolving and there is disagreement about what certain terms mean -- these
are the working definitions from Ann Marie Fred's cross-team strategy
doc.

- **Agent Skill**: a folder containing a SKILL.md file with metadata
  (name, description) and instructions for a specific task. May bundle
  scripts, references, templates. Defined at agentskills.io.

- **Plugin**: Anthropic, OpenAI, and Microsoft's packaging concept --
  bundles skills, MCP servers, and related functionality into one
  artifact to avoid folder collisions and enable coherent installation.

- **Marketplace**: a `marketplace.json` file listing plugins, hosted on
  a git server. Anthropic, OpenAI, and Copilot all use this pattern.

- **Skill Bundle**: Hermes concept -- bundles of related skills that
  work together. Similar to Plugin. Used in the MLflow skill registry
  RFC because MLflow already has a "plugin" concept.

- **Skill Card**: non-standardized markdown file in the skill root with
  human-readable metadata about the skill and testing performed. Similar
  to Model Card. NVIDIA example:
  github.com/NVIDIA/skills/blob/main/skills/cudaq-guide/skill-card.md

- **Skill Signature**: cryptographic signature proving trusted supply
  chain of the signing party. NVIDIA presents these in the skill folder
  (`.oms.sig` files).

- **Installed Skill**: written to a location on disk where the agent
  automatically loads it into context at session start. Location is
  harness-specific (configuration folder or project skills subfolder).

- **Skill Catalog** (RHOAI): curated list of recommended, validated
  skills. Kubeflow hub surface. Discovery-focused. Cluster-level,
  admin-managed. NOT the agentskills.io "catalog" (which means loaded
  skills for the session).

- **Skill Registry** (RHOAI): MLflow metadata store tracking build,
  version, and usage of skills. Namespace-level, project-scoped. Tracks
  relationships between skills, agents, observability data, evaluations.

- **Code Repository**: any repo that might contain a skill (GitHub,
  GitLab).

- **Artifact Repository**: any repo for container images, OCI artifacts,
  zips, signatures (Quay, Nexus, Artifactory).

- **Package Manager**: tool to install and manage dependencies (PyPI,
  npm, Lola, APM).
