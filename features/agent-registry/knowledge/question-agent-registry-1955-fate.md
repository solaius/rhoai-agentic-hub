---
type: question
title: Does RHAISTRAT-1955 get re-baselined onto OpenShell/Sandbox, or follow its closed sibling?
description: The registration-CR lifecycle feature is the only vehicle for BYO/Mode-1 agent discovery, but its strategy is kagenti-shaped and its sibling (1956) just closed — its fate determines where BYO discovery lives.
status: open
timestamp: 2026-07-16
tags: [agent-registry, jira, byoa, discovery]
features: [agent-interop]
---
RHAISTRAT-1955 (agent lifecycle management — single CR to register,
paraphrased) is compatible with the post-kagenti architecture as a fourth
discovery source and the GitOps-native registration path
([research/09-architecture](/features/agent-registry/research/09-architecture.md) §3),
but its written strategy targets the removed kagenti operator, and its
sibling RHAISTRAT-1956 closed between 2026-07-11 and 2026-07-16. Needs an
owner check: re-baseline or close? The answer decides the home for
[question-byo-agent-discovery-labels](/features/agent-registry/knowledge/question-byo-agent-discovery-labels.md).
