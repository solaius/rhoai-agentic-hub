---
type: question
title: Feast as a pluggable storage backend for Mem0/Zep — engineering effort?
description: Umberto's proposal needs a Feast storage-provider interface for Mem0's write loop — unclear if Mem0 OSS supports pluggable storage, or what a feast init -t agent scaffolding template would cost to build.
status: open
timestamp: 2026-07-06
tags: [agent-memory, feast, mem0]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
[ref-unified-platform-agentic-memory-infrastructure.md](/features/agent-memory/knowledge/ref-unified-platform-agentic-memory-infrastructure.md)'s Phase C (Write loop) needs a Feast storage-provider interface for Mem0 ("Mem0 owns the cognitive logic; Feast owns the data boundary"). Open: does the Mem0 OSS tier actually support pluggable storage backends, or would this require forking/extending Mem0? What's the engineering effort for the `feast init -t agent` scaffolding template?
