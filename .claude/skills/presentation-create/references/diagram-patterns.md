# Diagram Patterns Reference

All diagrams in presentations must be HTML-based. Three approaches are used, each suited to different visualization needs.

## Approach 1: Cytoscape.js — Architecture & Topology Diagrams

Best for: System architecture, component relationships, data flows, swim-lane diagrams.

### Setup

```html
<script src="https://cdn.jsdelivr.net/npm/cytoscape@3.30.4/dist/cytoscape.min.js"></script>
```

### Container Structure

```html
<div id="cy-container" style="position: relative; max-width: 1100px; margin: 2rem auto; border: 1px solid var(--border-subtle); border-radius: 12px; overflow: hidden;">
  <div id="cy" style="width: 100%; height: 800px;"></div>

  <!-- Layer labels (positioned on left edge) -->
  <div class="layer-labels" style="position: absolute; left: 0; top: 0; height: 100%; width: 40px;">
    <div class="layer-label" style="position: absolute; top: 10%; transform: rotate(-90deg); font-family: var(--font-mono); font-size: 0.6rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.15em;">LAYER NAME</div>
  </div>

  <!-- Legend -->
  <div class="arch-legend" style="display: flex; gap: 1.5rem; padding: 0.75rem 1rem; border-top: 1px solid var(--border-subtle); background: var(--bg-elevated); font-family: var(--font-mono); font-size: 0.65rem;">
    <div style="display: flex; align-items: center; gap: 0.4rem;">
      <span style="width: 12px; height: 12px; background: var(--rh-red); border-radius: 3px;"></span>
      Core Component
    </div>
    <div style="display: flex; align-items: center; gap: 0.4rem;">
      <span style="width: 12px; height: 3px; background: var(--rh-teal);"></span>
      Data Flow
    </div>
  </div>
</div>
```

### Cytoscape Configuration Pattern

```javascript
const cy = cytoscape({
  container: document.getElementById('cy'),
  elements: [
    // Nodes
    { data: { id: 'registry', label: 'MCP Registry', type: 'core' },
      position: { x: 400, y: 300 } },
    { data: { id: 'gateway', label: 'MCP Gateway', type: 'runtime' },
      position: { x: 700, y: 300 } },

    // Edges
    { data: { source: 'registry', target: 'gateway', label: 'publish', flowType: 'data' } }
  ],
  style: [
    // Node styles
    {
      selector: 'node',
      style: {
        'label': 'data(label)',
        'text-valign': 'center',
        'text-halign': 'center',
        'font-family': '"Red Hat Text", sans-serif',
        'font-size': '11px',
        'color': '#ffffff',
        'text-wrap': 'wrap',
        'text-max-width': '90px',
        'background-color': '#1a1a1a',
        'border-width': 2,
        'border-color': '#333333',
        'width': 100,
        'height': 50,
        'shape': 'roundrectangle'
      }
    },
    // Core component styling
    {
      selector: 'node[type="core"]',
      style: {
        'border-color': '#EE0000',
        'border-width': 2
      }
    },
    // Runtime component styling
    {
      selector: 'node[type="runtime"]',
      style: {
        'border-color': '#009596',
        'border-width': 2
      }
    },
    // Edge styles
    {
      selector: 'edge',
      style: {
        'width': 2,
        'line-color': '#444444',
        'target-arrow-color': '#444444',
        'target-arrow-shape': 'triangle',
        'curve-style': 'bezier',
        'label': 'data(label)',
        'font-size': '9px',
        'font-family': '"Red Hat Mono", monospace',
        'color': '#8a8a8a',
        'text-rotation': 'autorotate',
        'text-margin-y': -10
      }
    },
    // Data flow edge
    {
      selector: 'edge[flowType="data"]',
      style: {
        'line-color': '#009596',
        'target-arrow-color': '#009596'
      }
    }
  ],
  layout: { name: 'preset' },
  userZoomingEnabled: false,
  userPanningEnabled: false,
  boxSelectionEnabled: false
});
```

### Swim Bands (Row Backgrounds)

Add alternating row backgrounds using positioned div overlays:

```html
<div class="swim-bands" style="position: absolute; inset: 0; pointer-events: none;">
  <div style="position: absolute; top: 0; left: 0; right: 0; height: 25%; background: rgba(255,255,255,0.02);"></div>
  <div style="position: absolute; top: 25%; left: 0; right: 0; height: 25%; background: rgba(255,255,255,0.05);"></div>
  <div style="position: absolute; top: 50%; left: 0; right: 0; height: 25%; background: rgba(255,255,255,0.02);"></div>
  <div style="position: absolute; top: 75%; left: 0; right: 0; height: 25%; background: rgba(255,255,255,0.05);"></div>
</div>
```

## Approach 2: CSS Grid/Flex — Flows, Pipelines, Comparisons

Best for: Step-by-step flows, capability grids, comparison layouts, timelines.

### Pipeline / Step Flow

```html
<div class="flow-steps" style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; justify-content: center;">

  <div class="flow-step" style="background: var(--bg-elevated); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 1rem 1.25rem; text-align: center; min-width: 120px; flex: 0 1 auto;">
    <div style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--rh-red); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.3rem;">STEP 1</div>
    <div style="font-family: var(--font-sans); font-weight: 600; font-size: 0.85rem; color: var(--text-primary);">Discover</div>
    <div style="font-family: var(--font-text); font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">Find MCP servers</div>
  </div>

  <div class="flow-connector" style="color: var(--rh-red); font-size: 1.2rem; opacity: 0.6;">&#x2192;</div>

  <div class="flow-step" style="background: var(--bg-elevated); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 1rem 1.25rem; text-align: center; min-width: 120px; flex: 0 1 auto;">
    <div style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--rh-teal); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.3rem;">STEP 2</div>
    <div style="font-family: var(--font-sans); font-weight: 600; font-size: 0.85rem; color: var(--text-primary);">Validate</div>
    <div style="font-family: var(--font-text); font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">Security scan</div>
  </div>

  <!-- ... more steps -->
</div>
```

