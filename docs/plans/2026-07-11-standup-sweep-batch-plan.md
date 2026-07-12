# Standup + Sweep Batch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship three prompt-only skills: `hub.standup` (daily Jira/Slack/
Gemini Notes/AI News brief), `hub.weekly-plan` (weekly superset with
calendar + carry-over), and `hub.sweep` (per-feature staleness audit with
live source cross-referencing). All SKILL.md instruction files, no Python
CLI backbone.

**Architecture:** Each skill is a `.claude/skills/<name>/SKILL.md`
instruction file. The agent follows the steps at runtime, calling MCP tools
(Slack, Google Workspace, WebSearch) and CLI commands (`hub_jira.py`) as
directed. `hub.standup` and `hub.weekly-plan` are read-only (no repo
writes). `hub.sweep` writes entry updates through the standard gate +
post-write sequence.

**Tech Stack:** SKILL.md (prompt instructions). MCP tools: `mcp__slack__*`,
`mcp__google-workspace__*`, `WebSearch`. CLI: `python scripts/hub_jira.py`.
No new Python code. No new dependencies.

## Global Constraints

- Precondition. This must print `ready` before Task 1:
  `cd F:/code/rh/rhoai-agentic-hub && python scripts/hub_lint.py >/dev/null && echo ready`
- Repo root (Windows + Git Bash): `F:\code\rh\rhoai-agentic-hub`.
  Use `python`, never `python3`.
- **This repo is PUBLIC.** No customer names, no deal context, no dollar
  figures in any tracked file.
- **No em dashes** in any output: code, comments, docs, skill prose, commit
  messages. Use commas, colons, parentheses, or spaced hyphens.
- **No LLM-provider credentials** anywhere.
- New dependencies: none.
- All file writes: `encoding="utf-8", newline="\n"`.
- After every task: `python scripts/hub_lint.py` reports **0 errors** and the
  warning count has not increased over the pre-task baseline (currently **95**).
- Never hand-edit generated files (`features/index.md`, `*/index.md`,
  `views/*`, `memory/index.md`). Run `python scripts/hub_index.py`.
- `AGENTS.md` has a 150-line CI budget. Three new skill rows must fit.
- Links in markdown use the leading-slash repo-root form.
- Commit with **explicit pathspecs**, never `git add -A` (shared checkout; see
  `fact-concurrent-session-git-hygiene`). Check `git diff --cached --stat`
  before every commit. Another session may be working in this clone.
- Every commit message ends with the Co-Authored-By trailer for the model
  that writes the commit.
- Spec: [/docs/specs/2026-07-11-standup-sweep-batch-design.md](/docs/specs/2026-07-11-standup-sweep-batch-design.md).

---

### Task 1: Create `hub.standup` skill

**Files:**
- Create: `.claude/skills/hub.standup/SKILL.md`

**Interfaces:**
- Consumes: `python scripts/hub_jira.py` (Jira CLI), Slack MCP tools,
  Google Workspace MCP tools, `WebSearch` tool
- Produces: daily brief output in the conversation (read-only, no repo writes)

- [ ] **Step 1: Create the skill directory**

```bash
mkdir -p .claude/skills/hub.standup
```

- [ ] **Step 2: Write the SKILL.md**

Create `.claude/skills/hub.standup/SKILL.md` with the following exact content:

```markdown
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

### Known gap

Issues in the user's feature areas that lack a "Product Manager" assignment
are invisible to this brief. A future improvement could cross-reference
against `features/features.yaml` JQL scopes and flag issues in those scopes
without a PM.
```

- [ ] **Step 3: Verify lint is clean**

Run: `python scripts/hub_lint.py`
Expected: 0 errors, warnings <= 95

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/hub.standup/SKILL.md
git diff --cached --stat
git commit -m "feat(#28): add hub.standup skill -- daily PM brief

Prompt-only skill pulling from Jira (Product Manager field),
Slack, Gemini Meeting Notes, and AI news. Read-only, no repo
writes. Complements hub_status.py (hub-centric) with a
system-centric daily brief.

