# Enhancements-to-issues migration

**Date:** 2026-08-01
**Owner:** Peter Double

## Overview

Migrate actionable items from `docs/enhancements.md` into GitHub issues,
then rewrite the doc as a narrative index linking to those issues. The doc
becomes the strategic "what and why" layer; the issues become the
actionable "scope and done" layer.

## Decisions

- **New numbering.** GitHub assigns sequential issue numbers; all old `#N`
  identifiers are retired. Existing references in enhancements-complete.md
  and specs are not updated (they're historical).
- **Scope of migration.** Only "Next" and "Later" items become issues (14
  total). "Someday" and "Deliberately not doing" stay doc-only.
- **Item #6 excluded.** R5 remaining cross-machine steps dropped from migration
  per owner decision.
- **Issue-first order.** Labels created, then issues created, then doc rewritten
  using the real issue numbers.

## Label taxonomy

### Priority labels (mutually exclusive)

| Label | Color | Meaning |
|---|---|---|
| `priority: next` | `#1d76db` | Active candidates, ready to pick up |
| `priority: later` | `#5319e7` | Data-gated or low urgency |

### Theme labels (non-exclusive)

| Label | Color | Meaning |
|---|---|---|
| `theme: integration` | `#0e8a16` | Integrating external tools/repos |
| `theme: infrastructure` | `#fbca04` | Doctor, cross-machine, env tooling |
| `theme: content` | `#f9d0c4` | Publishing, narrative, FAQ |
| `theme: tooling` | `#c5def5` | Agent context, search, logging, scripts |
| `theme: process` | `#d4c5f9` | Slack sweep, JTBD mining, multi-writer |

Every issue also receives the existing `enhancement` label.

## Issue mapping

| Old # | Title | Priority | Themes |
|---|---|---|---|
| #37 | Outcome Creator integration | next | integration |
| #38 | UX Research Insights integration | next | integration |
| #32 | Prototyping skills | next | integration, tooling |
| #12 | Curated FAQ / JTBD publishing | later | content |
| #17 | Slack sweep assist | later | process, tooling |
| #18 | JTBD mining | later | process |
| #20 | Agent context pack | later | tooling |
| #21 | Search for humans | later | tooling, content |
| #22 | Narrative growth | later | content |
| #23 | Weekly digest view | later | content, tooling |
| #24 | Multi-writer promotion | later | process |
| #31 | Red Hat Support case search/analysis | later | process, tooling |
| #33 | PostToolUse usage logging | later | tooling, infrastructure |
| #36 | Python-based doctor rewrite | later | infrastructure |

## Issue body format

```
[What this is and why it matters -- context needed to understand
the problem before acting]

### Scope
- [Concrete deliverables, bulleted]
- [What's NOT in scope, if ambiguous]

### Acceptance criteria
- [ ] [Verifiable checkbox]
- [ ] [Another one]

### Starting points
- `path/to/relevant/file` -- [why it matters]
- [Link to related spec/issue if relevant]

---
*Migrated from enhancements.md (original #N)*
```

Optimized for both human and AI agent pickup: explicit scope prevents
drift, acceptance criteria give a verifiable "done" signal, starting
points eliminate the "where do I begin" problem.

## Enhancements.md new format

```markdown
# Hub enhancements backlog

- **What this is:** the hub's improvement direction and rationale.
  Each item links to a GitHub issue for scope, acceptance criteria,
  and implementation detail.
- **How items graduate:** when picked up, the issue tracks the work;
  on completion, the item moves to enhancements-complete.md with a
  completion date and outcome summary.
- **Owner:** Peter Double -- **Last groomed:** YYYY-MM-DD

---

## Next (active candidates)

**[#N Title](link).** 2-3 sentences on *why* this matters and what
it connects to strategically. The issue holds the how.

## Later (data-gated or low urgency)

Same format.

## Someday

Items too speculative for issues. No links, just the idea and why
it's parked.

## Deliberately not doing

Conscious design decisions. No issues, pure narrative context.
```

Key changes from current format:
- Each actionable item is a short narrative paragraph with an issue link
- Technical detail (upstream reviews, recommended shapes) lives in the
  issue body
- Someday and Deliberately not doing unchanged
- `#N` identifiers are real GitHub issue numbers

## Implementation order

1. Create the 7 new labels (2 priority + 5 theme)
2. Create 14 issues with full detail, labels applied
3. Rewrite enhancements.md using the assigned issue numbers
4. Commit and push
