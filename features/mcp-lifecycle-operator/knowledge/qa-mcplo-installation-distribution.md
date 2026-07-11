---
type: qa
title: "How is the MCP Lifecycle Operator distributed and installed?"
description: Field QA -- MCPLO is bundled with RHOAI operator (not standalone OLM), disconnected via RHOAI offline bundle, updates via RHOAI releases. Upstream available for BYO.
status: answered
timestamp: 2026-07-11
tags: [mcp-lifecycle-operator, distribution, installation]
asks:
  - date: 2026-07-11
    by: pm
    context: FAQ on RHOAI Limited (internal collaborative FAQ)
source: FAQ GDoc 1qZ66JjL99KhV-OF67ArQjT-GNOGiHYCKdLZW9ptqtHQ
---

**Q: How is the MCP Lifecycle Operator distributed and installed?**

The MCP Lifecycle Operator is NOT available in OperatorHub and is NOT
distributed as a standalone OLM operator. It ships bundled within
RHOAI operator releases.

- **Connected clusters:** Updates delivered automatically via RHOAI
  operator updates
- **Disconnected clusters:** Install via the official RHOAI
  offline/disconnected installation bundle
- **Upstream alternative:** The upstream kubernetes-sigs project is
  public and can be used independently by customers who want to
  BYO MCP servers without the downstream RHOAI distribution

The RHOAI operator engineering team receives new MCPLO versions from
the OCP team and bundles them in RHOAI operator releases.
