# Slide & Section Patterns Reference

Common component patterns used across presentations. Each pattern includes the HTML structure. All patterns use the design tokens from `design-tokens.md`.

## Hero Section

The opening section sets the stage. Used as the first slide or the top section of a scrolling page.

```html
<div class="slide-inner" style="max-width: var(--content-max); margin: 0 auto; display: flex; flex-direction: column; justify-content: center; min-height: 80vh; position: relative;">

  <!-- Background glow -->
  <div style="position: absolute; top: -100px; right: -100px; width: 500px; height: 500px; border-radius: 50%; background: radial-gradient(circle, rgba(238,0,0,0.2) 0%, transparent 70%); pointer-events: none;"></div>

  <div class="anim-fade-up" style="--index: 0">
    <div style="font-family: var(--font-mono); font-size: var(--fs-label); font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: var(--rh-red); margin-bottom: var(--space-sm);">
      RED HAT OPENSHIFT AI
    </div>
  </div>

  <h1 class="display-xl anim-fade-up" style="--index: 1">
    <span style="color: var(--rh-red);">Presentation</span> Title
  </h1>

  <p class="lead anim-fade-up" style="--index: 2">
    One-sentence tagline that captures the value proposition.
  </p>

  <!-- Optional: Key stats strip -->
  <div class="anim-fade-up" style="--index: 3; display: flex; gap: 2.5rem; margin-top: 2rem;">
    <div>
      <div style="font-family: var(--font-sans); font-size: 2rem; font-weight: 800; color: var(--rh-red);">5</div>
      <div style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em;">Components</div>
    </div>
    <div>
      <div style="font-family: var(--font-sans); font-size: 2rem; font-weight: 800; color: var(--text-primary);">3.5</div>
      <div style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em;">Target Release</div>
    </div>
  </div>
</div>
```

## Problem / Scenario Cards

Present the problem through concrete scenarios the audience recognizes.

```html
<div style="display: flex; gap: 1rem; flex-wrap: wrap;">

  <div style="flex: 1; min-width: 250px; background: linear-gradient(135deg, rgba(238,0,0,0.06), rgba(238,0,0,0.02)); border: 1px solid rgba(238,0,0,0.2); border-radius: 12px; padding: 1.25rem; position: relative; overflow: hidden;">
    <!-- Top accent bar -->
    <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, var(--rh-red), #ff4444);"></div>

    <div style="font-family: var(--font-mono); font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.15em; color: var(--rh-red); margin-bottom: 0.5rem;">SCENARIO</div>
    <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
      A data scientist discovers a useful MCP server but has <strong style="color: var(--text-primary);">no way to verify</strong> it meets security requirements...
    </p>
  </div>

  <!-- More scenario cards... -->
</div>
```

## Feature / Capability Cards

Grid of capabilities with color-coded left borders.

```html
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">

  <div style="background: var(--bg-elevated); border: 1px solid var(--border-subtle); border-left: 4px solid var(--rh-red); border-radius: 0 8px 8px 0; padding: 1.25rem; transition: border-color 300ms, transform 200ms;">
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
      <span style="font-family: var(--font-mono); font-size: 0.6rem; background: rgba(238,0,0,0.12); color: var(--rh-red); padding: 0.15rem 0.5rem; border-radius: 3px; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;">GOVERNANCE</span>
    </div>
    <div style="font-family: var(--font-sans); font-weight: 600; font-size: 0.95rem; color: var(--text-primary); margin-bottom: 0.4rem;">Card Title</div>
    <ul style="list-style: none; padding: 0; margin: 0;">
      <li style="padding: 0.2rem 0 0.2rem 1rem; position: relative; font-size: 0.8rem; color: var(--text-secondary); font-family: var(--font-text);">
        <span style="position: absolute; left: 0; top: 0.55rem; width: 5px; height: 5px; border-radius: 50%; background: var(--rh-red);"></span>
        Feature item one
      </li>
      <li style="padding: 0.2rem 0 0.2rem 1rem; position: relative; font-size: 0.8rem; color: var(--text-secondary); font-family: var(--font-text);">
        <span style="position: absolute; left: 0; top: 0.55rem; width: 5px; height: 5px; border-radius: 50%; background: var(--rh-red);"></span>
        Feature item two
      </li>
    </ul>
  </div>

  <!-- More capability cards with different colors (--rh-teal, --rh-blue, --rh-green) -->
</div>
```

### Color-Coding Convention

| Category | Border Color | Tag Background |
|---|---|---|
| Security / Governance | `var(--rh-red)` | `rgba(238,0,0,0.12)` |
| Runtime / MCP | `var(--rh-teal)` | `rgba(0,149,150,0.12)` |
| Features / Capabilities | `var(--rh-blue)` | `rgba(0,102,204,0.12)` |
| Production / GA | `var(--rh-green)` | `rgba(62,134,53,0.12)` |
| Governance / Policy | `var(--rh-purple)` | `rgba(103,83,172,0.12)` |
| Warning / Manual | `var(--rh-orange)` | `rgba(244,180,0,0.12)` |

## Architecture Overview Card

A standalone card that frames a diagram or key component explanation.

```html
<div style="background: var(--bg-elevated); border: 1px solid var(--border-subtle); border-radius: 16px; padding: 2rem; max-width: var(--content-max); margin: 0 auto;">
  <div style="font-family: var(--font-mono); font-size: var(--fs-label); color: var(--rh-red); text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: var(--space-sm);">ARCHITECTURE</div>
  <h2 class="display-lg">How It Works</h2>
  <p class="lead" style="margin-bottom: 2rem;">Brief explanation of the architecture.</p>

  <!-- Diagram goes here (Cytoscape, CSS, or SVG) -->

</div>
```

