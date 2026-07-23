---
type: fact
title: NVIDIA skills ecosystem -- mature catalog, verification pipeline, complementary to MLflow
description: NVIDIA has the most mature public skills catalog (2.7K stars, 35+ products, OMS signing, SkillSpector scanning, Skill Evaluator, Tier-3 evals, BENCHMARK.md, agentskills.io compliance, 5+ marketplace syndications); complements MLflow (trust/quality layer, not a registry). JFrog already partnered at GTC 2026.
timestamp: 2026-07-23
tags: [skills-catalog, skills-registry, nvidia, competitive, signing, evaluation]
features: [skills-catalog, skills-registry]
review_after: 2026-10-23
source: NVIDIA/skills GitHub fetch + Aditi Saluja GDoc NVIDIA gap analysis
---

NVIDIA has built the most mature public skills ecosystem as of
2026-07-23. Their tools are **complementary to MLflow, not competing**
-- NVIDIA provides the trust and quality layer; MLflow provides the
registry foundation.

## Catalog (github.com/nvidia/skills)

2.7K stars, 299 forks, 448 commits. Apache 2.0 + CC-BY-4.0.
35+ product lines, hundreds of skills. Skills maintained in product
repos, mirrored daily via automated sync pipeline. Sync-time gates
enforce signature, card, and eval presence.

Distribution: `npx skills add nvidia/skills` with multi-agent support
(Claude Code, Codex, Cursor, Kiro, Snowflake CoCo). Syndicated to
Skills.sh, Codex plugin, Claude Code plugin, ClawHub, Hermes Hub.
Follows agentskills.io Agent Skills specification.

## Verification pipeline

| Layer | Tool | What it does |
|---|---|---|
| Scanning | SkillSpector | Prompt injection, tool poisoning, credential access, data exfiltration |
| Metadata | Skill Cards (SKILLCARD.yaml) | Structured author, license, dependencies, risks, verification status |
| Signing | OMS via cosign/Sigstore | Identity + integrity (not just content_digest hash) |
| Quality | Skill Evaluator | Trigger accuracy, task completion rate, token efficiency |

## MLflow gap (from Aditi's analysis)

MLflow RFC-0008 has no scanning, no SKILLCARD.yaml, only SHA-256
content_digest (no cryptographic signing), no quality benchmarks, no
verification pipeline. These are the gaps NVIDIA fills.

## Integration approach

NVIDIA tools run in CI/CD pipeline; results attach to MLflow skill
versions as structured metadata. Loosely coupled -- customers without
NVIDIA GPUs don't need it. No hard upstream dependency.

**Competitive signal**: JFrog has already partnered with NVIDIA at GTC
2026 for scanning, signing, and governance of skills used with
NemoClaw. This is a fast-moving space.
