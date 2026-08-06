---
title: "Skills Catalog research -- partnership: partner skills ecosystem models"
description: "Eight-vendor comparison of partner skill inclusion models reveals three archetype patterns (curated/gated, federated, aggregated); NVIDIA co-engineering + JFrog scan-verify-sign is the closest precedent for RHOAI; Red Hat's existing ISV certification programs (container, operator) provide a proven template for a skills partner program; recommendation is curated-with-federation hybrid using Konflux pipelines and partnerVerified trust tier."
timestamp: 2026-08-06
lens: partnership
review_after: 2026-11-06
---

# Partner Skills Ecosystem Models

## Context

On 2026-08-05, Red Hat PE (Adel Zaalouk), Eng architecture (Ann Marie
Fred), and PM (Peter Double) aligned on including a curated subset of
NVIDIA skills as pre-loaded partner content in the RHOAI skills catalog
([decision-include-nvidia-skills-as-partner-content](/components/skills-catalog/knowledge/decision-include-nvidia-skills-as-partner-content.md)).
NVIDIA contacts confirmed: Babak Mozaffari and Raj Rao (PMs on the AI
Factory partnership). Red Hat is also interested in NVIDIA's
verification/validation pipeline for the ai-asset-pipeline.

But there is no model yet for HOW to do partner skill inclusion. This
document surveys the industry to answer: what patterns exist for
partner/ISV skill ecosystems, and which model should RHOAI adopt?


## 1. Vendor-by-vendor partner skill inclusion models

### 1.1 NVIDIA -- Verified Skills + partner co-engineering

