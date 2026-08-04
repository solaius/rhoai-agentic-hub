---
title: Skills Catalog Landscape Refresh (August 2026)
description: UIE/Compass discovery (300+ engineers, gold/silver scorecards, marketplace publishing), OCP5 operator-gated distribution model, NVIDIA catalog growth (2.8K stars, 300+ skills, SkillSpector Aug 3 update), catalog.redhat.com/en/ai launched (4 packs + 2 skills + 6 MCP servers), RHEcosystemAppEng/agentic-collections revealed (48 stars, 7 packs, 68 skills), skills.sh hits 600K+ with Snyk partnership, Kubeflow KEP-0005 status (no evidence of merge).
timestamp: 2026-08-04
lens: landscape
review_after: 2026-11-04
---

# Skills Catalog Landscape Refresh (August 2026)

## Context

This refresh updates [02-landscape](/components/skills-catalog/research/02-landscape.md) with changes discovered between August 2-4, 2026. The primary catalyst: discovery of Red Hat's UIE (Unified Intelligence Engineering) organization and the Compass skills registry during internal alignment meetings, revealing parallel Red Hat skill governance efforts unknown to the RHAI team.

## 1. Red Hat Internal: UIE/Compass Discovery

### What We Learned

Red Hat operates a **300+ engineer Unified Intelligence Engineering (UIE) organization** with a skills governance platform called **Compass**. Key capabilities reported in internal meetings (Aug 4):

- **Skills registry with security auditing**
- **Scorecard system**: gold tier (public-ready), silver tier (internal-only)
- **Marketplace publishing**: skills flow from Compass to Claude/ChatGPT/Gemini marketplaces
- **Light Trail team**: builds MCP server hosting infrastructure on Managed Platforms (MP+)

### Public Search Results: No Confirmation

Web searches for "Red Hat UIE Unified Intelligence Engineering Compass skills registry" returned **no public documentation** of Compass as a distinct product. The only "UIE" result was InsightFinder's unrelated "Unified Intelligence Engine" for IT ops. Red Hat AI engineering initiatives and the [agentic skills repository announcement](https://thenewstack.io/red-hat-agentic-skills-repository/) at Summit 2026 are public, but no mention of "Compass" or a scorecard-based registry appears in external sources.

### Status: Internal Only

Compass appears to be an **internal Red Hat capability** not yet publicly documented. Greg Bowman (marketplace strategy) is arranging a Compass alignment session with the RHAI team. This discovery changes the landscape: instead of three independent Red Hat skill sources (EX agentic-plugins, openshift/agentic-skills, opendatahub-io/ai-helpers), there may be a **fourth governance layer** above them.

### Implications

1. **Potential consolidation path**: Compass could serve as the single registry backing catalog.redhat.com/en/ai, with RHOAI skills catalog federating from it.
2. **Scorecard adoption**: Gold/silver tiering aligns with the trust tier model proposed in [09-requirements-refresh](/components/skills-catalog/research/09-requirements-refresh.md) (`platformProvided`, `verified`, `community`).
3. **Duplication risk**: If RHOAI builds MLflow-based registry and Compass exists, Red Hat would operate two skill registries without a clear boundary.
4. **Light Trail + MCP**: MCP server hosting on MP+ could become the distribution channel for Red Hat MCP servers currently listed on catalog.redhat.com/en/ai.

**Action required**: Attend Compass alignment session; determine whether RHOAI skills catalog integrates with Compass or operates independently.

## 2. Red Hat Public: catalog.redhat.com/en/ai Launched

### Current Inventory

Red Hat's [AI catalog](https://catalog.redhat.com/en/ai) is **live and public** as of August 2026. Complete listing:

