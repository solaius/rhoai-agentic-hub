---
name: hub.weekly-plan
description: Weekly planning brief -- superset of hub.standup with Google Calendar analysis and carry-over tracking. Adds meeting prep recommendations, conflict detection, suggested focus blocks, and a living checklist carried forward week to week. Output is a weekly-plan-<date>.md file. Use when the user says "weekly plan", "plan my week", "weekly brief", or "what's my week look like". Companion to hub.standup (daily).
---

# hub.weekly-plan

Input: optional output directory for the plan file. Resolved in order:
(1) user provides a path, (2) conversation context, (3) `PM_OUTPUT_DIR`
env var, (4) ask the user. The plan file is written OUTSIDE the repo --
never under the rhoai-agentic-hub tree.

1. PRE-FLIGHT: same as hub.standup step 1 (Jira, Slack, Google Workspace
   checks), plus confirm Google Calendar access via
   `mcp__google-workspace__get_events` with a short range.

2. RESOLVE OUTPUT DIR: determine where to write the plan file. If no
   previous plan exists in the directory, note this (no carry-over for
   the first run).

3. GATHER DATA -- all hub.standup queries, widened to 7 days, plus:

   **Jira (widened):**
   a. `"Product Manager" = currentUser() AND updated >= -7d`
   b. `"Product Manager" = currentUser() AND status = Blocked`
   c. `"Product Manager" = currentUser() AND due <= 14d AND due >= 0d`
   d. Comment scan: last 7 days instead of 24h

   **Slack (widened):**
   a. `to:me after:<7 days ago>` (limit 50)
   b. `@<username> after:<7 days ago>` (limit 50)

   **Gemini Notes (widened):** search with page_size 20, scan docs from
   last 14 days (to catch action items from late last week).

   **AI News:** same as hub.standup (last 24h -- weekly doesn't need a
   week of news).

   **Google Calendar:**
   `mcp__google-workspace__get_events` with `time_min` = Monday 00:00
   and `time_max` = Friday 23:59 of the current week, max_results 50,
   detailed=true (includes attendees, description, location).

   **Previous week's plan:**
   Read the most recent `weekly-plan-*.md` file in the output directory.
   Parse it for unchecked `- [ ]` items under "Urgent" and "Carried Over"
   sections. These become this week's "Carried Over (Still Open)" items.
   Completed `- [x]` items are dropped.

4. CALENDAR ANALYSIS:

   a. **Meetings to Prepare For:** filter events that are NOT routine
      (recurring daily standup, 1:1s that happen every week). Flag
      meetings with: external attendees, "review" or "demo" in the title,
      or 3+ attendees. For each, note what prep is needed.

   b. **Conflicts and Recommendations:** find overlapping events. For
      each conflict, recommend which to attend vs skip/delegate, based on
      attendee count, whether you're the organizer, and whether it's a
      recurring meeting.

   c. **Suggested Focus Blocks:** find calendar gaps of 90+ minutes
      between events (Mon-Fri, 9am-6pm). Map each gap to a specific task
      from the Urgent or Important buckets.

5. FORMAT OUTPUT using this template, written to
   `<output-dir>/weekly-plan-<YYYY-MM-DD>.md` where the date is Monday
   of the current week:

   ```
   ## Weekly Plan -- week of <date>

   ### Key Dates
   - <milestones, releases, PTO from calendar or Jira>

   ### Urgent

   #### New This Week
   - [ ] <items from Jira/Slack/meetings>

   #### Carried Over (Still Open)
   - [ ] <unchecked items from last week's plan>

   ### Important
   - [ ] <items needing progress this week>

   ### Monitor
   - [ ] <items to watch>

   ### Jira Status (7d)

   **Issues Updated (PM Portfolio):**
   | Key | Summary | Status | Last Change |
   |-----|---------|--------|-------------|

   **Blocked Items:**
   | Key | Summary | Blocked Since |
   |-----|---------|---------------|

   **Approaching Deadlines (14d):**
   | Key | Summary | Due Date |
   |-----|---------|----------|

   ### Slack Highlights (7d)

   **Needs Response:**
   | From | Channel | Summary | Urgency |
   |------|---------|---------|---------|

   **FYI:**
   | From | Channel | Summary |
   |------|---------|---------|

   ### Meeting Action Items (Gemini Notes, 7d)
   | Action Item | Meeting | Date | Status |
   |-------------|---------|------|--------|

   ### Meetings to Prepare For
   | Meeting | Date/Time | Why Prep Needed | Prep Notes |
   |---------|-----------|-----------------|------------|

   ### Conflicts and Recommendations
   | Time | Conflict | Recommendation |
   |------|----------|----------------|

   ### Suggested Focus Blocks
   | Time | Duration | Suggested Task |
   |------|----------|----------------|

   ### Quick AI Pulse
   1. <headline> -- <summary>
   2. <headline> -- <summary>
   3. <headline> -- <summary>
   ```

   Omit any section with no data.

6. PRIORITIES LOGIC: same as hub.standup step 4, plus:
   - Carried-over items that were Urgent last week stay Urgent
   - Meeting prep items are Important
   - Calendar conflicts are Urgent if both meetings are today

7. WRITE THE FILE: write to `<output-dir>/weekly-plan-<YYYY-MM-DD>.md`.
   This file is OUTSIDE the repo -- no gate, no index, no lint, no commit
   against the hub. Confirm the path with the user before writing.

8. FOOTER: end with:
   ```
   ---
   For a full hub picture, also run: `python scripts/hub_status.py`
   ```

## Known gap

Same "Product Manager" field gap as hub.standup. Additionally, carry-over
parsing depends on the `- [ ]` / `- [x]` format -- if the user edits the
plan file and changes the format, carry-over may miss items.
