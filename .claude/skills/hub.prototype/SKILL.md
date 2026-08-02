---
name: hub.prototype
description: Create, version, publish, or list prototypes for a component or across components. Produces self-contained HTML + PatternFly 6 CDN prototypes grounded in the component's real architecture, knowledge, and upstream repos. Use when the user says "prototype", "mockup", "UI prototype", "create a prototype for <component>", "new version of the prototype", "list prototypes", or "prototype the <feature>".
---

# hub.prototype

Input: a subcommand (`create`, `version`, `publish`, `list`) plus a
component id and/or slug. Default subcommand: `create`.

Spec: /docs/specs/2026-08-02-prototype-system-design.md.
Structure: /conventions/layout.md (prototype/ skeleton leg, prototype.yaml
schema).

## Subcommand dispatch

Parse the invocation to determine the mode:

| invocation pattern | mode |
|---|---|
| `hub.prototype create <component>` | CREATE a new prototype |
| `hub.prototype <component>` (no subcommand) | CREATE (default) |
| `hub.prototype version <component>/<slug>` | VERSION an existing prototype |
| `hub.prototype publish <component>/<slug>` | PUBLISH via hub.publish |
| `hub.prototype list` | LIST all prototypes |
| `hub.prototype list <component>` | LIST prototypes for one component |

Cross-component prototypes: use `narrative` as the component id. The
prototype lands in `narrative/prototype/<slug>/`.

---

## LIST mode

1. Read `views/prototypes.md` and display its contents.
2. If a component id was given, filter to that component's section.
3. Done.

---

## PUBLISH mode

Hand off to `hub.publish` with:
- source: `components/<id>/prototype/<slug>/` (the slug directory, not a
  version — publishes the whole prototype including all versions)
- If the user wants a single version published instead:
  source: `components/<id>/prototype/<slug>/<version>/`
- audience: `internal` (default for prototypes; user can override)
- title and description from `prototype.yaml`

Nothing else to do — hub.publish handles the gate, manifest, CI, and
verification.

---

## VERSION mode

Input: `<component>/<slug>` identifying an existing prototype.

1. LOCATE: read `components/<id>/prototype/<slug>/prototype.yaml`. If it
   does not exist, error and suggest `create` instead.
2. CONTEXT LOAD: same as CREATE step 1, plus:
   - Read the CURRENT version's `index.html` to understand what exists
   - Read ALL prior version summaries from prototype.yaml
   - If the user provided feedback or change requests, incorporate them
3. SCOPE: ask what changed — new feedback, architecture evolution, feature
   additions, design refinements, or a full rethink. Accept a description,
   a Jira key, or "iterate on the feedback."
4. ARCHITECTURE DELTA: produce a brief (shown to user) of what changed
   since the current version — new knowledge entries, strategy updates,
   Jira movements, upstream changes. User confirms.
5. COMPONENT PLANNING: same as CREATE step 6 — mandatory PatternFly MCP
   queries for any NEW components being introduced in this version. Reused
   components from the prior version can skip re-querying unless the user
   reports rendering issues.
6. GENERATE: write to the NEXT version directory
   (`components/<id>/prototype/<slug>/v<N+1>/`). Derive N from the highest
   existing version directory number.
7. VERIFY: same as CREATE step 8 — Playwright screenshot + visual check.
8. UPDATE METADATA: update `prototype.yaml`:
   - `current: v<N+1>`
   - Add new entry under `versions:`
   - Preserve all existing version entries
9. GATE: inline confirm before committing (same pattern as CREATE step 10).
10. REINDEX + LINT: `python scripts/hub_lint.py` then `python scripts/hub_index.py`.
11. COMMIT: stage prototype files + regenerated indexes/views explicitly,
    NEVER `git add -A`; check `git diff --cached --stat`, then commit with
    pathspecs:
    `git commit -m "proto(<id>): <slug> v<N+1>" -- <those paths>`
12. Offer `hub.publish` if a manifest entry already exists for this
    prototype (it may need updating to point at the new version).

