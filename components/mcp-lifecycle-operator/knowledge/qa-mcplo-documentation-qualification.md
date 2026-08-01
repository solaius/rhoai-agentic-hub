---
type: qa
title: "Where do MCPLO docs live and who qualifies it?"
description: Field QA -- documentation lives in RHOAI docs (not OCP docs); qualification is joint between OCP team (functional) and RHOAI team (deployment/integration).
status: answered
timestamp: 2026-07-11
tags: [mcp-lifecycle-operator, documentation, qualification]
asks:
  - date: 2026-07-11
    by: pm
    context: FAQ on RHOAI Limited (internal collaborative FAQ)
source: FAQ GDoc 1qZ66JjL99KhV-OF67ArQjT-GNOGiHYCKdLZW9ptqtHQ
---

**Q: Where will the official MCPLO documentation live?**

In the RHOAI documentation. Originally discussed as OCP docs with
RHOAI install links, but settled as RHOAI-owned since MCPLO ships
via the RHOAI operator and OCP customers without RHOAI can use the
upstream version.

**Q: Who qualifies the MCP Lifecycle Operator?**

Joint responsibility:
- **OCP team** -- functional qualification (verifying that MCPLO can
  deploy, discover, and manage target MCP servers)
- **RHOAI team** -- deployment and integration qualification (ensuring
  MCPLO rolls out smoothly via the RHOAI operator with all
  prerequisites satisfied)
