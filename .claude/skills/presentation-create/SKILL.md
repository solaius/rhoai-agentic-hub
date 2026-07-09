---
name: presentation-create
description: Create or update polished HTML presentations following Red Hat branding standards, staged under a feature's enablement/ directory. Use this skill whenever the user wants to create a presentation, slide deck, overview page, pitch deck, scrolling narrative, executive summary page, or says things like "create a presentation about X", "I need a slide deck", "make an overview page", "build a presentation", "update the presentation", or "presentation for [audience]". Also use when the user has existing HTML presentations they want to refresh, extend, or adapt for a different audience. Covers both slide-deck format (keyboard-navigated, full-screen slides) and vertical-scrolling format (long-form narrative pages with fixed header navigation). Building the artifact does not publish it — hand off to hub.publish when it's ready to go live. Requires the superpowers plugin (for brainstorming) and benefits from Google Workspace MCP (for accessing GDrive source materials).
---

# presentation-create

Create polished, Red Hat-branded HTML presentations with HTML diagrams, smooth animations, and responsive layouts. Supports two formats: slide deck (keyboard-navigated, full-screen) and vertical scrolling (long-form narrative with fixed header nav).

## Workflow Routing

Not every request needs the full 5-phase workflow. Route based on the complexity of the ask:

### Full Workflow (Phases 1–5)

Use for: New presentations from scratch, major restructures, audience pivots, anything where the narrative arc matters. This is the default for new work.

### Quick Build

Use when:
- The user provides a specific, detailed brief ("make a 6-slide deck about X with these 4 points")
- Adding 1-3 slides/sections to an existing presentation
- Recreating content that already exists in another format (e.g., turning a doc into slides)
- The user says "just build it" or "I know exactly what I want"

Quick build process:
1. **Confirm scope** — Read any source material, confirm the feature and output path (`features/<feature>/enablement/<artifact-slug>/`), and summarize what you'll build in 2-3 sentences. Get a thumbs-up.
2. **Read the template and references** — Same as Phase 4 Step 1 (still need the design tokens and patterns).
3. **Build and write** — Go straight to building the HTML. Apply the branding checklist.
4. **Review** — Same as Phase 5.

What quick build skips: The formal brainstorming phase and the structured outline approval step. The narrative thinking still happens — it's just compressed into the build step because the user has already done the strategic thinking.

### Minor Update

Use for: Fixing typos, swapping a stat, updating a date, adding a link, changing a color. No process needed — just read the file, make the edit, done.

## Prerequisites

Before starting, confirm the user has these tools available:

1. **Superpowers plugin** — needed for the brainstorming phase. The brainstorming skill helps explore narrative arc, key messages, and structure before building. This produces significantly better presentations than jumping straight to slides.
2. **Google Workspace MCP** — needed if the user wants to pull in Google Docs, Sheets, or Drive files as source material. Not strictly required if all source material is local.

If either is missing, let the user know and explain why it matters. Don't block on Google Workspace if the user has all their source material locally.

## Presentation Patterns

Within the two formats (slide deck and scrolling), different requests call for different structural patterns. Use this guide during intake to match the user's need to the right layout, or to suggest one when they're unsure.

### Slide Deck Patterns

| Pattern | Best For | Typical Slides | Key Features |
|---|---|---|---|
| **Product Pitch Deck** | Client/Partner demos, sales enablement | 8-12 slides | Problem → solution → architecture → capabilities → roadmap → CTA. Heavy on scenario cards and diagrams. |
| **Executive Brief Deck** | Leadership updates, steering committee, board-level | 5-7 slides | Compact, minimal text. Stats-heavy hero, key decisions, 1-2 diagrams max. Every slide earns its spot. |
| **Technical Deep-Dive Deck** | Engineering reviews, architecture discussions | 10-15 slides | Diagram-first. Cytoscape architecture views, API surface details, sequence flows, implementation specifics. |
| **Competitive Positioning Deck** | Analyst briefings, partner comparisons | 7-10 slides | Comparison grids, side-by-side before/after, feature matrices. Uses green/amber/red scoring indicators. |

### Scrolling Page Patterns

| Pattern | Best For | Key Features |
|---|---|---|
| **Product Overview Page** | General audience, website-style landing | Hero + stats strip → problem scenarios → capabilities grid → architecture diagram → roadmap → CTA. Comprehensive but scannable. |
| **Strategy & Roadmap Page** | Marketing, partner strategy, initiative overviews | Timeline-driven. Phase chevrons, milestone markers, capability build-up over time. Less about current state, more about the journey. |
| **Solution Architecture Page** | Engineering/Partner integration docs | Diagram-heavy. Multiple Cytoscape views (system topology, data flows, deployment model). Diagrams are the content, not decoration. |
| **Ecosystem Overview Page** | Broad audience, multi-product narratives | Multiple component sections, each with its own mini-architecture. Uses the scrolling format's length to cover a wide surface area. |

