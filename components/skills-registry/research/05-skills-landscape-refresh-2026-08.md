---
title: Skills Landscape Refresh (August 2026)
description: Landscape changes since April 2026 — SKILL.md adoption surge, Databricks Unity Catalog agent registry, NVIDIA SkillSpector maturation, and Red Hat's internal UIE/Compass discovery
timestamp: 2026-08-04
lens: landscape
review_after: 2026-11-04
---

# Skills Landscape Refresh (August 2026)

**Purpose**: Document what has CHANGED in the skills landscape since the April 2026 baseline research (docs 01 and 03). Focus on new developments, not a rehash of the April findings.

**Context**: The April 2026 landscape found no standardized skills registry, SKILL.md emerging as de facto standard, 7+ fragmented packaging formats, security as first-order concern post-ClawHub crisis, and no unified skills specification. This refresh examines what shifted in the four months since.

---

## Executive Summary: Four Months of Rapid Change

Between April and August 2026, the skills landscape underwent three major shifts:

1. **SKILL.md crossed the chasm** — From 7 tools in December 2025 to 40+ by June 2026. The standard is now effectively universal across AI coding agents, with Anthropic, OpenAI, Microsoft, Google, JetBrains, AWS, Databricks, and ByteDance all shipping compatible implementations. This represents one of the fastest standardization events in AI tooling history.

2. **Enterprise governance platforms shipped** — Databricks Unity Catalog (DAIS, June 2026), JFrog Agent Skills Registry (GTC, March 2026), and Microsoft APM (2026) all delivered production-grade skills registries with scanning, signing, and policy enforcement. The gap identified in April ("no skills registry anywhere") closed in Q2.

3. **Red Hat's internal skills ecosystem surfaced** — Meetings on 2026-08-04 revealed a 300+ engineer Unified Intelligence Engineering (UIE) org with a Compass skills registry (gold/silver scorecards, marketplace publishing) and a Light Trail team building MCP server hosting on MP+. This was a complete blind spot in April's external research.

**Bottom line**: The April landscape described a fragmented pre-standard ecosystem. The August landscape shows rapid convergence on SKILL.md for packaging, Unity Catalog / JFrog / APM for governance, and OCI artifacts gaining traction for enterprise distribution.

---

## 1. SKILL.md Standard: From Emerging to Universal (Dec 2025 → Aug 2026)

### Adoption Timeline

| Date | Event |
|------|-------|
| Dec 18, 2025 | Anthropic publishes Agent Skills spec at agentskills.io |
| Dec 20, 2025 (48 hrs) | OpenAI adds to ChatGPT and Codex CLI; Microsoft integrates into VS Code and GitHub Copilot |
| Jan 2026 | Google Gemini CLI adopts; Vercel launches skills.sh marketplace |
| Mar 2026 | 32 tools supporting the standard |
| Apr 2026 | 30+ tool adoption milestone |
| Jun 2026 | ~40 products on agentskills.io showcase |

**April baseline**: SKILL.md "adopted by Anthropic, OpenAI Codex, Google Gemini CLI, GitHub Copilot" (doc 01, line 476).

**August status**: 40+ products including Claude Code, OpenAI Codex, ChatGPT, Microsoft VS Code, GitHub Copilot, Google Gemini CLI, Google Antigravity, JetBrains Junie, AWS Kiro, Block Goose, Sourcegraph Amp, Snowflake Cortex Code, Databricks Genie Code, ByteDance TRAE, Mistral AI, Cursor, OpenCode, and Windsurf.

### Spec Updates

- **Claude Code 2.1.0** (Jan 2026): Skill hot-reloading — skills update mid-session without restart
- **Specification docs** (May 2026 update): Progressive disclosure model reinforced — metadata (~100 tokens) at startup, instructions (<5000 tokens recommended) on activation, resources as needed. Main SKILL.md kept under 500 lines.
- **GitHub Copilot integration**: Recognizes skills in `.github/skills/`, `.claude/skills/`, and `.agents/skills/` directories

**Verdict**: SKILL.md is no longer "emerging" — it is the de facto standard. April research identified it as the most likely path forward; August confirms it won.

---

## 2. Enterprise Skills Registries: The Gap Closed (Q2 2026)

