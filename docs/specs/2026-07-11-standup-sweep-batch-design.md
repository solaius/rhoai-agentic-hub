# Standup + sweep batch design

**Enhancements:** #28 (PM standup brief) + #3 (feature staleness sweep)
**Date:** 2026-07-11
**Owner:** Peter Double

## Summary

Three new prompt-only skills: `hub.standup` (daily brief across
Jira/Slack/Gemini Notes/AI News), `hub.weekly-plan` (weekly superset adding
calendar analysis and carry-over), and `hub.sweep` (per-feature staleness
audit with live source cross-referencing). All follow the hub's skill
conventions: SKILL.md instruction files, gated writes, standard post-write
sequence.

## Decisions

1. **All three are prompt-only skills** (SKILL.md, no Python CLI backbone).
   The agent orchestrates MCP tool calls and reads entries directly. This
   matches pm-toolkit's proven pattern and avoids splitting logic between
   Python and prompts.

2. **Standup ports as a pair** (`hub.standup` + `hub.weekly-plan`), matching
   pm-toolkit's `pm-standup` + `weekly-plan` structure.

3. **Sweep is standalone** (`hub.sweep`), not a mode on hub.intake or
   hub.reindex. Clean separation: intake adds content, sweep audits it.

4. **Jira queries use "Product Manager" field**, not reporter or assignee.
   The RFE creator sets a different reporter, and assignment typically goes
   to engineers. The PM custom field is the real ownership signal. Known gap:
   strats without the PM field set are invisible -- noted as a future
   improvement.

5. **Sweep flags and proposes, does not rewrite content.** It is an auditor,
   not an author. The user decides what to update after reviewing findings.

## Skill 1: hub.standup

**Location:** `.claude/skills/hub.standup/SKILL.md`

**Purpose:** Personal daily brief -- what needs your attention today across
all systems. Complements `hub_status.py` (#15), which is hub-centric (stale
entries, open questions, CI state). The standup is system-centric.

### Data sources

All independent queries run in parallel.

| Source | Tool | Query |
|---|---|---|
| Jira -- PM issues updated | `python scripts/hub_jira.py` | `"Product Manager" = currentUser() AND updated >= -1d` |
| Jira -- PM issues blocked | same | `"Product Manager" = currentUser() AND status = Blocked` |
| Jira -- PM deadlines | same | `"Product Manager" = currentUser() AND due <= 7d AND due >= 0d` |
| Jira -- comments needing response | agent scans comment fields | Questions/requests from others in last 24h |
| Slack -- messages to you | `mcp__slack__search_messages` | `to:me after:<yesterday>` (limit 20) |
| Slack -- mentions | `mcp__slack__search_messages` | `@<username> after:<yesterday>` (limit 20) |
| Gemini Notes | `search_drive_files` + `get_doc_as_markdown` | `"Notes by Gemini"`, last 10, scan for action items |
| AI News | `WebSearch` | Enterprise AI + Red Hat AI, last 24h |

### Jira client usage

The skill uses `hub_jira.py` (the hub's async Jira CLI, backed by
`hublib/jira.py`). Credentials come from `restricted/.env` via
`hublib/shellenv.py`. The "Product Manager" field may require `cf[NNNNN]`
syntax depending on the Jira instance -- the skill notes this and asks the
user to confirm on first run.

### Slack message classification

Each Slack message is classified by the agent as:
- **Needs Response** -- question, action request, review request, deadline
- **FYI** -- informational, no action needed

### Gemini Notes action item extraction

The agent searches for sections titled "Action items", "Next steps",
"Follow-ups", "Decisions and action items" and looks for the user's name
near keywords like "will", "should", "needs to", "action:", "TODO",
"follow up", "owns". Deduplicates across recurring meeting notes (keeps
most recent).

### Output template

```
## PM Daily Brief -- <date>

### Jira (Last 24h)
- PM issues updated -- table (key, summary, status, last change)
- Blocked items
- Approaching deadlines (7d)
- Comments needing response (with suggested action)

### Slack Highlights
- Needs Response (from, channel, summary, urgency)
- FYI

### Meeting Action Items (Gemini Notes)
- Table: action item, meeting, date, status

### Quick AI Pulse
- 3 enterprise AI headlines + Red Hat mentions

### Today's Priorities
1. **Urgent** -- immediate attention needed
2. **Important** -- make progress today
3. **Monitor** -- keep an eye on

### Suggested Actions
- Table: action, priority, source

---
For a full hub picture, also run: `python scripts/hub_status.py`
```

### Known gap

Issues in the user's feature areas that lack a "Product Manager" assignment
are invisible. A future improvement could cross-reference against
`features.yaml` JQL scopes and flag issues in those scopes without a PM.

## Skill 2: hub.weekly-plan

**Location:** `.claude/skills/hub.weekly-plan/SKILL.md`

**Purpose:** Weekly planning superset of the standup. Adds Google Calendar
analysis (meeting prep, conflicts, focus blocks) and carry-over tracking
from the previous week's plan.

### Additional data sources

| Source | Tool | Query |
|---|---|---|
| Google Calendar | `mcp__google-workspace__get_events` | Mon 00:00 to Fri 23:59, up to 50 events |
| Previous week's plan | `Read` tool | Last `weekly-plan-<date>.md` in output dir |

### Time window changes

All standup queries widen: Jira `updated >= -7d`, deadlines out to 14d,
Slack and Gemini Notes from 7d ago.

