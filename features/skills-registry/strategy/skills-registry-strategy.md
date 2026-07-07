---
title: Skills Registry — RHOAI Strategy
description: Strategy for governed identity, versioning, lifecycle state, and metadata for AI skills in RHOAI as metadata-first records.
source: ai-asset-registry/skills/skills-registry/strategy/skills-registry-strategy.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Skills Registry — RHOAI Strategy

## Summary

The Skills Registry provides governed identity, versioning, lifecycle state, and metadata for AI skills in Red Hat OpenShift AI. Skills are reusable AI capabilities — backed by any combination of MCP servers, CLI tools, templates, configurations, prompts, or scripts — that agents and workflows consume. The registry governs these capabilities as metadata-first records so that catalog, consumption surfaces, and governance workflows operate from a single source of truth.

This document defines the full strategy for skills in RHOAI, covering upstream contributions to MLflow, downstream governance and platform integration, and the roadmap for phased delivery.

## Problem

AI skills are proliferating across frameworks, formats, and distribution channels (ClawHub, LangChain Hub, Azure Skills, OpenAI Codex Skills, vendor catalogs). Enterprises face:

1. **No governance**: Skills are consumed ad-hoc by agents with no visibility into what's running, who approved it, or what version is in use
2. **No standard packaging**: Skills exist as markdown files, Python packages, npm modules, container images, and zip bundles — with no consistent metadata or manifest format
3. **No lifecycle management**: Skills are created and consumed with no versioning, deprecation, or retirement process
4. **Supply chain risk**: The ClawHub crisis (12-20% malicious skills) demonstrated that skill registries face the same supply chain attacks as npm/PyPI, with added prompt injection vectors
5. **No asset relationships**: Skills depend on specific MCP servers, models, prompts, and other skills — but these dependencies are implicit and untracked

RHOAI needs a governed skills capability that lets enterprises discover, trust, version, and consume skills across their AI platform.

## Definition: What is a Skill?

A skill in the RHOAI context is a **named, versioned, reusable AI capability** that may be backed by any combination of:

- MCP servers (tool-serving capabilities)
- CLI tools and scripts
- Prompt templates and configurations
- Instruction sets (SKILL.md format)
- Code libraries or modules

Skills exist above individual tools but below full agents in the abstraction hierarchy:

```
Agent (composed runtime capability)
  └── Skills (reusable capabilities — governed in this registry)
        └── Tools / MCP Tools (atomic functions)
```

**What a skill is NOT**: A skill is not a container that needs deployment like an MCP server. Skills are consumed as artifacts — downloaded, referenced, or resolved by agents and frameworks. Some skills may reference deployed MCP servers, but the skill itself is a governance and packaging construct, not a runtime one.

## Strategic Approach

### Two-Track Model

The skills registry follows the same two-track model as MCP Registry:

**Track 1 — Upstream (MLflow)**: Registry primitives. Skill and SkillVersion entities, versioning, lifecycle states, tags, aliases, opaque artifact storage. Red Hat submits requirements and user stories to shape this foundation. The upstream proposal is packaging-agnostic — MLflow stores whatever artifact you give it.

**Track 2 — RHOAI (downstream)**: Enterprise governance layer. Approval workflows, certification, trust tiers, verification status, security scanning, catalog integration (Kubeflow Hub), consumption integration (AAA/Studio), packaging intelligence, ingestion pipeline, relationship tracking. This is where Red Hat differentiates.

### Registry vs. Catalog Separation

Consistent with the MCP approach:

- **Registry (MLflow)** = Governance. System of record for identity, versioning, lifecycle, trust. *"Who is this skill, what state is it in, is it approved?"*
- **Catalog (Kubeflow Hub)** = Discovery. Browsing, searching, filtering, trust-tier presentation. *"What skills are available to me?"*

The registry is the source of truth. The catalog reads from it.

### Relationship to MCP Registry

Skills and MCP servers are governed through the same federated registry framework with the same patterns:

| Pattern | MCP Registry | Skills Registry |
|---------|-------------|-----------------|
| Backend | MLflow | MLflow |
| Entity model | MCPServer + MCPServerVersion | Skill + SkillVersion |
| Governance tracks | Lifecycle, Approval, Verification, Certification | Same |
| Payload | Immutable `server_json` | Immutable skill artifact reference |
| Catalog | Kubeflow Hub | Kubeflow Hub |
| Workspace scoping | Yes | Yes |
| Publish state (MVP) | Draft / Published / Deprecated | Draft / Published / Deprecated |

**Key difference**: Skills have no deployment/runtime phase. MCP servers need lifecycle operator deployment, gateway registration, and ConfigMap updates. Skills are consumed as artifacts directly by agents or frameworks. This simplifies the lifecycle but introduces different challenges around packaging and consumption models.

## Jira Tracking

