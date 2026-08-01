---
title: "Skills Catalog research -- landscape and market patterns"
description: Three-layer taxonomy (catalog/registry/marketplace), Git-backed curation model, SKILL.md 40+ tools, SkillsBench quality data (curated +16.6pp, public 6.2/12), trust pipeline maturity (NVIDIA/JFrog/cloud policy engines), ARD v0.9 federated discovery, EU AI Act compliance, ClawHavoc supply-chain attacks, governance gap (96% run agents, 12% govern).
timestamp: 2026-07-23
lens: landscape
review_after: 2026-10-23
---

# Skills Catalog research -- landscape and market patterns

## 1. Taxonomy

The ecosystem has settled into a three-layer taxonomy:

- **Catalog/Directory**: read-only discovery (NVIDIA, Azure Agent
  Skills, Kubeflow Hub, skillmd.io)
- **Registry**: system of record with governance (MLflow, JFrog, Google
  Agent Registry, Credo AI)
- **Marketplace**: distribution + monetization (Anthropic ~600 skills,
  skills.sh 669K+, SkillsMP 1.9M, Salesforce AgentExchange, ClawHub)

The RHOAI catalog/registry separation aligns with this structure.

## 2. Implementation patterns

**Git-backed** (NVIDIA, Microsoft, Kubeflow Hub): dominant for
vendor-curated content. GitOps-native, auditable, disconnected-friendly.
No dynamic metadata (downloads, ratings).

**Database-backed** (MLflow, JFrog, Google): SQL/API querying, RBAC,
version lineage, audit trails. Required for governance.

**API-aggregated** (Kubeflow Hub, ARD): pluggable sources queried at
browse time. The future direction for federated discovery.

**Curation models**: vendor-curated (high trust, limited breadth),
community with review (moderate trust, Anthropic), community open (low
trust, ClawHub 8.5% malware), federated (variable per source).
SkillsBench: curated skills raise pass rates by +16.6pp. 73% of public
skills carry elevated safety risk. Curation is a prerequisite for
enterprise value.

## 3. Packaging standards

**SKILL.md**: ~40 platforms, AAIF-governed, progressive disclosure.
**APM** (Microsoft): git-based, 3.3K stars, SBOM, org-wide policy.
**LOLA** (Red Hat): convention-based, federated marketplace, Apache-2.0.
**npx skills** (Vercel): 669K+ indexed, 51+ agents, Snyk partnership.
**OCI Artifacts** (Vitale spec v0.1.0): Red Hat's strongest
enterprise/disconnected story; draft but architecturally sound.

Not mutually exclusive -- MLflow RFC-0008 PackageManagerPlugin supports
all via plugins.

## 4. Trust and verification

**Threat landscape**: ClawHavoc (1,184 malicious, 8.5% infection),
ToxicSkills (36% flaws, 76 credential-stealing), SkillsBench (73%
elevated safety risk).

**NVIDIA pipeline** (reference): SkillSpector (64 patterns, 16
categories) -> Skill Cards -> OMS signing (cosign/Sigstore) -> Skill
Evaluator (trigger accuracy, task completion, token efficiency).

**JFrog**: scan-verify-sign on upload, promotion model, NVIDIA
partnership (GTC 2026).

**Cloud policy engines**: AWS Cedar (GA, default-deny, MCP filtering),
Google semantic governance (NLC), Databricks service policies (beta).

**Table stakes**: static scanning, cryptographic signing, skill cards.
**Differentiator**: LLM semantic analysis, quality benchmarking, runtime
policy enforcement, federated trust verification.

## 5. Federated discovery (ARD)

ARD v0.9 (May 2026): open standard for publishing, discovering, and
verifying AI capabilities. Google, Microsoft, Hugging Face. Two
primitives: `ai-catalog.json` static manifests + registry search API.
Coalition: Cisco, Databricks, GitHub, GoDaddy, Google, HF, NVIDIA,
Salesforce, ServiceNow, Snowflake.

Early implementations: GitHub Agent Finder, HF Discover Tool, Google
Agent Registry. Near-zero public deployment. Worth tracking as a future
catalog source type, not betting on yet.

## 6. Market signals

- SKILL.md adopted by 16+ tools (standard)
- EU AI Act high-risk deferred to Dec 2027; Article 50 transparency
  obligations Aug 2 2026
- 1,184 malicious skills on ClawHub; scanning becoming table stakes
- 96% of enterprises run agents; 12% can govern them (OutSystems 2026)
- Every cloud shipped governance tooling in 2026
- MLflow unique positioning: open source, ML lifecycle integration,
  vendor-neutral, metadata-first

## Key findings

1. Git-backed is the right model for curated enterprise catalogs.
2. SKILL.md is the standard. Fighting it is swimming upstream.
3. Curation is the differentiator, not volume.
4. Trust pipeline is table stakes for enterprise.
5. OCI is the strongest Red Hat distribution story.
6. ARD worth tracking, not betting on.
7. Package managers coexist via plugins.
8. EU AI Act compliance is a tailwind.
9. Governance gap is the market opportunity.