Co-Authored-By: <model> <noreply@anthropic.com>" -- .claude/skills/hub.standup/SKILL.md
```

---

### Task 2: Create `hub.weekly-plan` skill

**Files:**
- Create: `.claude/skills/hub.weekly-plan/SKILL.md`

**Interfaces:**
- Consumes: same tools as `hub.standup`, plus Google Calendar MCP and
  previous week's plan file
- Produces: a `weekly-plan-<YYYY-MM-DD>.md` file in a user-specified
  directory (write is outside the repo, no gate needed)

- [ ] **Step 1: Create the skill directory**

```bash
mkdir -p .claude/skills/hub.weekly-plan
```

- [ ] **Step 2: Write the SKILL.md**

Create `.claude/skills/hub.weekly-plan/SKILL.md` with the following exact content:

```markdown
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

### Known gap

Same "Product Manager" field gap as hub.standup. Additionally, carry-over
parsing depends on the `- [ ]` / `- [x]` format -- if the user edits the
plan file and changes the format, carry-over may miss items.
```

- [ ] **Step 3: Verify lint is clean**

Run: `python scripts/hub_lint.py`
Expected: 0 errors, warnings <= 95

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/hub.weekly-plan/SKILL.md
git diff --cached --stat
git commit -m "feat(#28): add hub.weekly-plan skill -- weekly planning brief

Prompt-only skill extending hub.standup with Google Calendar
analysis (meeting prep, conflicts, focus blocks) and carry-over
tracking from previous week. Writes a checklist file outside the
repo.

Co-Authored-By: <model> <noreply@anthropic.com>" -- .claude/skills/hub.weekly-plan/SKILL.md
```

---

### Task 3: Create `hub.sweep` skill

**Files:**
- Create: `.claude/skills/hub.sweep/SKILL.md`

**Interfaces:**
- Consumes: `python scripts/hub_jira.py` (Jira CLI), Google Workspace MCP,
  `gh` CLI, `python scripts/hub_index.py`, `python scripts/hub_lint.py`,
  `conventions/staleness.yaml`
- Produces: updated knowledge entries through the gate (tracked repo writes)

- [ ] **Step 1: Create the skill directory**

```bash
mkdir -p .claude/skills/hub.sweep
```

- [ ] **Step 2: Write the SKILL.md**

Create `.claude/skills/hub.sweep/SKILL.md` with the following exact content:

