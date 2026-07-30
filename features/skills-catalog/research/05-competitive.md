---
title: "Skills Catalog research -- competitive analysis"
description: Deep competitive positioning across supply chain security (Konflux vs NVIDIA/JFrog/Snyk/Cisco), feature matrices (14 vendors, 13 dimensions), installer ecosystems (APM/skills.sh/LOLA/OCI), pricing models, blind spots, and win/loss analysis for RHOAI skills catalog.
timestamp: 2026-07-30
lens: competitive
review_after: 2026-10-30
---

# Skills Catalog research -- competitive analysis

## 1. Supply chain security competitive positioning

The agent skills supply chain is under active attack. Snyk's ToxicSkills
audit (Feb 2026) found 36.8% of 3,984 skills carried security flaws and
13.4% had critical issues. ClawHavoc poisoned 1,184 skills on ClawHub.
OWASP published the Agentic Skills Top 10 (AST10) in April 2026. Every
serious enterprise buyer now asks about trust before they ask about
features.

### Who has what

**NVIDIA (SkillSpector + OMS signing)**: Open-source scanner (Apache
2.0), 68 vulnerability patterns across 17 categories including prompt
injection, taint tracking, YARA signatures, and optional LLM semantic
analysis. Two-stage pipeline: fast static analysis (no API key needed)
plus optional LLM evaluation. Integrates into NVIDIA Verified Skills
publishing flow with daily catalog updates, automated + human review,
and cosign/Sigstore signing. Outputs SARIF for CI integration.

**JFrog (scan-verify-sign)**: Enterprise-grade Agent Skills Registry
announced at GTC 2026. Every skill is automatically versioned, scanned
for malicious intent, cryptographically signed, and access-controlled on
upload. Policy-driven approval workflows. Positioned as Gartner Leader
in Software Supply Chain Security (June 2026). NVIDIA partnership:
Artifactory as unified registry for AI models and agent skills within
NemoClaw/AI-Q Blueprint. JFrog's 2026 report tracked 969 malicious
agent skills alongside 495 malicious AI models on Hugging Face.
Partnership with Anthropic for Claude Code governance.

**Snyk (agent-scan)**: Formerly Invariant Labs MCP-Scan. Auto-discovers
agent configs across Claude Code, Cursor, Gemini CLI, Windsurf. Two
modes: scan (CLI, one-shot) and background MDM (continuous monitoring
reporting to Snyk Evo). Scans for prompt injection, sensitive data
handling, malware payloads in natural language. Partnered with Tessl
Registry -- every public skill carries a Snyk security score. Requires
Python 3.10+ and Snyk API token.

**Cisco (DefenseClaw)**: Five open-source components (Apache 2.0):
Skills Scanner, MCP Scanner, AI Bill of Materials (AI BoM), A2A Scanner,
CodeGuard. Three-tier architecture: Python CLI, Go gateway (policy
enforcement + audit logging), TypeScript plugin. Integrates with NVIDIA
OpenShell for sandbox enforcement using Landlock LSM and seccomp-BPF.
Streams all events to Splunk. Skills Scanner has ~2.4K GitHub stars.
Limitation: sandbox enforcement currently coupled to OpenShell runtime.

**Fortinet (FortiCNAPP)**: Agentless and agent-based workload scanning
for containers and serverless. RiskWatch detects when containerized
workloads actively execute vulnerable code at runtime. AI Assist for
triage. Focused on cloud workload security, NOT agent skills
specifically. No SKILL.md scanning, no skills registry integration.

### What Red Hat can do via Konflux that others cannot

Konflux is Red Hat's open-source secure software factory achieving SLSA
Level 3 compliance. It produces signed in-toto provenance attestations
via Tekton Chains, enforces machine-readable policies via Conforma, and
has built 2M+ artifacts across four architectures (x86_64, PPC64, ARM,
Z) in 2025 alone.

**Unique Konflux advantages for skills**:
- SLSA Level 3 provenance: cryptographic chain from source to artifact
  that no other skills vendor achieves. JFrog signs artifacts but does
  not produce SLSA-compliant provenance attestations.
- Hermetic builds: offline, reproducible builds that produce SBOMs as a
  byproduct. Critical for air-gapped environments.
- Multi-arch: skills packaged as OCI artifacts can be built for x86,
  ARM, PPC, Z from a single pipeline. No competitor does this.
- Conforma policy engine: machine-readable enterprise contracts that
  gate artifact promotion. More flexible than JFrog's approval workflows
  and fully open source.