## CTA / Next Steps Slide

The closing section with a clear call to action.

```html
<div style="max-width: var(--content-max); margin: 0 auto; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 60vh;">

  <div style="font-family: var(--font-mono); font-size: var(--fs-label); color: var(--rh-red); text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: var(--space-sm);">NEXT STEPS</div>

  <h2 class="display-lg" style="margin-bottom: var(--space-lg);">Ready to Get Started?</h2>

  <p class="lead" style="text-align: center; max-width: 60ch; margin-bottom: 2rem;">
    Summary of what comes next for the audience.
  </p>

  <div style="display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center;">
    <a href="#" style="display: inline-flex; align-items: center; gap: 0.5rem; background: var(--rh-red); color: white; padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; font-family: var(--font-sans); font-weight: 600; font-size: 0.9rem; transition: background 180ms;">
      Primary Action &#x2192;
    </a>
    <a href="#" style="display: inline-flex; align-items: center; gap: 0.5rem; background: transparent; color: var(--text-secondary); border: 1px solid var(--border-subtle); padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; font-family: var(--font-sans); font-weight: 600; font-size: 0.9rem; transition: border-color 180ms, color 180ms;">
      Secondary Action
    </a>
  </div>

  <!-- Resources -->
  <div style="display: flex; gap: 2rem; margin-top: 3rem; font-size: 0.85rem;">
    <a href="#" style="color: var(--rh-blue-light); text-decoration: none;">Documentation</a>
    <a href="#" style="color: var(--rh-blue-light); text-decoration: none;">GitHub Repository</a>
    <a href="#" style="color: var(--rh-blue-light); text-decoration: none;">Contact</a>
  </div>
</div>
```

## Badge / Tag Components

Inline tags for categorization:

```html
<!-- Standard tag -->
<span style="font-family: var(--font-mono); font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; padding: 0.15rem 0.5rem; border-radius: 3px; background: rgba(238,0,0,0.12); color: var(--rh-red);">TAG</span>

<!-- Status badge -->
<span style="font-family: var(--font-mono); font-size: 0.6rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; padding: 0.15rem 0.5rem; border-radius: 3px; background: rgba(62,134,53,0.15); color: var(--rh-green);">GA</span>

<!-- Product badge -->
<span style="font-family: var(--font-mono); font-size: 0.6rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; padding: 0.15rem 0.5rem; border-radius: 100px; background: rgba(0,102,204,0.12); color: var(--rh-blue-light); border: 1px solid rgba(0,102,204,0.2);">RHOAI</span>
```

## Key Metric / Stat Display

```html
<div style="display: flex; gap: 2rem; padding: 1.5rem; background: var(--bg-elevated); border-radius: 12px; border: 1px solid var(--border-subtle);">
  <div style="text-align: center;">
    <div style="font-family: var(--font-sans); font-size: 2.5rem; font-weight: 900; color: var(--rh-red); line-height: 1;">47%</div>
    <div style="font-family: var(--font-mono); font-size: 0.6rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.3rem;">Reduction</div>
  </div>
  <!-- More stats -->
</div>
```

## Quote / Callout

```html
<div style="border-left: 3px solid var(--rh-red); padding: 1rem 1.5rem; background: rgba(238,0,0,0.04); border-radius: 0 8px 8px 0; margin: 1.5rem 0;">
  <p style="font-family: var(--font-text); font-size: 1rem; color: var(--text-primary); font-style: italic; line-height: 1.6; margin: 0;">
    "Quote text goes here."
  </p>
  <p style="font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-muted); margin: 0.5rem 0 0; text-transform: uppercase; letter-spacing: 0.1em;">
    — Attribution
  </p>
</div>
```

## Scrolling Page: Fixed Header Navigation

```html
<nav style="position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: rgba(21,21,21,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid var(--border-subtle);">
  <div style="max-width: var(--content-max); margin: 0 auto; display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1.5rem;">
    <div style="display: flex; align-items: center; gap: 0.75rem;">
      <div style="display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; background: var(--rh-red); color: white; font-family: var(--font-sans); font-weight: 800; font-size: 0.65rem; border-radius: 4px;">RH</div>
      <span style="font-family: var(--font-sans); font-weight: 600; font-size: 0.9rem; color: var(--text-primary);">Product Name</span>
    </div>
    <div style="display: flex; gap: 1.5rem;">
      <a href="#section1" style="color: var(--text-muted); text-decoration: none; font-size: 0.8rem; font-family: var(--font-text); transition: color 0.2s;">Section 1</a>
      <a href="#section2" style="color: var(--text-muted); text-decoration: none; font-size: 0.8rem; font-family: var(--font-text); transition: color 0.2s;">Section 2</a>
    </div>
  </div>
</nav>
```

Each section should have `scroll-margin-top: 72px` to account for the fixed header.

## Card-Grid Pattern

The hub's public landing page is generated by CI from `publish/manifest.yaml`
(see `/conventions/publishing.md`) — you won't hand-edit an `index.html` to
list presentations. This markup is still useful any time an artifact itself
needs a card grid (e.g. a scrolling page's own landing section, or a
multi-page enablement site's internal index):

```html
<a class="card" href="path/to/page.html">
  <div class="card-label">LABEL TYPE</div>
  <h2>Page Title</h2>
  <p>Brief description of what this page covers.</p>
</a>
```

Labels used: `Presentation`, `Strategy`, `MVP`, `Client Overview`, `Technical Deep Dive`.
