# Skills guide

Skills are how the repo stays organized *over time* — the second charter
pillar. They live in `.claude/skills/<name>/SKILL.md` and come in three
families (design decisions D8/D11):

1. **`hub.*` operational skills** — maintain the structure itself: capture,
   consolidate, file, reindex, publish, migrate, doctor. Built for this repo.
2. **First-party content skills** — produce content (decks, blogs, the
   customer tracker). Ported from the predecessor repo as *reviewed,
   adapted* ports — output routing, publish handoff, and knowledge lookups
   were rewritten to hub conventions; the craft content was preserved.
3. **Marketplace skills** — shared across repos (`rfe.*`, `strat.*`,
   `assess-rfe`, …), installed from the ODH skills-registry plugin
   marketplace wired in `.claude/settings.json`. Verify with `/plugin`
   inside Claude Code.

## The common chains

- **Capture:** work normally → durable item surfaces → `hub.capture` (one
  item, seconds) — or at session end, `hub.consolidate` (batch sweep of
  `memory/.scratch/` + the session). Both gate, reindex, and commit.
- **Intake:** new Google Doc / PDF / URL / transcript → `hub.file` → typed
  knowledge entry in the right feature partition (creates the partition on
  first use).
- **Artifact:** `presentation-create` (or `blog-mockup`) → self-contained
  `features/<f>/enablement/<slug>/` → `hub.publish` → live on the pages
  site. Building never publishes by itself.
- **Blog:** `blog-create` → multi-agent draft/review pipeline under
  `enablement/` → final draft ships via **Workfront**, not `hub.publish`.
- **Customer tracker:** `customer-feedback-ingest` (add/update from a
  transcript or notes) → `customer-feedback-refresh` (staleness/accuracy
  audit) → `customer-feedback-sync` (diff against the shared Google Sheet,
  push approved changes via the rhai-tracker MCP). Tracker data is
  restricted — it lives under `restricted/`, never tracked.
- **Migration:** something from the old repo needed here → `hub.migrate`
  (reshapes to conventions; never edits the old repo).
- **Health:** `hub.doctor` (machine setup/check), `hub.reindex`
  (indexes + lint after edits).

## Quick reference

| skill | use when | gated? | writes |
|---|---|---|---|
| `hub.capture` | one durable item surfaces mid-session | inline confirm | memory or knowledge entry + reindex + commit |
| `hub.consolidate` | session end / "consolidate memory" | batch approve/edit/reject, per-item public-vs-restricted | tracked store + clears `.scratch/` + one commit |
| `hub.file` | intake an external source as knowledge | confirm (incl. partition creation) | `ref-`/typed entry, `features.yaml` on first use |
| `hub.reindex` | after adding/editing entries; CI reports stale indexes | no | regenerates all `index.md` + `views/`, runs linter |
| `hub.doctor` | new machine; something feels broken | setup mode confirms writes | per-machine config only (see [/docs/tooling.md](/docs/tooling.md)) |
| `hub.publish` | ship an enablement artifact to the public site | disclosure confirm | `publish/manifest.yaml` entry |
| `hub.migrate` | bring old-repo content over | ruling per item | hub files only; old repo is read-only |
| `presentation-create` | "create a presentation about X" | output path confirm | `features/<f>/enablement/<slug>/index.html` |
| `blog-create` | draft/review a Red Hat blog post | pipeline checkpoints | drafts under `enablement/`; ships via Workfront |
| `blog-mockup` | quick branded HTML preview of blog content | no | preview HTML under `enablement/` |
| `customer-feedback-ingest` | new customer signal from a transcript/email/Jira | confirm per change | `restricted/` tracker only |
| `customer-feedback-refresh` | audit the tracker for staleness/accuracy | proposals confirmed | `restricted/` tracker only |
| `customer-feedback-sync` | push tracker changes to the shared Sheet | diff approved before push | Google Sheet via rhai-tracker MCP |

## The `hub.*` skills in more depth

