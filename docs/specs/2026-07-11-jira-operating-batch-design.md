# Jira operating batch (#30, #27, #29) - design spec

- **Date:** 2026-07-11 · **Owner:** Peter Double · **Status:** approved design, pre-implementation
- **Closes:** enhancements backlog #30 (audit-only: Create mode ruled out),
  #27(b) (fully), #29 (the write surface is narrowed to labels, comments, and
  the close/approve transitions, see decision 2; cross-component discovery and
  comment digests deferred, see decisions 5 and 6). Builds entirely on
  `scripts/hublib/jira.py`, which shipped 2026-07-10 with #2.
- **Posture change:** this batch makes the first Jira write in the hub's
  history. Every existing Jira skill advertises "Read-only against Jira"; that
  invariant now holds for all of them except `hub.jira-triage`.

## Problem

The hub can read Jira and file it (#2 shipped `hublib/jira.py`, `hub_jira.py`,
`hub.jira-sweep`, `hub.jira-sync`, tracked `work/jira-snapshot.yaml`, and
`views/jira-map.md`). What it cannot do is *operate* on Jira. Three gaps,
all named in `docs/enhancements.md` and all blocked on nothing but this spec:

- **#30** There is no way to ask "is this issue well formed?" The conventions
  exist (naming prefixes, parent links, clone links, Fix Version, Components,
  refinement docs) but they live in people's heads and in a pm-toolkit prose
  file, so they are applied unevenly.
- **#27(b)** `hub.research` has five lenses; the sixth, `jira-gap`, is stubbed
  as FUTURE in `.claude/skills/hub.research/SKILL.md:16` and has a reserved,
  commented-out `jira:` block waiting for it in
  `.claude/skills/hub.research/domains/redhat-ai.yaml:74`. Without it, research
  tells us what the industry is doing but never crosses that against what we
  have actually committed to build, so the "what we are NOT building" early
  warning never fires.
- **#29** RFE triage is a recurring ceremony done by hand in the Jira UI. There
  is no staleness detection, no suggestion engine, and no batch apply.

The source material is pm-toolkit (`C:/Users/peter/code/rh/pm-toolkit`,
read-only). Its shape is not what the backlog implies: only `rfe-triage`
carries real code (`scripts/analysis/triage.py`, 786 lines, plus
`scripts/presentation/triage_html.py`, 438 lines). `jira-hygiene` is 100%
prose (a 158-line SKILL.md plus a 242-line reference template, zero Python),
and `jira-gap` does not exist as a skill at all: the capability is Phase 3 of
pm-toolkit's `research` skill, also pure prose plus domain YAML. So this batch
is one code port and two prompt/config ports. Per the standing preference,
each is a review/optimize/enhance pass, not a lift-and-shift.

## Decisions made during brainstorming

1. **One spec, three parts, sequenced by ascending risk.** #30 (read-only
   prose) lands first, then #27(b) (prose plus YAML), then #29 (new code and
   the first Jira write this hub has ever made). The three share a spine (the
   same client, the same `features.yaml` JQL scope, the same inline gate), so
   a single spec is not artificial bundling. The file touches are conflict
   free, so a stall on any one part does not block the others.

2. **The write door opens to labels, comments, and the two triage
   transitions, always gated.** Every Jira skill in the hub today advertises
   "Read-only against Jira" and nothing calls the client's write methods. This
   batch changes that, and the change is bounded by owner ruling:
   `hub.jira-triage` may **add labels**, **post comments**, and **transition
   issues via `close` and `approve`**. It may not change assignees, edit
   arbitrary fields, or create issues. Rationale for including transitions
   (owner ruling 2026-07-11, amending an earlier narrower call): closing stale
   RFEs and approving ready ones are the headline moves of a triage ceremony,
   and a triage that can only relabel is not really a triage. Consequences:
   pm-toolkit's `assign` and `claim_component` actions are not ported; #30
   loses its Create mode entirely and becomes audit-only; the `create_link`
   method that pm-toolkit references but never implements does not need to be
   written. The write surface stays in exactly one skill, so the posture is
   legible at the point of use.