```markdown
---
name: hub.sweep
description: Feature staleness sweep -- per-feature "what's outdated?" audit. Combines date-arithmetic staleness (timestamp + type defaults from conventions/staleness.yaml) with live source cross-referencing (Jira status, GDoc last-modified, GitHub activity). Flags stale entries and proposes updates through the gate. Use when the user says "sweep <feature>", "what's stale in <feature>", "check for outdated entries", "staleness check", or "what changed since I last touched <feature>". Generalizes the customer-feedback-refresh pattern to all knowledge entries.
---

# hub.sweep

Input: a feature id (from features/features.yaml), or `--all` to sweep
every feature.

1. PRE-FLIGHT:
   - Validate the feature id against `features/features.yaml`. If `--all`,
     load all feature ids from that file.
   - Read `conventions/staleness.yaml` for the type defaults:
     `profile_default_days` (30) and `fact_default_days` (90).
   - `python scripts/hub_jira.py --check` -- needed for Jira
     cross-referencing. Failure -> warn "Jira checks will be skipped" and
     continue (date-arithmetic still works without Jira).
   - Confirm Google Workspace MCP is connected (try
     `mcp__google-workspace__list_calendars`). Failure -> warn "GDoc
     checks will be skipped" and continue.

2. PHASE 1 -- DATE-ARITHMETIC STALENESS (hub-local, no API calls):

   For each target feature, use `Glob` to list all `*.md` files in
   `features/<id>/knowledge/`. For `--all`, also check
   `narrative/knowledge/` and `memory/facts/` and `memory/profiles/`.

   Read each file and parse its YAML frontmatter. Skip files that:
   - Cannot be read as UTF-8 (git-crypt locked files)
   - Have `status: superseded`
   - Are `index.md` (generated files)

   Check each entry against staleness rules:
   a. If `review_after` is set and that date < today -> FLAG as
      "review overdue (review_after <date>)"
   b. If `type` is `profile` and `timestamp` + 30 days < today -> FLAG as
      "profile stale (last updated <date>, 30d default)"
   c. If `type` is one of `fact`, `reference`, `decision`, `person`,
      `question`, `qa`, `jtbd` and `timestamp` + 90 days < today -> FLAG
      as "entry stale (last updated <date>, 90d default)"

   Collect: `{path, type, timestamp, review_after, resource, source,
   status, description, staleness_reason}` for each flagged entry.

3. PHASE 2 -- LIVE SOURCE CROSS-REFERENCING (API calls):

   For each entry (flagged or not) that has a `resource:` or `source:`
   field containing a URL, check the live source:

   **Jira (URL contains `issues.redhat.com`):**
   Extract the issue key from the URL. Run
   `python scripts/hub_jira.py --try-jql 'key = <KEY>' --fields status,updated,resolution`
   to get current status.
   - If the entry describes a status (e.g., "In Progress" in the
     description or a `status:` frontmatter field) and Jira shows a
     different status -> FLAG as "Jira status changed (<old> -> <new>)"
   - If the Jira issue was updated more recently than the entry's
     timestamp -> FLAG as "Jira issue updated since entry
     (issue: <date>, entry: <date>)"
   - If the issue has a resolution (Done, Won't Do, etc.) and the entry
     does not reflect this -> FLAG as "Jira issue resolved (<resolution>)"

   **Google Docs (URL contains `docs.google.com`):**
   Extract the document ID from the URL. Run
   `mcp__google-workspace__get_drive_file_permissions` with the file ID
   to get `modifiedTime`.
   - If the doc was modified after the entry's timestamp -> FLAG as
     "GDoc updated since entry (doc: <date>, entry: <date>)"

   **GitHub (URL contains `github.com`):**
   Determine if it's a repo, issue, or PR URL.
   - Repo: `gh api repos/<owner>/<repo> --jq .pushed_at` for last push
   - Issue: `gh api repos/<owner>/<repo>/issues/<num> --jq '.state,.updated_at'`
   - PR: `gh api repos/<owner>/<repo>/pulls/<num> --jq '.state,.merged_at,.updated_at'`
   Flag if the source changed state or was updated since the entry.

   **Slack (URL contains `slack.com/archives`):**
   Skip -- Slack messages do not change after posting.

   **Unknown URLs:** skip, do not attempt to fetch.

   Merge phase 2 flags into the phase 1 results. An entry can have
   multiple flags (both date-stale and source-changed).

4. PHASE 3 -- PRESENT FINDINGS (gated):

   Group findings by feature. Present a summary:

   ```
   sweep findings for <feature> (<n> entries checked, <m> flagged):

   1. <filename> -- <staleness_reason>
      -> suggest: <suggested action>
   2. <filename> -- <staleness_reason>
      -> suggest: <suggested action>
   ...

   Apply updates? [review each / skip all]
   ```

   Suggested actions by flag type:
   - "review overdue" -> "review content and bump review_after, or mark
     superseded"
   - "entry stale (date)" -> "review content and update timestamp, or
     mark superseded"
   - "Jira status changed" -> "update entry to reflect new status, or
     mark superseded if the issue is resolved"
   - "GDoc updated" -> "review GDoc changes and update timestamp"
   - "GitHub state changed" -> "update entry to reflect new state"

   If no entries are flagged, report:
   ```
   sweep for <feature>: <n> entries checked, all current. Nothing to do.
   ```

5. APPLY UPDATES (only after user approval, entry by entry):

   For each accepted finding, the user chooses the action. The agent then:
   a. Updates the entry's `timestamp` to today
   b. Bumps `review_after` if present (add 90 days from today, or ask
      the user for a specific date)
   c. Updates `status` fields if the source shows a state change
   d. Marks `status: superseded` with `superseded_by: <path>` if the user
      provides a replacement entry path
   e. Does NOT rewrite entry descriptions or body content -- the agent
      flags, the user decides what to write. If the user wants content
      changes, they dictate the new text.

6. POST-WRITE SEQUENCE (standard, only if any entries were updated):

   a. Append to `memory/log.md` under today's heading:
      `- **Update** -- sweep(<feature>): <n> entries refreshed`
   b. Run `python scripts/hub_index.py`
   c. Run `python scripts/hub_lint.py` -- 0 errors required; fix the
      updated entries (not the scripts) if it reports errors.
   d. Commit with explicit paths, NEVER `git add -A`:
      `git add <updated entries> memory/log.md memory/index.md
      features/index.md "features/*/index.md"
      "features/*/knowledge/index.md" narrative/index.md
      narrative/knowledge/index.md views/`
      Check `git diff --cached --stat` for anything the sweep did not
      write, then commit WITH PATHSPECS:
      `git commit -m "sweep(<feature>): refresh <n> stale entries" -- <those paths>`

7. KNOWLEDGE-CAPTURE HANDOFF: if the sweep discovers a non-entry-specific
   product fact (e.g., a Jira issue moved to Done reveals a feature
   shipped), offer `hub.capture` for that item into the relevant feature's
   knowledge or `memory/profiles/roadmap.md`.

### Scope boundary

The sweep flags and proposes -- it does not rewrite entry content. If a
fact's description is wrong because Jira moved to Done, the agent flags it
and the user decides what to write. This is an auditor, not an author.

### git-crypt awareness

Since #14 shipped, `restricted/` is git-crypt encrypted and tracked. If
the sweep targets a feature with restricted knowledge entries, locked
(encrypted) files are skipped silently -- check for binary/non-UTF-8
content before parsing frontmatter.

### Known gap

The sweep checks entries that have a `resource:` or `source:` URL. Entries
without any URL can only be checked by date-arithmetic. A future
improvement could attempt to match entry descriptions against known Jira
issues or GDocs by title/keyword search.
```