**`hub.capture`** — the hot path into the tracked store. Classifies the item
(profile update / new fact / knowledge entry), shows a one-line confirm,
files it in the right home per the boundary rule, reindexes, commits.
Roadmap/strategy/status changes are **profile updates** (in place +
`## History`), not new files. Field questions become qa- entries (dedupe
first — recurrence appends to asks:); user jobs become jtbd- entries;
story-shaped items route to narrative/knowledge/.

**`hub.consolidate`** — the batch gate. Sweeps `memory/.scratch/` and the
session, dedupes against the store, classifies each candidate (profile
update / new fact / knowledge entry / RESTRICTED / discard), presents the
batch inline. Conflicts with existing profiles are surfaced, never
auto-resolved. Ends with reindex, scratch cleared, one commit. Details:
[/docs/memory.md](/docs/memory.md).

**`hub.file`** — intake. Normalizes the source URL to its canonical form
([/conventions/uris.md](/conventions/uris.md)), picks feature + type, writes
the entry with a load-bearing one-line `description`. If no feature fits, it
proposes a new partition (appending to `features/features.yaml` and creating
only the needed subdirectories) — the **only** sanctioned way partitions are
born. Transcripts land in `features/<f>/work/transcripts/` (gitignored) with
a tracked `ref-` entry pointing at them.

**`hub.reindex`** — wraps `python scripts/hub_index.py` + `hub_lint.py`.
Run it (or let capture/consolidate run it) after **any** entry edit —
CI fails on stale generated files, so "edit, forget to reindex, push" is the
most common way to go red.

**`hub.publish`** — publishing is a disclosure decision, so it is a skill
with a confirm, not a hand-edit. Adds/updates a manifest entry
(source/dest/audience/title/description) and re-states what will become
public. Pipeline mechanics: [/docs/publishing.md](/docs/publishing.md).

**`hub.migrate`** — the old repo
([ai-asset-registry](https://github.com/solaius/ai-asset-registry)) is
read-only source material. This skill brings content over *reshaped*: typed
entries, canonical URIs, re-timestamped, restricted content routed out, all
through the gate. Never a straight copy, never an edit to the old repo.

**`hub.doctor`** — `bash scripts/doctor.sh [check|setup]` with a skill
wrapper. `check` is read-only; `setup` installs deps and writes the
per-machine config (auto-memory redirect, `.mcp.json` for rhai-tracker, and
the user-level slack + google-workspace MCP servers with secrets from
`restricted/.env`). Section-by-section reference:
[/docs/tooling.md](/docs/tooling.md); MCP server guide:
[/docs/mcp-servers.md](/docs/mcp-servers.md).

## Content-skill notes

- `presentation-create` carries the Red Hat brand system in its
  `references/` (brand standards, design tokens, slide + diagram patterns)
  and two self-contained HTML templates. Artifacts must be self-contained
  directories — assets live inside `enablement/<slug>/`, nothing reaches
  into other features.
- `blog-create` and `blog-mockup` split on weight: full multi-agent pipeline
  with review gates vs. a quick branded preview. Only `blog-mockup` output
  ever goes near `hub.publish`, and only on request — real blogs publish
  through Workfront.
- The customer-feedback suite treats the shared **Google Sheet as
  canonical**; the local tracker is the working copy and `-sync` is the
  cross-machine reconciliation mechanism. All three skills keep customer
  names and deal detail inside `restricted/`.

## Adding or changing a skill

- One directory per skill: `.claude/skills/<name>/SKILL.md` (+ optional
  `references/`, `assets/`, `evals/`). The frontmatter `description` is the
  trigger — write it for the matcher, with the phrases users actually say.
- Follow the family split: structure maintenance → `hub.*` namespace;
  content production → plain name; shared/generic → contribute to the ODH
  marketplace instead of vendoring here.
- Any skill that writes tracked memory/knowledge must route through the
  gate (reuse `hub.capture`'s pattern rather than inventing a second gate),
  and any skill that produces publishable output must hand off to
  `hub.publish` rather than touching the manifest itself.
- Add a row to the skills table in [AGENTS.md](/AGENTS.md) (mind its
  150-line CI budget) and, if user-facing behavior changed, to this guide.
