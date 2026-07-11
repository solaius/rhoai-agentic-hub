---
name: hub.research
description: Deep research on a feature or narrative topic — sized fan-out across lenses (landscape, upstream, architecture, requirements, competitive), producing a numbered series under <home>/research/ plus gated knowledge entries and a living executive summary. Use when the user says "research <topic>", "deep dive on <feature>", "competitive research on <feature>", "refresh the research on <feature>", or after hub.intake offers a kickoff. Lens names in the prompt scope the run to exactly those lenses.
---

# hub.research

Input: a feature id, narrative topic, or free topic + optional lens names
and depth from the prompt. Series contract: /conventions/research.md.

Lenses: landscape (definitions, state of the art, best practices) ·
upstream (OSS projects, standards, protocols, repos) · architecture
(patterns, reference architectures, build-vs-buy) · requirements
(capability expectations, enterprise needs, persona demands) · competitive
(competitor moves + analyst coverage, driven by domains/*.yaml) ·
jira-gap (strategic alignment: cross active Jira work against the
landscape, both directions, driven by the `jira:` block in
`domains/*.yaml`).

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

1. RESOLVE HOME: feature id → features/<id>/research/; story-shaped →
   narrative/research/. Free topic with no home in
   features/features.yaml → offer hub.intake first (research needs a home
   to write into); stop there if declined.
2. CONTEXT LOAD: read <home>/knowledge/index.md (if present), every doc
   in the existing <home>/research/ series, and open question- entries
   for the home. Open questions become research inputs. RHOAI feature
   topics: the RHOAI architecture repo
   (/features/platform/knowledge/ref-opendatahub-architecture-context-repo.md)
   is STANDING CONTEXT — include its matching release snapshot in every
   lens agent's brief. A non-empty series ⇒ this is a REFRESH run.
3. PLAN GATE: propose lenses × depth and expected output BEFORE any
   research starts:
   - quick: 1 agent (run inline, no fan-out), 1-2 docs, ~5 sources/lens
   - standard: 3-4 lens agents, one doc each, ~15 sources/lens
   - deep: full lens set incl. competitive, plus an adversarial
     source-verification pass on load-bearing claims
   Lenses named in the prompt run exactly as given — no additions.
   Refresh runs default to the existing series' lenses. Size by existing
   hub coverage, breadth of the domain, and how contested the space is;
   say why. The approved plan is a HARD CAP — a big subtopic discovered
   mid-run becomes a "recommended follow-up" note in 00, never silent
   expansion. Wait for OK.
4. FAN OUT: one research subagent per lens (Agent tool; no subagents
   available → run lenses sequentially inline). Each brief: the step-2
   context summary + the lens definition + (competitive and jira-gap only)
   the domain config from domains/*.yaml — pick by explicit ask, then by
   `features:` match, then `default: true`. Sources: web search/fetch, GitHub, Google
   Drive MCP, Slack MCP, context7. The customer tracker
   (rhai-tracker/restricted) MAY be read as input, but any finding citing
   it is restricted (step 6). A failed lens shrinks the run, never sinks
   it — report and continue. MCP down → say so, offer pasted-content
   fallback, point at hub.doctor check; no retry loops.
5. DRAFT in the session/scratchpad — no repo writes yet: one numbered doc
   per lens (frontmatter per /conventions/research.md; continue existing
   numbering on refresh) + rewrite 00-executive-summary.md as the living
   synthesis. Refresh: contradicted findings get a supersede note in the
   OLD doc per the convention; never delete. Lenses that did not run are
   listed in 00 with the exact retry invocation. Also draft knowledge
   entries for decision-ready atoms: fact-/ref-/question- entries and
   answers to existing question- entries (status: answered).
6. WRITE GATE: one batch table — every file, one line:
   `path: description [public|restricted] [new|update|supersede]`. Full
   content on request. Approve/edit/reject per line; nothing touches the
   repo before OK. Routing rules: customer names/deal context,
   tracker-sourced findings, NDA-marked GDoc content →
   restricted/<home-path>/research/ (same series shape); dollar figures
   and agreement language never go to tracked files. Conflicts with
   existing knowledge entries are shown as pairs with a proposed
   supersede — never auto-resolved.
7. On OK: write the approved files, run `python scripts/hub_index.py`,
   then `python scripts/hub_lint.py` (0 errors — fix the written content,
   not the scripts). Commit: stage the approved files plus regenerated
   indexes/views explicitly, NEVER `git add -A` (shared checkout, see
   fact-concurrent-session-git-hygiene); check `git diff --cached --stat`,
   then commit with pathspecs:
   `git commit -m "research(<home>): <lenses> <depth>" -- <those paths>`
   && `git push`.
8. Offer follow-ups the run surfaced (a deeper lens pass, hub.intake for
   an adjacent topic) — never auto-run them.
