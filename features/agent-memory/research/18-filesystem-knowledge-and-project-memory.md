---
title: Filesystem Knowledge Organization & Project-Scoped Agent Memory — Best Practices
description: Verified best practices for organizing knowledge at the filesystem level and implementing project-scoped, in-repo, harness-agnostic agent memory in git repos.
source: ai-asset-registry/agent-memory/research/18-filesystem-knowledge-and-project-memory.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Filesystem Knowledge Organization & Project-Scoped Agent Memory — Best Practices

**Purpose:** Survey verified best practices for organizing knowledge at the filesystem level and implementing project-scoped, in-repo, harness-agnostic agent memory in git repos — capture-as-you-go, cross-session continuity, keeping changeable facts current, and file/frontmatter/index conventions — and assess the evidence for how to decompose a monolithic knowledge registry. Companion to the [OKF evaluation](17-open-knowledge-format.md); both commissioned by the rhoai-agentic-hub charter research agenda.

**Date:** 2026-07-05

**Author:** Peter Double (Principal PM — MCP & AI Asset Registries)

**Status:** EXPLORATORY — commissioned for the [rhoai-agentic-hub charter](https://github.com/solaius/ai-asset-registry/blob/main/docs/superpowers/specs/2026-07-05-rhoai-agentic-hub-charter.md) research agenda (§8). Builds on [research 09](09-agent-harness-memory.md) (harness memory mechanisms) and [research 10](10-claude-memory-dreaming.md) (Claude memory architecture) — this document does not repeat that ground; it extracts what is directly reusable for an **in-repo** store and adds the filesystem-knowledge and docs-as-code prior art those documents did not cover.

**Research series — Agent Memory:**
- Document 18 of 19
- **Phase 1 (landscape):** [00](00-executive-summary.md) · [01](01-landscape-and-definitions.md) · [02](02-solution-survey.md) · [03](03-memoryhub-deep-dive.md) · [04](04-technical-patterns.md) · [05](05-standards-and-protocols.md) · [06](06-ogx-memory-primitives.md) · [07](07-taxonomy-and-decomposition.md) · [08](08-rhoai-ocp-alignment.md)
- **Phase 2 (deep dives):** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · [11](11-adversarial-memory.md) · [12](12-benchmarking-evaluation.md) · [13](13-kv-cache-optimization.md) · [14](14-enterprise-use-cases.md) · [15](15-multi-modal-memory.md) · [16](16-ai-gateway-memory-substrate.md)
- **Phase 3 (rhoai-agentic-hub charter):** [17](17-open-knowledge-format.md) · 18 (this doc)
- **Strategy:** [README](/features/agent-memory/strategy/strategy-overview.md) · [Strategy](/features/agent-memory/strategy/agent-memory-strategy.md) · [Use Cases](/features/agent-memory/strategy/use-cases-and-personas.md) · [Architecture](/features/agent-memory/strategy/recommended-architecture.md) · [Outcome](/features/agent-memory/strategy/rhaistrat-1345-outcome-update.md) · [RFE Roadmap](/features/agent-memory/strategy/rfe-roadmap.md)

---

## Contents

1. [Scope and Evidence Standard](#1-scope-and-evidence-standard)
2. [Harness Conventions: What Ships Today](#2-harness-conventions-what-ships-today)
3. [Memory-Platform Prior Art](#3-memory-platform-prior-art)
4. [Filesystem Knowledge Methods (PKM)](#4-filesystem-knowledge-methods-pkm)
5. [Docs-as-Code Modularization Evidence](#5-docs-as-code-modularization-evidence)
6. [Convergent Design Patterns](#6-convergent-design-patterns)
7. [Decomposing the Knowledge Registry (Strand C)](#7-decomposing-the-knowledge-registry-strand-c)
8. [Implications](#8-implications)
9. [Open Questions](#9-open-questions)
10. [Sources](#10-sources)

---

## 1. Scope and Evidence Standard

Same method and labeling as [research 17 §1](17-open-knowledge-format.md#1-context-and-method): **[verified]** = survived 3-vote adversarial verification (25/25 confirmed, 0 refuted) or confirmed first-party; **[reported]** = fetched source, not independently verified; **[inference]** = grounded interpretation.

**Coverage caveat (important):** several systems named in the research brief produced no *verified* claims — Cursor rules specifics, OpenAI/Codex conventions, and MemoryHub-style scoped governance are covered only via [reported] sources or earlier series docs ([09](09-agent-harness-memory.md), [03](03-memoryhub-deep-dive.md)). The verified prior art concentrates on **Claude Code, Letta, and Zep/Graphiti**. Strand C (decomposition axis) produced **no directly verified evidence** — §7 is explicit about resting on [reported] docs-as-code sources plus design inference.

---

## 2. Harness Conventions: What Ships Today

[Research 09](09-agent-harness-memory.md) surveyed harness memory broadly; this section verifies the specifics that constrain an **in-repo, harness-agnostic** store.

### 2.1 Claude Code: the gap and the bridge

- **Auto memory is per-repository but lives OUTSIDE the repo** (`~/.claude/projects/<project>/memory/`) and is explicitly machine-local — "Files are not shared across machines or cloud environments" [verified, official docs, fetched live 2026-07-05]. Open feature requests (#25739 portable project memory, #38519 in-repo storage) independently corroborate the gap. **The default mechanism cannot serve as in-repo, team-shared memory** — the hub must supply its own store.
- **The index-plus-topic-files convention is directly reusable**: a concise `MEMORY.md` index — only its **first 200 lines or 25KB** load at session start — with detailed notes moved to topic files that are read on demand [verified]. The convention, not the implementation, is what transfers.
- **Relocation is possible but awkward**: `autoMemoryDirectory` (readable from any settings scope, gated by the workspace-trust dialog for project settings) can point auto memory into the repo — but the value **must be an absolute path or `~/`**, which does not port cleanly when checked into project settings across machines [verified; GH #36636 confirms the contract is enforced]. Practical options: per-machine `.claude/settings.local.json`, or a repo-doctor bootstrap step that writes the absolute path locally [inference].
- **The harness-agnostic entry point is a shim**: Claude Code reads `CLAUDE.md`, not `AGENTS.md`, at session start; the officially recommended bridge is a `CLAUDE.md` containing `@AGENTS.md` (on Windows, the import — symlinks need Administrator/Developer Mode) [verified]. Native AGENTS.md support remains an open issue (#34235; predecessor had 3,200+ upvotes). Precision caveat: `/init` *does* read an existing AGENTS.md when generating a CLAUDE.md — "does not read" is exact only for session-start loading [verified].
- **Sizing guidance**: keep each CLAUDE.md under ~200 lines (longer files reduce adherence); `@path` imports recurse at most 4 hops and **load fully at launch** — imports organize content but do not reduce context cost; `.claude/rules/` files with `paths` frontmatter load only when matching files are touched [reported, official docs via extraction — consistent with observed behavior].

### 2.2 The AGENTS.md ecosystem

- AGENTS.md is the de facto cross-tool instruction standard: read natively by Codex, Cursor, Copilot, Gemini CLI, Aider, Windsurf, Zed, and others; shipping in 60,000+ public repositories; **Claude Code is the notable absentee** from the native-reader list [reported, prpm.dev, May 2026]. Nearest-file-wins directory scoping (root file for defaults, per-package overrides) is prior art for directory-scoped knowledge decomposition [reported].
- **Instruction files are not memory.** They are human-authored, static configuration; nothing in the AGENTS.md convention covers agent-written, evolving facts. The hub's store fills a layer the instruction-file ecosystem deliberately leaves empty [inference].
- **Quality evidence — human curation matters**: a February 2026 ETH Zurich study (AGENTbench; 138 instances, 12 Python repos, arXiv 2602.11988) reportedly found **LLM-generated repo context files reduced agent task success ~3% versus no context while raising inference cost 20%+, whereas human-written files improved success ~4%** [reported — not independently verified; the arXiv ID should be checked before citing onward]. Directional implication: auto-capture needs a curation gate, not blind accumulation.

### 2.3 Bottom line for the hub

No harness reads an in-repo memory store natively today. The proven wiring is: **in-repo store (own conventions) ← referenced by → AGENTS.md ← imported by → CLAUDE.md shim**, with `autoMemoryDirectory` as an optional Claude-specific enhancement handled per-machine [verified components; composition is inference].

---

## 3. Memory-Platform Prior Art

### 3.1 Letta (MemGPT lineage): the closest direct precedent

- **Memory blocks**: typed records with four core fields — `label` (unique id), `description` (purpose), `value` (content), `limit` (character cap) — living *inside* the context window, persistent across interactions, no retrieval step. "The description is the main information used by the agent to determine how to read and write to that block" [verified]. Precedent for (a) an always-in-context tier and (b) description-bearing frontmatter as the read/write routing signal. Caveat: blocks persist *while attached*; Letta also has a separate retrieval-based archival tier [verified].
- **MemFS — a git-backed "context repository"**: Letta projects agent memory into **plain markdown files with YAML frontmatter carrying a required `description`**, on the local machine, with version history, conflict resolution, and direct human inspection/editing. Two-tier loading: a `system/` directory (persona, user preferences, durable project facts, workflow rules) is **always injected into the system prompt**; all other files are exposed only as a **tree of paths and descriptions**, contents loaded on demand [verified, docs + OSS implementation]. This is the closest shipping analog of what the charter describes. Scoping caveats: MemFS is specific to the Letta Agent/Letta Code product line and is managed by Letta's harness — the *format* (markdown-in-git, frontmatter descriptions, tiered loading) is what transfers, not the management layer [verified caveat].

### 3.2 Zep/Graphiti: the temporal-validity mechanism

- **Three-tier graph**: raw episode subgraph (verbatim capture) → semantic entity subgraph (extracted, resolved facts) → community subgraph (higher-level clusters; optional/on-demand in OSS Graphiti) [verified, paper + code].
- **Bi-temporal model**: fact-valid time (`t_valid`/`t_invalid`) tracked separately from system-ingest time (`t'_created`/`t'_expired`); when new information contradicts a stored fact, the superseded edge is **invalidated (t_invalid set), not deleted** [verified against paper and shipped code fields]. This is the best-verified mechanism for the charter's problem 3 — roadmap dates and strategy shifts that must stay current *without losing history* — and it approximates cleanly in frontmatter (§6.4).
- Reported benchmarks (vendor-authored, not independently validated): DMR 94.8% vs MemGPT's 93.4%; LongMemEval accuracy +18.5% with ~90% latency reduction vs full-context baselines [reported].

### 3.3 Mem0: how much machinery is actually needed

- Architecture: an **extraction-based pipeline** — extract, consolidate, and retrieve salient facts rather than persist transcripts; the canonical capture-as-you-go shape [reported, arXiv 2504.19413].
- Two findings bear directly on how heavy the hub's store needs to be [reported, vendor paper]: (1) adding graph memory on top of the base fact store yielded only **~2%** overall improvement on LOCOMO — consolidated *fact stores capture most of the value*; (2) selective memory vs full-history replay: 91% lower p95 latency, >90% token savings. Directional support for a plain, file-based fact store over graph infrastructure at this scale [inference].

### 3.4 LangMem: the taxonomy and two decisive distinctions

- Long-term memory divided into **semantic** (facts), **episodic** (past interactions as examples), **procedural** (evolving behavioral instructions) [reported] — consistent with the CoALA framing in [research 01](01-landscape-and-definitions.md).
- **Collections vs. profiles** — the sharpest available answer to "how do changeable facts stay current": *collections* are append-oriented sets of individual records; *profiles* are **single schema-bound documents representing current state, updated in place** when new information arrives — no stale accumulation [reported]. Roadmap dates, strategy direction, and feature status are profile-shaped; decisions and meeting-derived facts are collection-shaped [inference].
- **Hot-path vs. background formation**: capture during the conversation (immediate, adds latency/effort) vs. reflective consolidation afterwards [reported] — the same split as Claude's dreaming consolidation ([research 10](10-claude-memory-dreaming.md)). The charter's goal B is hot-path; a maintenance skill doing periodic consolidation is the background half [inference].
- Contrast point: LangMem persists via LangGraph's `BaseStore` (database-backed) — harness-coupled, the opposite of the charter's constraint [reported].

---

## 4. Filesystem Knowledge Methods (PKM)

Human personal-knowledge-management methods are prior art for the *organization* half of the charter (all [reported] — practitioner literature, not controlled studies):

- **PARA** splits a knowledge base into four top-level categories **by actionability and time-horizon**, not topic: Projects (deadline-bound), Areas (ongoing standards), Resources (reference topics), Archive (inactive). Notably orthogonal to both feature-based and type-based decomposition (§7).
- **Johnny.Decimal** numeric prefixes (`10-`, `20-`, …) buy deterministic, stable sort order and citable addresses — at the cost of renumbering friction when structure changes.
- **Zettelkasten** contributes atomic notes plus explicit links (`[[wiki-links]]`) over folder placement as the discoverability mechanism; hybrid PARA × Johnny.Decimal schemes are common practice.
- Practitioner claim worth keeping: **findability degrades non-linearly with note volume** — decompose before the monolith crosses the threshold, not after [reported].
- One practitioner template (jabez007/johnny-decimal-zettelkasten) demonstrates the full combination *as agent memory*: a dedicated `AGNT/` namespace separating machine memory from human knowledge — atomic procedural-rule files plus chronological session logs (`JRNL/`), a boot/shutdown protocol restoring state at session start and writing durable rules back at end, a "librarian" agent proposing to file insights from live sessions ("crystallization"), strict frontmatter (`entities`, `communities`, `status` lifecycle), and generated indexes replacing hand-maintained ones. **Illustrative only — single-author template, 2 stars, no adoption** [reported, with explicit maturity flag]. Its *shape* (namespace separation, session log + rule store, capture-with-proposal) closely matches the charter's B→A goals [inference].

---

## 5. Docs-as-Code Modularization Evidence

The strongest available evidence on splitting monolithic knowledge artifacts comes from documentation engineering (all [reported] unless noted):

- **Red Hat modular docs** (the in-house standard): decompose into typed **modules** — concept / procedure / reference, encoded in filename prefixes (`con-`, `proc-`, `ref-`) — combined into **assemblies**, where an assembly is explicitly "the docs realization of a user story." Granularity criterion: **standalone value** — a module must make sense read alone; modules never nest modules. Anti-pattern warning: deeply nested assemblies harm usability and maintainability. Storage axis = content type; aggregation axis = user goal — *two different axes at two different layers* — the pattern §7 builds on.
- **Diátaxis**: four forms by user need (tutorials, how-to, reference, explanation); adopted by hundreds of projects (Cloudflare credits it as the basis of its IA). Two process warnings directly relevant to the hub migration: improve **incrementally, smallest unit at a time** — good structure *emerges from* iteration rather than being imposed — and **never pre-create empty category scaffolds** before content exists to fill them.
- **SUSE monolith→modular case study** (tcworld): decomposed modular articles drew **~15× more views** than the same content as a monolithic guide chapter (11,105 vs 755 over three months), attributed to per-article metadata and search ranking; >80% of readers arrive via search seeking specific answers. Splitting axis chosen in practice: audience/task. They kept plain files in git specifically to preserve developer contributions (docs-as-code) — the same contribution argument the transcript's "engineers submit PRs against deployment guides" vision makes.
- **Pragmatic thresholds** (adoc-studio): modularity pays off above ~10 documents / multiple variants / multiple writers; below ~5 docs with one author it's overhead. **Start coarse, split when a concrete reuse or maintenance need appears; migrate existing content at its next revision, not big-bang.** Modularization is a workflow commitment more than a technical one.

---

## 6. Convergent Design Patterns

Where independent systems arrive at the same answer, confidence is highest. Six convergences:

### 6.1 Index + lazy-loaded, frontmatter-described files
Claude Code (MEMORY.md 200-line/25KB index + on-demand topic files) [verified], Letta MemFS (paths-and-descriptions tree + on-demand content, small always-loaded `system/` tier) [verified], and OKF (`index.md` progressive disclosure over `description`-bearing concepts) [verified] independently converge. **This is the settled architecture for the hub's store**: a small always-loaded index; everything else described in frontmatter and loaded on demand.

### 6.2 The always-loaded tier must stay small
200 lines/25KB (Claude), `system/` only (Letta), CLAUDE.md ~200-line guidance with imports that don't reduce context [verified/reported]. Budget discipline on the index is a design requirement, not a style preference.

### 6.3 `description` is the load-bearing field
Letta: "the main information used by the agent to determine how to read and write to that block" [verified]; OKF: feeds index generation and previews [verified]; Claude memory frontmatter: drives recall relevance. Every file in the store carries a one-line description; index entries derive from it.

### 6.4 Changeable facts: update-in-place + invalidate-don't-delete
LangMem profiles (current-state documents updated in place) [reported] answer *where the current value lives*; Zep's bi-temporal invalidation [verified] answers *how history survives*. File-based approximation [inference]: profile-shaped files for volatile state (roadmap dates, strategy direction, feature status) carrying validity frontmatter — e.g. `valid_from`, `superseded_by`, `status: current|superseded` — with git history plus OKF `log.md` as the transaction timeline. This is the concrete fix for the charter's "stop re-reminding the agent" problem, and the two-timeline distinction (fact-valid vs recorded) maps naturally onto frontmatter vs git commits.

### 6.5 Capture is two-phase: hot-path + background consolidation, with a human gate
LangMem hot-path vs subconscious formation [reported]; Claude dreaming ([research 10](10-claude-memory-dreaming.md)); Mem0 extraction pipeline [reported]; the librarian/crystallization proposal pattern [reported]; and the ETH-Zurich finding that generated context can be net-negative without human curation [reported]. Design shape: capture-as-you-go writes small, typed facts immediately (goal B); a periodic maintenance skill consolidates, dedupes, and prunes; a human review gate guards durable promotions [inference].

### 6.6 Migrate incrementally, never big-bang
Diátaxis (structure emerges from iteration; no empty scaffolds) [reported]; adoc-studio (split on concrete need; convert at next revision) [reported]; OKF's tolerated broken links enabling incremental decomposition [verified]. The hub migration should move content as it's touched, not restructure 1,105 lines in one pass.

---

## 7. Decomposing the Knowledge Registry (Strand C)

**Evidence status: no directly verified prior art surfaced for the specific question** (feature vs asset type vs source axis for a PM knowledge registry). What follows combines [reported] docs-as-code evidence, local first-party analysis, and clearly-flagged design inference.

### 7.1 The local problem, precisely

First-party analysis of this repo (2026-07-05): `docs/knowledge-registry.md` is a 1,105-line monolith with 13 *topical* sections; `docs/knowledge-review/` already decomposes similar content into 24 files across 11 *aspect* directories (architecture/, components/, personas/, strategy/, …); and the workspaces (`mcps/`, `agents/`, `agent-memory/`, `skills/`) split by *feature*. **Three organizing axes coexist, with an undefined division of labor between the monolith and its decomposition** — the monolith is the designated "start here" yet substantially overlaps the per-domain files. The decomposition question is therefore not "which single axis" but "which axis at which layer."

### 7.2 What the prior art actually says

| Source | Axis it decomposes on | Layer |
|---|---|---|
| Red Hat modular docs [reported] | Content type (concept/procedure/reference) for *storage*; user story for *aggregation* (assemblies) | Two axes, two layers |
| Diátaxis [reported] | User need (learn/do/look up/understand) | Presentation |
| SUSE case [reported] | Audience/task, self-contained topics assembled into articles | Storage → aggregation |
| PARA [reported] | Actionability/time-horizon (project/area/resource/archive) | Top level |
| LangMem namespaces [reported] | Hierarchical scope (org/user/app) | Store partitioning |
| OKF [verified] | Deliberately none — "directory structure is independent of the domain" | — |
| AGENTS.md nearest-file-wins [reported] | Directory proximity to the code it governs | Instruction scoping |

The consistent meta-pattern: **mature systems separate the storage axis from the consumption axis** — small typed units stored one way, aggregated into audience/goal-shaped views another way, with indexes/assemblies bridging. No system in evidence stores knowledge monolithically by topic, which is what `knowledge-registry.md` currently does.

### 7.3 Direction this suggests (design inference, to be settled in the design phase)

- **Feature/domain as the primary storage partition** — it matches how the work arrives (per-feature research, RFEs, hubs), how the workspaces already split, and PARA's insight that active work areas (Areas) are the natural first cut. Registries become per-feature bundles (OKF: bundle-as-subdirectory).
- **Typed entries within each partition** (decision, fact/status, reference/pointer, person/stakeholder, open question — echoing the registry's 13 sections, Red Hat's typed modules, and this repo's existing memory `type:` frontmatter) rather than prose sections.
- **Cross-cutting views as generated indexes, not hand-maintained files** — the "all decisions," "all open questions," "everything about roadmap dates" views the monolith currently provides by topic section become index files derived from frontmatter (OKF `index.md` synthesis; the practitioner Bases pattern; `frontmatter.py rebuild-index` is this repo's own working precedent).
- **Granularity by standalone value, split on concrete need, migrate at next touch** (§5, §6.6) — start with coarse per-feature registries and let entry-level atomization emerge where change frequency demands it.

Held loosely: strand C is the design phase's decision to make, with targeted follow-up (enterprise wiki IA literature, PM knowledge-base cases) if more evidence is wanted before committing.

---

## 8. Implications

### 8.1 For rhoai-agentic-hub (charter goals B → A → C)

1. **B (capture-as-you-go):** two-phase capture — immediate small typed writes + periodic consolidation skill + human gate for durable promotions (§6.5). OKF `log.md` is the spec-blessed chronological capture surface ([17 §6](17-open-knowledge-format.md)).
2. **A (continuity):** index-plus-lazy-load store (§6.1–6.3) wired through the AGENTS.md → CLAUDE.md shim (§2.3); profile-shaped current-state files with validity frontmatter kill the re-reminding problem (§6.4).
3. **C (deferred dogfooding):** the semantic/episodic/procedural taxonomy (§3.4, [research 01](01-landscape-and-definitions.md)) maps onto entry types without constraining them now; nothing in the proposed shape blocks later alignment with the RHOAI substrate direction ([research 16](16-ai-gateway-memory-substrate.md)).
4. **Structure:** per-feature registries of typed, frontmatter-described entries with generated cross-cutting indexes; incremental migration (§7.3).

### 8.2 For the RHOAI agent-memory product line

- **The file-tier pattern is converging in public** (Claude, Letta, OKF — §6.1). [Research 09 §9](09-agent-harness-memory.md)'s harness-integration implications now have a concrete, spec-shaped at-rest format candidate; any RHOAI memory product that can import/export the index-plus-frontmatter file shape meets agents where they already are [inference].
- **Bi-temporal validity is the differentiating mechanism** for enterprise "facts that change" (§3.2) — governed memory without it loses audit history; MemoryHub-derived governance ([research 03](03-memoryhub-deep-dive.md)) plus bi-temporal fact management is a natural pairing [inference].
- **The curation-gate evidence** (§2.2) supports the human-review-gate posture this series already adopted (REVIEW-NOTES) and should inform any auto-capture feature claims [inference].
- This document plus [17](17-open-knowledge-format.md) updates the [research 05](05-standards-and-protocols.md) standards map: still no memory standard, but the knowledge-at-rest layer now has a draft convention with real velocity.

---

## 9. Open Questions

1. **Strand C follow-up:** is targeted research into enterprise wiki/IA literature worth it before the design phase, or is §7.3 enough to design against? (Charter design phase decides.)
2. **Validity schema:** minimal sufficient frontmatter set for changeable facts — `valid_from`/`superseded_by`/`status`? Does `log.md` or git history serve as the transaction timeline? (Shared with [17 §10](17-open-knowledge-format.md).)
3. **Windows/harness wiring:** shim + relative-path references vs per-machine `settings.local.json` vs repo-doctor writing `autoMemoryDirectory` — which combination, and does the harness auto-memory remain a *cache* over the in-repo store or get retired?
4. **Consolidation cadence:** what triggers the background consolidation skill (session end, scheduled, threshold), and what is its authority without the human gate?
5. **ETH Zurich study verification:** confirm arXiv 2602.11988 and its findings before citing in any strategy artifact.

---

## 10. Sources

**Verified primary:**
- [Claude Code memory docs](https://code.claude.com/docs/en/memory) (fetched live 2026-07-05) — auto memory location/limits, MEMORY.md index, `autoMemoryDirectory`, CLAUDE.md/@AGENTS.md guidance
- [Letta — memory blocks](https://docs.letta.com/guides/core-concepts/memory/memory-blocks) · [Letta Agent memory / MemFS](https://docs.letta.com/letta-agent/memory) · [MemFS docs](https://docs.letta.com/letta-code/memfs) · [Context Repositories blog](https://www.letta.com/blog/context-repositories/) (cross-checked against OSS letta-code implementation)
- [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956) (cross-checked against shipped Graphiti code fields) · [Graphiti docs](https://help.getzep.com/graphiti) · [getzep/graphiti](https://github.com/getzep/graphiti)
- Claude Code GitHub issues [#25739](https://github.com/anthropics/claude-code/issues/25739), [#38519](https://github.com/anthropics/claude-code/issues/38519), [#34235](https://github.com/anthropics/claude-code/issues/34235), [#36636](https://github.com/anthropics/claude-code/issues/36636)
- First-party repo analysis: `docs/knowledge-registry.md` (1,105 lines, 13 sections), `docs/knowledge-review/` (24 files, 11 dirs), workspace layout — 2026-07-05

**Reported (fetched, not independently verified):**
- [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](https://arxiv.org/abs/2504.19413) (vendor paper)
- [LangMem conceptual guide](https://github.com/langchain-ai/langmem/blob/main/docs/docs/concepts/conceptual_guide.md)
- [prpm.dev — AGENTS.md deep dive](https://prpm.dev/blog/agents-md-deep-dive) · [codersera — AGENTS.md vs CLAUDE.md vs Cursor rules](https://codersera.com/blog/agents-md-vs-claude-md-vs-cursor-rules-comparison-2026/)
- [Red Hat Modular Documentation Reference Guide](https://redhat-documentation.github.io/modular-docs/) · [Diátaxis](https://diataxis.fr/) · [tcworld — From monolithic to modular documentation (SUSE)](https://www.tcworld.info/e-magazine/technical-writing/from-monolithic-to-modular-documentation) · [adoc-studio — Modularize documentation](https://www.adoc-studio.app/blog/modularize-documentation)
- [NotePlan — Johnny.Decimal + PARA](https://help.noteplan.co/article/155-how-to-organize-your-notes-and-folders-using-johnny-decimal-and-para) · [jabez007/johnny-decimal-zettelkasten](https://github.com/jabez007/johnny-decimal-zettelkasten) (illustrative practitioner template; 2 stars — no adoption weight)

**Method:** Deep-research workflow wf_3bbb2259-92b (2026-07-05): 5 angles, 24 sources fetched, 119 claims extracted, 25 verified 3-0 (0 refuted). Strand-C and PKM claims are from the extraction layer (fetched sources) below the top-25 verification cut — labeled [reported] throughout.
