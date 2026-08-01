# Implementation plan: enhancements-to-issues migration

**Spec:** [2026-08-01-enhancements-to-issues-design.md](/docs/superpowers/specs/2026-08-01-enhancements-to-issues-design.md)
**Date:** 2026-08-01

## Phase 1: Create labels (sequential, must complete before Phase 2)

Create 7 labels via `gh label create`:

1. `priority: next` -- `#1d76db` -- "Active candidates, ready to pick up"
2. `priority: later` -- `#5319e7` -- "Data-gated or low urgency"
3. `theme: integration` -- `#0e8a16` -- "Integrating external tools/repos"
4. `theme: infrastructure` -- `#fbca04` -- "Doctor, cross-machine, env tooling"
5. `theme: content` -- `#f9d0c4` -- "Publishing, narrative, FAQ"
6. `theme: tooling` -- `#c5def5` -- "Agent context, search, logging, scripts"
7. `theme: process` -- `#d4c5f9` -- "Slack sweep, JTBD mining, multi-writer"

## Phase 2: Create issues (parallel subagents, after Phase 1)

Create 14 issues. Each subagent creates one issue via `gh issue create`
with the title, body (following the spec format), and labels.

Issues must be created sequentially to control number assignment. Order:
"next" priority first, then "later" -- within each tier, by theme
clustering for a clean issue list.

### Next tier (issues 1-3)
1. Outcome Creator integration (old #37) -- `enhancement, priority: next, theme: integration`
2. UX Research Insights integration (old #38) -- `enhancement, priority: next, theme: integration`
3. Prototyping skills (old #32) -- `enhancement, priority: next, theme: integration, theme: tooling`

### Later tier (issues 4-14)
4. Curated FAQ / JTBD publishing (old #12) -- `enhancement, priority: later, theme: content`
5. Narrative growth (old #22) -- `enhancement, priority: later, theme: content`
6. Weekly digest view (old #23) -- `enhancement, priority: later, theme: content, theme: tooling`
7. Search for humans (old #21) -- `enhancement, priority: later, theme: tooling, theme: content`
8. Agent context pack (old #20) -- `enhancement, priority: later, theme: tooling`
9. PostToolUse usage logging (old #33) -- `enhancement, priority: later, theme: tooling, theme: infrastructure`
10. Python-based doctor rewrite (old #36) -- `enhancement, priority: later, theme: infrastructure`
11. Slack sweep assist (old #17) -- `enhancement, priority: later, theme: process, theme: tooling`
12. JTBD mining (old #18) -- `enhancement, priority: later, theme: process`
13. Multi-writer promotion (old #24) -- `enhancement, priority: later, theme: process`
14. Red Hat Support case search/analysis (old #31) -- `enhancement, priority: later, theme: process, theme: tooling`

## Phase 3: Rewrite enhancements.md (after Phase 2, needs issue numbers)

Rewrite `docs/enhancements.md` in the new narrative format using the
assigned GitHub issue numbers. The current technical detail moves into
the issue bodies (done in Phase 2); the doc retains only the strategic
narrative per item.

## Phase 4: Commit and push

Single commit covering the spec, plan, and rewritten enhancements.md.
