---
name: hub.strategy
description: Synthesize or refresh a feature's living strategy document (features/<id>/strategy/strategy.md) from its knowledge, research series, and Jira scope - the WHAT/WHY, gaps and risks, Jira coverage map plus candidate jiras, and watchlist - through the inline gate. Use when the user says "write the strategy for <feature>", "generate the strategy doc", "create the strategy", "refresh the strategy", or after hub.intake / hub.research offer it. One living doc per feature, rewritten in place - never a series.
---

# hub.strategy

Input: a feature id (features/features.yaml). Contract:
/conventions/strategy.md — ONE living document, eight fixed sections, PM
working register, rewritten in place with a ## History entry per refresh.
Spec: /docs/specs/2026-07-16-hub-strategy-skill-design.md.

1. RESOLVE: feature id → features/<id>/strategy/strategy.md. No home in
   features.yaml → offer hub.intake (research needs a home), stop there
   if declined. The file already exists ⇒ this is a REFRESH run.
2. PRECONDITIONS: knowledge/index.md must exist — none → hand off to
   hub.intake and stop. Empty research/ → warn that Why/market will be
   thin, offer hub.research first; proceed only on the user's explicit
   OK. No jira: block or work/jira-snapshot.yaml → offer hub.jira-sweep;
   proceeding means the Jira map names the missing scope as its first
   gap.
3. CONTEXT LOAD (read, in order): knowledge/index.md and every
   decision-/question-/fact- entry in the partition; research/
   00-executive-summary.md, then each lens doc; work/jira-snapshot.yaml
   and the partition's Jira ref- entries; memory/profiles/roadmap.md and
   memory/profiles/strategy.md; each related: sibling's overview fact
   (features.yaml). A missing input shrinks the document, never sinks
   the run — name it in Gaps & risks.
4. DRAFT in the session scratchpad per the /conventions/strategy.md
   section contract — no repo writes. Register: PM working doc (dense,
   hub-context assumed; The brief is the owner's 60-second re-entry).
   Every load-bearing claim cites its hub source (leading-slash link).
   PUBLIC repo: no customer names or deal context; Jira keys/type/status
   only, all prose your own words — NEVER probe-withheld text. Candidate
   jiras: one line each — gap → problem statement → suggested project
   (RHAIRFE/RHAISTRAT) — written to hand straight to /rfe.create.
5. GATE: show The brief inline plus one write line —
   `features/<id>/strategy/strategy.md: <description> [new|update]` —
   full document on request. REFRESH runs show a per-section
   what-changed summary (unchanged/updated/new) instead of the full doc,
   plus the proposed History line. Nothing touches the repo before OK.
6. On OK: write the file, run `python scripts/hub_index.py`, then
   `python scripts/hub_lint.py` (0 errors — fix the document, not the
   scripts). Commit: stage the doc plus regenerated indexes/views
   explicitly, NEVER `git add -A` (shared checkout, see
   fact-concurrent-session-git-hygiene); check
   `git diff --cached --stat`, then commit with pathspecs:
   `git commit -m "strat(<id>): strategy doc <new|refresh>" -- <those paths>`
   && `git push`.
7. OFFER, never auto-run: /rfe.create for candidate jiras the user
   approves; the marketplace review quartet (/scope-review,
   /architecture-review, /feasibility-review, /testability-review)
   against the document or its anchor STRAT; hub.publish only on
   explicit ask (publishing is a separate disclosure decision).
