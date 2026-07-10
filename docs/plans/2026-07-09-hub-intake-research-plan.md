# hub.intake + hub.research Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the `hub.intake` (guided multi-source feature intake) and `hub.research` (lens-scoped deep research with organized series output) skills per the approved spec at `/docs/specs/2026-07-09-hub-intake-research-design.md`, closing backlog #1 and #27(a).

**Architecture:** Two new SKILL.md procedure files in the `hub.*` operational family, a new `conventions/research.md` pinning the research-series contract, one `redhat-ai.yaml` domain config for the competitive lens, and a warning-only addition to `scripts/hublib/schema.py` that lints research-doc frontmatter. Skills reuse `hub.file`'s filing procedure and `hub.consolidate`'s batch-gate pattern by reference — no changes to existing skills.

**Tech Stack:** Markdown skill procedures (`.claude/skills/`), Python 3.11 + pyyaml (linter), pytest (`scripts/tests/`).

## Global Constraints

- This repo is **PUBLIC**: no customer names, deal context, dollar figures, or agreement language in any tracked file, ever.
- `python scripts/hub_lint.py` must report **0 errors** after every task (warnings allowed; the repo currently emits 47 pre-existing warnings — do not add new ones except where a task says so).
- `python scripts/hub_index.py --check` must report 0 stale files after every task.
- Research-doc lint findings are **warnings only** — the 21 pre-convention docs in `features/agent-memory/research/` must never fail the build (they all carry `description` + `timestamp` today, so the expected new-warning count on this repo is **zero**).
- `AGENTS.md` has a hard 150-line CI budget (currently 71 lines; lint errors above 150).
- No behavior changes to `hub.file`, `hub.capture`, or `hub.consolidate`.
- Markdown links use leading-slash repo-root form (`/conventions/research.md`); files are UTF-8 with LF newlines.
- No new Python dependencies.
- Every commit message ends with `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- Run all commands from the repo root: `C:\Users\peter\code\rh\rhoai-agentic-hub` (POSIX path `/c/Users/peter/code/rh/rhoai-agentic-hub`).

---

### Task 1: conventions/research.md — the series contract

**Files:**
- Create: `conventions/research.md`

**Interfaces:**
- Consumes: nothing (first task).
- Produces: the convention document that Tasks 2–4 reference by path (`/conventions/research.md`), including the lens vocabulary (`landscape`, `upstream`, `architecture`, `requirements`, `competitive`), the exempt filenames (`index.md`, `REVIEW-NOTES.md`), and the frontmatter contract (`title`, `description`, `timestamp`, `lens`, `review_after`).

- [ ] **Step 1: Write the file**

Create `conventions/research.md` with exactly this content:

```markdown
# Research series conventions

`research/` directories (feature or narrative skeleton) hold deep
documents — the numbered-series contract below. Typed atoms (facts, refs,
questions) belong in `knowledge/`, not here; research runs propose them
separately through the gate.

## The series

