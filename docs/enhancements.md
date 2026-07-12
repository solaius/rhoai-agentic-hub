# Hub enhancements backlog

- **What this is:** the repo's own improvement backlog — R5/R6 plus every
  candidate enhancement to how humans use the hub, how agents use it, and
  what the machinery can do. Living document; edit freely.
- **How items graduate:** an item here is an idea, not a commitment. When one
  is picked up it follows the standard workflow (brainstorm → spec → plan →
  build with owner gates); its ruling gets a `memory/log.md` line and the
  item moves to *Done* below or gets deleted.
- **Owner:** Peter Double · **Last groomed:** 2026-07-11

## Priority view

Value = impact on daily PM work + repo trustworthiness. Effort = build cost
including review. "When" is a best guess, not a schedule.

| # | Enhancement | Value | Effort | When |
|---|---|---|---|---|
| 6 | R5: cross-machine continuity runbook + fixes it surfaces | **High**. Steps 2 and 3 executed 2026-07-11 on machine B (round-trip passed both directions; #14 answered). Step 1 (cold path) deferred: B was warm. Step 4 (push race) NOT executed. See R5 outcome below | Small (run it) | Steps 2-3 done; 1 and 4 open |
| ~~9~~ | ~~R6 — Cursor end-to-end validation (D2 debt)~~ | Done | Done | Done |
| 12 | Curated FAQ / JTBD publishing (narrative spec Phase 2) | Medium now, High once qa/jtbd volume exists | Small–Medium | When ~20+ answered qa entries or UX/Docs ask |
| 13 | `audience: internal` publishing target | Medium–High — gives GA-readout-class content a legitimate home instead of archive-only | Medium–Large | Shipped (interim) |
| ~~14~~ | ~~`restricted/` cross-machine sync~~ | Done | Done | Done |
| 17 | Slack sweep assist for qa capture (spec Phase 2) | Medium, gated on evidence Slack dominates `asks:` | Medium | Later (data-driven) |
| 18 | JTBD mining from qa/tracker (spec Phase 2) | Medium, needs qa volume first | Small–Medium | Later |
| ~~19~~ | ~~Doctor: env wiring + Slack probe~~ | Done | Done | Done |
| 20 | Agent context pack (`hub_index.py --brief`) | Medium — cheaper session bootstrap for agents | Small–Medium | Later |
| 21 | Human search over the published site (static index) | Medium — humans lack grep | Medium | Later |
| 22 | Narrative growth: stories for Inference/Data/Safety & Governance pillars | Medium — content, not tooling; map has `_no stories yet_` ×3 | Small each | As stories emerge |
| 23 | Weekly "what changed" digest view | Low–Medium — team-comms aid | Small | Later |
| 24 | Multi-writer promotion (CONTRIBUTING, PR gate discipline) | Low now, High if a second PM joins | Medium | When real (D1) |
| 25 | `rhoai-atlas` template extraction (hublib as reusable core) | Low now — strategic later | Large | Someday |
| 26 | Pages-site usage analytics | Low — informative, adds an external dependency | Small | Maybe never |
| 31 | Red Hat Support case search/analysis (pm-toolkit port) | **Medium** — post-sales signal from 1M+ support cases across full AI portfolio; complements the pre-sales customer tracker | Medium | Later |
| 32 | Prototyping skills — setup + delegate to RHOAI prototype repo (pm-toolkit port) | **Low–Medium** — convenience wrapper for PatternFly prototyping via internal GitLab; VPN-dependent | Small | Later |
| 33 | PostToolUse usage logging + report (pm-toolkit port) | **Low** — meta-tooling: JSONL log of every tool invocation + usage summary report | Small | Whenever |
| 35 | Component hub build-out (Catalog, MCPLO, Registry) + Management-hub umbrella devolution | **High** - owner-committed content project; slugs pre-staged, sequenced plan recorded | Large (3 hubs + devolution) | Next |

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
   is tolerable — this feeds item 14 (restricted sync).
4. Race handling: intentionally create a push race (commit on both machines)
   and confirm the rebase discipline documented in the plans works for a
   human following the docs.
5. Deliverables: fixes committed as found; a short `## R5 outcome` note
   appended to this section (what broke, what was fixed, what's now
   parked); memory log line.

**Known gaps to expect** (predicted BEFORE the run, kept here as the
prediction record; see "Predictions vs reality" in the outcome below for what
actually happened, including the Slack one, which was disproved): podman
engine install needs the admin shell (doctor prints it, human must act);
Slack xoxc/xoxd tokens are per-login session tokens — B needs its own
extraction or fresh copies; `.mcp.json` is per-machine (doctor rewrites the
tracker path); `CTRACK_DIR` differs per machine (restricted/.env override).

### R5 outcome (2026-07-11)

**Non-goals (stated plainly so nobody reads R5 as proving more than it did):**
- Step 1 (cold path) was NOT executed: B was warm (already cloned, deps
  installed, restricted/.env copied). Machine C will self-verify via
  `doctor.sh check`, which is why #19 shipped as doctor coverage rather than
  as a checklist a human has to remember to run.
- No cross-OS signal: B is Windows + Git Bash, same as A. The doctor's shell
  assumptions remain unproven on Linux and macOS.
- Step 4 (push race) was NOT executed as designed. See below.

**Step 2 (round-trip): PASSED, both directions.**
- B to A: `hub.capture` gated, committed and pushed from B (`5a49308`);
  pulled on A, `hub_index.py --check` reported 0 stale, lint 0 errors, 222
  tests green.
- A to B: this outcome note itself was the payload, pushed from A and
  verified on B.

**Step 3 (restricted-tier, the #14 evidence): the run's most useful result.**
1. B needs **only `restricted/.env`** day to day (14 keys: Jira, Google
   OAuth, Slack tokens, GitHub, tracker config). The `restricted/features/`
   and `restricted/memory/` trees do not exist on B and were never needed.
2. **No drift problem.** `.env` was copied once and stayed stable.
3. **Manual copying is tolerable** at one file. It would NOT be tolerable if
   customer-feedback workflows ran on B (dozens of NDA files, drift tracked
   by hand).

**Ruling on #14:** manual `.env` copy is sufficient for 1-2 machines.
Parked at Low. Revisit only if customer-feedback workflows move to B or a
third machine joins.

**Addendum, later 2026-07-11 — #14 un-parked.** The revisit condition fired
the same day the ruling was written: customer-feedback gathering was run on
B, where `restricted/features/` does not exist, and the session bypassed the
local-first ingest flow entirely (no tracker to write to, straight past the
gate). Interim method stands — hand-copy the missing `restricted/features/`
files from A per `docs/setup.md` step 6 — but #14 moves to Next. Approach
(private mirror vs git-crypt) still open; note `restricted/` already mirrors
the hub layout and the linter checks it when present, which a private mirror
repo could reuse as-is.

**Step 4 (push race): NOT EXECUTED.** A genuine two-machine simultaneous
race was never orchestrated. A natural single-machine push rejection was
resolved with `git pull --rebase` during the session, which is weaker
evidence and does NOT validate the documented race discipline. Recorded as
untested rather than claimed as passing.

**Predictions vs reality:**
- Podman engine: already installed on B, no admin shell needed.
- Slack tokens: **prediction DISPROVED.** xoxc/xoxd travelled inside the
  copied `restricted/.env` and authenticate on B (`slack auth ok: pedouble
  @ Red Hat`). They are still per-login session tokens that will expire, so
  the section 9 probe keeps earning its place: it names the failure in one
  line instead of leaving it to be discovered mid-task.
- `.mcp.json` is per-machine: confirmed, doctor rewrites the tracker path.
- `~/.bashrc` wiring: B had Jira credentials **hardcoded in plaintext** in
  two duplicate blocks, not sourced from `.env` at all. Removed during the
  run; the hub block now sources them exclusively from `restricted/.env`.

**Doctor gaps R5 surfaced, and what became of them:**
- Section 7 hard-FAILed on a missing customer-tracker clone, so `0 fail` was
  unreachable on any machine that does not do customer-feedback work. A
  health target you cannot hit trains people to skim past FAILs. Owner ruling
  2026-07-11: downgraded to WARN, matching section 8's intent-aware severity.
  `restricted/.env` is copied between machines wholesale, so its `CTRACK_*`
  keys cannot signal intent, which is why an opt-out key was rejected.
- Plugin installs (`rfe-creator`, `assess-rfe`) FAIL on a fresh machine until
  `/plugin` is run interactively in Claude Code. Section 2 DID apply the
  ssh-to-https rewrite correctly, so this is not a doctor bug: the install
  itself simply cannot be automated. `docs/setup.md` step 3 already covers it.

**Machine B final state: `22 ok, 1 warn, 0 fail` (verified).** The route
there: `18 ok / 1 warn / 5 fail` cold, then `21 ok / 0 warn / 3 fail` after
`doctor.sh setup`, then `0 fail` once `/plugin` installed the two marketplace
plugins and the section 7 ruling turned the tracker FAIL into a WARN. That
remaining WARN is correct and expected: B does not do customer-feedback work,
so it has no tracker clone and needs none.

**Machine A: `27 ok, 0 warn, 0 fail`.** The retired `ai-asset-registry`
clone is no longer load-bearing for daily work.

**Both machines reach `0 fail`, which is what R5 owed.** Note what that
number now means: it is reachable, so a FAIL is once again a real signal
rather than background noise a human learns to skim past.

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

### R6 outcome (2026-07-11)

**Status:** Validation runbook executed in Cursor. Core daily loop works;
project MCP enable is the main friction. Full write-up:
[/docs/cursor.md](/docs/cursor.md).

**Shipped earlier (code/config):**
- `.cursor/mcp.json` config (doctor-managed, section 8)
- `docs/cursor.md` (now filled with validation findings)
- Linter guards for git-crypt (Task 1, benefits both enhancements)
- Doctor section 11 (git-crypt)

**Validation runbook results:**
1. [x] AGENTS.md + session-start — **PASS** (agent read `memory/index.md` first)
2. [x] Skill discovery — **PASS**. Cursor loads `.claude/skills/` natively
   (compat with Claude/Codex skill dirs). No `.cursor/skills` symlink needed.
   All 20 hub skills appeared in the agent skill list. Marketplace
   `/plugin` wrappers remain Claude-only; CLIs still work.
3. [x] MCP servers — **PASS** (after follow-ups). Project `.cursor/mcp.json`
   servers stay disconnected in Cursor Settings; user-level
   `~/.cursor/mcp.json` is the reliable path. All three servers (Google,
   Slack, rhai-tracker) working after mirroring to user-level config.
   `CTRACK_DIR` path corrected; doctor section 7 now mirrors tracker.
4. [x] Memory tier — **PASS**. `memory/.scratch/` empty (0 files); capture
   does not depend on scratch.
5. [x] Full gated capture → reindex → commit → push — **PASS** (this session)
6. [x] Multi-step `hub.file` — **PASS** (`ref-cursor-mcp-docs` under platform)
7. [x] Gaps recorded in `docs/cursor.md`

**Predictions vs reality:**
- Skills need `.cursor/skills` symlink — **DISPROVED**. Native `.claude/`
  discovery works.
- Scratch degrades gracefully — **CONFIRMED**.
- Doctor MCP config is enough — **PARTIAL**. File is written correctly, but
  a human must still enable project servers once per machine/workspace.
- Three MCP servers usable after setup — **CONFIRMED** (after follow-ups:
  user-level config + CTRACK_DIR path fix).

**Follow-ups (all resolved 2026-07-11):**
- Slack mirrored into `~/.cursor/mcp.json` (user-level) -- confirmed working
  after Cursor restart.
- `rhai-tracker` path fixed (`CTRACK_DIR` in `restricted/.env` pointed to
  stale `../rh/c-track`; corrected to `../rhai-customer-tracker`). Doctor
  section 7 now mirrors tracker to `.cursor/mcp.json` successfully.
- `docs/setup.md` step 8 and `docs/mcp-servers.md` Cursor appendix updated:
  user-level `~/.cursor/mcp.json` is the reliable path; project-level alone
  is insufficient (Cursor does not auto-surface project servers in Settings).

---

## Human-usage enhancements

**35 · Component hub build-out + umbrella devolution.** Owner ruling
2026-07-10: dedicated hubs for MCP Catalog, MCP Lifecycle Operator, and MCP
Registry (slugs `mcp-catalog/hub/`, `mcp-lifecycle-operator/hub/`,
`mcp-registry/hub/`, pre-staged in the Management hub's nav); the Management
hub thins to the umbrella. Build order Catalog then MCPLO then Registry;
seed each from BOTH parents (RHCL govern pages + Management component
sections) in one pass. Full devolution map + sequenced plan:
[/features/mcp-ecosystem/work/management-hub-umbrella-plan.md](/features/mcp-ecosystem/work/management-hub-umbrella-plan.md).
Each new hub ships with a `work/refresh-<slug>.yaml` so hub.refresh-site
covers it from day one.
**Audience ruling, 2026-07-11:** all knowledge hubs, existing and
prestaged, are `audience: internal` (GA-readout-class detail, not for the
public site); the two live hubs (RHCL, Management) flipped from public to
internal the same day #13 landed in interim form. The three new hubs
(Catalog, MCPLO, Registry) enter the manifest as `audience: internal` from
their first commit, never public first. Spec:
[/docs/specs/2026-07-11-component-hub-buildout-design.md](/docs/specs/2026-07-11-component-hub-buildout-design.md).

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

**27 · Jira gap analysis (`hub.research` jira-gap lens).** The remaining
half of the pm-toolkit research port: strategic alignment analysis that
maps active Jira work against competitive developments and surfaces "NOT
building" gaps as early warnings. Ships as a `hub.research` lens (the
skill already names it as FUTURE) now that #2 (shipped 2026-07-10)
provides the Jira intake pipeline; the domain YAML gains a `jira:` block
(project/components/JQL) to drive it. The competitive sweep half -- domain-config-driven web
research (`domains/redhat-ai.yaml`) -- shipped 2026-07-09 as the
`hub.research` competitive lens (see Done).

**29 · RFE triage batch workflow.** Port pm-toolkit's `rfe-triage` — a
5-step playbook: (1) prepare — set component scope and JQL; (2) scan —
`scan_rfes()` with AI-powered comment summarization (Claude via Vertex/
Anthropic/Bedrock); (3) generate interactive HTML triage report with three
sections (Untriaged, Waiting on Input, Backlogged) plus a suggestion engine
(8 pattern rules: stale detection, UI/UX keywords, etc.); (4) apply —
JSON export/import for batch decisions back to Jira (roadmap/backlog/
needs-uxd/clarify/close-stale labels); (5) summarize results. Also has
`discover_cross_component_rfes()` for adjacent-component scanning.
Distinct from `assess-rfe` (single-issue quality rubric) and RICE
prioritization scoring (retired to Deliberately not doing) — this is the periodic triage ceremony.

**30 · Jira hygiene auditor.** Port pm-toolkit's `jira-hygiene` — three
modes: Audit (fetch an issue, check against type-specific checklists for
RHAIRFE Feature Requests, RHAISTRAT Features, maturity-chain features,
RHAIENG Epics — naming conventions, parent links, clone/dependency links,
Fix Version, Components, Labels, refinement docs, platform refinement
reviews); Create (guide new Jira creation at any lifecycle stage with
proper links and structure); Help (explain hierarchy and conventions).
Companion to #2 (Jira hub skills) — #2 files Jira data into the hub,
hygiene ensures the Jira issues themselves are well-formed.
The client layer it needs now exists (`scripts/hublib/jira.py`, including
the write methods hygiene fixes would use behind a gate).

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

**13 · `audience: internal` target.** The manifest schema already accepts
`internal`; nothing implements it. A second publish target (VPN'd GitLab
Pages or a private pages repo) would give internal-only artifacts — the
GA-readout class — a real home with the same manifest discipline, instead
of the current binary public-or-archived. Design questions: where it
hosts, how links between public and internal artifacts behave.
**Shipped in interim form, 2026-07-11:** the internal target is this
repo's own `gh-pages` branch (`https://solaius.github.io/rhoai-agentic-hub/`),
not the originally envisioned VPN'd GitLab Pages. Accepted caveat: this
repo is public, so the interim internal target carries no real access
control, it is simply unlisted and unlinked from the public site. The
protected-GitLab tail stays open, still tracked as the remaining scope of
this item. Spec:
[/docs/specs/2026-07-11-component-hub-buildout-design.md](/docs/specs/2026-07-11-component-hub-buildout-design.md).

**14 · `restricted/` sync.** Shipped 2026-07-11 via git-crypt. See Done
section below.

**19 · Remaining old-doctor coverage.** `~/.bashrc` sourcing of
`restricted/.env` (so `JIRA_*` reaches every shell — required by the `rfe.*`
skills on a hub-only machine) plus Jira and Slack connectivity
probes as new doctor sections. Natural companion to R5. (Per the
2026-07-08 ruling: no LLM-provider credential handling in any form.)
The Jira connectivity probe shipped 2026-07-10 with #2 (doctor section 4
runs `hub_jira.py --check`); the remaining scope is the env wiring and a
Slack probe.

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
- **No `rice-strats` port** (owner ruling 2026-07-11): RICE scoring work
  no longer needs to live in this hub. The rubric at
  `features/platform/strategy/rice-scoring-rubric.md` stays as reference;
  the qa → RICE evidence hook that rode with the port is retired with it.
- **No LLM-provider credential handling** — owner ruling 2026-07-08,
  recorded in the preferences profile.

## Done

- **#28 PM standup brief + weekly plan** -- shipped 2026-07-11: `hub.standup`
  (daily brief from Jira/Slack/Gemini Notes/AI News using the "Product
  Manager" JQL field) and `hub.weekly-plan` (weekly superset with Google
  Calendar analysis and carry-over tracking). Both are prompt-only skills;
  hub.standup is read-only, hub.weekly-plan writes a checklist file outside
  the repo. Spec:
  [/docs/specs/2026-07-11-standup-sweep-batch-design.md](/docs/specs/2026-07-11-standup-sweep-batch-design.md).
- **#3 Feature staleness sweep** -- shipped 2026-07-11: `hub.sweep` skill
  combining date-arithmetic staleness (conventions/staleness.yaml defaults)
  with live source cross-referencing (Jira status, GDoc last-modified,
  GitHub activity). Flags stale entries and proposes updates through the
  standard gate. Prompt-only skill, no Python backbone. Spec:
  [/docs/specs/2026-07-11-standup-sweep-batch-design.md](/docs/specs/2026-07-11-standup-sweep-batch-design.md).
- **#9 R6 Cursor validation** -- shipped 2026-07-11: Cursor validated as a
  fully operable harness for daily hub work. Skills discovered natively from
  `.claude/skills/` (no symlink needed). Memory scratch tier degrades
  gracefully. MCP servers work via user-level `~/.cursor/mcp.json` (project
  servers stay disconnected in Cursor Settings). Doctor sections 7-8 mirror
  configs to `.cursor/mcp.json`. Full write-up: [/docs/cursor.md](/docs/cursor.md).
  Spec: [/docs/specs/2026-07-11-restricted-sync-cursor-validation-design.md](/docs/specs/2026-07-11-restricted-sync-cursor-validation-design.md).
  Plan: [/docs/plans/2026-07-11-restricted-sync-cursor-validation-plan.md](/docs/plans/2026-07-11-restricted-sync-cursor-validation-plan.md).
- **#14 restricted/ cross-machine sync** -- shipped 2026-07-11: git-crypt
  encrypts `restricted/` in-repo (`.gitattributes` patterns, `.env.example`
  stays plaintext). Linter guards skip encrypted files gracefully on CI.
  Doctor section 11 checks git-crypt install + lock state. Manual `.env` copy
  replaced by one-time key file copy + `git pull`.
  Spec: [/docs/specs/2026-07-11-restricted-sync-cursor-validation-design.md](/docs/specs/2026-07-11-restricted-sync-cursor-validation-design.md).
  Plan: [/docs/plans/2026-07-11-restricted-sync-cursor-validation-plan.md](/docs/plans/2026-07-11-restricted-sync-cursor-validation-plan.md).
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
  **SHIPPED, NOT YET ACCEPTED: 0 of 5 acceptance runs done** (they need live
  Jira and the owner at the gate; checklist at the end of the plan). Until run
  3 and run 4 happen, the write path has never touched production Jira. Run 3
  is a real pass approved for labels and comments ONLY (proving scan, report,
  browser export, gate, apply and log end to end while the sharp tool stays
  holstered); run 4 is the first real `close` and `approve`; run 5
  deliberately exercises the rejection path (a workflow with no matching close
  transition), which is the branch least likely to be hit by accident.
  **Design changed during implementation, in the code's favour:** review found
  that the planned read-modify-write of the labels array could DELETE labels
  when the decisions file was stale (Jira's PUT replaces the array wholesale),
  so the label write became atomic (`JiraClient.add_label` sends Jira's
  `{"update": {"labels": [{"add": l}]}}`). Label deletion is now structurally
  impossible rather than merely guarded, and the write surface narrowed:
  `update_issue` and `create_issue` have zero call sites repo-wide.
  **NOT a complete pm-toolkit port, deliberately** - do not read "Done" as
  "everything came over". Ruled out: assignment, field edits, issue creation
  (owner ruling, spec decision 2). Deferred, still available if wanted:
  cross-component discovery (needed an "adjacent components" config that does
  not exist, spec decision 5) and comment-thread digests (needed an LLM
  provider key, which the 2026-07-08 ruling forbids, spec decision 6). The
  83-row pm-component-ownership registry was not ported: real names and emails
  cannot enter a public repo, and feature JQL scopes replace it.
- **#19 Doctor: env wiring + Slack probe** — shipped 2026-07-11
  (`823e90e..6b74ab7`): `hublib/shellenv.py` (profile-block transforms,
  shared restricted/.env reader), `hub_env.py` (--check/--setup CLI),
  `hublib/slack.py` (auth.test probe), `hub_slack.py` (--check CLI),
  `hublib/doctorio.py` (kind-TAB-message boundary). Doctor section 4
  extended with shell wiring, section 9 extended with Slack auth probe;
  sections were extended, not renumbered. Machine A repaired (retired
  ai-asset-registry block removed, taking the banned LLM-credential `unset`
  machinery with it; hub block written). Why it was needed: the marketplace
  `rfe.*` scripts read `os.environ` with no `.env` fallback and the hub
  cannot patch them, so they had been working on A only because the retired
  clone still sat on disk, and were already broken on B. R5 steps 2 and 3
  executed on machine B 2026-07-11 (step 4 was NOT); the run also forced the
  section 7 severity ruling (a missing customer-tracker clone is a WARN, not
  a FAIL). Both machines now reach `0 fail`. Spec:
  [/docs/specs/2026-07-11-r5-cross-machine-design.md](/docs/specs/2026-07-11-r5-cross-machine-design.md).
  Plan: [/docs/plans/2026-07-11-r5-cross-machine-plan.md](/docs/plans/2026-07-11-r5-cross-machine-plan.md).
- **#34 + #8 + #4 published-site trust batch** - shipped 2026-07-10:
  heuristic over full entry text + generated views/indexes in the disclosure
  scan surface (#34); full-branded grouped landing page with snapshot-v2
  NEW/UPDATED badges (#8); hub.refresh-site skill + tracked
  refresh-<slug>.yaml configs for the RHCL and Management hubs, with the
  disclosure contract the old update skills lacked (#4). Spec:
  [/docs/specs/2026-07-10-published-site-trust-batch-design.md](/docs/specs/2026-07-10-published-site-trust-batch-design.md).
  Plan: [/docs/plans/2026-07-10-published-site-trust-batch-plan.md](/docs/plans/2026-07-10-published-site-trust-batch-plan.md).
  **Both acceptance runs passed - fully accepted 2026-07-11**: RHCL hub
  refresh (`03e3d04`, 20 pages, 5-source sweep, 2 owner rulings) and
  Management hub refresh (`0e21278`, 22 pages + design pass, umbrella
  devolution plan recorded, spawned #35), each ending in a green publish
  run with the landing badges activating as designed. Owner Registry/
  Catalog re-plan applied same day (`e7d8527`): Registry DP misses 3.5
  stable, Catalog TP + Registry TP + integration to 3.6 EA1. Acceptance
  outcomes + run-friction fixes recorded in the plan doc.
- **#2 Jira hub skills** — shipped 2026-07-10 (`629cb3d`): `hublib/jira.py`
  (pm-toolkit client port, httpx), `hublib/jiramap.py` + `hub_jira.py`
  (check/try-jql/sweep/sync CLI), `hub.jira-sweep` + `hub.jira-sync`
  skills, tracked public `work/jira-snapshot.yaml` per feature with the
  unauthenticated-probe summary rule, enriched `views/jira-map.md`, and
  the doctor Jira probe (#19's Jira slice). Spec:
  [/docs/specs/2026-07-09-jira-hub-skills-design.md](/docs/specs/2026-07-09-jira-hub-skills-design.md).
  Plan: [/docs/plans/2026-07-09-jira-hub-skills-plan.md](/docs/plans/2026-07-09-jira-hub-skills-plan.md).
- **#1 `hub.intake` + `hub.research`** — shipped 2026-07-09 (`58ee066`):
  guided multi-source intake (partition scaffold, batch-gated entries) +
  lens-scoped deep research (numbered series per
  `/conventions/research.md`, gated entries, living synthesis,
  `domains/redhat-ai.yaml`), plus warning-only research-doc lint. Spec:
  [/docs/specs/2026-07-09-hub-intake-research-design.md](/docs/specs/2026-07-09-hub-intake-research-design.md).
  Acceptance runs tracked in
  [/docs/plans/2026-07-09-hub-intake-research-plan.md](/docs/plans/2026-07-09-hub-intake-research-plan.md):
  **all five acceptance runs passed** (1/3/4 on 2026-07-09 — mcp-catalog
  partition `b543a4f` + verified 2-lens series `c49269e`; 2/5 on
  2026-07-10 — agent-memory transcript bulk-add `daaef27` + quick-depth
  series refresh `82160c3`). Review minors folded back (`e7e2d99`);
  both skills carry the RHOAI architecture repo as standing context
  (`504b476`). Fully accepted.
- **#27(a) competitive sweep** — shipped 2026-07-09 inside `hub.research`
  (competitive lens + domain configs); #27(b) jira-gap shipped 2026-07-11 with
  the Jira operating batch (see above). #27 is now closed in full.
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
