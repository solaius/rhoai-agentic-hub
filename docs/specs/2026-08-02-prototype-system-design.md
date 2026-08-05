# Prototype system design

> **Superseded (2026-08-04):** principles P1/P3/P8 (static HTML, on-disk
> version dirs, static-over-React) are replaced by the UXD fork pipeline --
> see /docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md.
> The prototype/ skeleton leg, grounding flow, and gate discipline remain.

> Approved: 2026-08-02. Adds a `prototype/` skeleton leg, a `hub.prototype`
> skill, versioned prototypes grounded in real architecture, a generated
> portal, and the full documentation sweep.

## Problem

The hub produces enablement artifacts (decks, hub sites, blogs) but has no
structured path for interactive UI prototypes. Prototypes today land ad-hoc
in `enablement/` (the registry-ui-prototype) with no versioning convention,
no cross-component portal, and no grounding in the component's real
architecture. Stakeholder review and design iteration need a first-class
home.

## Decisions

| # | decision |
|---|---|
| P1 | Prototypes are self-contained static HTML + PatternFly 6 CDN -- no build step, no React, no dev server |
| P2 | `prototype/` is a new skeleton leg (sixth dir), peer of `knowledge/`, `research/`, `strategy/`, `enablement/`, `work/` |
| P3 | Explicit versioning: `prototype/<slug>/v1/`, `v2/`, etc. coexist on disk for side-by-side comparison |
| P4 | Cross-component prototypes live in `narrative/prototype/` (same convention as other cross-component content) |
| P5 | The central portal is a generated view (`views/prototypes.md` + `views/prototypes-portal.html`), not a maintained artifact |
| P6 | The skill deep-reads the component's knowledge, research, strategy, related components, Jira scope, upstream repos, and restricted context before generating -- prototypes are grounded in reality, not invented |
| P7 | PatternFly MCP is the mandatory accuracy mechanism -- every component used in a prototype must be validated against the MCP's v6 design guidelines, examples, and accessibility docs before HTML is generated |
| P8 | Static HTML over React -- the hub is a knowledge repo, not a codebase; prototypes serve stakeholder review and design iteration, not engineering handoff; the publish pipeline stays clean with no build step |

## Directory structure

### Per-component prototype

```
components/<id>/prototype/
  <slug>/
    prototype.yaml        # metadata
    v1/
      index.html          # entry point, self-contained
      assets/             # images, icons if needed
    v2/
      index.html
      assets/
```

### Cross-component prototype

```
narrative/prototype/
  <slug>/
    prototype.yaml
    v1/index.html
```

### prototype.yaml schema

```yaml
title: MCP Registry UI                     # required, human-readable
description: Interactive mockup of ...     # required
status: active                             # required: active | superseded | archived
current: v2                                # required: which version dir is "latest"
versions:                                  # required: map keyed by version dir name
  v1:
    timestamp: 2026-07-09
    summary: Initial list/detail layout
  v2:
    timestamp: 2026-07-15
    summary: Added version comparison and policy badge states
components: [mcp-registry]                 # required: component ids this prototype covers
```

Created on first use, never pre-created empty (same rule as other skeleton
legs).

## Generated views

### views/prototypes.md

Markdown cross-cutting view (like `views/decisions.md`). Lists all
prototypes grouped by component (routing-table order, narrative last),
showing title, status, current version, and timestamp.

### views/prototypes-portal.html

Self-contained HTML page (same pattern as the landing template). Prototype
cards with title, description, component badge, status, version selector
linking to each version's `index.html`, "Current" badge on the active
version. Grouped by component. Publishable via the manifest as an internal
artifact.

### Per-component index.md

Each component's generated `index.md` gains a Prototypes section listing
that component's prototypes with title, status, and current version.

## Publishing integration

### Individual prototypes

Published independently via `hub.publish`:

```yaml
- source: components/mcp-registry/prototype/registry-ui/v2/
  dest: mcp-registry/prototype/registry-ui/
  audience: internal
  title: MCP Registry UI Prototype (v2)
  description: Interactive mockup of the Registry list/detail/version UI
```

Source points at the version directory. Two manifest entries for two
published versions, or publish the whole slug directory with the generated
version-switching index.

### Version-switching index

When a prototype has more than one version, the indexer generates a
lightweight `index.html` at the prototype slug root
(`components/<id>/prototype/<slug>/index.html`) that lets users toggle
between versions. This file is generated (same `<!-- generated ... -->`
marker), never hand-edited. It enables publishing the whole slug directory
as one manifest entry instead of one-per-version.

### Central portal

```yaml
- source: views/prototypes-portal.html
  dest: prototypes/
  audience: internal
  title: Prototype Portal
  description: Auto-generated index of all prototypes across components
```

### Audience

Defaults to `internal`. Individual prototypes can be promoted to `public`
through the normal `hub.publish` gate.

## The hub.prototype skill

### Invocation modes