### How to Choose

- **Slide deck** when the user will present live (meetings, demos, keynotes) or needs PDF export for async sharing
- **Scrolling page** when the content lives on a website, is consumed self-serve, or needs to cover more ground than 12 slides allows
- If the user says "overview" or "one-pager" — ask whether they'll present it (deck) or share it as a link (scrolling)
- If the user names a persona, suggest the pattern that matches: Client → Product Pitch, Engineering → Technical Deep-Dive, etc.

## Phase 1: Intake

Gather requirements through conversational questions. Skip any that the user already answered in their request.

### Required Information

| Question | Why It Matters |
|---|---|
| **Feature**: Which feature partition does this belong to (see `features/features.yaml`)? | Determines where the artifact is filed — `features/<feature>/enablement/` |
| **Purpose**: What is this presentation trying to achieve? | Shapes the narrative structure and CTA |
| **Topic & products**: What specific topic(s) and Red Hat products are involved? | Determines technical depth and which components to highlight |
| **Messaging**: What key message should the audience take away? | Drives the thesis slide and narrative arc |
| **Audience/persona**: Client, Partner, Engineering, Marketing, General? | Controls technical depth, jargon level, and framing |
| **Format**: Slide deck (keyboard navigation) or vertical scrolling? | Determines which template to use |
| **Artifact slug**: Short kebab-case name for this artifact (e.g. `mcp-gateway-pitch-deck`)? | Becomes the `enablement/<artifact-slug>/` directory name |
| **Knowledge sources**: Any docs, transcripts, repos, or Drive files beyond what's already in this feature's `knowledge/` or in `memory/`? | Ensures all relevant context is captured |

### Adaptive Behavior

- If the user gives a broad topic, help them narrow the thesis
- If the user names a persona, infer appropriate technical depth rather than asking again
- If the user provides source material (files, links, docs), read them during intake to reduce follow-up questions
- If updating an existing presentation, read the HTML first, then ask what needs changing
- If no existing feature fits, don't invent a partition — hand off to `hub.file` (it creates new feature partitions in `features/features.yaml`); resume once it exists

### Exit Condition

User confirms a qualifying summary:

```markdown
## Presentation Qualifying Summary

- **Title** (working): [title]
- **Feature**: [feature id from features/features.yaml]
- **Purpose**: [what this achieves]
- **Thesis**: [one-sentence takeaway]
- **Audience**: [persona — Client/Partner/Engineering/Marketing/General]
- **Technical depth**: [Low / Medium / High]
- **Format**: [Slide deck / Vertical scrolling]
- **Products**: [list]
- **Source material**: [list of sources reviewed]
- **Output path**: `features/[feature]/enablement/[artifact-slug]/index.html`
```

## Phase 2: Brainstorm

Invoke the `superpowers:brainstorming` skill to explore:

- **Narrative arc**: What story are we telling? What's the journey from problem to solution to outcome?
- **Key sections/slides**: What are the major beats?
- **Diagram opportunities**: Where would a visual tell the story better than text?
- **Messaging tensions**: What might the audience push back on? How do we address it?
- **Competitive framing**: If relevant, how do we position against alternatives?

The brainstorming output becomes the foundation for the presentation outline. Don't skip this phase.

## Phase 3: Outline

Based on the brainstorming output, create a structured outline.

### Slide Deck Outline Format

```
Slide 1: [Title] — TITLE SLIDE
  - Eyebrow label
  - Main heading
  - Tagline/subtitle
  - Key stats (if applicable)

Slide 2: [Title] — PROBLEM/CONTEXT
  - What problem does the audience face?
  - 2-3 scenario cards
  - Why does this matter now?

Slide 3: [Title] — SOLUTION OVERVIEW
  - Core value proposition
  - Component overview or architecture diagram
  ...

Slide N: [Title] — CTA / NEXT STEPS
  - Clear call to action
  - Resources/links
```

### Scrolling Format Outline

```
Section: Hero
  - Eyebrow label
  - Main heading
  - Tagline
  - Key stats strip

Section: Problem
  - Problem statement
  - Scenario cards (2-3)

Section: [Component/Feature 1]
  - Overview + diagram
  - Key capabilities

Section: Roadmap/Timeline
  - Phased approach

Section: CTA
  - Call to action
  - Resources
```

