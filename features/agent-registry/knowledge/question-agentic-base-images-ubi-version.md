---
type: question
title: Agentic base images — which UBI version?
description: UBI 10 is preferred but may hurt supportability on OCP clusters still running RHCOS 9; specific kernel features need minimum versions.
status: open
timestamp: 2026-07-06
tags: [agent-registry, base-images, ubi]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
Raised by Adel Zaalouk / Doug Hellmann against [fact-agentic-base-images.md](/features/agent-registry/knowledge/fact-agentic-base-images.md): UBI 10 (latest) is preferred but may impact supportability on OCP clusters running RHCOS 9. Landlock filesystem, seccomp, and network-namespace features need kernel ≥5.13; Landlock TCP/IPC scoping needs ≥6.12.
