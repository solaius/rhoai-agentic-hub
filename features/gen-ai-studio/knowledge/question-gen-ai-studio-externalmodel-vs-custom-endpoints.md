---
type: question
title: Does ExternalModel CR support make Gen AI Studio's custom-endpoints feature redundant?
description: If the ExternalModel CR satisfies the same use case as Playground's existing custom-endpoints feature, should custom endpoints be deprecated in its favor?
status: open
timestamp: 2026-07-06
tags: [gen-ai-studio, externalmodel, decision-pending]
source: ai-asset-registry/docs/knowledge-review/components/gen-ai-studio-architecture.md §14 (as of 2026-07-05)
---
[RHAISTRAT-2049](https://redhat.atlassian.net/browse/RHAISTRAT-2049) adds ExternalModel CR support to Playground; [RHAISTRAT-2050](https://redhat.atlassian.net/browse/RHAISTRAT-2050) is an explicit, still-open re-evaluation of whether the existing custom-endpoints feature should be deprecated once ExternalModel CR covers the same ground. Both are targeted 3.6, decision pending. See [gen-ai-studio-architecture.md](/features/gen-ai-studio/research/gen-ai-studio-architecture.md) for the surrounding model-serving-integration roadmap context.
