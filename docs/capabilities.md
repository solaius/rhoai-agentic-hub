# What the hub can do

A complete guide to the hub's capabilities — for PMs evaluating whether
this system solves their problems.

**Three ways to read this:**
- [What problems does this solve?](#problems-this-solves) — scan the table,
  click what resonates
- [What does a day look like?](#a-day-in-the-life) — a walkthrough of how
  capabilities compose into real workflow
- [What can it do?](#capabilities) — the full capability breakdown by
  category

## Problems this solves

| If you've ever said... | The hub does this |
|---|---|
| "I lose context between sessions" | Two-tier memory with profiles that update in place plus an always-loaded index — no transcript replay needed. [Memory & Continuity](#memory--continuity) |
| "Knowledge is scattered across tools" | One routing rule (component × type) files everything in a predictable place, with nine generated cross-cutting indexes. [Knowledge Management](#knowledge-management) |
| "I can't find past decisions or their rationale" | Every decision is a typed entry with context, timestamp, and a supersede trail — never deleted. The decisions view shows all of them, newest first. [Knowledge Management](#knowledge-management) |
| "Enablement artifacts go stale" | Staleness audits run date-arithmetic plus live source cross-referencing (Jira, GDocs, GitHub); hub sites refresh from their sources with gated diffs. [Daily Operations](#daily-operations) and [Content Creation](#content-creation) |
| "RFE triage is tedious and inconsistent" | Scan open RFEs, review in a browser report, batch-apply labels/comments/transitions to Jira through an inline gate — the only skill with a Jira write surface, deliberately bounded. [Jira & Project Management](#jira--project-management) |
| "First 30 min every day: figuring out what needs attention" | Morning brief pulling Jira priorities, Slack messages, meeting action items, and AI news — structured as Urgent/Important/Monitor. [Daily Operations](#daily-operations) |
| "Research is one-off and never maintained" | Multi-lens fan-out with a living executive summary; re-runs are refreshes that update, never start from scratch. [Research & Strategy](#research--strategy) |
| "Strategy docs are disconnected from Jira reality" | One living strategy doc per component synthesized from knowledge + research + Jira — refresh rewrites in place with history, includes a Jira coverage map and gap-derived candidate RFEs. [Research & Strategy](#research--strategy) |
| "Customer feedback is trapped in transcripts" | Extract structured signals from notes/emails/Jira, track locally, sync to a shared Sheet — all data lives in a restricted encrypted tree. [Customer Tracking](#customer-tracking) |
| "Building a deck takes a full day" | Red Hat-branded slide decks and scrolling narratives in minutes — brand standards, design tokens, and templates built into the skill. [Content Creation](#content-creation) |
| "UI prototypes look nothing like the real product" | Prototypes are now real React + PatternFly 6 pages, built in the UXD team's RHOAI prototype fork with live internal previews. [Content Creation](#content-creation) |
| "I'm worried about leaking NDA content" | Inline approve on every tracked write with public-vs-restricted choice, encrypted restricted tree, publish allowlist, and disclosure lint. [Trust & Security](#trust--security) |

## A day in the life

**Morning (5 min):**

Run **[hub.standup](#daily-operations)** and read a structured brief. It pulls from your Jira portfolio, Slack messages and mentions, Gemini meeting notes for action items, and recent AI news, then sorts everything as Urgent/Important/Monitor. You know what needs attention before opening any tool.

**During the day (as things happen):**

- **New source material** (one doc or twenty) comes in. Fire **[hub.intake](#knowledge-management)** as the universal front door — it routes to a home (creating the component partition if new), files each source, extracts typed knowledge entries, and gates the whole batch before writing anything. Works for new components, narrative topics, transcripts, Google Docs, Slack threads, and Jira links.
- **A decision, date change, or useful link** surfaces mid-work. Hit **[hub.capture](#memory--continuity)** — the reflex for durable items. Takes seconds, not a filing exercise. It classifies (profile update / new fact / knowledge entry), shows a one-line confirm, files it in the right place, reindexes, and commits.
- **Need to go deeper** on a component or narrative topic. Run **[hub.research](#research--strategy)** and it fans out across lenses (landscape, upstream, architecture, requirements, competitive, jira-gap) with a living executive summary. Re-runs refresh — numbering continues, contradicted findings get supersede notes, nothing is lost.
- **Stakeholder asks for a deck.** Use **[presentation-create](#content-creation)** and get a Red Hat-branded slide deck or scrolling narrative in minutes — self-contained HTML with all assets, brand standards and design tokens built in.
- **Need a UI prototype** for stakeholder review. Run **[hub.prototype](#content-creation)** -- it loads the component's architecture, upstream repos, and strategy, queries PatternFly MCP for every component it will use, and generates a React page on a branch in the UXD fork; pushing the branch lands its live GitLab Pages preview URL in `views/prototypes.md`.
- **Customer meeting prep.** Check the **[restricted tracker](#customer-tracking)** for signals from prior conversations, then update it afterward with notes from the new meeting.
- **Jira issue quality check.** Run **[hub.jira-hygiene](#jira--project-management)** to audit one issue against type-specific checklists (naming, links, Fix Version, Components, labels) — read-only, reports findings in chat.

**Weekly / periodic:**

- **[hub.weekly-plan](#daily-operations)** — planning superset of standup. Adds Google Calendar analysis (time distribution, conflicts, no-meeting blocks), carry-over tracking from last week, and a living checklist file you can tick off as the week progresses.
- **[hub.jira-triage](#jira--project-management)** — scan open RFEs for a component, review in a browser report with full Jira fidelity, export decisions, approve a batch gate, and the skill applies labels/comments/transitions to Jira. The only skill that writes to Jira, with a deliberately narrow surface.
- **[hub.sweep](#daily-operations)** — staleness audit for a component. Runs date-arithmetic plus live source cross-referencing against Jira, GDocs, and GitHub. Flags what's stale and proposes gated updates.
- **[hub.strategy](#research--strategy)** — refresh a component's one living strategy doc. Synthesized from knowledge + research + Jira snapshot, rewritten in place with history. Includes a Jira coverage map and gap-derived candidate RFEs ready to feed RFE creation.
- **[hub.refresh-site](#daily-operations)** — update a published hub site from its live sources (GDocs, GitHub, Jira, Slack, local entries). Reports New/Changed/Confirmed-current per page and gates the whole batch before writing edits. The disclosure contract keeps customer/partner names and deal detail out.

**Session end:**

Run **[hub.consolidate](#memory--continuity)** to sweep scratch memory, dedupe against the store, classify each candidate (profile update / new fact / knowledge entry / RESTRICTED / discard), approve the batch, clear scratch, reindex, and commit. Everything durable from the session is now tracked; nothing is lost.

## Capabilities

### Knowledge Management

The hub files everything with one routing rule: **component × type**. That's it. Story-shaped content (pillars, cross-component stories, the strategy spine) goes in `narrative/`; everything else picks a component from the routing table. Current partitions: skills-registry, mcp-gateway, mcp-registry, mcp-catalog, mcp-lifecycle-operator, mcp-ecosystem, agent-registry, agent-memory, agent-ops, gen-ai-studio, and platform (cross-cutting). Each partition has the identical skeleton: `knowledge/`, `research/`, `strategy/`, `enablement/`, `prototype/`, `work/`.

**Key capabilities:**

- **hub.intake** — the universal front door. Onboard a new component area or bulk-add sources (URLs, GDocs, Slack permalinks, Jira/RFE links, transcripts, pasted notes). Routes to a home, files each source, extracts typed knowledge entries, and gates the whole batch. Creates the partition on first use. Offers a hub.research kickoff afterward.
- **Typed entries** — every knowledge item gets a type (decision, fact, reference, person, question, qa, jtbd) with fixed frontmatter (type, description, timestamp). Filename prefixes match the type. Decisions and facts are never deleted; superseded entries stay traversable.
- **Component partitions** — one per product area (skills-registry, mcp-gateway, …), each with the identical skeleton. Replaces the old 1,105-line monolith with predictable places.
- **Narrative layer** — `narrative/` is a peer of `components/`, same skeleton, for cross-component stories and strategic pillars. Connections declared via `components:` cross-reference fields, validated against the routing table, then generated — never hand-maintained.
- **Generated views** — nine cross-cutting indexes derived from frontmatter: decisions (newest first), FAQs (unanswered / most-asked / by component), JTBDs (status × component, evidence flagged), people (by component), Jira map (keys → entries), stale facts (past review_after), artifacts (enablement + publish state), narrative map (pillars → stories → components), open questions.
- **OKF v0.1 conformance** — structured markdown + YAML frontmatter; every entry has a type, description, and timestamp. Local extensions documented as producer extensions per the spec.

Nothing lands in an inconsistent place, nothing requires an ad-hoc filing decision, and you can find anything via the views.

### Memory & Continuity

The hub solves the "lose context between sessions" problem with a two-tier system: ungated scratch (harness writes freely) + gated tracked store (inline human approve on every write). Changed facts get updated in place with a history trail instead of re-explained. An always-loaded index means no transcript replay at session start.

**Key capabilities:**

- **Two-tier memory** — harness auto-memory redirected to `memory/.scratch/` (gitignored); hub.capture and hub.consolidate promote items to the tracked store (`memory/`) through the gate. Only what you approve becomes durable.
- **Profiles** — current state of volatile subjects (roadmap dates, stakeholder preferences, active work). Updated in place with a `## History` section, never duplicated. Always loaded at session start.
- **Facts** — dated atomic working facts. Superseded items never deleted, so you can trace how understanding evolved. `review_after` dates flag when facts need re-checking; the stale-facts view surfaces them.
- **hub.capture** — the hot path. File one durable item mid-session (decision, date change, link, preference). Takes seconds. Classifies (profile update / new fact / knowledge entry), shows a one-line confirm, files it in the right place per the boundary rule, reindexes, commits. Roadmap/strategy/status changes are profile updates, not new files.
- **hub.consolidate** — the batch sweep at session end. Reads `memory/.scratch/` and the session transcript, dedupes against the store, classifies each candidate (profile update / new fact / knowledge entry / RESTRICTED / discard), presents the batch inline for approve/edit/reject per item, then reindexes, clears scratch, and commits. Conflicts with existing profiles are surfaced, never auto-resolved.
- **Cross-machine via git** — tracked memory commits sync across machines. Per-machine config (auto-memory redirect, .mcp.json, MCP server secrets) managed by hub.doctor stays local.

Nothing durable gets lost, nothing is re-explained, and you start every session with full context.

### Research & Strategy

Research is no longer one-off. The hub runs multi-lens fan-outs with living executive summaries that refresh — re-runs update, never start from scratch. Strategy docs synthesize from knowledge + research + Jira and rewrite in place with history, so they stay honest to current reality.

**Key capabilities:**

- **hub.research** — standalone deep research on any component or narrative topic. Lenses (landscape, upstream, architecture, requirements, competitive, jira-gap) are scoped by your prompt: name lenses and only those run. Context load pulls the home's knowledge/research/questions plus its `related:` boundary siblings (sibling knowledge, research summaries, strategy docs, Jira snapshots all become standing context). Two gates: a plan gate (lenses × depth quick/standard/deep, a hard cap) before any fan-out, and a batch write gate before any file lands. Re-runs are refreshes: numbering continues, the living `00-executive-summary` is rewritten, contradicted findings get supersede notes — never deletions. Tracker/NDA-sourced findings route to `restricted/`. Output: a numbered series under `research/` plus gated knowledge entries.
- **hub.strategy** — the synthesis layer. One living strategy document per component (`strategy/strategy.md`, eight-section contract) built from the partition's knowledge entries, research series, Jira snapshot + refs, memory profiles, and `related:` siblings. PM working register — dense, 60-second re-entry brief, honest gaps section, Jira coverage map plus gap-derived candidate jiras ready for `/rfe.create`. Rewritten in place on refresh with a `## History` entry. Preconditions nudge toward hub.research / hub.jira-sweep first when those inputs are missing.
- **Natural handoffs** — hub.intake offers hub.research at the end; hub.research offers hub.strategy; hub.strategy's candidate jiras feed `/rfe.create`. Each step is a gate, never automatic.

Research that stays current, strategy that's honest to Jira reality, and candidate RFEs grounded in gaps you can prove.

### Content Creation

Building enablement no longer takes a full day. The hub generates Red Hat-branded slide decks, scrolling narratives, and multi-page hub sites with brand standards and design tokens built in. All artifacts are self-contained directories — assets live inside, nothing reaches into other components.

**Key capabilities:**

- **presentation-create** — create or update Red Hat-branded slide decks (keyboard-navigated, full-screen) or scrolling narratives (vertical-scroll, fixed header nav). Staged under a component's `enablement/<slug>/` as self-contained HTML with all assets. Brand standards, design tokens, and templates built into the skill's `references/`. Custom illustration assets supported. Building never publishes — hand off to hub.publish when ready.
- **blog-create** — multi-agent drafting + iterative review pipeline for Red Hat blog posts. Drafts land under `enablement/`. Final approved draft ships via **Workfront** (the Red Hat blog submission process), never hub.publish.
- **blog-mockup** — quick Red Hat-branded HTML preview of any blog content. Lightweight alternative to blog-create's full pipeline. Output ships via hub.publish only on request.
- **`hub.prototype`** -- UI prototypes as real React + PatternFly 6 pages
  in the UXD RHOAI fork (`pedouble/rhoai`, based off `upstream/3.6`, one
  branch per prototype). The skill deep-reads the component's knowledge,
  research, strategy, related components, Jira scope, and upstream repos,
  runs mandatory PatternFly MCP component planning, generates the page(s)
  + route + nav wiring in the fork, and verifies with the fork's own
  eslint + build. Pushing the branch yields a live internal preview at
  `<pages>/branch-<slug>/`; the hub records metadata in
  `prototype/<slug>/prototype.yaml` (branch, preview_url, versions as
  commits) and links the preview from `views/prototypes.md`. Versions are
  commits; side-by-side comparison via frozen `<slug>-vN` snapshot
  branches. Internal-only -- the preview URL is the artifact; nothing
  publishes through the pages site.
- **Knowledge hub sites** — multi-page enablement sites organized as understand/sell/build/govern/plan. Built with presentation-create, refreshable from live sources (GDocs, GitHub, Jira, Slack, local entries) via hub.refresh-site. Currently five hub sites live: MCP Gateway (23 pages), MCP Management (22 pages), MCP Catalog (14 pages), MCP Lifecycle Operator (16 pages), MCP Registry (12 pages).
- **Currently 19 enablement artifacts, 20 published** to the pages site. Landing page auto-generated with area grouping and NEW/UPDATED badges for artifacts published or changed in the last 14 days.

Everything is self-contained, brand-compliant, and ready to ship.

### Jira & Project Management

Jira is read-only everywhere except one skill. The hub sweeps scopes, diffs against stored snapshots, audits issue quality, and runs the RFE triage ceremony with a deliberately narrow write surface: add label, post comment, close, approve — that's the entire vocabulary.

**Key capabilities:**

- **hub.jira-sweep** — sweep Jira for one component. First run does conversational scope discovery (`--try-jql` iterations until the JQL looks right; approved scope stored as a `jira:` block in `components/components.yaml`). Every run fetches the scope, builds a whitelisted public snapshot (`work/jira-snapshot.yaml` — summaries admitted only when an unauthenticated probe proves the issue world-readable), picks strategic-tier issues (Outcome/Feature by default) as gated ref- candidates, and batches everything through one table. Read-only against Jira.
- **hub.jira-sync** — diff-driven refresh of stored scopes + watched keys against live Jira. Re-runs every stored scope, diffs against committed snapshots (NEW / CHANGED / VANISHED), and watches every Jira key referenced by ref- `resource:` URLs or jtbd `jira:` lists even outside the scopes. Consequences (snapshot refresh, ref- status notes, jtbd `delivered` nudges, new ref- candidates) proposed through the gate; an all-quiet run is a one-line report. Read-only against Jira.
- **hub.jira-hygiene** — read-only audit of one issue against type-specific checklists (Feature Request, Feature, DP/TP/GA maturity chain, Epic, all-issues basics). Checks naming, parent/clone links, Fix Version, Components, labels, refinement docs. Reports findings in chat, does not fix. A `help` mode answers hierarchy/lifecycle questions from the same checklist doc without touching Jira.
- **hub.jira-triage** — the periodic RFE triage ceremony for one component. `--scan` fetches the component's open Feature Requests (same stored `jira:` JQL scope), flags staleness, classifies, suggests an action per issue, and renders a browser report (full Jira fidelity, lands under `restricted/`). Review in the browser, export decisions, `--plan` renders them as a gate table, the skill shows that table as the inline batch gate (TRANSITIONS separate from LABELS/COMMENTS, since transitions are destructive), then `--apply` fires the write-back. **This is the only skill in the hub with a Jira write surface**, and it is deliberately narrow: add a label, post a comment, fire the `close` transition, fire the `approve` transition — that's the entire vocabulary. It cannot assign, edit fields, or create issues. Tracked result (`work/triage-log.yaml`) is prose-free by design (no summaries, no comment bodies) so it needs no redaction in this public repo.
- **RFE creation, review, assessment** — marketplace skills (rfe.*, assess-rfe) handle the full RFE lifecycle: feasibility, scope, testability, architecture review, auto-fix, split, speedrun, submit. Those skills can create issues; hub.jira-triage is the only **hub** skill that writes to Jira.
- **hub.enhance** — GitHub issue creation and tracking for the hub's own improvements. Bridges the narrative backlog (RFEs that improve this repo itself) and actionable issues with labels/milestones.

Jira writes are bounded, auditable, and gated. Everything else is read-only snapshots and diffs.

### Daily Operations

The first 30 minutes of every day used to be "figuring out what needs attention." Now it's a structured brief, and staleness audits run date-arithmetic plus live source cross-referencing so you know what's stale before stakeholders ask.

**Key capabilities:**

- **hub.standup** — morning brief pulling from Jira (PM portfolio queries), Slack (messages/mentions since last run), Gemini meeting notes (action items), and AI news feeds. Output structured as Urgent/Important/Monitor. You know priorities before opening any tool.
- **hub.weekly-plan** — weekly planning superset of standup. Adds Google Calendar analysis (time distribution by category, conflict detection, no-meeting focus blocks), carry-over tracking (last week's unfinished items), and a living checklist file (`work/weekly-plan-<date>.md`) you can tick off as the week progresses. Surfaces calendar red flags (back-to-back days with no focus time, double-booked slots).
- **hub.sweep** — per-component staleness audit. Runs date-arithmetic (entries past `review_after` or the staleness defaults) plus live source cross-referencing (Jira keys, GDocs URLs, GitHub issue links). Flags what's stale, what's moved, what's closed, and proposes gated updates (status notes, supersede nudges).
- **hub.refresh-site** — update path for already-published hub sites (RHCL, Management, or any site with a `work/refresh-<slug>.yaml` config). Sweeps the config's live sources (GDocs, GitHub, Jira, Slack, local hub entries) in parallel, reports New/Changed/Confirmed-current/Fetch-failures per page, and gates the whole batch before writing a single edit. The disclosure contract (never introduce customer/partner names or deal detail, anonymized phrasing only, full product name on first use) keeps NDA content out.
- **hub_status.py** — morning status page. Stale items, open questions, unanswered QA, evidence-less JTBDs, log rotation reminders, CI state. Run it before standup to know what's broken.

Morning brief in 5 minutes, staleness caught before it's a problem, and hub sites that stay current with their sources.

### Customer Tracking

Customer feedback used to be trapped in transcripts and email threads. The hub extracts structured signals, tracks locally in an encrypted tree, and syncs to a shared Sheet — all customer data stays in `restricted/`, never publicly tracked.

**Key capabilities:**

- **customer-feedback-ingest** — add or update a customer from a transcript, email, Jira ticket, or pasted notes. Extracts company, contact, use case, pain points, feature feedback, tooling preferences, deployment environment, and geo. Structured schema with component tagging (multi-component classification supported). All data lands in `restricted/` — never publicly tracked.
- **customer-feedback-refresh** — staleness and accuracy audit of the tracker. Flags entries missing sources, past review_after dates, or with stale Jira links. Proposes updates via the gate.
- **customer-feedback-sync** — diff the local tracker against the shared Google Sheet (canonical source), propose changes (new customers, updated fields, removed entries), and push approved changes via the rhai-tracker MCP server. The shared Sheet is the cross-machine truth; the local tracker is the working copy.
- **All customer data lives under `restricted/`** — git-crypt encrypted tree (plaintext locally when unlocked, opaque blobs on GitHub and in CI). The bar: customer-named risks, deal-specific numbers, SKU commitments, partner pipeline detail. Enforced by the capture gate's public-vs-restricted choice and disclosure lint.

Customer signals extracted, tracked locally, and synced to a shared Sheet — all protected by the encrypted tree.

### Integrations

The hub pulls context from your existing tools and pushes to the right places. It doesn't replace Jira, Google Workspace, or Slack — it orchestrates across them.

**Key integrations:**

- **Google Workspace** (MCP server) — Calendar (standup/weekly-plan time analysis, conflict detection), Drive (intake GDocs as refs, blog-create sourcing), Gmail (standup message scan), Docs/Sheets/Slides/Forms (refresh-site live sources), Tasks (weekly-plan checklist sync). Used by hub.standup, hub.weekly-plan, hub.intake, hub.refresh-site, customer-feedback-sync, blog-create.
- **Jira** — async REST client supporting Cloud + DC auth, scope-based sweeps, bounded write-back (triage only). Used by all hub.jira-* skills, marketplace rfe.* skills, hub.standup (portfolio queries), hub.research (jira-gap lens), hub.strategy (coverage map), hub.sweep (live cross-referencing).
- **Slack** (MCP server via podman container) — message access for standup briefs (messages/mentions since last run), search for refresh-site live sources. Used by hub.standup, hub.refresh-site.
- **GitHub** — issue management (hub.enhance), CI/CD (validate + publish workflows on every push/PR), pages publishing (manifest-driven pipeline pushes to separate pages repo). Used by hub.enhance, hub.sweep (issue cross-referencing), hub.refresh-site (live sources), CI automation.
- **rhai-tracker** (MCP server) — customer tracking Sheet sync. Used by customer-feedback-sync to push approved changes from the local restricted tracker to the canonical Google Sheet.

Pulls from Jira/Slack/Google, pushes to GitHub/Sheets/Jira (triage only), and everything stays in sync.

### Trust & Security

This repo is **public**. Every tracked write is world-readable. Three layers keep that safe: the capture gate (inline approve on every write), the encrypted restricted tree (git-crypt), and the publish allowlist (nothing ships without a manifest entry).

**Key protections:**

- **Capture gate** — no agent writes the tracked store (memory or knowledge entries) without an inline human approve. Every promotion gets an explicit public-vs-restricted call. hub.capture shows a one-line confirm; hub.consolidate shows a batch table per item (approve/edit/reject). Profile conflicts are surfaced, never auto-resolved.
- **`restricted/`** — tracked but encrypted via git-crypt. Mirrors the main layout (`restricted/components/…`, `restricted/memory/…`, `restricted/.env`). Files are plaintext locally when unlocked, opaque blobs on GitHub and in CI. The restricted bar: dollar figures, SKU specifics, customer-named risks, org-sensitive numbers, partner pipeline detail. Codified in `/conventions/memory.md` plus disclosure lint.
- **Publish allowlist** — nothing reaches the public pages site without a `publish/manifest.yaml` entry. The failure mode is *forgot to publish*, never *leaked by default*. hub.publish is the skill that adds manifest entries (disclosure confirm required).
- **Disclosure lint** — restricted-pattern scanning (local, from an optional gitignored pattern file) + generic heuristics (CI-visible) over enablement HTML and knowledge entries. Warns on matches: customer/partner names, deal-specific language, dollar figures, SKU commitments. CI runs this; `hub_lint.py` must report 0 errors before commit.
- **Pre-commit hooks** — doctor-installed, run lint + index freshness before every commit. Catches stale generated files, disclosure warnings, and schema violations before they hit CI.

The gates enforce the boundary, the restricted tree keeps secrets encrypted, and the publish allowlist keeps the failure mode safe.

### Publishing

Knowledge lives in this repo; published artifacts live in a separate pages repo. That decoupling means this repo could go private or move (e.g., VPN GitLab for Red Hat-internal knowledge) without breaking a single published URL.

**Key capabilities:**

- **Manifest-driven pipeline** — `publish/manifest.yaml` names what ships (source/dest/audience/title/description). CI applies it to the separate pages repo ([solaius/rhoai-agentic-hub-pages](https://github.com/solaius/rhoai-agentic-hub-pages)) on every push to main. The manifest is the truth.
- **Decoupled repos** — knowledge lives here, published artifacts live in the pages repo served by GitHub Pages. This repo could go private without breaking published URLs. A future `audience: internal` target (VPN GitLab Pages) can be added without touching the public one.
- **CI-driven** — `validate.yml` (schema/lint/index/manifest check) on every push/PR; `publish.yml` (apply manifest, check links, push pages) on main only. Links are checked in CI, not locally.
- **Landing page** — auto-generated with area grouping (mcp-gateway, mcp-registry, agent-memory, …) and NEW/UPDATED badges for artifacts published or changed in the last 14 days.
- **Audience targeting** — `audience: public` (live now on GitHub Pages) + `audience: internal` (schema-reserved for future VPN GitLab Pages target). Each manifest entry declares its audience.
- **Currently 20 published artifacts** across the pages site. Slide decks, scrolling narratives, hub sites, blog previews, RFE narratives, deep-dive decks.

Publishing is a disclosure decision (hub.publish skill, gated), not a hand-edit. The pipeline handles the rest.

### Setup & Health

New machine to working in 30 minutes. The doctor checks ten sections, fixes on request, and writes only per-machine config (never tracked files). Indexes regenerate from entry frontmatter, linter enforces the rules, and CI verifies everything before merge.

**Key capabilities:**

- **hub.doctor** — 10-section machine health check (check mode, read-only) or fix mode (setup). Checks Python deps, plugin installs, auto-memory redirect, restricted/.env (Jira/Slack/Google auth), MCP server wiring (rhai-tracker, slack, google-workspace), pre-commit hooks, git-crypt unlock, and CI state. `setup` mode installs deps and writes the per-machine config only (auto-memory redirect in `.claude/settings.local.json`, `.mcp.json` for rhai-tracker, user-level MCP server configs with secrets from `restricted/.env`). Handles platform differences (Windows, macOS, Linux).
- **hub.reindex** — regenerate all generated indexes and views (`components/index.md`, `components/*/index.md`, `components/*/knowledge/index.md`, `memory/index.md`, all `views/*`) + run the linter. Run it after any entry edit — CI fails on stale generated files, so "edit, forget to reindex, push" is the most common way to go red. hub.capture and hub.consolidate run this automatically.
- **Cross-platform** — doctor handles platform differences. Works on Windows (Git Bash / MSYS2), macOS, Linux.
- **CI pipelines** — `validate.yml` (every push/PR): runs linter, index freshness check, manifest schema check, and tests. `publish.yml` (main only): applies manifest, checks links, pushes to pages repo. Both run on GitHub Actions; no secrets in CI except git-crypt key (restricted tree stays opaque).
- **New machine to working in 30 minutes** with the setup guide (`/docs/setup.md`) + `hub.doctor setup`. Clone, unlock restricted, run doctor, done.

Health checks, linter enforcement, CI verification, and setup automation — operable without Peter in the room.
