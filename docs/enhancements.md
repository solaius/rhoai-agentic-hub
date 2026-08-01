# Hub enhancements backlog

- **What this is:** the repo's own improvement backlog. Living document; edit
  freely.
- **How items graduate:** an item here is an idea, not a commitment. When one
  is picked up it follows the standard workflow (brainstorm -> spec -> plan ->
  build with owner gates); its ruling gets a `memory/log.md` line and the
  item moves to [/docs/enhancements-complete.md](/docs/enhancements-complete.md).
- **Owner:** Peter Double -- **Last groomed:** 2026-07-31

---

## Next (active candidates)

**#6 R5: remaining cross-machine steps.** Steps 2 and 3 executed on
machine B 2026-07-11 (both passed). Step 1 (cold path) and step 4 (push
race) remain unexecuted. Step 1 is partially covered by the cross-platform
doctor work (2026-07-31) but has not been run end-to-end on a fresh
macOS/Fedora machine. Full R5 outcome:
[/docs/enhancements-complete.md](/docs/enhancements-complete.md).

**#37 Outcome Creator integration.** Integrate with Engineering's Jira
outcome creation skill(s) -- `andybraren/outcome-creator`. Connects the
hub's component/strategy layer to the outcome artifacts that Engineering
produces in Jira, enabling PM-to-Engineering outcome handoff and
tracking.

*Upstream review 2026-07-31:*

- **No packaging.** No `.claude-plugin/` at all -- no `marketplace.json`,
  no `plugin.json`; its `.claude/settings.json` is a permissions
  allowlist only. Not in `opendatahub-io/skills-registry` (which carries
  rfe-creator, strat-creator, assess-rfe), and `opendatahub-io/
  outcome-creator` does not exist. No instructions for consuming it from
  another repo -- the README's only guidance is "fork this repo as
  private" (for JTBD). It is built to be cloned and run from inside.
- **Flat skill layout.** Its 14 skills are flat files
  (`.claude/skills/outcome.create.md`), not `<name>/SKILL.md`. A plugin
  manifest's `skills:` field means "directories containing
  `<name>/SKILL.md`"; flat `.md` is what `commands:` takes. Copying the
  rfe-creator registry entry verbatim would load zero skills. Verify
  empirically (clone, open Claude, type `/outcome`) before anything else.
- **Bare repo-relative paths.** Skills reference `config/rubric.yaml`,
  `templates/`, `docs/`, `scripts/`, `make sync-jtbd` -- all assume
  cwd == repo root, so they break under plugin install. rfe-creator
  already has this wart here: `artifacts/rfe-tasks/` is populated while
  `scripts/next_rfe_id.py` does not exist in this repo. Jira keys are
  placeholders too (`config/pipeline-settings.yaml` ships `PROJSTRAT`/
  `PROJGOALS`), and that file sits in the plugin cache -- wiped on
  update, so real keys need a hub-side override.
- **Disclosure risk (blocking).** `make sync-jtbd` clones the
  confidential internal JTBD Knowledge Registry into
  `knowledge/jtbd-registry/`, and `/outcome.create` fires that sync
  automatically when the directory is missing. Upstream gitignores it;
  this repo is public. Route to `restricted/` with a defensive
  `.gitignore` entry. Shared dependency with #38 -- decide once.

*Recommended shape:* marketplace plugin -- not vendoring (owns the drift)
and not a submodule (Windows symlink friction, still cwd-bound). Matches
how rfe-creator/assess-rfe already install here: two lines in
`.claude/settings.json`, `hub.doctor` already verifies plugin installs,
updates via `/plugin marketplace update`. Three layers: (1) fork,
restructure to `skills/<name>/SKILL.md`, add `.claude-plugin/` (a repo
can be its own single-plugin marketplace via `source: "./"`), then PR the
packaging upstream and/or a registry entry to `opendatahub-io/
skills-registry` -- its schema accepts `source: {type: github, repo:
andybraren/outcome-creator}`, no re-hosting needed -- so the fork becomes
disposable; (2) rewrite plugin-internal paths to `${CLAUDE_PLUGIN_ROOT}`
/ `${CLAUDE_SKILL_DIR}`, leaving `artifacts/` and `local/` cwd-relative
so output lands in the hub; (3) a thin `hub.outcome` wrapper -- component
knowledge/research/strategy + stored Jira scope -> `/outcome.derive` ->
gated `ref-` entry under `components/<id>/work/` + strategy Jira coverage
map. Layer 3 is the actual enhancement; 1 and 2 are prerequisites.

