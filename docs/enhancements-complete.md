# Hub enhancements -- completed

Completed items from the hub enhancement backlog, ordered by completion date.
See [/docs/enhancements.md](/docs/enhancements.md) for open items.

---

## 2026-08-02

**#3 Prototyping skills.** Superseded by native prototype system (#15).
The original approach (thin delegation to internal GitLab prototype repo,
VPN-dependent) was replaced with a native `prototype/` skeleton leg,
`hub.prototype` skill, PatternFly MCP integration, and generated views
([/docs/specs/2026-08-02-prototype-system-design.md](/docs/specs/2026-08-02-prototype-system-design.md)).

## 2026-07-09

**#5 Disclosure lint.** `restricted/lint-patterns.txt`
(gitignored, errors) over enablement HTML + knowledge entries;
`RESTRICTED_HINTS` hardened (dollar figures, signed-agreement) and extended
to enablement HTML (warnings). Shipped in the enhancement batch
([/docs/specs/2026-07-09-enhancement-batch-design.md](/docs/specs/2026-07-09-enhancement-batch-design.md)).

**#7 Pre-commit gate hook.** Doctor section 10 installs
hub_lint + hub_index --check as `.git/hooks/pre-commit`.

**#10 Recorded small-fix batch.** Pillar-path warning, faq
"by home" heading, indexer test gaps, hub.migrate enumeration + historical
link-repoint carve-out, docs/memory.md boundary line, artifact.md
scaffolding in presentation/blog skills, log rotation helper
(`hub_index.py --rotate-log`).

**#15 `hub_status.py` morning brief.** Stale / open questions
/ unanswered qa / JTBD without evidence / descriptor-less enablement dirs /
rotation reminder / recent log + gh CI state.

**#16 Published-site link checker.**
`hub_publish.py --check-links` + publish.yml step between apply and push.

**#1 `hub.intake` + `hub.research`** (`58ee066`):
guided multi-source intake (partition scaffold, batch-gated entries) +
lens-scoped deep research (numbered series per
`/conventions/research.md`, gated entries, living synthesis,
`domains/redhat-ai.yaml`), plus warning-only research-doc lint. Spec:
[/docs/specs/2026-07-09-hub-intake-research-design.md](/docs/specs/2026-07-09-hub-intake-research-design.md).
Acceptance runs tracked in
[/docs/plans/2026-07-09-hub-intake-research-plan.md](/docs/plans/2026-07-09-hub-intake-research-plan.md):
all five acceptance runs passed (1/3/4 on 2026-07-09, 2/5 on
2026-07-10). Review minors folded back (`e7e2d99`);
both skills carry the RHOAI architecture repo as standing context
(`504b476`). Fully accepted.

**#27(a) Competitive sweep.** Shipped inside `hub.research`
(competitive lens + domain configs); #27(b) jira-gap shipped 2026-07-11 with
the Jira operating batch (see below). #27 closed in full.

## 2026-07-10