| Ticket | Scope |
|--------|-------|
| RHAIRFE-1712 | Skills Public Registry — discovery surface for externally sourced skills |
| RHAIRFE-1713 | Skills In-Cluster Registry — governed system of record on-cluster |
| RHAIRFE-1370 | AI Asset Registries (parent epic) |

## Component Boundaries

| Component | Responsibility | Reads from Registry | Writes to Registry |
|-----------|---------------|--------------------|--------------------|
| **Skills Registry** (MLflow) | Governed identity, versioning, lifecycle state, metadata | — | — |
| **Skills Catalog** (Kubeflow Hub) | Discovery, browsing, trust-tier presentation | Published skills for surfacing | No |
| **AAA / Studio** | Consumption — resolve and attach skills to agents | Published, scope-filtered skills | No |
| **Ingestion Pipeline** | Validate, scan, evaluate incoming skills | No | Creates draft registry records |

Components that exist for MCP but NOT for skills:
- **Lifecycle Operator**: Skills are not deployed as services
- **MCP Gateway**: Skills do not route through gateway

## Consumption Models

Skills have two distinct consumption paths that the registry must support:

### Client-Side Consumption (Dominant Today)
The agent or framework downloads the skill artifact and uses it directly. The skill code runs in the agent's context.

- **Example**: Agent downloads a SKILL.md file, incorporates instructions, executes scripts locally
- **Registry role**: Resolve the correct version, verify trust/approval status, provide artifact reference
- **Governance strength**: Can enforce "only consume published, approved skills" at resolution time
- **Governance gap**: Once downloaded, execution is outside registry control

### Server-Side Consumption (Emerging)
A server executes the skill on behalf of the agent via an API (e.g., Responses API). The skill runs in a managed environment.

- **Example**: Agent calls a skill endpoint that wraps an MCP server with additional logic
- **Registry role**: Resolve the skill, provide endpoint reference, verify trust status
- **Governance strength**: Server-side execution enables runtime controls, observability, policy enforcement
- **Governance gap**: Requires additional infrastructure beyond the registry

The registry must accommodate both models. The `packaging_type` metadata on SkillVersion distinguishes how a skill is consumed. For 3.5 Dev Preview, client-side consumption is the primary target.

## Trust and Security Model

### Trust Tiers
Mirroring MCP catalog trust tiers:

| Tier | Description | Governance Requirements |
|------|-------------|------------------------|
| **Red Hat** | Red Hat-developed or fully certified skills | Full internal review, testing, security scanning |
| **Partner** | Partner-provided skills with consent and maintenance commitment | Partner attestation, security scanning, periodic review |
| **Community** | Community-contributed skills with basic validation | Basic scanning, community reporting, no SLA |
| **Unverified** | External skills with no validation | Warning, restricted visibility, admin opt-in only |

### Security Considerations Specific to Skills
Skills present different security challenges than MCP servers:

1. **Code execution risk**: Skills may contain scripts that execute in the agent's context. Security scanning must cover code, not just container images.
2. **Prompt injection**: Skill instructions (markdown) can contain prompt injection attacks. Need LLM-aware scanning beyond traditional SAST.
3. **Dependency chains**: Skills may reference other skills, MCP servers, or models — each link in the chain is an attack surface.
4. **Supply chain**: The ClawHub incident demonstrated 12-20% malicious skill rates in open registries. Enterprise registries must scan, verify, and sign all skill artifacts.

### Ingestion Pipeline (Adapted from MCP Pipeline)

```
Discover/Submit → Validate → Scan → Evaluate → Register (Draft) → Govern → Publish
```

| Stage | MCP Pipeline | Skills Pipeline | Key Difference |
|-------|-------------|-----------------|----------------|
| Validate | Repo integrity, provenance | Repo integrity, provenance, format validation | Skills may be single files, not repos |
| Scan | CVE scanning (Quay), container image scanning | Code scanning (SAST), prompt injection detection, dependency scanning | Skills contain code, not containers |
| Evaluate | MCP Checker (functional eval with agents) | Skill evaluation (TBD — no equivalent to MCP Checker yet) | Gap: no standard skill testing framework |
| Register | MLflow MCPServerVersion with `server_json` | MLflow SkillVersion with skill artifact reference | Same pattern |
| Containerize | Podman/Docker or Gen MCP wrapping | **Not applicable** — skills are not containerized | Fundamental difference |

## Relationship Model

### Phase 1 — Loose References (3.5 Dev Preview)
Skills carry tags and metadata that *name* related assets but the registry does not enforce or validate these relationships:

```
Skill "email-assistant" v1.2
  tags: {
    "depends_on_mcp": "email-tools-server",
    "depends_on_model": "text-generation",
    "framework": "claude-code",
    "packaging": "skill-md"
  }
```

This matches MLflow's tag-based model and is sufficient for discovery and human-readable dependency tracking.

### Phase 2 — First-Class Relationships (Future)
The registry supports formal entity associations with version constraints:

