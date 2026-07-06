---
type: fact
title: MCP ingestion pipeline — two lanes + shared components
description: How MCP servers get into the platform — partner ingestion vs. client/customer generation, and the pipeline stages shared by both lanes.
timestamp: 2026-07-06
tags: [mcp-ecosystem, ingestion, gen-mcp]
source: ai-asset-registry/docs/knowledge-registry.md §4 (as of 2026-07-05)
review_after: 2026-08-05
---
Two ingestion lanes get MCP servers into the platform (identified at the 2026-04-10 Gen MCP meeting — see [fact-mcp-pipeline-gen-mcp-transcript.md](/features/mcp-ecosystem/knowledge/fact-mcp-pipeline-gen-mcp-transcript.md)):

**Lane 1 — Partner MCP ingestion** (Partnership Ecosystem Team): partners provide ready-to-go repos. Validate → scan for CVEs → evaluate → containerize (podman/docker for already-production-ready MCPs; [Gen MCP](/features/mcp-ecosystem/knowledge/fact-gen-mcp.md) runtime wraps basic/stdio/unsecured MCPs with auth/TLS/observability) → registry. Goal: manage partner MCPs off-cycle from product releases, with continuous updates and onboarding. 3.4 state: Jose Gonzalez manually adapted partner containers (rebase to UBI, add labels, handle licenses); CVE scanning via Quay; partner dependencies left mostly untouched to avoid breakage.

**Lane 2 — Client/customer MCP generation**: platform engineers build MCPs from existing APIs/repos. API definition (OpenAPI) or HTTP backend → Gen MCP generation → containerization → validation → registry/catalog. A lower-code path for platform engineers; sales/field teams are requesting this as a product capability.

**Shared pipeline components** (reusable across both lanes):
- Validate: repo integrity, provenance, supply-chain checks
- Scan: CVE scanning (Quay), AI-specific scanning (Snyk — under investigation per Ann Murray's recommendation; open research question is what Snyk's AI/agent scanning actually checks beyond standard CVE scanning, and whether it's needed), dependency checking
- Evaluate: [MCP Checker](/features/mcp-ecosystem/knowledge/fact-mcp-checker.md) for functional evaluation with configurable agents
- Containerize: no current standard metadata schema — all 4 partner MCPs in 3.4 had different formats; a gap Red Hat could lead upstream on

Key decisions from the meeting: Gen MCP containerization doesn't fit already-containerized partner MCPs (use podman/docker); Gen MCP's runtime-wrapping *is* useful for partners lacking auth/TLS/observability; evaluations are generic (MCP Checker) and reusable across all lanes including post-catalog customer re-evaluation; MLflow will be the main AI-asset evaluation tool, with MCP-evaluation integration TBD.

See [question-mcp-ingestion-orchestration.md](/features/mcp-ecosystem/knowledge/question-mcp-ingestion-orchestration.md) for the open orchestration-mechanism question.
