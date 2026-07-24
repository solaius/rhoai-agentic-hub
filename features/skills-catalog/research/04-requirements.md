---
title: "Skills Catalog research -- requirements and 3.6 scope"
description: 3.6 browse-only TP feasible (6-7 sprints to code freeze), RHAISTRAT-1940 existential risk (no PM, empty catalog = negative value), SkillsBench quality evidence (curated +16.2pp, focused 2-3 modules +18.6pp), Red Hat agentic skills as fastest seed content, instructional install UX for MVP, disconnected as design constraint, EU AI Act Article 50 Aug 2 2026, trust tiers as brand promise.
timestamp: 2026-07-23
lens: requirements
review_after: 2026-10-23
---

# Skills Catalog research -- requirements and 3.6 scope

## 1. 3.6 scope feasibility

6-7 two-week sprints to October 23 code freeze fits the low end of the
6-9 sprint estimate. 90% confidence if scope stays at browse +
pre-loaded content (Bill Murdock). Pattern reuse from existing catalogs
reduces greenfield risk.

### Must ship (3.6 TP) vs defer

| Must ship | Can defer (3.7+) |
|---|---|
| Browse/search/filter UI | One-click install to harness |
| Skill detail cards | Automated install commands (npx, APM, LOLA) |
| Pre-loaded Red Hat skills (RHAISTRAT-1940) | Partner feed ingestion |
| Git-backed metadata (YAML source) | Telemetry |
| Trust tier badges | Full-text semantic search |
| ConfigMap disconnected import | Registry integration |
| Category/tag filtering | Quality scores / benchmarks |

## 2. Pre-loaded content (RHAISTRAT-1940)

Empty catalog has negative value. Marketplace cold-start evidence:
"buyers arrive, find nothing, leave permanently." Portal trust: 3% full
trust, 50% doubt accuracy, one stale card triggers permanent bypass
(Port 2025).

SkillsBench: curated skills +16.2pp pass rate; self-generated -1.3pp.
Focused 2-3 modules +18.6pp vs larger bundles +5.9pp. Quality and
focus beat catalog size.

**Minimum viable content (15-20 skills)**:

| Category | Count | Source |
|---|---|---|
| RH Platform Skills (RHEL, OpenShift, Ansible) | 5-8 | redhat.com/skills packs |
| RHOAI/AI Engineering Skills | 3-5 | Internal RHOAI team |
| MCP Server Configurations | 3-5 | rhoai-mcp repo |
| Starter Kit Templates | 3-5 | Existing quickstarts |

**Critical**: RHAISTRAT-1940 has no PM assigned. Single highest risk.
PM assignment by August 2026 is critical.

**Red Hat already has seed content**: redhat.com/skills (Summit 2026
launch), subscription-backed skill packs with live API connections.
Converting these is the fastest path.

## 3. Persona requirements

### AI Engineer
- Discovery UX: search by name, keyword, category, compatible harness
- Card accuracy non-negotiable (stale = permanent bypass)
- Preview before acquisition: SKILL.md content, usage examples
- Clear acquisition path per harness (copy-paste for MVP)
- Time-to-working-skill benchmark: under 5 minutes

### Platform Engineer
- Curation controls: add org-approved skills, hide community
- GitOps compatibility: YAML definitions, ConfigMap import
- Skills-as-Code import without marketplace submission

### Cluster Admin
- Trust tier enforcement: admin-configurable policy on allowed tiers
- Disconnected operation: catalog works without internet
- No runtime fetching: self-contained images
- Admission policy alignment (less critical than for containers)

## 4. Installation UX

For MVP: **instructional, not automated**.
- Copy-paste instructions per harness (proven by Agent Catalog DP)
- Git URL as acquisition primitive
- Harness-specific command suggestions (npx, lola, etc.)

Post-MVP: one-click install, registry integration, APM/LOLA plugin
integration, OCI artifact distribution.

Installation should become a shared service consumed by both catalog
and registry, owned by neither (same pattern as agent deployment).

## 5. Disconnected requirements

| Capability | Requirement | Mechanism |
|---|---|---|
| Browse | Must work offline | YAML baked into image |
| Search/filter | Must work offline | Local index |
| View details | Must work offline (metadata) | YAML; link-out URLs dead |
| Skill content | Should work offline | Bundled into image or PVC |
| Install | Should work offline | Copy from local content |
| Refresh | Offline via signed media | Rebuild image, oc-mirror |

Disconnected is a design constraint, not a feature. Architecture must
assume no runtime network access from day one.

OCI artifacts as future disconnected distribution channel: single
artifact store for images + models + skills with signing, SBOM, and
oc-mirror. Red Hat's strongest technical differentiation.

## 6. Compliance and governance

**EU AI Act Article 50** transparency obligations take effect Aug 2,
2026. Skills generating user-facing outputs trigger disclosure
requirements. Catalog metadata should flag user-interaction scope.

High-risk deadline deferred to Dec 2027 (Annex III, Digital Omnibus).
But traceability (Article 12), risk management (Article 9), and human
oversight (Article 14) requirements are unchanged.

**Trust tier to compliance mapping**:

| Tier | Compliance posture |
|---|---|
| Red Hat-provided | Full provenance, SBOM, errata, signing. Audit-ready. |
| Partner-verified | Partner provenance + RH attestation. Audit-ready with cooperation. |
| Organization-approved | Customer governance. Discovery, not assurance. |
| Community | Use at own risk. Clear labeling required. |

**Security landscape**: 22,511 skills audited = 140,963 issues (~6.3
per skill), 36% prompt injection rate. Scanning and verification are
table stakes.

## 7. Day-zero value

Ship: 15-20 working curated skills, accurate fresh cards, clear
acquisition path, trust tier visibility, disconnected browse.

Do not ship: empty catalog with great search, 1000 unverified community
skills, one-click install with nothing to install.

**Golden-path checklist per skill**:
- SKILL.md follows agentskills.io spec
- Tested with at least one RHOAI-supported model endpoint
- Tested with at least two supported harnesses
- Usage instructions include RHOAI-specific config
- Source repo accessible (or bundled for disconnected)
- Trust tier assigned and visible
- Last-verified date within 90 days

## Key findings

1. 3.6 browse-only TP is feasible if scope is held.
2. RHAISTRAT-1940 is the existential risk (no PM assigned).
3. Quality beats quantity by a measured margin.
4. Installation can be instructional for MVP.
5. Disconnected is a design constraint, not a feature.
6. EU AI Act compliance metadata is urgent.
7. Trust tiers are the catalog's brand promise.