- [ ] **Step 3: Verify lint is clean**

Run: `python scripts/hub_lint.py`
Expected: 0 errors, warnings <= 95

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/hub.sweep/SKILL.md
git diff --cached --stat
git commit -m "feat(#3): add hub.sweep skill -- feature staleness audit

Prompt-only skill combining date-arithmetic staleness checks with
live source cross-referencing (Jira, GDocs, GitHub). Flags stale
entries and proposes updates through the standard gate.

Co-Authored-By: <model> <noreply@anthropic.com>" -- .claude/skills/hub.sweep/SKILL.md
```

---

### Task 4: Register skills in AGENTS.md and update enhancements.md

**Files:**
- Modify: `AGENTS.md` (add 3 rows to the skills table)
- Modify: `docs/enhancements.md` (#28 and #3 move to Done)

**Interfaces:**
- Consumes: the three SKILL.md files from Tasks 1-3
- Produces: updated AGENTS.md and enhancements.md

- [ ] **Step 1: Read current AGENTS.md**

Read `AGENTS.md` and find the skills table. Identify where to insert the
three new rows. They should go in the hub skills section (after
`hub.refresh-site` and before the first-party content skills section).

- [ ] **Step 2: Add skill rows to AGENTS.md**

Add these three rows to the hub skills table, maintaining alphabetical
order within the hub.* group:

```
| hub.standup | daily PM brief -- Jira (PM portfolio) + Slack + Gemini Notes + AI news, structured as Urgent/Important/Monitor |
| hub.sweep | per-feature staleness audit -- date-arithmetic + live source cross-referencing (Jira/GDocs/GitHub), gated updates |
| hub.weekly-plan | weekly planning superset of hub.standup -- adds Google Calendar analysis, carry-over tracking, checklist file |
```

- [ ] **Step 3: Update enhancements.md**

Move #28 and #3 to the Done section at the bottom of `docs/enhancements.md`.
Remove their rows from the priority table. Add Done entries:

For #28:
```
- **#28 PM standup brief + weekly plan** -- shipped <date>: `hub.standup`
  (daily brief from Jira/Slack/Gemini Notes/AI News using the "Product
  Manager" JQL field) and `hub.weekly-plan` (weekly superset with Google
  Calendar analysis and carry-over tracking). Both are prompt-only skills;
  hub.standup is read-only, hub.weekly-plan writes a checklist file outside
  the repo. Spec:
  [/docs/specs/2026-07-11-standup-sweep-batch-design.md](/docs/specs/2026-07-11-standup-sweep-batch-design.md).
