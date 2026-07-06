---
type: fact
title: Agentic Base Images (RHAIRFE-2443)
description: Proposed shared, Konflux-validated UBI base images for coding-agent harnesses (Claude Code, OpenCode, etc.) — AIPCC scope decision pending.
timestamp: 2026-07-06
tags: [agent-registry, base-images, proposal]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
Problem: AI Engineering teams are each building agent container images independently, with no shared base, conventions, or Red Hat validation (no Konflux/SBOM) — fragmented, licensing-risky, inconsistent. Proposed architecture: a shared UBI 10-minimal base layer (~150-250 MB) plus a per-harness layer (~150-300 MB), distinct from accelerator base images. Initial harness set: Claude Code, OpenCode, Codex, Pi, OpenClaw, Antigravity, Goose. Build pipeline: Konflux with signed SBOM (CycloneDX), multi-arch (x86_64/aarch64), automated CVE patching.

Open licensing concern: proprietary harnesses (Claude Code, Antigravity) need redistribution agreements with Anthropic/Google, or an install-at-runtime fallback. Complementary to (does not require) the OpenShell Agent Runtime Contract. Proposal by Adel Zaalouk; AIPCC ownership/scope decision still pending. See [ref-agentic-base-images-rhairfe-2443.md](/features/agent-registry/knowledge/ref-agentic-base-images-rhairfe-2443.md).