```
Skill "email-assistant" v1.2
  dependencies:
    - type: mcp-server
      name: email-tools-server
      version: ">=1.0.0, <2.0.0"
    - type: model
      name: text-generation
      capability: function-calling
    - type: skill
      name: identity-provider
      version: ">=1.0.0"
```

The registry validates that dependencies exist and are in compatible lifecycle states. This requires the `EntityAssociationType` support discussed in the MCP data model proposal (open question #4).

## Roadmap Phasing

### Phase 1 — Skills Registry MVP (3.5 Dev Preview)
**Upstream (MLflow)**:
- Skill + SkillVersion entities
- Versioning (auto-incrementing integers, immutable versions)
- Publish state (Draft / Published / Deprecated)
- Tags and aliases
- Opaque artifact storage (packaging-agnostic)
- Workspace-scoped visibility

**RHOAI**:
- Governance metadata layer (approval, verification, certification status)
- Catalog integration (Kubeflow Hub plugin for skills)
- AAA/Studio integration (resolve published skills for consumption)
- Basic ingestion (register skills with metadata, basic validation)
- Trust tier assignment
- Loose reference relationships via tags

### Phase 2 — Skills Registry Hardening (3.5 GA / 3.6)
- Security scanning integration (code scanning, prompt injection detection)
- Full ingestion pipeline (automated scan, evaluate, register)
- First-class relationship model (entity associations with version constraints)
- Skill evaluation framework (equivalent of MCP Checker for skills)
- Skill packs (grouped skills as a composite asset type)
- Packaging format recommendations and tooling
- Public registry integration (RHAIRFE-1712 — discover and import from external sources)

### Phase 3 — Enterprise Skills Platform (Future)
- Server-side skill consumption support
- Cross-cluster skill distribution and sync
- Partner skill onboarding pipeline (mirroring MCP partner pipeline)
- Automated lifecycle management (health monitoring, deprecation policies)
- Advanced composition and dependency resolution
- Policy-as-code for skill governance (Cedar or equivalent)

## Open Questions

1. **Packaging format**: What should the recommended skill packaging format be? SKILL.md is emerging as de facto but may be insufficient for complex skills. OCI artifacts provide governance but are "heavy" for individual skills. This needs further exploration with stakeholders.

2. **Skill evaluation**: MCP Checker evaluates MCP servers against configurable agents. What is the equivalent for skills? No standard skill testing framework exists.

3. **Databricks prototype alignment**: Matt Prahl has shared Red Hat requirements via Slack. What was shared and does it align with this strategy? Follow up with Matt and Edson.

4. **Skills catalog value**: Adam Bellusci argues catalogs come first with customers. Peter questions the value for skills given the volume and lack of per-use optimization. Needs resolution for 3.5 scoping.

5. **Llama Stack Skills API**: Francisco Arceo is building this. How does it complement or overlap with the MLflow skills registry?

6. **Ann Marie Fred's ODH repo**: Was a tactical starting point proposed (ODH repo for validated skills). Status and potential to build on it?

7. **Skill Packs**: Identified as a future asset type — grouped capabilities. When should this be addressed?

8. **Client-side governance gap**: Once a skill is downloaded and consumed client-side, the registry has no runtime enforcement. How important is this gap for enterprise customers?

## Key People

| Person | Role |
|--------|------|
| **Peter Double** | Principal PM — skills registry ownership |
| **Edson Tirelli** | Agents/Skills lead; Databricks liaison |
| **Matt Prahl** | Engineering; upstream MLflow collaboration |
| **Ann Marie Fred** | Skills packaging research; ODH repo proposal |
| **Adam Bellusci** | Direction — MLflow registries, Kubeflow catalogs |
| **Adel Zaalouk** | Agentic strategy alignment |
| **Hunter Gerlach** | Consulting — field demand for trusted skills |
| **Francisco Arceo** | Llama Stack skills API |
| **Dan Kuc** | MLflow/Registry engineering |
| **Aakanksha Duggal** | Cross-team coordination |

## Source Documents

- [Skills Registry Research — Executive Summary](/features/agent-memory/research/00-executive-summary.md)
- [Skills Ecosystem Research](/features/skills-registry/research/01-skills-ecosystem.md)
- [MLflow Upstream Research](/features/skills-registry/research/02-mlflow-upstream.md)
- [Skill Management Landscape](/features/skills-registry/research/03-skill-management-landscape.md)
- [RHOAI Patterns & Meeting Insights](/features/skills-registry/research/04-rhoai-patterns-and-meetings.md)
- [MCP Registry — 3.5 DP Overview](https://github.com/solaius/ai-asset-registry/blob/main/mcps/mcp-registry-mvp-overview-rewrite.md)
- [MCP Registry — 3.5 DP User Stories](https://github.com/solaius/ai-asset-registry/blob/main/mcps/mcp-registry-3.5-user-stories.md)
