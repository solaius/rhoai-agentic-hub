# Jira Operating Batch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the hub three Jira operating capabilities on top of the read-only
client that shipped with #2: audit an issue against type checklists (#30),
cross active Jira work against the competitive landscape (#27b), and run the RFE
triage ceremony with a gated write-back to Jira (#29).

**Architecture:** `hub_jira.py` gains a read-only `--audit` mode that dumps a
structured issue for the agent to judge against a prose checklist. `hub.research`
gains a `jira-gap` lens, which is prose plus a `jira:` block in the domain YAML
and no new code. `#29` adds `hublib/triage.py` (pure classification, transition
resolution, gated apply), `hublib/triage_html.py` (the self-contained report),
and `scripts/hub_triage.py` (the CLI). The CLI never writes into the repo; the
skill writes after the gate. Transitions are resolved during the scan so the
gate can name what will fire.

**Tech Stack:** Python 3.11+, httpx (async), PyYAML, pytest. No new dependencies.

## Global Constraints

- Precondition. This must print `ready` before Task 1:
  `cd /c/Users/peter/code/rh/rhoai-agentic-hub && python -m pytest scripts/tests -q >/dev/null && python scripts/hub_lint.py >/dev/null && echo ready`
- Repo root (Windows + Git Bash): `C:\Users\peter\code\rh\rhoai-agentic-hub`.
  Use `python`, never `python3`.
- **This repo is PUBLIC** (`solaius/rhoai-agentic-hub`, verified
  `"isPrivate": false`). No customer names, no deal context, no dollar figures,
  and **no verbatim Jira summaries or comment bodies in any tracked file**. The
  full-fidelity triage report goes to `restricted/` only.
- **No em dashes** in any output: code, comments, docs, skill prose, commit
  messages. Use commas, colons, parentheses, or spaced hyphens.
- **No LLM-provider credentials** anywhere. Nothing in this plan reads
  `ANTHROPIC_API_KEY`, `VERTEX_PROJECT`, or `AWS_REGION`.
- The Jira write surface is exactly: add label, post comment, `close`
  transition, `approve` transition. No assignment, no field edits, no issue
  creation. Anything else is rejected at the gate.
- New dependencies: none. `httpx`, `pyyaml`, `pytest` are already in
  `scripts/requirements.txt`.
- All file writes: `encoding="utf-8", newline="\n"`.
- No `pytest-asyncio`. Async tests wrap coroutines in a local
  `def run(coro): return asyncio.run(coro)` helper. Jira is mocked at the
  transport layer with `httpx.MockTransport`, injected via the existing
  `transport=` kwarg.
- After every task: `python scripts/hub_lint.py` reports **0 errors** and the
  warning count has not increased over the pre-task baseline (currently **81**).
- Never hand-edit generated files (`features/index.md`, `*/index.md`,
  `views/*`, `memory/index.md`). Run `python scripts/hub_index.py`.
- `AGENTS.md` has a 150-line CI budget. Two new skill rows must fit.
- Links in markdown use the leading-slash repo-root form.
- Commit with **explicit pathspecs**, never `git add -A` (shared checkout; see
  `fact-concurrent-session-git-hygiene`). Check `git diff --cached --stat`
  before every commit. Another session may be working in this clone.
- Every commit message ends with:
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`
- Spec: [/docs/specs/2026-07-11-jira-operating-batch-design.md](/docs/specs/2026-07-11-jira-operating-batch-design.md).
  Decision numbers referenced below are that spec's.

---

### Task 1: `hub_jira.py --audit` (read-only issue dump)

**Files:**
- Modify: `scripts/hub_jira.py` (docstring, `_audit`, argparse wiring)
- Test: `scripts/tests/test_hub_jira.py` (append)

**Interfaces:**
- Consumes: `hublib.jira.client_from_env`, `JiraClient.get_issue_with_links`,
  `hublib.jira.adf_to_text` (all existing).
- Produces: `hub_jira.main(["--audit", "<KEY>"])` prints a YAML dump of one
  issue to stdout and returns 0. Task 2's skill reads that stdout.

- [ ] **Step 1: Write the failing test**

Append to `scripts/tests/test_hub_jira.py`:

```python
def test_audit_is_a_mode(tmp_path):
    # --audit combined with another mode is rejected
    with pytest.raises(SystemExit):
        hub_jira.main(["--audit", "RHAIRFE-1", "--check"])


def test_audit_needs_no_out_dir(tmp_path, monkeypatch):
    # --audit is read-only and prints to stdout, so unlike --sweep/--sync
    # it must NOT require --out. Argparse must not reject it.
    calls = {}

    def fake_run(coro):
        coro.close()
        calls["ran"] = True
        return 0

    monkeypatch.setattr(hub_jira.asyncio, "run", fake_run)
    rc = hub_jira.main(["--audit", "RHAIRFE-1",
                        "--root", str(make_repo(tmp_path))])
    assert rc == 0
    assert calls["ran"] is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /c/Users/peter/code/rh/rhoai-agentic-hub && python -m pytest scripts/tests/test_hub_jira.py -v`
Expected: FAIL. `test_audit_is_a_mode` fails because argparse does not know
`--audit` (SystemExit is raised for the wrong reason, but
`test_audit_needs_no_out_dir` fails with
`error: unrecognized arguments: --audit RHAIRFE-1`).

- [ ] **Step 3: Implement**

In `scripts/hub_jira.py`, extend the module docstring's mode list (after the
`--check` line):

```
  --audit <KEY>                 read-only structured dump of one issue (hub.jira-hygiene)
```

Add this function immediately after `_try_jql`:

```python
async def _audit(key):
    """Read-only structured dump of one issue for hub.jira-hygiene to judge.

    Prints YAML, not prose. The skill applies the checklists; this only
    supplies the facts. Never writes anything, anywhere.
    """
    async with client_from_env() as client:
        issue = await client.get_issue_with_links(key)
        base = client.base_url
    f = issue.get("fields", {})
    links = []
    for link in f.get("issuelinks") or []:
        ltype = (link.get("type") or {})
        if link.get("outwardIssue"):
            other, direction = link["outwardIssue"], ltype.get("outward", "")
        elif link.get("inwardIssue"):
            other, direction = link["inwardIssue"], ltype.get("inward", "")
        else:
            continue
        of = other.get("fields", {})
        links.append({
            "direction": direction,
            "key": other.get("key"),
            "type": (of.get("issuetype") or {}).get("name"),
            "status": (of.get("status") or {}).get("name"),
        })
    dump = {
        "key": issue.get("key"),
        "url": f"{base}/browse/{issue.get('key')}",
        "type": (f.get("issuetype") or {}).get("name"),
        "status": (f.get("status") or {}).get("name"),
        "summary": f.get("summary", ""),
        "assignee": (f.get("assignee") or {}).get("displayName"),
        "priority": (f.get("priority") or {}).get("name"),
        "components": [c.get("name") for c in f.get("components") or []],
        "labels": list(f.get("labels") or []),
        "fix_versions": [v.get("name") for v in f.get("fixVersions") or []],
        "parent": (f.get("parent") or {}).get("key"),
        "links": links,
        "description": adf_to_text(f.get("description")),
    }
    print(yaml.safe_dump(dump, sort_keys=False, allow_unicode=True))
    return 0
```

`get_issue_with_links` does not request `fixVersions` or `parent` by default, so
widen the call. Replace the `async with client_from_env() as client:` block in
`_audit` above with the explicit field list:

```python
    fields = [
        "summary", "status", "assignee", "priority", "issuetype", "project",
        "issuelinks", "components", "labels", "created", "updated",
        "fixVersions", "parent", "description",
    ]
    async with client_from_env() as client:
        issue = await client.get_issue_with_links(key, fields=fields)
        base = client.base_url
```

In `main()`, add the argument after `--try-jql`:

```python
    ap.add_argument("--audit", metavar="KEY")
```

Extend the mode list and keep `--out` unrequired for audit:

```python
    modes = [bool(args.check), args.try_jql is not None, args.audit is not None,
             args.sweep is not None, args.sync is not None]
    if sum(modes) != 1:
        ap.error("pick exactly one mode: --check | --try-jql | --audit | "
                 "--sweep | --sync")
```

And dispatch it beside `--try-jql` (before the `out = Path(args.out)` line, which
must stay after the read-only modes so audit never needs `--out`):

```python
        if args.audit is not None:
            return asyncio.run(_audit(args.audit))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_hub_jira.py -v`
Expected: 7 PASS.

- [ ] **Step 5: Full suite + real-repo lint**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: all PASS, `0 error(s), 81 warning(s)`, `0 stale file(s)`.

- [ ] **Step 6: Commit**

```bash
git add scripts/hub_jira.py scripts/tests/test_hub_jira.py
git diff --cached --stat
git commit -m "feat(jira): --audit read-only issue dump for hub.jira-hygiene (#30)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: `hub.jira-hygiene` skill (#30, audit-only)

**Files:**
- Create: `.claude/skills/hub.jira-hygiene/SKILL.md`
- Create: `.claude/skills/hub.jira-hygiene/checklists.md`

**Interfaces:**
- Consumes: `python scripts/hub_jira.py --audit <KEY>` from Task 1.
- Produces: nothing other tasks depend on. This task is complete and shippable
  on its own: it closes #30.

No Create mode (spec decision 2 ruled out issue creation), so pm-toolkit's
missing `create_link` never needs writing. The skill reports; it does not fix.

- [ ] **Step 1: Write `checklists.md`**

Create `.claude/skills/hub.jira-hygiene/checklists.md`:

```markdown
# Jira hygiene checklists

Reference for hub.jira-hygiene. Adapted from pm-toolkit's
jira-hygiene-template.md. Judge the `--audit` dump against the checklist that
matches the issue's type. Report Pass / Fail / Warning per line, never guess.

## Hierarchy

RHAISTRAT Outcome
  -> RHAISTRAT Feature (`[Feat]` prefix)
       -> RHAIENG Epic
            -> Story / Task
RHAIRFE Feature Request is the intake form. It is cloned into a RHAISTRAT
Feature when it is accepted, and the two stay linked by a Cloners link.

## All issues

- Summary reads as a clear statement, not a fragment.
- Description is structured, not a single paragraph dump.
- Assignee, Priority and Status are set.

## RHAIRFE Feature Request

- Description carries the four sections: Problem Statement, Business Alignment,
  Proposed Solution, Acceptance Criteria.
- If accepted: an "is cloned by" link to a RHAISTRAT Feature.
- Labels do not include `<release>-committed` (that is set on the STRAT side).

## RHAISTRAT Feature (11 checks)

1. Summary starts with `[Feat]`.
2. Parent is a RHAISTRAT Outcome.
3. A Cloners link back to the originating RHAIRFE.
4. Blocks / Depends links present where the work has real ordering.
5. At least one child RHAIENG Epic.
6. A Documents link to a `[ccs]` doc task.
7. Fix Version set.
8. Components set.
9. Labels carry a maturity tag (`DP` / `TP` / `GA`) and a release tag
   (`<release>-candidate` or `<release>-committed`).
10. A Feature Refinement Doc link at the top of the description.
11. GA only: a Platform Refinement Review link.

## Maturity-chain features (DP / TP / GA)

- Stage suffix in the summary (`[DP]`, `TP`, `GA`).
- A Depends link to the prior stage's feature.

## RHAIENG Epic

- Parent is a RHAISTRAT Feature.
- Has child Stories or Tasks.
- `[design]` prefix for UX epics, `[ccs Epic]` for docs epics.

## House style

- Inclusive language.
- No em dashes.
```

- [ ] **Step 2: Write `SKILL.md`**

Create `.claude/skills/hub.jira-hygiene/SKILL.md`:

```markdown
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
```

- [ ] **Step 3: Verify the skill loads and the checklist is reachable**

Run: `python scripts/hub_lint.py && ls .claude/skills/hub.jira-hygiene/`
Expected: `0 error(s), 81 warning(s)`, and both `SKILL.md` and `checklists.md`
listed.

- [ ] **Step 4: Full suite**

Run: `python -m pytest scripts/tests -v && python scripts/hub_index.py --check`
Expected: all PASS, `0 stale file(s)`.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/hub.jira-hygiene/
git diff --cached --stat
git commit -m "feat(skill): hub.jira-hygiene, audit-only issue checklists (#30)

Read-only. Create mode ruled out by spec decision 2, so the create_link
method pm-toolkit references but never implements is not needed.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: `jira-gap` research lens (#27b)

**Files:**
- Modify: `.claude/skills/hub.research/SKILL.md` (lens list, brief assembly)
- Modify: `conventions/research.md` (the `lens` enum line)
- Modify: `.claude/skills/hub.research/domains/redhat-ai.yaml` (the reserved
  `jira:` block, currently commented out at the end of the file)

**Interfaces:**
- Consumes: `python scripts/hub_jira.py --try-jql '<jql>'` (existing) to fetch
  the active-work baseline. No new code.
- Produces: nothing other tasks depend on. Closes #27b.

- [ ] **Step 1: Fill the reserved `jira:` block**

In `.claude/skills/hub.research/domains/redhat-ai.yaml`, replace the commented
placeholder at the end of the file:

```yaml
# jira-gap (future, backlog #27b): a jira: block here
# (project/components/jql) will drive the gap-analysis lens - the Jira
# client it needs landed with #2 (2026-07-10, scripts/hublib/jira.py).
```

with the live block:

```yaml
# Drives the jira-gap lens (#27b, shipped 2026-07-11). This is the
# "what we are building" baseline that the landscape is crossed against.
# jql wins if set; otherwise project + components compose one.
jira:
  project: RHAISTRAT
  components: []
  jql: 'project = RHAISTRAT AND status in ("In Progress", "New", "To Do") AND issuetype in (Feature, Outcome) ORDER BY updated DESC'
```

- [ ] **Step 2: Promote the lens in `hub.research/SKILL.md`**

Find the lens list line (it currently ends with the FUTURE stub):

```
jira-gap (FUTURE - refuse politely; the Jira hub skills landed 2026-07-10, the lens itself ships with backlog #27b).
```

Replace with:

```
jira-gap (strategic alignment: cross active Jira work against the landscape, both directions, driven by the `jira:` block in `domains/*.yaml`).
```

In step 4 FAN OUT, the brief-assembly sentence currently carves out the
competitive lens only. Extend the carve-out so jira-gap also receives the
domain config:

```
Each brief: the step-2 context summary + the lens definition + (competitive and jira-gap only) the domain config from `domains/*.yaml`.
```

Add the lens body as a new subsection near the competitive lens description:

```markdown
JIRA-GAP LENS. Needs the domain's `jira:` block. Two directions, and the
second is the payload:

1. BASELINE. `python scripts/hub_jira.py --try-jql '<the domain jql>'` gives
   the active work. This is "what we are building". Read-only.
2. DIRECTION A, active work vs landscape. For each active Feature or Outcome,
   find the related industry developments from the other lenses' findings (or
   search directly if run alone). Flag each as ahead / behind / different
   approach, with the evidence.
3. DIRECTION B, landscape vs active work. Significant developments with NO
   corresponding Jira work. Categorize each gap: intentional omission (we
   decided not to), blind spot (we did not see it), or emerging opportunity
   (too new to have decided). This is the strategic early warning and it is
   the reason the lens exists.
4. Output a `| Area | Signal strength | Category | Notes |` table for
   direction B. Never write a Jira summary verbatim into the research doc
   (this repo is PUBLIC and Jira serves nothing anonymously): cite the key and
   describe the work in your own words.
```

- [ ] **Step 3: Add the lens to the conventions enum**

In `conventions/research.md`, find the frontmatter enum line:

```
lens: landscape|upstream|architecture|requirements|competitive
```

Replace with:

```
lens: landscape|upstream|architecture|requirements|competitive|jira-gap
```

- [ ] **Step 4: Verify the linter accepts a jira-gap research doc**

The research linter warns rather than errors on frontmatter, so prove the enum
change is real by checking the file, then run the suite.

Run: `grep -n "jira-gap" conventions/research.md .claude/skills/hub.research/SKILL.md .claude/skills/hub.research/domains/redhat-ai.yaml`
Expected: at least one hit in each of the three files, and no remaining
occurrence of the word `FUTURE` on the jira-gap line.

- [ ] **Step 5: Full suite + lint**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: all PASS, `0 error(s), 81 warning(s)`, `0 stale file(s)`.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/hub.research/SKILL.md conventions/research.md .claude/skills/hub.research/domains/redhat-ai.yaml
git diff --cached --stat
git commit -m "feat(research): jira-gap lens, promoted from FUTURE (#27b)

Crosses active Jira work against the landscape in both directions. The
'what we are NOT building' table is the payload. No new code: the lens is
prose plus the domain YAML's reserved jira: block, now filled.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: `hublib/triage.py` pure classification functions (#29)

**Files:**
- Create: `scripts/hublib/triage.py`
- Test: `scripts/tests/test_triage.py`

**Interfaces:**
- Consumes: nothing. These functions are pure and offline.
- Produces, for Tasks 5 to 8:
  - `STALE_THRESHOLD_DAYS = 90`, `STAKEHOLDER_STALE_DAYS = 270`
  - `LABEL_ACTIONS: dict[str, str | None]` (action -> label, `roadmap` maps to
    `None` because its label is release-dependent)
  - `TRANSITION_ACTIONS = ("close", "approve")`
  - `SUPPORTED_ACTIONS: frozenset[str]`
  - `DEFAULT_CLOSE_COMMENT: str`
  - `issue_to_row(issue: dict) -> dict`
  - `flag_staleness(row: dict, today: datetime.date) -> list[str]`
  - `has_strat_clone(row: dict) -> bool`
  - `classify_rfe(row: dict, today: datetime.date) -> str`
  - `suggest_action(row: dict, today: datetime.date) -> dict` with keys
    `action` and `reason`

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_triage.py`:

```python
import datetime

from hublib import triage

TODAY = datetime.date(2026, 7, 11)


def row(**kw):
    base = {
        "key": "RHAIRFE-1",
        "summary": "A thing",
        "status": "New",
        "assignee": None,
        "priority": "Normal",
        "labels": [],
        "components": ["AI Hub"],
        "updated": "2026-07-10",
        "created": "2026-01-01",
        "links": [],
        "transitions": [],
    }
    base.update(kw)
    return base


# -- issue_to_row --

def test_issue_to_row_normalizes_jira_shape():
    issue = {
        "key": "RHAIRFE-9",
        "fields": {
            "summary": "Add a dashboard",
            "status": {"name": "Stakeholder Review"},
            "assignee": {"displayName": "Peter"},
            "priority": {"name": "Major"},
            "labels": ["mcp"],
            "components": [{"name": "AI Hub"}],
            "updated": "2026-05-01T10:00:00.000+0000",
            "created": "2026-01-01T10:00:00.000+0000",
            "issuelinks": [
                {"type": {"outward": "clones"},
                 "outwardIssue": {"key": "RHAISTRAT-5",
                                  "fields": {"issuetype": {"name": "Feature"}}}},
            ],
        },
    }
    r = triage.issue_to_row(issue)
    assert r["key"] == "RHAIRFE-9"
    assert r["status"] == "Stakeholder Review"
    assert r["assignee"] == "Peter"
    assert r["labels"] == ["mcp"]
    assert r["components"] == ["AI Hub"]
    assert r["updated"] == "2026-05-01"          # date only, no time
    assert r["links"] == [{"type": "clones", "key": "RHAISTRAT-5",
                           "issuetype": "Feature"}]


# -- flag_staleness --

def test_fresh_issue_has_no_staleness_flags():
    assert triage.flag_staleness(row(assignee="Peter"), TODAY) == []


def test_no_update_flag_fires_past_90_days():
    flags = triage.flag_staleness(
        row(updated="2026-01-01", assignee="Peter"), TODAY)
    assert "no_update_191d" in flags


def test_no_update_flag_does_not_fire_at_89_days():
    updated = (TODAY - datetime.timedelta(days=89)).isoformat()
    flags = triage.flag_staleness(row(updated=updated, assignee="Peter"), TODAY)
    assert not any(f.startswith("no_update_") for f in flags)


def test_stakeholder_review_stale_needs_270_days():
    updated = (TODAY - datetime.timedelta(days=280)).isoformat()
    flags = triage.flag_staleness(
        row(status="Stakeholder Review", updated=updated, assignee="Peter"),
        TODAY)
    assert "stakeholder_review_stale_280d" in flags


def test_missing_assignee_and_components_flag():
    flags = triage.flag_staleness(row(assignee=None, components=[]), TODAY)
    assert "no_assignee" in flags
    assert "no_components" in flags


def test_invalid_status_flag():
    flags = triage.flag_staleness(row(status="Marinating"), TODAY)
    assert "invalid_status:Marinating" in flags


# -- has_strat_clone --

def test_strat_clone_detected():
    r = row(links=[{"type": "clones", "key": "RHAISTRAT-5",
                    "issuetype": "Feature"}])
    assert triage.has_strat_clone(r) is True


def test_non_strat_clone_is_not_a_strat_clone():
    r = row(links=[{"type": "clones", "key": "RHOAIENG-5",
                    "issuetype": "Epic"}])
    assert triage.has_strat_clone(r) is False


def test_strat_link_of_wrong_type_is_not_a_clone():
    r = row(links=[{"type": "blocks", "key": "RHAISTRAT-5",
                    "issuetype": "Feature"}])
    assert triage.has_strat_clone(r) is False


# -- classify_rfe --

def test_roadmapped_when_release_candidate_label_present():
    assert triage.classify_rfe(row(labels=["3.6-candidate"]), TODAY) == "roadmapped"


def test_roadmapped_when_strat_clone_exists():
    r = row(links=[{"type": "clones", "key": "RHAISTRAT-5",
                    "issuetype": "Feature"}])
    assert triage.classify_rfe(r, TODAY) == "roadmapped"


def test_backlogged_when_pm_backlogged_label_present():
    assert triage.classify_rfe(row(labels=["pm-backlogged"]), TODAY) == "backlogged"


def test_close_candidate_when_very_stale():
    r = row(updated="2025-01-01", assignee="Peter")
    assert triage.classify_rfe(r, TODAY) == "close_candidate"


def test_needs_attention_is_the_default():
    assert triage.classify_rfe(row(assignee="Peter"), TODAY) == "needs_attention"


# -- suggest_action --

def test_suggests_close_for_a_close_candidate():
    s = triage.suggest_action(row(updated="2025-01-01", assignee="Peter"), TODAY)
    assert s["action"] == "close"
    assert "stale" in s["reason"].lower()


def test_suggests_approve_when_pending_approval():
    s = triage.suggest_action(row(status="Pending Approval", assignee="Peter"),
                              TODAY)
    assert s["action"] == "approve"


def test_suggests_needs_uxd_on_ui_keywords():
    s = triage.suggest_action(
        row(summary="Improve the dashboard UI layout", assignee="Peter"), TODAY)
    assert s["action"] == "needs-uxd"


def test_suggests_clarify_when_no_assignee():
    s = triage.suggest_action(row(assignee=None), TODAY)
    assert s["action"] == "clarify"


def test_roadmapped_issue_gets_no_suggestion():
    s = triage.suggest_action(row(labels=["3.6-candidate"], assignee="Peter"),
                              TODAY)
    assert s["action"] == ""
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_triage.py -v`
Expected: collection ERROR: `ImportError: cannot import name 'triage' from 'hublib'`.

- [ ] **Step 3: Implement**

Create `scripts/hublib/triage.py`:

```python
"""RFE triage: classification, suggestion, transition resolution, gated apply.

Ported from pm-toolkit's scripts/analysis/triage.py, narrowed to the hub's
write surface (spec decision 2: labels, comments, close, approve - no
assignment, no field edits, no issue creation) and re-shaped so transitions
resolve BEFORE the gate rather than during apply (spec decision 3).

Spec: docs/specs/2026-07-11-jira-operating-batch-design.md
"""
import datetime

STALE_THRESHOLD_DAYS = 90
STAKEHOLDER_STALE_DAYS = 270

VALID_STATUSES = {
    "New", "Open", "Draft", "Stakeholder Review", "Pending Approval",
    "Rejection Pending", "Approved", "Closed", "Resolved",
}

# action -> label it adds. roadmap is None: its label is release-dependent
# and comes from the decision row (<release>-candidate).
LABEL_ACTIONS = {
    "roadmap": None,
    "backlog": "pm-backlogged",
    "needs-uxd": "needs-uxd",
    "clarify": "pm-needs-clarification",
}
TRANSITION_ACTIONS = ("close", "approve")
SUPPORTED_ACTIONS = frozenset(
    set(LABEL_ACTIONS) | set(TRANSITION_ACTIONS) | {"comment", "skip"})

# Never written by this hub: <release>-committed is set on the STRAT side.
PROTECTED_LABEL_SUFFIX = "-committed"

DEFAULT_CLOSE_COMMENT = "Closed during PM triage pass. Reopen if still needed."

CLOSE_TRANSITION_NAMES = ("closed", "resolved", "close issue", "done")
APPROVE_TRANSITION_NAMES = ("approved", "approve")

UI_UX_KEYWORDS = ("dashboard", "ui", "ux", "layout", "design", "usability",
                  "wireframe", "screen")


def _date(value):
    """'2026-05-01T10:00:00.000+0000' or '2026-05-01' -> date. None on junk."""
    if not value:
        return None
    try:
        return datetime.date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _days_since(value, today):
    d = _date(value)
    return None if d is None else (today - d).days


def issue_to_row(issue):
    """Normalize a Jira issue dict into the flat row the rest of this module
    (and the HTML report, and the log) uses. Dates are truncated to day."""
    f = issue.get("fields", {}) or {}
    links = []
    for link in f.get("issuelinks") or []:
        ltype = link.get("type") or {}
        if link.get("outwardIssue"):
            other, name = link["outwardIssue"], ltype.get("outward", "")
        elif link.get("inwardIssue"):
            other, name = link["inwardIssue"], ltype.get("inward", "")
        else:
            continue
        links.append({
            "type": name,
            "key": other.get("key"),
            "issuetype": ((other.get("fields") or {}).get("issuetype")
                          or {}).get("name"),
        })
    return {
        "key": issue.get("key"),
        "summary": f.get("summary") or "",
        "status": (f.get("status") or {}).get("name") or "",
        "assignee": (f.get("assignee") or {}).get("displayName"),
        "priority": (f.get("priority") or {}).get("name"),
        "labels": list(f.get("labels") or []),
        "components": [c.get("name") for c in f.get("components") or []],
        "updated": str(f.get("updated") or "")[:10],
        "created": str(f.get("created") or "")[:10],
        "links": links,
        "transitions": [],   # filled by fetch_transitions (Task 5)
    }


def flag_staleness(row, today):
    """Objective flags. No judgement, no suggestion: just what is true."""
    flags = []
    age = _days_since(row.get("updated"), today)
    status = row.get("status") or ""

    if status == "Stakeholder Review":
        if age is not None and age >= STAKEHOLDER_STALE_DAYS:
            flags.append(f"stakeholder_review_stale_{age}d")
    elif age is not None and age >= STALE_THRESHOLD_DAYS:
        flags.append(f"no_update_{age}d")

    if not row.get("assignee"):
        flags.append("no_assignee")
    if not row.get("components"):
        flags.append("no_components")
    if status and status not in VALID_STATUSES:
        flags.append(f"invalid_status:{status}")
    return flags


def has_strat_clone(row):
    """True if this RFE is already cloned into a RHAISTRAT feature, which is
    the signal that it has been accepted onto the roadmap."""
    for link in row.get("links") or []:
        ltype = (link.get("type") or "").lower()
        key = link.get("key") or ""
        if any(t in ltype for t in ("clone", "duplicate")) \
                and key.startswith("RHAISTRAT"):
            return True
    return False


def classify_rfe(row, today):
    """roadmapped | backlogged | close_candidate | needs_attention.
    Ordered rules: the first match wins."""
    labels = row.get("labels") or []
    status = row.get("status") or ""

    if any(lbl.endswith("-candidate") or lbl.endswith(PROTECTED_LABEL_SUFFIX)
           for lbl in labels):
        return "roadmapped"
    if has_strat_clone(row):
        return "roadmapped"
    if status in ("Approved", "Closed", "Resolved"):
        return "roadmapped"
    if "pm-backlogged" in labels:
        return "backlogged"

    age = _days_since(row.get("updated"), today)
    if status == "Stakeholder Review":
        if age is not None and age >= STAKEHOLDER_STALE_DAYS:
            return "close_candidate"
    elif age is not None and age >= STALE_THRESHOLD_DAYS * 2:
        return "close_candidate"
    return "needs_attention"


def suggest_action(row, today):
    """A pre-selected action plus the reason shown as a badge in the report.
    Ordered rules: the first match wins. The human overrides freely; this only
    saves keystrokes on the obvious ones."""
    cls = classify_rfe(row, today)
    status = row.get("status") or ""
    age = _days_since(row.get("updated"), today)
    summary = (row.get("summary") or "").lower()

    if cls == "roadmapped":
        return {"action": "", "reason": "already on the roadmap"}
    if cls == "close_candidate":
        return {"action": "close",
                "reason": f"stale for {age}d with no roadmap signal"}
    if status == "Pending Approval":
        return {"action": "approve", "reason": "sitting in Pending Approval"}
    if status == "Rejection Pending":
        return {"action": "close", "reason": "already in Rejection Pending"}
    if any(k in summary for k in UI_UX_KEYWORDS):
        return {"action": "needs-uxd", "reason": "UI or UX language in summary"}
    if not row.get("assignee"):
        return {"action": "clarify", "reason": "no assignee, owner unclear"}
    if cls == "backlogged":
        return {"action": "", "reason": "already backlogged"}
    return {"action": "backlog", "reason": "no roadmap signal yet"}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_triage.py -v`
Expected: 19 PASS.

- [ ] **Step 5: Full suite + lint**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py`
Expected: all PASS, `0 error(s), 81 warning(s)`.

- [ ] **Step 6: Commit**

```bash
git add scripts/hublib/triage.py scripts/tests/test_triage.py
git diff --cached --stat
git commit -m "feat(triage): classification and suggestion engine (#29)

Pure functions, ported from pm-toolkit which ships zero tests for them.
19 tests cover the staleness thresholds, the ordered classify rules, the
strat-clone link walk, and the suggestion rules.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Scan and transition resolution (#29, spec decision 3)

**Files:**
- Modify: `scripts/hublib/triage.py` (append)
- Test: `scripts/tests/test_triage.py` (append)

**Interfaces:**
- Consumes: `hublib.jira.JiraClient.search`, `.get_transitions` (existing);
  `issue_to_row` from Task 4.
- Produces, for Tasks 6 to 8:
  - `RFE_FILTER: str` (the clause layered onto a feature's stored JQL)
  - `compose_jql(feature_jql: str) -> str`
  - `SCAN_FIELDS: list[str]`
  - `async fetch_transitions(client, rows) -> None` (mutates `row["transitions"]`
    in place; each entry is `{"id", "name", "to"}`)
  - `async scan(client, jql, today) -> list[dict]` (rows, each carrying
    `flags`, `classification`, `suggestion`, `transitions`)
  - `resolve_transition(action: str, transitions: list[dict]) -> tuple[dict | None, str]`
    returning `(transition, "")` on success or `(None, reason)` on failure.
    **Pure.** This is what lets the gate name the transition before anything
    fires.

- [ ] **Step 1: Write the failing tests**

Append to `scripts/tests/test_triage.py`:

```python
import asyncio
import json

import httpx

from hublib import jira


def run(coro):
    return asyncio.run(coro)


def client_with(handler):
    return jira.JiraClient("https://jira.test", personal_token="t",
                           transport=httpx.MockTransport(handler))


# -- compose_jql --

def test_compose_jql_layers_the_rfe_filter():
    jql = triage.compose_jql('project = RHAIRFE AND component = "AI Hub"')
    assert 'project = RHAIRFE AND component = "AI Hub"' in jql
    assert 'issuetype = "Feature Request"' in jql
    assert "resolution = Unresolved" in jql


# -- resolve_transition (pure) --

TRANSITIONS = [
    {"id": "11", "name": "Start Progress", "to": {"name": "In Progress"}},
    {"id": "31", "name": "Closed", "to": {"name": "Closed"}},
    {"id": "41", "name": "Approved", "to": {"name": "Approved"}},
]


def norm(ts):
    return [{"id": t["id"], "name": t["name"], "to": t["to"]["name"]}
            for t in ts]


def test_resolve_close_transition():
    t, reason = triage.resolve_transition("close", norm(TRANSITIONS))
    assert t["id"] == "31"
    assert reason == ""


def test_resolve_approve_transition():
    t, reason = triage.resolve_transition("approve", norm(TRANSITIONS))
    assert t["id"] == "41"


def test_resolve_is_case_insensitive():
    ts = [{"id": "9", "name": "DONE", "to": "Done"}]
    t, reason = triage.resolve_transition("close", ts)
    assert t["id"] == "9"


def test_resolve_rejects_when_no_transition_matches():
    ts = [{"id": "11", "name": "Start Progress", "to": "In Progress"}]
    t, reason = triage.resolve_transition("close", ts)
    assert t is None
    assert "no matching transition" in reason


def test_resolve_rejects_ambiguous_match_rather_than_guessing():
    ts = [{"id": "31", "name": "Closed", "to": "Closed"},
          {"id": "32", "name": "Resolved", "to": "Resolved"}]
    t, reason = triage.resolve_transition("close", ts)
    assert t is None
    assert "ambiguous" in reason


def test_resolve_of_a_non_transition_action_is_a_programming_error():
    t, reason = triage.resolve_transition("backlog", norm(TRANSITIONS))
    assert t is None
    assert "not a transition action" in reason


# -- scan --

def test_scan_fetches_flags_classifies_and_resolves_transitions():
    def handler(request):
        if "/search/jql" in request.url.path:
            return httpx.Response(200, json={
                "isLast": True,
                "issues": [{
                    "key": "RHAIRFE-1",
                    "fields": {
                        "summary": "Old thing",
                        "status": {"name": "New"},
                        "assignee": None,
                        "priority": {"name": "Normal"},
                        "labels": [],
                        "components": [],
                        "updated": "2025-01-01T00:00:00.000+0000",
                        "created": "2024-01-01T00:00:00.000+0000",
                        "issuelinks": [],
                    },
                }],
            })
        if request.url.path.endswith("/transitions"):
            return httpx.Response(200, json={"transitions": [
                {"id": "31", "name": "Closed", "to": {"name": "Closed"}},
            ]})
        raise AssertionError(f"unexpected request: {request.url}")

    async def go():
        async with client_with(handler) as c:
            return await triage.scan(c, "project = RHAIRFE", TODAY)

    rows = run(go())
    assert len(rows) == 1
    r = rows[0]
    assert r["key"] == "RHAIRFE-1"
    assert "no_assignee" in r["flags"]
    assert r["classification"] == "close_candidate"
    assert r["suggestion"]["action"] == "close"
    assert r["transitions"] == [{"id": "31", "name": "Closed", "to": "Closed"}]


def test_scan_survives_a_transitions_fetch_failure():
    # A 403 on transitions must not sink the run: the row simply carries no
    # transitions, and close/approve will be rejected at the gate for it.
    def handler(request):
        if "/search/jql" in request.url.path:
            return httpx.Response(200, json={
                "isLast": True,
                "issues": [{"key": "RHAIRFE-2", "fields": {
                    "summary": "x", "status": {"name": "New"},
                    "labels": [], "components": [], "issuelinks": [],
                    "updated": "2026-07-10T00:00:00.000+0000",
                    "created": "2026-01-01T00:00:00.000+0000"}}],
            })
        return httpx.Response(403, json={"errorMessages": ["nope"]})

    async def go():
        async with client_with(handler) as c:
            return await triage.scan(c, "project = RHAIRFE", TODAY)

    rows = run(go())
    assert rows[0]["transitions"] == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_triage.py -v -k "compose or resolve or scan"`
Expected: FAIL with `AttributeError: module 'hublib.triage' has no attribute 'compose_jql'`.

- [ ] **Step 3: Implement**

Append to `scripts/hublib/triage.py`:

```python
import asyncio as _asyncio

import httpx as _httpx

RFE_FILTER = 'issuetype = "Feature Request" AND resolution = Unresolved'

SCAN_FIELDS = ["summary", "status", "assignee", "priority", "labels",
               "components", "updated", "created", "issuelinks"]

MAX_RESULTS = 500
TRANSITION_CONCURRENCY = 5


def compose_jql(feature_jql):
    """The feature's stored scope, narrowed to open RFEs (spec decision 5).
    ORDER BY is stripped from the stored scope: it would be illegal mid-query.
    """
    base = feature_jql.strip()
    order = ""
    lowered = base.lower()
    if " order by " in lowered:
        cut = lowered.rindex(" order by ")
        base, order = base[:cut].strip(), base[cut:].strip()
    return f"({base}) AND {RFE_FILTER} " + (order or "ORDER BY updated ASC")


def resolve_transition(action, transitions):
    """(transition, "") on success, (None, reason) on failure. PURE.

    Resolved during the scan so the gate can name the transition that will
    fire. pm-toolkit resolved this during apply, AFTER posting the close
    comment, so a workflow with no matching transition left a "Closed during
    PM triage pass" comment on an issue that stayed open. That half-apply is
    the bug this function exists to prevent.
    """
    if action == "close":
        wanted = CLOSE_TRANSITION_NAMES
    elif action == "approve":
        wanted = APPROVE_TRANSITION_NAMES
    else:
        return None, f"'{action}' is not a transition action"

    matches = [t for t in transitions
               if (t.get("name") or "").strip().lower() in wanted]
    if not matches:
        available = ", ".join(t.get("name", "?") for t in transitions) or "none"
        return None, (f"no matching transition for '{action}' in this workflow "
                      f"(available: {available})")
    if len(matches) > 1:
        names = ", ".join(t.get("name", "?") for t in matches)
        return None, (f"ambiguous transition for '{action}': {names}. "
                      f"Resolve it in Jira, not here.")
    return matches[0], ""


async def fetch_transitions(client, rows):
    """Fill row["transitions"] for every row, concurrently. A failure on one
    issue leaves that row with an empty list: close/approve will then be
    rejected at the gate for it, which is the correct fail-closed behavior.
    """
    sem = _asyncio.Semaphore(TRANSITION_CONCURRENCY)

    async def one(row):
        async with sem:
            try:
                raw = await client.get_transitions(row["key"])
            except _httpx.HTTPError:
                return
        row["transitions"] = [
            {"id": t.get("id"), "name": t.get("name"),
             "to": (t.get("to") or {}).get("name")}
            for t in raw
        ]

    await _asyncio.gather(*(one(r) for r in rows))


async def scan(client, jql, today):
    """Fetch, normalize, flag, classify, suggest, and resolve transitions.
    Everything the report and the gate need, in one pass. Read-only."""
    issues = await client.search(jql, fields=SCAN_FIELDS,
                                 max_results=MAX_RESULTS)
    rows = [issue_to_row(i) for i in issues]
    await fetch_transitions(client, rows)
    for row in rows:
        row["flags"] = flag_staleness(row, today)
        row["classification"] = classify_rfe(row, today)
        row["suggestion"] = suggest_action(row, today)
    return rows
```

Move the two new imports (`asyncio`, `httpx`) to the top of the file with the
existing `import datetime`, and delete the aliased `_asyncio` / `_httpx` names,
replacing their uses with `asyncio` and `httpx`. The aliases above exist only
to make this append-step readable; the committed file must have clean top-level
imports:

```python
import asyncio
import datetime

import httpx
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_triage.py -v`
Expected: 27 PASS.

- [ ] **Step 5: Full suite + lint**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py`
Expected: all PASS, `0 error(s), 81 warning(s)`.

- [ ] **Step 6: Commit**

```bash
git add scripts/hublib/triage.py scripts/tests/test_triage.py
git diff --cached --stat
git commit -m "feat(triage): scan + transition resolution before the gate (#29)

Transitions resolve during the scan, not during apply (spec decision 3), so
the gate names the transition that will fire and an unresolvable or
ambiguous one is rejected rather than half-applied. A transitions fetch that
403s leaves the row with no transitions, which fails closed.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Gated apply (#29, the first Jira write)

**Files:**
- Modify: `scripts/hublib/triage.py` (append)
- Test: `scripts/tests/test_triage.py` (append)

**Interfaces:**
- Consumes: `resolve_transition` (Task 5); `JiraClient.update_issue`,
  `.add_comment`, `.transition_issue` (existing, never before called).
- Produces, for Tasks 7 to 9:
  - `plan_decisions(decisions: dict, rows: list[dict]) -> dict` with keys
    `labels`, `comments`, `transitions`, `rejected`, `skipped`. **Pure.** This
    is exactly what the gate renders.
  - `async apply_decisions(client, plan) -> dict` with keys `applied`,
    `skipped`, `rejected`, `errors` (each a list of
    `{"key", "action", "detail"}`).
  - `build_triage_log(feature, jql, rows, plan, result, today) -> str` (YAML text)

Apply order is labels, then comments, then transitions (spec skill flow step 6):
a workflow surprise on the sharpest action cannot strand the cheap ones.

- [ ] **Step 1: Write the failing tests**

Append to `scripts/tests/test_triage.py`:

```python
# -- plan_decisions (pure) --

def scan_row(**kw):
    r = row(**kw)
    r["flags"] = []
    r["classification"] = "needs_attention"
    r["suggestion"] = {"action": "", "reason": ""}
    return r


CLOSABLE = [{"id": "31", "name": "Closed", "to": "Closed"}]


def test_plan_sorts_actions_into_buckets():
    rows = [scan_row(key="A-1", labels=["old"]),
            scan_row(key="A-2", transitions=CLOSABLE),
            scan_row(key="A-3")]
    decisions = {
        "A-1": {"action": "backlog", "current_labels": ["old"]},
        "A-2": {"action": "close"},
        "A-3": {"action": "skip"},
    }
    plan = triage.plan_decisions(decisions, rows)
    assert plan["labels"] == [
        {"key": "A-1", "action": "backlog", "label": "pm-backlogged",
         "current_labels": ["old"]}]
    assert plan["transitions"][0]["key"] == "A-2"
    assert plan["transitions"][0]["transition"]["id"] == "31"
    assert plan["skipped"] == [{"key": "A-3", "action": "skip",
                                "detail": "skipped"}]
    assert plan["rejected"] == []


def test_plan_rejects_unsupported_actions():
    rows = [scan_row(key="A-1")]
    plan = triage.plan_decisions({"A-1": {"action": "assign"}}, rows)
    assert plan["rejected"][0]["key"] == "A-1"
    assert "not a supported action" in plan["rejected"][0]["detail"]
    assert plan["labels"] == []


def test_plan_rejects_a_close_with_no_matching_transition():
    rows = [scan_row(key="A-1", transitions=[])]
    plan = triage.plan_decisions({"A-1": {"action": "close"}}, rows)
    assert plan["transitions"] == []
    assert plan["comments"] == []          # the half-apply guard
    assert "no matching transition" in plan["rejected"][0]["detail"]


def test_plan_rejects_a_decision_for_an_issue_not_in_the_scan():
    plan = triage.plan_decisions({"GHOST-9": {"action": "backlog"}},
                                 [scan_row(key="A-1")])
    assert "not in the scan" in plan["rejected"][0]["detail"]


def test_plan_skips_a_label_already_present():
    rows = [scan_row(key="A-1", labels=["pm-backlogged"])]
    plan = triage.plan_decisions(
        {"A-1": {"action": "backlog", "current_labels": ["pm-backlogged"]}}, rows)
    assert plan["labels"] == []
    assert plan["skipped"][0]["detail"] == "label pm-backlogged already present"


def test_plan_roadmap_requires_a_release():
    rows = [scan_row(key="A-1")]
    plan = triage.plan_decisions({"A-1": {"action": "roadmap"}}, rows)
    assert "needs a release" in plan["rejected"][0]["detail"]

    plan = triage.plan_decisions(
        {"A-1": {"action": "roadmap", "release": "3.6"}}, rows)
    assert plan["labels"][0]["label"] == "3.6-candidate"


def test_plan_never_writes_a_committed_label():
    rows = [scan_row(key="A-1")]
    plan = triage.plan_decisions(
        {"A-1": {"action": "roadmap", "release": "3.6-committed"}}, rows)
    assert plan["labels"] == []
    assert "committed" in plan["rejected"][0]["detail"]


def test_plan_close_carries_the_default_comment():
    rows = [scan_row(key="A-1", transitions=CLOSABLE)]
    plan = triage.plan_decisions({"A-1": {"action": "close"}}, rows)
    assert plan["transitions"][0]["comment"] == triage.DEFAULT_CLOSE_COMMENT


# -- apply_decisions --

def test_apply_writes_labels_comments_and_transitions_in_order():
    seen = []

    def handler(request):
        seen.append((request.method, request.url.path,
                     json.loads(request.content or b"{}")))
        return httpx.Response(204 if request.method == "PUT" else 200, json={})

    rows = [scan_row(key="A-1", labels=["old"]),
            scan_row(key="A-2", transitions=CLOSABLE)]
    plan = triage.plan_decisions({
        "A-1": {"action": "backlog", "current_labels": ["old"]},
        "A-2": {"action": "close"},
    }, rows)

    async def go():
        async with client_with(handler) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    assert len(result["applied"]) == 2
    assert result["errors"] == []

    # label write carries the FULL array, not just the new label
    put = [s for s in seen if s[0] == "PUT"][0]
    assert put[2]["fields"]["labels"] == ["old", "pm-backlogged"]

    # transitions go last, and the close comment precedes its transition
    kinds = [(m, p.rsplit("/", 1)[-1]) for m, p, _ in seen]
    assert kinds.index(("POST", "comment")) < kinds.index(("POST", "transitions"))
    assert kinds[-1] == ("POST", "transitions")


def test_apply_never_touches_jira_for_a_rejected_decision():
    seen = []

    def handler(request):
        seen.append(request.url.path)
        return httpx.Response(200, json={})

    rows = [scan_row(key="A-1", transitions=[])]        # cannot close
    plan = triage.plan_decisions({"A-1": {"action": "close"}}, rows)

    async def go():
        async with client_with(handler) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    assert seen == []                                   # zero requests
    assert result["applied"] == []
    assert len(result["rejected"]) == 1


def test_apply_partial_failure_still_applies_the_rest():
    def handler(request):
        if request.url.path.endswith("/A-2/transitions") \
                and request.method == "POST":
            return httpx.Response(400, json={"errorMessages": ["workflow moved"]})
        return httpx.Response(204 if request.method == "PUT" else 200, json={})

    rows = [scan_row(key="A-1", labels=[]),
            scan_row(key="A-2", transitions=CLOSABLE)]
    plan = triage.plan_decisions({
        "A-1": {"action": "backlog", "current_labels": []},
        "A-2": {"action": "close"},
    }, rows)

    async def go():
        async with client_with(handler) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    applied_keys = [a["key"] for a in result["applied"]]
    assert "A-1" in applied_keys                        # label still landed
    assert any(e["key"] == "A-2" for e in result["errors"])


# -- build_triage_log --

def test_triage_log_is_yaml_and_carries_no_jira_prose():
    rows = [scan_row(key="A-1", summary="Secret internal roadmap detail",
                     labels=[], transitions=CLOSABLE)]
    plan = triage.plan_decisions({"A-1": {"action": "close"}}, rows)

    async def go():
        async with client_with(
                lambda r: httpx.Response(200, json={})) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    text = triage.build_triage_log("mcp-registry", "project = X", rows, plan,
                                   result, TODAY)
    assert "do not hand-edit" in text
    assert "feature: mcp-registry" in text
    assert "Secret internal roadmap detail" not in text   # NO Jira prose
    assert "transition: Open -> Closed" in text or "Closed" in text
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_triage.py -v -k "plan or apply or log"`
Expected: FAIL with `AttributeError: module 'hublib.triage' has no attribute 'plan_decisions'`.

- [ ] **Step 3: Implement**

Append to `scripts/hublib/triage.py`:

```python
import yaml


def plan_decisions(decisions, rows):
    """Turn the browser's exported decisions into an explicit, inspectable
    plan. PURE: this is what the gate renders, and nothing here touches Jira.

    Every rejection carries its reason. Nothing is ever silently dropped
    (spec decision 2).
    """
    by_key = {r["key"]: r for r in rows}
    plan = {"labels": [], "comments": [], "transitions": [],
            "rejected": [], "skipped": []}

    for key, decision in decisions.items():
        action = (decision or {}).get("action") or "skip"
        row = by_key.get(key)

        if row is None:
            plan["rejected"].append({
                "key": key, "action": action,
                "detail": "not in the scan (stale decisions file?)"})
            continue
        if action not in SUPPORTED_ACTIONS:
            plan["rejected"].append({
                "key": key, "action": action,
                "detail": f"'{action}' is not a supported action. This hub "
                          f"writes labels, comments, close and approve only."})
            continue
        if action == "skip":
            plan["skipped"].append({"key": key, "action": "skip",
                                    "detail": "skipped"})
            continue

        # current_labels round-trips through the report so label writes stay
        # read-modify-write. Fall back to the scanned row if it is absent.
        current = list(decision.get("current_labels") or row.get("labels") or [])

        if action in LABEL_ACTIONS:
            label = LABEL_ACTIONS[action]
            if action == "roadmap":
                release = (decision.get("release") or "").strip()
                if not release:
                    plan["rejected"].append({
                        "key": key, "action": action,
                        "detail": "roadmap needs a release (for example 3.6)"})
                    continue
                if release.endswith(PROTECTED_LABEL_SUFFIX) \
                        or PROTECTED_LABEL_SUFFIX in release:
                    plan["rejected"].append({
                        "key": key, "action": action,
                        "detail": f"'{release}' would write a committed label. "
                                  f"That is set on the STRAT side, never here."})
                    continue
                label = f"{release}-candidate"
            if label in current:
                plan["skipped"].append({
                    "key": key, "action": action,
                    "detail": f"label {label} already present"})
                continue
            plan["labels"].append({"key": key, "action": action, "label": label,
                                   "current_labels": current})
            continue

        if action == "comment":
            body = (decision.get("comment") or "").strip()
            if not body:
                plan["rejected"].append({
                    "key": key, "action": action,
                    "detail": "comment action with no comment text"})
                continue
            plan["comments"].append({"key": key, "action": "comment",
                                     "comment": body})
            continue

        # close | approve: resolve the transition NOW, before the gate.
        transition, reason = resolve_transition(action, row.get("transitions") or [])
        if transition is None:
            plan["rejected"].append({"key": key, "action": action,
                                     "detail": reason})
            continue
        entry = {"key": key, "action": action, "transition": transition,
                 "from": row.get("status") or "?", "comment": None}
        if action == "close":
            # The comment and the transition are a UNIT. If we could not
            # resolve the transition we rejected above, so no comment is
            # posted on an issue that stays open (the pm-toolkit bug).
            entry["comment"] = ((decision.get("comment") or "").strip()
                                or DEFAULT_CLOSE_COMMENT)
        plan["transitions"].append(entry)

    return plan


async def apply_decisions(client, plan):
    """Execute an approved plan. Labels, then comments, then transitions:
    a workflow surprise on the sharpest action cannot strand the cheap ones.

    Per-item try/except. One failure never sinks the batch.
    """
    result = {"applied": [], "skipped": list(plan["skipped"]),
              "rejected": list(plan["rejected"]), "errors": []}

    for item in plan["labels"]:
        labels = list(item["current_labels"]) + [item["label"]]
        try:
            await client.update_issue(item["key"], {"labels": labels})
        except httpx.HTTPError as exc:
            result["errors"].append({"key": item["key"], "action": item["action"],
                                     "detail": f"label write failed: {exc}"})
            continue
        result["applied"].append({"key": item["key"], "action": item["action"],
                                  "detail": f"+label {item['label']}"})

    for item in plan["comments"]:
        try:
            await client.add_comment(item["key"], item["comment"])
        except httpx.HTTPError as exc:
            result["errors"].append({"key": item["key"], "action": "comment",
                                     "detail": f"comment failed: {exc}"})
            continue
        result["applied"].append({"key": item["key"], "action": "comment",
                                  "detail": "comment posted"})

    for item in plan["transitions"]:
        key, action, transition = item["key"], item["action"], item["transition"]
        if item.get("comment"):
            try:
                await client.add_comment(key, item["comment"])
            except httpx.HTTPError as exc:
                result["errors"].append({
                    "key": key, "action": action,
                    "detail": f"close comment failed, transition NOT attempted: {exc}"})
                continue
        try:
            await client.transition_issue(key, transition["id"])
        except httpx.HTTPError as exc:
            detail = f"transition to {transition['name']} failed: {exc}"
            if item.get("comment"):
                detail += (" (the close comment HAS already posted; the issue "
                           "is still open. Resolve it in Jira.)")
            result["errors"].append({"key": key, "action": action,
                                     "detail": detail})
            continue
        result["applied"].append({
            "key": key, "action": action,
            "detail": f"{item['from']} -> {transition['to'] or transition['name']}"})

    return result


def build_triage_log(feature, jql, rows, plan, result, today):
    """The tracked record: keys, flags, decisions, outcomes. NO Jira prose
    (no summaries, no comment bodies, no assignee names) so it needs no
    redaction in a PUBLIC repo (spec decision 4).
    """
    outcome_by_key = {}
    labels_by_key = {}
    transition_by_key = {}
    for bucket, name in (("applied", "applied"), ("skipped", "skipped"),
                         ("rejected", "rejected"), ("errors", "error")):
        for item in result[bucket]:
            outcome_by_key.setdefault(item["key"], name)
    for item in plan["labels"]:
        labels_by_key.setdefault(item["key"], []).append(item["label"])
    for item in plan["transitions"]:
        t = item["transition"]
        transition_by_key[item["key"]] = \
            f"{item['from']} -> {t.get('to') or t.get('name')}"

    entries = []
    for row in sorted(rows, key=lambda r: r["key"]):
        key = row["key"]
        if key not in outcome_by_key:
            continue          # not decided this pass: not our business to log
        entries.append({
            "key": key,
            "flags": list(row.get("flags") or []),
            "suggestion": (row.get("suggestion") or {}).get("action") or "",
            "decision": _decision_of(key, plan),
            "outcome": outcome_by_key[key],
            "labels_added": labels_by_key.get(key, []),
            "transition": transition_by_key.get(key),
        })

    doc = {"feature": feature, "jql": jql, "triaged": today.isoformat(),
           "issues": entries}
    header = ("# generated by hub.jira-triage (scripts/hub_triage.py) - "
              "do not hand-edit\n")
    return header + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True)


def _decision_of(key, plan):
    for bucket in ("labels", "comments", "transitions", "rejected", "skipped"):
        for item in plan[bucket]:
            if item["key"] == key:
                return item["action"]
    return ""
```

Move `import yaml` to the top of the file with the other imports.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_triage.py -v`
Expected: 39 PASS.

- [ ] **Step 5: Full suite + lint**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py`
Expected: all PASS, `0 error(s), 81 warning(s)`.

- [ ] **Step 6: Commit**

```bash
git add scripts/hublib/triage.py scripts/tests/test_triage.py
git diff --cached --stat
git commit -m "feat(triage): gated apply, the hub's first Jira write surface (#29)

plan_decisions is pure and is exactly what the gate renders; nothing is
silently dropped. apply_decisions writes labels, then comments, then
transitions. A close whose transition did not resolve posts NO comment,
which is the pm-toolkit half-apply bug, covered by a named regression test.
build_triage_log emits the tracked record with no Jira prose in it.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: The HTML triage report

**Files:**
- Create: `scripts/hublib/triage_html.py`
- Test: `scripts/tests/test_triage_html.py`

**Interfaces:**
- Consumes: rows from `triage.scan` (Task 5).
- Produces, for Task 8: `render(feature, jql, rows, today, base_url) -> str`
  (a complete, self-contained HTML document).

The report carries full Jira summaries, so Task 8 writes it under `restricted/`
only. It embeds the feature in a `data-feature` attribute rather than scraping
`document.title` (spec decision 9).

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_triage_html.py`:

```python
import datetime

from hublib import triage, triage_html

TODAY = datetime.date(2026, 7, 11)


def scan_row(**kw):
    base = {
        "key": "RHAIRFE-1", "summary": "A thing", "status": "New",
        "assignee": None, "priority": "Normal", "labels": [],
        "components": [], "updated": "2026-07-10", "created": "2026-01-01",
        "links": [], "transitions": [], "flags": [],
        "classification": "needs_attention",
        "suggestion": {"action": "backlog", "reason": "no roadmap signal yet"},
    }
    base.update(kw)
    return base


def test_report_is_self_contained():
    html = triage_html.render("mcp-registry", "project = X", [scan_row()],
                              TODAY, "https://jira.test")
    assert html.startswith("<!doctype html>")
    assert "<style>" in html and "<script>" in html
    # no external anything: a CSP-hostile report is a broken report
    assert "http-equiv" not in html
    assert 'src="http' not in html
    assert 'href="http' not in html or 'href="https://jira.test/browse' in html


def test_feature_is_a_data_attribute_not_a_title_scrape():
    html = triage_html.render("mcp-registry", "project = X", [scan_row()],
                              TODAY, "https://jira.test")
    assert 'data-feature="mcp-registry"' in html
    # the em-dash title split that pm-toolkit used must not reappear
    assert "document.title.split" not in html
    assert "—" not in html          # no em dashes anywhere, ever


def test_rows_are_grouped_into_the_three_sections():
    rows = [
        scan_row(key="A-1", classification="needs_attention"),
        scan_row(key="A-2", classification="backlogged"),
        scan_row(key="A-3", status="Stakeholder Review",
                 classification="needs_attention"),
    ]
    html = triage_html.render("f", "jql", rows, TODAY, "https://jira.test")
    assert "Untriaged" in html
    assert "Waiting on Input" in html
    assert "Backlogged" in html
    for key in ("A-1", "A-2", "A-3"):
        assert key in html


def test_current_labels_round_trip_through_a_hidden_cell():
    rows = [scan_row(labels=["mcp", "3.6-candidate"])]
    html = triage_html.render("f", "jql", rows, TODAY, "https://jira.test")
    assert "labels-data" in html
    assert "3.6-candidate" in html


def test_close_and_approve_are_offered_only_when_the_workflow_allows_it():
    closable = scan_row(key="A-1",
                        transitions=[{"id": "31", "name": "Closed",
                                      "to": "Closed"}])
    stuck = scan_row(key="A-2", transitions=[])
    html = triage_html.render("f", "jql", [closable, stuck], TODAY,
                              "https://jira.test")
    # the closable row offers close; the stuck one says why it cannot
    assert 'value="close"' in html
    assert "no matching transition" in html


def test_suggestion_and_reason_are_rendered():
    html = triage_html.render("f", "jql", [scan_row()], TODAY,
                              "https://jira.test")
    assert "no roadmap signal yet" in html
    assert 'data-suggestion="backlog"' in html


def test_summaries_are_html_escaped():
    rows = [scan_row(summary='<script>alert("x")</script> & more')]
    html = triage_html.render("f", "jql", rows, TODAY, "https://jira.test")
    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_triage_html.py -v`
Expected: collection ERROR: `ImportError: cannot import name 'triage_html' from 'hublib'`.

- [ ] **Step 3: Implement**

Create `scripts/hublib/triage_html.py`:

```python
"""The triage report: a self-contained HTML page with per-row decisions and an
Export Decisions button.

This report renders authenticated Jira text (summaries, statuses), so it is
written under restricted/ ONLY and never into the tracked tree (spec decision
4: this repo is PUBLIC and Jira serves nothing anonymously).

The exported JSON is a PROPOSAL. It is not applied until the inline gate in
hub.jira-triage approves it line by line (spec decision 7).
"""
import html
import json

from . import triage

SECTIONS = (
    ("Untriaged", "needs_attention"),
    ("Waiting on Input", "waiting"),
    ("Backlogged", "backlogged"),
)

CSS = """
:root { color-scheme: light dark; }
body { font: 14px/1.5 system-ui, sans-serif; margin: 0; padding: 2rem;
       background: #fbfbfd; color: #1a1a1a; }
h1 { font-size: 1.4rem; margin: 0 0 .25rem; }
.scope { color: #666; font-size: .8rem; margin-bottom: 1.5rem;
         font-family: ui-monospace, monospace; word-break: break-all; }
.tiles { display: flex; gap: .75rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.tile { background: #fff; border: 1px solid #e3e3e8; border-radius: 8px;
        padding: .6rem 1rem; min-width: 5rem; }
.tile b { display: block; font-size: 1.5rem; }
.tile span { color: #666; font-size: .75rem; }
h2 { font-size: 1rem; margin: 1.75rem 0 .5rem; }
table { width: 100%; border-collapse: collapse; background: #fff;
        border: 1px solid #e3e3e8; border-radius: 8px; overflow: hidden; }
th, td { text-align: left; padding: .5rem .6rem; border-bottom: 1px solid #f0f0f3;
         vertical-align: top; }
th { background: #f6f6f8; font-size: .75rem; text-transform: uppercase;
     letter-spacing: .04em; color: #555; }
tr:last-child td { border-bottom: none; }
.key { font-family: ui-monospace, monospace; white-space: nowrap; }
.flag { display: inline-block; background: #fdecea; color: #a32; font-size: .7rem;
        padding: .1rem .35rem; border-radius: 4px; margin-right: .25rem; }
.why { color: #666; font-size: .75rem; }
.blocked { color: #a32; font-size: .72rem; }
.bar { position: sticky; top: 0; background: #fbfbfdee; padding: .75rem 0;
       backdrop-filter: blur(6px); display: flex; gap: .75rem; align-items: center;
       border-bottom: 1px solid #e3e3e8; margin-bottom: 1rem; z-index: 2; }
button { font: inherit; padding: .4rem .9rem; border-radius: 6px;
         border: 1px solid #c9c9d0; background: #fff; cursor: pointer; }
button.primary { background: #06c; color: #fff; border-color: #06c; }
#count { color: #666; font-size: .8rem; }
@media (prefers-color-scheme: dark) {
  body { background: #16161a; color: #e8e8ea; }
  .tile, table { background: #1e1e23; border-color: #33333a; }
  th { background: #26262c; color: #aaa; }
  td { border-color: #2a2a30; }
  .bar { background: #16161aee; border-color: #33333a; }
  button { background: #26262c; color: #e8e8ea; border-color: #3a3a42; }
}
"""

JS = """
function decisions() {
  const out = {};
  document.querySelectorAll('tr[data-key]').forEach(tr => {
    const sel = tr.querySelector('select');
    if (!sel || !sel.value) return;
    const rel = tr.querySelector('.release');
    const com = tr.querySelector('.commenttext');
    out[tr.dataset.key] = {
      action: sel.value,
      release: rel && rel.value ? rel.value.trim() : null,
      comment: com && com.value ? com.value.trim() : null,
      current_labels: JSON.parse(tr.querySelector('.labels-data').textContent || '[]')
    };
  });
  return out;
}
function refresh() {
  const n = Object.keys(decisions()).length;
  document.getElementById('count').textContent = n + ' decision(s) staged';
}
document.addEventListener('change', e => {
  if (e.target.tagName === 'SELECT') {
    const tr = e.target.closest('tr');
    const rel = tr.querySelector('.release');
    if (rel) rel.style.display = e.target.value === 'roadmap' ? '' : 'none';
    const com = tr.querySelector('.commenttext');
    if (com) com.style.display =
      (e.target.value === 'comment' || e.target.value === 'close') ? '' : 'none';
  }
  refresh();
});
function exportDecisions() {
  const payload = {
    exported_at: document.body.dataset.today,
    feature: document.body.dataset.feature,
    decisions: decisions()
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)],
                        {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'triage-decisions-' + payload.exported_at + '.json';
  a.click();
}
document.addEventListener('DOMContentLoaded', refresh);
"""


def _esc(value):
    return html.escape(str(value if value is not None else ""), quote=True)


def _options(row):
    """The action menu for one row. close and approve appear only when the
    workflow actually offers the transition (spec decision 3), so the human
    cannot stage a decision that the gate will only reject later."""
    opts = ['<option value="">-- decide --</option>']
    for action in ("roadmap", "backlog", "needs-uxd", "clarify", "comment"):
        opts.append(f'<option value="{action}">{action}</option>')
    blocked = []
    for action in triage.TRANSITION_ACTIONS:
        transition, reason = triage.resolve_transition(
            action, row.get("transitions") or [])
        if transition is not None:
            opts.append(f'<option value="{action}">{action} '
                        f'({_esc(transition.get("to") or transition.get("name"))})'
                        f'</option>')
        else:
            blocked.append(f"{action}: {reason}")
    opts.append('<option value="skip">skip</option>')
    return "\n".join(opts), blocked


def _section_of(row):
    if row.get("classification") == "backlogged":
        return "Backlogged"
    if row.get("status") in ("Stakeholder Review", "Pending Approval"):
        return "Waiting on Input"
    return "Untriaged"


def _row_html(row, base_url):
    options, blocked = _options(row)
    flags = "".join(f'<span class="flag">{_esc(f)}</span>'
                    for f in row.get("flags") or [])
    suggestion = (row.get("suggestion") or {})
    labels_json = _esc(json.dumps(row.get("labels") or []))
    blocked_html = ("".join(f'<div class="blocked">{_esc(b)}</div>'
                            for b in blocked))
    return f"""
<tr data-key="{_esc(row['key'])}" data-suggestion="{_esc(suggestion.get('action'))}">
  <td class="key"><a href="{_esc(base_url)}/browse/{_esc(row['key'])}"
      target="_blank" rel="noopener">{_esc(row['key'])}</a></td>
  <td>{_esc(row.get('summary'))}<div>{flags}</div>{blocked_html}</td>
  <td>{_esc(row.get('status'))}</td>
  <td>{_esc(row.get('assignee') or '-')}</td>
  <td>{_esc(row.get('updated'))}</td>
  <td>
    <select>{options}</select>
    <input class="release" placeholder="3.6" style="display:none" size="5">
    <textarea class="commenttext" placeholder="comment" style="display:none"
              rows="2"></textarea>
    <div class="why">{_esc(suggestion.get('reason'))}</div>
    <span class="labels-data" hidden>{labels_json}</span>
  </td>
</tr>"""


def render(feature, jql, rows, today, base_url):
    """A complete, self-contained HTML document. No network, no repo writes."""
    buckets = {name: [] for name, _ in SECTIONS}
    for row in rows:
        buckets[_section_of(row)].append(row)

    tiles = "".join(
        f'<div class="tile"><b>{len(buckets[name])}</b><span>{_esc(name)}</span></div>'
        for name, _ in SECTIONS)
    tiles += (f'<div class="tile"><b>{len(rows)}</b><span>Total</span></div>')

    sections = []
    for name, _ in SECTIONS:
        section_rows = buckets[name]
        if not section_rows:
            continue
        body = "".join(_row_html(r, base_url) for r in section_rows)
        sections.append(f"""
<h2>{_esc(name)} ({len(section_rows)})</h2>
<table>
  <thead><tr><th>Key</th><th>Summary</th><th>Status</th><th>Assignee</th>
             <th>Updated</th><th>Decision</th></tr></thead>
  <tbody>{body}</tbody>
</table>""")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Triage: {_esc(feature)}</title>
<style>{CSS}</style>
</head>
<body data-feature="{_esc(feature)}" data-today="{_esc(today.isoformat())}">
<h1>RFE triage: {_esc(feature)}</h1>
<div class="scope">{_esc(jql)}</div>
<div class="bar">
  <button class="primary" onclick="exportDecisions()">Export Decisions</button>
  <span id="count">0 decision(s) staged</span>
</div>
<div class="tiles">{tiles}</div>
{''.join(sections)}
<script>{JS}</script>
</body>
</html>
"""
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_triage_html.py -v`
Expected: 7 PASS.

- [ ] **Step 5: Full suite + lint**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py`
Expected: all PASS, `0 error(s), 81 warning(s)`.

- [ ] **Step 6: Commit**

```bash
git add scripts/hublib/triage_html.py scripts/tests/test_triage_html.py
git diff --cached --stat
git commit -m "feat(triage): self-contained HTML report (#29)

Feature travels in a data- attribute, not an em-dash title scrape. close and
approve are offered only where the workflow actually allows the transition,
so a decision the gate would reject cannot be staged. Summaries are escaped.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 8: `scripts/hub_triage.py` CLI

**Files:**
- Create: `scripts/hub_triage.py`
- Test: `scripts/tests/test_hub_triage.py`

**Interfaces:**
- Consumes: `hublib.triage` (Tasks 4 to 6), `hublib.triage_html` (Task 7),
  `hublib.jira.client_from_env`, `hublib.shellenv.load_env`.
- Produces, for Task 9:
  - `python scripts/hub_triage.py --scan <feature> --out DIR` writes
    `DIR/triage-<feature>-<date>.html` and `DIR/rows-<feature>.json`, printing
    both paths.
  - `python scripts/hub_triage.py --plan <decisions.json> --rows <rows.json>`
    prints the gate table and exits 0 without touching Jira.
  - `python scripts/hub_triage.py --apply <decisions.json> --rows <rows.json>
    --feature <f> --out DIR` applies and writes `DIR/triage-log-<f>.yaml`.

The CLI never writes into the repo: `--out DIR` is mandatory, exactly like
`hub_jira.py`. The skill copies the report into `restricted/` and the log into
the tracked tree after the gate.

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_hub_triage.py`:

```python
import json
from pathlib import Path

import pytest

import hub_triage


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


def make_repo(tmp_path: Path) -> Path:
    write(tmp_path, "features/features.yaml",
          "features:\n"
          "- id: mcp-registry\n  title: R\n  description: d\n"
          "  jira:\n    jql: 'project = RHAIRFE'\n"
          "- id: bare\n  title: B\n  description: d\n")
    return tmp_path


def test_exactly_one_mode_required():
    with pytest.raises(SystemExit):
        hub_triage.main([])
    with pytest.raises(SystemExit):
        hub_triage.main(["--scan", "x", "--apply", "y"])


def test_scan_requires_out_dir(tmp_path):
    with pytest.raises(SystemExit):
        hub_triage.main(["--scan", "mcp-registry",
                         "--root", str(make_repo(tmp_path))])


def test_scan_unknown_feature_exits_2(tmp_path, capsys):
    rc = hub_triage.main(["--scan", "nope", "--out", str(tmp_path / "o"),
                          "--root", str(make_repo(tmp_path))])
    assert rc == 2
    assert "unknown feature" in capsys.readouterr().out


def test_scan_without_stored_scope_exits_2(tmp_path, capsys):
    rc = hub_triage.main(["--scan", "bare", "--out", str(tmp_path / "o"),
                          "--root", str(make_repo(tmp_path))])
    assert rc == 2
    assert "no stored jira scope" in capsys.readouterr().out


def test_plan_mode_prints_the_gate_table_and_touches_no_network(tmp_path, capsys):
    rows = [{
        "key": "A-1", "summary": "s", "status": "New", "assignee": None,
        "priority": None, "labels": [], "components": [], "updated": "2026-07-01",
        "created": "2026-01-01", "links": [], "transitions": [],
        "flags": [], "classification": "needs_attention",
        "suggestion": {"action": "backlog", "reason": "r"},
    }]
    rows_p = tmp_path / "rows.json"
    rows_p.write_text(json.dumps(rows), encoding="utf-8")
    dec_p = tmp_path / "d.json"
    dec_p.write_text(json.dumps({
        "feature": "mcp-registry",
        "decisions": {"A-1": {"action": "backlog", "current_labels": []},
                      "A-2": {"action": "assign"}},
    }), encoding="utf-8")

    rc = hub_triage.main(["--plan", str(dec_p), "--rows", str(rows_p)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "LABELS (1)" in out
    assert "+pm-backlogged" in out
    assert "REJECTED (1)" in out
    assert "not in the scan" in out


def test_apply_requires_rows_and_feature(tmp_path):
    with pytest.raises(SystemExit):
        hub_triage.main(["--apply", str(tmp_path / "d.json")])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_hub_triage.py -v`
Expected: collection ERROR: `ModuleNotFoundError: No module named 'hub_triage'`.

- [ ] **Step 3: Implement**

Create `scripts/hub_triage.py`:

```python
"""CLI: the RFE triage pipeline.

  --scan <feature> --out DIR                       fetch + report + rows -> DIR
  --plan <decisions.json> --rows <rows.json>       render the gate table (no network)
  --apply <decisions.json> --rows <rows.json> --feature <f> --out DIR

WRITES TO JIRA (labels, comments, close, approve) in --apply mode only, and
only through the gate in hub.jira-triage. --scan and --plan are read-only.

The CLI never writes into the repo: --out DIR is required, and the gated skill
copies the report into restricted/ and the log into the tracked tree.

Spec: docs/specs/2026-07-11-jira-operating-batch-design.md
"""
import argparse
import asyncio
import datetime
import json
import sys
from pathlib import Path

import httpx
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib import triage, triage_html
from hublib.jira import client_from_env
from hublib.shellenv import load_env


def _jira_cfg(root, feature):
    """The feature's jira: block. None = unknown feature, {} = no scope."""
    p = root / "features" / "features.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) if p.is_file() else {}
    for f in (data or {}).get("features") or []:
        if isinstance(f, dict) and f.get("id") == feature:
            return f.get("jira") or {}
    return None


async def _scan(root, feature, out, today):
    cfg = _jira_cfg(root, feature)
    if cfg is None:
        print(f"ERROR unknown feature '{feature}' (not in features/features.yaml)")
        return 2
    if not cfg.get("jql"):
        print(f"ERROR no stored jira scope for '{feature}' - run hub.jira-sweep "
              f"scope discovery first")
        return 2

    jql = triage.compose_jql(cfg["jql"])
    print(f"scope: {jql}")
    async with client_from_env() as client:
        rows = await triage.scan(client, jql, today)
        base = client.base_url

    out.mkdir(parents=True, exist_ok=True)
    report = out / f"triage-{feature}-{today.isoformat()}.html"
    report.write_text(triage_html.render(feature, jql, rows, today, base),
                      encoding="utf-8", newline="\n")
    rows_path = out / f"rows-{feature}.json"
    rows_path.write_text(json.dumps(rows, indent=2), encoding="utf-8",
                         newline="\n")

    counts = {}
    for row in rows:
        counts[row["classification"]] = counts.get(row["classification"], 0) + 1
    summary = " · ".join(f"{v} {k}" for k, v in sorted(counts.items()))
    print(f"scanned {feature}: {len(rows)} open RFE(s) ({summary})")
    print(f"report: {report}")
    print(f"rows:   {rows_path}")
    print("NOTE the report carries live Jira summaries. It belongs under "
          "restricted/, never in the tracked tree (this repo is PUBLIC).")
    return 0


def _print_gate(plan):
    """The gate table. Transitions first and separate: they are the
    destructive ones (spec decision 3)."""
    if plan["transitions"]:
        print(f"\nTRANSITIONS ({len(plan['transitions'])})")
        for item in plan["transitions"]:
            t = item["transition"]
            line = (f"  {item['key']}: {item['from']} -> "
                    f"{t.get('to') or t.get('name')}")
            if item.get("comment"):
                line += f'  (+comment "{item["comment"][:60]}")'
            print(line)
    if plan["labels"]:
        print(f"\nLABELS ({len(plan['labels'])})")
        for item in plan["labels"]:
            print(f"  {item['key']}: +{item['label']}")
    if plan["comments"]:
        print(f"\nCOMMENTS ({len(plan['comments'])})")
        for item in plan["comments"]:
            print(f'  {item["key"]}: "{item["comment"][:80]}"')
    if plan["skipped"]:
        print(f"\nSKIPPED ({len(plan['skipped'])})")
        for item in plan["skipped"]:
            print(f"  {item['key']}: {item['detail']}")
    if plan["rejected"]:
        print(f"\nREJECTED ({len(plan['rejected'])})")
        for item in plan["rejected"]:
            print(f"  {item['key']}: {item['action']} - {item['detail']}")
    total = len(plan["transitions"]) + len(plan["labels"]) + len(plan["comments"])
    print(f"\n{total} Jira mutation(s) staged. Nothing has been written yet.")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _plan_from(decisions_path, rows_path):
    payload = _load(decisions_path)
    decisions = payload.get("decisions") or {}
    rows = _load(rows_path)
    return triage.plan_decisions(decisions, rows), rows


async def _apply(decisions_path, rows_path, feature, out, today):
    plan, rows = _plan_from(decisions_path, rows_path)
    _print_gate(plan)

    async with client_from_env() as client:
        result = await triage.apply_decisions(client, plan)

    cfg_jql = _load(decisions_path).get("jql", "")
    out.mkdir(parents=True, exist_ok=True)
    log_path = out / f"triage-log-{feature}.yaml"
    log_path.write_text(
        triage.build_triage_log(feature, cfg_jql, rows, plan, result, today),
        encoding="utf-8", newline="\n")

    print(f"\napplied {len(result['applied'])} · skipped {len(result['skipped'])}"
          f" · rejected {len(result['rejected'])} · errors {len(result['errors'])}")
    for item in result["applied"]:
        print(f"  OK       {item['key']}: {item['detail']}")
    for item in result["errors"]:
        print(f"  ERROR    {item['key']}: {item['detail']}")
    print(f"proposed log: {log_path}")
    return 1 if result["errors"] else 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scan", metavar="FEATURE")
    ap.add_argument("--plan", metavar="DECISIONS_JSON")
    ap.add_argument("--apply", metavar="DECISIONS_JSON")
    ap.add_argument("--rows", metavar="ROWS_JSON")
    ap.add_argument("--feature", metavar="FEATURE")
    ap.add_argument("--out", metavar="DIR")
    ap.add_argument("--root", help=argparse.SUPPRESS)  # tests only
    args = ap.parse_args(argv)

    modes = [args.scan is not None, args.plan is not None, args.apply is not None]
    if sum(modes) != 1:
        ap.error("pick exactly one mode: --scan | --plan | --apply")
    if args.scan is not None and not args.out:
        ap.error("--out DIR is required with --scan "
                 "(proposals are written there, never into the repo)")
    if args.plan is not None and not args.rows:
        ap.error("--rows ROWS_JSON is required with --plan")
    if args.apply is not None and not (args.rows and args.feature and args.out):
        ap.error("--apply needs --rows ROWS_JSON, --feature FEATURE and --out DIR")

    root = Path(args.root) if args.root else Path(__file__).resolve().parents[1]
    today = datetime.date.today()
    load_env(root, prefixes=("JIRA_",))

    try:
        if args.scan is not None:
            return asyncio.run(_scan(root, args.scan, Path(args.out), today))
        if args.plan is not None:
            plan, _ = _plan_from(args.plan, args.rows)
            _print_gate(plan)
            return 0
        return asyncio.run(_apply(args.apply, args.rows, args.feature,
                                  Path(args.out), today))
    except RuntimeError as exc:
        print(f"ERROR {exc}")
        return 1
    except httpx.HTTPStatusError as exc:
        code = exc.response.status_code
        if code in (401, 403):
            print(f"ERROR jira auth failed ({code}) - JIRA_TOKEN expired? "
                  f"Generate a new API token at https://id.atlassian.com/"
                  f"manage-profile/security/api-tokens, update JIRA_TOKEN in "
                  f"restricted/.env, re-run. (Token values are never printed.)")
        else:
            print(f"ERROR jira request failed: {code} on {exc.request.url}")
        return 1
    except httpx.HTTPError as exc:
        print(f"ERROR network failure talking to Jira: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_hub_triage.py -v`
Expected: 6 PASS.

- [ ] **Step 5: Full suite + lint**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: all PASS, `0 error(s), 81 warning(s)`, `0 stale file(s)`.

- [ ] **Step 6: Commit**

```bash
git add scripts/hub_triage.py scripts/tests/test_hub_triage.py
git diff --cached --stat
git commit -m "feat(triage): hub_triage.py CLI, scan/plan/apply (#29)

--out is mandatory, so the CLI never writes into the repo. --plan renders
the gate table with zero network calls, which is what the skill shows before
anything fires.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 9: `hub.jira-triage` skill + disclosure coverage

**Files:**
- Create: `.claude/skills/hub.jira-triage/SKILL.md`
- Modify: `scripts/hublib/disclosure.py` (the `_scan_files` surfaces tuple)
- Test: `scripts/tests/test_disclosure.py` (append)

**Interfaces:**
- Consumes: `hub_triage.py` (Task 8).
- Produces: the skill. Closes #29.

- [ ] **Step 1: Write the failing test**

Append to `scripts/tests/test_disclosure.py`:

```python
def test_triage_log_is_in_the_scan_surface(tmp_path):
    # The tracked triage log is a new public surface. If the disclosure net
    # does not scan it, a future change to the log format could leak Jira
    # prose into a PUBLIC repo without anything noticing.
    from hublib import disclosure

    p = tmp_path / "features" / "mcp-registry" / "work" / "triage-log.yaml"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("feature: mcp-registry\n", encoding="utf-8", newline="\n")

    scanned = [f.name for f, _ in disclosure._scan_files(tmp_path)]
    assert "triage-log.yaml" in scanned
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest scripts/tests/test_disclosure.py -v -k triage`
Expected: FAIL with `AssertionError: assert 'triage-log.yaml' in []`.

- [ ] **Step 3: Implement the disclosure coverage**

In `scripts/hublib/disclosure.py`, in the `surfaces` tuple inside `_scan_files`,
add one line directly after the `jira-snapshot.yaml` entry:

```python
        ("features/*/work/jira-snapshot.yaml", False),
        ("features/*/work/triage-log.yaml", False),
        ("features/*/work/refresh-*.yaml", False),
```

- [ ] **Step 4: Write the skill**

Create `.claude/skills/hub.jira-triage/SKILL.md`:

```markdown
---
name: hub.jira-triage
description: Run the RFE triage ceremony for one feature - scan its open Feature Requests, flag staleness, suggest actions, review them in a browser report, then batch-apply the decisions back to Jira through an inline gate. Use when the user says "triage the RFEs for <feature>", "run a triage pass", "what RFEs need attention", or on a periodic triage cadence. WRITES TO JIRA (adds labels, posts comments, and fires the close and approve transitions) - every mutation is gated line by line and nothing fires before approval. It cannot assign, edit fields, or create issues.
---

# hub.jira-triage

Input: a feature id (its `jira:` scope in features.yaml supplies the JQL).
Spec: [/docs/specs/2026-07-11-jira-operating-batch-design.md](/docs/specs/2026-07-11-jira-operating-batch-design.md).

This is the ONLY skill in the hub with a Jira write surface. Every other
hub.jira-* skill is read-only, and that is deliberate: keep it that way.

1. PRE-FLIGHT. `python scripts/hub_jira.py --check`. On failure, stop and point
   at `bash scripts/doctor.sh check` (section 4). No retry loop.
   Confirm `restricted/` exists. If it does not, STOP: the report carries live
   Jira summaries and this repo is PUBLIC. Never fall back to a tracked path.
2. SCOPE. `python scripts/hub_triage.py --scan <feature> --out <scratch>` echoes
   the composed JQL (the feature's stored scope narrowed to open Feature
   Requests) before it fetches. Read it back to the human and confirm.
   Unknown feature or no stored scope: exit 2, offer hub.jira-sweep.
3. REVIEW. Move the report to
   `restricted/features/<feature>/work/triage-<date>.html` and tell the human
   to open it. Keep `rows-<feature>.json` in scratch: the apply step needs it.
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
   --rows <rows.json> --feature <feature> --out <scratch>`. Labels land, then
   comments, then transitions. Report applied/skipped/rejected/errors and name
   every transition that fired.
6. RECORD. Copy the proposed `triage-log-<feature>.yaml` to
   `features/<feature>/work/triage-log.yaml`. It carries no Jira prose by
   design: never add summaries or comment bodies to it.
   `python scripts/hub_index.py` then `python scripts/hub_lint.py` (0 errors).
7. COMMIT. Stage explicitly, NEVER `git add -A` (shared checkout; see
   fact-concurrent-session-git-hygiene). Check `git diff --cached --stat`, then:
   `git commit -m "triage(<feature>): <n> issues, <m> applied" -- features/<feature>/work/triage-log.yaml <regenerated indexes>`
   and `git push`.

NEVER: write the HTML report into the tracked tree; put a Jira summary or
comment body into triage-log.yaml; apply a decisions file without showing the
gate table first; retry a rejected transition by picking a different one.
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_disclosure.py -v`
Expected: all PASS, including `test_triage_log_is_in_the_scan_surface`.

- [ ] **Step 6: Full suite + lint**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: all PASS, `0 error(s), 81 warning(s)`, `0 stale file(s)`.

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/hub.jira-triage/ scripts/hublib/disclosure.py scripts/tests/test_disclosure.py
git diff --cached --stat
git commit -m "feat(skill): hub.jira-triage, the hub's only Jira write surface (#29)

The tracked triage log joins the disclosure scan surface, so a future change
to its format cannot quietly leak Jira prose into a PUBLIC repo.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 10: Docs, conventions, backlog, and log

**Files:**
- Modify: `AGENTS.md` (skills table: two new rows)
- Modify: `docs/skills.md`, `docs/tooling.md`
- Modify: `conventions/layout.md` (name `triage-log.yaml` as machine-written)
- Modify: `docs/enhancements.md` (#30, #27, #29 to Done, with the carve-outs)
- Create: `memory/facts/fact-jira-write-surface.md`
- Modify: `memory/log.md`

**Interfaces:**
- Consumes: everything above.
- Produces: nothing. This is the paperwork task.

- [ ] **Step 1: AGENTS.md skills table**

Add two rows to the hub skills table, after the `hub.jira-sync` row:

```markdown
| hub.jira-triage | run the RFE triage ceremony for a feature - scan, review in a browser, gated batch write-back to Jira (labels, comments, close, approve) |
| hub.jira-hygiene | audit one Jira issue against its type checklist (read-only) |
```

Check the 150-line CI budget: `wc -l AGENTS.md` must be under 150.

- [ ] **Step 2: docs/skills.md and docs/tooling.md**

In `docs/skills.md`, document the two new skills alongside the existing
`hub.jira-*` entries, and state plainly that `hub.jira-triage` is the only
skill that writes to Jira, with the exact bounded surface (labels, comments,
close, approve) and the gate.

In `docs/tooling.md`, document `scripts/hub_triage.py` beside `hub_jira.py`:
the three modes, the mandatory `--out`, and that `--scan` and `--plan` are
read-only while `--apply` writes.

- [ ] **Step 3: conventions/layout.md**

Where `work/` is described, name the new file alongside `jira-snapshot.yaml`:

```
`triage-log.yaml` (machine-written by hub.jira-triage; tracked; carries no
Jira prose by design, so it needs no redaction in this PUBLIC repo)
```

- [ ] **Step 4: docs/enhancements.md**

Remove rows 27, 29 and 30 from the priority table. Add to `## Done`, at the
top:

```markdown
- **#30 + #27(b) + #29 Jira operating batch** - shipped 2026-07-11: the three
  capabilities unblocked by #2's client. `hub.jira-hygiene` audits one issue
  against type checklists (read-only; pm-toolkit's Create mode ruled out).
  `hub.research` gains the `jira-gap` lens, promoted from FUTURE, driven by the
  domain YAML's `jira:` block ("what we are NOT building" is the payload).
  `hub.jira-triage` runs the triage ceremony and makes **the first Jira write
  in this hub's history**, bounded to labels, comments, and the close and
  approve transitions, every one of them gated line by line.
  Spec: [/docs/specs/2026-07-11-jira-operating-batch-design.md](/docs/specs/2026-07-11-jira-operating-batch-design.md).
  Plan: [/docs/plans/2026-07-11-jira-operating-batch-plan.md](/docs/plans/2026-07-11-jira-operating-batch-plan.md).
  **NOT a complete pm-toolkit port, deliberately** - do not read "Done" as
  "everything came over". Ruled out: assignment, field edits, issue creation
  (owner ruling, spec decision 2). Deferred, still available if wanted:
  cross-component discovery (needed an "adjacent components" config that does
  not exist, spec decision 5) and comment-thread digests (needed an LLM
  provider key, which the 2026-07-08 ruling forbids, spec decision 6). The
  83-row pm-component-ownership registry was not ported: real names and emails
  cannot enter a public repo, and feature JQL scopes replace it.
```

- [ ] **Step 5: The durable fact**

The write-posture change reverses a documented invariant, so it needs a fact,
not just a log line. Create `memory/facts/fact-jira-write-surface.md`:

```markdown
---
type: fact
description: "The hub can now WRITE to Jira, but only via hub.jira-triage and only labels, comments, close and approve - every other Jira skill is still read-only"
timestamp: 2026-07-11
status: current
---
Until 2026-07-11 every Jira skill in the hub was read-only, and
`hublib/jira.py`'s write methods (`update_issue`, `add_comment`,
`transition_issue`, `create_issue`) were dead code carried for a future
backlog item. The Jira operating batch (#29) turned the first three on.

**The exact surface, and it is deliberately small:**
- `hub.jira-triage` is the ONLY skill that writes to Jira.
- It may: add a label, post a comment, fire the `close` transition, fire the
  `approve` transition.
- It may NOT: assign, edit arbitrary fields, or create issues. `create_issue`
  is still dead code. `<release>-committed` labels are never written.
- Every mutation is gated line by line. Transitions are resolved during the
  scan and rendered separately at the gate, so the gate names what will fire
  and an unresolvable transition is rejected rather than half-applied.

**Do not generalize.** `hub.jira-sweep`, `hub.jira-sync` and `hub.jira-hygiene`
still say "read-only against Jira" in their descriptions and that is still
true. A future agent reading one of those must not conclude the hub is
read-only overall, nor that the write door is open wider than these four
actions.

See [[fact-hub-design-decisions]]. Spec:
[/docs/specs/2026-07-11-jira-operating-batch-design.md](/docs/specs/2026-07-11-jira-operating-batch-design.md).
```

- [ ] **Step 6: The log line**

Append to `memory/log.md`:

```markdown
- 2026-07-11 - **Creation** - Jira operating batch shipped (#30, #27b, #29):
  hub.jira-hygiene (audit-only), the hub.research jira-gap lens (promoted from
  FUTURE), and hub.jira-triage, which makes the first Jira write in the hub's
  history - labels, comments, close and approve, all gated. Transitions resolve
  before the gate so nothing half-applies (the pm-toolkit close_stale bug).
  Full-fidelity report lives in restricted/; the tracked triage-log.yaml is
  prose-free by design. Ruled out: assign, field edits, issue creation.
  Deferred: cross-component discovery, comment digests.
  New fact: fact-jira-write-surface.
```

- [ ] **Step 7: Reindex, lint, verify**

Run: `python scripts/hub_index.py && python scripts/hub_lint.py && python scripts/hub_index.py --check && python -m pytest scripts/tests -v && wc -l AGENTS.md`
Expected: `0 error(s)`, warnings not above 81 plus at most 1 new (the new fact
may trip the restricted-content heuristic; if it does, triage it as benign and
extend `fact-disclosure-warning-triage-2026-07-10` rather than editing the
scanner). `0 stale file(s)`. All tests PASS. AGENTS.md under 150 lines.

- [ ] **Step 8: Commit**

```bash
git add AGENTS.md docs/skills.md docs/tooling.md conventions/layout.md docs/enhancements.md memory/facts/fact-jira-write-surface.md memory/log.md memory/index.md views/ features/index.md
git diff --cached --stat
git commit -m "docs: Jira operating batch paperwork (#30, #27b, #29)

Backlog rows move to Done with the carve-outs named, so a future session does
not read 'Done' as 'fully ported'. New fact records the write-surface change:
it reverses a documented invariant, and the other Jira skills are still
read-only.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 11: Full verification and push

**Files:** none (verification only).

- [ ] **Step 1: Clean-tree check**

Another session may be working in this clone.

Run: `git status --short`
Expected: empty. If not, STOP and reconcile before pushing.

- [ ] **Step 2: Full local verification**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: all PASS. `0 error(s)`. `0 stale file(s)`.

- [ ] **Step 3: Confirm the write surface is exactly what was ruled**

Prove by grep that nothing wandered outside the four allowed actions.

Run: `grep -rn "create_issue\|assignee\|\"name\":" scripts/hublib/triage.py scripts/hub_triage.py`
Expected: no hit that performs a write. `create_issue` must appear NOWHERE in
the triage code. If it does, the scope was exceeded: stop and remove it.

- [ ] **Step 4: Push and watch CI**

```bash
git push
gh run watch --exit-status
```
Expected: `validate.yml` green (pytest, hub_lint, hub_index --check).

- [ ] **Step 5: Confirm the report never entered the tracked tree**

Run: `git log --oneline --all -- 'features/*/work/triage-*.html' | head`
Expected: empty. The HTML report must exist only under `restricted/` (gitignored)
and in scratch. If anything shows here, it is a disclosure incident: the repo is
PUBLIC and the report carries live Jira summaries.

---

## Acceptance runs (owner-in-the-loop - NOT subagent tasks)

Live sessions with Peter at the gates and real Jira access, after the plan
lands. Findings become skill or CLI edits (normal commits), not plan changes.
Update this list in place after each run with the commit SHA, the date, and
what was learned.

- [ ] 1. **A hygiene audit on a known-messy issue.** Pick something real with a
  missing link or an absent Fix Version. Does the checklist catch it? Does the
  audit dump carry enough to judge every line, or does it force too many
  Warnings for "cannot evaluate from the dump"? That answer edits
  `--audit`'s field list.

- [ ] 2. **A jira-gap lens run on a feature with a live scope** (mcp-registry
  is the only one with a stored JQL today). The test is direction B: does the
  "what we are NOT building" table say anything Peter did not already know? If
  it does not, the lens is decoration and the domain `jira:` JQL is the thing
  to fix.

- [ ] 3. **A triage pass approved for LABELS AND COMMENTS ONLY.** Deliberately
  no transitions on the first live run. This proves the whole chain end to end
  (scope, scan, report, browser export, gate table, apply, log, commit) while
  the sharpest action stays holstered. Confirm: the report opened from
  `restricted/` and renders real summaries; the exported JSON round-tripped;
  the gate table matched what was clicked; `triage-log.yaml` landed tracked
  with NO Jira prose in it.

- [ ] 4. **A triage pass that fires a real `close` and a real `approve`.** Only
  after run 3 passes. Pick the issues deliberately. This is the first
  irreversible-feeling thing the hub does: a close is reopenable, but it
  notifies reporters and watchers and that cannot be taken back. Confirm the
  gate named the exact transition before it fired, and that the log recorded
  it. Then check the issues in Jira by hand.

- [ ] 5. **A triage pass against a workflow with no matching close transition.**
  The rejection path is the one that matters most and the one least likely to
  be exercised by accident. Confirm the gate rejects it with a readable reason
  and that NO comment was posted on the issue that stayed open (the pm-toolkit
  half-apply bug this design exists to prevent).