**Agentic Skill Packs (4)**:
- [Agentic skill pack for Red Hat customers](https://catalog.redhat.com/en/ai/skills/detail/agentic-skill-pack-for-red-hat-customers) (Site Reliability)
- [Agentic skill pack for Site Reliability Engineers](https://catalog.redhat.com/en/ai/skills/detail/agentic-skill-pack-for-site-reliability-engineers) (Site Reliability)
- [Agentic skill pack for Red Hat OpenShift](https://catalog.redhat.com/en/ai/skills/detail/agentic-skill-pack-for-red-hat-openshift) (Site Reliability, **Developer Preview**, 3 skills: cluster-creator, cluster-inventory, cluster-report)
- [Agentic skill pack for Red Hat OpenShift Virtualization](https://catalog.redhat.com/en/ai/skills/detail/agentic-skill-pack-for-red-hat-openshift-virtualization) (Site Reliability)

**Agentic Skills (2)**:
- Best practices AI skill for Red Hat Enterprise Linux (Administration)
- Translator AI skill for Red Hat Enterprise Linux (Administration)

**MCP Servers (6)**:
- MCP server for Red Hat Enterprise Linux (Administration, Troubleshooting)
- MCP server for Red Hat OpenShift (Administration)
- Ansible Automation Platform MCP image (Administration, **Tech Preview** indicated by URL path)
- Red Hat Lightspeed MCP server (Administration)
- Satellite MCP server (Administration)
- Two "Coming soon" placeholders for additional skills and MCP servers

**Provider**: All items are Red Hat-provided. **Support model**: Included with Red Hat subscription.

### Relationship to RHEcosystemAppEng/agentic-collections

The [OpenShift skill pack detail page](https://catalog.redhat.com/en/ai/skills/detail/agentic-skill-pack-for-red-hat-openshift) references the source repository as [RHEcosystemAppEng/agentic-collections](https://github.com/RHEcosystemAppEng/agentic-collections), described as the "source repository for this skill pack and the broader skill packs catalog."

**Discrepancy**: The GitHub repository name is `agentic-collections`, but catalog.redhat.com sources from it while [08-upstream-refresh](/components/skills-catalog/research/08-upstream-refresh.md) tracked `RHEcosystemAppEng/agentic-plugins` (68 skills). Fetching the GitHub page revealed these are **the same repository** — it may have been renamed, or the naming inconsistency reflects internal vs external branding.

### RHEcosystemAppEng/agentic-collections Details

**Repository stats** (as of Aug 2026):
- 48 stars, 29 forks
- 582 commits on main branch
- Apache 2.0 licensed
- Maintained by Red Hat Ecosystem Engineering

**Structure**: Monorepo with 7 skill packs containing **68 total skills**:

| Pack | Skills | Notes |
|------|--------|-------|
| rh-sre | 13 | Site Reliability Engineers |
| rh-developer | 14 | Developers |
| rh-virt | 10 | Virtualization Administrators |
| ocp-admin | 3 | OpenShift Administrators |
| rh-ai-engineer | 11 | AI/ML Engineers |
| rh-automation | 11 | Automation specialists |
| rh-basic | 6 | Basic Red Hat skills |

**Governance**: Automated validation via GitHub Actions (Tier 1 and Tier 2 checks), pre-commit hooks with gitleaks, `CONTRIBUTING.md`, `CODEOWNERS`, `MAINTAINERS` files, and `SKILL_DESIGN_PRINCIPLES.md`. Skills validated against DP1-DP7 design principles. Recommended contribution workflow: run `/agentic-contribution-skill` in Claude Code.

**Distribution**: Pre-packaged ZIP downloads via GitHub Releases for upload to ChatGPT Custom GPT, Claude. Skill packs designed for Claude Code, Cursor, and OpenShift Dev Spaces.

**Catalog UI**: Separate browsable catalog at [rhecosystemappeng.github.io/agentic-catalog](https://rhecosystemappeng.github.io/agentic-catalog), powered by the [agentic-catalog](https://github.com/RHEcosystemAppEng/agentic-catalog) project. The README states: "This repo is where skills are authored and maintained. The catalog aggregates content from here periodically."

### Federation Risk Confirmed

[08-upstream-refresh](/components/skills-catalog/research/08-upstream-refresh.md) flagged catalog.redhat.com/en/ai as a "parallel surface with federation risk." This refresh confirms the risk is **real**:

- catalog.redhat.com/en/ai lists 4 skill packs + 2 skills + 6 MCP servers
- RHEcosystemAppEng/agentic-collections contains 7 skill packs with 68 skills
- openshift/agentic-skills contains 2-3 skills (cluster-update, find-token)
- opendatahub-io/ai-helpers exists in the Claude Code marketplace (unknown skill count)

**No evidence of a single registry backend.** The RHOAI Kubeflow hub-based skills catalog, when built, will be a **fifth surface** unless federation or consolidation occurs.

## 3. OpenShift 5 Operator-Gated Distribution Model

### What We Learned

Internal sources (Ju Lim, Aug 4 meetings) confirmed **OCP5 will ship agentic skills as part of the core payload and via layered product operators**:

- **Core payload**: Base agentic skills packaged as a single container image in the OpenShift 5 core distribution
- **Operator-gated**: Product-specific skills (e.g., troubleshooting skills) ship with their corresponding operator (e.g., observability operator)
- **Availability model**: A skill is available to agents only if the operator providing it is installed on the cluster

### Public Search Results: No OCP5 Evidence

Searches for "OpenShift 5 OCP5 agentic skills operator distribution 2026" returned **no mention of OpenShift 5 or OCP5**. Results focused on:

- [openshift/agentic-skills](https://github.com/openshift/agentic-skills) repository (confirmed active, 39 commits)
- [Agentic skill pack for Red Hat OpenShift](https://catalog.redhat.com/en/ai/skills/detail/agentic-skill-pack-for-red-hat-openshift) (3 skills for cluster lifecycle)
- [Red Hat OpenShift roadmap for 2026](https://tv.redhat.com/detail/6397335514112/red-hat-openshift-roadmap-your-intelligent-application-platform-for-2026-and-beyond) (no mention of agentic skills in search results)

OpenShift 4.20, 4.21, 4.22 are the current/upcoming versions referenced in public sources. "OpenShift 5" may be an internal code name or a future-dated initiative not yet publicly announced.

### Implications for Skills Catalog

If OCP5 ships skills via operators, **skills become Kubernetes resources** with lifecycle tied to operator installation. This creates a potential integration point:

- **Dynamic catalog source**: Kubeflow hub could query installed operators and dynamically surface their skills
- **K8s-native RBAC**: Skill access control aligns with operator RBAC, leveraging OpenShift's existing identity model
- **Versioning**: Skill versions match operator versions, automatically tracked in cluster state

**Risk**: If RHOAI skills catalog and OCP5 operator-based distribution operate independently, users see two disjoint skill inventories — one in the RHOAI catalog UI, another in the OpenShift operator ecosystem.

**Recommendation**: Coordinate with OCP5 skills architecture team to ensure Kubeflow hub can federate operator-provided skills as a catalog source.

## 4. NVIDIA Skills Catalog Maturation

### Repository Growth

The [nvidia/skills](https://github.com/nvidia/skills) repository shows significant maturation:

- **2,800 stars** (up from "2.7K+" in prior references)
- **324 forks**, 18 watchers
- **489 commits**
- **~300+ individual skills** across 35+ product areas

### Product Coverage Expansion

Skills now span: AIQ, CUDA-Q, cuDF, cuOpt, cuPyNumeric, DALI, Data Designer, DeepStream, Digital Health, **DOCA** (~55 skills alone), Dynamo, Earth2Studio, Holoscan SDK, Holoscan Sensor Bridge, Isaac for Healthcare Workflows, Jetson BSP, Jetson Device, Medical AI Skills, Megatron-Core, NeMo AutoModel, **NeMo MBridge** (~20 skills), NeMo Platform, NeMo Relay, NeMo Retriever, NeMo-RL, NemoClaw, Nemotron, Nemotron Speech, Physical AI, PhysicsNeMo, Portfolio Optimization, RAG Blueprint, Skill Card Generator, **TAO Toolkit** (~50+ skills), TileGym, and Video Search & Summarization.

Bolded areas represent significant concentrations of skills, suggesting prioritization of DOCA (networking/DPU), NeMo MBridge (multimodal), and TAO Toolkit (transfer learning).

### Governance Pipeline: Production-Ready

Every skill in the catalog ships with:
- `skill.oms.sig` — OMS signature verifiable against `nv-agent-root-cert.pem`
- `skill-card.md` — skill identity and governance card (machine-readable metadata)
- Tier-3 evaluation dataset
- `BENCHMARK.md` — verifiable benchmark uplift data

**Sync pipeline enforcement**: Signature drift detection and missing-artifact enforcement are marked as **completed** roadmap items. The daily sync from product repos to the public catalog now includes automated compliance gates.

### Roadmap Status

**Completed (✅)**:
- Public catalog, automated daily sync, security scanning, skill signing, universal evaluation criteria, skill cards, sync-time compliance gates
- **Syndication to external marketplaces**: Skills.sh, Codex plugin, Claude Code plugin, ClawHub, Hermes Hub

**Pending (🔲)**:
- Syndication to additional MCP hubs and partner channels

### SkillSpector August 3 Update

A [Help Net Security article dated August 3, 2026](https://www.helpnetsecurity.com/2026/08/03/skillspector-open-source-agent-skill-security-scanner/) provides the latest SkillSpector details:

**Detection capabilities**:
- **68 vulnerability patterns** across 17 categories (updated from "64 patterns, 16 categories" in prior docs)
- Categories: prompt injection, data exfiltration, privilege escalation, supply chain, excessive agency, output handling, system prompt leakage, memory poisoning, tool misuse, rogue agent, anti-refusal, trigger abuse, dangerous code (AST), taint tracking, YARA signatures, MCP least privilege, MCP tool poisoning
- Detects homoglyphs, right-to-left overrides, zero-width characters, hidden HTML directives
- Dependency checking via batched queries to OSV.dev with one-hour caching; built-in list for air-gapped environments

**Two-stage architecture**:
1. **Static analysis** (default, no API key): AST walking, taint tracking, YARA rules — fast, offline-capable
2. **LLM-enhanced pass** (optional, `--no-llm` to skip): OpenAI-compatible endpoint (defaults to NVIDIA's build.nvidia.com) reviews flagged code contextually, achieving "roughly 87% precision." Includes anti-jailbreak instructions since scanned content is itself model instructions.

**Risk scoring**:
- Findings accumulate points weighted by severity
- Executable content (Python scripts) applies 1.3x multiplier
- Score > 50 triggers "do not install" recommendation
- Research finding: 26.1% of skills contain vulnerabilities, 5.2% show likely malicious intent
- Skills with Python scripts are 2.12x more likely to be vulnerable

**Output formats**: Terminal display, JSON, Markdown, SARIF (for CI integration)

**Availability**: Free, open-source (Apache 2.0) at [github.com/NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector)

### JFrog Partnership Status: No Evidence

Searches and repository content show **no mention of JFrog**. The [05-competitive](/components/skills-catalog/research/05-competitive.md) analysis documented a NVIDIA-JFrog partnership announced at GTC 2026, but the August 2026 nvidia/skills repository and blog posts do not reference JFrog. The partnership may be focused on NIM/model distribution (Artifactory as unified registry) rather than the skills catalog specifically.

### agentskills.io Compliance

The [NVIDIA Verified Skills blog](https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/) confirms: "Verified skills build on agentskills.io open skills specification, so the same SKILL.md that works in one AI coding agent is designed to work reliably across Claude Code, Codex, and Cursor."

NVIDIA skills use the **Agent Skills specification (agentskills.io)** as the foundational format, extending it with verification metadata (skill cards, signatures, benchmarks).

## 5. catalog.redhat.com AI Section Analysis

See **Section 2** above for complete inventory. Key findings:

**Current state**: 4 skill packs + 2 individual skills + 6 MCP servers, all Red Hat-provided, all included with RHOAI/RHEL/OpenShift subscriptions.

**Target personas**: Site Reliability Engineers, Administrators. No developer-focused skill packs yet (though `rh-developer` exists in RHEcosystemAppEng/agentic-collections with 14 skills).

**Maturity labels**: "Developer Preview" for OpenShift skill pack, "Tech Preview" indicated by URL path for Ansible MCP server. No explicit GA labels, but presence of a detail page implies at least beta status.

**Source repository strategy**: Skills source from RHEcosystemAppEng/agentic-collections (monorepo, 7 packs, 68 skills). MCP servers likely have separate source repos (not documented on catalog pages).

**Governance**: No public security scanning, signing, or scorecard information visible on the catalog pages. Links to Red Hat's standard license agreement and privacy policy, but no skill-specific trust metadata.

**Gap vs Summit 2026 announcement**: Red Hat [announced agentic skill packs for RHEL, OpenShift, and Ansible at Summit 2026](https://www.redhat.com/en/blog/lab-ledger-scaling-enterprise-ai-red-hat-summit-2026). The catalog lists OpenShift (3 skills) and RHEL (2 skills), but **no Ansible skill pack** — only an Ansible MCP server. This suggests either the Ansible skills are not yet published or they are distributed via a different channel.

## 6. skills.sh Marketplace Evolution

### Growth Statistics

Multiple sources confirm skills.sh reached **600,000+ skills** by mid-2026:

- [Totalum Blog (May 2026)](https://www.totalum.app/blog/agent-skills-marketplaces-2026): "669,670 skills as of June 2026"
- [Agensi.io (2026 comparison)](https://www.agensi.io/learn/best-ai-agent-skills-marketplaces-2026): "83,627 skills and 8M+ total installs as of one report; another source indicates 600,000+ skills"
- [Ry Walker Research](https://rywalker.com/research/skills-sh): "600,000 OSS skills distributed via Vercel OIDC" at GA on June 5, 2026

**Growth trajectory**: December 2025 (few thousand) → January 2026 launch (tens of thousands) → February 2026 (vertical growth) → June 2026 (600K+).

**Top skills by install count (June 2026)**:
- vercel-labs/find-skills: 2.0M installs
- anthropics/frontend-design: 531.8K
- vercel-react-best-practices: 468.8K
- agent-browser: 440.9K
- microsoft/microsoft-foundry: 386.4K

**Agent platform support**: 18 different AI agents (Claude Code, Cursor, Codex, Copilot, Windsurf, and 13 more)

### Governance: Snyk Partnership (Feb 2026)

The [Snyk-Vercel partnership](https://snyk.io/blog/snyk-vercel-securing-agent-skill-ecosystem/) (announced Feb 17, 2026) integrated automated security scanning into skills.sh:

**How it works**:
- When a skill is installed via `npx skills`, Vercel's infrastructure calls Snyk's high-throughput API to analyze the skill **before it reaches the developer's machine**
- Scanner built on **agent-scan engine** (also called mcp-scan), combining "multiple customized LLM-based judges with deterministic rules"
- Dual analysis: executable code + natural language instructions to detect "toxic flows" (benign prompts triggering malicious behavior)
- Results displayed as "Security Verified" badge on skill pages after checking **8 security policy categories**
- Continuous re-evaluation as detection capabilities improve

**Security checks target**:
- Prompt injection (direct and indirect)
- Malicious code patterns
- Suspicious download URLs
- Insecure credentials
- Third-party content exposure

**Detection accuracy**: "90-100% recall on confirmed malicious skills" with "0% false positive rate on the top 100 legitimate skills"

**Research findings** (Snyk audit of 3,984 skills):
- Ecosystem growing at **147 new skills per day** (as of Feb 2026)
- 4,257 total skills at publication (Feb 2026) — confirms the explosive growth to 600K+ by June

**Governance model**: **Zero-curation, telemetry-ranked**, with automated security scanning as the trust layer. Anyone can publish; ranking is by install counts (gameable). Snyk scanning aims to block malicious skills at submission time without slowing legitimate developers. This contrasts with NVIDIA's human + automated review pipeline.

**Enterprise governance gap**: For organizations needing stricter controls, the article mentions "Evo provides the visibility, policy enforcement, and orchestration needed to govern AI systems across environments." This suggests skills.sh itself does not provide enterprise RBAC or policy enforcement — external tools (Snyk Evo) are required.

## 7. Kubeflow Hub KEP-0005 Status: No Evidence of Merge

### Search Results

Searches for "Kubeflow hub KEP-0005 skills plugin implementation status" and related queries returned **no mention of KEP-0005**. Results showed:

- Kubeflow Hub (formerly Model Registry) supports **two catalog source types**: YAML Catalog (static YAML) and Hugging Face Hub
- [GitHub releases](https://github.com/kubeflow/hub/releases) mention "Add Kind dev environment setup skill and slash command" in PR #2307, but this appears to be a development environment setup feature, not a catalog type
- [Documentation last modified June 13, 2026](https://www.kubeflow.org/docs/components/hub/overview/) describes two catalog types, with "pluggable sources via configuration" mentioned as a capability
- No evidence of "skills" as a fourth catalog type alongside models, datasets, notebooks

### Contradiction with 08-upstream-refresh

[08-upstream-refresh](/components/skills-catalog/research/08-upstream-refresh.md) states: "**KEP-0005 merged -- the skills catalog is now being built.** The first-mover window from 01-upstream has closed in the best way: Red Hat (rareddy) authored the implementation. SKILL.md parser, OpenAPI spec, and plugin scaffold all landed. Tracking issue #3014 has 32 tasks for full implementation."

**This refresh finds no public evidence supporting that claim.** Possible explanations:

1. **KEP-0005 is not the correct designation** — the actual KEP number may be different, or it's tracked as a GitHub issue/PR rather than a formal KEP
2. **Implementation is in progress but not merged** — the work exists in PRs but hasn't landed in the main branch
3. **Internal vs public repositories** — the implementation may be in a Red Hat-internal fork or downstream repository not yet pushed to kubeflow/hub upstream
4. **Misidentification** — the "Kind dev environment setup skill" (PR #2307) may have been misinterpreted as a skills catalog implementation

**Action required**: Verify the KEP-0005 claim with rareddy or the Kubeflow hub team. If the skills catalog implementation exists, determine its location (merged, in-PR, downstream-only) and status.

**Impact on 3.6 TP timeline**: [00-executive-summary](/components/skills-catalog/research/00-executive-summary.md) states "KEP-0005 merged Jul 27-31, skills IS the fourth catalog type." If this is incorrect, the assumption that RHOAI can extend an upstream-merged skills catalog is invalid. The 3.6 TP would require either:
- Building the skills catalog as a standalone Kubeflow hub plugin (larger scope)
- Using the YAML catalog source provider as a workaround (confirmed viable in [09-requirements-refresh](/components/skills-catalog/research/09-requirements-refresh.md))

## Key Findings

**1. Red Hat operates multiple skill initiatives with unclear boundaries.** UIE/Compass (internal, 300+ engineers, gold/silver scorecards), catalog.redhat.com/en/ai (public, 4 packs + 2 skills + 6 MCP servers), RHEcosystemAppEng/agentic-collections (public GitHub, 7 packs, 68 skills), openshift/agentic-skills (Lightspeed-tied), opendatahub-io/ai-helpers (Claude marketplace). **No single registry backend.** Federation or consolidation is required to avoid fragmentation.

**2. Compass discovery changes the architecture question.** If Compass is Red Hat's central skills registry with marketplace publishing, RHOAI skills catalog should federate from it rather than building a parallel MLflow-based registry. Attend the alignment session before finalizing registry architecture.

**3. OCP5 operator-gated skills create a dynamic catalog source opportunity.** Skills shipped via operators are K8s-native resources with lifecycle tied to installation. Kubeflow hub could query operator-provided skills, enabling dynamic catalog updates without manual curation. **Coordinate with OCP5 skills architecture team.**

**4. NVIDIA sets the bar for production-grade skill governance.** 300+ skills, daily sync, signature drift detection, skill cards, benchmarks, 68-pattern scanning, SARIF output, syndication to 5+ marketplaces. The [05-competitive](/components/skills-catalog/research/05-competitive.md) positioning remains accurate: Red Hat's differentiation is SLSA L3 provenance via Konflux, not scanning breadth.

**5. SkillSpector matured into the de facto open-source scanner.** 68 patterns (up from 64), 17 categories, LLM-enhanced pass with 87% precision, SARIF output, air-gapped support. **Free and Apache 2.0.** Red Hat should integrate SkillSpector into Konflux pipeline as planned (05, 09).

**6. skills.sh won the developer marketplace with zero curation + Snyk scanning.** 600K+ skills, 8M+ installs, 18 agent platforms, 147 skills/day growth rate. Governance model: automated scanning, no human review, install-count ranking. Enterprise buyers need external tools (Snyk Evo) for policy enforcement. **This validates Red Hat's curated, governance-first positioning.**

**7. catalog.redhat.com/en/ai launched without trust metadata.** No public security scanning, signing, scorecard, or compliance information on catalog pages. Gap vs NVIDIA's skill cards and Snyk's security badges. **EU AI Act Article 50 is now in effect** — 5 of 7 EX packs generate user-facing outputs requiring disclosure ([09-requirements-refresh](/components/skills-catalog/research/09-requirements-refresh.md)).

**8. KEP-0005 merge claim cannot be verified.** No public evidence of a skills catalog type in kubeflow/hub. Kubeflow hub docs (updated June 13, 2026) list two catalog types: YAML and Hugging Face. **Verify with rareddy.** If KEP-0005 is not merged, the 3.6 TP scope must use the YAML source provider workaround (confirmed viable in 09).

**9. No Ansible skill pack on catalog.redhat.com/en/ai despite Summit 2026 announcement.** Red Hat announced skill packs for RHEL, OpenShift, and Ansible at Summit. Catalog shows RHEL (2 skills) and OpenShift (3 skills) but only an Ansible MCP server. **Where are the Ansible skills?**

**10. JFrog partnership with NVIDIA appears model-focused, not skills-focused.** No mention of JFrog in nvidia/skills repository or recent NVIDIA skills blog posts. The GTC 2026 partnership may be limited to Artifactory as a unified registry for NIM/models, not the skills catalog.

## Sources

- [Red Hat Ecosystem Catalog — AI Section](https://catalog.redhat.com/en/ai)
- [Agentic skill pack for Red Hat OpenShift](https://catalog.redhat.com/en/ai/skills/detail/agentic-skill-pack-for-red-hat-openshift)
- [RHEcosystemAppEng/agentic-collections GitHub](https://github.com/RHEcosystemAppEng/agentic-collections)
- [openshift/agentic-skills GitHub](https://github.com/openshift/agentic-skills)
- [NVIDIA/skills GitHub](https://github.com/nvidia/skills)
- [NVIDIA Verified Agent Skills Blog](https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/)
- [SkillSpector: NVIDIA's open-source security scanner - Help Net Security](https://www.helpnetsecurity.com/2026/08/03/skillspector-open-source-agent-skill-security-scanner/)
- [Snyk-Vercel Partnership: Securing the Agent Skill Ecosystem](https://snyk.io/blog/snyk-vercel-securing-agent-skill-ecosystem/)
- [7 AI Agent Skills Marketplaces in 2026 (Compared) - Agensi.io](https://www.agensi.io/learn/best-ai-agent-skills-marketplaces-2026)
- [Agent Skills Marketplace in 2026: Anthropic vs Vercel vs OpenAI vs Cline vs MCP Compared - Totalum](https://www.totalum.app/blog/agent-skills-marketplaces-2026)
- [skills.sh | Ry Walker Research](https://rywalker.com/research/skills-sh)
- [Red Hat's skill packs give AI agents something a bigger model never could - The New Stack](https://thenewstack.io/red-hat-agentic-skills-repository/)
- [From lab to ledger: Scaling enterprise AI at Red Hat Summit 2026](https://www.redhat.com/en/blog/lab-ledger-scaling-enterprise-ai-red-hat-summit-2026)
- [Kubeflow Hub Overview](https://www.kubeflow.org/docs/components/hub/overview/)
- [Kubeflow Hub Releases](https://github.com/kubeflow/hub/releases)
