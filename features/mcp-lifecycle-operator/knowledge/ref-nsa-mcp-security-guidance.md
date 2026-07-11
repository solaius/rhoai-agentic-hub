---
type: reference
title: NSA MCP Security Guidance (June 2026)
description: NSA/CISA cybersecurity information sheet on MCP security -- isolation, egress allowlists, input validation, host shell blocking. Key external reference for MCP server security posture.
resource: https://media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF
tags: [mcp-lifecycle-operator, security, nsa, guidance]
timestamp: 2026-07-11
features: [mcp-ecosystem, mcp-gateway]
source: requirements research 2026-07-11
---

NSA/CISA cybersecurity guidance on MCP server security (published June
2, 2026). Key recommendations:

- Every MCP server should run in an isolated container or microVM
- Egress allowlists to prevent SSRF
- Input validation against well-defined schemas
- Host-level shell execution blocked at container boundary

MCPLO's Restricted PSS defaults (non-root, read-only rootfs, dropped
capabilities, seccomp RuntimeDefault) align with these recommendations.
The NetworkPolicy gap (no source restrictions, no egress restrictions)
is a partial miss against the egress allowlist recommendation.

Cross-cutting: relevant to MCP ecosystem (server building standards),
MCP Gateway (runtime enforcement), and Agent Sandbox (code execution
isolation).
