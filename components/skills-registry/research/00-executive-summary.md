---
title: Skills Registry Research - Executive Summary
description: Synthesis of all skills ecosystem research into actionable findings for RHOAI Skills Registry strategy.
source: ai-asset-registry/skills/skills-registry/research/00-executive-summary.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Skills Registry Research - Executive Summary

**Date**: 2026-04-15
**Author**: Peter Double (Principal PM - MCP & AI Asset Registries)
**Purpose**: Synthesize all skills ecosystem research into actionable findings for RHOAI Skills Registry strategy.

---

## The Bottom Line

**There is no standardized skills registry anywhere.** The market has tool definitions (MCP), agent protocols (A2A), packaging formats (npm, OCI, pip), and community catalogs (ClawHub, LangChain Hub) — but no one has built the governance layer. MLflow issue #20435 is literally waiting for a design proposal. This is Red Hat's gap to fill.

---

## Research Documents

| # | Document | What It Covers |
|---|----------|---------------|
| 01 | [Skills Ecosystem](01-skills-ecosystem.md) | Terminology, framework analysis, packaging formats, metadata schemas, composition patterns, standards |
| 02 | [MLflow Upstream](02-mlflow-upstream.md) | MLflow issues/PRs, registry architecture, Databricks prototype, Red Hat contributor activity |
| 03 | [Skill Management Landscape](03-skill-management-landscape.md) | 30+ platforms surveyed, feature comparison matrix, enterprise vs. open source, emerging standards |
| 04 | [RHOAI Patterns & Meetings](04-rhoai-patterns-and-meetings.md) | MCP registry patterns, meeting transcript analysis, decisions, open questions, people |

---

## Ten Key Findings

### 1. "Skill" means different things at different levels
At the tool level (LangChain, CrewAI), a skill = a function. At the plugin level (Semantic Kernel), a skill = a group of functions. At the agent level (A2A), a skill = a capability. For RHOAI, the right level is **the Semantic Kernel/A2A level: a named, versioned, reusable capability** that may contain multiple tools.

### 2. No unified skills specification exists
MCP standardizes tool-level protocol. A2A standardizes agent-level discovery. **Nobody standardizes the skill layer in between** — packaging, lifecycle, composition, governance. This is the gap.

### 3. The SKILL.md format is emerging as de facto standard
Launched by Anthropic (Dec 2025), adopted by OpenAI Codex, Google Gemini CLI, GitHub Copilot, VS Code. Directory with YAML frontmatter + markdown instructions + optional scripts/resources. Progressive disclosure model (metadata at startup, instructions on demand, resources during execution).

### 4. MLflow has no skills registry — and is waiting for one
- Issue #20435 requests skills version management. Maintainer Corey Zumar invited a design proposal in February. Nobody has submitted one.
- PR #21725 adds skills to evaluation framework only (not registry).
- The Databricks prototype stores markdown as MLflow artifacts (privately, not public).
- The likely path: skills as a specialized entity type extending the Prompt Registry pattern.

### 5. Packaging is fragmented across 7+ formats
Python packages, npm, OCI containers, OCI artifacts, OpenAPI specs, MCP Registry packages, Markdown/YAML. The meeting consensus: skills are "more like prompts than MCPs" — file-based, not deployed services. OCI artifacts are "heavy" and "not consumable" for individual skills (Hunter Gerlach, Ann Marie Fred).

### 6. Security is a first-order concern
The ClawHub crisis (12-20% malicious skills, CVE-2026-25253 for RCE) proved skill registries face supply chain attacks identical to npm/PyPI plus prompt injection vectors. JFrog's scan-verify-sign approach is the enterprise standard. Skills contain executable code — need code scanning, not just container scanning.

### 7. Two consumption models exist: client-side vs. server-side
- **Client-side**: Download skill code, run it locally in your agent (currently dominant)
- **Server-side**: Server executes the skill via Responses API (emerging, more governable)
- These are "very disjoint right now" (Ann Marie Fred) — the registry needs to support both.

### 8. The MCP registry pattern transfers directly (7/10 user stories)
The two-tier entity model (Skill + SkillVersion), four governance tracks (lifecycle, approval, verification, certification), workspace scoping, and trust tiers all apply unchanged. The key difference: skills have no deployment/runtime phase — steps 6-7 of the 8-stage lifecycle are fundamentally different.

### 9. Enterprise governance is the differentiator
AWS Agent Registry (preview April 2026) has Cedar-based policy. IBM watsonx Orchestrate has 400+ validated tools. JFrog provides cryptographic provenance. Google has Cloud API Registry for tool governance. None of them are open source or run on-prem. **Red Hat's differentiation: enterprise-grade governance for skills running on your infrastructure.**

