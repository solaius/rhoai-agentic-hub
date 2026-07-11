---
name: hub.jira-sync
description: Refresh the hub against live Jira — re-run every stored feature scope, diff against the committed snapshots, watch each ref-'d and jtbd-linked issue key, and propose the consequences (snapshot refresh, ref- updates, jtbd status nudges) through the gate. Use when the user says "sync jira", "refresh the jira map", "what changed in jira", or periodically once sweeps exist. Read-only against Jira.
---

# hub.jira-sync

Input: optional feature id — default is every feature with a `jira:` block
in features/features.yaml. Spec:
/docs/specs/2026-07-09-jira-hub-skills-design.md.

1. PRE-FLIGHT: `python scripts/hub_jira.py --check`. Failure → stop and
   point at `bash scripts/doctor.sh check` (section 4).
2. DIFF: `python scripts/hub_jira.py --sync [<feature>] --out
   <scratchpad>/jira`. It reads committed snapshots, re-runs stored JQLs,
   and reports NEW / CHANGED / VANISHED per feature, plus WATCHED lines
   for every Jira key referenced by ref- resource: URLs or jtbd jira:
   lists outside the swept scopes — refs never silently rot. "sync: all
   quiet" → report that and stop; zero ceremony.
3. INTERPRET the diff into proposals (scratch only):
   - the refreshed snapshot per changed feature (the CLI already wrote
     the proposed file to --out);
   - ref- updates only where the change matters to the entry's prose or
     validity: resolved / closed / won't-fix → a status note in the body
     + a `review_after` bump. Routine status churn is snapshot-only —
     do not rewrite refs for it;
   - jtbd nudges: every key in a jtbd's `jira:` list resolved → propose
     `status: delivered` (the user rules; never automatic);
   - NEW arrivals whose type is in the feature's `ref_types` → ref-
     candidates drafted per hub.jira-sweep step 4;
   - VANISHED or unreachable WATCHED keys → flag the referencing entries
     for the user's ruling (deleted, moved, or permission change).
4. GATE: one batch table — `path: description [new|update]`;
   approve/edit/reject per line; nothing touches the repo before OK.
5. On OK: write, `python scripts/hub_index.py`, `python
   scripts/hub_lint.py` (0 errors). Commit: stage this run's writes plus
   regenerated indexes/views explicitly, NEVER `git add -A` (shared
   checkout, see fact-concurrent-session-git-hygiene); check
   `git diff --cached --stat`, then commit with pathspecs:
   `git commit -m "jira(sync): <features> - <summary>" -- <those paths>`
   && `git push`.
