---
type: question
title: OLS transition to MCPLO-deployed OCP MCP server
description: Open -- OLS currently uses its own internal OCP MCP server; when MCPLO is productized, OLS will ask users to install via MCPLO. Transition plan and subscription implications unclear.
status: open
timestamp: 2026-07-11
tags: [mcp-lifecycle-operator, ols, lightspeed, transition]
features: [platform]
source: FAQ GDoc 1qZ66JjL99KhV-OF67ArQjT-GNOGiHYCKdLZW9ptqtHQ (OCP MCP Server & OLS section)
---

OpenShift Lightspeed (OLS) currently uses the OCP MCP server
internally. When the MCP Lifecycle Operator is productized, OLS will
remove its internal MCP server and ask users to install the OCP MCP
server via MCPLO.

Open questions:
1. What is the transition timeline?
2. Does this mean all OLS users need RHOAI installed (even if just
   the limited-use entitlement)?
3. What happens to "continued same experience" for existing OLS users?

Calum Murray confirmed OLS currently uses OCP MCP server internally.
Gaurav Singh confirmed the transition plan. Steve Gordon clarified
that OCP customers should not have to think about an RHOAI Limited
SKU for platform-internal applied AI use cases. Joshua Wilson raised
concern about OLS potentially having a cost.