NVIDIA operates the most mature open-source skills catalog: 300+ skills
across 35+ product lines in the
[nvidia/skills](https://github.com/nvidia/skills) GitHub repository
(2,800 stars, 489 commits). Skills are synced daily from internal product
repos to the public catalog through an automated pipeline with compliance
gates
([NVIDIA Verified Agent Skills blog](https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/)).

**Partner inclusion model**: NVIDIA's catalog is primarily first-party --
product teams onboard by adding a YAML file to the `components.d/`
registry directory. External partner skills enter through co-engineering
partnerships rather than open submission. The JFrog partnership
(announced GTC 2026) validated the pattern: JFrog Artifactory serves as
a governed endpoint for distributing NVIDIA-verified skills, with cuOpt
as the first packaged skill
([JFrog + NVIDIA press release](https://jfrog.com/press-room/jfrog-delivers-trust-layer-for-ai-driven-software-with-nvidia/)).

**Trust pipeline**: Each verified skill goes through a six-stage release
gate: (1) authoring, (2) SkillSpector scanning (68 vulnerability patterns,
17 categories), (3) remediation, (4) skill card completion, (5) OMS
signing (cosign/Sigstore), (6) consumer verification. Three trust layers
operate in parallel: SkillSpector scan (detect risky behavior), skill card
(human-readable intent/ownership/limits), and OMS signature (integrity and
authenticity)
([Trust Pipeline docs](https://docs.nvidia.com/skills/agent-skill-trust-pipeline)).

**Trust tier matrix**: NVIDIA recommends running every skill through Tiers
1-4 within 60 days, with five scoring dimensions: security scanning,
skill card completeness, runtime controls, observability/reversibility,
and evaluation metrics. Score 20-25 = Tier 1 (production-approved).

**Syndication**: NVIDIA skills are syndicated to Claude Code marketplace,
Codex plugin, Skills.sh, ClawHub, and Hermes Hub, with additional MCP
hubs planned
([NVIDIA skills roadmap](https://github.com/nvidia/skills)).

**Red Hat co-engineering precedent**: The OpenShell secure runtime is
jointly developed -- NVIDIA founded it, Red Hat is a key upstream
contributor and productized it into the Red Hat AI Factory. At Summit
2026, Red Hat and NVIDIA announced expanded agentic AI support including
OpenShell integration and NVIDIA Confidential Computing on OpenShift
sandboxed containers
([Red Hat press release](https://www.redhat.com/en/about/press-releases/red-hat-ai-factory-nvidia-expands-support-new-class-autonomous-agents-enterprise),
[Red Hat blog](https://www.redhat.com/en/blog/red-hat-and-nvidia-collaborate-more-secure-foundation-agent-ready-workforce)).

### 1.2 Anthropic -- Curated marketplace with revenue sharing

Anthropic operates two distinct partner surfaces:

**Claude Skills Marketplace** (launched May 1, 2026): ~600 skills (~90
first-party, rest community). Curated rather than open submission -- skills
ship through the Claude Skills directory and partner repositories.
Anthropic takes 15% of paid skill revenue (developers keep 85%). Most
skills are free
([Anthropic marketplace](https://claude.com/platform/marketplace),
[500k.io analysis](https://500k.io/journal/anthropic-skills-marketplace-launch)).

**Claude Marketplace** (enterprise): Organizations with existing Anthropic
spend commitments can use a portion for Claude-powered partner solutions.
Launch partners include GitLab, Harvey, Lovable, Replit, Rogo, and
Snowflake. Anthropic manages all invoicing
([Anthropic news](https://www.anthropic.com/news/services-track-partner-hub)).

**Claude Partner Network**: Three-tiered (Consulting, Technology,
Services), backed by a $100M commitment for 2026. Application involves
capability review, reference check, and 60-day onboarding. Four
certification exams ($99-$175 each) gated to Partner Network members.
Tier promotions processed semi-annually
([Claude Partner Network](https://www.anthropic.com/news/claude-partner-network)).

### 1.3 AWS -- AgentCore + Marketplace integration

AWS centers its 2026 partner strategy on Amazon Bedrock AgentCore as the
foundational platform for ISV agentic AI.

**ISV onboarding**: AWS Partner Central now uses AgentCore-powered agents
to guide new partners through registration, compliance, tax setup, and
Marketplace listing. The agent auto-populates partner profiles from
company websites and identifies next steps
([AWS Partner Central agents](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-partner-central/)).

**Marketplace for agents**: AWS Marketplace supports listing both MCP and
A2A servers, making tools and agents discoverable within agentic
workflows. ISVs can convert existing REST APIs into MCP tools via
AgentCore Gateway. The Agentic AI module helps partners build responsible
agents and publish to the AI Agents & Tools solution page
([AWS APN blog](https://aws.amazon.com/blogs/apn/powering-partner-success-2026-innovations/)).

**Incentives**: $25K additional Marketing Development Funds (MDF) for
qualifying Agentic AI partners on top of existing $50K MDF. The program
grew from 45 to 360 partners in one cycle. ACE-linked traction metrics
are now mandatory for specialization renewals
([Futurum analysis](https://futurumgroup.com/insights/aws-pushes-the-agent-stack-quick-connect-verticals-openai-on-amazon-bedrock/)).

**Skills as included**: No separate skills marketplace -- agent skills
are included with the AgentCore platform and Bedrock consumption model.
No per-skill revenue sharing.

### 1.4 Microsoft Azure -- ISV publishing via unified Marketplace

Microsoft is aggressively reshaping its partner ecosystem around agentic
AI in 2026.

**Marketplace publishing**: Partners enroll in the Microsoft AI Cloud
Partner Program, then publish through Partner Center. Two AI-focused
categories: "AI Apps and Agents" and "Machine Learning." Certification
checks require SOC 2 Type II, ISO 27001 compliance documentation.
Monetization models include SaaS entitlement-based (per-user, flat rate),
usage-based, or hybrid
([Microsoft Learn - publish AI agents](https://learn.microsoft.com/en-us/partner-center/marketplace-offers/artificial-intelligence-app-agent-publish-release)).

**Frontier Accelerate** (September 2026): Unifies ISV Success, Marketplace
Rewards, Azure IP co-sell, and certified software designations into a
single offering aligned to business milestones
([Partner Center announcements](https://learn.microsoft.com/en-us/partner-center/announcements/2026-june)).

**New certifications**: AI-103 (Azure AI Apps and Agents Developer
Associate), AB-100 (Agentic AI Business Solutions Architect), AB-620 (AI
Agent Builder Associate), SC-500 (Cloud and AI Security Engineer) all
launched in 2026, replacing legacy certifications
([Microsoft Build 2026 recap](https://blog.cloudfactorygroup.com/posts/microsoft-build-2026-recap-ai-agents-and-the-new-partner-opportunity)).

**Incentives**: AI-related incentives increased 50%, Azure outcome-based
incentives grew 70% YoY.

### 1.5 Google Gemini Enterprise -- Agent Gallery with validation

Google brings partner-built agents into the Agent Gallery inside Gemini
Enterprise, creating a centrally governed hub.

**Partner validation**: "Google Cloud Ready - Gemini Enterprise"
designation recognizes agents meeting highest standards. Every partner
agent is validated for security and interoperability by Google Cloud.
Secured chain of custody spans three personas: Billing Administrator,
Discovery Engine Administrator (registers verified agents, determines
org access), and Discovery Engine User
([Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/partner-built-agents-available-in-gemini-enterprise)).

**Onboarding**: Partners join Google Cloud Partner Network, review
Agent-as-a-Service listing requirements, accept the Marketplace Vendor
Agreement. Dynamic Client Registration (DCR) provisions unique OAuth 2.0
credentials when Gemini connects to an app instance, bound to active
Marketplace Entitlement
([Google Cloud docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/ai-agent-ecosystem-partners)).

**Incentives**: $750M partner fund for agentic development. Access to
$460B+ backlog of committed enterprise spend
([Google Cloud blog](https://cloud.google.com/blog/topics/partners/partners-powering-the-gemini-enterprise-agent-ecosystem)).

**Notable contrast**: Gemini CLI extensions are sourced from public repos
with no vetting or endorsement. Enterprise and CLI ecosystems operate
under completely different trust models.

### 1.6 Databricks -- Unity AI Gateway + OpenSharing

Databricks governs AI skills alongside data in Unity Catalog. Unity AI
Gateway (GA, June 2026) provides runtime governance: hard spend caps,
smart routing, service policies, PII guardrails. Skills, MCP services,
agents, and models share the same access controls, discovery, lineage,
and auditing framework
([Databricks blog](https://www.databricks.com/blog/ai-governance-data-ai-summit-2026-whats-new-unity-ai-gateway)).

**Partner ecosystem**: Eight security partners announced for runtime
governance (Netskope, Noma Security, Obsidian Security, Cyera,
HiddenLayer, Alice/WonderFence, CrowdStrike, Openlayer). Partners
provide runtime protection, not skill content
([Databricks blog](https://www.databricks.com/blog/building-open-ecosystem-ai-governance-unity-ai-gateway)).

**OpenSharing** (Linux Foundation, June 2026): Vendor-neutral protocol
for sharing AI assets including agent skills, models, and data. Extends
Delta Sharing's REST-based, zero-copy architecture to the full AI stack.
Apache 2.0. Table sharing is functional; skill sharing support is in
progress
([Linux Foundation announcement](https://www.linuxfoundation.org/press/linux-foundation-announces-opensharing-project-to-standardize-ai-asset-and-data-exchange)).

### 1.7 JFrog -- Enterprise skills registry

JFrog launched the Agent Skills Registry (private beta, GTC 2026) as the
first enterprise-grade private skills registry, part of the JFrog AI
Catalog.

**Scan-verify-sign pipeline**: Every skill is automatically versioned,
scanned for malicious intent, cryptographically signed, and
access-controlled on upload. Policy-driven approval workflows gate which
developers and agents can access which skills. Four governance pillars:
agent governance (provenance/audit), smart discovery (semantic search),
risk prevention (pre-consumption blocking), access control (project/team
scoping)
([JFrog Skills Registry](https://jfrog.com/ai-catalog/skills-registry/)).

**NVIDIA integration**: JFrog Artifactory serves as skills registry for
NVIDIA NemoClaw runtime. Validated with NVIDIA using cuOpt as first
packaged skill. Promotion model enforces increasing security gates from
team to enterprise-wide use
([BusinessWire](https://www.businesswire.com/news/home/20260408282466/en/JFrog-Delivers-Trust-Layer-for-AI-Driven-Software-with-NVIDIA)).

**Model**: Pure enterprise governance -- JFrog hosts the private
registry, organizations manage their own skill content. Not a public
marketplace. No skill publishing to external audiences.

### 1.8 skills.sh (Vercel) -- Open aggregation

skills.sh is Vercel's open agent-skills registry: 669K+ skills indexed
(June 2026), 2M+ installs on top skill, 27+ agent support.

**Publishing model**: Anyone can publish. A skill is a SKILL.md file in
a GitHub repo. No registry submission flow -- skills appear on skills.sh
automatically via install telemetry when installed via `npx skills add
owner/repo`. Zero curation, telemetry-ranked
([Vercel docs](https://vercel.com/docs/agent-resources/skills),
[skills.sh research](https://rywalker.com/research/skills-sh)).

**Security**: Snyk partnership (Feb 2026) provides automated scanning
before skills reach developer machines. 8 security policy categories.
90-100% recall on confirmed malicious skills, 0% false positive rate on
top 100 legitimate skills. Trail of Bits researchers bypassed the
malicious-skill detector, highlighting limits
([Snyk blog](https://snyk.io/blog/snyk-vercel-securing-agent-skill-ecosystem/)).

**Enterprise gap**: No RBAC, no policy enforcement, no air-gapped
support. Enterprise buyers need external tools (Snyk Evo) for
governance.


## 2. Three ecosystem archetype patterns

Analysis of the eight vendors reveals three distinct patterns for partner
skill inclusion. Most platforms use a hybrid.

### 2.1 Curated/Gated

**Pattern**: Vendor reviews and approves all partner content before
listing. Quality control is centralized.

**Examples**: Anthropic (skill submission through review), Google Gemini
Enterprise (validated agent gallery), Microsoft Marketplace (SOC 2/ISO
27001 certification checks), NVIDIA (human + automated review pipeline).

**Pros**: High trust, consistent quality, brand protection, compliance
guarantees, enterprise buyer confidence.

**Cons**: Slow iteration, bottleneck at review, limited ecosystem growth,
vendor becomes single point of failure for partner content velocity.

**Best for**: Enterprise platforms where trust and compliance outweigh
ecosystem breadth.

### 2.2 Federated

**Pattern**: Partner maintains their own catalog/repo; platform indexes
or federates from it. Each authority owns its content lifecycle.

**Examples**: NVIDIA skills (product repos sync to public catalog),
Kubeflow Hub (multiple catalog sources via YAML), Databricks OpenSharing
(vendor-neutral sharing protocol), OCP5 operator-gated skills (skills
ship with operators, catalog queries installed operators).

**Pros**: Partners control their content lifecycle, scales without central
bottleneck, each authority owns quality, natural multi-source support,
works for disconnected environments.

**Cons**: Quality variation across sources, trust verification complexity,
metadata consistency challenges, discovery fragmentation if not well
indexed.

**Best for**: Platforms that must integrate content from multiple
authoritative sources with different lifecycles.

### 2.3 Aggregated/Open

**Pattern**: Platform crawls/imports partner content from public repos.
Zero curation, telemetry-ranked. Anyone can publish.

**Examples**: skills.sh (auto-indexed via install telemetry), Gemini CLI
extensions (public repos, no vetting), community skills marketplaces
(open submission with basic metadata).

**Pros**: Maximum ecosystem breadth, lowest barrier to entry, fastest
growth, developer-friendly.

**Cons**: Quality highly variable, security risks (36.8% of skills have
flaws per Snyk ToxicSkills), gameable rankings, no enterprise governance,
no air-gapped support.

**Best for**: Developer-focused ecosystems where breadth and velocity
matter more than trust.


## 3. Comparison matrix

| Dimension | NVIDIA | Anthropic | AWS | Microsoft | Google | Databricks | JFrog | skills.sh |
|---|---|---|---|---|---|---|---|---|
| **Archetype** | Curated + Federated | Curated/Gated | Marketplace-integrated | Curated/Gated | Curated/Gated | Federated (OpenSharing) | Private registry | Aggregated/Open |
| **Partner onboarding** | Co-engineering partnership | Partner Network application (60-day) | Partner Central agent-guided | AI Cloud Partner Program enrollment | Google Cloud Partner Network | Unity Catalog registration | Enterprise sales | None (open publish) |
| **Submission flow** | components.d/ YAML + PR | Curated directory | Marketplace listing | Partner Center + certification | MVA + Agent-as-a-Service reqs | UC asset registration | Artifactory upload | SKILL.md in any GitHub repo |
| **Review process** | Human + automated (SkillSpector) | Centralized review | FTR validation | SOC 2/ISO 27001 checks | Google Cloud validation | No central review | Automated scan-verify-sign | Snyk automated scanning |
| **Certification tiers** | Trust Tier 1-4 matrix | Registered/Select/Preferred/Global Premier | Agentic AI Specialization | AI-103, AB-100, AB-620 certs | Google Cloud Ready designation | None | None | None |
| **Security scanning** | SkillSpector (68 patterns) | Not public | None | None | Model Armor | Partner-provided (8 vendors) | JFrog Xray + NVIDIA scan | Snyk agent-scan |
| **Signing** | OMS cosign/Sigstore | None | None | None | Cryptographic agent ID | Audit logs | cosign signing | None |
| **Revenue model** | Free (GPU revenue) | 85/15 split on paid skills | Included (Bedrock consumption) | SaaS monetization options | GCP consumption | Platform consumption | SaaS subscription | Free (Vercel stickiness) |
| **Partner incentives** | Co-engineering, AI Factory | $100M partner fund, certifications | $25K-$75K MDF | 50-70% incentive increases | $750M partner fund | OpenSharing governance | Enterprise registry | Install count rankings |
| **Air-gapped support** | OCI mirror | No | S3 VPC endpoints | No | No | No | Artifactory on-prem | No |
| **Open source** | Yes (Apache 2.0 + CC-BY-4.0) | No | No | No | No | OpenSharing (Apache 2.0) | No | Yes (MIT) |


## 4. Partner verification programs compared

### 4.1 Security scanning requirements

| Vendor | Scanner | Patterns | Air-gapped capable | Output format |
|---|---|---|---|---|
| NVIDIA | SkillSpector | 68 across 17 categories | Yes (static mode) | Terminal, JSON, Markdown, SARIF |
| JFrog | JFrog Xray + NVIDIA SkillSpector | Full Xray + 68 SkillSpector | Yes (on-prem) | JFrog reports |
| Snyk (skills.sh) | agent-scan | 8 policy categories | No | API response |
| Anthropic | Not disclosed | N/A | No | N/A |
| AWS/Azure/Google | None skills-specific | N/A | N/A | N/A |

### 4.2 Certification tier comparison

| Vendor | Tiers | Criteria | Renewal |
|---|---|---|---|
| NVIDIA | Tier 1-4 (Trust Matrix) | Security scan score, skill card completeness, runtime controls, observability, evaluation metrics | 60-day window recommended |
| Anthropic | Registered, Select, Preferred, Global Premier | Certifications earned, joint customers, success stories | Semi-annual (Jan 1, Jul 1) |
| AWS | Agentic AI Specialization | AI Competency validation (agent-led, 70% faster), ACE activity mandatory | Annual (performance-based) |
| Microsoft | AI-103, AB-100, AB-620, SC-500 | Exam pass (720/1000, 120 min), third-party capabilities audit | Exam retirement/replacement cycle |
| Google | Google Cloud Ready - Gemini Enterprise | Performance and quality validation by Google Cloud | Not disclosed |
| Red Hat (existing) | Container Certified, Operator Certified, Validated Platform | Tekton pipeline validation, preflight tests, documentation reqs | Per OpenShift EUS window |

### 4.3 Ongoing compliance requirements

**NVIDIA**: Daily automated sync pipeline with signature drift detection
and missing-artifact enforcement (completed roadmap items). Skills must
maintain skill card, signature, and evaluation dataset.

**Anthropic**: Recommended cadence: patch-level monthly, minor quarterly,
major annually. Every change documented in listing changelog.

**Microsoft**: Third-party capabilities audit replaces customer
references, valid for two years. OpenShift EUS certification windows
apply for Microsoft-on-Azure scenarios.

**Red Hat (existing model)**: Operator certification requires re-validation
per OpenShift EUS cycle. Continuous monitoring for container
vulnerabilities. Partners must update product documentation to list
OpenShift as supported platform and provide installation instructions
using certified artifacts
([Red Hat Partner Certification 2026](https://docs.redhat.com/en/documentation/red_hat_partner_certification/2026)).


## 5. Co-engineering patterns and precedents

### 5.1 NVIDIA + Red Hat: OpenShell

The most relevant precedent for RHOAI partner skills integration.

NVIDIA founded OpenShell as an open-source sandboxed runtime for
autonomous AI agents. Red Hat became a key upstream contributor and
productized it into the Red Hat AI Factory with NVIDIA. Justin Boitano
(NVIDIA VP): "Red Hat and NVIDIA are co-engineering the Red Hat AI Factory
with NVIDIA, bringing NVIDIA OpenShell, NVIDIA Confidential Computing and
the full AI stack together"
([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/enterprise-software-leaders-build-ai-agents-with-nvidia)).

**Pattern**: NVIDIA creates and open-sources the technology. Red Hat
contributes upstream and productizes as a supported component in the Red
Hat platform. Joint go-to-market under the AI Factory banner.

**Relevance to skills**: The same pattern can apply -- NVIDIA creates and
verifies skills, Red Hat curates a subset, verifies through Konflux
pipeline, and distributes as partnerVerified content in the RHOAI catalog.

### 5.2 NVIDIA + JFrog: Scan-verify-sign

At GTC 2026, JFrog launched its Agent Skills Registry with validated
NVIDIA integration. JFrog Artifactory serves as the centralized skills
registry for NVIDIA NemoClaw runtime.

**Pattern**: NVIDIA provides the skill content and verification metadata
(SkillSpector scans, OMS signatures). JFrog provides the enterprise
governance layer (versioning, access control, policy-driven approval
workflows, promotion model). The NVIDIA-JFrog teams validated a workflow
for ingestion and management using cuOpt as the first packaged skill
([TechTarget](https://www.techtarget.com/searchitoperations/news/366640420/Nvidia-NemoClaw-JFrog-shore-up-OpenClaw-security)).

**Promotion model**: Skills progress through increasing security gates
from team-level use to enterprise-wide deployment.

**Relevance to skills**: This is the closest operational model to what
RHOAI needs. Replace JFrog's governance layer with Konflux + MLflow;
NVIDIA's role stays the same.

### 5.3 Snyk + Vercel: Security scanning partnership

Snyk provides automated security scanning for skills.sh -- scans execute
before skills reach developer machines, combining LLM-based judges with
deterministic rules. "Security Verified" badges appear on skill pages
after passing 8 security policy categories
([Snyk blog](https://snyk.io/blog/snyk-vercel-securing-agent-skill-ecosystem/)).

**Pattern**: Platform (Vercel) handles distribution; security partner
(Snyk) handles verification. Clear separation of concerns.


## 6. Revenue and business models

The market has bifurcated into three models:

### 6.1 Free-as-funnel (dominant pattern)

Skills management is given away free to drive consumption of the core
platform.

| Vendor | Core revenue driver | Skills cost |
|---|---|---|
| AWS | Bedrock API consumption | Included |
| Google | GCP compute/API | Included |
| Databricks | Unity Catalog + compute | Included |
| NVIDIA | GPU/NIM sales | Free + open source |
| Red Hat (RHOAI) | RHOAI subscription | Included |

### 6.2 Revenue share on paid skills

| Vendor | Split | Volume |
|---|---|---|
| Anthropic | 85% creator / 15% platform | ~600 skills, most free |

### 6.3 Standalone governance subscription

| Vendor | Model | Notes |
|---|---|---|
| JFrog | Enterprise SaaS subscription | Skills registry as AI Catalog add-on |
| TrueFoundry | Tiered ($499-$2,999/mo) | SOC 2/HIPAA compliant |

**Implications for RHOAI**: Red Hat's subscription model fits naturally
in 6.1 (free-as-funnel). Partner skills are included in the RHOAI
subscription, not separately monetized. This simplifies the partner
relationship -- no revenue-share negotiations needed.


## 7. Red Hat-specific implications and recommendations

### 7.1 Recommended model: Curated-with-federation hybrid

RHOAI should adopt a **curated-with-federation** model that combines:

1. **Curated**: Red Hat controls which partner skills appear in the
   catalog. Not all NVIDIA skills (300+) are appropriate -- only those
   relevant to RHOAI platform use cases (GPU effectiveness, RAG, NeMo,
   inference serving). Ann Marie: "skills for using their GPUs
   effectively." This aligns with Red Hat's existing curated-tested-
   supported philosophy for open-source software
   ([Red Hat blog](https://www.redhat.com/en/blog/curated-tested-and-supported-how-enterprise-vendors-mitigate-open-source-supply-chain-risk)).

2. **Federated source**: NVIDIA maintains its own GitHub repo
   (nvidia/skills) as the authoritative source. Red Hat configures a
   Kubeflow Hub catalog source pointing to a filtered subset. NVIDIA
   controls the content lifecycle; Red Hat controls the curation filter
   and adds verification. This mirrors NVIDIA's own internal model
   (product repos sync to public catalog) and the Kubeflow Hub design
   (multiple YAML catalog sources per authority).

**Why not fork/copy**: Copying NVIDIA skills into a Red Hat repo creates
a maintenance burden and version drift. NVIDIA updates skills via daily
automated sync. Red Hat would need to track every update manually.

**Why not full aggregation**: RHOAI is not a marketplace. Open aggregation
(skills.sh model) contradicts the governance-first positioning and
introduces the 36.8% vulnerability exposure.

### 7.2 Trust tier mapping

The existing trust tier enum maps cleanly to partner skills:

| Trust tier | Source | Verification |
|---|---|---|
| `platformProvided` | Red Hat-authored (EX packs) | Konflux SLSA L3 (planned), RH engineering review |
| `partnerVerified` | ISV/partner authored, Red Hat verified | Partner's own pipeline (e.g., NVIDIA SkillSpector + OMS) + Red Hat verification overlay (Konflux scan, metadata validation) |
| `organizationApproved` | Customer-uploaded | Customer's own governance + admin approval |
| `communityContributed` | Unverified community | No verification guarantee |

NVIDIA skills should enter as `partnerVerified`. This means:

- NVIDIA has already verified (SkillSpector scan, OMS signature, skill
  card, Tier-3 evaluation dataset)
- Red Hat adds verification overlay: Konflux pipeline scan (when ready),
  metadata schema validation, RHOAI platform relevance filter, EU AI
  Act Article 50 compliance check

### 7.3 VIP partner tier -- operational meaning

The "VIP partner tier" for NVIDIA means:

1. **Priority inclusion**: NVIDIA skills are in the DP/TP launch content
   list, not deferred to GA or 3.7+
2. **Co-engineering relationship**: Joint work on verification pipeline
   integration (SkillSpector into ai-asset-pipeline), not arm's-length
   catalog source configuration
3. **Lifecycle model alignment**: Red Hat considers adopting NVIDIA's
   skill lifecycle practices (Adel's interest)
4. **Dedicated contact path**: Named PM contacts (Babak, Raj) with
   direct relationship, not partner portal submission

This is operationally distinct from a future "standard partner tier"
where ISVs self-service through a published partner program.

### 7.4 Verification pipeline: what Red Hat adds on top

Red Hat's verification overlay for partnerVerified skills:

| Stage | NVIDIA provides | Red Hat adds |
|---|---|---|
| Scanning | SkillSpector (68 patterns, SARIF) | Konflux pipeline re-scan (when ready); additional enterprise-specific checks (air-gapped compatibility, multi-arch) |
| Signing | OMS cosign/Sigstore signature | Konflux SLSA L3 attestation wrapping partner signature + Red Hat provenance |
| Metadata | Skill card (agentskills.io spec) | RHOAI catalog metadata (trustTier, category, tags, EU AI Act Article 50 fields) |
| Evaluation | Tier-3 eval dataset + BENCHMARK.md | RHOAI-specific evaluation (platform compatibility, harness verification) |
| Compliance | NVIDIA license (Apache 2.0 + CC-BY-4.0) | Red Hat subscription terms overlay, export control review |

### 7.5 Lifecycle: who maintains partner skills?

**Recommended model**: Partner pushes updates; Red Hat controls ingestion
cadence.

| Lifecycle event | Partner responsibility | Red Hat responsibility |
|---|---|---|
| New skill version | Push to partner repo (nvidia/skills) | Detect via catalog source sync; re-run verification overlay; promote to catalog |
| Security vulnerability | Issue fix in partner repo; re-sign | Re-scan via Konflux; update catalog entry; notify affected clusters |
| Skill deprecation | Mark deprecated in partner repo | Remove from active catalog; retain in archive for audit |
| New skill addition | Add to partner repo | Evaluate against curation filter; add to catalog source YAML if approved |

**Sync cadence options**:
- **Daily** (NVIDIA's model): Maximum freshness, higher operational cost
- **Release-aligned**: Sync at RHOAI release boundaries (quarterly)
- **On-demand**: Sync when partner notifies of material changes

**Recommendation**: Start with release-aligned sync for DP/TP. Move to
weekly or on-demand once operational confidence is established.

### 7.6 Disconnected/air-gapped implications

Partner skills must work in disconnected environments. This requires:

1. **OCI packaging**: Partner skills packaged as OCI artifacts and pushed
   to Quay. Customers mirror via `oc-mirror` for air-gapped clusters.
2. **Signature portability**: Partner signatures (NVIDIA OMS) and Red Hat
   attestations must be verifiable offline. Sigstore's Rekor transparency
   log requires network access; offline verification requires bundled
   trust roots.
3. **Dependency resolution**: Skills with external dependencies (API
   endpoints, model downloads) must declare disconnected alternatives or
   be excluded from air-gapped catalog builds.

### 7.7 Red Hat precedent models: container and operator certification

Red Hat already operates mature ISV certification programs that can
inform the skills partner program:

| Dimension | Container Certification | Operator Certification | Skills Partner Program (proposed) |
|---|---|---|---|
| **Entry point** | Red Hat Partner Connect | Red Hat Partner Connect | Red Hat Partner Connect (new track) |
| **Technical validation** | UBI base, vulnerability scan, health index | Tekton CI pipeline, preflight tests, OLM validation | Konflux pipeline scan, metadata validation, RHOAI compatibility |
| **Distribution** | Red Hat Ecosystem Catalog | OperatorHub + Red Hat Marketplace | RHOAI Skills Catalog (Kubeflow Hub) |
| **Documentation reqs** | Installation instructions, support matrix | Install/update instructions on OpenShift, certification docs | SKILL.md (agentskills.io), skill card, RHOAI compatibility matrix |
| **Lifecycle** | Continuous vulnerability monitoring | Re-validate per EUS cycle | Release-aligned re-verification |
| **Automation** | Partner build pipeline (Tekton) | operator-pipelines (Tekton, open source on GitHub) | Konflux pipeline tasks (Tekton, extending operator-pipelines model) |

The operator certification pipeline
([github.com/redhat-openshift-ecosystem/operator-pipelines](https://github.com/redhat-openshift-ecosystem/operator-pipelines))
is the most direct template. It uses Tekton pipelines triggered by
partners on-premise, validates against minimum requirements, and
optionally submits results to trigger the next certification stage.
A skills certification pipeline could follow the same pattern:
partner-triggered Tekton pipeline, automated preflight checks
(SkillSpector + RHOAI compatibility), result submission, and PR-based
promotion to the catalog source.


## 8. Emerging patterns to watch

### 8.1 OpenSharing (Linux Foundation)

Databricks-contributed, vendor-neutral protocol for sharing AI assets
including agent skills across organizations and platforms. REST-based,
zero-copy architecture. Skill sharing support is in progress (table
sharing is functional). If OpenSharing achieves adoption, it could
become the federation protocol for cross-platform skill catalogs --
potentially replacing custom YAML catalog source configurations
([Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-opensharing-project-to-standardize-ai-asset-and-data-exchange)).

### 8.2 Agent Registry Discovery (ARD)

Google-led spec (v0.9) for cross-platform agent discovery. NVIDIA is
a contributor. Near-zero adoption as of August 2026, but backed by major
vendors. Could complement OpenSharing (ARD for discovery, OpenSharing
for asset exchange).

### 8.3 OCI as universal skill packaging

The OCI Skills spec (v0.1.0, Thomas Vitale) and JFrog's Artifactory
integration both point to OCI as the convergence format for enterprise
skill distribution. NVIDIA already packages some skills as OCI
artifacts. Red Hat's OCI expertise (Quay, oc-mirror, Konflux) is a
natural fit.

### 8.4 Microsoft APM for policy

APM (manifest-driven dependency manager) with `apm-policy.yml` for
org-level policy enforcement and air-gap support (`apm pack / apm
unpack`) is the most enterprise-ready package manager. Its policy
model could inform Red Hat's own skill governance policies.


## Key findings

1. **Three archetype patterns dominate**: curated/gated (Anthropic, Google, Microsoft), federated (NVIDIA, Kubeflow, Databricks/OpenSharing), and aggregated/open (skills.sh) -- most enterprise platforms use curated or curated-federated hybrids.

2. **NVIDIA + JFrog is the closest operational precedent for RHOAI's partner model**: NVIDIA provides verified skill content, JFrog provides the enterprise governance registry -- RHOAI should replace JFrog's role with Konflux + MLflow while preserving the same pattern.

3. **No vendor has solved federated trust across organizational boundaries**: every verification pipeline is single-org; Konflux's SLSA L3 in-toto attestations are the strongest candidate for cross-org trust verification because they use open standards (Sigstore, in-toto).

4. **Revenue sharing is rare and unnecessary for RHOAI**: only Anthropic (85/15) charges for skills; all enterprise platforms (AWS, Azure, Google, Databricks, Red Hat) include skills in platform subscription pricing.

5. **Red Hat's existing ISV certification programs (container, operator) provide a proven template**: the operator-pipelines Tekton model (partner-triggered, automated preflight, PR-based promotion) maps directly to a skills partner program.

6. **NVIDIA skills should enter the catalog as partnerVerified with a Red Hat verification overlay**: NVIDIA's own pipeline (SkillSpector + OMS + skill cards) provides the base; Red Hat adds Konflux re-scan, metadata validation, platform relevance filtering, and SLSA provenance attestation.

7. **The curated-with-federation model is the right fit for RHOAI**: Red Hat controls curation (which skills appear); NVIDIA controls content lifecycle (daily sync from product repos); Kubeflow Hub federates via catalog source YAML -- this avoids both the maintenance burden of fork/copy and the security risk of open aggregation.

8. **VIP partner tier is operationally distinct from a future self-service program**: NVIDIA gets co-engineering, named contacts, and priority inclusion; a scalable partner program for other ISVs should follow the operator certification self-service model.

9. **Disconnected/air-gapped partner skills require OCI packaging and offline signature verification**: partner signatures must be verifiable without network access, which means bundled trust roots and SLSA attestation portability.

10. **OpenSharing (Linux Foundation) is the emerging federation protocol to watch**: if it achieves adoption for skill sharing (currently in progress), it could standardize cross-platform skill exchange and replace custom federation configurations.


## Sources

- [NVIDIA Verified Agent Skills blog](https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/)
- [NVIDIA Trust Pipeline docs](https://docs.nvidia.com/skills/agent-skill-trust-pipeline)
- [NVIDIA/skills GitHub repository](https://github.com/nvidia/skills)
- [JFrog Agent Skills Registry](https://jfrog.com/ai-catalog/skills-registry/)
- [JFrog + NVIDIA Trust Layer announcement](https://jfrog.com/press-room/jfrog-delivers-trust-layer-for-ai-driven-software-with-nvidia/)
- [NVIDIA NemoClaw + JFrog security (TechTarget)](https://www.techtarget.com/searchitoperations/news/366640420/Nvidia-NemoClaw-JFrog-shore-up-OpenClaw-security)
- [Red Hat AI Factory with NVIDIA press release](https://www.redhat.com/en/about/press-releases/red-hat-ai-factory-nvidia-expands-support-new-class-autonomous-agents-enterprise)
- [Red Hat + NVIDIA secure foundation blog](https://www.redhat.com/en/blog/red-hat-and-nvidia-collaborate-more-secure-foundation-agent-ready-workforce)
- [Anthropic Claude Partner Network](https://www.anthropic.com/news/claude-partner-network)
- [Anthropic Services Track + Partner Hub](https://www.anthropic.com/news/services-track-partner-hub)
- [Claude Marketplace](https://claude.com/platform/marketplace)
- [Anthropic Skills Marketplace analysis (500k.io)](https://500k.io/journal/anthropic-skills-marketplace-launch)
- [AWS Partner Central agents announcement](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-partner-central/)
- [AWS APN: Powering Partner Success 2026](https://aws.amazon.com/blogs/apn/powering-partner-success-2026-innovations/)
- [AWS AgentCore analysis (Futurum)](https://futurumgroup.com/insights/aws-pushes-the-agent-stack-quick-connect-verticals-openai-on-amazon-bedrock/)
- [Microsoft: Publish AI agents on Marketplace](https://learn.microsoft.com/en-us/partner-center/marketplace-offers/artificial-intelligence-app-agent-publish-release)
- [Microsoft Build 2026 partner recap](https://blog.cloudfactorygroup.com/posts/microsoft-build-2026-recap-ai-agents-and-the-new-partner-opportunity)
- [Microsoft Partner Center June 2026 announcements](https://learn.microsoft.com/en-us/partner-center/announcements/2026-june)
- [Google: Partner-built agents in Gemini Enterprise](https://cloud.google.com/blog/products/ai-machine-learning/partner-built-agents-available-in-gemini-enterprise)
- [Google: Partners powering Gemini Enterprise](https://cloud.google.com/blog/topics/partners/partners-powering-the-gemini-enterprise-agent-ecosystem)
- [Google AI Agent Ecosystem Partners docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/ai-agent-ecosystem-partners)
- [Databricks: Unity AI Gateway ecosystem blog](https://www.databricks.com/blog/building-open-ecosystem-ai-governance-unity-ai-gateway)
- [Databricks: What's new with Unity Catalog at DAIS 2026](https://www.databricks.com/blog/whats-new-unity-catalog-data-ai-summit-2026)
- [Linux Foundation OpenSharing announcement](https://www.linuxfoundation.org/press/linux-foundation-announces-opensharing-project-to-standardize-ai-asset-and-data-exchange)
- [Vercel Agent Skills docs](https://vercel.com/docs/agent-resources/skills)
- [skills.sh research (Ry Walker)](https://rywalker.com/research/skills-sh)
- [Snyk-Vercel partnership blog](https://snyk.io/blog/snyk-vercel-securing-agent-skill-ecosystem/)
- [Red Hat Partner Certification 2026 docs](https://docs.redhat.com/en/documentation/red_hat_partner_certification/2026)
- [Red Hat container certification](https://connect.redhat.com/explore/red-hat-container-certification)
- [Red Hat ISV operator certification pipelines (GitHub)](https://github.com/redhat-openshift-ecosystem/operator-pipelines)
- [Red Hat: Curated, tested and supported blog](https://www.redhat.com/en/blog/curated-tested-and-supported-how-enterprise-vendors-mitigate-open-source-supply-chain-risk)
- [NVIDIA enterprise agent software leaders (Newsroom)](https://nvidianews.nvidia.com/news/enterprise-software-leaders-build-ai-agents-with-nvidia)
- [Agent Skills Marketplace comparison (Totalum)](https://www.totalum.app/blog/agent-skills-marketplaces-2026)
- [AI Agent Skills Marketplaces 2026 (Agensi.io)](https://www.agensi.io/learn/best-ai-agent-skills-marketplaces-2026)
