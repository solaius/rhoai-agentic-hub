# Hub enhancements backlog

- **What this is:** the repo's own improvement backlog — R5/R6 plus every
  candidate enhancement to how humans use the hub, how agents use it, and
  what the machinery can do. Living document; edit freely.
- **How items graduate:** an item here is an idea, not a commitment. When one
  is picked up it follows the standard workflow (brainstorm → spec → plan →
  build with owner gates); its ruling gets a `memory/log.md` line and the
  item moves to *Done* below or gets deleted.
- **Owner:** Peter Double · **Last groomed:** 2026-07-09 (post-batch)

## Priority view

Value = impact on daily PM work + repo trustworthiness. Effort = build cost
including review. "When" is a best guess, not a schedule.

| # | Enhancement | Value | Effort | When |
|---|---|---|---|---|
| 2 | Jira hub skills — sweep, track, and sync Jiras per feature | **High** — Jira is the source of truth for delivery but has no intake pipeline into the hub; pm-toolkit has the client, hub has the filing conventions, nothing connects them | Medium | Now |
| 3 | Feature staleness sweep — per-feature "what's outdated?" | **Medium** — no way to ask "what changed since I last touched mcp-gateway?" without manually comparing sources | Medium | Next |
| 4 | `hub.refresh-site` — refresh the migrated RHCL/Management hub sites from live sources | **High** — the hubs are now the live copies and have no update path; they start rotting today | Medium | Now |
| 6 | R5 — cross-machine continuity runbook + fixes it surfaces | **High** — second machine is already in use; every gap found is a real workflow break | Small (run it) | Now |
| 8 | Pages-site landing page upgrade (grouped, descriptor-driven) | High — the public front door; descriptors already carry the data | Small–Medium | Now/Next |
| 9 | R6 — Cursor end-to-end validation (D2 debt) | Medium–High — bus-factor + harness independence | Small–Medium (run it) | Next |
| 11 | `rice-strats` port (rubric already lives here) | Medium–High in scoring season, idle otherwise | Medium | Next (before the next RICE pass) |
| 12 | Curated FAQ / JTBD publishing (narrative spec Phase 2) | Medium now, High once qa/jtbd volume exists | Small–Medium | When ~20+ answered qa entries or UX/Docs ask |
| 13 | `audience: internal` publishing target | Medium–High — gives GA-readout-class content a legitimate home instead of archive-only | Medium–Large | Next/Later |
| 14 | `restricted/` cross-machine sync (private mirror or git-crypt) | Medium — R5 will feel this pain first-hand | Medium | After R5 |
| 17 | Slack sweep assist for qa capture (spec Phase 2) | Medium, gated on evidence Slack dominates `asks:` | Medium | Later (data-driven) |
| 18 | JTBD mining from qa/tracker (spec Phase 2) | Medium, needs qa volume first | Small–Medium | Later |
| 19 | Doctor: `~/.bashrc` env wiring + Jira/Slack connectivity probes (parked old-doctor coverage) | Medium — needed the first time Jira skills run on a hub-only machine | Small | With R5 |
| 20 | Agent context pack (`hub_index.py --brief`) | Medium — cheaper session bootstrap for agents | Small–Medium | Later |
| 21 | Human search over the published site (static index) | Medium — humans lack grep | Medium | Later |
| 22 | Narrative growth: stories for Inference/Data/Safety & Governance pillars | Medium — content, not tooling; map has `_no stories yet_` ×3 | Small each | As stories emerge |
| 23 | Weekly "what changed" digest view | Low–Medium — team-comms aid | Small | Later |
| 24 | Multi-writer promotion (CONTRIBUTING, PR gate discipline) | Low now, High if a second PM joins | Medium | When real (D1) |
| 25 | `rhoai-atlas` template extraction (hublib as reusable core) | Low now — strategic later | Large | Someday |
| 26 | Pages-site usage analytics | Low — informative, adds an external dependency | Small | Maybe never |
| 27 | Jira gap analysis — `hub.research` jira-gap lens (remainder of the pm-toolkit research port) | **Medium–High** — "NOT building" early warnings mapping competitor moves vs. active Jira work; the competitive-sweep half shipped 2026-07-09 as the `hub.research` competitive lens | Medium | After #2 |
| 28 | PM standup brief — Jira + Slack + Gemini + AI news (pm-toolkit port) | **Medium–High** — the personal daily loop across all systems; complements #15 (hub-only brief) | Medium | Next |
| 29 | RFE triage batch workflow (pm-toolkit port) | **Medium–High** — periodic triage ceremony (scan → classify → interactive HTML report → batch apply); distinct from assess-rfe (single-issue quality) and RICE (#11, scoring) | Medium | Next |
| 30 | Jira hygiene auditor (pm-toolkit port) | **Medium** — audit individual issues against type-specific checklists (links, labels, naming, Fix Version, refinement); companion to #2 (data filing) | Small–Medium | Next |
| 31 | Red Hat Support case search/analysis (pm-toolkit port) | **Medium** — post-sales signal from 1M+ support cases across full AI portfolio; complements the pre-sales customer tracker | Medium | Later |
| 32 | Prototyping skills — setup + delegate to RHOAI prototype repo (pm-toolkit port) | **Low–Medium** — convenience wrapper for PatternFly prototyping via internal GitLab; VPN-dependent | Small | Later |
| 33 | PostToolUse usage logging + report (pm-toolkit port) | **Low** — meta-tooling: JSONL log of every tool invocation + usage summary report | Small | Whenever |
| 34 | Disclosure heuristic frontmatter gap | **Medium** — the generic `RESTRICTED_HINTS` net misses knowledge-entry frontmatter (lint_entry scans body only) and the generated views it propagates into; the local restricted-pattern pass covers frontmatter, CI's generic net does not (found by the 2026-07-09 batch's final review) | Small | Next |

