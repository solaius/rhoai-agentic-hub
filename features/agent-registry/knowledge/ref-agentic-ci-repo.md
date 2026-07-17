---
type: reference
title: opendatahub-io/agentic-ci (GitHub)
description: Agentic CI/CD framework — SDLC workflows and runner images for coding-agent harnesses; publishes daily-rebuilt runner images to quay.io/aipcc/agentic-ci/ — the public tip of the AIPCC base-image pipeline.
resource: https://github.com/opendatahub-io/agentic-ci
tags: [agent-registry, ci-cd, github]
timestamp: 2026-07-16
source: ai-asset-registry/docs/knowledge-registry.md §12 (as of 2026-07-05)
---
SDLC workflows using coding agents (Claude Code, OpenCode, etc. runner images) with e2e tests for agent harnesses. Will be rebased onto [fact-agentic-base-images.md](/features/agent-registry/knowledge/fact-agentic-base-images.md) once those images exist. Routing here (agent-registry) is a judgment call — flag if a dedicated "agent-ops/CI" partition emerges later.

As of 2026-07-16: 53 releases; Claude Code + OpenCode runners; local/Podman/OpenShell backends; daily-rebuilt images published to quay.io/aipcc/agentic-ci/ — the public signal of the AIPCC pipeline behind RHAIRFE-2443 (see [research/07-upstream](/features/agent-registry/research/07-upstream.md)).