**#2 Jira hub skills** (`629cb3d`): `hublib/jira.py`
(pm-toolkit client port, httpx), `hublib/jiramap.py` + `hub_jira.py`
(check/try-jql/sweep/sync CLI), `hub.jira-sweep` + `hub.jira-sync`
skills, tracked public `work/jira-snapshot.yaml` per component with the
unauthenticated-probe summary rule, enriched `views/jira-map.md`, and
the doctor Jira probe (#19's Jira slice). Spec:
[/docs/specs/2026-07-09-jira-hub-skills-design.md](/docs/specs/2026-07-09-jira-hub-skills-design.md).
Plan: [/docs/plans/2026-07-09-jira-hub-skills-plan.md](/docs/plans/2026-07-09-jira-hub-skills-plan.md).

**#34 + #8 + #4 Published-site trust batch**: heuristic over full entry
text + generated views/indexes in the disclosure scan surface (#34);
full-branded grouped landing page with snapshot-v2 NEW/UPDATED badges (#8);
hub.refresh-site skill + tracked refresh-<slug>.yaml configs for the RHCL
and Management hubs, with the disclosure contract the old update skills
lacked (#4). Spec:
[/docs/specs/2026-07-10-published-site-trust-batch-design.md](/docs/specs/2026-07-10-published-site-trust-batch-design.md).
Plan: [/docs/plans/2026-07-10-published-site-trust-batch-plan.md](/docs/plans/2026-07-10-published-site-trust-batch-plan.md).
Both acceptance runs passed (fully accepted 2026-07-11): RHCL hub
refresh (`03e3d04`, 20 pages, 5-source sweep, 2 owner rulings) and
Management hub refresh (`0e21278`, 22 pages + design pass, umbrella
devolution plan recorded, spawned #35). Owner Registry/Catalog re-plan
applied same day (`e7d8527`).

## 2026-07-11

**#19 Doctor: env wiring + Slack probe**
(`823e90e..6b74ab7`): `hublib/shellenv.py` (profile-block transforms,
shared restricted/.env reader), `hub_env.py` (--check/--setup CLI),
`hublib/slack.py` (auth.test probe), `hub_slack.py` (--check CLI),
`hublib/doctorio.py` (kind-TAB-message boundary). Doctor section 4
extended with shell wiring, section 9 extended with Slack auth probe;
sections were extended, not renumbered. Machine A repaired (retired
ai-asset-registry block removed). Why it was needed: the marketplace
`rfe.*` scripts read `os.environ` with no `.env` fallback and the hub
cannot patch them. Both machines now reach `0 fail`. Spec:
[/docs/specs/2026-07-11-r5-cross-machine-design.md](/docs/specs/2026-07-11-r5-cross-machine-design.md).
Plan: [/docs/plans/2026-07-11-r5-cross-machine-plan.md](/docs/plans/2026-07-11-r5-cross-machine-plan.md).

**#28 PM standup brief + weekly plan**: `hub.standup`
(daily brief from Jira/Slack/Gemini Notes/AI News using the "Product
Manager" JQL field) and `hub.weekly-plan` (weekly superset with Google
Calendar analysis and carry-over tracking). Both are prompt-only skills;
hub.standup is read-only, hub.weekly-plan writes a checklist file outside
the repo. Spec:
[/docs/specs/2026-07-11-standup-sweep-batch-design.md](/docs/specs/2026-07-11-standup-sweep-batch-design.md).

**#3 Component staleness sweep**: `hub.sweep` skill
combining date-arithmetic staleness (conventions/staleness.yaml defaults)
with live source cross-referencing (Jira status, GDoc last-modified,
GitHub activity). Flags stale entries and proposes updates through the
standard gate. Prompt-only skill, no Python backbone. Spec:
[/docs/specs/2026-07-11-standup-sweep-batch-design.md](/docs/specs/2026-07-11-standup-sweep-batch-design.md).

**#9 R6 Cursor validation**: Cursor validated as a
fully operable harness for daily hub work. Skills discovered natively from
`.claude/skills/` (no symlink needed). Memory scratch tier degrades
gracefully. MCP servers work via user-level `~/.cursor/mcp.json` (project
servers stay disconnected in Cursor Settings). Doctor sections 7-8 mirror
configs to `.cursor/mcp.json`. Full write-up: [/docs/cursor.md](/docs/cursor.md).
Spec: [/docs/specs/2026-07-11-restricted-sync-cursor-validation-design.md](/docs/specs/2026-07-11-restricted-sync-cursor-validation-design.md).
Plan: [/docs/plans/2026-07-11-restricted-sync-cursor-validation-plan.md](/docs/plans/2026-07-11-restricted-sync-cursor-validation-plan.md).

**#14 restricted/ cross-machine sync**: git-crypt
encrypts `restricted/` in-repo (`.gitattributes` patterns, `.env.example`
stays plaintext). Linter guards skip encrypted files gracefully on CI.
Doctor section 11 checks git-crypt install + lock state. Manual `.env` copy
replaced by one-time key file copy + `git pull`.
Spec: [/docs/specs/2026-07-11-restricted-sync-cursor-validation-design.md](/docs/specs/2026-07-11-restricted-sync-cursor-validation-design.md).
Plan: [/docs/plans/2026-07-11-restricted-sync-cursor-validation-plan.md](/docs/plans/2026-07-11-restricted-sync-cursor-validation-plan.md).

**#30 + #27(b) + #29 Jira operating batch**: the three
capabilities unblocked by #2's client. `hub.jira-hygiene` audits one issue
against type checklists (read-only; pm-toolkit's Create mode ruled out).
`hub.research` gains the `jira-gap` lens, driven by the domain YAML's
`jira:` block. `hub.jira-triage` runs the triage ceremony and makes the
first Jira write in this hub's history, bounded to labels, comments, and
the close and approve transitions, every one gated line by line.
Spec: [/docs/specs/2026-07-11-jira-operating-batch-design.md](/docs/specs/2026-07-11-jira-operating-batch-design.md).
Plan: [/docs/plans/2026-07-11-jira-operating-batch-plan.md](/docs/plans/2026-07-11-jira-operating-batch-plan.md).
Note: shipped, not yet accepted (0 of 5 acceptance runs done). Design
changed during implementation: label write became atomic
(`JiraClient.add_label`) to prevent accidental deletion.

## 2026-07-12

**#35 Component hub build-out + Management umbrella devolution**: three new
knowledge hubs built and published internal: MCP Catalog (14 pages), MCP
Lifecycle Operator (16 pages), MCP Registry (12 pages), each seeded from
both parent hubs in one pass. The Management hub devolved from 22 pages to
an 18-page cross-component umbrella. Backlog #13 (`audience: internal`
publish target) shipped in interim form as part of this effort: all five
hubs now publish to this repo's own `gh-pages`. `hub.refresh-site` gained
standing JTBD and Jira Tracker section contracts; all five hubs carry both.
Spec:
[/docs/specs/2026-07-11-component-hub-buildout-design.md](/docs/specs/2026-07-11-component-hub-buildout-design.md).
Plan:
[/docs/plans/2026-07-11-component-hub-buildout-plan.md](/docs/plans/2026-07-11-component-hub-buildout-plan.md).

---

## R5 -- cross-machine continuity test

**Goal:** prove a second machine reaches full working parity with no help
beyond `docs/setup.md`, and that day-to-day work ping-pongs between
machines without loss.

### R5 outcome (2026-07-11)

**Non-goals:** Step 1 (cold path) was NOT executed (B was warm). No cross-OS
signal (B is Windows, same as A). Step 4 (push race) was NOT executed as
designed.

**Step 2 (round-trip): PASSED, both directions.**
- B to A: `hub.capture` gated, committed and pushed from B (`5a49308`);
  pulled on A, indexes clean, lint 0 errors, 222 tests green.
- A to B: outcome note pushed from A, verified on B.

**Step 3 (restricted-tier):** B needs only `restricted/.env` day to day.
No drift problem. Manual copying is tolerable at one file.

**Machine B final state: `22 ok, 1 warn, 0 fail`.**
**Machine A: `27 ok, 0 warn, 0 fail`.**
Both machines reach `0 fail`.

Remaining open steps (1 cold path, 4 push race) tracked as #6 in
[/docs/enhancements.md](/docs/enhancements.md).

## R6 -- Cursor end-to-end validation

### R6 outcome (2026-07-11)

Cursor validated as a fully operable harness. Core daily loop works;
project MCP enable is the main friction. Full write-up:
[/docs/cursor.md](/docs/cursor.md).

All 7 runbook steps passed. Skills discovered natively from `.claude/skills/`.
Memory scratch degrades gracefully. MCP servers work via user-level
`~/.cursor/mcp.json`. Doctor mirrors configs to `.cursor/mcp.json`.
