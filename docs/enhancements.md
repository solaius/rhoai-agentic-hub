# Hub enhancements backlog

- **What this is:** the repo's own improvement backlog — R5/R6 plus every
  candidate enhancement to how humans use the hub, how agents use it, and
  what the machinery can do. Living document; edit freely.
- **How items graduate:** an item here is an idea, not a commitment. When one
  is picked up it follows the standard workflow (brainstorm → spec → plan →
  build with owner gates); its ruling gets a `memory/log.md` line and the
  item moves to *Done* below or gets deleted.
- **Owner:** Peter Double · **Last groomed:** 2026-07-09

## Priority view

Value = impact on daily PM work + repo trustworthiness. Effort = build cost
including review. "When" is a best guess, not a schedule.

| # | Enhancement | Value | Effort | When |
|---|---|---|---|---|
| 1 | `hub.refresh-site` — refresh the migrated RHCL/Management hub sites from live sources | **High** — the hubs are now the live copies and have no update path; they start rotting today | Medium | Now |
| 2 | Disclosure lint for enablement HTML (local-only pattern layer) | **High** — the scrub episode proved grep-gates + review are the only net; make the first net mechanical | Small–Medium | Now |
| 3 | R5 — cross-machine continuity runbook + fixes it surfaces | **High** — second machine is already in use; every gap found is a real workflow break | Small (run it) | Now |
| 4 | Pre-commit gate hook installed by `hub.doctor` | High — kills the #1 CI failure (edit → forget reindex → red) | Small | Now |
| 5 | Pages-site landing page upgrade (grouped, descriptor-driven) | High — the public front door; descriptors already carry the data | Small–Medium | Now/Next |
| 6 | R6 — Cursor end-to-end validation (D2 debt) | Medium–High — bus-factor + harness independence | Small–Medium (run it) | Next |
| 7 | Small-fix batch: recorded findings from the narrative build (see §Recorded small fixes) | Medium — cheap trust/polish wins in one sitting | Small | Next |
| 8 | `rice-strats` port (rubric already lives here) | Medium–High in scoring season, idle otherwise | Medium | Next (before the next RICE pass) |
| 9 | Curated FAQ / JTBD publishing (narrative spec Phase 2) | Medium now, High once qa/jtbd volume exists | Small–Medium | When ~20+ answered qa entries or UX/Docs ask |
| 10 | `audience: internal` publishing target | Medium–High — gives GA-readout-class content a legitimate home instead of archive-only | Medium–Large | Next/Later |
| 11 | `restricted/` cross-machine sync (private mirror or git-crypt) | Medium — R5 will feel this pain first-hand | Medium | After R5 |
| 12 | `hub_status.py` morning brief (one-command dashboard) | Medium — daily-loop QoL | Small | Whenever |
| 13 | Published-site link checker in CI | Medium — automates what the migration did by hand | Small | Whenever |
| 14 | Slack sweep assist for qa capture (spec Phase 2) | Medium, gated on evidence Slack dominates `asks:` | Medium | Later (data-driven) |
| 15 | JTBD mining from qa/tracker (spec Phase 2) | Medium, needs qa volume first | Small–Medium | Later |
| 16 | Doctor: `~/.bashrc` env wiring + Jira/Slack connectivity probes (parked old-doctor coverage) | Medium — needed the first time Jira skills run on a hub-only machine | Small | With R5 |
| 17 | Agent context pack (`hub_index.py --brief`) | Medium — cheaper session bootstrap for agents | Small–Medium | Later |
| 18 | Human search over the published site (static index) | Medium — humans lack grep | Medium | Later |
| 19 | Narrative growth: stories for Inference/Data/Safety & Governance pillars | Medium — content, not tooling; map has `_no stories yet_` ×3 | Small each | As stories emerge |
| 20 | Weekly "what changed" digest view | Low–Medium — team-comms aid | Small | Later |
| 21 | Multi-writer promotion (CONTRIBUTING, PR gate discipline) | Low now, High if a second PM joins | Medium | When real (D1) |
| 22 | `rhoai-atlas` template extraction (hublib as reusable core) | Low now — strategic later | Large | Someday |
| 23 | Pages-site usage analytics | Low — informative, adds an external dependency | Small | Maybe never |

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

