---
type: fact
title: Skills registry/catalog competitive landscape (2026-07-21)
description: Comprehensive competitive landscape -- cloud platforms (AWS AgentCore, Azure Agent 365, Google Gemini Enterprise, Databricks Unity AI), frameworks (Anthropic Marketplace ~600 skills, skills.sh 669K+, HF 40K+ with ARD spec, LangChain/LangSmith), security specialists (JFrog+NVIDIA, Cisco DefenseClaw, Credo AI, Zenity, TrueFoundry); SKILL.md is the standard (16+ tools), EU AI Act high-risk Aug 2 2026.
timestamp: 2026-07-21
tags: [skills-catalog, skills-registry, competitive, landscape]
features: [skills-catalog, skills-registry]
review_after: 2026-10-21
source: Aditi Saluja status/scope/roadmap GDoc
---

The skills registry/governance space has exploded in 2026. Every major
cloud, multiple agent frameworks, and several startups are building
skills management. EU AI Act high-risk rules land August 2, 2026 (fines
up to EUR 15M / 3% of global turnover).

## Cloud platforms

- **AWS AgentCore** (preview): Agent Registry, Cedar policies
  (default-deny), Gateway enforcement, EventBridge audit trail. No
  skills-specific scanning/signing.
- **Microsoft Agent 365**: Agent Registry, 133 official skills, Entra
  Agent ID (OAuth2), shadow agent discovery via Defender/Intune across
  20+ agent types.
- **Google Gemini Enterprise**: Skill Registry + Agent Registry + Agent
  Gateway with Model Armor, cryptographic agent identity, Apigee-to-MCP
  bridge. Three-layer architecture.
- **Databricks**: Unity AI Gateway extends Unity Catalog to
  agents/tools/skills. OpenSharing standard (Linux Foundation).

## Agent frameworks and marketplaces

- **Anthropic**: Skills Marketplace (~600 skills), created the SKILL.md
  standard adopted by 16+ tools, 15% revenue share on paid skills. No
  enterprise governance.
- **Vercel skills.sh**: 669K+ skills indexed, 51 agent support, Snyk
  scanning partnership. Minimal curation; security bypasses reported.
- **Hugging Face**: 40K+ public skills, ARD spec (with Microsoft +
  Google) for federated discovery. 46.3% duplicate rate, no governance.
- **LangChain/LangSmith**: Skills boost Claude Code on LangSmith tasks
  from 17% to 92%. No scanning/signing.
- **OpenAI**: Codex skills, Connector Registry, AgentKit. Skills
  default-on for Enterprise from July 2026.

## Security and governance specialists

- **JFrog**: Agent Skills Registry + NVIDIA trust layer. Already
  partnered at GTC 2026.
- **NVIDIA**: SkillSpector, Skill Cards, Skill Evaluator, OMS signing.
  Trust/quality layer, not a registry.
- **Cisco DefenseClaw**: OSS scanner, AI BOM, MCP Catalog, Zero Trust.
- **Credo AI**: Agent Registry, agent cards, GAIA governance. Gartner
  Visionary (June 2026).
- **TrueFoundry**: Agent Skills Registry with versioning, RBAC, GitOps.
  $499/mo. Launched May 2026.

## Key signals

- SKILL.md is the emerging standard (Anthropic, Dec 2025; 16+ tools)
- MCP is the connectivity standard (spec v2026-07-28)
- ARD (Hugging Face + Microsoft + Google) for federated discovery
- 1,184 malicious skills discovered on ClawHub; scanning becoming
  table stakes
- MLflow unique positioning: open source, ML lifecycle integration,
  vendor-neutral, metadata-first