### Output file

Written to a user-specified directory as `weekly-plan-<YYYY-MM-DD>.md`
(Monday of current week). The directory is resolved from conversation
context or `PM_OUTPUT_DIR` env var. Uses `- [ ]` / `- [x]` checkbox format
for use as a living checklist.

### Carry-over logic

Reads previous plan file. Unchecked `- [ ]` items under Urgent and Carried
Over sections move to this week's Carried Over. Completed `- [x]` items
are dropped.

### Output template

```
## Weekly Plan -- <week of date>

### Key Dates
- Milestones, releases, PTO

### Urgent
#### New This Week
- [ ] items from Jira/Slack/meetings
#### Carried Over (Still Open)
- [ ] unchecked items from last week's plan

### Important
- [ ] items needing progress this week

### Monitor
- [ ] items to watch

### Jira Status (7d)
- PM issues updated / blocked / approaching deadlines

### Slack Highlights (7d)
- Needs Response / FYI

### Meeting Action Items (Gemini Notes, 7d)

### Meetings to Prepare For
- Non-routine meetings needing active prep

### Conflicts & Recommendations
- Overlapping meetings, which to attend vs skip

### Suggested Focus Blocks
- 90+ min calendar gaps mapped to specific tasks

### Quick AI Pulse
- 3 headlines
```

## Skill 3: hub.sweep

**Location:** `.claude/skills/hub.sweep/SKILL.md`

**Purpose:** Per-feature staleness audit. Combines date-arithmetic checks
(what `stale_rows()` already does) with live source cross-referencing
(checking whether the thing an entry points to has changed). Presents
findings through the gate.

### Invocation

`sweep <feature-id>` (e.g., `sweep mcp-gateway`) or `sweep --all`.

### Phase 1 -- Date-arithmetic staleness (hub-local)

The agent reads the target feature's `knowledge/` directory and checks
every entry:
- `review_after` date passed (any type)
- `timestamp` + type default exceeded (per `conventions/staleness.yaml`:
  profiles 30d, facts 90d)
- `status: superseded` entries skipped

This covers gaps in current `stale_rows()`: reference, decision, and person
entries get checked too. The agent uses `Glob` to list `*.md` files in the
feature's `knowledge/` directory, then `Read` on each to parse frontmatter
(type, timestamp, review_after, status, resource, source).

### Phase 2 -- Live source cross-referencing (API calls)

For each entry with a `resource:` or `source:` field, the agent checks the
live source:

| Source type | Detection | Check | Tool |
|---|---|---|---|
| Jira issue | URL contains `issues.redhat.com` | Status, last updated, resolution | `python scripts/hub_jira.py` |
| Google Doc | URL contains `docs.google.com` | Last modified date | `mcp__google-workspace__get_drive_file_permissions` |
| GitHub repo/issue/PR | URL contains `github.com` | Last commit, issue state | `gh` CLI |
| Slack permalink | URL contains `slack.com/archives` | Skip (messages don't change) | -- |

### What gets flagged

- Entry says a Jira issue is "In Progress" but it moved to "Done" or "Closed"
- Entry's timestamp is 90+ days old and the linked GDoc was updated since
- Entry references a GitHub PR that merged (fact may need updating)
- Entry has `review_after` in the past
- Entry has no `resource:`/`source:` and is older than the type default

### Phase 3 -- Gated findings

Findings grouped by feature, one entry per line:

```
sweep findings for mcp-gateway (7 entries checked, 3 flagged):

1. ref-mcplo-design-doc.md -- GDoc updated 2026-07-08, entry timestamp 2026-06-15
   -> suggest: update timestamp, review content for changes
2. fact-registry-tp-scope.md -- Jira RHAISTRAT-1234 moved to Done (was In Progress)
   -> suggest: mark superseded or update status
3. decision-api-versioning.md -- review_after 2026-07-01 passed
   -> suggest: review and bump review_after or mark superseded

Apply updates? [review each / skip all]
```

### Accepted update actions

For each accepted finding, the agent:
- Updates the entry's `timestamp` to today
- Bumps `review_after` if present
- Updates `status` if the source shows a state change
- Marks `superseded` with `superseded_by` if the user provides a replacement

### Post-write sequence (standard)

`python scripts/hub_index.py` -> `python scripts/hub_lint.py` (0 errors)
-> commit with explicit pathspecs.

### git-crypt awareness

Since #14 shipped, `restricted/` is git-crypt encrypted and tracked. If
the sweep runs with `--all` or targets a feature that has restricted
knowledge entries, locked (encrypted) files must be skipped silently --
the agent checks for binary/non-UTF-8 content before parsing frontmatter.
The linter already does this (`_is_git_crypt_locked()` in `hublib/schema.py`).

### Scope boundary

The sweep flags and proposes -- it does not rewrite entry descriptions or
content. If a fact's description is wrong because Jira moved to Done, the
agent flags it and the user decides what to write.

## Enhancements.md updates

On completion:
- #28 moves to Done with skill locations and the PM-field decision noted
- #3 moves to Done with skill location noted
- Both get log lines in `memory/log.md`

## Testing

No pytest-able code (all prompt-only skills). Validation is acceptance runs:
- **Standup:** run once, verify all 4 sources return data, output matches template
- **Weekly-plan:** run once, verify calendar + carry-over sections populate
- **Sweep:** run against one feature with known stale entries, verify findings
  are accurate and the gate works