**5 · Pages landing page upgrade.** The published site's generated index is
a flat list. The publisher already has every artifact's title/description
(manifest) and could group by area (mcp-gateway / mcp-ecosystem / …/
narrative), add one-line descriptions, and a "new/updated" marker from the
publish snapshot. This is the page customers/stakeholders actually see —
the highest-visibility small win available. (`scripts/hublib/publisher.py`
landing-page generation + tests.)

**9 · Curated FAQ / JTBD publishing.** Already specced (narrative spec §9):
when qa volume justifies it, ship a curated FAQ page (per audience) and a
JTBD catalog via `hub.publish` — pulled by demand, never auto-published raw
views. Trigger: ~20+ answered qa entries, or UX/Docs asking for a URL.

**12 · `hub_status.py` morning brief.** One command printing: stale items
due (from stale-facts), open questions count by feature, unanswered qa,
jtbd candidates lacking evidence, last log entries, un-descriptored
enablement dirs, CI state of last push. The daily loop's "where was I."

**18 · Search for humans.** Agents grep; humans can't. Cheapest real option:
a static search page on the pages site (lunr/minisearch index generated
from published content only — keeps the public/publish boundary intact).
Defer until the published surface is bigger; GitHub search covers the repo
meanwhile.

**19 · Narrative growth (content).** The narrative map renders
`_no stories yet_` for Inference, Data, and Safety & Governance. As real
cross-feature work touches those pillars, write the story entry — that's
how the layer compounds. Candidate third story from the original design
discussion: "from prompt to governed asset" (gen-ai-studio +
skills-registry + mcp-registry).

**20 · Weekly digest view.** `views/digest.md` (or a script emitting
markdown for Slack/email): log entries + new/changed entries + published
artifacts in the last N days. Useful the day someone besides Peter follows
the hub; cheap to add then.

## Agent-usage enhancements

**2 · Disclosure lint for enablement HTML — the scrub-episode lesson.**
Today the restricted-content heuristic scans only `knowledge/*.md`; the
leaks that mattered lived in enablement HTML, and literal name lists can't
be committed to a public repo. Design: `hub_lint.py` reads an OPTIONAL,
gitignored `restricted/lint-patterns.txt` (customer names, program
identifiers, agreement phrases, `\$[0-9]` style rules) and scans
`enablement/**/*.html` + knowledge entries with it locally and via a
doctor-installed pre-commit hook — CI never sees the patterns (they're
restricted), so this is a local-first net; CI keeps the generic heuristics.
Also add the generic patterns learned this week (dollar figures,
`signed.*agreement`) to the public heuristic.

**4 · Pre-commit gate hook.** `hub.doctor setup` installs a git pre-commit
hook running `hub_lint.py` + `hub_index.py --check` (+ the disclosure lint
above when present). Eliminates the most common CI failure and moves the
disclosure net to the earliest possible moment.

**17 · Agent context pack.** `python scripts/hub_index.py --brief` emits a
single size-budgeted markdown pack: memory index + features table +
narrative map + open questions + stale queue, trimmed to ~N tokens.
Sessions (especially non-Claude harnesses, see R6) bootstrap with one read
instead of five.

**14 · Slack sweep assist (spec Phase 2).** Periodic sweep of the channels
where Peter answers questions → drafts qa entries through the gate. Build
only if `asks:` data shows Slack dominating; inherits xoxc/xoxd token
brittleness — an assist, never the system of record.

**15 · JTBD mining (spec Phase 2).** Extend `customer-feedback-refresh` to
propose jtbd candidates from recurring qa entries + tracker interests
(gated). Needs qa volume first.