3. **Transitions are resolved before the gate, never during apply.**
   pm-toolkit's `close_stale` posts its comment first, then fetches
   `get_transitions`, string-matches the name, and if nothing matches it logs a
   warning and no-ops, having already left the comment behind. That half-apply
   is unacceptable in a gated system. Here, the scan resolves each `close` and
   `approve` candidate's available transitions up front, so the gate line names
   the transition that will actually fire (`RHAIRFE-2630: Open -> Closed
   (+comment)`). An issue whose workflow offers no matching transition is
   **rejected at the gate with a reason**, and neither its comment nor its
   transition is attempted. Matching is case-insensitive over
   `("closed", "resolved", "close issue", "done")` for close and
   `("approved", "approve")` for approve; an ambiguous match (more than one
   candidate) is also rejected rather than guessed. Transitions are the
   sharpest tool in the batch: they are visible to reporters and watchers and
   they fire notifications, so they are rendered distinctly at the gate rather
   than mixed in with label lines.

4. **The full-fidelity triage report is restricted; the tracked record is
   prose free.** `solaius/rhoai-agentic-hub` is PUBLIC on github.com (verified
   2026-07-11: `"isPrivate": false`). A useful triage report must render
   authenticated Jira text (summaries, statuses, assignees) that the
   fail-closed probe rule forbids in tracked files, and `redhat.atlassian.net`
   serves nothing anonymously (all 35 summaries in the mcp-registry snapshot
   are `null`). Tracked-and-redacted would be a report you cannot triage from;
   tracked-and-unredacted would be a leak. So the two concerns split: the HTML
   report is written to `restricted/features/<f>/work/` (gitignored, full
   fidelity, no redaction needed because it never enters the public repo), and
   a tracked `features/<f>/work/triage-log.yaml` records the decisions with no
   Jira prose in it at all. The log satisfies the disclosure net by
   construction rather than by redaction.

5. **Triage scope reuses the `features.yaml` `jira:` scopes.** pm-toolkit
   scopes by Jira component via an 83-row registry of real Red Hat names and
   emails, which cannot enter a public repo and would be a second scope
   language besides. Instead `hub.jira-triage <feature>` reads the feature's
   stored JQL, the same one `hub.jira-sweep` and `hub.jira-sync` already use,
   and layers the RFE filter on top. This holds spec decision 6 of the #2
   design ("JQL is the single stored scope language"). The ownership registry
   is not ported. Cross-component discovery is dropped with it (it needed an
   "adjacent components" config that does not exist).

6. **No LLM-provider credentials, so comment digests are dropped.**
   pm-toolkit's triage calls Anthropic/Vertex/Bedrock from Python
   (`scripts/clients/claude.py`) to summarize comment threads. The standing
   owner ruling (2026-07-08, recorded in the preferences profile) is no
   LLM-provider credential handling anywhere in the hub. That module is not
   ported. Comment digests were scoped out of this batch entirely, which
   removes the last reason it existed and also removes the per-issue comment
   fetch (the slowest part of a run). Classification never needed comments:
   it reads status, labels, links and dates. Note the asymmetry: triage never
   *reads* comment threads, but `comment` remains a supported *write* action
   (decision 2). Reading digests needed an LLM call; posting a comment does
   not.

7. **The browser is the input device; the gate is the authority.** Clicking
   through 40 dropdowns is faster than typing 40 decisions, so the HTML report
   keeps its per-row `<select>` and Export Decisions button. But the exported
   JSON is a *proposal*, not a command: the skill reads it and raises the
   standard inline batch gate, one line per Jira mutation, before anything
   fires. pm-toolkit applies the JSON directly with no confirm step, which is
   the one pattern in it that contradicts how every other hub skill works.

8. **The suggestion engine is ported; the markdown report is not.**
   `flag_staleness`, `classify_rfe` and `suggest_action` (the 8 ordered rules,
   90-day and 270-day staleness thresholds) are pure functions and are most of
   what makes the report smarter than a saved Jira filter. pm-toolkit has zero
   tests for them; they get real unit tests here.
   `format_triage_report()` (~190 lines of markdown generation) is superseded
   by the HTML, unreferenced by pm-toolkit's own happy path, and is dropped.