- Red Hat Trusted Libraries (Tech Preview, Feb 2026): Python libraries
  built from source, signed and attested in SLSA Level 3 pipeline.
  Extensible to skill dependencies.

**The gap**: Konflux does not currently have a skills-specific scanning
stage (equivalent to SkillSpector's 68 patterns). Integrating NVIDIA
SkillSpector or Snyk agent-scan as a Tekton task in the Konflux pipeline
would close this gap while preserving the SLSA provenance chain.

## 2. Skills management feature matrix

| Capability | RHOAI (planned) | AWS AgentCore | Azure Agent 365 | Google Gemini Ent. | Databricks Unity | Anthropic | JFrog | skills.sh | NVIDIA |
|---|---|---|---|---|---|---|---|---|---|
| **Discovery/browse** | Kubeflow Hub UI | Console + API | Graph API + catalog | Agent Registry + Studio | Unity Catalog UI | marketplace.anthropic.com | Artifactory UI | Web + CLI | agentskills.io |
| **Search** | Hub search | Registry API + MCP | Graph API queries | Skill Registry API | UC search | CLI + web search | Xray queries | npx skills find | NVIDIA catalog |
| **Install** | OCI pull / LOLA | S3 + git clone + harness | APM / native | Skill upload / zip | UC registration | claude skills install | Artifactory pull | npx skills add | NVIDIA CLI |
| **Governance/RBAC** | K8s RBAC + MLflow | IAM + Cedar policies | Entra ID + M365 E7 | Agent Identity + IAM | UC ACLs + service policies | None (single-tenant) | Artifactory perms | None | N/A (trust layer) |
| **Trust/signing** | Konflux SLSA L3 (planned) | None currently | None currently | Cryptographic agent ID | Audit logs only | None | cosign signing | None | OMS cosign/Sigstore |
| **Scanning** | Konflux pipeline (planned) | None | None | Model Armor | None | None | Xray + NVIDIA scan | Snyk partnership | SkillSpector (68 patterns) |
| **Eval/benchmarks** | MLflow metrics (planned) | None | None | None | Inference tables | None | None | SkillsBench (external) | NVSkills-Eval (3-tier) |
| **Disconnected** | OCI mirror + oc-mirror | S3 VPC endpoints | None | None | None | None | Artifactory on-prem | None | OCI mirror |
| **OCI support** | Native (planned) | No | No | No | No | No | Yes (native) | No | Yes |
| **Bundling** | OCI multi-skill | S3 glob patterns | APM bundles | Zip upload | UC packages | CLI bundle | Promotion model | npx bundle | NIM bundles |
| **Federated (ARD)** | Kubeflow Hub sources | Registry MCP server | ARD co-author | ARD co-author | OpenSharing (LF) | No | No | No | ARD contributor |
| **Compliance metadata** | Skill cards (planned) | None | Certification reqs | None | Audit tables | None | SBOM | None | Skill Cards + BENCHMARK.md |
| **Pricing** | RHOAI subscription | Free (included) | M365 E7 or add-on | GCP consumption | Databricks consumption | Free + 15% rev share | SaaS pricing | Free | Free + open |

### Key observations from the matrix

1. **No vendor has it all.** AWS has strong RBAC but no scanning/signing.
   Google has governance but no air-gapped story. NVIDIA has the best
   trust pipeline but is not a registry. JFrog has scanning + signing
   but not a catalog UX.

2. **RHOAI's planned combination of Konflux SLSA L3 + OCI + air-gapped
   + MLflow governance is unique.** No other vendor combines provenance
   attestation, disconnected distribution, and open-source governance
   in a single stack.

3. **Governance is the gap everywhere.** 96% of enterprises run agents,
   12% can govern them (OutSystems 2026). Whoever solves governance
   first wins the enterprise market.

## 3. Installer ecosystem analysis

Five packaging/installation approaches compete in mid-2026:

**npx skills (Vercel/skills.sh)**: The npm of agent skills. 669K+ skills
indexed, 2M+ installs on top skill, 51+ agent support. Simple CLI
(`npx skills add owner/repo`). Zero curation, telemetry-ranked. Snyk
scanning partnership. Dominant in developer mindshare. No enterprise
governance. No OCI. No air-gapped support.

**APM (Microsoft)**: Manifest-driven dependency manager for AI agents.
Supports GitHub Copilot, Claude Code, Cursor, Codex, Gemini, Windsurf,
Kiro. Lockfile with 40-char commit SHA pinning. Org-level policy
enforcement via apm-policy.yml. SARIF output for Code Scanning. Air-gap
support via `apm pack / apm unpack`. MIT licensed. No runtime footprint.
The most enterprise-ready package manager but still early.

**LOLA (Red Hat)**: Convention-based, federated marketplace, Apache 2.0.
Designed for Red Hat's ecosystem. Less ecosystem adoption than APM or
npx skills. No active maintainers as of July 2026 -- may be archived
unless AAET commits.

**Native harness install**: Claude Code (`claude skills install`), Codex,
Gemini CLI each have native mechanisms. Fragmented, non-portable. Each
harness installs to its own location with its own format.

**OCI/ORAS**: Draft spec (v0.1.0, April 2026) by Thomas Vitale. Skills
packaged as OCI artifacts, pushed to any OCI registry (GHCR, Docker
Hub, Harbor, Quay). Reference implementations: Arconia CLI (Java),
skills-oci (Go), skillctl. Lock file with exact digests. No container
runtime required. Strongest air-gapped story via `oc-mirror`. Weakest
developer experience (no public registry with search/browse yet).

### Who is winning

**Developer adoption**: skills.sh dominates (669K+ indexed, 2M+ top
installs). Developers prefer `npx skills add` over any alternative.

**Enterprise adoption**: Too early to call. APM has the right design
(policy, lockfiles, air-gap) but no deployment data. JFrog Artifactory
is the incumbent for artifact management but skills-specific features
are new. OCI is architecturally strongest for regulated/disconnected
but lacks a polished UX layer.

**Red Hat's play**: OCI is the right bet. It leverages Red Hat's existing
strengths (Quay, oc-mirror, Konflux, Kubernetes). The gap is UX: Red
Hat needs a discovery/browse layer on top of OCI distribution. Kubeflow
Hub fills this role.

## 4. Pricing and business model analysis

| Vendor | Model | Price point | Notes |
|---|---|---|---|
| **Anthropic** | Free + 15% rev share | Creators keep 85% | ~600 skills, free dominates |
| **skills.sh** | Free (zero-curation index) | $0 | Revenue via Vercel platform stickiness |
| **NVIDIA** | Free + open source | $0 | Trust layer free; revenue via GPU/NIM sales |
| **JFrog** | SaaS subscription | $0 (free tier) to enterprise custom | Skills registry as Artifactory add-on |
| **TrueFoundry** | Tiered subscription | $499/mo (Pro), $2,999/mo (Pro Plus), custom (Enterprise) | SOC 2/HIPAA compliant |
| **AWS** | Included with AgentCore | $0 (no extra charge) | Revenue via Bedrock API consumption |
| **Azure** | M365 E7 or add-on | E7 suite includes | Revenue via M365 licensing + consumption |
| **Google** | GCP consumption | Standard GCP pricing | Revenue via GCP compute + API |
| **Databricks** | Platform consumption | Standard Databricks pricing | Revenue via Unity Catalog + compute |
| **Red Hat (RHOAI)** | Subscription | RHOAI subscription pricing | Skills catalog included in platform |

The market has bifurcated: **free-as-funnel** (cloud platforms give away
skills management to drive compute consumption) vs **standalone
subscription** (JFrog, TrueFoundry sell governance as a product). Red
Hat's subscription model fits naturally -- the skills catalog is a
feature of RHOAI, not a standalone product.

## 5. Competitive blind spots

Beyond disconnected/air-gapped (where Red Hat has an obvious advantage):

**Multi-architecture skills**: No vendor builds skills for PPC64, s390x,
or ARM alongside x86. Konflux does this today for container images. If
skills contain compiled components, multi-arch OCI artifacts become a
real differentiator.

**Kubernetes-native RBAC for skills**: Kubernetes RBAC breaks down for
AI agents at ~100-200 agents (Tigera research). CNCF's March 2026
agentic standards recommend SPIFFE/SVID workload identities. Red Hat has
deep SPIFFE expertise. No other skills vendor integrates K8s-native
identity with skills access control.

**Open-source governance stack**: JFrog is proprietary. TrueFoundry is
proprietary. Red Hat could deliver the first fully open-source skills
governance stack: MLflow (registry) + Konflux (build/sign) + Conforma
(policy) + Kubeflow Hub (catalog).

**Supply chain for skill dependencies**: Skills often bundle Python
scripts. Nobody scans skill dependency trees with the same rigor as
application dependencies. Red Hat Trusted Libraries (SLSA L3 Python
packages) could extend to skill dependencies.

**Compliance-as-metadata**: EU AI Act Article 50 lands August 2, 2026.
No vendor provides structured compliance metadata in skill manifests.

**Federated trust across registries**: ARD solves federated discovery.
Nobody solves federated trust -- verifying provenance across
organizational boundaries. Konflux's in-toto attestations are verifiable
across orgs because they use open standards (SLSA, Sigstore, in-toto).

## 6. Win/loss positioning

### Where RHOAI wins

| Competitor | RHOAI advantage |
|---|---|
| **AWS AgentCore** | Disconnected, multi-cloud, open-source governance, SLSA provenance |
| **Azure Agent 365** | No M365 E7 lock-in, disconnected, Linux/K8s-native, open-source stack |
| **Google Gemini Enterprise** | Disconnected, multi-cloud, open-source governance, no GCP dependency |
| **Databricks Unity AI** | Broader AI platform scope, disconnected, K8s-native, operator ecosystem |
| **JFrog** | Integrated AI platform, K8s-native deployment, SLSA L3, open-source policy engine |
| **NVIDIA** | Integrated catalog+registry+governance, K8s deployment, air-gapped, enterprise SLA |
| **Anthropic** | Enterprise governance, multi-model, disconnected, RBAC, compliance |
| **skills.sh** | Security, governance, enterprise support, air-gapped, compliance metadata |

### Where RHOAI loses

| Competitor | RHOAI disadvantage |
|---|---|
| **AWS AgentCore** | Deeper IAM/Cedar policy, larger ecosystem, lower friction for AWS customers |
| **Azure Agent 365** | APM (best package manager), Entra ID, M365 integration, 193 skills |
| **Google Gemini Enterprise** | Agent Gateway GA, Agent Identity, ARD co-author, Model Armor, 200+ models |
| **Databricks Unity AI** | Service policies (runtime enforcement), 14K+ orgs on UC, OpenSharing |
| **JFrog** | Gartner Leader, Anthropic partnership, mature artifact lifecycle, real-time scanning |
| **NVIDIA** | SkillSpector (68 patterns), Skill Cards, NVSkills-Eval, OMS signing |
| **Anthropic** | Created SKILL.md standard, 600+ curated skills, first-mover marketplace |
| **skills.sh** | 669K+ indexed, massive developer mindshare, 51+ agent support |

### Critical competitive gaps to close

1. **Skills-specific scanning**: No SkillSpector equivalent in the RHOAI
   pipeline. Integrate SkillSpector or Snyk agent-scan as a Tekton task.
2. **Skill cards / compliance metadata**: No structured metadata format
   beyond SKILL.md frontmatter. Define a Red Hat Skill Card format.
3. **Developer UX for install**: `npx skills add` is one command. RHOAI's
   OCI-based install needs a similarly frictionless CLI wrapper.
4. **Runtime policy enforcement**: AWS Cedar, Google semantic governance,
   Databricks service policies all enforce at runtime. RHOAI needs
   equivalent runtime policy gates.
5. **Ecosystem breadth**: Red Hat's skill catalog is small compared to
   Azure's 193, AWS's 43 packs, or community catalogs with 600K+.

## Key findings

1. **Supply chain security is table stakes, not a differentiator** --
   every serious vendor now scans, signs, or both. Red Hat's
   differentiation is SLSA Level 3 provenance via Konflux, which no
   other skills vendor achieves.
2. **The Konflux + OCI + MLflow combination is unique** -- no competitor
   delivers open-source build attestation + OCI distribution + ML
   lifecycle governance in an integrated stack.
3. **Disconnected/air-gapped is necessary but insufficient** -- it wins
   federal/defense/regulated deals but the broader market cares more
   about developer UX and ecosystem breadth.
4. **Multi-arch skills are an unexploited advantage** -- Konflux builds
   for x86, ARM, PPC64, Z. No competitor does multi-arch skills.
5. **The governance gap is the market opportunity** -- position the
   skills catalog as governance-first, not discovery-first.
6. **APM is the package manager to watch** -- Microsoft's design (policy,
   lockfiles, air-gap, multi-harness) is the most enterprise-ready.
7. **Federated trust is the next frontier** -- nobody solves cross-org
   trust verification. Konflux's in-toto attestations are verifiable
   across boundaries.
8. **Pricing is not a battleground** -- skills management is a platform
   feature, not a standalone product.
9. **Close the scanning gap immediately** -- integrate SkillSpector or
   Snyk agent-scan into Konflux before TP.
10. **K8s-native identity for skills is greenfield** -- SPIFFE/SVID for
    skills access control, leveraging OpenShift Service Mesh expertise.