### Capability Grid (2x2 or 3-column)

```html
<div class="cap-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; max-width: 900px;">

  <div class="cap-card" style="background: var(--bg-elevated); border: 1px solid var(--border-subtle); border-left: 4px solid var(--rh-red); border-radius: 0 8px 8px 0; padding: 1.25rem;">
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
      <span style="font-family: var(--font-mono); font-size: 0.6rem; background: rgba(238,0,0,0.12); color: var(--rh-red); padding: 0.15rem 0.5rem; border-radius: 3px; text-transform: uppercase; letter-spacing: 0.1em;">SECURITY</span>
    </div>
    <div style="font-family: var(--font-sans); font-weight: 600; font-size: 0.95rem; color: var(--text-primary); margin-bottom: 0.4rem;">Authentication & RBAC</div>
    <ul style="list-style: none; padding: 0; margin: 0;">
      <li style="padding: 0.2rem 0 0.2rem 1rem; position: relative; font-size: 0.8rem; color: var(--text-secondary);">
        <span style="position: absolute; left: 0; top: 0.55rem; width: 5px; height: 5px; border-radius: 50%; background: var(--rh-red);"></span>
        mTLS between components
      </li>
    </ul>
  </div>

  <!-- ... more cards with different border-left colors -->
</div>
```

### Comparison Layout (Side-by-Side)

```html
<div class="two-col" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">

  <div style="background: linear-gradient(135deg, rgba(238,0,0,0.06), rgba(238,0,0,0.02)); border: 1px solid rgba(238,0,0,0.2); border-radius: 12px; padding: 1.5rem;">
    <div style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--rh-red); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.5rem;">WITHOUT</div>
    <p style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5;">Problem scenario...</p>
  </div>

  <div style="background: linear-gradient(135deg, rgba(62,134,53,0.06), rgba(62,134,53,0.02)); border: 1px solid rgba(62,134,53,0.2); border-radius: 12px; padding: 1.5rem;">
    <div style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--rh-green); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.5rem;">WITH</div>
    <p style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5;">Solution scenario...</p>
  </div>

</div>
```

### Timeline / Roadmap

```html
<div class="timeline-cols" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">

  <div style="border-top: 3px solid var(--rh-green); padding-top: 1rem;">
    <div style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--rh-green); text-transform: uppercase; letter-spacing: 0.15em;">PHASE 1 — NOW</div>
    <div style="font-family: var(--font-sans); font-weight: 600; font-size: 0.95rem; color: var(--text-primary); margin: 0.5rem 0;">Foundation</div>
    <ul style="list-style: none; padding: 0;">
      <li style="font-size: 0.8rem; color: var(--text-secondary); padding: 0.2rem 0;">Core registry</li>
    </ul>
  </div>

  <div style="border-top: 3px solid var(--rh-blue); padding-top: 1rem;">
    <div style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--rh-blue); text-transform: uppercase; letter-spacing: 0.15em;">PHASE 2 — NEXT</div>
    <!-- ... -->
  </div>

  <div style="border-top: 3px solid var(--rh-purple); padding-top: 1rem;">
    <div style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--rh-purple); text-transform: uppercase; letter-spacing: 0.15em;">PHASE 3 — FUTURE</div>
    <!-- ... -->
  </div>

</div>
```

## Approach 3: Inline SVG — Custom Flow Diagrams

Best for: Simple flows with animated connectors, custom shapes, or precise positioning.

### Animated Connector Pattern

```html
<svg viewBox="0 0 800 200" style="width: 100%; max-width: 800px;">
  <!-- Animated dashed line -->
  <line x1="100" y1="100" x2="700" y2="100"
        stroke="#EE0000" stroke-width="2" stroke-dasharray="8,6"
        style="animation: dash-flow 2s linear infinite;" />

  <!-- Arrow head -->
  <polygon points="700,90 720,100 700,110" fill="#EE0000" />

  <!-- Node boxes -->
  <rect x="50" y="70" width="100" height="60" rx="8"
        fill="#1a1a1a" stroke="#333" stroke-width="1.5" />
  <text x="100" y="105" text-anchor="middle" fill="#fff"
        font-family="Red Hat Text" font-size="12">Source</text>
</svg>

<style>
  @keyframes dash-flow {
    to { stroke-dashoffset: -28; }
  }
</style>
```

## Choosing the Right Approach

| Need | Approach |
|---|---|
| System architecture with many nodes and edges | Cytoscape.js |
| Swim-lane diagrams with layer groupings | Cytoscape.js |
| Step-by-step pipeline (3-7 steps) | CSS flex flow |
| Feature/capability comparison grid | CSS grid cards |
| Before/after or with/without comparison | CSS two-column |
| Phased roadmap or timeline | CSS grid columns |
| Simple flow with animated lines | Inline SVG |
| Component relationship with just a few nodes | Either CSS or SVG |

## Responsive Diagram Tips

- Cytoscape containers: set `max-width` and let height be responsive via aspect ratio
- CSS flows: use `flex-wrap: wrap` and hide arrow connectors on mobile (`@media max-width: 768px { .flow-connector { display: none; } }`)
- Grids: switch to single column at 768px
- SVG: use `viewBox` for fluid scaling
