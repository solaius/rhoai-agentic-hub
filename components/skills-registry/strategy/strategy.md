---
title: Skills Registry — strategy
description: Red Hat's MLflow-native, hybrid-first skills governance platform — upstream design ownership, enterprise differentiation, and the competitive window
timestamp: 2026-08-04
status: current
review_after: 2026-10-04
source: hub.strategy synthesis from 8-doc research series + 14 knowledge entries, 2026-08-04
---

## The brief

Red Hat now **owns the upstream MLflow skills registry design** through Bill Murdock's authorship of RFC-0008/0009. What was a "submit before Databricks" race in April became Red Hat defining the canonical specification by August. The bet: MLflow-native, Kubernetes-governed, hybrid-first skills governance for enterprises that lack Unity Catalog's centralized platform — the **only open-source option** spanning on-prem, edge, and multi-cloud. The format war is over (SKILL.md won, 40+ tools adopted). Enterprise registries shipped (Databricks Unity Catalog, JFrog, AWS, Microsoft APM). Our window narrowed but our differentiation strengthened: every competitor locks to one cloud; Red Hat delivers portable governance. **Next gate**: Thursday 2026-08-07 PM sync with Databricks — secure user-journey buy-in, then technical merge. Timeline risk: RFC-0008 open 3 weeks, no merge yet; if upstream stalls, parallel paths (Kubeflow hub, midstream, OCP5 ecosystem) activate.

## What

Skills Registry is the **governance and system-of-record layer** for AI agent skills — versioning, lifecycle states, approval workflows, security scanning, cryptographic signing, provenance tracking, and audit trails. It **is not a catalog** (discovery/storefront lives in skills-catalog via Kubeflow hub).

