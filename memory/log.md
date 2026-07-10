---
type: fact
description: Chronological capture trail — newest first (reserved OKF log file)
timestamp: 2026-07-05
---
## 2026-07-10
- **Update** - preferences profile: no em dashes in any new agent output (conversation, repo entries, docs, commit messages); existing content not retroactively rewritten.
- **Update** — product naming corrected across published hubs + knowledge: "RHOAI Limited" → "RHOAI restricted use entitlement for OpenShift" (owner ruling; surfaced by the disclosure net's first activation; 12 files, republished). restricted/lint-patterns.txt authored and active (10 account patterns + asker-identity, owner-approved).
- **Update** — owner ruling captured: kubeflow/hub confirmed as the RHOAI MCP Catalog upstream — question-kubeflow-hub-catalog-alignment answered; ref + overview lineage documented.
- **Update** — agent-memory research refresh (quick, run 5): doc 19 (market/direction — standalone service phasing supersede, EU AI Act Annex-III deferral provisional, Vertex Memory Revisions, Perplexity Brain validates outcome-weighted episodic, MCP statelessness hits memory-as-MCP), 00 synthesis refreshed (17/18 finally indexed), doc 16 superseded. ALL 5 hub.intake/hub.research acceptance runs complete.
- **Creation** — agent-memory transcript intake (1:1 + 2 team syncs, 2026-06-30/07-07): 3 meeting facts incl. standalone-service direction + revised 3.6-DP/3.7-TP/3.8-GA phasing, ODH agent-memory team repo ref, Wes memory-types doc ref, Khaled Sulayman person entry; MemoryHub ref + Feast-overlap question updated (Feast out as interim; OGX memory tool + MemoryHub are the candidate pair).
- **Creation** — Jira hub skills shipped (backlog #2): hublib Jira client (httpx port from pm-toolkit), hub.jira-sweep/hub.jira-sync, tracked public snapshots with probe-gated summaries, enriched jira-map view, doctor Jira probe (#19 slice). #27(b) jira-gap unblocked.
- **Creation** — fact-concurrent-session-git-hygiene: the two cross-session contamination mechanisms (shared index sweep f9a1e31/ef4cc49; nested-worktree edits) + standing guards — consolidated from both sessions' scratch notes.
- **Creation** — fact-disclosure-warning-triage-2026-07-10: all 18 new HTML heuristic warnings ruled benign (11 public market figures, 6 JS $1 tokens, 1 illustrative $500); don't re-triage unless the lines change.
- **Update** — enhancement batch shipped (#5 #7 #10 #15 #16 → Done): disclosure lint (restricted/lint-patterns.txt, errors) + pre-commit gate hook (doctor §10, installed on this machine, 20 ok/0 fail) + hub_status.py morning brief + hub_index --rotate-log + hub_publish --check-links publish gate; the link gate's first CI run caught and led to repair of 80 broken RHCL-hub subpage cross-links. Follow-up filed as #34 (frontmatter heuristic gap).
- **Update** — RHOAI architecture repo (opendatahub-io/architecture-context) promoted to standing-context status: ref rewritten (what's inside, AGENT_USAGE.md entry, per-release snapshots), new ADR-repo ref filed, and hub.research/hub.intake now reference it routinely (research briefs carry the matching snapshot; new feature overviews link it).

## 2026-07-09
- **Creation** — hub.intake + hub.research skills shipped (backlog #1, #27a): conventions/research.md series contract, warning-only research lint, domains/redhat-ai.yaml. #27(b) jira-gap re-scoped, gated on #2.
- **Update** — customer-tracker data landed (migrate-on-touch): tracker HTML + 5 meeting transcripts (3 accounts) + 2 customer deliverable docs copied byte-identical from the old repo into restricted/features/platform/work/customer-tracker/ (gitignored, local-only; transcriptions/ → transcripts/ rename applied; old-repo copy frozen with a MOVED note). Owner rulings: deliverables stay with the suite; keep + breadcrumb. A real tracker now exists on this machine — the wave-3 refresh/sync smokes are unblocked.
- **Creation** — docs/enhancements.md: the repo's own improvement backlog — R5/R6 runbooks spelled out + 23 prioritized enhancements across human usage, agent usage, and repo functionality, plus the recorded small-fix batch and explicit anti-goals.
- **Update** — HTML enablement migration complete (sets 1–4): 14 artifacts live on the pages site incl. the RHCL and MCP Management hubs (scrubbed per owner disclosure rulings 1b/2b); NVIDIA POC, auth deck, and GA readout stay archived in the old repo (3c/4c/5c).

## 2026-07-08
- **Creation** — narrative layer live (D12–D16): narrative/ seeded (4 RHAI pillars + 2 source refs + 2 stories), features: connection axis, qa/jtbd/artifact types, 4 new views; platform shed story content to narrative/; JTBD persona vocabulary locked (7).
- **Update** — owner ruling: no LLM-provider credential handling in the hub at all (users arrive with Claude Code/Cursor already configured; restricted/.env never carries such keys) — the exclusion machinery ported with R4 wave 4 earlier today was removed (doctor.sh, tooling.md, history.md scrubbed; convention stated once in docs/mcp-servers.md; preferences profile updated).
- **Update** — R4 wave 4: slack + google-workspace MCP setup ported from the old repo-doctor (doctor sections 8–9: Claude-config write + podman runtime; doctor now sources restricted/.env with the LLM-cred exclusion; new docs/mcp-servers.md guide). Live-verified on this machine: 19 ok / 0 warn / 0 fail.

## 2026-07-07
- **Creation** — documentation suite: six guides added under docs/ (architecture, memory, skills, publishing, tooling, history), README rebuilt as the front door with a doc index, AGENTS.md/CLAUDE.md/setup/working-here cross-linked. Goal: bus-factor pillar — operable without Peter in the room.

## 2026-07-06
- **Update** — R4 wave 3: customer-feedback suite ported (tracker data model: restricted + external rhai-customer-tracker; rhai-tracker doctor section live; customer names scrubbed from skill texts). Active R4 waves complete.
- **Update** — R4 wave 2: blog-create + blog-mockup ported (guide co-located as skill reference); first real blog will be the smoke.
- **Update** — R4 wave 1: presentation-create ported (10 adaptations); first enablement artifact migrated + published (mcp-registry catalog deck).
- **Update** — Batch 6 applied: workspace document parity → 48 docs into research/, strategy/, and work/ (agent-memory 27, agent-registry 9, skills-registry 10, agent-ops 1, gen-ai-studio 1); document parity COMPLETE.
- **Update** — Batch 5 applied: knowledge-review parity pass → 12/25 already covered, 3 dead (unified-framework), 10 new + 10 edits + 3 documents (first research/ + strategy/ content); content parity with old repo COMPLETE.
- **Update** — R2 COMPLETE: batch 4 applied (monolith §9–§11+§13 + R3 seed) → 66 new (37 fact/decision/question + 29 person) + 5 edits + 10 restricted + 4 memory facts; monolith fully decomposed across 4 batches.
- **Update** — R2 batch 3 applied: monolith §5–§8 → 18 new (14 public + 4 restricted) + 7 edits; roadmap profile refreshed (past milestones → History, 3.5 = Dev Preview).
- **Update** — R2 batch 2 applied: monolith §1+§2+§4 → 4 new + 4 edits; asset-registry partition removed (dead proposal — Kubeflow Hub entries re-homed to platform).
- **Update** — R2 batch 1 applied: monolith §3+§12 → 85 entries (74 public + 11 restricted-local + 3 public siblings), 9 partitions created (mcp-gateway, mcp-registry, mcp-ecosystem, agent-registry, asset-registry, platform, agent-memory, agent-ops, gen-ai-studio).
- **Creation** — filed ref-odh-skills-registry; created skills-registry partition (T13 smoke)
- **Update** — consolidated 1 scratch item: build progress → profiles/now.md
- **Creation** — captured ODH plugin availability fact (hub build T11 smoke)

## 2026-07-05
- **Creation** — memory store seeded at hub creation: profiles (roadmap,
  strategy, now, preferences) and fact-hub-design-decisions, carried from the
  design-brainstorm session and old-repo CLAUDE.md.
