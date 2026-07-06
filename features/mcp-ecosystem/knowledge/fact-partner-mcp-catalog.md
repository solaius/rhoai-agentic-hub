---
type: fact
title: Partner MCP Catalog (3.4 DP — completed)
description: A partner + community MCP server catalog shipped in the RHOAI 3.4 DP catalog for Summit; the business onboarding pipeline, technical bar, and disqualification criteria behind it.
timestamp: 2026-07-06
tags: [mcp-ecosystem, partners, 3.4-dp]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3, §4 (as of 2026-07-05)
---
A curated set of partner and community MCP servers was integrated into the RHOAI 3.4 DP catalog by the April 10 code freeze — 5 partner servers and 2 community servers, the latter positioned in the "periphery" (demos/blogs/Gen AI Studio configmap only, not full catalog treatment).

Quay org `quay.io/rhoai-partner-mcp` hosts the images; upstream metadata repo is `opendatahub-io/model-metadata-collection`. Technical bar for partners: Streamable HTTP only, on-cluster/local hosting only, UBI-based container, ongoing maintenance commitment, and no RHOAI support for partner-server tickets.

**Disqualification criteria**: technical (stdio-only transport, stale/unmaintained assets, remote-only servers for DP) or business (no consent, no maintenance commitment, no "skin in the game").

**Business onboarding pipeline**: (1) curate partner list — invitation-only, strategic categories (CI/CD, databases, hyperscalers, security); (2) BDM outreach with consent letter + value proposition; (3) partner signs consent form (Google Form managed by Katie Giglio — 7 of the partners approached said yes); (4) technical attestation by Ecosystem Engineering (Matt Dorn's team); (5) image build and push to `quay.io/rhoai-partner-mcp`; (6) catalog integration and testing by the RH AI team (Chris Hambridge).

**Post-DP scaling plans**: define a lighter-weight maintenance/support policy (distinct from the operator support model — AI assets age differently); scale the partner pipeline for adding/maintaining MCP servers over time; feature quickstarts with select partners (Dynatrace and Azure/ARO prioritized); deprecate the FY25 web-based catalog (`redhat.com/en/products/ai/openshift-ai/mcp-servers`); rename the UI's "Others" tab to "Community"; use MCP as the template for how other AI asset types (plugins, agents) onboard partners.

Who made the cut and additional partner-specific post-Summit plans (Azure "Agentic Packs," Oracle/CyberArk revisit) live in the restricted counterpart of this entry. See [fact-mcp-catalog-metadata-schema.md](/features/mcp-ecosystem/knowledge/fact-mcp-catalog-metadata-schema.md) for the catalog metadata shape, and [fact-mcp-ingestion-pipeline.md](/features/mcp-ecosystem/knowledge/fact-mcp-ingestion-pipeline.md) for the technical ingestion pipeline this business pipeline runs alongside.