### 2.1 Databricks Unity Catalog Agent Registry (DAIS, June 2026)

**What shipped**: Unity AI Gateway now registers "Databricks-hosted and external models, MCP services, agents, and skills" as Unity Catalog securable objects with the same access controls, discovery, lineage, and auditing used for data.

**Key capabilities** (all new since April):

| Feature | Status | Description |
|---------|--------|-------------|
| **Agent Registry** | GA | Single system of record in Unity Catalog for every agentic asset (Databricks or third-party). Agents registered as UC models; tools governed as MCP services, functions, and connections. |
| **Skills Catalog** | GA | Governed inventory of reusable skills. Teams can register agent endpoints, publish approved skills, and discover capabilities through a common catalog experience. |
| **MCP Support** | GA | Managed MCP services for Google Drive, Jira, Confluence, Slack, GitHub, SharePoint, Outlook out-of-the-box. Custom MCP servers can be registered. |
| **Contextual Service Policies** | Beta | Runtime governance of MCP interactions — admins can allow/deny/require-approval for actions (e.g., writing to sensitive folders, pushing code). |
| **Unified Tracing** | GA | Captures model and MCP activity in one governed telemetry layer. |
| **Budget Controls** | GA | Hard spend caps for external providers (OpenAI, Anthropic, Gemini, Grok, Kimi) including BYOK connections. Requests stop when budget is reached. |
| **ABAC Grant Policies** | Beta (models); future for MCP/agents | Attribute-based access control for AI components. |

**Distribution model**: Agents install skills via Unity Catalog APIs. Framework support includes Claude Code SDK, LangGraph, Agno, CrewAI, OpenAI Agent SDKs, with horizontal autoscaling through Databricks Apps.

**OpenSharing protocol**: Databricks announced "the first open, vendor-neutral protocol for securely sharing AI assets, including Agent Skills, AI models, and unstructured data" the week before DAIS.

**April gap**: "No standardized skills registry anywhere" (doc 03, line 33). Unity Catalog now provides exactly this for Databricks customers.

**MLflow upstream**: The April meetings discussed a Databricks/MLflow skills registry prototype targeting "end of April 2026" (doc 04, line 119). As of July 31, 2026, MLflow 3.15.0 shipped with a centralized MCP Registry and an upgraded MLflow Assistant. The `mlflow agent setup` command installs curated MLflow skills from `github.com/mlflow/skills` for agent evaluation, trace analysis, and instrumentation. The standalone skills registry prototype status is unclear — Unity Catalog may have subsumed that effort.

### 2.2 JFrog Agent Skills Registry (GTC, March 2026)

**What shipped**: JFrog Agent Skills Registry validated with NVIDIA OpenShell at NVIDIA GTC on March 16, 2026.

**Partnership**: JFrog + NVIDIA validated a workflow for ingestion and management of Artifactory as a skills registry, using NVIDIA cuOpt as the first packaged skill. JFrog Artifactory serves as a registry for AI models and agent skills with NVIDIA AI-Q Blueprint as part of NVIDIA Agent Toolkit.

**Features** (from April doc 03, lines 242–246, now GA):
- Centralized system of record for MCPs, models, agent skills, and agentic binary assets
- Automated security scanning — scans, verifies, and signs all AI skills upon upload
- Policy-driven governance with strict approval workflows
- Cryptographic provenance for all artifacts
- Separate JFrog MCP Registry for governing MCP servers

**April baseline**: JFrog identified as "enterprise-grade skill supply chain security" with NVIDIA partnership. Status was unclear. Now confirmed as GA with production integration.

### 2.3 Microsoft APM (Agent Package Manager, 2026)

**What shipped**: APM is a dependency manager for AI agents. Declare skills, prompts, instructions, plugins, and MCP servers in one `apm.yml` file; run `apm install` and get the same agent context across GitHub Copilot, Claude Code, Cursor, OpenCode, Codex, Gemini, Windsurf, and Kiro.

**Skills capabilities**:
- Install skills with `apm install vercel-labs/agent-skills` (bundle) or `apm install vercel-labs/agent-skills --skill deploy-to-vercel` (single skill), persisted to `apm.yml`
- Install from any git host; lock resolved commit in `apm.lock.yaml` for reproducibility
- Audit for hidden Unicode on every install/compile/unpack (zero config)
- Every install scans for hidden Unicode, pins content hashes, blocks transitive MCP servers unless explicitly declared or trusted
- Open source (MIT), built on AGENTS.md, Agent Skills, MCP