---

## R5 — cross-machine continuity test (deferred runbook, chartered)

**Goal:** prove a second machine reaches full working parity with no help
beyond `docs/setup.md`, and that day-to-day work ping-pongs between
machines without loss. The test IS the deliverable: every friction point
becomes a doctor section, a setup.md fix, or a backlog item here.

**Runbook (execute on machine B, record everything):**
1. Cold path: clone → trust prompt → `/plugin` check → `doctor.sh setup` →
   restart → copy `restricted/` tree + `.env` from machine A → re-run
   `setup` (MCP servers + podman runtime per docs/mcp-servers.md) → restart
   → `doctor.sh check` must reach **0 fail** with slack/google/rhai-tracker
   connected (`/mcp`).
2. Round-trip work test: on B, run one real `hub.capture` (gated, committed,
   pushed); on A, pull and verify indexes clean (`hub_index.py --check`);
   then the reverse direction.
3. Restricted-tier reality check: confirm which restricted files B actually
   needs day-to-day, how stale A↔B copies drift, and whether manual copying
   is tolerable — this feeds item 11 (restricted sync).
4. Race handling: intentionally create a push race (commit on both machines)
   and confirm the rebase discipline documented in the plans works for a
   human following the docs.
5. Deliverables: fixes committed as found; a short `## R5 outcome` note
   appended to this section (what broke, what was fixed, what's now
   parked); memory log line.

**Known gaps to expect** (predicted, so the runbook checks them): podman
engine install needs the admin shell (doctor prints it, human must act);
Slack xoxc/xoxd tokens are per-login session tokens — B needs its own
extraction or fresh copies; `.mcp.json` is per-machine (doctor rewrites the
tracker path); `CTRACK_DIR` differs per machine (restricted/.env override).

## R6 — Cursor end-to-end validation (deferred, D2 debt)

**Goal:** the hub is operable from Cursor, not just Claude Code — D2 said
"Cursor validated post-build" and it never was. Bus-factor insurance and
harness independence.

**Runbook:**
1. Open the hub in Cursor; confirm AGENTS.md is picked up as the operating
   protocol (Cursor reads AGENTS.md natively) and that a session actually
   follows the session-start rule (reads `memory/index.md` first).
2. Skills: Cursor has no `.claude/skills` loader — test whether pointing the
   agent at a SKILL.md file ("follow .claude/skills/hub.capture/SKILL.md")
   reproduces the gated behavior. Record which skills degrade and how.
3. MCP servers: translate the Claude config to Cursor's `mcp.json`
   (google-workspace, slack, rhai-tracker) and verify tool calls; decide
   whether `docs/mcp-servers.md` gains a Cursor appendix or a separate
   snippet per server.
4. Memory tiers: Cursor has no `autoMemoryDirectory` — confirm the scratch
   tier degrades gracefully (nothing writes there; capture/consolidate still
   work directly) and document the difference.
5. Run one full gated capture → reindex → commit → push from Cursor.
6. Deliverables: a "Cursor notes" subsection in `docs/working-here.md` (or
   `docs/cursor.md` if it outgrows a subsection), doctor tweaks if any,
   `## R6 outcome` note here, log line.

---

## Human-usage enhancements

