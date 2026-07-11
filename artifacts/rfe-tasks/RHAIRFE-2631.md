---
rfe_id: RHAIRFE-2631
title: Agent memory available as governed MCP tools
priority: Normal
size: M
status: Submitted
parent_key: null
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory)

## Summary

Agents and MCP-capable harnesses need to use OpenShift AI's memory capability through MCP tool calls, so that any MCP client gets memory without SDK-level integration work, and so that memory is discoverable and governable exactly like the rest of the platform's MCP portfolio.

## Problem Statement

Customers standardizing on MCP as their agent-tool transport cannot reach platform memory from MCP clients today. The pattern is already established in the field: leading harnesses expose memory through MCP servers, and enterprises are adopting MCP-based tool governance. Without an MCP surface, every harness needs bespoke integration, and memory sits outside the MCP governance model (catalog discovery, per-tool authorization, audit) that customers are adopting for everything else.

A further user-facing problem is scoping: the MCP protocol's move to stateless connections means a memory exposed over MCP cannot rely on transport sessions to know whose memory is being read or written. Users need their memory correctly scoped to them regardless of how the connection behaves.

## Affected Customers

- **Garanti BBVA**: evaluating MCP tools for governed access to internal data; memory as a governed MCP tool fits the same evaluation.
- The enterprise cohort driving OpenShift AI's MCP catalog and gateway adoption (multiple named accounts on file with the PM, spanning insurance, banking, and technology): these customers expect new platform capabilities to show up in their MCP-governed estate, not beside it.

## Business Justification

- Aligns the memory investment with the existing MCP Catalog, MCP Gateway, and AI Asset Registry strategy: one discovery, authorization, and audit model for all agent tools, memory included.
- Memory-as-MCP is the emerging cross-harness integration pattern; supporting it means one integration serves every MCP-capable client instead of per-framework work, directly reducing the cost of the framework-agnostic promise in the parent Outcome.
- A governed memory MCP tool strengthens the agentic portfolio story planned for the Summit 2027 timeframe.

## Acceptance Criteria

- [ ] An MCP-capable agent or harness can store, search, and retrieve memories through MCP tool calls with no custom SDK integration.
- [ ] The memory tool surface is discoverable through the platform's MCP catalog/registry surfaces like any other MCP server.
- [ ] Memory operations over MCP are scoped correctly to the calling user, agent, and project even when the underlying MCP connection is stateless.
- [ ] Memory MCP traffic can be governed like any other MCP server on the platform: authorization, usage metrics, and audit through the platform's existing MCP governance capabilities.
- [ ] Tool naming and semantics follow emerging community memory-tool conventions, so third-party MCP clients that already speak "memory tools" work without adaptation.

## Success Criteria

- An off-the-shelf MCP client (no Red Hat specific code) successfully uses platform memory end to end.
- The memory service appears in the platform MCP catalog and passes the same governance checks as other cataloged servers.