**Significance**: Microsoft converged on the same dependency-manager pattern as Lola and skills.sh — treat skills like npm packages with lockfiles and integrity checks.

**April gap**: Microsoft mentioned only as "Semantic Kernel / Copilot Studio / Agent Framework" with plugin model (doc 03, lines 49–72). APM is a new distribution layer above that.

### 2.4 Red Hat Lola (April 2026)

**What it is**: "Lola is able to package AI Context Modules or skills into a distributed package to be supported across multiple AI assistants. Think of your skill as the RPM package and Lola as the YUM/DNF."

**Components**:
- **Modules** (lolas): Portable packages bundling skills, command files, agent instructions (AGENTS.md), and MCP servers into a single cohesive group
- **Marketplaces** (Lola market): Curated catalogs of modules. Search and install AI context modules without manually hunting for repos.

**Origin**: Red Hat Product Security (`RedHatProductSecurity/lola`, GPL-2.0-or-later). Applies traditional Linux package management concepts (RPM/YUM/DNF) to AI assistant skills.

**April status**: Not mentioned. Appears to have launched between April and August.

**Observation**: Red Hat has at least three concurrent skills distribution efforts — Lola (Product Security), skills.sh integration (unknown owner), and the internal UIE Compass registry (see section 4).

---

## 3. Security: SkillSpector Maturation and ClawHub Crisis Aftermath

### 3.1 NVIDIA SkillSpector (Released 2026)

**What it is**: Security scanner for AI agent skills. Detects vulnerabilities, malicious patterns, and security risks. Released by NVIDIA in 2026 as the scanning layer under its NVIDIA-Verified Agent Skills program (announced May 19, 2026).

**Capabilities**:
- **68 vulnerability patterns** across 17 categories: prompt injection, data exfiltration, privilege escalation, supply chain, excessive agency, output handling, system prompt leakage, memory poisoning, tool misuse, rogue agent, anti-refusal, trigger abuse, dangerous code (AST), taint tracking, YARA signatures, MCP least privilege, MCP tool poisoning
- **Two-stage analysis**: Fast static analysis + optional LLM semantic evaluation
- **Live CVE lookups**: Via OSV.dev with automatic offline fallback
- **Risk scoring**: 0–100 scale with severity levels — 0–20 (LOW/SAFE), 21–50 (MEDIUM/CAUTION), 51–80 (HIGH/DO NOT INSTALL), 81–100 (CRITICAL/DO NOT INSTALL)
- **Open source**: Apache-licensed, actively maintained, thousands of GitHub stars

**Context**: Research shows 26.1% of skills contain vulnerabilities, 5.2% show likely malicious intent. Snyk scanned 3,984 published skills in Feb 2026: 36.8% had at least one security flaw, 13.4% a critical one, 76 confirmed malicious.

**April baseline**: "Security is first-order concern" post-ClawHub crisis (doc 03, line 41). SkillSpector is the first dedicated open-source scanner for skills, providing the supply chain tooling the ecosystem lacked.

### 3.2 ClawHub Crisis: Final Toll (Feb 2026)

**Timeline**:
- Jan 27, 2026: First malicious skill appears on ClawHub without being flagged
- Jan 31, 2026: Actor "hightower6eu" begins mass-uploading skills, eventually publishing 677 malicious packages
- Feb 1, 2026: Koi Security researcher Oren Yomtov publishes audit, names campaign "ClawHavoc"
- Feb 16, 2026: Confirmed malicious skills grow to 824+ across 10,700+ registry
- Bitdefender analysis: ~900 malicious packages (roughly 20% of total ecosystem)

**Attack methods**: Typosquatting, fake cryptocurrency wallets/trackers, Polymarket trading bots, YouTube utilities, auto-updaters, Google Workspace integrations. Primarily delivering Atomic macOS Stealer (AMOS).

**Root cause**: ClawHub open by default — only restriction was GitHub account age ≥1 week.

**April baseline**: "ClawHub security crisis (1,467 malicious skills discovered)" (doc 03, line 41). Final toll was lower (824–900) but still catastrophic at 11.9%–20% of the registry.