**8 · Pages landing page upgrade.** The published site's generated index is
a flat list. The publisher already has every artifact's title/description
(manifest) and could group by area (mcp-gateway / mcp-ecosystem / …/
narrative), add one-line descriptions, and a "new/updated" marker from the
publish snapshot. This is the page customers/stakeholders actually see —
the highest-visibility small win available. (`scripts/hublib/publisher.py`
landing-page generation + tests.)

**12 · Curated FAQ / JTBD publishing.** Already specced (narrative spec §9):
when qa volume justifies it, ship a curated FAQ page (per audience) and a
JTBD catalog via `hub.publish` — pulled by demand, never auto-published raw
views. Trigger: ~20+ answered qa entries, or UX/Docs asking for a URL.

**21 · Search for humans.** Agents grep; humans can't. Cheapest real option:
a static search page on the pages site (lunr/minisearch index generated
from published content only — keeps the public/publish boundary intact).
Defer until the published surface is bigger; GitHub search covers the repo
meanwhile.

**22 · Narrative growth (content).** The narrative map renders
`_no stories yet_` for Inference, Data, and Safety & Governance. As real
cross-feature work touches those pillars, write the story entry — that's
how the layer compounds. Candidate third story from the original design
discussion: "from prompt to governed asset" (gen-ai-studio +
skills-registry + mcp-registry).

**23 · Weekly digest view.** `views/digest.md` (or a script emitting
markdown for Slack/email): log entries + new/changed entries + published
artifacts in the last N days. Useful the day someone besides Peter follows
the hub; cheap to add then.

## Agent-usage enhancements