---

## CREATE mode (12 steps)

### Step 1: Context load

Before asking a single design question, deep-read the component's
ecosystem. Resolve the component id against `components/components.yaml`.
If `narrative` was given, the home is `narrative/`. If the id is not found,
offer `hub.intake` and stop.

Load, in order (skip what does not exist — a missing input shrinks the
prototype's grounding, never sinks the run):

a. **Knowledge entries** — read `components/<id>/knowledge/index.md`, then
   skim every `decision-`, `ref-`, `fact-` entry in the partition.
   Architecture decisions and ref- entries pointing to design docs,
   upstream repos, and API specs are highest priority.

b. **Research series** — read `components/<id>/research/
   00-executive-summary.md`, then landscape, architecture, and requirements
   lens docs if they exist.

c. **Strategy doc** — read `components/<id>/strategy/strategy.md` for the
   living WHAT/WHY, gaps, and roadmap alignment.

d. **Related components** — follow `related:` links in
   `components/components.yaml` and load each sibling's
   `knowledge/index.md`, `research/00-executive-summary.md`, and
   `strategy/strategy.md` (e.g., prototyping the MCP Catalog should
   understand the Registry's data model and the Lifecycle Operator's
   deployment flow).

e. **Jira scope** — read `work/jira-snapshot.yaml` for current feature
   state. If the component has a `jira:` block in components.yaml, note
   the active JQL scope.

f. **Upstream repos** — any `ref-` entries pointing to GitHub/GitLab repos:
   browse for real UI patterns, data models, API shapes. Use
   `gh api repos/<owner>/<repo>/contents/<path>` or web fetch for key
   files (e.g., types, schemas, route definitions).

g. **Existing prototypes** — read `prototype.yaml` files in this and
   related components' `prototype/` directories for continuity.

h. **Restricted context** — if `restricted/` exists locally, load the
   component's restricted knowledge (customer requirements, field
   feedback). NDA content informs design decisions but NEVER surfaces in
   the output (this repo is PUBLIC).

### Step 2: Scope

With context loaded, surface what was learned in a brief summary (2-5
sentences of the most design-relevant findings). Then ask what to
prototype. Accept:

- A description ("the server list and detail views")
- A Jira key ("RHAISTRAT-1780")
- A knowledge entry reference ("the primary-detail pattern from the
  architecture research")
- A Figma link or screenshot
- "The whole thing" (prototype the main UI surface)

### Step 3: Slug

Derive a kebab-case slug name from the scope (e.g., `registry-ui`,
`catalog-card-view`, `gateway-policy-editor`). Confirm with user. The
slug becomes the directory name: `components/<id>/prototype/<slug>/`.

### Step 4: Architecture grounding

Produce a brief (shown to user, NOT written to a file) summarizing:

- **Data model**: real entities, relationships, states drawn from the
  context load (e.g., "MCP servers have name, version, lifecycle status
  [draft, active, deprecated], certification level, and tool manifests")
- **API surface / interaction patterns**: real endpoints, operations, or
  user flows from upstream repos and design docs
- **Design constraints**: decisions from strategy or architecture entries
  that constrain the prototype (e.g., "the registry uses a primary-detail
  layout per decision-xyz")
- **Grounded vs. invented**: explicitly call out which elements come from
  real sources and which are the agent's design proposals

User confirms or corrects BEFORE any HTML is generated. This is a
mandatory checkpoint.

### Step 5: Design decisions

If the prototype involves layout or interaction choices, surface 2-3
options as conversational text comparisons referencing the architecture
grounding. Examples:

- "Table list vs. card grid for the server list — the upstream repo uses
  a table, but the card view would better showcase metadata badges"
- "Side panel detail vs. full-page detail — the primary-detail pattern
  from research suggests side panel for quick scanning"

User picks. If the scope is narrow or the architecture already prescribes
the approach, skip this step (say why).

### Step 6: Component planning (MANDATORY)

This step is NOT optional. Before writing any HTML, the skill MUST:

a. **Identify every PatternFly component** the prototype will use. List
   them explicitly (e.g., Page, Masthead, Sidebar, Table, Toolbar,
   Card, Badge, Label, Button, EmptyState, etc.).

b. **Query the PatternFly MCP** for each component. Use `version: "v6"`
   on every call:

   ```
   searchPatternFlyDocs(searchQuery: "<component name>", version: "v6")
   ```

   Then fetch the design guidelines and examples for each:

   ```
   usePatternFlyDocs(name: "<component name>", version: "v6")
   ```

   For complex components (Table, Toolbar, Page), also fetch:
   - The React examples (derive HTML structure from component composition)
   - Accessibility guidelines (ARIA labels, keyboard navigation)

c. **Query page-level patterns** from the PatternFly MCP for the
   prototype's composition pattern:

   ```
   searchPatternFlyDocs(searchQuery: "primary-detail", version: "v6")
   searchPatternFlyDocs(searchQuery: "dashboard", version: "v6")
   searchPatternFlyDocs(searchQuery: "card view", version: "v6")
   ```

   Fetch the relevant pattern docs.

d. **Query AI prompt guidance** from the PatternFly MCP:

   ```
   searchPatternFlyDocs(searchQuery: "AI", version: "v6")
   ```

   Fetch the ai-helpers docs for anti-patterns and common AI mistakes.

e. **Produce a component plan** (shown to user, NOT a file) mapping each
   prototype section/element to:
   - The specific PatternFly component and its CSS class
   - The HTML structure derived from the React examples
   - Any PatternFly design token references for custom styling

   Example format:
   ```
   Component Plan:
   - Page shell: pf-v6-c-page (with pf-v6-c-masthead, pf-v6-c-page__sidebar)
   - Server list: pf-v6-c-table with pf-v6-c-toolbar (bulk select, filter, pagination)
   - Status badges: pf-v6-c-label (green=active, blue=draft, red=deprecated)
   - Detail panel: pf-v6-c-drawer (primary-detail pattern)
   - Empty state: pf-v6-c-empty-state (when no servers match filter)
   ```

f. User confirms the component plan before generation proceeds.

### Step 7: Generate

Write self-contained HTML to `components/<id>/prototype/<slug>/v1/index.html`.

Requirements:

a. **PatternFly 6 CDN**: load from unpkg or CDN:
   ```html
   <link rel="stylesheet" href="https://unpkg.com/@patternfly/patternfly@6/patternfly.min.css">
   ```

b. **HTML structure**: match what the PatternFly React components render.
   The MCP examples show component composition; derive the equivalent DOM
   structure and class names. Use `pf-v6-c-*` for components,
   `pf-v6-l-*` for layouts, `pf-v6-u-*` for utilities.

c. **Design tokens**: all colors, spacing, and typography use PatternFly
   CSS custom properties (`--pf-t--global--*`), never hardcoded values.
   Example: `color: var(--pf-t--global--color--brand--default)` not
   `color: #06c`.

d. **Realistic data**: use real field names, status values, entity
   relationships from the architecture grounding. No lorem ipsum. If the
   prototype shows a list of MCP servers, use names like
   "postgres-mcp-server", "slack-mcp-server" with realistic version
   numbers, lifecycle states, and tool counts.

e. **Accessibility**: proper ARIA labels, keyboard navigation, semantic
   HTML, heading hierarchy, per the PatternFly accessibility docs from
   step 6.

f. **Interactivity**: prototype interactions with vanilla JavaScript (no
   frameworks). Tab switching, drawer open/close, filter toggling,
   toolbar actions. Keep it lightweight — this demonstrates the UX, not
   production logic.

g. **Self-contained**: everything in one HTML file (inline CSS for custom
   styles, inline JS for interactions). External dependencies only for
   the PatternFly CDN stylesheet and any CDN-hosted icon fonts.

h. **Create the directory structure**: `components/<id>/prototype/<slug>/v1/`
   with `index.html`. Create an `assets/` subdirectory only if needed
   (images, icons not available via CDN).

### Step 8: Verify

Open the generated prototype in Playwright and visually inspect:

```
browser_navigate(url: "file:///path/to/v1/index.html")
browser_take_screenshot(type: "png", scale: "css")
```

Check:
- Page structure renders correctly (masthead, sidebar, content areas)
- Component layout matches the intended pattern
- No broken styles, missing PatternFly classes, or unstyled elements
- Text is readable, spacing is correct
- Interactive elements look clickable/focusable

If issues are found, fix the HTML and re-verify. Iterate until the
rendering matches the component plan from step 6. Report the findings to
the user ("the prototype renders correctly" or "fixed X issue, re-verified
successfully").

### Step 9: Metadata

Generate `components/<id>/prototype/<slug>/prototype.yaml`:

```yaml
title: <descriptive title>
description: <one-line description of what the prototype shows>
status: active
current: v1
versions:
  v1:
    timestamp: <today YYYY-MM-DD>
    summary: <one-line summary of this version>
components: [<component-id>]
```

If the prototype spans multiple components (e.g., shows the Registry and
Catalog together), list all component ids in `components:`.

### Step 10: Gate

Show an inline summary and wait for explicit OK before committing:

```
prototype → components/<id>/prototype/<slug>/
  v1/index.html: <description>
  prototype.yaml: metadata (status: active, current: v1)
  [screenshot attached above]

Commit? [y/n]
```

Full content available on request. This follows the same gate pattern as
hub.capture — nothing touches git before approval.

On reject: discard everything, no writes. Ask what to change.

### Step 11: Reindex

On OK:
a. Run `python scripts/hub_index.py` to regenerate views (including
   `views/prototypes.md` and the component's `index.md`).
b. Run `python scripts/hub_lint.py` — 0 errors required. Fix the
   prototype files (prototype.yaml, directory structure) if lint reports
   errors, not the scripts.
c. Commit with explicit paths, NEVER `git add -A` (shared checkout, see
   memory/facts/fact-concurrent-session-git-hygiene.md):

   ```bash
   git add components/<id>/prototype/<slug>/ \
     components/<id>/index.md \
     components/index.md \
     views/prototypes.md \
     views/
   ```

   Check `git diff --cached --stat` for anything this prototype did not
   write, then commit WITH PATHSPECS:

   ```bash
   git commit -m "proto(<id>): <slug> v1" -- <those paths>
   ```

### Step 12: Offer publish

Ask if the user wants to publish the prototype:

- "Would you like to publish this prototype via hub.publish? (audience
  defaults to internal)"
- If yes, hand off to `hub.publish` with the prototype's source path
- If no, done. The prototype lives in the repo and can be published later.

Never auto-publish. Publishing is a separate disclosure decision.

---

## Key principles

1. **Grounded, not invented.** The context load (step 1) exists so the
   prototype reflects reality — real entity names, real status values, real
   navigation patterns from upstream projects. A prototype that invents its
   own data model is useless for stakeholder review.

2. **PatternFly accuracy is mandatory.** Step 6 is not optional. Every
   PatternFly component used in the prototype must be validated against the
   MCP's v6 docs before HTML generation. This prevents incorrect class
   names, non-existent components, and accessibility gaps.

3. **Static HTML, not React.** The hub is a knowledge repo, not a
   codebase. Prototypes serve stakeholder review and design iteration, not
   engineering handoff. No build step, no node_modules, no package.json.
   The publish pipeline stays clean.

4. **Self-contained.** One HTML file per version. External dependencies
   only for the PatternFly CDN. No cross-file imports, no shared
   stylesheets, no build artifacts.

5. **Versioned, not overwritten.** v1 and v2 coexist on disk for
   side-by-side comparison. Never modify a committed version's HTML —
   create a new version instead (unless fixing a rendering bug before the
   first commit).

6. **The gate is sacred.** Nothing touches git before the user approves.
   Show what will be written, wait for OK.
