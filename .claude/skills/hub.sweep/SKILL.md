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

   RELATED-FEATURE DRIFT (hub-local): if the feature has a `related:`
   list in `features/features.yaml` (its boundary siblings), find the
   target's newest entry timestamp, then list sibling entries
   (knowledge/ + research/) with timestamps newer than it. Carry these
   into phase 3 (PRESENT FINDINGS) as an informational "boundary drift
   candidates" block --
   sibling activity the target's entries may not reflect. Candidates
   only, never auto-flagged: no update is proposed unless the user picks
   one up.

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
