---
type: question
title: Does Gen AI Studio need a pluggable runtime layer abstracting OGX and AI Gateway?
description: Long-term, will Gen AI Studio need a pluggable layer abstracting OGX (Llama Stack) and AI Gateway, or will they coexist indefinitely as alternative backends?
status: open
timestamp: 2026-07-06
tags: [gen-ai-studio, ogx, ai-gateway, architecture]
source: ai-asset-registry/docs/knowledge-review/components/gen-ai-studio-architecture.md §14 (as of 2026-07-05)
---
Gen AI Studio is currently built on OGX (Red Hat's Llama Stack Distribution) as its AI runtime. [RHAISTRAT-1935](https://redhat.atlassian.net/browse/RHAISTRAT-1935) proposes supporting the AI Gateway (see [fact-ai-gateway.md](/features/platform/knowledge/fact-ai-gateway.md)) as an alternative backend, targeted for 3.7. Open question: does Gen AI Studio eventually need a pluggable runtime abstraction so it can run against either backend transparently, or will OGX and AI Gateway simply coexist as two named, explicitly-chosen options? This connects to the E2E usability finding that users want to "try a model before infra investment" — a lightweight experimentation path may favor whichever backend is faster to stand up. See the fuller architecture context in [gen-ai-studio-architecture.md](/features/gen-ai-studio/research/gen-ai-studio-architecture.md).