### 10. Three critical decisions are unresolved
1. **Skills catalog: yes or no?** Peter is skeptical; Adam says catalogs always come first with customers.
2. **Packaging format**: No consensus — markdown files, OCI artifacts, zip bundles? Start with markdown in MLflow artifacts.
3. **Relationship to Llama Stack Skills API**: Francisco Arceo is building this. Complement or compete?

---

## Competitive Positioning

| Competitor | Strength | RHOAI Differentiator |
|------------|----------|---------------------|
| AWS Agent Registry | Cedar-based policy, semantic search | Open source, on-prem, federated (MLflow + Kubeflow) |
| IBM watsonx Orchestrate | 400+ tools, "any agent any framework" | Not locked to IBM cloud, deeper governance |
| Google Cloud API Registry | Native GCP integration | Multi-cloud, hybrid, self-managed |
| JFrog Agent Skills Registry | Supply chain security, provenance | Broader governance (lifecycle, approval, certification), not just security |
| ClawHub (OpenClaw) | 18K+ skills, community scale | Enterprise governance, security, trust tiers |
| Kong MCP Registry | API governance integration | Full AI asset lifecycle, not just MCP |
| Microsoft Copilot Studio | Enterprise deployment, MCP steering | Open source, framework-agnostic |

---

## Architecture Patterns Worth Adopting

### From MCP Registry (internal)
- Two-tier entity model (Skill + SkillVersion)
- Four independent governance tracks
- Workspace-scoped RBAC
- Metadata-first records
- "Store state, automate later" MVP approach

### From the Market
- **Three-persona model** (AWS): Admin / Publisher / Consumer
- **Trust tiers with publisher verification** (VS Code Marketplace, JFrog)
- **Progressive disclosure** (SKILL.md spec): metadata at startup, content on demand
- **Policy-as-code** (AWS Cedar): External policy enforcement
- **Supply chain security** (JFrog): Scan, verify, sign on upload

### From Developer Ecosystems
- **SemVer + lockfiles** (npm/pip): Version pinning for reproducibility
- **Organizational scoping** (npm @org/package): Prevent name squatting
- **OCI distribution** (Docker Hub): Leverage existing registry infrastructure
- **Declarative packaging with overrides** (Helm): Template/values separation

---

## Recommended Next Steps

### Immediate (This Week)
1. **Follow up with Edson Tirelli** on Databricks prototype status — is the end-of-April target still on track?
2. **Contact Matt Prahl** about Red Hat requirements already shared with Databricks via Slack
3. **Review Microsoft Azure Skills** (https://github.com/microsoft/azure-skills) — Microsoft expressed interest in Red Hat's skills future

### Short-Term (April-May)
4. **Draft a design proposal for MLflow issue #20435** — skills version management. This is the upstream opportunity. Nobody else has done it.
5. **Define RHOAI skill descriptor schema** — synthesize MCP annotations, A2A skill fields, and governance metadata into a proposed schema
6. **Decide on packaging MVP** — recommend starting with SKILL.md format stored as MLflow artifacts (aligned with Databricks prototype), with OCI artifact packaging as Phase 2

### Medium-Term (3.5 Planning)
7. **Write skills registry user stories** — adapt 7 transferable MCP user stories + add skills-specific stories (consumption, dependency tracking)
8. **Resolve catalog question** — is a skills catalog needed for 3.5, or is registry-only sufficient for Dev Preview?
9. **Define skills ingestion pipeline** — adapted from MCP pipeline: validate -> scan code -> evaluate -> register (no containerize step)
10. **Coordinate with Francisco Arceo** on Llama Stack Skills API alignment

---

## Open Questions for Stakeholder Input

1. **Peter**: Do you want to submit the MLflow #20435 design proposal, or should Red Hat engineering (Dan Kuc/Matt Prahl) drive it?
2. **Adam Bellusci**: For 3.5 Dev Preview, is skills registry alone sufficient or is catalog also needed?
3. **Edson Tirelli**: What's the actual status of the Databricks prototype? Can we see it?
4. **Ann Marie Fred**: Did the ODH repo for validated skills proceed? Can we build on it?
5. **Adel Zaalouk**: How do skills fit into the agentic strategy for Summit messaging?

---

## File Index

```
skills/skills-registry/research/
  00-executive-summary.md          <- This file
  01-skills-ecosystem.md           <- Terminology, frameworks, packaging, metadata, standards
  02-mlflow-upstream.md            <- MLflow issues, PRs, architecture, Databricks context
  03-skill-management-landscape.md <- 30+ platforms, comparison matrix, market gaps
  04-rhoai-patterns-and-meetings.md <- MCP patterns, meeting transcripts, decisions, people
```
