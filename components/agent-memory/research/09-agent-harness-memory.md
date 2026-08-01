---
title: Agent Harness Memory Mechanisms
description: Comparative analysis of how major agent harnesses (coding agents, CLI agents) implement memory, identifying portable patterns RHOAI could standardize.
source: ai-asset-registry/agent-memory/research/09-agent-harness-memory.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Harness Memory Mechanisms

**Purpose:** Comparative analysis of how major agent harnesses (coding agents, CLI agents) implement memory — covering architecture, storage, scope, extensibility, MCP integration, and cross-session persistence — to identify portable patterns that RHOAI could standardize.

**Date:** 2026-06-09

**Status:** EXPLORATORY — Phase 2 research. See [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345).

**Series:** Document 09 of 17 — Agent Memory & Knowledge Research
**Phase 1 (completed 2026-05-17):** [00 Executive Summary](00-executive-summary.md) · [01 Landscape & Definitions](01-landscape-and-definitions.md) · [02 Solution Survey](02-solution-survey.md) · [03 MemoryHub Deep-Dive](03-memoryhub-deep-dive.md) · [04 Technical Patterns](04-technical-patterns.md) · [05 Standards & Protocols](05-standards-and-protocols.md) · [06 OGX Memory Primitives](06-ogx-memory-primitives.md) · [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md) · [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md)
**Phase 2 (2026-06-09):** 09 Agent Harness Memory (this doc) · [10 Claude Memory & Dreaming](10-claude-memory-dreaming.md) · [11 Adversarial Memory](11-adversarial-memory.md) · [12 Benchmarking & Evaluation](12-benchmarking-evaluation.md) · [13 KV-Cache Optimization](13-kv-cache-optimization.md) · [14 Enterprise Use Cases](14-enterprise-use-cases.md) · [15 Multi-Modal Memory](15-multi-modal-memory.md) · [16 AI Gateway Memory Substrate](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)

---

## Contents

