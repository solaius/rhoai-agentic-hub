# AGENTS.md — agent guide to rhoai-agentic-hub

This repo is a PM knowledge hub operated by humans and agents together. It is
**PUBLIC** — treat every tracked write as world-readable.

## Session start (always)
1. Read `/memory/index.md` — current state, active work, recent changes.
2. If `restricted/memory/index.md` exists locally, read it too (NDA context).
3. Only then start the task. Load anything deeper lazily via the indexes.

## Map
| path | holds |
|---|---|
| `features/<id>/` | all content for one feature area — identical skeleton: `knowledge/ research/ strategy/ enablement/ work/` |
| `features/features.yaml` | the routing table (which features exist) |
| `memory/` | working context: profiles (current state), facts, log |
| `conventions/` | THE RULEBOOK — read before writing any content |
| `views/` | generated cross-cutting indexes (decisions, questions, stale, jira, people) |
| `publish/manifest.yaml` | the ONLY path to the public site |
| `restricted/` | gitignored local mirror for NDA content |
| `docs/` | the guides: architecture, setup, working-here, memory, skills, publishing, tooling, history |

## Writing rules (summary — details in /conventions/)
- Filing = two questions: which feature (features.yaml) × which type
  (/conventions/type-vocabulary.md). Working context vs domain knowledge
  boundary: /conventions/memory.md.
- Every entry: frontmatter with `type`, one-line `description`, `timestamp`.
  Filenames: `decision- fact- ref- person- question-` prefixes.
- NEVER hand-edit generated files (features/index.md, */index.md, views/*,
  memory/index.md) — run `python scripts/hub_index.py`.
- NEVER write to the tracked memory store without the inline gate — use the
  hub.capture / hub.consolidate skills.
- NEVER add publishable output outside `publish/manifest.yaml` flow.
- Links: leading-slash repo-root form. Dangling links allowed.
- Restricted/NDA-adjacent content → `restricted/…` (same shapes), never tracked.

## Capture protocol (memory goals B → A)
Durable item surfaces mid-session (decision, date change, preference,
link)? → fire `hub.capture` immediately. At session end, if work produced
scratch/log noise → offer `hub.consolidate`. Roadmap/strategy/status changes
are PROFILE updates (update in place + ## History), not new files.

## Skills
| skill | use for |
|---|---|
| hub.capture | file one durable item now (gated, committed) |
| hub.consolidate | scratch sweep → gated batch promotion → reindex |
| hub.file | intake a doc/URL/transcript as a typed entry |
| hub.reindex | regenerate all indexes/views + lint |
| hub.doctor | machine setup / health check |
| hub.publish | add/update a publish manifest entry (gated) |
| hub.migrate | bring content over from ai-asset-registry, reshaped |

First-party content skills (ported from ai-asset-registry, adapted to hub conventions):
| skill | use for |
|---|---|
| presentation-create | build Red Hat-branded HTML decks/pages under a feature's enablement/ (ships via hub.publish) |
| blog-create | multi-agent Red Hat blog drafting + review pipeline under a feature's enablement/ (final draft ships via Workfront, not hub.publish) |
| blog-mockup | quick Red Hat-branded HTML preview of any blog content (lightweight alternative to blog-create's full pipeline; ships via hub.publish only on request) |
| customer-feedback-ingest | add/update a customer in the restricted interest tracker from a transcript, email, Jira ticket, or pasted notes |
| customer-feedback-refresh | audit the tracker for staleness, missing sources, and accuracy |
| customer-feedback-sync | diff the tracker against the shared Google Sheet and push approved changes via rhai-tracker MCP (gated) |

Shared skills (rfe.*, strat.*, assess-rfe…) come from the ODH marketplace —
see `.claude/settings.json`.

## Verification
`python -m pytest scripts/tests -v` · `python scripts/hub_lint.py` ·
`python scripts/hub_index.py --check` — CI (`validate.yml`) runs all three.
