---
type: question
title: Who owns a discovery convention for BYO agents post-kagenti?
description: kagenti's label convention (kagenti.io/type=agent on plain Deployments) lost its owner — Sandbox-CR discovery only sees sandbox-shaped workloads, so Mode-1/BYO agents are invisible to the registry. Untracked regression.
status: open
timestamp: 2026-07-16
tags: [agent-registry, discovery, byoa]
features: [agent-interop]
---
Candidate answers: a platform label/annotation convention owned by the
BYOA journey (RHAISTRAT-1211, paraphrased), a registration CR
(RHAISTRAT-1955 direction), or self-registration via agent-card
endpoints. See
[research/09-architecture](/features/agent-registry/research/09-architecture.md) §1.6.

**Confirmed 2026-07-16 (jira-gap lens)**: the only tracked vehicle is
1955's registration CR, whose written strategy targets the removed
kagenti operator — and its sibling 1956 just closed. No label-convention
successor is tracked anywhere. Fate question:
[question-agent-registry-1955-fate](/features/agent-registry/knowledge/question-agent-registry-1955-fate.md).