**qa → RICE evidence hook (spec Phase 2, rides with #8).** When
`rice-strats` is ported, its justification comments should cite `asks:`
recurrence counts and qa Gaps sections as Reach/Impact evidence — the
capture loop starts paying for itself in prioritization.

## Repo functionality & structure

**1 · `hub.refresh-site`.** Successor to the old repo's
knowledge-hub-create / update-*-hub skills, now urgent: the RHCL and
Management hub sites live HERE and nothing updates them anymore (the old
update skills target the old repo's copies and are retired with it).
Scope: sweep live sources (GDocs, repos, Jira, Slack) per site, propose
page diffs through a gate, re-verify the disclosure rules on every touched
page (reuse the #2 lint), republish. Port-and-adapt, not lift-and-shift —
and the disclosure-scrub rules from this migration become part of the
skill's contract.

**8 · `rice-strats` port.** Rubric already at
`features/platform/strategy/rice-scoring-rubric.md`; the old skill needs
its knowledge lookups repointed (feature partitions + narrative instead of
the monolith) and the qa/RICE hook above designed in. Port before the next
scoring cycle rather than during it.

**10 · `audience: internal` target.** The manifest schema already accepts
`internal`; nothing implements it. A second publish target (VPN'd GitLab
Pages or a private pages repo) would give internal-only artifacts — the
GA-readout class — a real home with the same manifest discipline, instead
of the current binary public-or-archived. Design questions: where it
hosts, how links between public and internal artifacts behave.

**11 · `restricted/` sync.** Manual copy is the current contract and R5
will measure its pain. Options in rough preference order: a private
GitLab/GitHub mirror holding only `restricted/` (same layout, separate
repo, cloned into place), git-crypt in-repo (key management burden), or
keep manual with a doctor-assisted rsync checklist. Decide after R5 data.

**13 · Published-site link checker.** Post-publish CI step (or
`hub_publish.py --check-links`) that walks the pages repo's HTML for
internal links/assets and fails on 404s — automates the click-through
verification the migration did manually, and catches cross-artifact
rewrite regressions when sites get refreshed (#1).

**16 · Remaining old-doctor coverage.** `~/.bashrc` sourcing of
`restricted/.env` (so `JIRA_*` reaches every shell — required by `rfe.*` /
`rice-strats` on a hub-only machine) plus Jira and Slack connectivity
probes as new doctor sections. Natural companion to R5. (Per the
2026-07-08 ruling: no LLM-provider credential handling in any form.)

**21 · Multi-writer promotion.** Dormant by design (D1). Trigger: a second
regular writer. Work: promote the working-here contributor stub to
CONTRIBUTING.md, define PR-based gate discipline (memory promotions
proposed in PR description, owner applies via capture), branch protection.

**22 · `rhoai-atlas` template.** The charter's endgame idea: extract
hublib + conventions + skills into a template so other PMs/areas can stamp
their own hub. Only worth it after multi-writer proves the conventions
travel. Large.

**23 · Analytics.** Know which published artifacts get read (privacy-light
counter like GoatCounter). Informative for enablement ROI; adds an external
dependency to an otherwise self-contained pipeline — deliberately last.

## Recorded small fixes (batch these in one sitting — item 7)

Carried from the narrative-layer build reviews and migration, all verified
non-blocking when recorded:

- `schema.py`: warn when a story's `pillar:` value lacks the leading `/`
  (silently lands in "Stories without a pillar" today).
- Tests: multi-item Connections sort; combined entries+artifacts
  connection; empty-`narrative/` dir edge cases.
- `hub.migrate`: align its narrative subdir enumeration with
  working-here's (`knowledge|research|strategy`), and add the
  historical-docs carve-out to its link-repoint instruction (the Task-10
  judgment call, codified).
- `docs/memory.md`: classification line gains "(feature or narrative)".
- `presentation-create` / `blog-*`: scaffold an `artifact.md` descriptor
  when creating an enablement dir (today only hub.migrate instructs it).
- `memory/log.md` yearly rotation helper (convention documented, no tooling).
- `views/faq.md` "All, by feature" heading → "by home" once the first
  narrative-homed qa exists.

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

- (Move items here with date + commit when they ship.)
