---
type: reference
title: "NVIDIA SkillSpector -- agent skills security scanner"
description: Open-source scanner (Apache 2.0) with 68 vulnerability patterns across 17 categories -- AST analysis, taint tracking, YARA signatures, optional LLM semantic analysis; SARIF output for CI integration; reference implementation for the skills scan profile in the AI asset pipeline.
resource: https://github.com/NVIDIA/SkillSpector
tags: [ai-asset-pipeline, scanning, nvidia, skills, security]
components: [ai-asset-pipeline, skills-catalog]
timestamp: 2026-08-03
source: Ann Marie Fred architectural strategy GDoc + session research 2026-08-02
---

NVIDIA's open-source agent skills scanner. Two-stage pipeline: fast
static analysis (no API key needed) plus optional LLM evaluation.
Grounded in OWASP LLM Top 10 and MITRE ATLAS.

Integrates into NVIDIA's Verified Skills publishing flow. Outputs SARIF
for CI/CD integration. Ramesh Reddy expressed interest in sharing the
framework (Ann Marie Fred architectural strategy GDoc comments).

The reference implementation for the skills scan profile in the AI asset
pipeline. Would be integrated as a Tekton task in Konflux.
