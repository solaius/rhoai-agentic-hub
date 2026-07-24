---
type: reference
title: NVIDIA Verified Agent Skills -- trust pipeline deep-dive (Adel GDoc)
description: Adel's deep-dive on NVIDIA's 6-stage trust pipeline for agent skills -- SkillSpector (68 vuln patterns, 17 categories), NVSkills-Eval (3-tier, benchmark scores per agent), Skill Card Generator (structured governance cards), OMS signing (cryptographic provenance). Informational reference, not necessarily our direction.
resource: https://docs.google.com/document/d/1ME7-fjHRQow8FgNkvI2R0PWXCSq3x7sJzdpe-FJGIiw
tags: [skills-catalog, skills-registry, nvidia, trust, scanning, signing, evaluation, competitive]
features: [skills-catalog, skills-registry]
timestamp: 2026-07-24
review_after: 2026-10-24
source: Adel, shared 2026-07-24; published May 2026
---

Adel's write-up of NVIDIA's Verified Agent Skills trust pipeline.
Covers the full 6-stage flow: source repo, review, scan (SkillSpector),
evaluate (NVSkills-Eval), skill card, sign (OMS), catalog, and
marketplace syndication.

Key detail beyond what existing landscape entries capture:

- **SkillSpector**: 68 vulnerability patterns across 17 categories
  (prompt injection, data exfiltration, privilege escalation, supply
  chain, excessive agency, tool poisoning, MCP least privilege, trigger
  abuse, memory poisoning, system prompt leakage, rogue agent behavior,
  dangerous code/AST, taint tracking, YARA signatures, output handling,
  anti-refusal, live CVE lookup). Intent-layer analysis compares
  declared purpose against actual behavior.
- **NVSkills-Eval**: 3-tier (static validation, dedup, agent-based).
  Tier 3 dimensions: security, correctness, discoverability,
  effectiveness, efficiency. Published benchmark for skill-card-generator
  shows Claude Code vs Codex scores.
- **Skill Card Generator**: automated via discover_assets.py, agent
  context build, render_card.py, human review, validate_submission.py.
- **OMS signing**: detached skill.oms.sig covering all files; verifiable
  against nv-agent-root-cert.pem via model-signing.
- **Runtime vs capability framing**: runtime controls (OpenShell,
  NemoClaw, NeMo Guardrails) govern execution; verified skills govern
  what enters the workflow before execution.

Status: informational. Not necessarily our direction, but awareness of
the most mature public trust pipeline in the skills space.

See also: [[fact-nvidia-skills-catalog-landscape]],
[[ref-nvidia-skills-repo]], [[ref-agentskills-io-spec]],
[[question-skills-catalog-nvidia-collaboration]]