For each section, note:
- Whether it needs a **diagram** (and what type: architecture, flow, comparison, timeline)
- Whether it needs **cards** (capability cards, comparison cards, scenario cards)
- Whether it needs **data** (stats, metrics, timeline phases)

**Exit condition**: User approves the outline.

## Phase 4: Build

### Step 1: Read the Template and References

Read the appropriate template from the skill's assets:
- **Slide deck**: `assets/slide-deck-template.html`
- **Vertical scrolling**: `assets/scrolling-template.html`

Also read these references before building:
- `references/design-tokens.md` — CSS custom properties, animation library, typography
- `references/brand-standards.md` — Official color palette, fonts, brand links
- `references/diagram-patterns.md` — How to build HTML diagrams
- `references/slide-patterns.md` — Common component patterns (hero, cards, grids, timelines)

If the outline requires layouts or patterns not covered by the template, generate custom HTML using the design tokens from the references. The templates are starting points, not constraints.

### Step 2: Build Each Section

For each section/slide in the approved outline:

1. **Write the content** — Headlines, body text, card content, list items. Match the tone to the audience persona.
2. **Build diagrams in HTML** — Use patterns from `references/diagram-patterns.md`:
   - **Cytoscape.js** for architecture/topology diagrams (swim lanes, node relationships, data flows)
   - **CSS grid/flex** for pipeline steps, capability grids, comparison layouts, timelines
   - **SVG** for custom flow diagrams with animated connectors
3. **Apply animations** — Staggered fade-ups for cards and list items, scroll-triggered reveals for scrolling format, slide transitions for deck format.
4. **Apply Red Hat branding** — Fonts, colors, spacing per the design tokens.

### Step 3: Branding Checklist

Before finishing the build, verify:

- [ ] Red Hat fonts loaded (Display, Text, Mono from Google Fonts)
- [ ] Color palette uses only official Red Hat colors (see `references/brand-standards.md`)
- [ ] Dark theme with proper contrast (white/light text on dark backgrounds)
- [ ] Red accent used consistently for labels, eyebrows, highlighted states
- [ ] Cards have subtle borders, hover states, and consistent border-radius
- [ ] Typography hierarchy follows the design tokens (display-xl > display-lg > h2 > body-lead > body)
- [ ] Responsive layout works at 768px and 1024px breakpoints
- [ ] `@media (prefers-reduced-motion: reduce)` handles accessibility
- [ ] Print styles preserve dark theme for PDF export (see Print / PDF Export below)
- [ ] All diagrams are HTML-based (no external images for diagrams)
- [ ] Small decorative labels (badges, callouts) are at least `0.65rem` and readable against dark backgrounds

### Step 4: Write the Output

Write the HTML file to `features/<feature>/enablement/<artifact-slug>/index.html` (the path fixed during Phase 1 intake). Keep the artifact self-contained — if it needs assets beyond CDN-hosted fonts/libraries (Cytoscape.js, Google Fonts), place them alongside it in the same `enablement/<artifact-slug>/` directory rather than reaching into other features.

After writing, offer to:
1. **Open in browser** — Suggest the user open it to preview.
2. **Publish it** — Writing the file does not make it public. When the user is ready to ship it, hand off to `hub.publish`, which drafts the `publish/manifest.yaml` entry (source, dest slug, audience, title, description) and gates on an explicit disclosure confirm before anything goes live.
3. **Capture durable side-knowledge** — If building this surfaced a decision, scope call, or positioning choice worth keeping beyond this artifact (something a colleague would want to find later), offer `hub.capture` for that one item.

## Phase 5: Review & Iterate

After the user reviews the presentation:

1. Ask what works and what needs changing
2. For updates: ask whether they want in-place edits or a versioned copy (v2, v3, etc.) — if they haven't already specified
3. For diagram adjustments: re-read `references/diagram-patterns.md` for available patterns
4. Iterate until the user is satisfied

## Updating Existing Presentations

When the user wants to update an existing presentation rather than create one from scratch:

1. Read the existing HTML file (under `features/<feature>/enablement/<artifact-slug>/`)
2. Identify the current format (slide deck vs scrolling) and design tokens in use
3. Ask what needs changing (content, layout, audience shift, new sections, diagram updates)
4. Ask whether to edit in-place or create a versioned copy (if not already specified)
5. Make the changes, preserving the existing design tokens and animation patterns
6. Check `publish/manifest.yaml` for an entry whose `source` matches this artifact's path — if the title or description changed and an entry exists, flag that the manifest entry is now stale and hand off to `hub.publish` to update it (never change the `dest` slug once published)
7. If the update surfaced a durable decision or fact worth keeping beyond this artifact, offer `hub.capture`