| command | what it does |
|---|---|
| `hub.prototype create <component>` | Create a new prototype under a component (or `narrative` for cross-component) |
| `hub.prototype version <component>/<slug>` | Add a new version to an existing prototype |
| `hub.prototype publish <component>/<slug>` | Hand off to `hub.publish` |
| `hub.prototype list` | Show all prototypes (shortcut for the generated view) |

### Create flow

1. **Context load** -- before asking a single design question, deep-read
   the component's ecosystem:
   - **Knowledge entries** -- architecture decisions, ref- entries pointing
     to design docs, upstream repos, API specs
   - **Research series** -- landscape, architecture, and requirements lenses
   - **Strategy doc** -- the living `strategy/strategy.md`
   - **Related components** -- follow `related:` links in `components.yaml`
     and load their knowledge/strategy (e.g., prototyping the MCP Catalog
     should understand the Registry's data model and the Lifecycle
     Operator's deployment flow)
   - **Jira scope** -- stored JQL and `work/jira-snapshot.yaml` for current
     feature state
   - **Upstream repos** -- any `ref-` entries pointing to GitHub/GitLab
     repos get browsed for real UI patterns, data models, API shapes
   - **Existing prototypes** -- prior versions in this or related
     components' `prototype/` for continuity
   - **Restricted context** -- if `restricted/` exists locally, load the
     component's restricted knowledge (customer requirements, field
     feedback) without surfacing NDA content in the output

2. **Scope** -- with context loaded, surface what was learned and ask what
   to prototype. Accept: a description, a Jira key, a knowledge entry
   reference, a Figma link, or "the whole thing."

3. **Slug** -- derive a slug name, confirm with user.

4. **Architecture grounding** -- produce a brief (shown to user, not a
   file) summarizing:
   - The real data model (entities, relationships, states)
   - The real API surface or interaction patterns from upstream
   - Design constraints from strategy or architecture decisions
   - What is grounded vs. what is invented

   User confirms or corrects before any HTML is generated.

5. **Design decisions** -- if the prototype involves UI layout/interaction
   choices, surface 2-3 options as conversational text comparisons
   referencing the architecture grounding. User picks.

6. **Component planning** (mandatory) -- before writing any HTML, the
   skill must:
   - Identify every PatternFly component the prototype will use (table,
     card, toolbar, page, masthead, etc.)
   - Query the PatternFly MCP (`searchPatternFlyDocs` + `usePatternFlyDocs`)
     for each component's v6 design guidelines, examples, and accessibility
     docs. This is not optional or "if available."
   - Query the PatternFly MCP patterns docs (primary-detail, dashboard,
     card-view, filters) for the correct page-level composition pattern
   - Produce a component plan (shown to user, not a file) mapping each
     prototype element to a specific PatternFly component and pattern,
     with the CSS class names and HTML structure derived from the MCP docs
   - Reference the ai-helpers AI prompt guidance (served via the MCP) for
     anti-patterns: non-existent components, incorrect styling approaches,
     missing accessibility features

7. **Generate** -- self-contained HTML + PatternFly 6 CDN, grounded in
   the component plan from step 6:
   - HTML structure matches what the PatternFly React components render
     (the MCP examples show the component composition; the skill derives
     the equivalent DOM structure and `pf-v6-c-*` / `pf-v6-l-*` class
     names)
   - All colors, spacing, and typography use PatternFly CSS custom
     properties (`--pf-t--global--*`), never hardcoded values
   - Use realistic field names, status values, entity relationships from
     the architecture grounding -- not lorem ipsum
   - Follow PatternFly accessibility requirements: proper ARIA labels,
     keyboard navigation, semantic HTML, heading hierarchy
   - Write to `components/<id>/prototype/<slug>/v1/`

8. **Verify** -- open the generated prototype in Playwright
   (`browser_navigate` + `browser_take_screenshot`) and visually inspect
   against the PatternFly guidelines. Check:
   - Page structure renders correctly (masthead, sidebar, content areas)
   - Component layout matches the intended pattern
   - No broken styles or missing PatternFly classes
   - If issues are found, fix and re-verify before proceeding

9. **Metadata** -- generate `prototype.yaml`.

10. **Gate** -- inline confirm before committing.

11. **Reindex** -- `hub_index.py` to update views.

12. **Offer publish** -- ask if user wants to publish via `hub.publish`.

### Version flow

Same as create, but reads the existing `prototype.yaml` and prior version
HTML. Understands what changed, what feedback was received, and current
architecture state (may have evolved since v1). Increments version
directory, updates `current:` and `versions:`, reindexes.

### Key principle

The prototype should look like something that could actually exist in the
real product. Real entity names, real status values, real navigation
patterns borrowed from upstream projects. The context load step makes this
possible -- the skill knows the domain before it draws a single pixel.

## PatternFly accuracy strategy

### Why static HTML, not React