**Post-crisis measures** (from April doc 03, lines 226–229):
- Automated scanning
- Author verification badges
- Code signing for new submissions
- VirusTotal integration
- GitHub account age requirement (1 week)
- Community reporting and moderation hooks

**Comparison**: npm has ~2M packages with similar malware rates; PyPI similar. The ClawHub crisis proved AI skill registries face identical supply chain risks plus new prompt injection vectors.

### 3.3 NVIDIA Skills Repository Maturation

**GitHub stats** (as of Aug 2026):
- 2,800 stars (up from 2.7K in July, per April doc 02)
- 324 forks
- 489 commits on main
- Skills "synced from upstream product repos daily" via automated pipeline

**Catalog span**: 30+ NVIDIA product families (cuOpt, DOCA, DeepStream, Dynamo, Holoscan SDK, Isaac for Healthcare, Jetson, NeMo family, Nemotron, Physical AI/Omniverse, RAG Blueprint, TAO Toolkit, TileGym, Video Search & Summarization).

**Verified skills program** (roadmap completed):
- Public verified skills catalog with automated daily sync
- Security scanning and OMS signature signing for all skills
- Skill Cards with machine-readable metadata
- Syndication to external marketplaces — skills.sh, Codex plugin, Claude Code plugin, ClawHub, Hermes Hub

**Distribution**: Uses Vercel Labs `skills` CLI. Designed for installation into Claude Code, Codex, Cursor, Snowflake CoCo (Cortex), and Kiro. Follows agentskills.io specification. Dual-licensed: Apache 2.0 (source code), CC-BY-4.0 (docs/skills content).

**April baseline**: "Nvidia single-repo model endorsed by multiple Red Hat teams" (research brief). NVIDIA's centralized model with SkillSpector scanning, Skill Evaluator, OMS signing, and skill cards is now the reference implementation for governed skills distribution.

---

## 4. Red Hat's Internal Skills Ecosystem: The UIE/Compass Discovery

**Context**: On 2026-08-04, meetings revealed the existence of Red Hat's Unified Intelligence Engineering (UIE) org with a Compass skills registry and Light Trail MCP hosting team. This was a complete blind spot in April's external research.

### 4.1 What We Learned (2026-08-04)

| Component | Description | Source |
|-----------|-------------|--------|
| **UIE Org** | Unified Intelligence Engineering — 300+ engineer team | Meeting notes (2026-08-04) |
| **Compass** | Skills registry with security auditing, scorecards (gold=public, silver=internal), marketplace publishing | Meeting notes (2026-08-04) |
| **Light Trail Team** | Building MCP server hosting on MP+ (Marketplace Plus) | Meeting notes (2026-08-04) |
| **Ilan Pinto** | UIE team member (role unclear) | Meeting notes (2026-08-04) |
| **Mike Amburn Dixon** | AI & Offline Experiences Principal PM; UIE team member (role unclear) | Meeting notes (2026-08-04) |
| **Greg Bowman** | Marketplace strategy; arranging Compass alignment session | Meeting notes (2026-08-04) |

### 4.2 Public Evidence (Limited)

**Web search results** (2026-08-04):
- No public documentation of "UIE Unified Intelligence Engineering" as a Red Hat org
- No public documentation of "Compass" as a Red Hat skills registry
- No public documentation of "Light Trail" as an MCP hosting team
- Mike Amburn Dixon confirmed as AI & Offline Experiences Principal PM at Red Hat (LinkedIn)
- Ilan Pinto confirmed as Experienced Director of Software Engineering at Red Hat (LinkedIn)
- No public connection between these individuals and UIE/Compass/Light Trail

**HeadSpin Compass on Red Hat Marketplace** (March 2021): Unrelated product — self-serve test automation platform, not a skills registry.

### 4.3 Implications

1. **Parallel skills efforts**: Red Hat has at least three concurrent skills distribution initiatives:
   - **Lola** (Product Security) — package manager for AI context modules
   - **skills.sh integration** (unknown owner) — mentioned at Red Hat Summit 2026
   - **Compass** (UIE, 300+ engineers) — internal registry with gold/silver scorecards

2. **No "editor-in-chief" for Red Hat skills portfolio** (meeting notes, 2026-08-04): Multiple teams building overlapping capabilities without clear coordination.