- `00-executive-summary.md` — the living synthesis. Rewritten on every
  refresh; lists every doc in the series; records lens gaps with the exact
  retry invocation ("competitive lens not run — retry with
  `hub.research <home> competitive`").
- `01..N` — one doc per lens or subtopic, filename `NN-<slug>.md`.
  Numbering never restarts; refresh runs continue where the series left
  off.
- `REVIEW-NOTES.md` — human rulings on the series (what is DECIDED vs
  EXPLORATORY). Written by the owner, never by research runs. No
  frontmatter required.

## Frontmatter (research docs)

`title` · `description` (one line, written for someone deciding whether
to open it) · `timestamp` (ISO date) · `lens`
(`landscape|upstream|architecture|requirements|competitive` — omit for
pre-convention or migrated docs; `source:` marks migrated provenance) ·
`review_after` (ISO date). The linter checks `description` and
`timestamp` as **warnings only** — research docs never fail the build.
`index.md` and `REVIEW-NOTES.md` are exempt.

## Refresh & supersede

- A refresh rewrites `00-executive-summary.md` and appends new numbered
  docs; it never deletes.
- A finding contradicted by newer research gets a supersede note **in the
  old doc** — a blockquote directly under its H1:
  `> Superseded 2026-07-09 by [NN-slug](NN-slug.md) — <one line why>.`
  The old doc keeps its place in the series.
- Conflicts between new findings and existing knowledge entries are
  surfaced at the write gate, never auto-resolved.

## Producers

`hub.research` (primary), `hub.intake` (offers the kickoff),
`hub.migrate` (imports old-repo series; `source:` marks provenance).
The reference series:
[agent-memory research](/features/agent-memory/research/00-executive-summary.md).
```

- [ ] **Step 2: Verify lint and index stay clean**

Run: `python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: `hub_lint: 0 error(s), 47 warning(s)` and `hub_index --check: 0 stale file(s)`. (Before this task the count is 50 — this plan document links `/conventions/research.md` three times; creating the file resolves those three broken-link warnings back to the 47 baseline.)

- [ ] **Step 3: Commit**

```bash
git add conventions/research.md
git commit -m "conventions: research series contract (numbering, frontmatter, refresh/supersede)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Linter — research-doc frontmatter warnings (TDD)

**Files:**
- Modify: `scripts/hublib/schema.py` (constant near line 26, new function after `_lint_artifacts` ~line 127, two call sites in `_lint_tree` ~lines 203 and 220)
- Test: `scripts/tests/test_schema.py` (append)

**Interfaces:**
- Consumes: the contract from Task 1 (`description`/`timestamp` as warnings; `index.md`/`REVIEW-NOTES.md` exempt).
- Produces: `_lint_research(root, research_dir, warnings)` in `hublib.schema`, called from `_lint_tree` for every `features/<id>/research/` and `narrative/research/` (both the main tree and `restricted/`, since `_lint_tree` runs for both). Warning strings start with `<relpath>: research doc `.

- [ ] **Step 1: Write the failing tests**

Append to `scripts/tests/test_schema.py`:

```python
RESEARCH_DOC = ("---\ntitle: T\ndescription: d\ntimestamp: 2026-07-09\n"
                "lens: landscape\nreview_after: 2026-10-09\n---\nbody\n")


def test_valid_research_doc_no_warnings(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/research/01-landscape.md", RESEARCH_DOC)
    errors, warnings = lint_repo(root)
    assert errors == []
    assert not any("research doc" in w for w in warnings)


def test_research_doc_missing_description_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/research/01-landscape.md",
          "---\ntitle: T\ntimestamp: 2026-07-09\n---\nbody\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("research doc missing 'description'" in w for w in warnings)


def test_research_doc_without_frontmatter_is_warning_not_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/research/02-notes.md", "# just a heading\nbody\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("research doc lacks frontmatter" in w for w in warnings)


def test_review_notes_and_index_exempt_from_research_lint(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/research/REVIEW-NOTES.md", "# rulings\n")
    write(root, "features/x/research/index.md", "# idx\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert not any("research doc" in w for w in warnings)


def test_narrative_research_doc_missing_timestamp_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "narrative/research/01-x.md",
          "---\ntitle: T\ndescription: d\n---\nbody\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("research doc missing 'timestamp'" in w for w in warnings)
```

- [ ] **Step 2: Run the new tests to verify they fail**

Run: `python -m pytest scripts/tests/test_schema.py -v -k research`
Expected: exactly 3 FAIL, 2 pass vacuously. `test_research_doc_missing_description_is_warning`, `test_research_doc_without_frontmatter_is_warning_not_error`, and `test_narrative_research_doc_missing_timestamp_is_warning` FAIL their `any(...)` assertions (nothing lints research dirs yet — this proves the check does not exist). `test_valid_research_doc_no_warnings` and `test_review_notes_and_index_exempt_from_research_lint` pass vacuously; that is expected.

- [ ] **Step 3: Implement `_lint_research`**

In `scripts/hublib/schema.py`, add the constant directly below the existing `RESERVED = {"index.md", "log.md"}` line:

```python
RESEARCH_EXEMPT = {"index.md", "REVIEW-NOTES.md"}
```

Add this function directly after `_lint_artifacts` (before `lint_entry`):

```python
def _lint_research(root, research, warnings):
    """Research series docs (conventions/research.md). Warnings only —
    pre-convention series must never fail the build."""
    if not research.is_dir():
        return
    for doc in sorted(research.glob("*.md")):
        if doc.name in RESEARCH_EXEMPT:
            continue
        rel = _rel(root, doc)
        try:
            meta, _ = frontmatter.load_file(doc)
        except frontmatter.FrontmatterError:
            warnings.append(f"{rel}: research doc lacks frontmatter "
                            f"(see conventions/research.md)")
            continue
        for field in ("description", "timestamp"):
            if not meta.get(field):
                warnings.append(f"{rel}: research doc missing '{field}' "
                                f"(see conventions/research.md)")
```

Wire the two call sites in `_lint_tree`. In the feature loop, directly after the `_lint_artifacts(root, feat / "enablement", errors, warnings, feature_ids)` line, add:

```python
            _lint_research(root, feat / "research", warnings)
```

In the narrative block, directly after the `_lint_artifacts(root, narrative / "enablement", errors, warnings, feature_ids)` line, add:

```python
        _lint_research(root, narrative / "research", warnings)
```

- [ ] **Step 4: Run the new tests to verify they pass**

Run: `python -m pytest scripts/tests/test_schema.py -v -k research`
Expected: all 5 PASS.

- [ ] **Step 5: Run the full suite + lint the real repo**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py`
Expected: all tests PASS; `hub_lint: 0 error(s), 47 warning(s)` — the count must NOT increase (all 21 agent-memory research docs already carry `description`+`timestamp`; if new `research doc` warnings appear, a real repo file regressed — investigate, do not adjust the linter).

- [ ] **Step 6: Commit**

```bash
git add scripts/hublib/schema.py scripts/tests/test_schema.py
git commit -m "lint: research-doc frontmatter contract as warnings (conventions/research.md)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: hub.research skill + redhat-ai domain config

**Files:**
- Create: `.claude/skills/hub.research/SKILL.md`
- Create: `.claude/skills/hub.research/domains/redhat-ai.yaml`

**Interfaces:**
- Consumes: `/conventions/research.md` (Task 1); existing skills referenced by name: `hub.intake` (created in Task 4 — the forward reference is intentional and lands one commit later), `hub.doctor`.
- Produces: the skill Task 4's step 6 and Task 5's docs reference as `hub.research`; the domain-config shape (`name`, `slug`, `default`, `features`, `key_question`, `positioning_context`, `search_areas[].{name,topics,sources}`).

- [ ] **Step 1: Write SKILL.md**

Create `.claude/skills/hub.research/SKILL.md` with exactly this content:

```markdown
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
jira-gap (FUTURE — refuse politely; activates when the Jira hub skills
land, backlog #2).

1. RESOLVE HOME: feature id → features/<id>/research/; story-shaped →
   narrative/research/. Free topic with no home in
   features/features.yaml → offer hub.intake first (research needs a home
   to write into); stop there if declined.
2. CONTEXT LOAD: read <home>/knowledge/index.md (if present), every doc
   in the existing <home>/research/ series, and open question- entries
   for the home. Open questions become research inputs. A non-empty
   series ⇒ this is a REFRESH run.
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
   context summary + the lens definition + (competitive only) the domain
   config from domains/*.yaml — pick by explicit ask, then by `features:`
   match, then `default: true`. Sources: web search/fetch, GitHub, Google
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
   not the scripts). Commit:
   `git add -A && git commit -m "research(<home>): <lenses> <depth>"` &&
   `git push`.
8. Offer follow-ups the run surfaced (a deeper lens pass, hub.intake for
   an adjacent topic) — never auto-run them.
```

- [ ] **Step 2: Write the domain config**

Create `.claude/skills/hub.research/domains/redhat-ai.yaml` with exactly this content (reshaped from pm-toolkit `skills/research/domains/redhat-ai.yaml`: `output_path`, `knowledge_sources`, and `jira:` dropped — the hub's series convention, context load, and future jira-gap lens replace them):

```yaml
# Domain config for the hub.research competitive lens.
# Selection order: explicit ask > `features:` match > `default: true`.
name: "Red Hat AI"
slug: redhat-ai
default: true
# features: []  # optional hub feature ids that auto-select this domain

key_question: >
  How is Red Hat AI positioned in the enterprise AI platform market,
  what are competitors doing, and what industry trends should we be
  tracking?

positioning_context: >
  Red Hat ships a full-stack enterprise AI platform: RHEL AI
  (single-node), OpenShift AI (orchestrated), AI Inference Server
  (vLLM-based), and llm-d (distributed inference). Key differentiators
  are open source, hybrid/multi-cloud portability, and NVIDIA
  partnership. Evaluate findings against this positioning.

search_areas:
  - name: Enterprise AI Platforms
    topics:
      - enterprise AI platform comparison 2026
      - Kubernetes-native AI platforms
      - hybrid cloud AI deployment
      - on-prem vs cloud AI infrastructure trends
    sources: [company-blogs, product-announcements, analyst-reports]

  - name: Direct Competitors
    topics:
      - NVIDIA AI Enterprise updates
      - IBM watsonx releases and roadmap
      - Google Vertex AI new features
      - AWS SageMaker updates
      - Azure AI platform changes
      - Databricks Mosaic AI
      - Anyscale Ray AI platform
    sources: [company-blogs, product-announcements, press-releases]

  - name: Open Source AI Ecosystem
    topics:
      - vLLM releases and adoption
      - InstructLab community growth
      - KServe ModelMesh updates
      - open source LLM inference engines
      - open source AI training frameworks
    sources: [github, blogs, reddit, hacker-news]

  - name: Industry Trends
    topics:
      - enterprise AI adoption trends
      - AI infrastructure spending
      - sovereign AI and data residency requirements
      - EU AI Act compliance enterprise impact
      - AI regulatory trends
    sources: [analyst-reports, news, blogs]

  - name: Analyst Coverage
    topics:
      - Gartner Magic Quadrant AI platforms
      - Forrester Wave AI infrastructure
      - IDC MarketScape AI
      - Red Hat analyst mentions AI
    sources: [analyst-reports, news]

  - name: Partner Ecosystem
    topics:
      - NVIDIA Red Hat partnership updates
      - IBM Red Hat AI integration
      - cloud provider Red Hat AI support
      - hardware vendor AI validated platforms
    sources: [press-releases, company-blogs]

# jira-gap (future): when the Jira hub skills land (backlog #2), a jira:
# block here (project/components/jql) will drive the gap-analysis lens.
```

- [ ] **Step 3: Verify**

Run: `python -c "import yaml,sys; yaml.safe_load(open('.claude/skills/hub.research/domains/redhat-ai.yaml',encoding='utf-8')); print('yaml ok')" && python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: `yaml ok`; `hub_lint: 0 error(s), 47 warning(s)`; `0 stale file(s)` (`.claude/` is not linted — counts unchanged).

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/hub.research
git commit -m "skills: hub.research — lens-scoped deep research with series output (#1, #27a)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: hub.intake skill

**Files:**
- Create: `.claude/skills/hub.intake/SKILL.md`

**Interfaces:**
- Consumes: `hub.file` steps 1–5 (referenced, unchanged), `hub.capture` step 2's qa dedupe rule (referenced), `hub.research` (Task 3) by name, `/conventions/research.md`, `/conventions/uris.md`.
- Produces: the `hub.intake` skill referenced by Task 3 step 1 and Task 5's docs.

- [ ] **Step 1: Write SKILL.md**

Create `.claude/skills/hub.intake/SKILL.md` with exactly this content:

```markdown
---
name: hub.intake
description: Guided multi-source intake — onboard a new feature area or bulk-add sources to an existing one. Accepts a topic plus any pile of sources (URLs, Google Docs, Slack permalinks, Jira/RFE links, transcripts, pasted notes), routes to a home, files ref- entries, extracts typed entries through a batch gate, and offers a hub.research kickoff. Use when the user says "add a new feature <x>", "onboard <topic>", "intake these", "here's everything on <topic>", or drops multiple sources at once. A single source → hub.file is the faster path.
---

# hub.intake

Input: topic + sources (URLs, GDocs, Slack permalinks, Jira/RFE links,
transcript files, pasted text) from the prompt. Ask ONCE, upfront, for
anything obviously missing (no topic, or no sources and no facts to
file) — then run the flow without further questions until the gate.

1. ROUTE HOME: match the topic against features/features.yaml;
   story-shaped (pillar/cross-feature narrative) → narrative/. No fit →
   propose a new partition (id, title, one-line description) per
   hub.file step 1: on approval append to features.yaml and create ONLY
   the subdirectories this intake needs. A NEW partition also gets a
   starter knowledge/fact-<id>-overview.md (what it is, current status,
   key links) built from the user's basic info.
2. FILE SOURCES: each source per hub.file steps 2-5 — canonical URI
   (/conventions/uris.md), ref- entry with a load-bearing one-line
   description, transcripts → <home>/work/transcripts/ (gitignored) with
   a tracked ref- pointing at the source system, NDA-adjacent →
   restricted/ mirror. Jira/RFE links: ref- entry with the URL only
   (field ingestion arrives with the Jira hub skills, backlog #2).
   Unreachable source (paywall, auth, dead link): still draft the ref-
   (the pointer is real knowledge), mark its gate line `fetch failed`.
   MCP down → say so, offer pasted content, point at hub.doctor check.
3. EXTRACT: read the fetchable sources; draft typed entries for what is
   inside — fact-, decision-, question-, person-, qa- (dedupe per
   hub.capture step 2 — recurrence appends to asks:, never duplicates).
   Multi-feature material keeps the primary home and declares
   `features: [ids]`. Draft in the session/scratchpad — no repo writes
   before the gate.
4. BATCH GATE: one table — every proposed write, one line:
   `path: description [public|restricted] [new|update]`. Full content on
   request. Approve/edit/reject per line; nothing touches the repo
   before OK. Customer names/deal context → restricted/ sibling; dollar
   figures and agreement language never go to tracked files.
5. On OK: write the approved files, run `python scripts/hub_index.py`,
   then `python scripts/hub_lint.py` (0 errors — fix the written
   content, not the scripts). Commit:
   `git add -A && git commit -m "intake(<home>): <topic>"` && `git push`.
6. OFFER RESEARCH: suggest `hub.research <home>` with a lens set fitted
   to what intake revealed (unknown competitive space → competitive;
   heavy technical sources → architecture + upstream; scoping gaps →
   requirements). Never auto-run.
```

- [ ] **Step 2: Verify**

Run: `python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: `hub_lint: 0 error(s), 47 warning(s)`; `0 stale file(s)`.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/hub.intake
git commit -m "skills: hub.intake — guided multi-source feature intake (#1)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: Docs, backlog, and log updates

**Files:**
- Modify: `AGENTS.md` (skills table, after the `hub.file` row)
- Modify: `docs/skills.md` (chains list, quick-reference table, in-depth section)
- Modify: `docs/enhancements.md` (priority table rows 1 and 27, prose sections 1 and 27, Done section)
- Modify: `memory/log.md` (today's heading)

**Interfaces:**
- Consumes: skill names and one-line behaviors from Tasks 3–4; the commit hash of Task 4 (`git log -1 --format=%h` after Task 4's commit) for the Done entry.
- Produces: nothing downstream — this is the shipping paperwork.

- [ ] **Step 1: AGENTS.md — two skill rows**

In the `## Skills` table, directly after the `| hub.file | ... |` row, insert:

```markdown
| hub.intake | onboard a feature area / bulk-add sources (gated batch; offers research) |
| hub.research | lens-scoped deep research → research/ series + gated entries |
```

Then run: `wc -l AGENTS.md` — Expected: 73 (well under the 150 budget).

- [ ] **Step 2: docs/skills.md — chains, table, in-depth**

(a) In `## The common chains`, directly after the `- **Intake:** ...` bullet, add:

```markdown
- **Intake at scale:** topic + a pile of sources → `hub.intake` → home
  routed (partition created if new), sources filed, entries batch-gated →
  offers a `hub.research` kickoff.
- **Research:** `hub.research <feature|narrative> [lenses] [depth]` →
  plan gate (lenses × quick/standard/deep) → fan-out → numbered series
  under `research/` + gated knowledge entries + living
  `00-executive-summary`. Series contract:
  [/conventions/research.md](/conventions/research.md).
```

(b) In the `## Quick reference` table, directly after the `hub.file` row, add:

```markdown
| `hub.intake` | onboard a new feature area or bulk-add sources | plan confirm + batch write gate | partition (first use), ref-/typed entries, reindex + commit |
| `hub.research` | deep research on a feature/narrative topic | plan gate + batch write gate | `research/` series + knowledge entries, reindex + commit |
```

(c) In `## The hub.* skills in more depth`, directly after the `**hub.file**` paragraph, add:

```markdown
**`hub.intake`** — the guided multi-source front door: topic + a pile of
sources (URLs, GDocs, Slack permalinks, Jira/RFE links, transcripts,
pasted notes). Routes to a home (creating the partition per `hub.file`'s
procedure when new — plus a starter `fact-<id>-overview.md`), files each
source per `hub.file` steps 2–5, extracts typed entries, and gates the
whole batch in one table before writing anything. Ends by offering a
`hub.research` kickoff — never auto-runs it. One source? Use `hub.file`.

**`hub.research`** — standalone deep research on any feature or narrative
topic, organized per [/conventions/research.md](/conventions/research.md).
Lenses (landscape · upstream · architecture · requirements · competitive
— the last driven by `domains/*.yaml` configs; a future `jira-gap` lens
waits on the Jira hub skills) are scoped by your prompt: name lenses and
only those run. Two gates: a plan gate (lenses × depth
quick/standard/deep, a hard cap) before any fan-out, and a batch write
gate before any file lands. Re-runs are refreshes: numbering continues,
`00-executive-summary` is rewritten, contradicted findings get supersede
notes — never deletions. Tracker/NDA-sourced findings route to
`restricted/`.
```

- [ ] **Step 3: docs/enhancements.md — close #1, re-scope #27**

(a) Priority table: **delete** the row starting `| 1 | \`hub.intake\` — feature intake skill with research |`.

(b) Priority table: **replace** the row starting `| 27 |` with:

```markdown
| 27 | Jira gap analysis — `hub.research` jira-gap lens (remainder of the pm-toolkit research port) | **Medium–High** — "NOT building" early warnings mapping competitor moves vs. active Jira work; the competitive-sweep half shipped 2026-07-09 as the `hub.research` competitive lens | Medium | After #2 |
```

(c) In `## Agent-usage enhancements`: **delete** the entire `**1 · \`hub.intake\` — feature intake skill with research.**` paragraph (it moves to Done).

(d) In `## Agent-usage enhancements`: **replace** the entire `**27 · Competitive research with Jira gap analysis.**` paragraph with:

```markdown
**27 · Jira gap analysis (`hub.research` jira-gap lens).** The remaining
half of the pm-toolkit research port: strategic alignment analysis that
maps active Jira work against competitive developments and surfaces "NOT
building" gaps as early warnings. Ships as a `hub.research` lens (the
skill already names it as FUTURE) once #2 provides the Jira intake
pipeline; the domain YAML gains a `jira:` block (project/components/JQL)
to drive it. The competitive sweep half — domain-config-driven web
research (`domains/redhat-ai.yaml`) — shipped 2026-07-09 as the
`hub.research` competitive lens (see Done).
```

(e) In `## Done`, replace the placeholder line `- (Move items here with date + commit when they ship.)` with (substitute `<hash>` with Task 4's commit hash from `git log --format=%h --grep="hub.intake" -1`):

```markdown
- **#1 `hub.intake` + `hub.research`** — shipped 2026-07-09 (`<hash>`):
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
```

(f) Update the header line `**Owner:** Peter Double · **Last groomed:** 2026-07-09` — the date is already today; leave as is.

- [ ] **Step 4: memory/log.md — ship line**

Under the `## 2026-07-09` heading (create it at the TOP of the body, directly after the frontmatter, if absent), add:

```markdown
- **Creation** — hub.intake + hub.research skills shipped (backlog #1,
  #27a): conventions/research.md series contract, warning-only research
  lint, domains/redhat-ai.yaml. #27(b) jira-gap re-scoped, gated on #2.
```

- [ ] **Step 5: Reindex, lint, verify**

Run: `python scripts/hub_index.py && python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: lint `0 error(s)` (warning count may shift only if enhancements.md edits removed/added links — broken-link warnings must not increase); `0 stale file(s)`.

- [ ] **Step 6: Commit**

```bash
git add AGENTS.md docs/skills.md docs/enhancements.md memory/log.md memory/index.md
git commit -m "docs: ship hub.intake + hub.research — backlog #1 done, #27 re-scoped to jira-gap

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

(If `hub_index.py` regenerated other `views/*` or `index.md` files, `git add -A` instead — generated files must ship with the edit that staled them.)

---

### Task 6: Full verification + push

**Files:** none created or modified (verification only).

**Interfaces:**
- Consumes: everything above.
- Produces: a green CI run on `main`.

- [ ] **Step 1: Full local verification**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: all tests PASS; `0 error(s)`; `0 stale file(s)`.

- [ ] **Step 2: Push and watch CI**

```bash
git push
gh run watch --exit-status $(gh run list --workflow=validate.yml --limit 1 --json databaseId --jq '.[0].databaseId')
```

Expected: `validate.yml` completes successfully. If it fails, read the log (`gh run view --log-failed`), fix in the offending file (never by weakening the linter/tests), commit, and re-push.

---

## Acceptance runs (owner-in-the-loop — NOT subagent tasks)

The spec's real acceptance gate. These are live sessions with Peter at the
gates and real web/MCP access; run them in normal working sessions after
the plan lands, roughly in this order (5 is the richest fixture — run it
early):

- [x] 1. `hub.intake` on a genuinely new small topic: partition created,
  2–3 sources filed, entries gated, CI green after push. *(2026-07-09,
  `b543a4f` — mcp-catalog: partition + 3 new entries + 2 dedupe-driven
  updates; single write-gate covered partition creation cleanly.)*
- [x] 2. `hub.intake` against an existing feature with new sources (the
  bulk-add path). *(2026-07-10, `daaef27` — agent-memory: 3 meeting
  transcripts → 3 facts + 2 refs + 1 person + 2 dedupe-driven updates;
  transcripts to gitignored work/transcripts/; dedupe correctly skipped
  4 already-filed sources.)*
- [x] 3. `hub.research` quick run, single lens, on the new partition —
  series born with `00` + one lens doc. *(2026-07-09, `c49269e` —
  combined with run 4 into one standard 2-lens run on mcp-catalog;
  series born (00–02), gated entries incl. a cross-partition supersede.
  The quick-depth no-fan-out path itself is still unexercised — cover it
  in run 5 by doing the agent-memory refresh at quick depth.)*
- [x] 4. `hub.research` "competitive only" on an existing feature with
  `redhat-ai.yaml` — verifies prompt scoping + domain configs.
  *(2026-07-09, `c49269e` — prompt scoping held (2 named lenses ran, no
  additions), the domain config drove the competitive brief, and the
  adversarial verify pass caught 1 refuted + 2 softened claims before
  the gate.)*
- [ ] 5. Refresh on `features/agent-memory/research/` — numbering
  continues at 19, `00` refresh proposed through the gate.

Findings from these runs are skill edits (normal commits), not plan
changes. Check items off here as they complete.
