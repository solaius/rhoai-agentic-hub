# Implementation Plan: hub.prototype Template System

**Spec:** /docs/superpowers/specs/2026-08-03-prototype-template-system-design.md
**Date:** 2026-08-03

## Implementation Order

### Phase 1: Extract shell from verified prototype (parallel tasks)

The skills-catalog prototype (`components/skills-catalog/prototype/skills-catalog-ui/v1/index.html`) is our verified-correct reference. Extract the shared pieces from it first, then build the extraction script to refresh from UXD later.

**Task 1A: Create shell.html + shell.css + assets**
- Extract the page shell (PM Hub banner, RHOAI masthead, app-body container) from the skills-catalog prototype
- Extract all CSS into shell.css
- Copy RHOAI.svg to conventions/prototype-shell/assets/
- Replace content-specific parts with {{CONTENT}}, {{NAV}}, {{SCRIPTS}}, {{COMPONENT_NAME}}, {{VERSION}} placeholders

**Task 1B: Create nav/nav.html + nav/nav.js**
- Extract the full sidebar nav HTML (60 items, all expandable sections)
- Extract toggleNavSection, navigateTo, expandNav, initNavDisplay functions into nav.js
- The nav.html should work standalone when injected into shell.html

**Task 1C: Create pattern files**
- catalog.html: extract from the skills-catalog catalog view, replace data with placeholders
- detail.html: extract from the detail view, replace with placeholders
- admin-table.html: extract from the admin view, replace with placeholders
- modal.html: extract the register modal, replace with placeholders
- empty.html: minimal content wrapper

### Phase 2: Build script

**Task 2: Create build_prototype.py**
- Reads shell.html, injects nav.html into {{NAV}}
- Reads chosen pattern, injects content fragments into placeholders
- Inlines shell.css into <style> block
- Inlines nav.js + content scripts.js into <script> block
- Replaces {{COMPONENT_NAME}} and {{VERSION}}
- Outputs self-contained index.html
- CLI: --pattern, --content, --output, --component, --version

### Phase 3: Extraction script

**Task 3: Create extract_uxd_styles.py**
- Fetches app.css, AppLayout.tsx, routes.tsx from GitLab API
- Fetches MCP page components for pattern references
- Generates/refreshes shell.html, shell.css, nav/nav.html, nav/nav.js, patterns/
- Writes extraction-metadata.yaml
- Optional Playwright verification pass

### Phase 4: Skill update

**Task 4: Update SKILL.md**
- Add Step 0.5 (shell freshness check)
- Update Step 6 (pattern selection instead of full HTML planning)
- Rewrite Step 7 (write content fragments + run build script)
- Reference the spec and new file paths

### Phase 5: Verify

**Task 5: Rebuild skills-catalog prototype using the new system**
- Use build_prototype.py with the catalog pattern and skills-catalog content
- Compare output against the existing verified prototype
- Confirm visual match via Playwright
