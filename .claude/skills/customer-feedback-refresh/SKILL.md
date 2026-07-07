---
name: customer-feedback-refresh
description: Use when reviewing or refreshing the customer interest tracker for accuracy, staleness, or completeness. Also use when the user says "refresh the tracker", "check for stale items", "review action items", "update tracker status", or wants to audit the tracker against current project state. All tracker content is restricted (NDA customer data) — this skill only ever reads/writes under restricted/.
---

# Customer Feedback Refresh

Reviews the customer interest tracker for staleness, completeness, and accuracy against current sources.

## Tracker Location

`restricted/features/platform/work/customer-tracker/customer-interest-tracker.html`

Same file `customer-feedback-ingest` writes. If it doesn't exist yet on this
machine, tell the user and point them at `customer-feedback-ingest` to create
it from a first source — there is nothing to refresh yet.

## Refresh Checks

### 1. Action Item Staleness

Review every row in the Open Action Items table:
- Flag items with no status change in 2+ weeks
- Check if the action has been completed elsewhere (email, Jira, Slack)
- Suggest status updates or removal for resolved items
- Add new action items discovered from recent sources

### 2. Source Coverage

Compare files in `restricted/features/platform/work/customer-tracker/transcripts/`
against meetings listed in the tracker:
- Flag transcriptions not yet ingested
- Flag tracker entries with no source transcription

### 3. Status Accuracy

For each customer, verify status tag matches current engagement:
- `EVAL` — no active PoC or production plans
- `ENGAGED` — active discussions, no formal PoC
- `PoC` — proof of concept planned or in progress
- `PROD` — targeting or in production

Cross-reference with recent emails (Google Workspace MCP) or Jira tickets if available.

### 4. Interest Accuracy

Check tracker interest levels against product roadmap changes:
- If a feature shipped (moved to GA), note that in the detail section
- If a customer's requirement was addressed by a new release, update the detail notes
- Check `memory/profiles/roadmap.md` and the relevant feature's
  `features/<f>/knowledge/index.md` (mcp-gateway, mcp-registry, mcp-ecosystem,
  agent-registry, etc. — whichever this customer's interests map to) for
  newly captured decisions or facts that affect a tracked customer's interest
  areas. This replaces the old repo's single `docs/knowledge-registry.md`
  monolith check — the hub spreads that same living-knowledge-base role
  across `memory/` and each feature's `knowledge/`.

### 5. Summary Card Accuracy

Verify:
- Active Customers count matches actual rows in the Interest Matrix
- Meetings Tracked count matches total meetings listed across all customer detail rows
- Targeting Production count matches customers with `PROD` tag
- Most Requested feature is still accurate

### 6. Cross-Customer Theme Accuracy

Check the Cross-Customer Themes table:
- Customer lists match actual interest markers in the matrix
- Product status tags reflect current release state (check
  `memory/profiles/roadmap.md` for the current dev-preview/GA timeline rather
  than assuming the version numbers named in the tracker are still current)
- New themes that span 2+ customers should be added

## Process

1. **Read the full tracker HTML**
2. **Run each check** above, collecting findings
3. **Present findings** to the user as a summary:
   - Stale items (action items, status tags)
   - Missing sources (transcriptions not ingested)
   - Accuracy issues (counts, themes, product status)
4. **Apply updates** only after user approval — same direct-write discipline
   as `customer-feedback-ingest` (this is restricted/ content, not a
   `hub.capture` write; still confirm before writing)
5. **Report** what was changed
6. **Knowledge-capture handoff** — if a refresh finding is really a
   non-customer-specific product fact worth keeping (a roadmap date that
   moved, a feature that shipped), offer `hub.capture` for that item into the
   relevant feature's knowledge or `memory/profiles/roadmap.md`, generalized
   away from the specific customer/meeting it was noticed in

## Related skills

- `customer-feedback-ingest` — the write path this skill audits.
- `customer-feedback-sync` — run after a refresh that changed data, so the
  shared Google Sheet reflects the cleaned-up tracker.
