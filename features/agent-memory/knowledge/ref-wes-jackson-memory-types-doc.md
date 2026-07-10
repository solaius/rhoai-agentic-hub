---
type: reference
title: Memory types — Wes Jackson (GDoc)
description: Wes's memory-types paper shared in the 2026-06-30 sync — types matter for storage/retrieval decisions, not to the model once content is in context; procedural accumulation should graduate into skills.
resource: https://docs.google.com/document/d/15VlkhjvuMkRJDqAcMa2tRtef4MDeaC7dG8YJiOzceQI
tags: [agent-memory, memory-types, gdoc]
timestamp: 2026-07-10
source: team sync 2026-06-30 (work/transcripts/, local)
---

Companion to Wes's
[platform-concern blog](/features/agent-memory/knowledge/ref-wes-jackson-agent-memory-platform-blog.md):
the taxonomy debate (episodic/procedural/semantic/…) is a developer-side
concern for storage and retrieval decisions — once content is in the
context window the model neither knows nor cares which type it was. The
practical rules that follow: files (Markdown + YAML frontmatter) when
humans must directly read/edit memories, database otherwise;
token-efficiency over metadata ceremony; graduate recurring procedural
memories into skills with stubs instead of pushing full content every
turn.