3. **OCP5 skills distribution via operators** (meeting notes, 2026-08-04): OpenShift 5 ships core agentic skills as a single image; layered product skills with operators. Public evidence: GitHub `openshift/agentic-skills` repo, Red Hat Catalog "Agentic skill pack for Red Hat OpenShift" and "...for Red Hat OpenShift Virtualization".

4. **Greg Bowman arranging Compass alignment session** (meeting notes, 2026-08-04): Suggests marketplace strategy recognizes need to reconcile Compass with other efforts.

### 4.4 Red Hat Skills Repository (Public, Red Hat Summit 2026)

**What shipped**: Red Hat launched an agentic skills repository at Red Hat Summit (May 11–14, 2026), described as "Red Hat's skill packs give AI agents something a bigger model never could: 20 years of institutional memory."

**Architecture**: Curated skill packs encoding institutional knowledge about RHEL subscriptions, CVEs, patch advisories, and product lifecycles into reusable AI agent behaviors. Turns RHEL, OpenShift, and Ansible into governed AI agent platforms.

**Distribution**: skills.sh marketplace with one-command installation, telemetry-based popularity rankings, category filtering. GitHub `openshift/agentic-skills` repo provides OpenShift Container Platform skills for AI agents.

**Skill packs available**:
- Agentic skill pack for Red Hat OpenShift (spans Assisted Installer, OCM, ROSA, ARO, kubeconfig fleets)
- Agentic skill pack for Red Hat OpenShift Virtualization (10 specialized skills for VM lifecycle management)

**Philosophy**: "Rather than chasing larger models, Red Hat is layering agent skills on top of RHEL, OpenShift, and Ansible to turn AI copilots into governed enterprise superusers."

**Relationship to Compass**: Unclear. Public skills.sh presence may be a storefront for Compass-governed skills, or a separate effort. No public documentation connects the two.

---

## 5. OCP5 and Skills Distribution via Operators

**What we know from 2026-08-04**: "OCP5 ships core agentic skills as a single image, layered product skills with operators."

**Public evidence**:
- **Note**: Search results show OpenShift 4.x series only; no public documentation of "OpenShift 5" or "OCP5" found.
- GitHub `openshift/agentic-skills`: "OpenShift Container Platform skills for AI agents and OpenShift"
- Red Hat Catalog: "Agentic skill pack for Red Hat OpenShift" (Assisted Installer, OCM, ROSA, ARO, kubeconfig fleets)
- Red Hat Catalog: "Agentic skill pack for Red Hat OpenShift Virtualization" (10 VM lifecycle skills)
- Red Hat Developer article (July 21, 2026): "Operationalize AI agents with OpenShift and Kubernetes primitives" — skills encapsulate OpenShift-specific operational capabilities for managing Routes, Operators, and platform features across clusters. Kubernetes primitives make AI agents operationally manageable as workloads; update agentic routing rules, add specialists, inject institutional knowledge through ConfigMaps and PVs.

**Distribution model**: Skills distributed as:
1. **Core skills**: Single container image (OCI artifact)
2. **Layered product skills**: Delivered via operators (Operator Lifecycle Manager)

**Significance**: OpenShift skills distribution follows the same OCI artifact pattern identified in April research as the emerging enterprise standard.

---

## 6. Skills Packaging Landscape Update

### April Baseline (doc 03, lines 433–443)

| Format | Language Agnostic | Governance Ready | Distribution | Runtime Isolation | Dependency Mgmt |
|---|---|---|---|---|---|
| Python packages (pip) | No | No | PyPI | No | Yes (pip) |
| npm packages | No | No | npm registry | No | Yes (npm) |
| Container images (OCI) | Yes | Partial | OCI registries | Yes | Yes (container) |
| OCI artifacts | Yes | Partial | OCI registries | No | No |
| OpenAPI specs | Yes | No | URLs/files | No | No |
| MCP Registry packages | Partial | Yes | MCP Registry | Varies | Varies |
| Markdown/YAML | Yes | No | Git repos | No | No |

### August Update: Three New Package Managers

