# Design: features → components terminology rename

**Date:** 2026-07-31
**Status:** approved (brainstorming session with owner)
**Approach:** atomic big-bang rename on a branch, CI green before merge

## Problem

The `features/` folder holds items that are *components* of RHOAI (MCP
Gateway, Agent Catalog, ...), not features. "Feature" is the wrong word —
and it is about to be needed for its real meaning: functionality added to
a component (the thing RHAISTRAT Feature tickets describe). Keeping the
old usage would leave one word carrying two meanings across the repo.

## Decisions (from brainstorming)

1. **Full rename** — directory, routing table, frontmatter key, script
   identifiers, skills, docs, conventions, and all content links/prose.
   No use of "feature" meaning component survives anywhere.
2. **Jira metadata modeled now** — components.yaml gains optional
   `jira_component:` and `jira_labels:` fields.
3. **"Feature" is reserved, not modeled** — conventions define the term;
   no new structure until a workflow needs it (YAGNI).
4. **Atomic execution** — one branch, ordered mechanical steps, no
   compatibility window. Single-owner repo; agents are the main
   consumers; nobody needs a deprecation period.

## Vocabulary contract

| term | meaning |
|---|---|
| **component** | an item in `components/` — a thing that exists in RHOAI. Replaces every prior use of "feature" that meant a partition. |
| **feature** | reserved: functionality added to a component. Defined in `conventions/layout.md`; not structurally modeled yet. |
| **partition** | unchanged generic structural word ("component partition"). |
| Jira `Feature` / `Feature Request` | external vocabulary — Jira issue type names keep the word everywhere (ref_types, JQL, triage prose). |

Component ↔ Jira relationship facts (recorded in conventions):

- Components do **not** necessarily map 1:1 to Jira components — e.g. the
  catalogs and registries land in the **AI Hub** Jira component.
- Components either have or can create Jira **labels** — always
  lowercase (e.g. `mcp-catalog`, `mcp-gateway`, `mcp-registry`).

## Structure & schema changes

- `features/` → `components/` and `restricted/features/` →
  `restricted/components/` — both via `git mv` (history preserved).
- `features/features.yaml` → `components/components.yaml`; top-level key
  `features:` → `components:`.
- Knowledge-entry frontmatter cross-spread key `features:` →
  `components:` (still closed vocabulary against components.yaml ids,
  lint-checked).
- New optional per-component fields:

  ```yaml
  - id: mcp-catalog
    title: MCP Catalog
    ...
    jira_component: AI Hub        # where its issues actually land; not 1:1
    jira_labels: [mcp-catalog]    # list; lowercase enforced by lint
  ```

- Initial population: `jira_component: AI Hub` for the catalog/registry
  components whose stored JQL already scopes to it (mcp-catalog,
  mcp-registry, agent-catalog, agent-registry); `jira_labels` for the
  confirmed labels (`mcp-catalog`, `mcp-gateway`, `mcp-registry`). All
  other entries (including skills-catalog/skills-registry) leave both
  fields absent until confirmed — the fields are optional.

## Rename sweep (in scope)

- **Scripts + tests** (~112 occurrences, 16 files): identifiers
  (`_feature_ids` → `_component_ids`, etc.), error/lint messages,
  `scan_dirs`, schema key handling, all tests.
- **Skills**: every `.claude/skills/*/SKILL.md` + references that mention
  `features/<id>/` or "feature" meaning partition.
- **Docs & conventions**: AGENTS.md, CLAUDE.md, `docs/*`,
  `conventions/*` (layout.md gets the vocabulary contract).
- **Content**: all `/features/...` leading-slash links → `/components/...`;
  `features:` frontmatter keys; prose where "feature" means component —
  including `memory/` profiles, facts, and log. No stale meaning
  survives.
- **Publish**: `publish/manifest.yaml` `source:` paths (19 entries).
- **Restricted**: same sweep under `restricted/` (git-crypt tracked),
  including `work/refresh-*.yaml` configs and lint-patterns if they
  reference paths.
- **Generated files** (views/, all index.md, memory/index.md): never
  hand-edited — regenerated via `python scripts/hub_index.py`.

## Explicitly out of scope / unchanged

- **Public site URLs** — manifest `dest:` paths don't contain
  `features/`; no republish needed, no public link breaks.
- The five-folder skeleton (`knowledge/ research/ strategy/ enablement/
  work/`) inside each partition.
- `narrative/` layer (structurally untouched; its prose gets the same
  terminology sweep only where "feature" meant partition).
- Git history (no rewrite; `git mv` preserves rename tracking).
- The retired `ai-asset-registry` source repo (hub.migrate's *source*
  stays as-is; its skill text about hub *destinations* updates).
- Jira issue-type vocabulary (see contract above).

## The trap: Jira vocabulary collision

A blind find/replace corrupts:

- `ref_types: [Outcome, Feature, Feature Request]` in components.yaml
- JQL strings and stored Jira scopes
- Skill prose about "Feature Request" triage (hub.jira-triage,
  hub.jira-sweep, rfe.* references)

Implementation must use a **reviewed pattern list** (path-scoped,
case-aware replacements), never a bare repo-wide sed, followed by a
**residual grep audit**: `\bfeature` over the tree with an allowlist for
legitimate Jira-vocabulary uses. Any hit outside the allowlist is a
defect.

## Lint & verification

- New lint rule: `jira_labels` values must be lowercase (error).
- Existing closed-vocabulary checks now validate against
  `components/components.yaml`.
- CI gate on the branch before merge:
  `python -m pytest scripts/tests -v` ·
  `python scripts/hub_lint.py` ·
  `python scripts/hub_index.py --check`
- Memory-store edits ride in the reviewed rename commits — the PR review
  is the gate for this batch (per-item hub.capture gating would be noise
  for a mechanical sweep the owner reviews whole).

## Error handling

- Work happens on a branch; `main` never holds a half-renamed state.
- If the residual audit or CI finds stragglers, they are fixed on the
  branch before merge — never merged with known leftovers.
- restricted/ changes verified with git-crypt unlocked before commit.
