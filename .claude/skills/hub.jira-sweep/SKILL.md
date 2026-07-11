---
name: hub.jira-sweep
description: Sweep Jira into the hub for one feature — conversational scope discovery (JQL stored in features.yaml), a curated public snapshot under <feature>/work/, and gated ref- entries for strategic issues (default Outcome/Feature types). Use when the user says "sweep jira for <feature>", "pull the jiras for <feature>", "set up jira tracking for <feature>", or when filed Jira links deserve field ingestion. Read-only against Jira; every repo write is gated.
---

# hub.jira-sweep

Input: a feature id (features/features.yaml) + optional JQL/scope hints.
Spec: /docs/specs/2026-07-09-jira-hub-skills-design.md. Read-only against
Jira — never comment, transition, or edit issues.

1. PRE-FLIGHT: `python scripts/hub_jira.py --check`. Failure → stop and
   point at `bash scripts/doctor.sh check` (section 4) — no retry loops.
2. SCOPE: a `jira:` block on the feature in features/features.yaml → use
   it. None → scope discovery: ask ONCE for hints (project? component?
   labels? a known issue key?), then iterate
   `python scripts/hub_jira.py --try-jql '<candidate>'` showing counts +
   sample rows until the user approves the JQL. The approved block
   (`jql:` + optional `ref_types:`, default [Outcome, Feature]) becomes a
   features.yaml edit proposed AT THE GATE (step 5) — nothing is written
   now. Component↔label mapping is messy by nature; JQL is the one stored
   scope language.
3. FETCH: `python scripts/hub_jira.py --sweep <feature> [--jql '<jql>']
   --out <scratchpad>/jira`. The CLI writes the proposed snapshot
   (summaries already redacted by the unauthenticated-probe rule) and
   candidates-<feature>.yaml (the strategic tier). Heed its WARN on
   result-count swings — a drifted scope needs the user's eyes on the JQL
   before anything is gated.
4. DRAFT (scratch only, no repo writes): one ref- entry per candidate the
   feature does not already track (match on resource: URL) — filename
   `ref-<key-lower>-<slug>.md`, `type: reference`, canonical `resource:`
   (/conventions/uris.md), one-line description written for a reader
   deciding whether to open it, body 2–4 sentences (what it is, status,
   why it matters to this feature). An existing ref- for a candidate →
   propose an update only if the issue materially changed. NEVER copy a
   probe-redacted summary into any tracked file — a withheld summary
   means Jira itself does not serve that text anonymously. Candidates
   marked public: false in candidates-<feature>.yaml are exactly those —
   draft their refs from the key and your own words only.
5. GATE: one batch table — every proposed write, one line:
   `path: description [new|update]` — the snapshot
   (features/<id>/work/jira-snapshot.yaml, redacted count called out),
   each ref-, and the features.yaml scope edit when new/changed. Full
   content on request. Approve/edit/reject per line; nothing touches the
   repo before OK.
6. On OK: write the approved files, `python scripts/hub_index.py`, then
   `python scripts/hub_lint.py` (0 errors — fix the written content,
   never the scripts). Commit: stage the sweep's writes plus regenerated
   indexes/views explicitly, NEVER `git add -A` (shared checkout, see
   fact-concurrent-session-git-hygiene); check `git diff --cached --stat`,
   then commit with pathspecs:
   `git commit -m "jira(<feature>): sweep - <n> issues, <m> refs" -- <those paths>`
   && `git push`.
7. Offer follow-ups, never auto-run: a `hub.jira-sync` cadence, or ref-
   entries for non-strategic issues the user names (hub.capture path).