**2 · Jira hub skills — sweep, track, and sync.** Jira is the delivery
source of truth but has no intake pipeline into the hub. pm-toolkit already
has the async Jira client (`scripts/_base`, httpx, Pydantic v2) and skills
(`rfe.*`, `assess-rfe`) — mine those for the client layer, then build hub-
native skills on top: (a) `hub.jira-sweep` — given a feature id + JQL or
component, query Jira and create/update `ref-` entries with `jira:` fields,
feeding `views/jira-map.md`; (b) `hub.jira-sync` — periodic refresh that
detects status changes (resolved, closed, won't-fix) and proposes entry
updates through the gate; (c) optionally, backlink from `jtbd-` entries to
their implementing Jiras. Design decision: whether the Jira client lives
in hublib (duplicating pm-toolkit) or the hub imports pm-toolkit as a
sibling — lean toward a thin adapter in hublib that calls the pm-toolkit
client if available, degrades to "paste a Jira URL" otherwise.

**3 · Feature staleness sweep.** Per-feature "what's outdated?" — compare
each `fact-`/`ref-`/`question-` entry's `timestamp` and `review_after`
against current sources (Jira status, GDoc last-modified, upstream repo
activity). Flag entries that look stale, propose updates or `superseded`
status through the gate. `customer-feedback-refresh` does this for the
tracker; this generalizes the pattern to knowledge entries. Could run as
a standalone skill or as a mode of `hub.intake` ("intake --refresh
mcp-gateway").

**20 · Agent context pack.** `python scripts/hub_index.py --brief` emits a
single size-budgeted markdown pack: memory index + features table +
narrative map + open questions + stale queue, trimmed to ~N tokens.
Sessions (especially non-Claude harnesses, see R6) bootstrap with one read
instead of five.

**17 · Slack sweep assist (spec Phase 2).** Periodic sweep of the channels
where Peter answers questions → drafts qa entries through the gate. Build
only if `asks:` data shows Slack dominating; inherits xoxc/xoxd token
brittleness — an assist, never the system of record.

**18 · JTBD mining (spec Phase 2).** Extend `customer-feedback-refresh` to
propose jtbd candidates from recurring qa entries + tracker interests
(gated). Needs qa volume first.

**qa → RICE evidence hook (spec Phase 2, rides with #11).** When
`rice-strats` is ported, its justification comments should cite `asks:`
recurrence counts and qa Gaps sections as Reach/Impact evidence — the
capture loop starts paying for itself in prioritization.

**27 · Jira gap analysis (`hub.research` jira-gap lens).** The remaining
half of the pm-toolkit research port: strategic alignment analysis that
maps active Jira work against competitive developments and surfaces "NOT
building" gaps as early warnings. Ships as a `hub.research` lens (the
skill already names it as FUTURE) once #2 provides the Jira intake
pipeline; the domain YAML gains a `jira:` block (project/components/JQL)
to drive it. The competitive sweep half — domain-config-driven web
research (`domains/redhat-ai.yaml`) — shipped 2026-07-09 as the
`hub.research` competitive lens (see Done).

**28 · PM standup brief.** Port pm-toolkit's `pm-standup` — a personal
daily brief pulling from: Jira (assigned/reported/blocked/approaching
deadlines/comments needing response), Slack (messages to you + mentions,
classified as Needs Response vs. FYI), Gemini Meeting Notes (Google Drive
search for "Notes by Gemini" → action item extraction), and AI news (top
enterprise AI items + Red Hat mentions). Output is structured priorities
(Urgent/Important/Monitor). Complements #15 (`hub_status.py` morning
brief), which is hub-centric (stale items, open questions, CI state) —
the standup is system-centric (what needs my attention today across all
tools). pm-toolkit also has `weekly-plan` (calendar analysis, carry-over
tracking, focus blocks) — consider porting both as a pair.

**29 · RFE triage batch workflow.** Port pm-toolkit's `rfe-triage` — a
5-step playbook: (1) prepare — set component scope and JQL; (2) scan —
`scan_rfes()` with AI-powered comment summarization (Claude via Vertex/
Anthropic/Bedrock); (3) generate interactive HTML triage report with three
sections (Untriaged, Waiting on Input, Backlogged) plus a suggestion engine
(8 pattern rules: stale detection, UI/UX keywords, etc.); (4) apply —
JSON export/import for batch decisions back to Jira (roadmap/backlog/
needs-uxd/clarify/close-stale labels); (5) summarize results. Also has
`discover_cross_component_rfes()` for adjacent-component scanning.
Distinct from `assess-rfe` (single-issue quality rubric) and RICE (#11,
prioritization scoring) — this is the periodic triage ceremony.

**30 · Jira hygiene auditor.** Port pm-toolkit's `jira-hygiene` — three
modes: Audit (fetch an issue, check against type-specific checklists for
RHAIRFE Feature Requests, RHAISTRAT Features, maturity-chain features,
RHAIENG Epics — naming conventions, parent links, clone/dependency links,
Fix Version, Components, Labels, refinement docs, platform refinement
reviews); Create (guide new Jira creation at any lifecycle stage with
proper links and structure); Help (explain hierarchy and conventions).
Companion to #2 (Jira hub skills) — #2 files Jira data into the hub,
hygiene ensures the Jira issues themselves are well-formed.

**31 · Red Hat Support case search/analysis.** Port pm-toolkit's
`redhat-support-cases` — Solr-based bulk search across 1M+ Red Hat support
cases + REST API for individual case detail and comments. Complete product
search registry for the full AI portfolio: RHOAI, RHAIIS (vLLM), RHEL AI/
InstructLab, Model Serving (KServe, Caikit, ModelMesh), Data Science
Pipelines, Model Registry, Distributed Workloads (Kueue, Ray, CodeFlare),
TrustyAI, Lightspeed, Llama Stack, NeMo Guardrails, Training Operator,
Feast, MLflow, Spark Operator, Kagenti, NVIDIA NIM. 5-phase workflow:
Broad Search → Stats → Filter → Deep Dive (details + comments) → Analyze.
Self-contained Python CLI with its own venv; requires Red Hat offline API
token + VPN. Complements the pre-sales customer tracker with post-sales
support signal.

**32 · Prototyping skills.** Port pm-toolkit's `prototype-set-up` (find or
clone the RHOAI prototype repo from `gitlab.cee.redhat.com/uxd/prototypes/
rhoai`) and `prototyping` (delegate to the prototype repo's own AGENTS.md
for PatternFly-based UI work). Thin skills — the hub wouldn't contain
prototyping logic, just the delegation wrapper. VPN-dependent (internal
GitLab). Lower priority: convenience, not a core PM workflow.

## Repo functionality & structure