Skip the brainstorming phase for minor updates (content tweaks, adding a slide, fixing data). Use brainstorming for significant changes (different audience, major restructure, new narrative arc).

## Key Principles

**Narrative first, not slides first.** The brainstorming and outline phases exist because good presentations tell a story. Every section should advance the narrative, not just display information. Ask "why does this slide exist?" — if the answer is just "to show data," it needs a narrative frame.

**Diagrams over bullet lists.** Where a concept can be shown visually, build an HTML diagram. Architecture views, data flows, pipeline steps, timelines, and comparisons all work better as diagrams. See `references/diagram-patterns.md` for the pattern library. All diagrams must be HTML-based (Cytoscape.js, CSS, or SVG) — no external image files for diagrams.

**Consistent design language.** All presentations in this repo share the same CSS custom properties, animation library, and component patterns. New presentations should feel like they belong in the same family. The design tokens in `references/design-tokens.md` are the source of truth.

**Print / PDF export must preserve the dark theme.** Users frequently print slide decks to PDF via the browser's Print dialog (landscape, no margins, "background graphics" checked). The `@media print` styles must:
- Apply `print-color-adjust: exact` on `*` (with `-webkit-` prefix) to force browsers to render background colors
- Keep `background: var(--bg-canvas)` on the deck and slides — never override to `#fff`
- Preserve all text colors as-is — never flip to dark-on-light
- Hide only UI chrome (controls, overview grid, notes panel), not content

The slide deck template already includes correct print styles. If you add custom components with background colors, they will inherit the `print-color-adjust: exact` rule automatically.

**Readability over decoration.** Small decorative labels (positioned badges, floating callouts, mono-text tags on cards) often look fine on a large monitor but become unreadable at typical slide-deck viewing distances or in PDF exports. Before adding a small positioned label, ask whether the information it conveys is important enough to warrant its own element. If it is, make it at least `0.65rem` with enough padding and contrast to be legible. If it's supplementary context, consider putting it in the body text or presenter notes instead of a floating badge.

**Audience-appropriate depth.** The persona drives everything:
- **Client**: Business language, outcome framing, ROI, competitive positioning
- **Partner**: Integration value, joint go-to-market, technical interoperability
- **Engineering**: Architecture details, API surfaces, implementation specifics
- **Marketing**: Messaging hooks, positioning, market context, competitive differentiation
- **General**: Accessible language, broad value proposition, minimal jargon

## Reference Files

| File | When to Read |
|---|---|
| `references/design-tokens.md` | Before building — CSS custom properties, animation library, typography scale, spacing |
| `references/brand-standards.md` | Before building — Official Red Hat color palette, font families, brand resource links |
| `references/diagram-patterns.md` | When building diagrams — Cytoscape.js setup, CSS diagram patterns, SVG flows |
| `references/slide-patterns.md` | When building slides/sections — Hero, problem cards, capability grids, timelines, CTAs |

## Examples

The old repo's root `index.html` landing-page example doesn't carry over — in the hub, the public landing page is generated by CI from `publish/manifest.yaml` titles/descriptions (see `/conventions/publishing.md`), not hand-authored. The `.card` markup pattern itself is preserved in `references/slide-patterns.md` (now "Card-Grid Pattern") if you need a card grid inside an artifact.

None of the presentation examples below have been migrated into the hub yet (that's `hub.migrate`'s job), so they're linked at their live GitHub Pages URLs in the old `ai-asset-registry` repo. They demonstrate the style, flow, and quality bar this skill should match:

- [mcp-gateway-presentation.html](https://solaius.github.io/rhoai-agentic-hub-pages/mcp-gateway/presentation/) — **Slide deck format**, 10 slides, client-facing
- [mcp-registry-catalog-deck.html](https://solaius.github.io/rhoai-agentic-hub-pages/mcp-registry/catalog-deck/) — **Slide deck format**, 9 slides, client-facing
- [mcp-ecosystem.html](https://solaius.github.io/rhoai-agentic-hub-pages/mcp-ecosystem/deck/) — **Scrolling format**, full MCP ecosystem overview
- [mcp-registry-overview.html](https://solaius.github.io/rhoai-agentic-hub-pages/mcp-registry/overview/) — **Scrolling format**, MVP scope overview
- [mcp-ingestion-pipeline.html](https://solaius.github.io/rhoai-agentic-hub-pages/mcp-ecosystem/ingestion-pipeline/) — **Scrolling format** with Cytoscape.js pipeline diagram

Each targets a different persona with different goals, but they share the same design language. New presentations should match this quality bar. Once an example is migrated into a feature's `enablement/`, update its entry here to the hub path.
