# Strategy document conventions

`features/<id>/strategy/strategy.md` is the feature's ONE living strategy
document — the synthesis a PM plans from. Evidence stays in `knowledge/`
and `research/`; this document cites, it never restates at length.
Producer: `hub.strategy` (gated). Hand-edits are allowed (it is a
document, not a generated file); the next refresh reconciles them and
records the reconciliation in `## History`.

## Shape

ONE file per feature: `strategy/strategy.md`. Current-state, rewritten in
place on refresh (the profile pattern) — never a dated series; the dated
record lives in `research/` and `knowledge/` decisions. Other strategy
artifacts (RFE roadmaps, outcome write-ups) may sit alongside it under
`strategy/`, but `strategy.md` is the entry point and must stand alone.

## Frontmatter

`title` ("<Feature> — strategy") · `description` (one line — feeds the
indexes) · `timestamp` (date of last rewrite) · `status: current` ·
`review_after` (default +60 days — hub.sweep flags staleness) · `source`
(generator note: inputs + date). Linted as warnings only, like research
docs — strategy documents never fail the build.

## The eight sections (fixed order, fixed names)

| # | section | contract |
|---|---|---|
| 1 | `## The brief` | ≤10 lines. What this is, the one-sentence bet, where it stands today, next milestone. The owner's 60-second re-entry. |
| 2 | `## What` | Product shape by release train (table: release → scope → status) + boundaries: what this feature is NOT, with routing to its `related:` siblings. |
| 3 | `## Why` | The problem and the bet stated plainly: jobs served (jtbd/persona links where they exist), market position (wedge vs behind, from research), why now. |
| 4 | `## Where we stand` | Decisions to date (dated, linked), delivery state, in-flight work. |
| 5 | `## Gaps & risks` | Open `question-` entries + research risks + tensions, each with one why-it-matters line. The honest section. |
| 6 | `## Jira map` | Coverage table (strategy element → keys → status), then `### Candidate jiras`: gap → one-line problem statement → suggested project, each ready to hand to `/rfe.create`. Keys/type/status only from Jira; ALL prose in the hub's own words (unauthenticated-probe rule — never probe-withheld text). |
| 7 | `## Watchlist` | Dated external triggers that would change this strategy (upstream merges, freezes, competitor moves), each with "if it fires → what changes". |
| 8 | `## History` | Profile-style dated entries, newest first; every refresh appends one (date, what changed, why, source). Never deleted. |

## Register & rules

- PM working document (owner decision, 2026-07-16): dense, hub-context
  assumed, optimized for the owner's planning and re-entry — not an
  outsider pitch. Public-repo discipline still applies in full.
- Every load-bearing claim links its hub source (leading-slash form).
- Target length: The brief ≤10 lines; the whole document 2–4 pages.
- No customer names, no deal context, ever (restricted-lint enforced).
- Refresh = rewrite the body in place + append one `## History` entry.

## Producers & consumers

- Producer: [hub.strategy](/docs/skills.md). Offered as a follow-up by
  `hub.intake` and `hub.research`; never auto-run.
- Consumers: `hub.sweep` (review_after staleness), `hub.research`
  (sibling standing context), the marketplace review quartet
  (scope/architecture/feasibility/testability reviews), `/rfe.create`
  (candidate jiras).