1. [Why Agent Harnesses Matter for RHOAI](#1-why-agent-harnesses-matter-for-rhoai)
2. [Harness-by-Harness Analysis](#2-harness-by-harness-analysis)
3. [Cross-Harness Comparison Matrix](#3-cross-harness-comparison-matrix)
4. [Architectural Patterns](#4-architectural-patterns)
5. [Memory Scope Models](#5-memory-scope-models)
6. [MCP and Memory Integration](#6-mcp-and-memory-integration)
7. [Consolidation and Decay Mechanisms](#7-consolidation-and-decay-mechanisms)
8. [Multi-Agent and Team Memory](#8-multi-agent-and-team-memory)
9. [Implications for RHOAI](#9-implications-for-rhoai)
10. [Sources](#10-sources)

---

## 1. Why Agent Harnesses Matter for RHOAI

**EXPLORATORY** — The term "agent harness" describes the runtime exoskeleton around a foundation model that adds session management, memory, tool use, trigger mechanisms, and output channels. An agent harness is not the model itself but the orchestration layer that makes a model behave as a persistent, capable agent. Understanding harness memory is critical for RHOAI because these harnesses are the systems enterprises will actually deploy on OpenShift, and their memory mechanisms define the state management requirements that RHOAI must support.

The agent harness landscape consolidated rapidly between late 2025 and mid-2026. Five harnesses now dominate the developer-facing agent market by distinct measures: OpenClaw by adoption volume (~347K GitHub stars by April 2026), Claude Code by developer workflow penetration, Codex CLI by enterprise backing (~74K stars, 3M weekly active users), Hermes by open-source innovation velocity (~64K stars), and Gemini CLI by ecosystem breadth (free tier with 1M token context). Each has independently arrived at a memory architecture, and the convergences and divergences between them reveal what the industry considers settled versus experimental.

For RHOAI, the central question is: which memory patterns are portable across harnesses, and which are vendor-locked? The answer determines what RHOAI should standardize at the platform level (storage, governance, scope) versus what it should leave to the harness (personality, consolidation heuristics, prompt injection format).

This document covers the five harnesses in depth, extracts seven recurring architectural patterns, and maps them to RHOAI's platform capabilities. It builds on the pattern families cataloged in [04 Technical Patterns](04-technical-patterns.md) and the scope model defined in [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md).

---

## 2. Harness-by-Harness Analysis

### 2.1 OpenClaw (Red Hat / Open Source)

**REFERENCE** — OpenClaw is an open-source personal AI agent released February 28, 2026, with ~347K GitHub stars by April 2026. Red Hat's Emerging Technologies team has published detailed work on deploying OpenClaw agents on Red Hat AI and integrating agent memory capabilities.

#### Memory Architecture

OpenClaw's memory architecture is fundamentally filesystem-native. The agent's entire identity and memory state lives in plain-text Markdown files inside a workspace folder (typically `~/clawd/`). When OpenClaw starts a session, it reads these files and assembles the agent's identity, behavior rules, memory, and task schedule dynamically. As Red Hat's deployment guide puts it: "The files are the agent."

The workspace uses up to eight optional files, each serving a distinct memory function:

| File | Memory Function | Persistence | Mutability |
|---|---|---|---|
| `SOUL.md` | Personality, values, boundaries — "the agent's constitution" | Permanent | Human-authored only |
| `AGENTS.md` | Behavioral rules, SOPs, workflows | Permanent | Human-authored |
| `IDENTITY.md` | Name, presentation, avatar | Permanent | Human-authored |
| `USER.md` | User context — preferences, habits, goals | Permanent | Agent-updatable |
| `MEMORY.md` | Long-term factual memory | Permanent | Agent-updatable |
| `TOOLS.md` | Capabilities and available tools | Permanent | Human-authored |
| `HEARTBEAT.md` | Scheduled tasks (read every 30 minutes) | Permanent | Human/agent |
| Daily logs (`memory/YYYY-MM-DD.md`) | Session-level working memory | Temporal | Agent-authored |

The SOUL.md file is architecturally distinctive. It is injected into the system prompt first — before any other context — and defines who the agent is rather than what it does. Best practice guidance recommends 300-600 words: long enough to be specific, short enough to avoid dominating the context window. This separation of identity from instruction is unique among the five harnesses and reflects OpenClaw's origin as a personal assistant (not a coding tool).

#### Storage Mechanism

All storage is local filesystem Markdown. No database, no vector store, no external service required for base functionality. This makes OpenClaw the most portable of the five harnesses — an agent can be copied to a new server by copying a directory. Version control with Git is natural and encouraged.

For enhanced memory beyond the built-in files, the ecosystem offers several integration paths. Red Hat's Emerging Technologies team demonstrated integration with Mem0 for automatic extraction and semantic recall. The community also developed a "memory-wiki" pattern — pre-compiled Markdown memory inspired by Karpathy's LLM Wiki pattern, which reports ~90% session-token reduction versus cold exploration.

#### Scope Model

OpenClaw uses cascade resolution for scope: Global -> Agent -> Workspace -> Default. The most specific definition wins. This four-tier cascade parallels but does not exactly match the scope models of the other harnesses. Notably, OpenClaw's scope model includes an "agent" level that the others lack — reflecting its support for multiple agent personalities within a single installation.

#### MCP Integration

OpenClaw supports MCP natively through the `openclaw mcp` CLI, with full stdio and HTTP/SSE transport support. Memory-specific MCP integration includes a built-in memory MCP server, the community-developed MemoClaw MCP (semantic memory with wallet-based identity), and an OpenClaw MCP server that exposes MEMORY.md search and assistant capabilities over Streamable HTTP. Per-agent MCP routing allows different agents to access different tool sets via `agents.<name>.mcpServers` in `openclaw.json`.

#### Cross-Session Persistence

The base OpenClaw memory (MEMORY.md and daily logs) persists across sessions by default, but the agent must choose to update MEMORY.md — there is no automatic extraction pipeline in the base system. Red Hat's analysis notes that the built-in memory "focus[es] heavily on remembering who you are, your preferences, and its own personality rather than specific task details." This is a significant gap for enterprise use cases where task-specific memory matters more than personality continuity.

#### Red Hat AI / Kagenti Connection

**EXPLORATORY** — Red Hat AI's "Bring Your Own Agent" blueprint uses OpenClaw as its reference agent, adding SPIFFE identity, MCP Gateway authorization, Kata Containers isolation, and MLflow tracing without touching agent code. The Kagenti ADK extends this with agent auto-discovery via A2A-based AgentCard CRDs. For memory specifically, Kagenti's runtime services include PostgreSQL for agent state and conversation history, and pgvector for embeddings and similarity search — providing the database-backed memory tier that base OpenClaw lacks. This architecture positions Kagenti as the enterprise memory layer beneath OpenClaw's filesystem-native memory layer, a pattern we identify as "layered override" in Section 4.

---

### 2.2 Hermes (NousResearch)

**REFERENCE** — Hermes Agent is NousResearch's open-source autonomous AI agent, released February 2026, with ~64K GitHub stars and 242+ contributors by April 2026 (v0.9.0). Hermes bills itself as "the agent that grows with you" — a self-improving system that persists memory, skills, and session history across restarts.

#### Memory Architecture

Hermes has the most architecturally layered memory system of the five harnesses, with four distinct persistence tiers plus a pluggable external provider system:

**Built-in Memory (always active):**
- `USER.md` — User preferences, habits, goals. Agent-curated with periodic nudges.
- `MEMORY.md` — Long-term project and factual memory.
- SQLite session database — Full-text search (FTS5) over conversation history with LLM summarization for cross-session recall.
- Honcho dialectic user modeling — Structured user modeling with semantic analysis.

**External Memory Providers (pluggable, one active at a time, additive to built-in):**
Hermes v0.7.0 introduced pluggable memory backends. Eight providers are shipped: Honcho, OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, and Supermemory. When active, the external provider automatically injects context into the system prompt, prefetches relevant memories before each turn (non-blocking), syncs conversation turns after each response, extracts memories on session end, and mirrors built-in memory writes.

The Honcho provider deserves special attention for its architectural sophistication. Rather than simple vector retrieval, Honcho uses dialectic reasoning — analyzing conversations after they conclude to derive structured conclusions about user preferences, habits, and goals. It implements a two-layer context injection system (base layer with session summary plus dialectic supplement with LLM reasoning) and models conversations as peer exchanges with independent identity representations per AI peer.

The Holographic provider (HRR — Holographic Reduced Representations) is architecturally novel: memories are stored as superposed complex-valued vectors, and recall is algebraic rather than similarity-based. This requires zero additional dependencies and represents a fundamentally different approach to memory retrieval from the dominant vector-similarity paradigm.

#### Storage Mechanism

The base system uses SQLite for session history and FTS5 search, plus Markdown files (MEMORY.md, USER.md) for curated long-term memory. The SQLite choice is intentional — it provides full-text search and transactional safety without requiring a separate database server.

However, the Git-Native Memory Engine proposal (GitHub issue #25571) represents the most architecturally ambitious memory rethinking in any current harness. Filed as "a philosophical conjecture, not a technical blueprint," it argues that Git itself is the most mature distributed memory system available. A v1 prototype has been running in production on the Tachikoma fork since mid-May 2026, with reported results:

- Immutable audit trail: "deleted" memory entries remain traceable via `git log`. The causal chain is never lost.
- Write performance: Git commit + diff outperforms SQLite FTS5 by orders of magnitude in write-heavy sessions.
- Atomic diffs: changes to individual facts show as single-line +/- entries, not full-record rewrites.
- Branch merging: when no cognitive conflict exists between branches, fast-forward merge is safe and correct.
- Session resilience: strategy shifted from timed sync to session-end merge, with no data loss across 7+ sessions.

The identified gap in the Git-native approach is episodic memory: Git log stores the causal chain chronologically, but there is no mechanism to inject "what happened last session" into the next session's context window. The proposed v2 fix is `~/.hermes/gnm/last-session/` — an auto-generated episodic dump written at session end and injected at session start, structured as narrative ("we were discussing X, on the topic of Y, with pending decision Z") rather than a fact list.

#### Scope Model

Hermes uses a simpler scope model than OpenClaw: per-user home directory (`~/.hermes/`) for global state, per-profile for agent-specific state. The multi-peer model in Honcho adds a user-peer/AI-peer scope distinction within each profile, where the user peer is global across profiles but each AI peer maintains its own independent representation.

#### MCP Integration

Hermes is bidirectional with MCP — it operates as both client and server. As a client, it connects to external MCP servers (configured in `~/.hermes/config.yaml`) and discovers tools at startup. As a server (since v0.6.0), it exposes conversation history, session search, and attachment management to external MCP clients like Claude Desktop and Cursor. The MCP server reads conversation data directly from Hermes's session store.

Hermes applies MCP tool filtering by default: rather than exposing every tool from every server, it encourages scoping to the tools the agent actually needs via `include`/`exclude` lists. This reduces token usage and prevents LLM confusion from too many options.

Dynamic tool discovery is supported: MCP servers can notify Hermes when their available tools change at runtime via `notifications/tools/list_changed`, triggering an automatic re-fetch and registry update.

#### Cross-Session Persistence

Hermes persists memory, skills, and session history in SQLite across restarts by default. The recommended practice is to treat profile memory (USER.md and MEMORY.md) as "high-signal infrastructure" — concise, durable, preference-focused rather than raw note dumps.

#### Plur and the Open Engram Format

**EXPLORATORY** — Plur (by plur-ai, currently beta) introduces an open engram format using YAML for portable, shared memory artifacts. This is architecturally significant because it proposes a standardized interchange format for agent memory — engrams that can be shared between different agent harnesses, not just different instances of Hermes. If the engram format gains adoption, it could become the memory equivalent of what AGENTS.md is for instructions. RHOAI should monitor this closely as a potential standardization target.

---

### 2.3 Claude Code (Anthropic)

**REFERENCE** — Claude Code is Anthropic's official CLI for Claude, providing a terminal-based coding agent with the most sophisticated multi-layer memory architecture of the five harnesses. As of mid-2026, it is the primary reference implementation for Anthropic's managed agents platform.

#### Memory Architecture

Claude Code implements a four-layer memory system, all stored as local Markdown files:

**Layer 1: CLAUDE.md (Manual/Static Context)**
CLAUDE.md files provide persistent project instructions. They operate at three scope levels:
- Project-level (`CLAUDE.md` in repo root) — team-shared conventions, checked into version control
- Local (`.claude/CLAUDE.md`) — personal preferences, not checked in
- User-global (`~/.claude/CLAUDE.md`) — cross-project personal configuration

CLAUDE.md files are loaded at session start and included in every prompt. Unlike AGENTS.md (which is a cross-tool convention), CLAUDE.md is Claude Code-specific but can reference AGENTS.md files in the same repository.

**Layer 2: Auto Memory (Automatic Notes)**
Auto Memory (introduced in Claude Code v2.1.59) lets Claude accumulate knowledge across sessions without user intervention. Each project gets its own memory directory at `~/.claude/projects/<project>/memory/`, with a main MEMORY.md index file and topic-specific detail files.

The agent decides what is worth remembering based on whether the information would be useful in a future conversation. It does not save something every session — the selection is opinionated and curated. High-value signals include: explicit user corrections ("no, not that"), explicit save requests ("remember that..."), recurring themes across 3+ sessions, and architectural decisions.

**Layer 3: Session Memory (Volatile)**
Conversation-level continuity within a single session. Does not persist after the session closes. This is the standard ephemeral working memory that all harnesses implement.

**Layer 4: Auto Dream (Consolidation)**
Auto Dream is architecturally unique among the five harnesses — it is a dedicated consolidation process that reviews, strengthens, removes, and reorganizes memory, analogous to REM sleep. It follows a four-phase process:

1. **Inventory:** Read the memory directory, open MEMORY.md, scan topic files, build a map of current state.
2. **Transcript Search:** Scan recent session transcripts for high-value patterns — corrections, save requests, recurring themes, architectural decisions.
3. **Consolidation:** Merge new information into existing topic files. Convert relative dates to absolute dates. Delete contradicted facts. Remove stale memories about deleted files. Merge overlapping entries.
4. **Prune and Index:** Keep MEMORY.md under 200 lines. Remove pointers to non-existent files. Add links to newly important memories. Resolve contradictions between index and file contents.

Auto Dream triggers only when both conditions are met: sufficient sessions (not just one long session over two days) and sufficient elapsed time (not ten quick sessions in two hours). This dual-gate prevents unnecessary consolidation on light-use projects while ensuring active projects get regular cleanup.

Performance: one observed case consolidated memory from 913 sessions in roughly 8-9 minutes.

Safety: During dream cycles, Claude can only write to memory files — no code changes, no tool execution outside the memory directory.

**Layer 5: Managed Agents Memory (API-level, May 2026)**
The Managed Agents API (requiring the `managed-agents-2026-04-01` beta header) adds a fifth layer: workspace-scoped memory stores. A memory store is mounted as a directory inside the agent's sandbox. The agent reads and writes it with the same file tools used for the rest of the filesystem. Every change creates an immutable memory version, providing an audit trail and point-in-time recovery.

#### Storage Mechanism

All memory is file-based Markdown. No vector database, no external service. This is a deliberate architectural choice — fully inspectable, editable, and version-controllable by humans. The 200-line cap on MEMORY.md is a practical constraint: that is the cutoff for what loads at session startup without search-by-meaning capability.

#### Scope Model

Claude Code has the most granular scope model of the five harnesses:
- User-global (`~/.claude/CLAUDE.md`)
- Project-repo (`CLAUDE.md` in repo root, version-controlled)
- Project-local (`.claude/CLAUDE.md`, gitignored)
- Project auto-memory (`~/.claude/projects/<project>/memory/`)
- Subagent-scoped (per-subagent memory directory, isolated)

#### Subagent Memory and Isolation

**REFERENCE** — Claude Code subagents are specialized instances with their own context window, system prompt, tool list, and permissions. Subagent memory is opt-in via the `memory` frontmatter field, and each subagent's memory directory is siloed from every other subagent's. The orchestrator receives only the final message — whatever the subagent learned (file locations, architectural patterns, dead ends, user decisions) vanishes when it returns.

Worktree isolation (`isolation: "worktree"`) gives each subagent its own git worktree on its own branch. As of mid-2026, teams run 4-8 concurrent worktrees per developer reliably. However, known issues exist: worktree branch name collisions from `agentId` prefix reuse can cause cross-scope file leakage, and subagents in background sessions have been observed bypassing worktree-isolation guards.

The cross-subagent memory sharing problem remains unsolved. The code-reviewer subagent does not see what the security-auditor subagent learned, and vice versa. This is an active area of development with no shipped solution as of June 2026.

#### MCP Integration

Claude Code uses MCP extensively for tool integration but does not currently expose a memory-specific MCP interface. Memory is managed internally via the file-based system. MCP servers are configured per-project or per-subagent, and subagents can have scoped MCP server configurations independent of the parent session.

#### Cross-Session Persistence

Auto Memory and Auto Dream provide strong cross-session persistence. The key limitation is the 200-line index cap on MEMORY.md, which constrains what is immediately available at session start. The agent is instructed to search topic files for detail beyond the summary, but this requires an active search step during the session.

---

### 2.4 Codex CLI (OpenAI)

**REFERENCE** — Codex CLI is OpenAI's open-source, terminal-first coding agent, rewritten from TypeScript to Rust in 2026. With ~74K GitHub stars, 14.5M monthly npm downloads, and 3M weekly active users as of April 2026, it is the most widely adopted coding agent by active user count. The unified "App Server" architecture powers the CLI, VS Code extension, web app, macOS desktop app, and third-party IDE integrations.

#### Memory Architecture

Codex CLI implements a two-layer memory architecture with a sophisticated asynchronous consolidation pipeline:

**Layer 1: AGENTS.md (Static Instruction Layer)**
AGENTS.md is the cross-tool instruction convention that Codex, Cursor, Aider, Jules, Gemini CLI, GitHub Copilot, and 20+ other platforms have adopted. Now governed by the Linux Foundation's Agentic AI Foundation (AAIF), AGENTS.md has been adopted by over 60,000 open-source projects.

AGENTS.md explains a project to agents the way README.md explains it to humans: build commands, test commands, code style, architectural constraints. The format is deliberately minimal — plain Markdown with no required schema, no YAML frontmatter, no special syntax. Hierarchy follows proximity: the closest AGENTS.md to the edited file takes precedence; explicit user prompts override everything.

There is a 32 KiB ceiling on AGENTS.md with silent truncation past the cap. Monorepos with deep nested instruction files can hit this limit without awareness.

**Layer 2: Memories Pipeline (`~/.codex/memories/`)**
The Memories system is a multi-phase asynchronous pipeline that extracts, consolidates, and injects persistent knowledge from past sessions:

*Phase 1 — Per-Rollout Extraction:*
After each session goes idle for 6+ hours, a small extraction model (gpt-5.4-mini) reads the entire rollout transcript and emits a structured `raw_memory` artifact. The extraction uses a strict-schema prompt and includes secret redaction before anything hits disk.

*Phase 2 — Global Consolidation:*
A heavier consolidation model (gpt-5.4) runs as a sandboxed sub-agent inside the memory folder with bash and Read/Write/Edit tools. It edits the canonical `MEMORY.md` handbook and a `skills/` tree. The consolidation uses diff labels: **added** (in current selection but not in prior baseline), **retained** (matches prior snapshot exactly), and **removed** (was in prior baseline but no longer in current top-N).

The on-disk layout is Markdown:

```
~/.codex/memory/
  memory_summary.md     -- Navigational summary injected into prompts
  MEMORY.md             -- Searchable registry of aggregated insights
  raw_memories.md       -- Temporary merge of Phase 1 outputs
  rollout_summaries/
    <thread_id>-<ts>-<slug>.md
  skills/
    <name>/SKILL.md     -- Reusable procedures and scripts
```

At session start, `memory_summary.md` is injected into the model's developer instructions, truncated to 5,000 tokens. The agent is then instructed to grep over `MEMORY.md` when it needs more detail than the summary covers.

#### Storage Mechanism

All storage is local filesystem Markdown, mirroring the pattern seen in Claude Code and OpenClaw. The usage tracking system is distinctive: the agent cites specific files and line ranges using `<oai-mem-citation>` blocks. Each citation increments `usage_count` and updates `last_usage` in a tracking database, and this usage data feeds the selection ranking for the next consolidation pass (`usage_count DESC -> last_usage DESC -> source_updated_at DESC`). Frequently cited memories rise; neglected ones age out. This is the only harness with explicit citation-driven memory decay.

#### Scope Model

Codex CLI has the simplest scope model of the five harnesses:
- User-global (`~/.codex/memories/`) for generated memory
- Project-local (AGENTS.md hierarchy) for static instructions
- No team-level or organization-level scope

There is no cross-machine sync. A second laptop, server, or fresh container starts with no memory. There is no team sharing — memories are per-user with no mechanism to pool across teammates.

#### Sandbox Architecture

Codex CLI's sandbox model is the most security-hardened of the five harnesses. Kernel-level sandboxing uses macOS Seatbelt, Linux Bubblewrap, and Windows restricted tokens with filesystem ACLs. The sandbox disables network access during command execution by default and scopes file operations to the current directory tree.

The memory consolidation sub-agent runs inside the same sandbox model — it has bash and file tools but only within the memory directory. This is architecturally similar to Claude Code's dream cycle safety constraint.

#### MCP Integration

Codex CLI supports MCP for tool integration. Memory itself is not exposed via MCP — it is managed by the internal pipeline. The multi-agent collaboration tools (spawn_agent, send_input, resume_agent, wait_agent, close_agent) support up to 6 concurrent agent threads by default, but memory is not shared across spawned agents.

#### Cross-Session Persistence

Memories must be explicitly enabled in `~/.codex/config.toml` (`generate_memories = true`, `use_memories = true`). The consolidation pipeline is the most configurable of any harness, with tunable parameters for minimum idle hours (1-48), max rollout age (0-90 days), max rollouts per startup (up to 128), max raw memories for consolidation (up to 4096), and max unused days before expiry (0-365).

A critical constraint: the agent cannot directly update memories. When a user says "remember that I prefer X," the agent cannot persist it immediately. The user must wait for the async Phase 1/2 pipeline or manually edit memory files. This contrasts sharply with Claude Code's Auto Memory, which can write memories during an active session.

#### Regional Limitations

At launch, Memories is not available in the EEA, UK, or Switzerland. Users in those regions get the AGENTS.md layer only. This is a significant constraint for enterprise deployments with European operations.

---

### 2.5 Gemini CLI (Google)

**REFERENCE** — Gemini CLI is Google's open-source AI agent for terminal use, using a ReAct (reason-and-act) loop with built-in tools and MCP server support. It offers a free tier with 60 requests/min, 1,000 requests/day, and access to Gemini 3 models with 1M token context windows.

#### Memory Architecture

Gemini CLI v0.40.0 (April 28, 2026) introduced a complete rebuild of the memory architecture, transitioning from a legacy `save_memory` tool to a four-tier prompt-driven system:

**Tier 1: Global Memory (`~/.gemini/GEMINI.md`)**
Rules that apply across every project. Written by the user, loaded at every session start.

**Tier 2: Project Memory (`./GEMINI.md`)**
Team-shared conventions, architecture rules, and workflows. Committed to the repository. Content from more specific files supplements or overrides content from more general files.

**Tier 3: Subdirectory Memory (`./src/GEMINI.md`, etc.)**
Component-specific instructions discovered dynamically. When a tool accesses a file or directory, the CLI automatically scans for GEMINI.md files in that directory and its ancestors up to a trusted root. This on-demand discovery means the agent only loads component-specific memory when it actually enters that part of the codebase.

**Tier 4: Auto-Extracted Skills and Memory Patches**
The Auto Memory system (experimental, off by default) uses a background extraction agent to analyze past session transcripts. It drafts skill SKILL.md files and memory patches, placing them in a review inbox for user approval before they become active.

Gemini CLI also supports modular context via the `@file.md` import syntax within GEMINI.md files, allowing large instruction sets to be decomposed into manageable, imported components. This is unique among the five harnesses.

#### Storage Mechanism

All memory is Markdown files on the local filesystem. The v0.40.0 rewrite replaced the `save_memory` tool with direct Markdown file editing by the agent, making memory changes fully transparent and inspectable. An adaptive token calculator (v0.43.0) provides more accurate content size estimation for managing what fits in context.

#### Scope Model

Gemini CLI's scope model is the most dynamic of the five harnesses due to its on-demand directory scanning:
- User-global (`~/.gemini/GEMINI.md`)
- Project-root (`./GEMINI.md`)
- Subdirectory (any `GEMINI.md` in the path from current file to trusted root)
- Dynamically discovered (scanned when tools access new directories)

The `/memory` commands provide runtime scope management:
- `/memory show` — display concatenated current memory
- `/memory reload` — force re-scan of all GEMINI.md files
- `/memory add <text>` — append to global memory on the fly
- `/memory inbox` — review auto-extracted skills and memory patches (v0.39.0+)

#### Auto Memory and Skill Extraction

**EXPLORATORY** — Gemini CLI's Auto Memory system is architecturally distinctive in its focus on skill extraction rather than fact memorization. The background extraction agent reviews sessions with 10+ messages that have been idle for 3+ hours, looking for repeated procedural workflows, common failure modes, and project-specific conventions. It drafts these as SKILL.md files.

Safety boundaries are significant:
- Auto Memory cannot directly edit active memory files, settings, credentials, or project GEMINI.md files.
- Skill update patches are parsed and dry-run validated before surfacing.
- Memory patches are target-allowlisted and applied atomically only on user approval.
- The extraction agent is instructed to redact secrets, tokens, and credentials.
- Auto Memory does not extract from the current session — only sessions idle for 3+ hours.

Inbox items are stored per-project. Skills extracted in one workspace are not visible from another until promoted to the user-scope skills directory. This project isolation is a deliberate design choice.

#### MCP Integration

Gemini CLI has the most comprehensive MCP implementation of the five harnesses, with full support for MCP servers (tool discovery, execution, and resources), three transport mechanisms (Stdio, SSE, Streamable HTTP), dynamic tool schema validation, and conflict resolution when multiple servers expose tools with the same name. MCP resource support was finalized in v0.40.0.

Memory is not exposed via MCP — it is managed by the internal GEMINI.md file system and Auto Memory pipeline. However, community-built MCP extensions exist that add persistent memory across sessions and projects using MCP tools for search and memory addition.

#### Cross-Session Persistence

GEMINI.md files persist across sessions by default. Auto Memory is opt-in and experimental. The inbox review workflow ensures users maintain control over what becomes persistent memory — nothing is auto-applied.

An experimental Task Tracker (v0.40.0) adds an internal persistent graph of tasks for monitoring progress on complex objectives, hinting at a future where Gemini CLI tracks not just what the agent knows but what it is working toward.

---

## 3. Cross-Harness Comparison Matrix

### 3.1 Memory Layer Comparison

| Capability | OpenClaw | Hermes | Claude Code | Codex CLI | Gemini CLI |
|---|---|---|---|---|---|
| **Static instruction file** | SOUL.md + AGENTS.md | USER.md + MEMORY.md | CLAUDE.md | AGENTS.md | GEMINI.md |
| **Cross-tool standard** | AGENTS.md (AAIF) | -- | -- (Claude-specific) | AGENTS.md (AAIF, originator) | AGENTS.md (AAIF) |
| **Auto memory extraction** | No (base); Yes (Mem0) | Yes (built-in + providers) | Yes (Auto Memory) | Yes (async pipeline) | Yes (experimental) |
| **Consolidation / dream** | No | No (proposed in Git-native) | Yes (Auto Dream, 4-phase) | Yes (2-phase pipeline) | No (inbox review) |
| **Memory decay** | No | No | Yes (dream prune) | Yes (citation-driven) | No |
| **User approval gate** | N/A | Provider-dependent | No (auto-applied) | No (async, agent-managed) | Yes (inbox) |
| **Identity layer** | SOUL.md (personality) | -- | -- | -- | -- |
| **Scheduled autonomy** | HEARTBEAT.md (30-min) | -- | -- | -- | -- |

### 3.2 Storage and Infrastructure

| Capability | OpenClaw | Hermes | Claude Code | Codex CLI | Gemini CLI |
|---|---|---|---|---|---|
| **Primary storage** | Filesystem (Markdown) | SQLite + Filesystem | Filesystem (Markdown) | Filesystem (Markdown) | Filesystem (Markdown) |
| **Vector store** | Optional (Mem0, etc.) | Optional (providers) | No | No | No |
| **Database** | No (base); PostgreSQL (Kagenti) | SQLite (built-in) | No | No | No |
| **Index size cap** | No hard cap | No hard cap | 200 lines (MEMORY.md) | 5,000 tokens (summary) | No hard cap |
| **Git-native storage** | No | Proposed (Tachikoma fork) | No | No | No |
| **Cross-machine sync** | Copy directory | No built-in | No built-in | No | No |
| **Team sharing** | No | No (base); Plur engrams | No | No | No |

### 3.3 MCP and Extensibility

| Capability | OpenClaw | Hermes | Claude Code | Codex CLI | Gemini CLI |
|---|---|---|---|---|---|
| **MCP client** | Yes (stdio + HTTP/SSE) | Yes (stdio + HTTP + OAuth) | Yes | Yes | Yes (stdio + SSE + HTTP) |
| **MCP server** | Yes (Streamable HTTP) | Yes (since v0.6.0) | No (internal only) | Yes | No |
| **Memory via MCP** | Yes (MemoClaw, memory server) | Yes (providers as bridge) | No | No | No (community only) |
| **Pluggable memory backend** | Yes (MCP servers) | Yes (8 providers shipped) | No | No | No |
| **Dynamic tool discovery** | Yes | Yes (notifications) | Yes | Yes | Yes |
| **Multi-agent memory** | No | Multi-peer (Honcho) | Subagent (siloed) | Spawn agent (6 threads) | No |

### 3.4 Enterprise Readiness

| Capability | OpenClaw | Hermes | Claude Code | Codex CLI | Gemini CLI |
|---|---|---|---|---|---|
| **Kernel sandbox** | No (base); Kata (RHOAI) | No | No | Yes (Seatbelt/bwrap/Win) | No |
| **Secret redaction** | No (base) | Provider-dependent | No (dream restricted) | Yes (Phase 1 pipeline) | Yes (Auto Memory) |
| **Audit trail** | Git (manual) | Git (proposed); SQLite | Immutable versions (API) | Usage tracking DB | No |
| **Regional restrictions** | None | None | None | EEA/UK/CH (memories only) | None |
| **Enterprise identity** | SPIFFE (Kagenti) | No | No | No | Google account |

---

## 4. Architectural Patterns

Seven recurring architectural patterns emerge from the cross-harness analysis. Each represents a distinct philosophy about where agent memory should live, who controls it, and how it evolves.

### Pattern 1: Harness-as-Memory-Store

**REFERENCE** — The harness itself manages the full memory lifecycle — extraction, storage, retrieval, consolidation, and injection. No external memory service is required.

**Who implements it:** Claude Code (Auto Memory + Auto Dream), Codex CLI (Memories pipeline), Gemini CLI (Auto Memory + inbox).

**Architecture:** The harness runs background processes (dream cycles, consolidation agents, extraction models) that transform raw session transcripts into curated memory artifacts. Memory is stored locally and injected into prompts at session start.

**Strengths:** Zero-dependency deployment. Memory format is under the harness vendor's control. Consolidation quality can leverage the vendor's strongest models (Claude Code uses Opus 4.7 for dreaming; Codex CLI uses gpt-5.4 for consolidation).

**Weaknesses:** Vendor lock-in of memory format. No portability between harnesses. No team sharing without manual export. When the harness is the memory store, migrating to a different harness means losing all accumulated memory or building a custom migration tool.

**RHOAI implication:** This is the dominant pattern today and the one RHOAI must integrate with rather than compete against. The platform should provide the storage substrate (pgvector, PostgreSQL) that harnesses can optionally use, but should not try to replace the harness's internal memory management.

### Pattern 2: Filesystem-Native Memory

**REFERENCE** — All memory is stored as plain-text files (overwhelmingly Markdown) on the local filesystem. No database, no service, no daemon.

**Who implements it:** All five harnesses use this as their primary storage mechanism.

**Architecture:** Memory files follow a known directory convention (`~/.<harness>/`, workspace-local, or both). The harness reads these files at session start and injects their content into prompts. Files are human-readable, human-editable, and version-controllable with Git.

**Strengths:** Universal portability — copy a directory to transfer an agent. Full human auditability — open a file, read the memory. Git-native versioning for free. Zero infrastructure requirements.

**Weaknesses:** No semantic search (except through LLM re-reading). Linear scanning does not scale beyond a few hundred kilobytes. No concurrent-write safety beyond filesystem locking. No access control beyond filesystem permissions.

**RHOAI implication:** This is the lowest common denominator that every harness supports. RHOAI should ensure that its storage primitives (PVCs, ConfigMaps, Secrets) can efficiently serve filesystem-native memory patterns. The 200-line / 5,000-token / 32-KiB caps seen across harnesses suggest that the "hot" memory layer is small — typically under 100KB — and fits comfortably in ConfigMap-sized storage.

### Pattern 3: Layered Override

**REFERENCE** — Memory context is loaded from multiple scope levels, with more specific levels overriding or supplementing more general ones.

**Who implements it:** All five harnesses, with varying numbers of layers.

**Architecture:** A hierarchy of memory files is loaded in order from broadest (user-global) to narrowest (subdirectory-specific). Claude Code has 5 layers; Gemini CLI has 4 with dynamic discovery; OpenClaw has 4 with cascade resolution; Codex CLI has 2 (static + generated); Hermes has 3+ with external providers.

**Strengths:** Separation of concerns — team conventions, project rules, personal preferences, and component-specific knowledge each have a natural home. Changes at one level do not require editing every other level.

**Weaknesses:** Debugging "why did the agent do that?" requires understanding which layers were loaded and in what order. Conflicting instructions across layers may produce unpredictable behavior. No harness currently provides tooling to visualize the resolved, merged memory state (Gemini CLI's `/memory show` is the closest).

**RHOAI implication:** The layered override pattern maps naturally to Kubernetes namespace hierarchy and RBAC. RHOAI could define standard scope tiers — cluster, namespace, workload, session — and provide a mechanism for memory at each tier to override or supplement the tier above. This is the pattern most directly aligned with existing OpenShift architecture.

### Pattern 4: Memory-as-MCP

**EXPLORATORY** — Memory is exposed as an MCP server, making it accessible to any MCP-compatible client regardless of the harness being used.

**Who implements it:** OpenClaw (MemoClaw MCP, built-in memory server), Hermes (MCP server mode exposing session data). Partial: community extensions for Gemini CLI.

**Architecture:** A dedicated MCP server wraps the memory store and exposes search, retrieval, and storage tools via the MCP protocol. Any MCP client — whether it is the same harness, a different harness, or an IDE — can read and write to the shared memory.

**Strengths:** Harness-agnostic memory access. A team could use Claude Code, Codex CLI, and Gemini CLI, all accessing the same memory store via MCP. Decouples memory from the harness lifecycle.

**Weaknesses:** Immature — no standard schema for MCP memory tools. Each implementation defines its own tool signatures. Performance overhead of MCP protocol for high-frequency memory reads.

**RHOAI implication:** This is the most strategically interesting pattern for RHOAI. If memory-as-MCP matures, RHOAI could provide a managed MCP memory server (backed by PostgreSQL + pgvector) that any harness deployed on the platform can connect to. This would give RHOAI a differentiated value proposition: "deploy any harness, get enterprise memory for free." The MCP Gateway (Kuadrant) already handles MCP server routing and authorization — adding memory as a managed MCP service is architecturally natural.

### Pattern 5: Team Memory

**EXPLORATORY** — Memory is shared across multiple users or agents, enabling collective learning and institutional knowledge.

**Who implements it:** No harness ships team memory natively. Partial implementations exist: Hermes (Plur engrams for portable shared artifacts), Hermes (Honcho multi-peer model for shared workspace), SoulClaw (swarm memory synchronization).

**Architecture:** In theory, team memory requires a shared storage backend (database or shared filesystem), access control (who can read/write what), conflict resolution (when two agents learn contradictory things), and a merge strategy (how individual memories consolidate into team knowledge).

**Strengths:** Institutional memory that survives individual user turnover. Collective learning — one agent's discovery becomes available to all. Consistent behavior across team members using different agents.

**Weaknesses:** No production-ready implementation exists. The conflict resolution problem (what happens when Agent A learns "use PostgreSQL" and Agent B learns "use MySQL"?) is unsolved. Privacy concerns — should one team member's personal memory be visible to others?

**RHOAI implication:** Team memory is the clear next frontier. RHOAI's multi-tenant architecture (namespaces, RBAC, NetworkPolicy) provides the access control primitives that team memory requires. The platform could offer a team memory tier that sits between personal agent memory and organizational policy, scoped to a namespace and governed by RBAC. This would be a genuinely novel capability that no harness provides today.

### Pattern 6: Dream Consolidation

**REFERENCE** — A dedicated background process periodically reviews accumulated memory, removes contradictions, merges duplicates, converts temporal references, and produces a clean consolidated state.

**Who implements it:** Claude Code (Auto Dream, 4-phase process), Codex CLI (Phase 2 consolidation with gpt-5.4 sub-agent).

**Architecture:** The consolidation process runs asynchronously (triggered by session count + elapsed time for Claude Code; triggered by idle time for Codex CLI). It operates with restricted permissions — write access only to memory files, no code changes, no external tool execution. It uses a stronger/larger model than the extraction phase.

**Strengths:** Memory quality improves over time rather than degrading. Contradictions are resolved rather than accumulated. The 200-line / 5,000-token caps remain manageable because the consolidation process actively manages size.

**Weaknesses:** Consolidation is computationally expensive (8-9 minutes for 913 sessions in Claude Code). The consolidation model's decisions are opaque — it may delete memories the user would have wanted to keep. No rollback mechanism if consolidation makes bad choices (Claude Code's Managed Agents API adds immutable versions for this; Codex CLI does not).

**RHOAI implication:** Dream consolidation requires compute resources (model inference) that RHOAI already manages via model serving. The platform could offer a "memory consolidation job" primitive — a scheduled Kubernetes Job that runs a consolidation model against accumulated memory. This would decouple consolidation from the harness, allowing any harness to benefit from platform-managed memory maintenance.

### Pattern 7: Git-Native Memory

**EXPLORATORY** — Git itself serves as the memory storage engine, using commits for temporal ordering, branches for memory isolation, diffs for atomic fact changes, and merge for memory reconciliation.

**Who implements it:** Hermes (Tachikoma fork prototype, mid-May 2026). Proposed but not shipped.

**Architecture:** Each memory update is a Git commit. Memory diffs show individual fact changes as single-line additions/removals. "Deleted" memories remain in `git log` — the causal chain is never lost. Branch merging handles multi-session reconciliation when no cognitive conflict exists.

**Strengths:** Immutable audit trail surpassing any database-backed approach. Distributed by design — Git's replication model is the most battle-tested distributed system in software. Write performance reportedly outperforms SQLite FTS5 in write-heavy sessions. Diff format is natural for atomic fact representation.

**Weaknesses:** No semantic search capability. Episodic memory (injecting "what happened last session" into the next session) requires additional tooling beyond Git. Branch merge conflicts map poorly to cognitive conflicts — how does `git merge` handle "I learned that PostgreSQL is best" versus "I learned that MySQL is best"?

**RHOAI implication:** Git-native memory is compelling for environments where Git is already the primary collaboration tool — which describes most enterprise development teams. RHOAI already manages Git-aware workloads (pipelines, source-to-image). If the Hermes Git-native pattern proves viable, RHOAI could provide a managed Git memory backend as an alternative to database-backed memory.

---

## 5. Memory Scope Models

### 5.1 Scope Tier Comparison

All five harnesses implement some form of hierarchical memory scope, but they differ in granularity and dynamism:

```
User/Global ──> Project ──> Component ──> Session ──> Turn
  (broadest)                                         (narrowest)
```

| Scope Tier | OpenClaw | Hermes | Claude Code | Codex CLI | Gemini CLI |
|---|---|---|---|---|---|
| **User-global** | `~/clawd/` config | `~/.hermes/` config | `~/.claude/CLAUDE.md` | `~/.codex/config.toml` | `~/.gemini/GEMINI.md` |
| **Agent/Profile** | Per-agent workspace | Per-profile | -- | -- | -- |
| **Project** | Workspace files | `~/.hermes/projects/` | `CLAUDE.md` (repo root) | `AGENTS.md` (repo root) | `GEMINI.md` (repo root) |
| **Component/Subdir** | -- | -- | -- | `AGENTS.md` (nested) | `GEMINI.md` (nested, dynamic) |
| **Session** | Daily log files | SQLite session DB | Session memory (volatile) | Rollout transcript | Session context |
| **Turn** | In-context | In-context | In-context | In-context | In-context |
| **Subagent** | -- | -- | Per-subagent memory dir | Per-spawn (no shared) | -- |

### 5.2 Dynamic vs. Static Scope Discovery

A key architectural divergence is how harnesses discover what memory to load:

**Static discovery** (OpenClaw, Claude Code, Codex CLI): Memory files are loaded from known paths at session start. The set of loaded files does not change during the session unless explicitly reloaded.

**Dynamic discovery** (Gemini CLI): When a tool accesses a file or directory, the CLI scans for GEMINI.md files in that directory and its ancestors. This means the agent's effective memory grows as it explores the codebase. This is architecturally significant because it means the agent's context changes based on which part of the codebase it is working in, without any manual configuration.

**Hybrid** (Hermes): Built-in memory is statically loaded, but external memory providers can dynamically prefetch relevant memories before each turn based on conversation context.

### 5.3 Mapping to RHOAI Scope Tiers

The scope models across all five harnesses map to a four-tier model that aligns with Kubernetes/OpenShift architecture (building on the scope model from [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md)):

| RHOAI Scope Tier | Kubernetes Primitive | Harness Equivalent |
|---|---|---|
| **Organization** | Cluster-scoped ConfigMap | User-global config across all harnesses |
| **Team** | Namespace-scoped ConfigMap | No harness equivalent (gap) |
| **Workload** | Pod-mounted PVC/ConfigMap | Project-level memory files |
| **Session** | Ephemeral storage / emptyDir | Session memory across all harnesses |

The "Team" tier is the most significant gap. No harness provides native team-scoped memory. This is where RHOAI has the clearest opportunity to add value.

---

## 6. MCP and Memory Integration

### 6.1 Current State of Memory-as-MCP

**EXPLORATORY** — The integration between MCP and memory is nascent. While all five harnesses support MCP for tool integration, only OpenClaw and Hermes expose memory through MCP interfaces, and these implementations use non-standardized tool schemas.

The current landscape:

| Harness | MCP Memory Pattern | Implementation |
|---|---|---|
| OpenClaw | Memory search/get via MCP tools | MemoClaw MCP server, OpenClaw MCP server (MEMORY.md search) |
| Hermes | Session data via MCP server | Built-in MCP server exposing conversation history and session search |
| Claude Code | None | Memory is internal only; MCP used for other tools |
| Codex CLI | None | Memory pipeline is internal |
| Gemini CLI | Community only | Third-party MCP extensions (Supermemory integration) |

### 6.2 The AAIF Convergence Opportunity

The Linux Foundation's Agentic AI Foundation (AAIF) now governs both AGENTS.md (static instructions) and MCP (tool protocol). This creates a natural convergence opportunity: defining a standard MCP memory tool schema that any harness can implement, analogous to how AGENTS.md standardized static instructions.

A hypothetical MCP memory standard would need to define:
- **Tool signatures:** `memory_search(query, scope, limit)`, `memory_write(key, content, scope, ttl)`, `memory_delete(key, scope)`
- **Scope model:** How MCP memory maps to user/project/team/session scopes
- **Content format:** Whether memories are plain text, structured YAML (Plur engrams), or JSON
- **Access control:** How MCP memory tools interact with authentication and authorization
- **Lifecycle:** TTL, consolidation triggers, decay semantics

No such standard exists today. RHOAI could contribute to its definition through participation in AAIF, which aligns with Red Hat's existing involvement in the Linux Foundation.

### 6.3 MCP Gateway as Memory Router

**PROPOSED** — The MCP Gateway (Kuadrant/mcp-gateway) already handles MCP server routing and authorization. Extending it to route memory-specific MCP requests to a platform-managed memory backend would require:

1. A standardized MCP memory tool schema (see 6.2)
2. A memory backend service (PostgreSQL + pgvector, consistent with Kagenti's existing architecture)
3. Gateway routing rules that map memory scope tiers to backend partitions
4. RBAC integration for memory access control

This would allow any harness deployed on RHOAI to access platform-managed memory by connecting to the MCP Gateway's memory endpoint, with the Gateway handling authentication, authorization, routing, and auditing.

---

## 7. Consolidation and Decay Mechanisms

### 7.1 Comparative Consolidation Approaches

Only two of the five harnesses implement automated consolidation, but their approaches differ significantly:

**Claude Code (Auto Dream):**
- **Trigger:** Dual-gate — sufficient sessions AND sufficient elapsed time
- **Process:** 4-phase (inventory -> transcript search -> consolidation -> prune)
- **Model:** Opus 4.7 / Sonnet 4.6
- **Safety:** Write access restricted to memory files only
- **Output:** Cleaned topic files + pruned 200-line MEMORY.md index
- **Decay:** Dream prune removes stale/contradicted memories
- **Audit:** Managed Agents API creates immutable memory versions

**Codex CLI (Memories Pipeline):**
- **Trigger:** Session idle for 6+ hours
- **Process:** 2-phase (per-rollout extraction -> global consolidation)
- **Model:** gpt-5.4-mini (extraction) + gpt-5.4 (consolidation)
- **Safety:** Consolidation sub-agent runs in sandboxed environment
- **Output:** `memory_summary.md` + `MEMORY.md` + `skills/` tree
- **Decay:** Citation-driven — `usage_count DESC -> last_usage DESC -> source_updated_at DESC`
- **Audit:** Usage tracking database with citation blocks

**Gemini CLI (Manual Inbox):**
- **Trigger:** Sessions with 10+ messages, idle for 3+ hours
- **Process:** Background extraction -> inbox -> user review -> apply
- **Model:** Configured model for extraction
- **Safety:** Cannot edit active memory; patches validated before surfacing
- **Output:** SKILL.md files and memory patches
- **Decay:** None (user manages manually)
- **Audit:** Inbox provides review trail

### 7.2 The Citation-Driven Decay Innovation

Codex CLI's citation-driven decay mechanism deserves attention as a novel approach. Rather than time-based decay (memories expire after N days of disuse) or consolidation-based pruning (a model decides what to remove), Codex CLI tracks actual usage via `<oai-mem-citation>` blocks. Each time the agent cites a memory, its usage count increments and its last-usage timestamp updates. The next consolidation pass ranks memories by `usage_count DESC -> last_usage DESC -> source_updated_at DESC`, naturally promoting frequently-used memories and demoting unused ones.

This is architecturally analogous to LRU caching — the most recently and frequently used memories survive longest. Unlike time-based TTLs, this approach means a rarely-accessed but critically important memory (e.g., a security policy) stays alive as long as the agent occasionally references it. The risk is that important but unreferenced memories can silently age out.

### 7.3 Consolidation Resource Requirements

Consolidation is not free. Claude Code's Auto Dream processed 913 sessions in ~8-9 minutes. Codex CLI's Phase 2 consolidation runs a gpt-5.4 model as a sub-agent. For RHOAI, this means memory consolidation should be modeled as a scheduled Kubernetes Job with defined resource requests, not as an incidental background process within an agent pod. The compute cost is proportional to accumulated session volume, which in enterprise deployments could be significant.

---

## 8. Multi-Agent and Team Memory

### 8.1 The Shared Memory Problem

The most significant architectural gap across all five harnesses is multi-agent memory sharing. When multiple agents (or multiple instances of the same agent) work on related tasks, each accumulates knowledge independently. No harness provides a production-ready mechanism for agents to share what they learn.

Claude Code's subagent architecture illustrates the problem most clearly: the code-reviewer subagent does not see what the security-auditor subagent learned. Whatever a subagent discovers — files found, patterns recognized, dead ends hit, decisions made — vanishes when it returns its final message to the orchestrator. The orchestrator gets the conclusion but not the reasoning path.

Codex CLI's multi-agent collaboration tools (spawn_agent, send_input, resume_agent, wait_agent, close_agent) support up to 6 concurrent threads, but memory is not shared across spawned agents.

### 8.2 Partial Solutions

Three partial approaches exist in the ecosystem:

**Hermes Honcho Multi-Peer Model:** Honcho models conversations as peers exchanging messages — one user peer plus one AI peer per profile, sharing a workspace. The workspace is the shared environment where the user peer is global across profiles and each AI peer maintains an independent representation. This does not solve agent-to-agent sharing, but it does solve the user-identity-across-agents problem.

**SoulClaw Swarm Memory Synchronization:** The SoulClaw fork of OpenClaw adds "native swarm memory synchronization" for multi-agent coordination. This is the most explicit attempt at shared agent memory, though documentation on the synchronization protocol is limited.

**Plur Open Engram Format:** Plur's YAML-based engram format is designed for portable, shared memory artifacts across agents and harnesses. If adopted, it could serve as the interchange format for multi-agent memory sharing. However, Plur is currently in beta and not widely adopted.

### 8.3 The Team Memory Opportunity for RHOAI

**PROPOSED** — RHOAI is uniquely positioned to solve team memory because it already has the infrastructure primitives:

| Team Memory Requirement | RHOAI Primitive |
|---|---|
| Shared storage | PostgreSQL + pgvector (Kagenti architecture) |
| Access control | Kubernetes RBAC + namespace isolation |
| Identity | SPIFFE/SPIRE (Kagenti) for agent identity |
| Conflict resolution | No existing primitive (requires new design) |
| Merge strategy | No existing primitive (requires new design) |
| Audit trail | PostgreSQL transaction log + MCP Gateway audit |

The two missing primitives — conflict resolution and merge strategy — are the research challenges. When Agent A learns "always use `pytest` for testing" and Agent B learns "this project uses `jest`," the platform needs a policy for how to reconcile the contradiction. Options include:
- Scope isolation (Agent A's memory stays in its namespace, Agent B's in its own — no merge needed)
- Latest-write-wins (simple but lossy)
- Human arbitration (an inbox mechanism, similar to Gemini CLI's Auto Memory inbox)
- Model-based arbitration (a consolidation model resolves conflicts, similar to Claude Code's dream cycle)

---

## 9. Implications for RHOAI

### 9.1 What Is Settled: Patterns RHOAI Can Standardize

The cross-harness analysis reveals several patterns that have converged sufficiently to standardize:

**Filesystem-native memory is universal.** Every harness stores memory as Markdown files. RHOAI should ensure its storage primitives (PVCs, ConfigMaps) efficiently serve this pattern. Memory volumes should be small (under 1MB for hot memory), fast (SSD-backed for session start), and inspectable (mountable by debug pods for troubleshooting).

**Layered override is universal.** Every harness loads memory from multiple scope tiers with narrower scopes overriding broader ones. RHOAI should define a standard scope hierarchy that maps to Kubernetes primitives: cluster -> namespace -> workload -> session.

**Static instruction files are converging.** AGENTS.md (AAIF/Linux Foundation) is the emerging cross-tool standard, adopted by OpenClaw, Codex CLI, Gemini CLI, and 60,000+ projects. RHOAI should support AGENTS.md as a first-class configuration surface, delivered via ConfigMap or Git-sourced volume.

**Memory consolidation requires scheduled compute.** Both Claude Code and Codex CLI run model-based consolidation as background processes. RHOAI should model this as a Kubernetes CronJob or Job with defined resource requests, not as an incidental process within an agent pod.

### 9.2 What Is Emerging: Patterns RHOAI Should Prepare For

**Memory-as-MCP** is the most strategically interesting emerging pattern. If the AAIF standardizes MCP memory tool schemas, RHOAI's MCP Gateway could serve as the memory access layer for all deployed harnesses. The platform investment would be: a managed memory backend (PostgreSQL + pgvector, already in Kagenti architecture) plus Gateway routing rules for memory endpoints.

**Team memory** is the clearest unmet need across all harnesses. RHOAI's multi-tenant architecture provides the access control primitives, but the conflict resolution and merge strategy problems require new design work.

**Open engram format** (Plur) is early but worth monitoring. A standardized memory interchange format would enable memory portability across harnesses — a significant enterprise value proposition.

### 9.3 What Is Experimental: Patterns RHOAI Should Monitor

**Git-native memory** (Hermes/Tachikoma) is philosophically compelling but unproven at scale. The audit trail properties are attractive for regulated industries. RHOAI should track whether the Hermes community adopts the pattern broadly.

**Dream consolidation** is powerful but expensive and opaque. The models that run consolidation can make mistakes (deleting important memories, misresolving contradictions), and there is no rollback mechanism in most implementations. RHOAI should ensure that any platform-managed consolidation creates immutable snapshots before each consolidation pass.

**Citation-driven decay** (Codex CLI) is an elegant solution to the memory TTL problem, but its effectiveness depends on the agent consistently citing memories, which is a behavioral property that cannot be guaranteed. RHOAI should consider offering both time-based and usage-based decay policies as configurable options.

### 9.4 What RHOAI Should Not Do

**Do not try to replace harness-internal memory management.** Every harness has its own memory extraction, consolidation, and injection pipeline. These are core competitive features with deep model-specific tuning. RHOAI should provide the storage substrate and governance layer, not the memory logic.

**Do not assume a single harness.** The enterprise landscape will be multi-harness. A single organization may use Claude Code for development, OpenClaw for operations, and custom Hermes agents for domain-specific tasks. RHOAI's memory architecture must be harness-agnostic.

**Do not conflate memory with model weights.** Memory (session knowledge, user preferences, project context) is fundamentally different from model fine-tuning. The registry/catalog distinction from the broader AI Asset Registry proposal applies here: memory is runtime state (governance concern), not a trained artifact (catalog concern).

### 9.5 Recommended Platform Capabilities

Based on this analysis, RHOAI should consider the following platform capabilities for the agent memory workstream:

1. **Memory Volume Primitive** — A PVC-backed storage class optimized for small-file, high-frequency-read Markdown workloads. Agents mount it at session start, write during sessions, and the platform handles backup, snapshot, and cross-node availability.

2. **Managed Memory MCP Server** — A platform-provided MCP server (backed by PostgreSQL + pgvector) that any harness can connect to via the MCP Gateway. Provides search, write, and lifecycle management tools via standardized MCP tool schemas.

3. **Memory Scope RBAC** — Kubernetes RBAC rules that map to memory scope tiers. A cluster admin can define organization-wide memory policies (e.g., "all agents must include security guidelines"), namespace admins can define team memory, and workload owners can manage agent-specific memory.

4. **Consolidation Job Scheduler** — A CronJob template that runs model-based memory consolidation against accumulated session transcripts. The consolidation model, schedule, and retention policy are configurable. Each consolidation run creates an immutable snapshot before modifying memory state.

5. **Memory Audit API** — An API endpoint that returns the full provenance of any memory: when it was created, from which session, which consolidation pass modified it, and its current usage metrics. This addresses compliance requirements in regulated industries.

---

## 10. Sources

| Source | Used for |
|---|---|
| [Deploying agents with Red Hat AI: The curious case of OpenClaw (Red Hat Developer)](https://developers.redhat.com/articles/2026/04/14/deploying-agents-red-hat-ai-openclaw) | OpenClaw deployment architecture on Red Hat AI |
| [Operationalizing BYOA on Red Hat AI, OpenClaw edition (Red Hat Blog)](https://www.redhat.com/en/blog/operationalizing-bring-your-own-agent-red-hat-ai-openclaw-edition) | Red Hat AI BYOA blueprint, SPIFFE, MCP Gateway integration |
| [From Context to Dreams: Architecting Memory for AI Agents (Red Hat Emerging Technologies)](https://next.redhat.com/2026/06/01/from-context-to-dreams-architecting-memory-for-ai-agents/) | Agent memory architecture, OpenClaw + Mem0 integration |
| [How Kagenti ADK simplifies production AI agent management (Red Hat Developer)](https://developers.redhat.com/articles/2026/05/04/how-kagenti-adk-simplifies-production-ai-agent-management) | Kagenti runtime services, A2A protocol, PostgreSQL/pgvector |
| [Kagenti project site](https://kagenti.github.io/.github/) | Kagenti ADK overview, agent discovery, runtime architecture |
| [OpenClaw Workspace Files Explained (Medium)](https://capodieci.medium.com/ai-agents-003-openclaw-workspace-files-explained-soul-md-agents-md-heartbeat-md-and-more-5bdfbee4827a) | SOUL.md, AGENTS.md, HEARTBEAT.md, USER.md, MEMORY.md file architecture |
| [OpenClaw MCP documentation](https://docs.openclaw.ai/cli/mcp) | OpenClaw MCP integration, per-agent routing |
| [SoulClaw — 4-tier memory and swarm sync (GitHub)](https://github.com/clawsouls/soulclaw) | SoulClaw memory tiers (T0-T3), swarm memory synchronization |
| [NousResearch/hermes-agent (GitHub)](https://github.com/nousresearch/hermes-agent) | Hermes Agent architecture, memory system, pluggable providers |
| [Hermes Agent Memory Providers (official docs)](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers) | External memory providers: Honcho, Plur, Holographic, ByteRover, etc. |
| [Git-Native Memory Engine proposal (Hermes Issue #25571)](https://github.com/NousResearch/hermes-agent/issues/25571) | Git-native memory architecture, Tachikoma fork prototype results |
| [Hermes Agent MCP integration (official docs)](https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes) | Hermes bidirectional MCP, tool filtering, OAuth support |
| [How Claude remembers your project (Claude Code Docs)](https://code.claude.com/docs/en/memory) | Claude Code 4-layer memory architecture |
| [Claude Code Memory System Explained (Milvus Blog)](https://milvus.io/blog/claude-code-memory-memsearch.md) | Auto Memory caps, search limitations |
| [Claude Code Dreams: Auto-Dream Feature (claudefa.st)](https://claudefa.st/blog/guide/mechanics/auto-dream) | Auto Dream 4-phase process, trigger conditions, safety |
| [Auto Memory and Auto Dream (antoniocortes.com)](https://antoniocortes.com/en/2026/03/30/auto-memory-and-auto-dream-how-claude-code-learns-and-consolidates-its-memory/) | Dream consolidation mechanics, date conversion, pruning |
| [Using agent memory (Claude API Docs)](https://platform.claude.com/docs/en/managed-agents/memory) | Managed Agents memory stores, immutable versions, audit trail |
| [Claude Code subagent memory isolation (Hindsight blog)](https://hindsight.vectorize.io/blog/2026/05/06/claude-code-subagents-shared-memory) | Cross-subagent memory sharing problem, worktree isolation |
| [Create custom subagents (Claude Code Docs)](https://code.claude.com/docs/en/sub-agents) | Subagent frontmatter, memory field, isolation modes |
| [Worktree isolation bug (GitHub Issue #51596)](https://github.com/anthropics/claude-code/issues/51596) | Worktree branch collision, cross-scope leakage |
| [Codex CLI Memories (OpenAI Developer Docs)](https://developers.openai.com/codex/memories) | Memories pipeline, Phase 1/Phase 2, on-disk layout |
| [Codex CLI Memory: How It Works + What Mem0 Adds (Mem0 Blog)](https://mem0.ai/blog/how-memory-works-in-codex-cli) | Two-layer architecture, AGENTS.md + Memories pipeline |
| [Memory Lifecycle Management in Codex CLI](https://codex.danielvaughan.com/2026/04/15/memory-lifecycle-management-codex-cli/) | Consolidation lifecycle, citation-driven decay, usage tracking |
| [Codex CLI Memories: Persistent Context (Codex Knowledge Base)](https://codex.danielvaughan.com/2026/05/01/codex-cli-memories-persistent-context-session-memory-ecosystem/) | Memory pipeline configuration, regional limitations, best practices |
| [AGENTS.md custom instructions (OpenAI Developer Docs)](https://developers.openai.com/codex/guides/agents-md) | AGENTS.md format, hierarchy, 32 KiB cap |
| [OpenAI Codex CLI Architecture (Zylos Research)](https://zylos.ai/research/2026-03-26-openai-codex-cli-architecture-multi-runtime-patterns) | Sandbox architecture, multi-runtime patterns |
| [openai/codex (GitHub)](https://github.com/openai/codex) | Codex CLI codebase, release history |
| [Gemini CLI Auto Memory (official docs)](https://geminicli.com/docs/cli/auto-memory/) | Auto Memory extraction, inbox, safety boundaries |
| [GEMINI.md context files (official docs)](https://geminicli.com/docs/cli/gemini-md/) | Hierarchical memory architecture, modular imports |
| [Gemini CLI memory management tutorial (official docs)](https://geminicli.com/docs/cli/tutorials/memory-management/) | /memory commands, scope management |
| [Gemini CLI v0.40.0: Tiered Memory (GitHub Discussion)](https://github.com/google-gemini/gemini-cli/discussions/26216) | Tiered memory rebuild, MCP resource support, Task Tracker |
| [Background memory service for skill extraction (Gemini CLI Issue #24272)](https://github.com/google-gemini/gemini-cli/issues/24272) | Auto Memory design, skill extraction architecture |
| [MCP servers with Gemini CLI (official docs)](https://geminicli.com/docs/tools/mcp-server/) | MCP integration, three transports, tool discovery |
| [Gemini CLI release notes (official docs)](https://geminicli.com/docs/changelogs/) | Release history: v0.39.0 inbox, v0.40.0 tiered memory, v0.42.0 Auto Memory inbox, v0.43.0 adaptive token |
| [Linux Foundation AAIF announcement](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) | AAIF formation, AGENTS.md + MCP governance |
| [Agent Instruction Files: Cross-Tool Portability (Codex Knowledge Base)](https://codex.danielvaughan.com/2026/05/27/agent-instruction-files-agents-md-claude-md-cross-tool-portability-codex-cli/) | AGENTS.md adoption, cross-tool instruction convention, 60K+ projects |
| [OpenClaw optimization guide (GitHub)](https://github.com/OnlyTerp/openclaw-optimization-guide) | OpenClaw memory optimization, context management |
