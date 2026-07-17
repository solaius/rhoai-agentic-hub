---
type: reference
title: "RHAISTRAT-2019: Agent Runtime Contract"
description: Formalize the bidirectional interface between the RHOAI agent platform and agent workloads -- AGENTS.md spec, environment injection, service binding, mounted skills. Originally Kagenti-based.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-2019
timestamp: 2026-07-11
tags: [agent-interop, runtime-contract, kagenti]
features: [agent-registry]
source: jira sweep 2026-07-11
---

Formalizes what the platform provides to agents at startup (identity
certs, proxy config, MCP discovery, credentials, skills) and what agents
must expose in return (health probes, A2A agent card). Originally
designed for the kagenti-operator; concept needs reimagining for
OpenShell.
