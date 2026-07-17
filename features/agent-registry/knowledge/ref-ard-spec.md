---
type: reference
title: Agentic Resource Discovery (ARD) specification
description: Joint Google+Microsoft federated-discovery spec (v0.9 draft 2026-05-28, announced 2026-06-17; Cisco/Databricks/GitHub/HF/NVIDIA/Salesforce/ServiceNow/Snowflake collaborating) — /.well-known/ai-catalog.json, urn:air URNs, wraps A2A and MCP cards; adoption thin (GitHub Agent Finder first).
resource: https://agenticresourcediscovery.org
timestamp: 2026-07-16
tags: [agent-registry, discovery, federation, standards]
---
Media-type envelope wrapping `a2a-agent-card+json` and
`mcp-server-card+json`; `urn:air:` domain-anchored URNs; trustManifest
(SPIFFE/DIDs); three federation modes. Anthropic and OpenAI absent.
Watch, don't bet — the cheap hedge is URN-mappable IDs + native-media-type
card storage (see
[research/07-upstream](/features/agent-registry/research/07-upstream.md),
[question-agent-registry-ard-endpoint](/features/agent-registry/knowledge/question-agent-registry-ard-endpoint.md)).
