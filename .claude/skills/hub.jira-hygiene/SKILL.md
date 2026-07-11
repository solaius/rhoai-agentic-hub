---
name: hub.jira-hygiene
description: Audit one Jira issue against the hub's type-specific hygiene checklists (RHAIRFE Feature Request, RHAISTRAT Feature, maturity-chain DP/TP/GA, RHAIENG Epic) - naming, parent and clone links, Fix Version, Components, labels, refinement docs. Use when the user says "audit RHAISTRAT-1322", "is this jira well formed", "check the hygiene of <KEY>", or before promoting an RFE. Also answers "explain the jira hierarchy" (help mode). Read-only against Jira and writes nothing to the repo; it reports, it does not fix.
---

# hub.jira-hygiene

Input: one issue key (audit mode), or a question about the hierarchy (help mode).
Spec: [/docs/specs/2026-07-11-jira-operating-batch-design.md](/docs/specs/2026-07-11-jira-operating-batch-design.md).

1. PRE-FLIGHT. `python scripts/hub_jira.py --check`. On failure, stop and point
   at `bash scripts/doctor.sh check` (section 4). No retry loop.
2. FETCH. `python scripts/hub_jira.py --audit <KEY>`. Read the YAML dump. It is
   the only source of facts; do not fetch anything else, and do not guess at
   fields it does not carry.
3. JUDGE. Read `checklists.md` in this skill directory. Pick the checklist that
   matches the dump's `type`, and also apply the "All issues" checklist. Walk
   every line. A check you cannot evaluate from the dump is a Warning with the
   reason, never a Pass.
4. REPORT. One table, in chat, nothing written anywhere:
   `| Check | Pass/Fail/Warning | Detail |`
   Then prioritized fixes, most load-bearing first. Quote the issue's own text
   only in chat; never write it into the repo (this repo is PUBLIC).
5. HAND OFF. This skill does not fix. A fix is either the human in Jira, or a
   comment via hub.jira-triage (the only skill with a Jira write surface).
   Offer, never auto-run.

HELP MODE. If the input is a question rather than a key, answer from
`checklists.md` (hierarchy, lifecycle, link matrix, naming) without touching
Jira at all.
