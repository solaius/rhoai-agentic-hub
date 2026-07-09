---
type: fact
title: Zero-trust for agents
description: The zero-trust principles for agent identity and access from Red Hat's Agentic AI Strategy — agent-native identity, fine-grained dynamic access, token exchange, enterprise IdP integration.
timestamp: 2026-07-06
tags: [agent-ops, zero-trust, security, identity]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §8 (as of 2026-07-05)
---
From Red Hat's Agentic AI Strategy (see [ref-agentic-ai-strategy-2026.md](/narrative/knowledge/ref-agentic-ai-strategy-2026.md)), four zero-trust principles for agents:

- Agents need their own verifiable identities (SPIFFE/SPIRE) — not borrowed service accounts or shared credentials.
- Fine-grained, dynamic access control rather than static role grants.
- On-behalf-of token exchange patterns for agents acting on a user's behalf.
- Integration with enterprise identity providers (Keycloak).

The agent registry's upstream proposal already implements a concrete piece of this: SPIFFE-based `identity`/`trust_domain`/`verified` fields for discovered agents, with the Gateway preferring to route to verified agents — see [fact-agent-registry.md](/features/agent-registry/knowledge/fact-agent-registry.md). This entry captures the broader strategic principle; that entry captures one registry's mechanized implementation of it.
