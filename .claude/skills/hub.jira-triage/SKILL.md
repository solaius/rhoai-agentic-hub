---
name: hub.jira-triage
description: Run the RFE triage ceremony for one component - scan its open Feature Requests, flag staleness, suggest actions, review them in a browser report, then batch-apply the decisions back to Jira through an inline gate. Use when the user says "triage the RFEs for <component>", "run a triage pass", "what RFEs need attention", or on a periodic triage cadence. WRITES TO JIRA (adds labels, posts comments, and fires the close and approve transitions) - every mutation is gated line by line and nothing fires before approval. It cannot assign, edit fields, or create issues.
---

# hub.jira-triage

Input: a component id (its `jira:` scope in components.yaml supplies the JQL).
Spec: [/docs/specs/2026-07-11-jira-operating-batch-design.md](/docs/specs/2026-07-11-jira-operating-batch-design.md).

This is the ONLY skill in the hub with a Jira write surface. Every other
hub.jira-* skill is read-only, and that is deliberate: keep it that way.

1. PRE-FLIGHT. `python scripts/hub_jira.py --check`. On failure, stop and
   point at `bash scripts/doctor.sh check` (section 4). No retry loop.
   Confirm `restricted/` exists. If it does not, STOP: the report carries live
   Jira summaries and this repo is PUBLIC. Never fall back to a tracked path.
2. SCOPE. `python scripts/hub_triage.py --scan <component> --out <scratch>` echoes
   the composed JQL (the component's stored scope narrowed to open Feature
   Requests) before it fetches. Read it back to the human and confirm.
   Unknown component or no stored scope: exit 2, offer hub.jira-sweep.
3. REVIEW. Move the report to
   `restricted/components/<component>/work/triage-<date>.html` and tell the human
   to open it. Keep `rows-<component>.json` in scratch: the apply step needs it.
   The human clicks through the rows and hits Export Decisions, which downloads
   `triage-decisions-<date>.json`. Ask where it landed.
4. GATE. `python scripts/hub_triage.py --plan <decisions.json> --rows <rows.json>`
   prints the batch table: TRANSITIONS first and separate (they are the
   destructive ones), then LABELS, COMMENTS, SKIPPED, REJECTED. Show it
   verbatim. Approve/edit/reject per line. NOTHING touches Jira before OK.
   A rejected line is never silently dropped: it is shown with its reason.
   Rejections are usually real (an unsupported action, or a workflow with no
   matching close transition). Do not try to route around one.
5. APPLY. `python scripts/hub_triage.py --apply <decisions.json>
   --rows <rows.json> --component <component> --out <scratch>`. Labels land, then
   comments, then transitions. Report applied/skipped/rejected/errors and name
   every transition that fired.
6. RECORD. Copy the proposed `triage-log-<component>.yaml` to
   `components/<component>/work/triage-log.yaml`. It carries no Jira prose by
   design: never add summaries or comment bodies to it.
   `python scripts/hub_index.py` then `python scripts/hub_lint.py` (0 errors).
7. COMMIT. Stage explicitly, NEVER `git add -A` (shared checkout; see
   fact-concurrent-session-git-hygiene). Check `git diff --cached --stat`, then:
   `git commit -m "triage(<component>): <n> issues, <m> applied" -- components/<component>/work/triage-log.yaml <regenerated indexes>`
   and `git push`.

NEVER: write the HTML report into the tracked tree; put a Jira summary or
comment body into triage-log.yaml; apply a decisions file without showing the
gate table first; retry a rejected transition by picking a different one.