| Package Manager | Launched | Packaging | Lockfile | Security Scanning | Distribution | Multi-Agent Support |
|----------------|----------|-----------|----------|-------------------|--------------|---------------------|
| **Lola** (Red Hat) | 2026 | Modules (skills + AGENTS.md + MCPs) | Unknown | Unknown | Lola marketplaces | Yes (multi-assistant) |
| **APM** (Microsoft) | 2026 | apm.yml (skills + prompts + plugins + MCPs) | apm.lock.yaml | Hidden Unicode detection, content hash pinning | Git repos | Yes (Copilot, Claude, Cursor, Codex, Gemini, Windsurf, Kiro) |
| **skills.sh** (Vercel) | Jan 2026 | SKILL.md bundles | Unknown | Unknown | skills.sh directory | Yes (40+ agents) |

**Common pattern**: All three treat skills like npm packages — declarative manifest, lockfile for reproducibility, support for multiple agent runtimes, distribution via public/private registries.

**Verdict**: The April fragmentation (7+ formats) is consolidating around:
1. **SKILL.md** for skill definition (universal)
2. **Package managers** (Lola, APM, skills.sh) for dependency management
3. **OCI artifacts** for enterprise distribution (Databricks, JFrog, OpenShift)
4. **MCP Registry** for server-level packaging (Kong, AWS, Google, JFrog)

---

## 7. What Contradicts or Supersedes the April Research

### Contradictions

1. **"No standardized skills registry anywhere"** (April doc 03, line 33)
   - **Superseded**: Databricks Unity Catalog, JFrog Agent Skills Registry, and Microsoft APM all GA in Q2 2026.

2. **"Skills lack the deployment/runtime phase"** (April doc 04, line 65)
   - **Nuanced**: Still true for client-side skills (downloaded and executed locally). But server-side skills via Databricks Unity AI Gateway and AWS AgentCore now have a deployment/runtime phase — skills are hosted, governed, and executed remotely. The two consumption models (client-side vs. server-side, April doc 04, lines 147–150) have diverged further.

3. **"No platform fully solves skill composition"** (April doc 03, line 565)
   - **Still true**: Declarative skill chaining/composition (like Helm chart dependencies) remains immature. No updates since April.

4. **"Framework portability: no portable format across agent frameworks"** (April doc 04, line 201)
   - **Superseded by SKILL.md**: With 40+ tools supporting agentskills.io, portability is now the norm. Caveat: platform-specific features still require adaptation, but the base format is universal.

5. **Databricks skills registry prototype status** (April doc 04, line 119)
   - **Unclear**: Prototype was "targeting end of April 2026." Unity Catalog shipped with skills support at DAIS (June 2026). MLflow 3.15.0 (July 31, 2026) shipped with `mlflow agent setup` for installing curated skills from `github.com/mlflow/skills`. The standalone MLflow skills registry prototype may have been subsumed by Unity Catalog or may still be in development.

### Reinforcements

1. **"Security is a first-order concern"** (April doc 03, line 41)
   - **Reinforced**: ClawHub crisis toll (824–900 malicious skills), SkillSpector's 68 vulnerability patterns, and Snyk's finding that 36.8% of skills have at least one security flaw all confirm this.

2. **"OCI containers as the distribution standard"** (April doc 03, line 41)
   - **Reinforced**: OpenShift skills distribution via OCI images, OCI Artifacts specification for skills (v0.1.0, April 1, 2026), Docker's push for OCI artifacts for AI model packaging, and JFrog/Databricks/Harbor all using OCI-based distribution.

3. **"Enterprise governance is the differentiator"** (April doc 03, line 38)
   - **Reinforced**: Unity AI Gateway, JFrog Agent Skills Registry, and AWS AgentCore Policy all compete on governance (approval workflows, scanning, signing, policy enforcement), not on the number of skills in the catalog.

---

## 8. Key Takeaways for RHOAI Skills Registry

### What Changed That Matters

1. **SKILL.md is the standard** — No longer a bet; it's the reality. RHOAI skills registry should accept SKILL.md as the canonical format and provide tooling to convert other formats to it.

2. **Enterprise registries shipped** — Databricks, JFrog, and Microsoft all delivered production-grade skills registries in Q2. The bar is: automated scanning, cryptographic signing, policy-driven approval workflows, versioned artifact storage, cross-framework support, and supply chain provenance.

