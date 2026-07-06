---
name: hub.consolidate
description: Sweep memory/.scratch/ (Claude auto-memory) plus the current session for durable items, dedupe against the tracked store, and promote through the inline gate - batch approve/edit/reject with an explicit public-vs-restricted call per item. Use at session end when scratch is non-empty, when the user says "consolidate memory", or after fact-heavy sessions.
---

# hub.consolidate

1. Read every file in memory/.scratch/ (Claude auto-memory format). Add any
   durable items from the current session not yet captured.
2. Dedupe against the tracked store (memory/index.md, profiles/, facts/):
   drop items the store already knows; mark items that CONTRADICT the store.
3. Classify each survivor: profile update | new memory fact | knowledge entry
   (which feature) | preference/feedback | RESTRICTED | discard.
4. Present a numbered batch:
   `N. [class] <target-path> — <proposed description> [public|restricted]`
   Conflicts render as: `N. CONFLICT — scratch: "X" vs store: "Y" — which wins?`
   The user may approve all, pick numbers, edit any item, or reject.
   NEVER auto-resolve a conflict.
5. Apply approved items exactly as hub.capture step 4 does (profile edits with
   ## History, new typed files, restricted routing). Conflict resolutions:
   the losing entry gets `status: superseded` + `superseded_by: <winner path>`.
6. One log.md line per applied item under today's heading.
7. Regenerate and verify: `python scripts/hub_index.py` then
   `python scripts/hub_lint.py` (must report 0 errors).
8. Delete processed scratch files — scratch is a per-machine cache; the
   tracked store is now authoritative. Keep a file only if the user says
   "later".
9. Single commit: `git add -A && git commit -m "mem: consolidate — <n> items"`
   then `git push`.
10. Report: promoted / rejected / conflicts resolved, plus anything now listed
    in /views/stale-facts.md.
