---
title: "Competitive — enterprise MCP catalogs (July 2026)"
description: What changed since the 2026-07-06 landscape snapshot — five new enterprise entrants (AWS, Google, IBM, Salesforce/MuleSoft, Kong), Docker/Databricks/ToolHive moves, structure patterns, and the two-way gap list vs the RHOAI MCP Catalog.
timestamp: 2026-07-09
lens: competitive
review_after: 2026-08-15
---

# Competitive — enterprise MCP catalogs (July 2026)

Research run 2026-07-09 (domain config `redhat-ai.yaml`, narrowed to the
MCP catalog/registry space). Supersedes the 2026-07-06 seven-competitor
snapshot — see the paired knowledge-entry supersede. Verification
verdicts from the adversarial pass noted inline.

## What changed per incumbent (vs the 2026-07-06 table)

| Competitor | Verdict | What changed |
|---|---|---|
| Docker MCP Catalog | **moved fast** | Custom/private catalogs as **signed OCI artifacts** (Cosign, provenance, OPA policy, composable team "profiles", host-anywhere incl. Harbor/Artifactory) [primary-fetched, Dec 2025]; **Docker AI Governance** launched May 2026 — org-wide MCP allow-listing, "unapproved servers are blocked by default" [verified on docker.com; "GA" is press framing, Docker doesn't say it] |
| Databricks | **escalated** | **Unity AI Gateway** (Data+AI Summit, ~2026-06-16, primary-fetched): Unity Catalog governance extended to MCP services/agents/skills; **Contextual Service Policies** (beta) — per-action allow/deny/require-approval based on user/agent/model/request content; managed MCP servers for Drive/Jira/Confluence/Slack/GitHub/SharePoint |
| ToolHive (Stacklok) | **reclassify: coopetition** | **Co-maintained by Red Hat** [verified: stacklok.com AND developers.redhat.com state it; GitHub governance files lag]. Feb 2026: embedded IdP-backed auth server, vMCP circuit breakers, multi-namespace K8s scanning; registry server federates Git/K8s/upstream/internal-API sources into named catalogs with per-catalog JWT visibility + SIEM audit |
| Microsoft Copilot Studio | **date-corrected** | MCP integration GA since **2025-05-29** (not 2026) [verified]; MCP-compliant tools in agent workflows GA **2026-07-15** (six days out); SSE transport still preview per the GA post; "certification still preview" claim unsubstantiated in primary text |
| GitHub MCP Registry | minor | API frozen v0.1; org/enterprise-scoped registry config shipped; 2026 roadmap is auth-centric (3LO/OBO/CIMD) [reported] |
| Official MCP Registry | **scale explosion** | ≥36K total / ≥10K latest server records by live API pull 2026-07-09 [verified — both prior snapshots stale]; still preview/v0.1 |
| Smithery | **demoted** | "Largest" no longer defensible: PulseMCP self-reports **21,564** servers [primary-fetched 2026-07-09], MCP.so ~21K [reported, 403 on fetch], Smithery ~7K [reported, 429 on fetch] |
| MCP.so / PulseMCP | grew | Now ~21K each — PulseMCP is the defensibly largest self-stated directory today (all counts self-reported, unaudited) |

## New entrants the table was missing

| Entrant | What it is | Status/date |
|---|---|---|
| **AWS Agent Registry** (Bedrock AgentCore) | Private governed catalog + discovery across agents/tools/skills/MCP servers; approval workflow, semantic+keyword search, IAM/OAuth/JWT, CloudTrail audit | Preview 2026-04-09 [primary-fetched]; namespace migration 2026-08-06 |
| **Google Cloud API Registry** (Gemini Enterprise Agent Platform / Vertex Agent Builder) | Private curated registry of approved MCP tools; Apigee converts managed APIs to MCP servers | Preview [reported] |
| **IBM watsonx Orchestrate** | Agent Catalog lists MCP servers; **Agentic Control Plane** (June 2026) adds shared catalog + cross-agent governance | Shipping [reported] |
| **Salesforce / MuleSoft** | Hosted MCP Servers GA (~Apr 2026); **Agent Fabric / Agent Registry** — curated catalog of enterprise MCP servers *hosted by their providers* (SaaS-hosted supply model); AgentExchange listings | GA/rolling [reported; MuleSoft blog 403] |
| **Kong MCP Registry** (Konnect) | Extends Konnect API Catalog; links MCP servers to underlying API dependencies; OAuth 2.1 RS alignment in Kong AI Gateway 3.12 | **Still tech preview** as of 2026-07-09 [verified — Kong FAQ declines GA timeline] |

Solo.io competes at the gateway layer (Agent Gateway on Gloo), no
discrete catalog product. No substantive 2026 analyst coverage found
(Gartner doc paywalled; secondhand stats left uncited by policy).

## Structure patterns across the field

1. **Registry = intake/metadata, catalog = curated storefront** is the
   loose convention (Docker's explicit split mirrors RH's) — but naming
   is inconsistent (AWS's "Registry" is a governed catalog; Kong's
   Registry lives inside a Catalog). The hub's three-way
   Directory/Registry/Enterprise-Platform frame remains analytically
   useful but is NOT market vocabulary — and AWS/Databricks/Docker/Kong
   are all converging on the enterprise-platform tier faster than the
   July-6 snapshot assumed.
2. **Curation models**: open/community (official, MCP.so, PulseMCP) ·
   platform-curated (Docker official catalog, RH tiers, IBM) ·
   **enterprise-private** (AWS, Kong, ToolHive, Docker custom catalogs)
   — the private-org-catalog pattern is the fastest-growing and RH's
   "approved enterprise" tier is its analog.
3. **Catalog-as-artifact vs catalog-as-database**: Docker versions the
   catalog itself as a signed OCI artifact (pin/rollback); everyone
   else runs a queryable metadata service.
4. **Trust baseline**: container scanning + signing is table stakes
   (Docker Cosign+SBOM, RH UBI+scan); IdP-backed identity is common
   (ToolHive, AWS, Databricks); content-aware per-action policy
   (Databricks) is the new high-water mark.
5. **Deployment handoff**: only RH (catalog→MCPLO→Gateway→Studio) and
   ToolHive (registry→vMCP runtime) wire catalog directly to a runtime;
   the hyperscalers keep discovery and execution in separate products.
6. **Monetization**: platform add-on subscriptions everywhere; pure
   discovery stays unmonetized community infrastructure.

## Gap list (two-way)

**They-have-we-lack (stated publicly):**
- Composable signed catalog artifacts + team profile remixing (Docker).
- Content-aware per-action policy — block a tool call by request
  content pending approval (Databricks Contextual Service Policies).
- NL/semantic search over a private org catalog + audit-backed approval
  workflow (AWS).
- Spec-aligned OAuth 2.1 Resource Server posture, stated loudly (Kong).
- Multi-source federation into named catalogs with per-catalog JWT
  visibility (ToolHive — RH-co-maintained, running on OpenShift today:
  channel-conflict risk with MCPLO/Catalog needs a stated story).
- SaaS-provider-hosted remote MCP servers as a supply tier
  (Salesforce/MuleSoft) — RH tiers assume deployable images.

**We-have-they-lack:**
- A shipped, single-platform discover→deploy→connect→consume chain.
- Hybrid/multi-cloud, open-source positioning vs single-cloud lock-in
  (AWS/Google/Databricks/Salesforce).
- Full AI-platform bundling (inference, llm-d, NVIDIA) under the same
  subscription as the catalog.

## Bearing on open hub questions

Registry-state → catalog surfacing (open question in mcp-registry):
Databricks' per-action policies and AWS's approval workflow both surface
governance state IN the catalog UX (badges/approval status) — evidence
for "Candidate shows next to Published, clearly labeled" rather than
hiding ungoverned entries. Informs, does not answer.

## Sources

Primary fetches: docker.com custom-catalog + OCI-catalog blogs,
docker.com/products/ai-governance, databricks.com Unity AI Gateway post,
aws.amazon.com Agent Registry what's-new, konghq.com press release +
developer.konghq.com catalog docs, stacklok.com/download,
docs.stacklok.com Feb-2026 updates, github.com/stacklok/* repos,
developers.redhat.com ToolHive article, microsoft.com Copilot Studio MCP
GA post, pulsemcp.com/servers, redhat.com MCP Catalog launch blog,
truefoundry.com registries post, latent.space "Why MCP Won" (2025-03,
background only). Fetch-failed (403/429/binary): blogs.mulesoft.com,
gartner.com doc 7233930, smithery.ai, mcp.so, Stacklok maturity-model
PDF. Reported-only items are labeled inline.