**4 · `hub.refresh-site`.** Successor to the old repo's
knowledge-hub-create / update-*-hub skills, now urgent: the RHCL and
Management hub sites live HERE and nothing updates them anymore (the old
update skills target the old repo's copies and are retired with it).
Scope: sweep live sources (GDocs, repos, Jira, Slack) per site, propose
page diffs through a gate, re-verify the disclosure rules on every touched
page (reuse the #5 lint), republish. Port-and-adapt, not lift-and-shift —
and the disclosure-scrub rules from this migration become part of the
skill's contract.

**11 · `rice-strats` port.** Rubric already at
`features/platform/strategy/rice-scoring-rubric.md`; the old skill needs
its knowledge lookups repointed (feature partitions + narrative instead of
the monolith) and the qa/RICE hook above designed in. Port before the next
scoring cycle rather than during it.

**13 · `audience: internal` target.** The manifest schema already accepts
`internal`; nothing implements it. A second publish target (VPN'd GitLab
Pages or a private pages repo) would give internal-only artifacts — the
GA-readout class — a real home with the same manifest discipline, instead
of the current binary public-or-archived. Design questions: where it
hosts, how links between public and internal artifacts behave.

**14 · `restricted/` sync.** Manual copy is the current contract and R5
will measure its pain. Options in rough preference order: a private
GitLab/GitHub mirror holding only `restricted/` (same layout, separate
repo, cloned into place), git-crypt in-repo (key management burden), or
keep manual with a doctor-assisted rsync checklist. Decide after R5 data.

**19 · Remaining old-doctor coverage.** `~/.bashrc` sourcing of
`restricted/.env` (so `JIRA_*` reaches every shell — required by `rfe.*` /
`rice-strats` on a hub-only machine) plus Jira and Slack connectivity
probes as new doctor sections. Natural companion to R5. (Per the
2026-07-08 ruling: no LLM-provider credential handling in any form.)

**24 · Multi-writer promotion.** Dormant by design (D1). Trigger: a second
regular writer. Work: promote the working-here contributor stub to
CONTRIBUTING.md, define PR-based gate discipline (memory promotions
proposed in PR description, owner applies via capture), branch protection.

**25 · `rhoai-atlas` template.** The charter's endgame idea: extract
hublib + conventions + skills into a template so other PMs/areas can stamp
their own hub. Only worth it after multi-writer proves the conventions
travel. Large.

**26 · Analytics.** Know which published artifacts get read (privacy-light
counter like GoatCounter). Informative for enablement ROI; adds an external
dependency to an otherwise self-contained pipeline — deliberately last.

**33 · PostToolUse usage logging.** Port pm-toolkit's `log_usage.py`
PostToolUse hook + `usage-report` skill — logs every tool invocation to
`<output_dir>/usage.jsonl` (timestamp, event type, skill/file name, session
ID). Companion `usage_report` summarizes: top skills, top knowledge files
read, session counts, with optional cross-team aggregation for PM leads.
Meta-tooling for understanding how the hub is actually used. Fits the
"files + scripts" envelope (JSONL + summarizer). Doctor-installable hook.

## Deliberately not doing

- **No database, no web app, no server** — files + scripts + CI is the
  design; everything above stays inside that envelope.
- **No embedding/vector search of the repo** — the partition/type/index
  system IS the retrieval design; revisit only if it demonstrably fails.
- **No auto-publishing of raw views** — publishing stays a per-artifact
  disclosure decision (D5/D16), permanently.
- **No LLM-provider credential handling** — owner ruling 2026-07-08,
  recorded in the preferences profile.

## Done

- **#1 `hub.intake` + `hub.research`** — shipped 2026-07-09 (`58ee066`):
  guided multi-source intake (partition scaffold, batch-gated entries) +
  lens-scoped deep research (numbered series per
  `/conventions/research.md`, gated entries, living synthesis,
  `domains/redhat-ai.yaml`), plus warning-only research-doc lint. Spec:
  [/docs/specs/2026-07-09-hub-intake-research-design.md](/docs/specs/2026-07-09-hub-intake-research-design.md).
  Acceptance runs tracked in
  [/docs/plans/2026-07-09-hub-intake-research-plan.md](/docs/plans/2026-07-09-hub-intake-research-plan.md).
- **#27(a) competitive sweep** — shipped 2026-07-09 inside `hub.research`
  (competitive lens + domain configs); #27(b) jira-gap re-scoped above,
  gated on #2.
- 2026-07-09 — **#5 disclosure lint** — `restricted/lint-patterns.txt`
  (gitignored, errors) over enablement HTML + knowledge entries;
  `RESTRICTED_HINTS` hardened (dollar figures, signed-agreement) and extended
  to enablement HTML (warnings). Shipped in the enhancement batch
  (/docs/specs/2026-07-09-enhancement-batch-design.md).
- 2026-07-09 — **#7 pre-commit gate hook** — doctor section 10 installs
  hub_lint + hub_index --check as `.git/hooks/pre-commit`.
- 2026-07-09 — **#10 recorded small-fix batch** — pillar-path warning, faq
  "by home" heading, indexer test gaps, hub.migrate enumeration + historical
  link-repoint carve-out, docs/memory.md boundary line, artifact.md
  scaffolding in presentation/blog skills, log rotation helper
  (`hub_index.py --rotate-log`).
- 2026-07-09 — **#15 `hub_status.py` morning brief** — stale / open questions
  / unanswered qa / JTBD without evidence / descriptor-less enablement dirs /
  rotation reminder / recent log + gh CI state.
- 2026-07-09 — **#16 published-site link checker** —
  `hub_publish.py --check-links` + publish.yml step between apply and push.