The PatternFly MCP's richest documentation is React-focused (component APIs,
JSX examples, import paths). React prototypes would map 1:1 to these docs.
However, React requires build tooling (`package.json`, `node_modules/`,
Vite/Webpack) per prototype, which changes the repo's identity from a
knowledge hub to a hybrid code repo. The prototypes serve stakeholder review
and design iteration -- not engineering handoff. Engineering builds the real
thing from scratch in their own codebase.

Static HTML + PatternFly 6 CDN keeps the repo clean: zero build step, zero
dependencies, publishes through the existing pipeline as-is.

### How accuracy is achieved without React

The PatternFly MCP serves content from the `patternfly/ai-helpers` repo
alongside the official PatternFly design guidelines, React examples, and
accessibility docs. The skill uses this as follows:

1. **Component selection** -- PatternFly MCP design guidelines (framework-
   agnostic) tell the skill WHICH component to use and WHEN. The patterns
   docs (primary-detail, dashboard, card-view, filters) guide page-level
   composition.

2. **HTML structure** -- the React examples show component composition;
   what React renders IS the DOM structure static HTML must replicate. The
   skill derives correct HTML element nesting from these examples.

3. **CSS classes** -- PatternFly 6 uses a predictable convention:
   `pf-v6-c-*` for components, `pf-v6-l-*` for layouts, `pf-v6-u-*` for
   utilities. The CDN stylesheet defines all of them. The skill emits the
   correct class names derived from the MCP docs and examples.

4. **Design tokens** -- all colors, spacing, and typography use PatternFly
   CSS custom properties (`--pf-t--global--*`), never hardcoded values.
   The MCP design guidelines document these.

5. **Anti-pattern avoidance** -- the ai-helpers AI prompt guidance and
   troubleshooting docs (served via the MCP) list common AI mistakes:
   using non-existent components, incorrect styling approaches, missing
   accessibility features. The skill references these before generating.

6. **Visual verification** -- after generating, Playwright opens the
   prototype and takes a screenshot for visual inspection against the
   PatternFly guidelines.

### What the PatternFly MCP provides (confirmed)

| content type | source | accuracy role |
|---|---|---|
| Design guidelines | patternfly-org | which component, when, how it looks (framework-agnostic) |
| React examples | patternfly-react | component composition → derive HTML structure |
| AI prompt guidance | patternfly/ai-helpers | how to prompt AI for PF accuracy, anti-patterns |
| Component rules | patternfly/ai-helpers | do's/don'ts, required structure, common issues |
| Layout patterns | patternfly-org | page structure, dashboard, primary-detail |
| Accessibility docs | patternfly-org | ARIA labels, keyboard nav, semantic HTML |
| JSON schemas | patternfly-react | component prop validation |
| Patterns | patternfly-org | card-view, filters, bulk-selection, status/severity |

## Migration

The existing `components/mcp-registry/enablement/registry-ui-prototype/`
moves to `components/mcp-registry/prototype/registry-ui/`:

- `index-v0.1-mockup.html` becomes `v1/index.html`
- `index.html` (v0.2) becomes `v2/index.html`
- `artifact.md` replaced by `prototype.yaml`
- `publish/manifest.yaml` source path updated
- Old enablement location removed

One commit, clean cut.

## Linter changes (hub_lint.py / hublib/schema.py)

- Accept `prototype/` as valid component subdirectory
- Validate every `prototype/*/` contains a `prototype.yaml`
- Validate required fields: title, description, status, current, versions,
  components
- Validate `status` is one of: active, superseded, archived
- Validate `current:` points to a directory that exists
- Validate every version directory contains an `index.html`

## Indexer changes (hub_index.py / hublib/indexer.py)

- Scan `components/*/prototype/*/prototype.yaml` and
  `narrative/prototype/*/prototype.yaml`
- Generate `views/prototypes.md`
- Generate `views/prototypes-portal.html`
- Per-component `index.md` gains a Prototypes section

## Documentation update scope

| file | change |
|---|---|
| `README.md` | Update "Layout in one breath" and skeleton list (5-dir to 6-dir) |
| `AGENTS.md` | Map table: add `prototype/`. Skills table: add `hub.prototype` |
| `conventions/layout.md` | New skeleton row, structure description, prototype.yaml schema |
| `docs/architecture.md` | Update skeleton table, top-level anatomy, mermaid diagram |
| `docs/working-here.md` | Add prototype filing example, mention `hub.prototype` in the loop |
| `docs/skills.md` | Document `hub.prototype` skill (create, version, publish, list) |
| `docs/publishing.md` | Add prototype publishing examples (individual + portal) |
| `docs/tooling.md` | Document indexer prototype scanning, portal generation, new lint rules |
| `docs/enhancements.md` | Track as an enhancement |
| `publish/manifest.yaml` | Update migrated registry-ui-prototype, add portal entry |

All generated files (`views/*`, `*/index.md`) are handled by the updated
`hub_index.py`, not manual edits.