3. **Package managers are the new middleware** — Lola, APM, and skills.sh all position themselves as "npm for skills." RHOAI registry should provide a package manager integration layer (e.g., `rhoai install <skill>` CLI wrapping MLflow APIs).

4. **Security tooling is mandatory** — SkillSpector's 68 vulnerability patterns and ClawHub's 20% malicious skill rate prove that skills registries need automated scanning at ingestion time. RHOAI should integrate SkillSpector or Snyk for AI-specific scanning.

5. **Red Hat has multiple uncoordinated skills efforts** — Lola (Product Security), skills.sh (Summit launch), Compass (UIE, 300+ engineers), OpenShift skill packs (catalog). The RHOAI skills registry must either consolidate these or serve as a federation layer across them.

### What Didn't Change (Still Gaps)

1. **Skill composition** — No framework provides declarative dependency graphs for skills (e.g., "skill A requires skill B v1.2+"). This remains a differentiator opportunity for RHOAI.

2. **Testing frameworks** — Unlike Helm (`helm test`), no standard framework exists for skill testing and validation. RHOAI could provide a `skill-test` framework.

3. **Lifecycle governance automation** — Salesforce's maintenance framework (daily/weekly/monthly/quarterly checks, April doc 03, lines 166–180) is still the most mature, but no platform automates skill health monitoring. RHOAI could auto-detect stale skills, broken dependencies, and deprecated APIs.

4. **Client-side vs. server-side skills** — The two consumption models are "very disjoint" (April doc 04, line 150). Unity AI Gateway and AWS AgentCore Policy handle server-side governance well; client-side skills (downloaded and executed locally) have no comparable governance layer. RHOAI could provide a local policy agent that enforces registry-defined guardrails on client-side skill execution.

---

## Sources