| Release | Scope | Status |
|---------|-------|--------|
| **Upstream MLflow** | RFC-0008 (skills/bundles MVP), RFC-0009 (extended bundles/subagents/MCP), package manager plugin interface (APM, LOLA, OCI) | RFC-0008 open (PR #26, 28 commits), RFC-0009 draft (PR #27); skills CLI shipped MLflow 3.14, MCP Registry shipped 3.15 |
| **RHOAI 3.6 DP/TP** | Skills Registry TP alongside MCP Registry TP (RHAISTRAT-2027 integration) — skill-level tracing, RBAC, OPA policy, SkillSpector scanning, Red Hat signing | Unscheduled; roadmap shows Registry work post-3.6 EA2; no committed DP target |
| **RHOAI 3.6 GA / 3.7** | Skills Registry GA with trust tiers (Red Hat Verified / Community Verified / Unverified), EU AI Act compliance kit, OpenShift sandboxed containers for runtime isolation | Directional; formal GA milestone TBD |

**Boundaries** (what this is NOT):

- **Not skills-catalog**: The catalog is the discovery/storefront layer (Kubeflow hub surface, search/browse UX) — this is governance/versioning
- **Not agent-registry**: Agent Registry governs post-deployment agent instances (running agents, their configs, fleet management) — Skills Registry governs the reusable capabilities (skills) agents consume
- **Not MCP Registry**: MCP Registry governs MCP servers (tool providers); Skills Registry governs skills (capabilities); both share governance primitives (lifecycle, approval, scanning, signing)

**Key routing decision** (from [/memory/profiles/strategy.md](/memory/profiles/strategy.md)): Registry = Governance (MLflow upstream). Catalog = Discovery (Kubeflow hub downstream). Metadata-first, plugin-based extensibility.

## Why

### The problem

**Red Hat's enterprise customer base** (financial services, healthcare, government, telecom) faces a governance crisis competitors don't see:

1. **No centralized governance platform**: Databricks customers have Unity Catalog; Red Hat's customers run fragmented multi-cloud/on-prem stacks with no equivalent
2. **Shadow AI sprawl**: 3 customers [built their own registries](/components/skills-registry/research/08-user-journeys-databricks-alignment.md) because "we can't use public skill catalogs; we're a regulated entity; every AI asset needs supply chain security"
3. **Regulatory forcing function**: [EU AI Act enforcement began Aug 2, 2026](/components/skills-registry/research/06-competitive-skills-registries-2026-08.md) — high-risk AI systems require tamper-evident logging, continuous risk management, post-market monitoring
4. **ClawHub crisis validated supply chain risk**: 800+ malicious skills (12-20% of registry), CVE-2026-25253 (CVSS 8.8 RCE), [China banned government use](/components/skills-registry/research/05-skills-landscape-refresh-2026-08.md) — proved AI skills need identical supply chain security as software packages

### Jobs served

1. **IT Security**: Discover shadow AI (47 ungoverned skills across 23 agents), assess risk, enforce policy
2. **Compliance Officers**: Generate EU AI Act audit trails (skill provenance, signing, approval workflows)
3. **Platform Engineers**: Respond to CVE in skill dependencies (understand blast radius, coordinate patching, verify remediation)
4. **Data Scientists**: Publish skills with automated approval workflows (security scan → architecture review → VP sign-off)
5. **AI Developers**: Discover compliant skills (trust tier badges, security scan status, IT approval visible at search time)
6. **Agent Runtimes**: Dynamically load approved skills with policy enforcement (IAM-based access control, lineage tracking)

### Market position

[Competitive analysis](/components/skills-registry/research/06-competitive-skills-registries-2026-08.md) shows **Red Hat is the only hybrid-first, MLflow-native, open-source option**:

| Competitor | Strength | Red Hat Differentiator |
|------------|----------|------------------------|
| **Databricks Unity AI Gateway** | MLflow-native, contextual policies, first-class UC governance | Cloud-only; RH offers same MLflow integration + on-prem/edge deployment |
| **AWS Agent Registry** | Cedar policy, semantic search, 3-persona model | AWS-only; RH multi-cloud with OPA (broader K8s ecosystem adoption) |
| **Google Cloud API Registry** | GCP integration, MCP via Apigee | GCP-only; RH not locked to one cloud |
| **JFrog + NVIDIA** | SkillSpector scanning, supply chain security, provenance | Cloud-agnostic but not K8s-optimized; RH offers tighter OpenShift integration |
| **Microsoft APM** | Unified SK+AutoGen, lockfiles, MCP steering committee | Azure-first; RH framework-agnostic (works with LangChain, AutoGen, CrewAI, etc.) |
| **Anthropic Marketplace** | Curated quality, ~600 skills, MCP leadership | Cloud-only, no enterprise governance dashboard; RH offers curated + community + private |

**Why now**: [SKILL.md crossed the chasm](/components/skills-registry/research/05-skills-landscape-refresh-2026-08.md) (40+ tools in 4 months), enterprise registries shipped GA in Q2 2026, [RFC strategy pivoted to user-journeys-first](/components/skills-registry/knowledge/fact-rfc-strategy-user-journeys-before-technical.md) creating alignment window with Databricks.

## Where we stand

### Decisions to date

- **2026-07-23**: [Push skills and agent registry RFCs upstream simultaneously](/components/skills-registry/knowledge/decision-dual-rfc-push-upstream.md) — stop self-throttling; RH has second MLflow maintainer, community calls starting
- **2026-07-14**: [RFC split into two phases](/components/skills-registry/knowledge/fact-skills-rfc-split-databricks.md) — RFC-0008 (skills/bundles MVP), RFC-0009 (extended bundles with subagents/hooks/MCP) per Databricks request
- **2026-08-04**: [RFC strategy evolved to user-journeys-first](/components/skills-registry/knowledge/fact-rfc-strategy-user-journeys-before-technical.md) — vision alignment before technical details; learned from MCP Registry delay

### Delivery state

**Upstream MLflow**:
- RFC-0008 (PR #26): **Open** since Jul 14; 28 commits; reviewed by mprahl (RH), HumairAK (Databricks maintainer), B-Step62 (Yuki, Databricks tech lead)
- RFC-0009 (PR #27): **Draft** since Jul 23; 2 commits; no reviews yet (parked pending RFC-0008 approval)
- MLflow 3.14 (Jun 17, 2026): `mlflow agent setup`, `mlflow skills view/list` CLI shipped
- MLflow 3.15 (Jul 31, 2026): MCP Registry shipped (Dan Kuc contributed docs)

**Red Hat contributors**:
- **Bill Murdock (jwm4)**: RFC author (Skills Registry MVP + Extended Bundles) — owns upstream design
- **Matt Prahl (mprahl)**: MLflow maintainer, RFC reviewer, PM liaison to Databricks
- **Dan Kuc (dkuc)**: MCP Registry docs contributor (PRs #24713, #24519)

**RHOAI product**: No fixversions yet; roadmap shows Registry work starts 3.6 EA2 at earliest ([/memory/profiles/roadmap.md](/memory/profiles/roadmap.md)), multi-release path to DP (~3.7 directional, no committed GA).

### In-flight work

- **Thursday 2026-08-07 PM sync**: Databricks PM Adam + tech lead Yuki — present user-journey vision doc + UI mockups ([prep materials in doc 08](/components/skills-registry/research/08-user-journeys-databricks-alignment.md))
- **RFC-0008 merge push**: Address B-Step62 feedback (UI mockups, field inference, versioning scheme); mprahl suggested deferring trace linking to accelerate merge
- **Compass alignment session**: Greg Bowman arranging follow-up with UIE/Compass team (300+ engineer org with internal skills registry discovered 2026-08-04; [landscape refresh doc 05](/components/skills-registry/research/05-skills-landscape-refresh-2026-08.md))

## Gaps & risks

### Open questions

- **[Mitigation if MLflow upstream blocked](/components/skills-registry/knowledge/question-mitigation-if-mlflow-upstream-blocked.md)**: What if RFCs approved but implementation delayed? Options: midstream fork, Kubeflow hub surface (fastest for 3.6), OCP5 ecosystem team, invest in other products. **Why it matters**: customers building own solutions; speed critical per competitive pressure.
- **[Skills packaging format gaps](/components/skills-registry/knowledge/question-skills-packaging-format-gaps.md)**: RFC-0008 PackageManagerPlugin interface resolves multi-format coexistence (APM, LOLA, NPM, OCI as plugins), but no single standard emerged and plugin interface not merged. **Why it matters**: enterprise customers need deterministic, signed, reproducible skill installation — lockfile patterns proven (npm, pip, APM) but not standardized for skills.
- **Skills customization framework need** ([fact](/components/skills-registry/knowledge/fact-skills-customization-framework-need.md)): Generic skills impractical for enterprise SDLC (every pipeline differs); Josh Salomon prototyping extension-point model in Ozark (POC ~2 weeks from 2026-08-04). **Why it matters**: without customization, enterprises fork skills → lose upstream updates → governance breaks.

### Research risks

From [executive summary doc 00](/components/skills-registry/research/00-executive-summary.md):

1. **Databricks governance disconnect** ([fact](/components/skills-registry/knowledge/fact-databricks-mlflow-governance-disconnect.md)): Databricks uses Unity Catalog for governance, not MLflow; "make MLflow famous" mantra means they won't prioritize non-Databricks-roadmap work unless proven to increase GenAI adoption. **Why it matters**: RFC merge depends on showing Databricks PM Adam that governance gap exists for non-UC customers.
2. **UIE/Compass blind spot**: 300+ engineer team with own skills registry (gold/silver scorecards, marketplace publishing); RHAI unaware until 2026-08-04. **Why it matters**: fragmented RH skills efforts (LOLA, skills.sh, Compass, OCP5 operators) — no "editor-in-chief" for portfolio coordination.
3. **No skills portfolio owner**: Light Trail (MCP hosting), Compass (UIE registry), LOLA (Product Security), OCP5 operators, RHAI MLflow — at least 3 parallel efforts. **Why it matters**: customer-facing story fragmented; internal competition for resources.
4. **Ramesh's position** ([fact](/components/skills-registry/knowledge/fact-ramesh-skills-governance-position.md)): Skills are static resources needing no governance; governance belongs at agent level; catalog value > registry value for skills. **Why it matters**: internal disagreement on product framing could slow prioritization.

### Tensions

1. **Speed vs. upstream-first**: Customers demanding DP fast ("taking on competitors' work streams," per doc 08); upstream RFC merge timeline uncertain (3 weeks open, no merge). Myriam argues proper collaboration > rushing; Peter counters competitive pressure forces speed.
2. **MLflow fame vs. governance**: Bill noted tension between "fame" (mass audience) and "governance" (IT execs controlling developers) may be structural headwind. Databricks optimizes for fame; RH needs governance.
3. **Generic skills vs. customization**: Current SKILL.md format is single-tenant; enterprise needs multi-tenant (same skill, many environments). Extension-point model (Josh's POC) is skills v2.0 but needs upstream buy-in.

## Jira map

**Coverage**: No `jira:` block in [components.yaml](/components/components.yaml) for skills-registry yet — first gap to address.

**Known related Jira** (from knowledge entries and research):

- **Upstream MLflow**: RFC-0008 (PR #26), RFC-0009 (PR #27), Issue #22833 (skills registry FR), PR #21725 (skills as evaluation criteria, stalled since May)
- **Skills-catalog Jira** (shared dependencies): RHAISTRAT-1780 (skills catalog), RHAISTRAT-1940 (pre-loaded skills), RHAISTRAT-1339 (multi-asset catalog)
- **RHOAI integration**: RHAISTRAT-2027 (Catalog-Registry integration, 3.6 EA1 target)

### Candidate jiras

| Gap | Problem Statement | Suggested Project |
|-----|-------------------|-------------------|
| **No skills-registry Jira scope** | Skills Registry component untracked in RHAISTRAT; work happening upstream (MLflow RFCs) and in meetings but no product planning artifacts | Create RHAISTRAT outcome (e.g., "Skills Registry TP in RHOAI 3.6/3.7") with child features for: SkillSpector integration, Red Hat signing, trust tiers, EU AI Act compliance kit, RBAC/OPA policy enforcement |
| **No upstream RFC merge milestone tracking** | RFC-0008/0009 status not visible in RHOAI planning; risk of silent drift if upstream stalls | Create RHAISTRAT feature request "Track MLflow Skills Registry RFC merge and RHOAI integration dependencies" |
| **Skills customization framework gap** | Josh Salomon's extension-point POC (Ozark) has no product home; enterprise need validated but no owner | Create RHAIRFE feature request "Skills customization framework with extension points" (link to /components/skills-registry/knowledge/fact-skills-customization-framework-need.md) |
| **SkillSpector integration unscheduled** | Competitive analysis shows NVIDIA SkillSpector as security gold standard; JFrog + NVIDIA partnership validates scan-verify-sign pipeline; Red Hat has no integration plan | Create feature "Integrate NVIDIA SkillSpector into Skills Registry publishing pipeline" |
| **Red Hat skills portfolio coordination gap** | UIE/Compass, LOLA, skills.sh, OCP5 operators, RHAI MLflow — no coordination, no editor-in-chief | Create RHAISTRAT outcome "Red Hat skills portfolio strategy and coordination" (cross-team alignment) |
| **Databricks PM sync outcomes untracked** | Thursday PM syncs with Databricks PM Adam + Yuki are critical alignment forum but outcomes not captured in Jira | Create recurring task "Document Databricks PM sync outcomes and RFC blockers" |

## Watchlist

External triggers that would change this strategy:

- **2026-08-07 — Databricks PM sync outcome**: If user-journey buy-in NOT secured, re-evaluate RFC strategy and parallel paths (Kubeflow hub, midstream). If secured, technical RFC proceeds with higher confidence of merge.
- **2026-09-01 — RFC-0008 merge status**: If not merged by early September (7+ weeks open), activate mitigation options from [open question](/components/skills-registry/knowledge/question-mitigation-if-mlflow-upstream-blocked.md) — midstream, Kubeflow surface, OCP5 ecosystem.
- **2026-10-23 — RHOAI 3.6 code freeze**: If Skills Registry TP not in 3.6 fixversions by code freeze, GA timeline slips to 3.7+ — customer commitments at risk.
- **2026-12-01 — EU AI Act high-risk deadline approach**: Compliance deadline Dec 2027 creates enterprise demand spike for governance; if RH not GA by mid-2027, customers adopt competitor solutions (AWS, Google, Databricks).
- **Q4 2026 — Competitive GA convergence**: AWS Agent Registry preview → GA, Google Cloud API Registry → GA, Databricks Unity AI Gateway GA expansions — if all ship before RH DP, positioning shifts from "first mover" to "open alternative."
- **Q1 2027 — NVIDIA/JFrog partnership expansion**: If JFrog becomes de facto enterprise skills registry (via NVIDIA ecosystem), RH risks "me too" positioning — partnership opportunity closes.
- **2026-08-04 — UIE/Compass discovery**: If Compass skills registry (300+ engineers) becomes RH's official solution, RHAI MLflow investment redirects or consolidates.
- **Ongoing — Josh Salomon POC completion (~2 weeks from 2026-08-04)**: If extension-point model proves viable, skills customization becomes differentiation vs. generic-skill-only competitors; if fails, generic SKILL.md format limitation remains.

## History

- **2026-08-04** — **Creation** — initial strategy doc synthesized from 8-doc research series (landscape refresh, competitive, upstream MLflow, user journeys) plus 14 knowledge entries (decisions, facts, questions, people, references). Research covers April-August 2026 period: SKILL.md universality (40+ tools), enterprise registries shipped (Databricks Unity Catalog, JFrog, Microsoft APM, AWS preview), Red Hat authorship of RFC-0008/0009 (Bill Murdock), RFC strategy pivot (user-journeys-first), Databricks governance disconnect (Unity Catalog not MLflow), UIE/Compass discovery (internal fragmentation), skills customization need (Josh Salomon POC), ClawHub crisis aftermath (800+ malicious skills validated supply chain risk), EU AI Act enforcement start (Aug 2, 2026).
