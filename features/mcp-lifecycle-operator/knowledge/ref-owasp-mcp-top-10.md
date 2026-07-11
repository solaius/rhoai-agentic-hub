---
type: reference
title: OWASP MCP Top 10 -- first dedicated MCP security framework
description: OWASP's MCP-specific security risks -- Credential Exposure, Privilege Creep, Tool Poisoning, Command Injection, Shadow MCP Servers. Real-world data shows 78.3% attack success rate.
resource: https://owasp.org/www-project-mcp-top-10/
tags: [mcp-lifecycle-operator, security, owasp]
features: [mcp-ecosystem, mcp-gateway]
timestamp: 2026-07-11
source: landscape research 2026-07-11
---

First dedicated OWASP Top 10 for MCP. Key MCP-specific risks:
Credential/Secret Exposure (#1), Privilege Creep, Tool Poisoning,
Command Injection, Inadequate Authentication, Shadow MCP Servers.

Real-world threat data (H1 2026):
- 30+ CVEs filed against MCP infrastructure (Jan-Feb 2026)
- 78.3% attack success rate when 5 MCP servers connected to one
  agent (Palo Alto Unit 42)
- 36.7% of 7,000+ MCP servers potentially SSRF-vulnerable
  (BlueRock Security)

Complemented by OWASP Top 10 for Agentic Applications (2026) and
OWASP Agentic Skills Top 10. Together with the NSA guidance and CSA
analysis, these form the enterprise compliance baseline for MCP
deployment governance.

Cross-cutting: relevant to MCPLO (operator-level enforcement), MCP
Gateway (runtime policy), and MCP ecosystem (server building standards).
