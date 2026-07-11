---
name: hub.standup
description: PM standup brief -- Jira + Slack + Gemini + AI news (pm-toolkit port). A personal daily brief pulling from Jira (PM portfolio issues updated/blocked/approaching deadlines/comments needing response), Slack (messages to you + mentions, classified as Needs Response vs FYI), Gemini Meeting Notes (action items from Google Drive), and AI news (enterprise AI + Red Hat mentions). Output is structured priorities (Urgent/Important/Monitor). Use when the user says "standup", "daily brief", "morning brief", "what needs my attention", or "pm standup". Complements hub_status.py (hub-centric brief) -- this is system-centric.
---

# hub.standup

Input: none (runs against current day). Optional: a date override.

1. PRE-FLIGHT: verify MCP servers are available.
   - `python scripts/hub_jira.py --check` -- Jira connectivity. Failure
     -> stop and point at `bash scripts/doctor.sh check` (section 4).
   - Confirm Slack MCP is connected (try `mcp__slack__whoami`). Failure
     -> warn "Slack section will be empty" and continue.
   - Confirm Google Workspace MCP is connected (try
     `mcp__google-workspace__list_calendars`). Failure -> warn "Gemini
     Notes section will be empty" and continue.

2. GATHER DATA -- run all independent queries in parallel where possible.

   **Jira (4 queries via hub_jira.py):**
   The "Product Manager" field is a custom field. On first run, confirm
   the exact JQL field name with the user (it may be `cf[NNNNN]` or the
   display name "Product Manager" depending on the Jira instance). Cache
   the confirmed name for future runs.

   a. PM issues updated in last 24h:
      `"Product Manager" = currentUser() AND updated >= -1d`
   b. PM issues blocked:
      `"Product Manager" = currentUser() AND status = Blocked`
   c. PM deadlines approaching (7 days):
      `"Product Manager" = currentUser() AND due <= 7d AND due >= 0d`
   d. For each issue from (a), scan the `comment` field for comments from
      the last 24h that contain questions, action requests, or review
      requests from OTHER users (not you). Classify each as needing a
      response.

   Run these via `python scripts/hub_jira.py` with appropriate JQL. The
   CLI returns JSON; parse it for the output tables.

   **Slack (2 queries via MCP):**
   a. Messages to you:
      `mcp__slack__search_messages` with query `to:me after:<yesterday>`
      (limit 20, sort by timestamp)
   b. Mentions:
      `mcp__slack__search_messages` with query `@<username> after:<yesterday>`
      (limit 20, sort by timestamp). Get `<username>` from the `whoami`
      result in pre-flight.

   Classify each message:
   - **Needs Response** -- contains a question, action request, review
     request, or deadline
   - **FYI** -- informational, no action needed
   Deduplicate across the two queries (same message may appear in both).

   **Gemini Meeting Notes (GDrive + doc read):**
   a. Search Google Drive:
      `mcp__google-workspace__search_drive_files` with query
      `"Notes by Gemini"`, ordered by `modifiedTime desc`, page_size 10
   b. For each result from the last 7 days, read the doc:
      `mcp__google-workspace__get_doc_as_markdown` with the document ID
   c. Scan each doc for sections titled "Action items", "Next steps",
      "Follow-ups", "Decisions and action items" (case-insensitive)
   d. Within those sections, look for items mentioning the user's name
      near keywords: "will", "should", "needs to", "action:", "TODO",
      "follow up", "owns"
   e. Deduplicate across recurring meeting notes -- if the same meeting
      title appears multiple times, keep only the most recent

   **AI News Pulse (web search):**
   a. `WebSearch` query: "enterprise AI platform news last 24 hours"
      -- take top 3 results
   b. `WebSearch` query: "Red Hat AI news" -- take top 2 results
   c. Deduplicate and pick the 3 most relevant headlines

3. FORMAT OUTPUT using this template:

   ```
   ## PM Daily Brief -- <date>

   ### Jira (Last 24h)

   **Issues Updated (PM Portfolio):**
   | Key | Summary | Status | Last Change |
   |-----|---------|--------|-------------|
   (table rows from query a)

   **Blocked Items:**
   | Key | Summary | Blocked Since |
   |-----|---------|---------------|
   (table rows from query b, or "None" if empty)

   **Approaching Deadlines (7d):**
   | Key | Summary | Due Date |
   |-----|---------|----------|
   (table rows from query c, or "None" if empty)

   **Comments Needing Response:**
   | Key | From | Comment Summary | Suggested Action |
   |-----|------|-----------------|------------------|
   (table rows from query d, or "None" if empty)

   ### Slack Highlights

   **Needs Response:**
   | From | Channel | Summary | Urgency |
   |------|---------|---------|---------|
   (classified messages)

   **FYI:**
   | From | Channel | Summary |
   |------|---------|---------|
   (classified messages)

   ### Meeting Action Items (Gemini Notes)
   | Action Item | Meeting | Date | Status |
   |-------------|---------|------|--------|
   (extracted items)

   ### Quick AI Pulse
   1. <headline 1> -- <one-line summary>
   2. <headline 2> -- <one-line summary>
   3. <headline 3> -- <one-line summary>

   ### Today's Priorities
   1. **Urgent** -- <items needing immediate attention>
   2. **Important** -- <items to make progress on today>
   3. **Monitor** -- <items to keep an eye on>

   ### Suggested Actions
   | Action | Priority | Source |
   |--------|----------|--------|
   (consolidated from all sections above; meeting action items
   auto-included as "Important")
   ```

   Omit any section that has no data (e.g., if Slack is unavailable, skip
   the Slack section entirely rather than showing empty tables).

4. PRIORITIES LOGIC: build the Urgent/Important/Monitor buckets:
   - **Urgent:** blocked Jira issues, Slack messages classified as Needs
     Response with a deadline, comments needing response on issues due
     within 3 days
   - **Important:** approaching deadlines (7d), Slack Needs Response
     without deadlines, meeting action items assigned to you
   - **Monitor:** updated issues with no action needed, FYI Slack
     messages, AI news items

5. FOOTER: end with:
   ```
   ---
   For a full hub picture, also run: `python scripts/hub_status.py`
   Want me to drill into any specific area or draft a reply?
   ```

This skill is READ-ONLY. It writes nothing to the repo, restricted/ or
otherwise. No gate, no index, no lint, no commit.

## Known gap

Issues in the user's feature areas that lack a "Product Manager" assignment
are invisible to this brief. A future improvement could cross-reference
against `features/features.yaml` JQL scopes and flag issues in those scopes
without a PM.
