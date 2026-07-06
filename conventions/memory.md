# Memory conventions

## Boundary rule
`memory/` = **working context**: current state, preferences, what changed,
what's in flight. `features/<f>/knowledge/` = **domain knowledge**: what a
colleague would look up. "The 3.5 date moved" → `memory/profiles/roadmap.md`.
"How the gateway does authz" → knowledge entry.

## Store
- `index.md` — always-loaded tier, ≤200 lines (CI-enforced), GENERATED.
- `profiles/` — one file per volatile subject; **update in place**; move the
  old value into the file's `## History` section with date + source.
- `facts/` — append-oriented dated atoms; supersede, never delete.
- `log.md` — chronological trail, newest first, OKF format: `## YYYY-MM-DD`
  headings, entries starting `**Creation**` / `**Update**` / `**Deprecation**`.
  Rotates yearly to `log-archive/<year>.md`.
- `.scratch/` — gitignored; Claude auto-memory writes here natively; raw feed
  for consolidation; NOT part of the OKF bundle.

## The gate (all writes to the tracked store)
1. `hub.capture` (hot path): one item, one-line inline confirm, commit.
2. `hub.consolidate` (batch): sweep `.scratch/` + recent log → dedupe →
   classify each candidate as **profile update / new fact / knowledge entry /
   RESTRICTED / discard** → present batch for inline approve/edit/reject —
   every item gets an explicit public-vs-restricted call (this repo is
   PUBLIC) → apply → regenerate `memory/index.md` → clear scratch → one commit.
3. Conflicts (scratch contradicts a profile) are never auto-resolved: present
   both, the human picks, the loser is superseded.
4. Restricted items go to `restricted/memory/` (same shapes, local-only).
5. Restricted bar: $ figures and SKU/entitlement specifics, consent/legal
   process detail, customer-named risks or deals, and org-sensitive numbers
   (headcount, ratios) → restricted/. Partner/company names in
   public-partnership contexts are public.

## Staleness
`review_after` (per file) wins; otherwise [staleness.yaml](/conventions/staleness.yaml)
defaults apply. Overdue items appear in `views/stale-facts.md`.
