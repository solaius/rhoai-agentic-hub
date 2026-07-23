---
type: reference
title: NVIDIA/skills -- verified agent skills catalog repo
description: NVIDIA's public skills catalog -- 2.7K stars, 35+ products (Physical AI, CUDA, RAG, robotics), OMS signing, skill cards, Tier-3 evals, BENCHMARK.md, npx distribution, daily sync from product repos, agentskills.io spec.
resource: https://github.com/nvidia/skills
tags: [skills-catalog, nvidia, competitive, github, signing, evaluation]
features: [skills-catalog, skills-registry]
timestamp: 2026-07-23
review_after: 2026-10-23
source: GitHub fetch 2026-07-23
---

The public NVIDIA agent skills catalog. Skills are maintained in
product repos and mirrored daily via an automated sync pipeline.
Apache 2.0 + CC-BY-4.0 licensed. 2.7K stars, 299 forks, 448 commits.

Key capabilities:
- **Distribution**: `npx skills add nvidia/skills` (v1.5.16+);
  multi-agent support (Claude Code, Codex, Cursor, Kiro, Snowflake CoCo)
- **Signing**: every skill ships with `skill.oms.sig` (OMS signature
  verifiable against `nv-agent-root-cert.pem` via model-signing/cosign)
- **Quality**: Tier-3 evaluation datasets required; `BENCHMARK.md`
  with verifiable uplift data
- **Metadata**: `skill-card.md` per skill (identity, provenance,
  quality, behavioral boundaries)
- **Compliance**: sync-time gates enforce signature, card, and eval
  presence; missing artifacts = skill not published
- **Syndication**: Skills.sh, Codex plugin, Claude Code plugin,
  ClawHub, Hermes Hub; additional MCP hubs planned
- **Spec compliance**: follows agentskills.io Agent Skills
  specification (SKILL.md with YAML frontmatter)

Roadmap items all marked [completed] except "syndication to additional
MCP hubs" [planned]. This is the most mature public skills catalog in
the ecosystem as of 2026-07-23.
