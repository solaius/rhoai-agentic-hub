---
type: fact
description: "The hub can now WRITE to Jira, but only via hub.jira-triage and only labels (atomic add), comments, close and approve - every other Jira skill is still read-only"
timestamp: 2026-07-11
status: current
---
Until 2026-07-11 every Jira skill in the hub was read-only, and
`hublib/jira.py`'s write methods (`update_issue`, `add_comment`,
`transition_issue`, `create_issue`) were dead code carried for a future
backlog item. The Jira operating batch (#29) turned writes on, narrowly.

**The exact surface, and it is deliberately small:**
- `hub.jira-triage` is the ONLY skill that writes to Jira.
- It may: add a label, post a comment, fire the `close` transition, fire the
  `approve` transition.
- It may NOT: assign, edit arbitrary fields, or create issues. `create_issue`
  is still dead code. `<release>-committed` labels are never written.
- Every mutation is gated line by line. Transitions are resolved during the
  scan and rendered separately at the gate, so the gate names what will fire
  and an unresolvable transition is rejected rather than half-applied.

**Label writes are atomic adds, not read-modify-write.** The design
originally had triage round-trip the labels array: the report carried
`current_labels`, and apply would PUT `existing + new` via `update_issue`. A
review caught this as CRITICAL before ship: Jira's PUT replaces the labels
array wholesale, so a stale or hand-edited decisions file would DELETE
labels that existed in Jira, and could smuggle in the protected
`-committed` label. Fixed by switching to Jira's atomic add operation:
`JiraClient.add_label` PUTs `{"update": {"labels": [{"add": l}]}}`, which
cannot remove anything. `update_issue` and `create_issue` now have ZERO
call sites repo-wide. `current_labels` survives only as an ADVISORY hint for
a "label already present, skip it" check in `hublib/triage.py`'s
`plan_decisions` and can never build a write payload.

**Do not generalize.** `hub.jira-sweep`, `hub.jira-sync` and `hub.jira-hygiene`
still say "read-only against Jira" in their descriptions and that is still
true. A future agent reading one of those must not conclude the hub is
read-only overall, nor that the write door is open wider than these four
actions.

See [[fact-hub-design-decisions]]. Spec:
[/docs/specs/2026-07-11-jira-operating-batch-design.md](/docs/specs/2026-07-11-jira-operating-batch-design.md).
