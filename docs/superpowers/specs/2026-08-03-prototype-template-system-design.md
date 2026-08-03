# hub.prototype Template System Enhancement

**Date:** 2026-08-03
**Status:** Design approved, pending implementation
**Goal:** Generate RHOAI dashboard prototypes that are visually faithful
on first attempt by extracting reusable templates and CSS from the UXD
prototype repo, eliminating iterative rework.

## Problem

The current hub.prototype skill generates the entire HTML file from
scratch each time -- page shell, masthead, sidebar nav, CSS overrides,
and content. The RHOAI dashboard deviates significantly from stock
PatternFly 6 (custom backgrounds, border-radius, nav behavior, content
area rounded corners, card borders). Without the real RHOAI CSS,
prototypes come out visually wrong and require many rounds of correction.

The skills-catalog prototype session (2026-08-02/03) required 15+ rounds
of fixes to get the page shell, backgrounds, border-radius, nav
structure, card styling, modal patterns, filter sidebar, and detail page
layout correct. Every one of those fixes was about the shell and
styling, not the component-specific content.

## Solution

A multi-file template system with a build script. Shared shell, CSS, nav,
and page patterns are extracted from the UXD prototype repo
(gitlab.cee.redhat.com/uxd/prototypes/rhoai, branch 3.6) and maintained
as reusable artifacts. The skill generates only component-specific
content. A build script assembles the final self-contained `index.html`.

## File Structure

```
conventions/prototype-shell/
  shell.html              # Page shell with {{CONTENT}} placeholder
  shell.css               # All RHOAI-specific CSS overrides
  assets/
    RHOAI.svg             # Dashboard logo
  patterns/
    catalog.html          # Faceted filter + card grid + toggle group
    detail.html           # Two-column: sections left, sidebar right
    admin-table.html      # Table with toolbar + tabs
    modal.html            # Register/Deploy modal overlay
    empty.html            # Blank content area for custom layouts
  nav/
    nav.html              # Full sidebar nav (60 items, expandable)
    nav.js                # toggleNavSection + navigateTo + init
  extraction-metadata.yaml  # Branch, commit, timestamp of extraction
scripts/
  extract_uxd_styles.py   # Pulls CSS + structure from UXD repo
  build_prototype.py      # Assembles shell + pattern + content
```

## Extraction Script (`extract_uxd_styles.py`)

Creates the shared shell from the UXD source. Run once per UXD branch
release.

### Inputs

- UXD GitLab repo (project ID 155361)
- Branch name (default: `3.6`, configurable via `--branch`)
- Deployed site URL (for optional Playwright verification)

### Files Fetched via GitLab API

All fetched via `curl -sk` (self-signed cert, see
memory ref-gitlab-cee-access):

- `src/app/app.css` -- CSS overrides (the source of truth)
- `src/app/AppLayout/AppLayout.tsx` -- page shell structure
- `src/app/routes.tsx` -- nav item list and hierarchy
- `src/app/AIHub/MCPServers/MCPCatalog.tsx` -- catalog page reference
- `src/app/AIHub/MCPServers/MCPCatalogDetails.tsx` -- detail page reference
- `src/app/AIHub/MCPServers/DeployMCPServerModal.tsx` -- modal reference

### Generated Outputs

- `shell.html` -- static HTML page shell derived from AppLayout.tsx
  structure. Contains PM Hub banner (dark, `{{COMPONENT_NAME}}` and
  `{{VERSION}}` placeholders), RHOAI masthead (logo, hamburger, icons,
  avatar), app-body flex container with sidebar slot and content area
  (rounded corners, white bg). Placeholders: `{{NAV}}`, `{{CONTENT}}`,
  `{{SCRIPTS}}`.
- `shell.css` -- extracted from app.css plus any PF6 override rules
  identified from the source. Contains all RHOAI-specific deviations
  from stock PatternFly: page layout, color palette, card borders,
  border-radius values, nav link styling, modal styling, spacing.
- `nav/nav.html` -- full nav tree derived from routes.tsx. All 60+
  items with proper expandable structure, icons, badges.
- `nav/nav.js` -- toggle/expand/collapse logic, navigateTo function,
  DOMContentLoaded init for inline display management.
- `patterns/*.html` -- content fragments derived from the MCP page
  components, converted to static HTML with `{{PLACEHOLDER}}` tokens.
- `extraction-metadata.yaml` -- branch, commit SHA, timestamp, list of
  files extracted. Used for staleness checks.

### How Extraction Works

The script reads JSX to understand STRUCTURE, then writes equivalent
static HTML. No React parsing or transpilation. No npm install. No
dependency on the UXD repo being cloned locally. All access via the
GitLab REST API.

### Optional Verification Pass (requires Playwright)

Opens the deployed site, captures computed styles for key elements,
compares against the generated CSS, logs discrepancies.

### Rerun Cadence

When the UXD team releases a new branch or when prototypes look wrong.
Idempotent -- same branch produces same output.

## Build Script (`build_prototype.py`)

Assembles a self-contained `index.html` from shell + pattern + content.

### Usage

```bash
python scripts/build_prototype.py \
  --pattern catalog \
  --content components/<id>/prototype/<slug>/v1/content/ \
  --output components/<id>/prototype/<slug>/v1/index.html \
  --component "Skills Catalog" \
  --version v1
```

### Assembly Steps

1. Read `shell.html`, replace `{{NAV}}` with `nav/nav.html` content
2. Replace `{{COMPONENT_NAME}}` and `{{VERSION}}` in PM Hub banner
3. Read chosen pattern file (e.g., `patterns/catalog.html`)
4. Read content fragments from `--content` directory (skill-generated:
   `cards.html`, `filters.html`, `sidebar-fields.html`, `readme.html`,
   `scripts.js`, etc.)
