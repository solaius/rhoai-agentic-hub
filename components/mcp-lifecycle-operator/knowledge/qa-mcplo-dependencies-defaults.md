---
type: qa
title: "Does the MCP Lifecycle Operator have dependencies or deploy servers by default?"
description: Field QA -- MCPLO has no Gateway dependency, deploys no servers by default, supports Day 2 server additions via catalog or CRDs.
status: answered
timestamp: 2026-07-11
tags: [mcp-lifecycle-operator, dependencies, defaults]
asks:
  - date: 2026-07-11
    by: pm
    context: FAQ on RHOAI Limited (internal collaborative FAQ)
source: FAQ GDoc 1qZ66JjL99KhV-OF67ArQjT-GNOGiHYCKdLZW9ptqtHQ
---

**Q: Does the MCP Lifecycle Operator depend on the MCP Gateway?**

No. The lifecycle operator has no installation dependency on the MCP
Gateway. It is installed first (or alongside RHOAI) to manage server
deployment, while the MCP Gateway is downstream for routing traffic
to deployed servers.

**Q: Does it deploy any MCP servers by default?**

No. It does not automatically deploy any MCP servers upon installation.

**Q: Can servers be installed after MCPLO is set up?**

Yes. The operator provides configuration options (catalog UI or CRDs)
for deploying and managing additional MCP servers as Day 2 operations.
During installation, the full MCP catalog is displayed and users select
which servers and tools to install.