### SKILL.md Standard Adoption
- [SKILL.md Open Standard Reaches 30+ AI Coding Tools](https://noqta.tn/en/news/skill-md-open-standard-30-ai-coding-tools-adoption-2026)
- [Agent Skills Open Standard Explained](https://www.paperclipped.de/en/blog/agent-skills-open-standard-interoperability/)
- [SKILL.md: The File Format That United OpenAI, Anthropic, Google, and Microsoft](https://mayursurani.medium.com/skill-md-the-file-format-that-united-openai-anthropic-google-and-microsoft-in-2026-2027-a5a0e4ad91ae)
- [Every AI Agent That Supports SKILL.md in 2026](https://www.agensi.io/learn/every-ai-agent-that-supports-skill-md-2026)
- [Specification - Agent Skills](https://agentskills.io/specification)
- [The Agent Skills Ecosystem in 2026](https://agentman.ai/blog/agent-skills-ecosystem-report-2026)

### Databricks Unity Catalog
- [What's new with Unity Catalog at Data + AI Summit 2026](https://www.databricks.com/blog/whats-new-unity-catalog-data-ai-summit-2026)
- [AI governance at Data + AI Summit 2026: What's new with Unity AI Gateway](https://www.databricks.com/blog/ai-governance-data-ai-summit-2026-whats-new-unity-ai-gateway)
- [Unity AI Gateway: Multi-AI governance and cost control](https://www.databricks.com/product/artificial-intelligence/unity-ai-gateway)
- [Agent Bricks: Data + AI Summit 2026](https://www.databricks.com/blog/agent-bricks-dais-2026)
- [Databricks Genie One, Agent Bricks, and What Builders Need to Know](https://chatforest.com/builders-log/databricks-genie-one-agent-bricks-dais-2026-builder-guide/)
- [Accelerate AI Development with Databricks: MCP and Agent Bricks](https://www.databricks.com/blog/accelerate-ai-development-databricks-discover-govern-and-build-mcp-and-agent-bricks)

### NVIDIA SkillSpector and Skills
- [GitHub - NVIDIA/SkillSpector](https://github.com/nvidia/skillspector)
- [NVIDIA-Verified Agent Skills Provide Capability Governance](https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/)
- [GitHub - NVIDIA/skills](https://github.com/nvidia/skills)
- [SkillSpector: NVIDIA's open-source security scanner for AI agent skills](https://www.helpnetsecurity.com/2026/08/03/skillspector-open-source-agent-skill-security-scanner/)
- [NVIDIA SkillSpector: AI Agent Skill Security Scanner — 2026 Guide](https://www.explainx.ai/blog/nvidia-skillspector-ai-agent-skill-security-scanner-2026)

### JFrog and NVIDIA Partnership
- [JFrog Delivers Trust Layer for AI-Driven Software with NVIDIA](https://investors.jfrog.com/news/news-details/2026/JFrog-Delivers-Trust-Layer-for-AI-Driven-Software-with-NVIDIA/default.aspx)
- [JFrog and NVIDIA partner to launch Agent Skills Registry](https://www.sahmcapital.com/news/content/jfrog-and-nvidia-partner-to-launch-agent-skills-registry-for-ai-agent-governance-2026-03-16)
- [JFrog Launches Agent Skills Registry To Govern AI Agents Running On Nvidia Infrastructure](https://smbtech.au/news/jfrog-launches-agent-skills-registry-to-govern-ai-agents-running-on-nvidia-infrastructure/)

### ClawHub Security Crisis
- [The OpenClaw security crisis](https://conscia.com/blog/the-openclaw-security-crisis/)
- [ClawHub Incident: 341 Malicious Skills Exposed](https://www.termdock.com/en/blog/clawhub-malicious-skills-incident)
- [Researchers Find 341 Malicious ClawHub Skills Stealing Data](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)
- [ToxicSkills and ClawHavoc — The Agent Skills Security Crisis (2026)](https://www.agensi.io/learn/toxicskills-clawhavoc-agent-skills-security-crisis-2026)
- [OpenClaw's Skill Marketplace and the Emerging AI Supply Chain Threat](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/)

### Package Managers
- [Microsoft APM: Package Manager for AI Agents](https://microsoft.github.io/apm/)
- [GitHub - microsoft/apm](https://github.com/microsoft/apm)
- [Agent Package Manager (APM): A DevOps Guide to Reproducible AI Agents](https://dev.to/pwd9000/agent-package-manager-apm-a-devops-guide-to-reproducible-ai-agents-4c25)
- [Manage AI context with the Lola package manager](https://developers.redhat.com/articles/2026/04/08/manage-ai-context-lola-package-manager)
- [GitHub - RedHatProductSecurity/lola](https://github.com/RedHatProductSecurity/lola)
- [Vercel Introduces Skills.sh](https://www.infoq.com/news/2026/02/vercel-agent-skills/)
- [The Agent Skills Directory](https://www.skills.sh/)

### Red Hat Skills Repository
- [Red Hat's skill packs give AI agents 20 years of institutional memory](https://thenewstack.io/red-hat-agentic-skills-repository/)
- [GitHub - openshift/agentic-skills](https://github.com/openshift/agentic-skills)
- [Agentic skill pack for Red Hat OpenShift](https://catalog.redhat.com/en/ai/skills/detail/agentic-skill-pack-for-red-hat-openshift)
- [Agentic skill pack for Red Hat OpenShift Virtualization](https://catalog.redhat.com/en/ai/skills/detail/agentic-skill-pack-for-red-hat-openshift-virtualization)
- [Operationalize AI agents with OpenShift and Kubernetes primitives](https://developers.redhat.com/articles/2026/07/21/operationalize-ai-agents-openshift-and-kubernetes-primitives)
- [Building skills for AI agents: pitfalls and best practices](https://next.redhat.com/2026/07/28/building-skills-for-ai-agents-pitfalls-and-best-practices/)

### OCI Artifacts for Skills
- [GitHub - ThomasVitale/agents-skills-oci-artifacts-spec](https://github.com/ThomasVitale/agents-skills-oci-artifacts-spec)
- [Agent Skills as OCI Artifacts](https://www.thomasvitale.com/agent-skills-as-oci-artifacts/)
- [Manage and distribute skills with skills-oci](https://www.salaboy.com/2026/04/19/manage-and-distribute-skills-with-skills-oci/)
- [Why Docker Chose OCI Artifacts for AI Model Packaging](https://www.docker.com/blog/oci-artifacts-for-ai-model-packaging/)

### MLflow
- [MLflow 3.15.0 Release](https://mlflow.org/releases/)
- [MLflow and APX Skills](https://deepwiki.com/databricks-solutions/ai-dev-kit/2.4-mlflow-and-apx-skills)