5. Substitute all `{{PLACEHOLDER}}` tokens with matching fragments
6. Inline `shell.css` into a `<style>` block (self-contained output)
7. Inline `nav.js` + content-specific JS into a `<script>` block
8. Write assembled `index.html`

### Output

A single self-contained HTML file. Opens in any browser. No server
needed. Stakeholders see the full RHOAI dashboard experience.

## Page Patterns

Each pattern is a content fragment (no `<html>`, `<head>`, or shell
markup) defining a specific page layout with `{{PLACEHOLDER}}` tokens.

### `catalog.html`

Page title with icon, tabs, description, two-column flex (faceted filter
sidebar 220px + main content), search bar, toggle group, tier section
header, card gallery grid, empty state.

Placeholders: `{{PAGE_TITLE}}`, `{{PAGE_ICON}}`,
`{{PAGE_DESCRIPTION}}`, `{{TABS}}`, `{{FILTER_SECTIONS}}`,
`{{TOGGLE_BUTTONS}}`, `{{CARDS}}`, `{{CONTENT_SCRIPTS}}`

### `detail.html`

Breadcrumb, title with icon + badges + action button, two-column flex
(stacked section cards left + metadata sidebar right 290px). Each
section card has `border: 1px solid #e5e7eb`, `border-radius: 16px`.

Placeholders: `{{BREADCRUMB_PARENT}}`, `{{BREADCRUMB_CURRENT}}`,
`{{TITLE}}`, `{{TITLE_ICON}}`, `{{BADGES}}`, `{{ACTION_BUTTON}}`,
`{{SECTIONS}}`, `{{SIDEBAR_FIELDS}}`, `{{README}}`

### `admin-table.html`

Page title + description, tabs, toolbar with search + filters, table
with headers + body + kebab actions.

Placeholders: `{{ADMIN_TITLE}}`, `{{ADMIN_DESCRIPTION}}`, `{{TABS}}`,
`{{TABLE_HEADERS}}`, `{{TABLE_BODY}}`, `{{CONTENT_SCRIPTS}}`

### `modal.html`

Backdrop + centered modal (840px, `border-radius: 24px`, shadow).
Header with title + close, body with form fields, footer with buttons.

Placeholders: `{{MODAL_TITLE}}`, `{{MODAL_FIELDS}}`,
`{{MODAL_PRIMARY_ACTION}}`, `{{MODAL_SCRIPTS}}`

### `empty.html`

Blank content area. For prototypes that don't match any existing
pattern.

## Updated Skill Flow

### Steps 1-5 (unchanged)

Context load, scope, slug, architecture grounding, design decisions.
These determine WHAT to prototype.

### New Step 0.5: Shell Freshness Check

Before generating, verify `conventions/prototype-shell/` exists. If
missing, run `extract_uxd_styles.py` automatically. If present, check
`extraction-metadata.yaml` timestamp -- warn if older than 30 days.

### Step 6: Component Planning (updated)

- Still identifies PatternFly components and queries the MCP
- NEW: selects a page pattern (catalog, detail, admin-table, empty)
- NEW: loads `fact-uxd-prototype-design-standards` and
  `ref-uxd-rhoai-prototype-repo` for RHOAI-specific patterns
- NEW: if the pattern needs a component not in the library, checks the
  UXD repo source via GitLab API
- Component plan maps to PATTERN PLACEHOLDERS, not raw HTML

### Step 7: Generate (rewritten)

- Writes content fragments to a `content/` directory:
  - `cards.html`, `filters.html`, `sidebar-fields.html`, `readme.html`,
    `scripts.js`, etc. (whatever the chosen pattern needs)
- Runs `build_prototype.py` to assemble final `index.html`
- The skill NEVER writes page shell, nav, masthead, or CSS

### Step 8: Verify (unchanged)

Playwright screenshot + visual check. Failures should be content-only
(wrong data, missing section), never shell/styling issues.

### Steps 9-12 (unchanged)

Metadata, gate, reindex, offer publish.

## What This Eliminates

Every issue from the skills-catalog session that was about the shell:

| Issue | Cause | Fix |
|---|---|---|
| RHOAI masthead not spanning full width | Generated PF6 grid instead of flex layout | Extracted from AppLayout.tsx |
| Wrong background colors (white sidebar, grey content) | Guessed instead of reading app.css | Extracted from app.css |
| Missing rounded corner at content/masthead junction | Didn't know about border-radius: 16px | Extracted from computed styles |
| Blue left border on active nav items | PF6 default, RHOAI removes it | Extracted CSS override |
| Nav expand/collapse broken for nested items | PF6 CSS specificity conflicts | Tested nav.js with !important + inline styles |
| Wrong card border color | Guessed #d2d2d2 instead of #e5e7eb | Extracted from UXD cards |
| Modal border-radius wrong | Guessed instead of extracting | Extracted from DeployMCPServerModal |
| Search bar pill shape | Guessed border-radius: 24px vs actual 6px | Extracted from UXD search |
| Missing filter sidebar right border | Didn't know about the separator | Extracted from catalog layout |

## Dependencies

- GitLab API access (curl -sk, no auth needed for public repo)
- Python 3.11+ (already required for hub scripts)
- Playwright plugin (optional, for verification pass)
- PatternFly MCP (still used for component-level docs)

## Future Work

- Add patterns as new page types emerge (dashboard, wizard, settings)
- Auto-detect UXD branch updates and suggest re-extraction
- Support dark mode toggle in shell
- Pattern library grows with each prototype built
