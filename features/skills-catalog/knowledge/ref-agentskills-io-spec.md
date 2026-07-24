---
type: reference
title: agentskills.io -- Agent Skills specification (AAIF/Linux Foundation)
description: The AAIF-governed Agent Skills specification -- defines SKILL.md directory structure, YAML frontmatter (name, description, license, compatibility, metadata, allowed-tools), progressive disclosure model; Apache 2.0, 170+ member orgs, 40+ supporting tools.
resource: https://agentskills.io/specification
tags: [skills-catalog, skills-registry, specification, standard, aaif]
features: [skills-catalog, skills-registry]
timestamp: 2026-07-23
review_after: 2026-10-23
source: skills-catalog research 01-upstream
---

The Agent Skills specification defines the SKILL.md standard for
portable agent skill packaging. Created by Anthropic (Dec 2025),
now governed by the Agentic AI Foundation (AAIF) under the Linux
Foundation. 170+ member organizations. Co-founders: Anthropic, OpenAI,
Block. Platinum members: AWS, Bloomberg, Cloudflare, Google, Microsoft.

Key elements: directory structure (SKILL.md + optional scripts/
references/assets), YAML frontmatter (name and description required,
license/compatibility/metadata/allowed-tools optional), progressive
disclosure model (discovery ~100 tokens -> activation <5,000 tokens ->
execution as needed).

40+ tools support the standard natively. 6 major agents parse SKILL.md:
Claude Code, Codex CLI, Cursor, Gemini CLI, Cline, OpenCode.