```

For #3:
```
- **#3 Feature staleness sweep** -- shipped <date>: `hub.sweep` skill
  combining date-arithmetic staleness (conventions/staleness.yaml defaults)
  with live source cross-referencing (Jira status, GDoc last-modified,
  GitHub activity). Flags stale entries and proposes updates through the
  standard gate. Prompt-only skill, no Python backbone. Spec:
  [/docs/specs/2026-07-11-standup-sweep-batch-design.md](/docs/specs/2026-07-11-standup-sweep-batch-design.md).
```

- [ ] **Step 4: Append to memory/log.md**

Under today's `## 2026-07-11` heading (or create it if absent), add:
```
- **Creation** -- standup + sweep batch shipped (#28, #3): hub.standup (daily PM brief), hub.weekly-plan (weekly planning), hub.sweep (feature staleness audit). All prompt-only skills.
```

- [ ] **Step 5: Regenerate indexes**

Run: `python scripts/hub_index.py`

- [ ] **Step 6: Verify lint is clean**

Run: `python scripts/hub_lint.py`
Expected: 0 errors, warnings <= 95

- [ ] **Step 7: Commit**

```bash
git add AGENTS.md docs/enhancements.md memory/log.md memory/index.md features/index.md "features/*/index.md" "features/*/knowledge/index.md" narrative/index.md narrative/knowledge/index.md views/
git diff --cached --stat
git commit -m "docs(#28,#3): register standup/sweep skills, move to Done

AGENTS.md gains 3 skill rows. Enhancements #28 and #3 move to Done.
Log line added.

Co-Authored-By: <model> <noreply@anthropic.com>" -- AGENTS.md docs/enhancements.md memory/log.md memory/index.md features/index.md "features/*/index.md" "features/*/knowledge/index.md" narrative/index.md narrative/knowledge/index.md views/
```

---

### Task 5: Acceptance runs (manual, not automatable)

These validate the skills work end-to-end with live systems. Each requires
human interaction at the gate.

- [ ] **Run 1: hub.standup** -- invoke `hub.standup`. Verify:
  - Jira section populated (PM field query returns results)
  - Slack section populated (messages/mentions appear)
  - Gemini Notes section populated (action items extracted)
  - AI News section populated (3 headlines)
  - Priorities section synthesizes across all sources
  - If the "Product Manager" field name needs adjustment, note the correct
    JQL field name and update the SKILL.md

- [ ] **Run 2: hub.weekly-plan** -- invoke `hub.weekly-plan`. Verify:
  - All standup sections appear (widened to 7d)
  - Calendar section populated (meetings, conflicts, focus blocks)
  - Carry-over section present (empty on first run, note this)
  - Plan file written to the specified directory
  - Checkbox format is correct (`- [ ]`)

- [ ] **Run 3: hub.sweep** -- invoke `sweep <feature>` for a feature with
  known stale entries (check `python scripts/hub_status.py` for candidates).
  Verify:
  - Phase 1 flags entries by date-arithmetic
  - Phase 2 cross-references live sources (at least one Jira or GDoc check)
  - Findings are presented in the expected format
  - Gate works: approve one update, reject another
  - Post-write sequence runs (index, lint, commit)
  - Log line appended
