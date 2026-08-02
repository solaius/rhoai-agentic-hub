---
type: question
title: Who runs the one-time SkillSpector security scan for 3.6 TP catalog skills?
status: open
description: The 30-35 EX skills entering the 3.6 TP catalog need a one-time SkillSpector scan (64 patterns, 16 categories) as the minimum viable security gate -- bypassing the full Konflux pipeline; scan ownership (EX CI vs RHOAI ProdSec) and results consumption unresolved.
timestamp: 2026-08-02
tags: [skills-catalog, ex, security, scanning, action-item]
components: [skills-catalog]
asks:
  - Peter Double (2026-08-02, research 09-requirements-refresh)
source: research 09-requirements-refresh §5, strategy.md Gaps & risks
---

The 3.6 TP catalog bypasses Konflux (acceptable for Red Hat-authored
skills), but still needs a security scan. SkillSpector (Apache 2.0,
NVIDIA, 64 vulnerability patterns across 16 categories including
prompt injection, tool poisoning, excessive agency) is the recommended
tool.

**Open questions**:
- Who runs it -- EX in their CI (they already have `make validate` and
  pre-commit hooks, adding SkillSpector is natural) or RHOAI ProdSec
  as a separate audit?
- Who reviews the results -- if EX runs it, does ProdSec still need to
  sign off for platformProvided trust tier?
- Where are results stored -- in the agentic-collections eval/ directory
  alongside existing eval reports, or in a separate scan-results
  artifact?
- What is the pass/fail threshold -- zero critical findings, or a
  risk-accept process for known patterns?

**Context**: Snyk ToxicSkills found 36% of community skills contain
flaws. EX skills are Red Hat-authored and likely cleaner, but the scan
is both a quality gate and a trust signal for the catalog.

**Related**: [fact-ex-onboarding-36-viable-without-konflux](/components/skills-catalog/knowledge/fact-ex-onboarding-36-viable-without-konflux.md),
[fact-skills-supply-chain-security](/components/skills-catalog/knowledge/fact-skills-supply-chain-security.md)
