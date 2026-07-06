---
type: fact
title: "MCP security pipeline — SBOM, scanning, attestation, secure execution"
description: The security-scanning and trust pipeline for MCP servers moving through ingestion — SBOM, CVE scanning, provenance, signed attestations, secure execution via ToolHive, and catalog trust vendor extensions.
timestamp: 2026-07-06
tags: [mcp-ecosystem, security, scanning, sbom]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §8 (as of 2026-07-05)
---
- **SBOM generation** for MCP server artifacts.
- **CVE scanning** via Clair, Syft, and Grype.
- **Provenance checks** and **signed attestations**.
- **Stacklok ToolHive** integration for secure MCP server execution (sandboxed/isolated runtime).
- Catalog trust signaled via vendor extension fields: `x-certificationStatus`, `x-securityScan`, `x-maturityLevel`.

Compare the concrete 3.4-era pipeline in [fact-mcp-ingestion-pipeline.md](/features/mcp-ecosystem/knowledge/fact-mcp-ingestion-pipeline.md) (CVE scanning via Quay, Snyk under investigation) and the defined catalog security-indicator fields in [fact-mcp-catalog-metadata-schema.md](/features/mcp-ecosystem/knowledge/fact-mcp-catalog-metadata-schema.md) (`verifiedSource`, `sast`, `secureEndpoint`, `readOnlyTools`) — different tool names and different field names than this entry's. It's unclear from source whether this is an earlier/aspirational architecture pass that the concrete 3.4 pipeline superseded, or a parallel/future-state design the 3.4 pipeline hasn't caught up to yet.