9. **Two upstream bugs are fixed rather than ported.** `assign_issue` sends
   `{"assignee": {"name": ...}}`, which is Data Center syntax against a Cloud
   instance (moot anyway, since assignment is out of scope by decision 2). And
   the decisions export scrapes its scope from
   `document.title.split(' — ')[1]`, an em-dash string split that is brittle
   and collides with the no-em-dashes preference; scope is embedded in a
   `data-` attribute instead.

## Architecture

| path | holds |
|---|---|
| `scripts/hublib/triage.py` | pure functions (`flag_staleness`, `classify_rfe`, `suggest_action`), the RFE fetch, transition resolution (`resolve_transition`), and `apply_decisions` (labels, comments, close/approve transitions) |
| `scripts/hublib/triage_html.py` | renders the self-contained report; no network, no repo writes |
| `scripts/hub_triage.py` | CLI: `--scan <feature> --out DIR` and `--apply <decisions.json> [--dry-run]` |
| `.claude/skills/hub.jira-triage/SKILL.md` | the triage ceremony; writes labels and comments to Jira, gated |
| `.claude/skills/hub.jira-hygiene/SKILL.md` | audit one issue against type checklists; read-only |
| `.claude/skills/hub.jira-hygiene/checklists.md` | reference doc (hierarchy, lifecycle, link matrix, naming), ported from pm-toolkit's template |
| `features/<f>/work/triage-log.yaml` | tracked, machine-written, prose free: the durable record of each triage pass |
| `restricted/features/<f>/work/triage-<date>.html` | gitignored, full fidelity: the working report |
| `scripts/tests/test_triage.py`, `scripts/tests/test_hub_triage.py` | offline tests, `httpx.MockTransport` |