**#38 UX Research Insights integration.** Integrate with the UX team's
(Andy Braren) UX Research Insights solution to enhance `hub.research`
capabilities. Surfaces UX research findings (usability studies, user
interviews, heuristic evaluations) alongside the hub's existing research
lenses. Shares the JTBD Knowledge Registry dependency surfaced by the #37
review (confidential, internal GitLab) -- settle the `restricted/` path
story once and reuse it. `rh-uxd/ai-helpers` (see #32) also ships
`uxd-research-heuristic-eval` and `uxd-evaluate-design-heuristics`, which
may cover part of this scope.

**#32 Prototyping skills.** Port pm-toolkit's `prototype-set-up` (find or
clone the RHOAI prototype repo from `gitlab.cee.redhat.com/uxd/prototypes/
rhoai`) and `prototyping` (delegate to the prototype repo's own AGENTS.md
for PatternFly-based UI work). Thin skills, just the delegation wrapper.
VPN-dependent (internal GitLab).

## Later (data-gated or low urgency)

**#12 Curated FAQ / JTBD publishing (narrative spec Phase 2).** When qa
volume justifies it, ship a curated FAQ page (per audience) and a JTBD
catalog via `hub.publish`. Trigger: ~20+ answered qa entries, or UX/Docs
asking for a URL.

**#17 Slack sweep assist (spec Phase 2).** Periodic sweep of the channels
where Peter answers questions, drafts qa entries through the gate. Build
only if `asks:` data shows Slack dominating; inherits xoxc/xoxd token
brittleness.

**#18 JTBD mining (spec Phase 2).** Extend `customer-feedback-refresh` to
propose jtbd candidates from recurring qa entries + tracker interests
(gated). Needs qa volume first.

**#20 Agent context pack.** `python scripts/hub_index.py --brief` emits a
single size-budgeted markdown pack: memory index + components table +
narrative map + open questions + stale queue, trimmed to ~N tokens.
Sessions (especially non-Claude harnesses) bootstrap with one read instead
of five.

**#21 Search for humans.** Agents grep; humans can't. Cheapest real option:
a static search page on the pages site (lunr/minisearch index generated
from published content only, keeps the public/publish boundary intact).
Defer until the published surface is bigger; GitHub search covers the repo
meanwhile.

**#22 Narrative growth (content).** The narrative map renders
`_no stories yet_` for Inference, Data, and Safety & Governance. As real
cross-component work touches those pillars, write the story entry. Candidate
third story from the original design discussion: "from prompt to governed
asset" (gen-ai-studio + skills-registry + mcp-registry).

**#23 Weekly digest view.** `views/digest.md` (or a script emitting
markdown for Slack/email): log entries + new/changed entries + published
artifacts in the last N days. Useful the day someone besides Peter follows
the hub; cheap to add then.

**#24 Multi-writer promotion.** Dormant by design (D1). Trigger: a second
regular writer. Work: promote the working-here contributor stub to
CONTRIBUTING.md, define PR-based gate discipline, branch protection.

**#31 Red Hat Support case search/analysis (pm-toolkit port).** Solr-based
bulk search across 1M+ Red Hat support cases + REST API for individual case
detail and comments. Complete product search registry for the full AI
portfolio. 5-phase workflow: Broad Search -> Stats -> Filter -> Deep Dive ->
Analyze. Self-contained Python CLI; requires Red Hat offline API token +
VPN. Complements the pre-sales customer tracker with post-sales support
signal.

**#33 PostToolUse usage logging (pm-toolkit port).** Logs every tool
invocation to `<output_dir>/usage.jsonl` (timestamp, event type,
skill/file name, session ID). Companion `usage_report` summarizes: top
skills, top knowledge files read, session counts. Meta-tooling for
understanding how the hub is actually used. Doctor-installable hook.

**#36 Python-based doctor rewrite.** Rewrite `doctor.sh` entirely in
Python, eliminating bash compatibility issues (macOS ships bash 3.2 from
2007 due to GPLv3 licensing). The current bash fixes (2026-07-31) cover
the three target platforms (macOS/Fedora/Windows), so this is low priority
until a fourth platform or a more complex check is needed. Would also allow
richer output formatting and easier testing.

## Someday

**#13 `audience: internal` remaining scope.** The interim form shipped
2026-07-11 (this repo's `gh-pages` branch, unlisted). The remaining scope:
a protected-GitLab-Pages target with real access control for truly
internal-only artifacts. Design questions: where it hosts, how links
between public and internal artifacts behave.

**#25 `rhoai-atlas` template extraction.** The charter's endgame idea:
extract hublib + conventions + skills into a template so other PMs/areas
can stamp their own hub. Only worth it after multi-writer proves the
conventions travel. Large.

**#26 Pages-site usage analytics.** Privacy-light counter like GoatCounter.
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
