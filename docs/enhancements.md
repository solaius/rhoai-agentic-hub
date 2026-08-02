# Hub enhancements backlog

- **What this is:** the hub's improvement direction and rationale.
  Each item links to a GitHub issue for scope, acceptance criteria,
  and implementation detail.
- **How items graduate:** when picked up, the issue tracks the work;
  on completion, the item moves to
  [enhancements-complete.md](/docs/enhancements-complete.md) with a
  completion date and outcome summary.
- **Owner:** Peter Double -- **Last groomed:** 2026-08-02
- **Convention:** when an enhancement completes that adds, changes, or
  removes a user-facing capability, update
  [docs/capabilities.md](docs/capabilities.md) as part of the completion --
  the relevant capability section plus the pain-points and day-in-the-life
  tables if affected.

---

## Next (active candidates)

**[#1 Outcome Creator integration](https://github.com/solaius/rhoai-agentic-hub/issues/1).**
Connect the hub's component/strategy layer to Engineering's Jira outcome
creation workflow (`andybraren/outcome-creator`). Enables PM-to-Engineering
outcome handoff and tracking. Requires upstream packaging work first -- the
repo has no plugin manifest and its skills assume cwd == repo root.

**[#2 UX Research Insights integration](https://github.com/solaius/rhoai-agentic-hub/issues/2).**
Surface UX research findings (usability studies, user interviews, heuristic
evaluations) alongside the hub's existing research lenses. Shares the JTBD
Knowledge Registry dependency with #1 -- both need the `restricted/` path
story settled once.

## Later (data-gated or low urgency)

**[#4 Curated FAQ / JTBD publishing](https://github.com/solaius/rhoai-agentic-hub/issues/4).**
Ship a curated FAQ page (per audience) and a JTBD catalog via `hub.publish`
when qa volume justifies it. Trigger: ~20+ answered qa entries, or UX/Docs
asking for a URL.

**[#5 Narrative growth](https://github.com/solaius/rhoai-agentic-hub/issues/5).**
The narrative map renders `_no stories yet_` for Inference, Data, and Safety
& Governance. As real cross-component work touches those pillars, write the
story entries. Content work, not tooling.

**[#6 Weekly digest view](https://github.com/solaius/rhoai-agentic-hub/issues/6).**
A `views/digest.md` (or script emitting markdown for Slack/email) showing
log entries, new/changed entries, and published artifacts from the last N
days. Useful the day someone besides Peter follows the hub.

**[#7 Search for humans](https://github.com/solaius/rhoai-agentic-hub/issues/7).**
Agents grep; humans can't. A static search page on the pages site
(lunr/minisearch index generated from published content only) preserves the
public/publish boundary. Defer until the published surface is bigger.

**[#8 Agent context pack](https://github.com/solaius/rhoai-agentic-hub/issues/8).**
`hub_index.py --brief` emits a single size-budgeted markdown pack for
session bootstrap: memory index + components table + narrative map + open
questions + stale queue, trimmed to ~N tokens. One read instead of five.

**[#9 PostToolUse usage logging](https://github.com/solaius/rhoai-agentic-hub/issues/9).**
Log every tool invocation to `usage.jsonl` with a companion summary report
(top skills, top knowledge files, session counts). Meta-tooling for
understanding how the hub is actually used. Doctor-installable hook.

**[#10 Python-based doctor rewrite](https://github.com/solaius/rhoai-agentic-hub/issues/10).**
Rewrite `doctor.sh` entirely in Python, eliminating bash compatibility
issues (macOS ships bash 3.2 from 2007 due to GPLv3 licensing). Low
priority until a fourth platform or more complex checks are needed.

**[#11 Slack sweep assist](https://github.com/solaius/rhoai-agentic-hub/issues/11).**
Periodic sweep of channels where Peter answers questions, drafting qa
entries through the gate. Build only if `asks:` data shows Slack dominating;
inherits xoxc/xoxd token brittleness.

**[#12 JTBD mining](https://github.com/solaius/rhoai-agentic-hub/issues/12).**
Extend `customer-feedback-refresh` to propose jtbd candidates from
recurring qa entries and tracker interests (gated). Needs qa volume first.

**[#13 Multi-writer promotion](https://github.com/solaius/rhoai-agentic-hub/issues/13).**
Dormant by design. Trigger: a second regular writer. Promote the
working-here contributor stub to CONTRIBUTING.md, define PR-based gate
discipline, branch protection.

**[#14 Red Hat Support case search/analysis](https://github.com/solaius/rhoai-agentic-hub/issues/14).**
Port pm-toolkit's Solr-based support case search to the hub. Bulk search
across 1M+ cases plus REST API for individual case detail. Complements the
pre-sales customer tracker with post-sales support signal. VPN-dependent.

## Someday

**Audience-internal remaining scope.** The interim form shipped 2026-07-11
(this repo's `gh-pages` branch, unlisted). The remaining scope: a
protected-GitLab-Pages target with real access control for truly
internal-only artifacts. Design questions: where it hosts, how links
between public and internal artifacts behave.

**`rhoai-atlas` template extraction.** The charter's endgame idea: extract
hublib + conventions + skills into a template so other PMs/areas can stamp
their own hub. Only worth it after multi-writer proves the conventions
travel. Large.

**Pages-site usage analytics.** Privacy-light counter like GoatCounter.
Informative for enablement ROI; adds an external dependency. Deliberately
last.

## Deliberately not doing

- **No database, no web app, no server** -- files + scripts + CI is the
  design; everything above stays inside that envelope.
- **No embedding/vector search of the repo** -- the partition/type/index
  system IS the retrieval design; revisit only if it demonstrably fails.
- **No auto-publishing of raw views** -- publishing stays a per-artifact
  disclosure decision (D5/D16), permanently.
- **No `rice-strats` port** (owner ruling 2026-07-11): RICE scoring work
  no longer needs to live in this hub.
- **No LLM-provider credential handling** -- owner ruling 2026-07-08,
  recorded in the preferences profile.