Modified: `scripts/hub_jira.py` gains `--audit KEY` (a structured issue dump
for #30 to judge, read-only); `.claude/skills/hub.research/SKILL.md` promotes
`jira-gap` from FUTURE to live; `conventions/research.md` adds `jira-gap` to
the `lens` enum; `.claude/skills/hub.research/domains/redhat-ai.yaml` fills its
reserved `jira:` block; `scripts/hublib/disclosure.py` adds
`features/*/work/triage-log.yaml` to its scan tuple.

### `features/<f>/work/triage-log.yaml` (tracked, public, prose free)

```yaml
# generated by hub.jira-triage (scripts/hub_triage.py) - do not hand-edit
feature: mcp-registry
jql: <the feature scope, plus the RFE filter>
triaged: '2026-07-11'
issues:
- key: RHAIRFE-2630
  flags: [no_update_112d, no_assignee]
  suggestion: backlog
  decision: backlog
  outcome: applied          # applied | skipped | rejected | error
  labels_added: [pm-backlogged]
  transition: null
- key: RHAIRFE-2644
  flags: [no_update_301d]
  suggestion: close
  decision: close
  outcome: applied
  labels_added: []
  transition: Open -> Closed
- key: RHAIRFE-2650
  flags: []
  suggestion: roadmap
  decision: skip
  outcome: skipped
  labels_added: []
  transition: null
```

No summaries, no comment bodies, no assignee names: nothing here is Jira prose,
so there is nothing for the probe rule to redact. The `transition` field
records status names, which are workflow vocabulary rather than issue content,
and are therefore safe. Field order is fixed and the file is byte-stable
(`yaml.safe_dump(sort_keys=False)`), matching `jira-snapshot.yaml`.

The log is the audit trail for a capability that can now close issues, so it
records `rejected` outcomes too (for example, a `close` whose transition could
not be resolved), not just what succeeded.

### Decisions JSON (scratch only, the browser's proposal)

```json
{"exported_at": "2026-07-11", "feature": "mcp-registry",
 "decisions": {"RHAIRFE-2630": {"action": "backlog", "release": null,
                                "comment": null,
                                "current_labels": ["mcp", "3.6-candidate"]}}}
```

`current_labels` round-trips through a hidden cell so label writes stay
read-modify-write and idempotent (pm-toolkit's discipline, kept). `feature`
comes from a `data-feature` attribute, not a title scrape (decision 8).

### Action vocabulary (the entire write surface)

| action | Jira effect | kind |
|---|---|---|
| `roadmap` | adds `<release>-candidate` | label |
| `backlog` | adds `pm-backlogged` | label |
| `needs-uxd` | adds `needs-uxd` | label |
| `clarify` | adds `pm-needs-clarification` | label |
| `comment` | posts a comment (free text, shown in full at the gate) | comment |
| `close` | posts a comment, then transitions to the resolved close transition | **transition** |
| `approve` | transitions to the resolved approve transition | **transition** |
| `skip` | nothing | none |

Any other action value in a decisions JSON (`assign`, `claim_component`, or
anything unrecognized) is **rejected at the gate with a reason**, never
silently dropped. `<release>-committed` is read-only by policy and is never
written.

The two transition actions carry extra ceremony (decision 3): their target
transition is resolved during the scan, the gate renders them in a separate,
visually distinct block from the label lines, and an unresolvable or ambiguous
transition is rejected rather than attempted. `close` applies its comment and
its transition as a unit: if the transition cannot be resolved, the comment is
not posted either, which is the half-apply bug pm-toolkit ships.

`close` uses pm-toolkit's default comment body ("Closed during PM triage pass.
Reopen if still needed.") unless the row supplies its own text. Closing is
reversible (an issue can be reopened) but it is not quiet: it notifies
reporters and watchers.

### Data flow (#29)

`features.yaml jira: scope` + RFE filter → `hub_triage.py --scan` fetches (+
flags + suggests) → `triage_html.py` writes the report to `restricted/…` →
human clicks → Export Decisions → JSON in scratch → skill reads it → **inline
batch gate** (one line per Jira mutation) → `apply_decisions` writes labels and
comments → `work/triage-log.yaml` → `hub_index.py` → `hub_lint.py` → commit
with explicit pathspecs.

Two invariants carried from `hub_jira.py` unchanged: the CLI **never writes
into the repo** (`--out DIR` is required; repo writes happen in the skill,
after the gate), and nothing reaches Jira before the gate says OK.

## Skill flows

### `hub.jira-triage <feature>`

1. **PRE-FLIGHT.** `hub_jira.py --check`. On failure, stop and point at
   `bash scripts/doctor.sh check` (section 4). No retry loop. If
   `restricted/` does not exist, refuse to run rather than falling back to a
   tracked path.
2. **SCOPE.** Read the feature's `jira: jql` from `features.yaml`; layer on
   `AND issuetype = "Feature Request" AND resolution = Unresolved`. Echo the
   composed JQL and the issue count; confirm before fetching. Unknown feature
   or no stored scope: exit 2, offer `hub.jira-sweep` to establish one.
3. **SCAN.** `hub_triage.py --scan <feature> --out <scratch>`: fetch, flag,
   classify, suggest, resolve transitions for every close/approve candidate
   (decision 3), render.
4. **REVIEW.** Report written to
   `restricted/features/<f>/work/triage-<date>.html`. Tell the human to open
   it. Three sections (Untriaged, Waiting on Input, Backlogged) plus stat
   tiles; each row carries a pre-selected suggestion and a reason badge.
5. **GATE.** Read the exported decisions JSON. Present one batch table, one
   line per Jira mutation, with **transitions in their own block above the
   label lines** because they are the destructive ones:

   ```
   TRANSITIONS (2)
     RHAIRFE-2644: Open -> Closed  (+comment "Closed during PM triage pass...")
     RHAIRFE-2651: Stakeholder Review -> Approved
   LABELS (3)
     RHAIRFE-2630: +pm-backlogged
     RHAIRFE-2633: +3.6-candidate
     RHAIRFE-2637: +needs-uxd
   COMMENTS (1)
     RHAIRFE-2640: "<full text>"
   REJECTED (1)
     RHAIRFE-2648: close - no matching transition in this workflow
   ```

   Approve/edit/reject per line. Nothing touches Jira before OK. Unsupported
   actions and unresolvable transitions appear under REJECTED with the reason,
   never silently dropped.
6. **APPLY.** `apply_decisions`, per-item try/except, returns
   `{applied, skipped, rejected, errors}`. A label already present is an
   idempotent no-op, reported as skipped. Transitions are applied last, after
   all label and comment writes have settled, so a workflow surprise on the
   sharpest action cannot strand the cheap ones.
7. **RECORD.** Write `work/triage-log.yaml`. Run `hub_index.py` then
   `hub_lint.py` (0 errors). Commit with explicit pathspecs, never
   `git add -A` (shared checkout; see `fact-concurrent-session-git-hygiene`):
   `git commit -m "triage(<feature>): <n> issues, <m> applied" -- <paths>`.
   Report applied/skipped/rejected/errors counts, naming every transition that
   fired.

### `hub.jira-hygiene audit <KEY>`

Read-only, no new module: the client already has `get_issue_with_links`.

1. **PRE-FLIGHT.** `hub_jira.py --check`.
2. **FETCH.** `hub_jira.py --audit <KEY>` dumps the issue (links, components,
   labels, fix versions, description) as structured YAML to stdout.
3. **JUDGE.** Branch on issue type and walk the matching checklist from
   `checklists.md`: RHAIRFE Feature Request, RHAISTRAT Feature (11 checks),
   maturity-chain DP/TP/GA, RHAIENG Epic, plus the all-issues basics.
4. **REPORT.** Emit a `Check | Pass/Fail/Warning | Detail` table plus
   prioritized fix recommendations, in chat. No file written.
5. **HAND OFF.** The skill reports; it does not fix. Fixes go through
   `hub.jira-triage`'s comment action or the human in Jira. `help` mode
   explains the hierarchy and lifecycle from the same `checklists.md`.

### `hub.research jira-gap <feature>`

No new code. The lens is dispatched exactly like `competitive`.

1. The domain YAML's `jira:` block (`project` / `components` / optional
   `jql_override`) supplies the scope; the lens fetches active work as the
   "what we are building" baseline.
2. **Direction A, active work vs landscape:** for each active Feature/Epic,
   find related industry developments; flag ahead / behind / different
   approach.
3. **Direction B, landscape vs active work:** significant developments with no
   corresponding Jira work. Each gap categorized as *intentional omission*,
   *blind spot*, or *emerging opportunity*. This is the strategic payload.
4. Output is a normal numbered research doc under `<home>/research/` through
   the existing research gate, with `00-executive-summary.md` refreshed.
   Depth control and the PLAN GATE are inherited unchanged.

## Repo integration

- `AGENTS.md` skills table: two new rows (`hub.jira-triage`,
  `hub.jira-hygiene`). Watch the 150-line CI budget.
- `docs/skills.md` and `docs/tooling.md`: the two skills and `hub_triage.py`.
- `conventions/research.md`: `jira-gap` joins the `lens` enum.
- `conventions/layout.md`: `work/triage-log.yaml` named alongside
  `jira-snapshot.yaml` as machine-written and tracked.
- `hublib/disclosure.py`: `features/*/work/triage-log.yaml` added to
  `_scan_files()`. The report itself is under `restricted/` and needs no
  scan coverage.
- `docs/enhancements.md`: #30 and #27 move to Done; #29 moves to Done with an
  explicit note that assignment and issue creation were ruled out of scope
  (decision 2) and that cross-component discovery and comment digests were
  deferred (decisions 5 and 6), so a future session does not read "Done" as
  "fully ported".
- `memory/log.md`: a ship line. The write-posture change (decision 2) also
  warrants a durable **fact**, since it reverses a documented invariant: the
  hub can now close and approve Jira issues, and a future agent reading
  "Read-only against Jira" in the older skills must not generalize that to the
  whole hub. The fact should name the exact bounded surface (labels, comments,
  close, approve) and the one skill that holds it.

## Error handling

- **401/403:** the existing token-regeneration remediation text. Token values
  are never printed.
- **429/5xx:** surfaced; the run degrades rather than sinks (the client already
  retries with backoff, honoring `Retry-After`).
- **Decisions JSON references an issue not in the scan:** rejected at the gate.
- **Decisions JSON carries an unsupported action** (`assign`,
  `claim_component`, anything unrecognized): rejected at the gate, with the
  reason. Never silently dropped.
- **A `close` or `approve` whose workflow offers no matching transition, or
  more than one:** rejected at the gate (decision 3). Neither the comment nor
  the transition is attempted. This is the pm-toolkit half-apply bug, fixed.
- **A transition that resolves at scan time but fails at apply time** (the
  workflow moved underneath us, or a permission is missing): that issue is
  recorded as `error` in the log with the Jira message; the rest of the batch
  still applies. For a `close`, the comment has already posted at that point,
  so the log records the comment as applied and the transition as errored,
  and the run reports it explicitly rather than burying it in a count.
- **Label already present:** idempotent no-op, counted as skipped.
- **Partial apply failure:** the remaining items still apply; the run returns a
  coherent applied/skipped/rejected/errors split and the log records per-issue
  outcome.
- **`restricted/` absent:** triage refuses to run. It does not fall back to a
  tracked path.
- **Unknown feature / no stored scope:** exit 2, offer `hub.jira-sweep`.

## Testing

All offline and CI-safe, matching the house style in `scripts/tests/`
(`httpx.MockTransport` injected via the existing `transport=` kwarg, no
`pytest-asyncio`, async tests wrap in `asyncio.run()`, `tmp_path` plus local
`write()` / `make_repo()` helpers).

- `test_triage.py`: the pure functions first (`flag_staleness` thresholds,
  `classify_rfe`'s 7 ordered rules, `suggest_action`'s 8, `_has_strat_clone`
  link walking). pm-toolkit ships zero tests for these and they are the logic
  most likely to be wrong. Then transition resolution: an exact match resolves;
  a case-mismatched name still resolves; no match rejects; two matches reject
  rather than guess. Then `apply_decisions`: a rejected action issues no
  request at all; a label write carries the full existing array; a `close`
  whose transition did not resolve posts **no comment** (the half-apply
  regression test); a partial failure returns a coherent split.
- `test_hub_triage.py`: CLI arg and error paths only, never the network
  (`--out` mandatory, unknown feature exits 2, argparse errors via
  `pytest.raises(SystemExit)`), following `test_hub_jira.py`.
- Existing suites must stay green: `python -m pytest scripts/tests -v` ·
  `python scripts/hub_lint.py` (0 errors, warning count not increased) ·
  `python scripts/hub_index.py --check`.

**Live acceptance (owner-in-the-loop, NOT subagent tasks):** a hygiene audit on
a known-messy issue; a `jira-gap` run on a feature with a live scope; a real
triage pass whose gate is approved for **labels and comments only**, verifying
the round trip end to end; and only then a second pass that actually fires a
`close` and an `approve` on issues chosen deliberately for the purpose.

Splitting the triage acceptance in two is on purpose. Transitions are the first
irreversible-feeling thing this hub does (a close is reopenable, but it
notifies reporters and watchers, and that cannot be taken back). Proving the
scan, the report, the export, and the gate on a labels-only pass first means
that when the first `close` fires, the only untested element is the transition
call itself.

## Sequencing

Ascending risk, so the write path lands after two read-only capabilities have
already exercised the client from inside a skill:

1. **#30 hygiene** (prose plus a read-only `--audit` flag on `hub_jira.py`).
2. **#27(b) jira-gap lens** (prose plus the domain YAML `jira:` block; no new
   code).
3. **#29 triage** (`hublib/triage.py`, `hublib/triage_html.py`,
   `hub_triage.py`, the skill, the tests, the disclosure touch, and the first
   Jira write).

File touches are conflict free across the three. Each part is independently
shippable.
