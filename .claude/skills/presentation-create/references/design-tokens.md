# Design Tokens Reference

CSS custom properties, animation library, typography scale, and spacing system used across all presentations in this repo. These tokens are the source of truth — use them in every presentation to maintain visual consistency.

## CSS Custom Properties

```css
:root {
  /* === BACKGROUNDS === */
  --bg-canvas:      #151515;
  --bg-elevated:    #1a1a1a;
  --bg-card:        #202020;

  /* === TEXT === */
  --text-primary:   #ffffff;
  --text-secondary: #d2d2d2;
  --text-muted:     #8a8a8a;

  /* === RED HAT BRAND COLORS === */
  --rh-red:         #EE0000;
  --rh-red-dark:    #A30000;
  --rh-teal:        #009596;
  --rh-blue:        #0066CC;
  --rh-blue-light:  #4394e5;
  --rh-purple:      #6753AC;
  --rh-green:       #3E8635;
  --rh-orange:      #F4B400;

  /* === BORDERS === */
  --border-subtle:  #333333;
  --border-muted:   #444444;

  /* === TYPOGRAPHY === */
  --font-sans: "Red Hat Display", "Inter", -apple-system, "Segoe UI", system-ui, sans-serif;
  --font-text: "Red Hat Text", "Inter", -apple-system, "Segoe UI", system-ui, sans-serif;
  --font-mono: "Red Hat Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;

  /* === FONT SIZES === */
  --fs-display-xl: 2.8rem;   /* Hero titles */
  --fs-display-lg: 2rem;     /* Section titles */
  --fs-h2:         1.5rem;   /* Subsection headings */
  --fs-body-lead:  1.15rem;  /* Introductory paragraphs */
  --fs-body:       0.95rem;  /* Content text */
  --fs-label:      0.7rem;   /* Section labels, tags (uppercase, monospace) */
  --fs-small:      0.6rem;   /* Timestamps, secondary labels */

  /* === SPACING === */
  --space-xs:  0.5rem;
  --space-sm:  0.75rem;
  --space-md:  1rem;
  --space-lg:  1.5rem;
  --space-xl:  2rem;
  --space-2xl: 3rem;
  --content-max: 1100px;

  /* === ANIMATION === */
  --stagger-delay:    80ms;
  --transition-exit:  220ms;
  --transition-enter: 350ms;
  --ease-out-pop:     cubic-bezier(0.22, 1, 0.36, 1);
}
```

## Google Fonts Import

Include this in `<head>` for every presentation:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@400;500;600;700;800;900&family=Red+Hat+Mono:wght@400;500;600&family=Red+Hat+Text:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## Typography Classes

```css
.display-xl {
  font-size: var(--fs-display-xl);
  line-height: 1.05;
  letter-spacing: -0.03em;
  font-weight: 800;
  color: var(--text-primary);
}

.display-lg {
  font-size: var(--fs-display-lg);
  line-height: 1.1;
  letter-spacing: -0.02em;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 var(--space-md);
}

.lead {
  font-size: var(--fs-body-lead);
  line-height: 1.45;
  color: var(--text-secondary);
  margin: var(--space-sm) 0 0;
  max-width: 80ch;
  font-family: var(--font-text);
}

.body {
  font-size: var(--fs-body);
  line-height: 1.6;
  color: var(--text-secondary);
  margin: var(--space-md) 0 0;
  max-width: 70ch;
  font-family: var(--font-text);
}
```

## Eyebrow/Label Pattern

Used for section labels above headings. Always uppercase, monospace, red:

```css
.slide-eyebrow, .section-label {
  font-size: var(--fs-label);
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--rh-red);
  font-family: var(--font-mono);
  margin-bottom: var(--space-sm);
}
```

## Animation Library

### Keyframes

```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-right {
  from { opacity: 0; transform: translateX(-40px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes slide-left {
  from { opacity: 0; transform: translateX(40px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes scale-in {
  from { opacity: 0; transform: scale(0.92); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes pulseGlow {
  0%, 100% { box-shadow: 0 0 20px rgba(238,0,0,0.15); }
  50% { box-shadow: 0 0 40px rgba(238,0,0,0.3); }
}

@keyframes arrow-pulse {
  0%, 100% { opacity: 0.5; transform: translateY(0); }
  50% { opacity: 1; transform: translateY(4px); }
}
```

### Animation Trigger Classes (Slide Deck)

In slide deck format, animations fire when a slide becomes current:

```css
main.deck .slide.current .anim-fade-up     { animation: fade-up    400ms var(--ease-out-pop) both; animation-delay: calc(var(--index, 0) * var(--stagger-delay)); }
main.deck .slide.current .anim-fade-in     { animation: fade-in    400ms ease-out both;           animation-delay: calc(var(--index, 0) * var(--stagger-delay)); }
main.deck .slide.current .anim-slide-right { animation: slide-right 500ms var(--ease-out-pop) both; animation-delay: calc(var(--index, 0) * var(--stagger-delay)); }
main.deck .slide.current .anim-slide-left  { animation: slide-left  500ms var(--ease-out-pop) both; animation-delay: calc(var(--index, 0) * var(--stagger-delay)); }
main.deck .slide.current .anim-scale-in    { animation: scale-in   450ms var(--ease-out-pop) both; animation-delay: calc(var(--index, 0) * var(--stagger-delay)); }
```

### Animation Triggers (Scrolling Format)

In scrolling format, use IntersectionObserver to trigger animations on scroll:

```css
.animate-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}
.animate-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}
```

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));
```

### Stagger Pattern

To stagger children, use `data-stagger` on the parent and set `--index` via JS:

```html
<div class="card-grid" data-stagger>
  <div class="card anim-fade-up">...</div>
  <div class="card anim-fade-up">...</div>
  <div class="card anim-fade-up">...</div>
</div>
```

```javascript
function applyStaggerIndices(container) {
  Array.from(container.querySelectorAll('[data-stagger] > *')).forEach((el, i) => {
    el.style.setProperty('--index', String(i));
  });
}
```

## Hover Effects

Standard card hover:

```css
.card {
  transition: border-color 300ms ease, transform 200ms ease, box-shadow 300ms ease;
}
.card:hover {
  border-color: var(--rh-red);
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(238, 0, 0, 0.1);
}
```

## Glow Effects

```css
/* Subtle background glow (used behind hero sections) */
.glow::before {
  content: '';
  position: absolute;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(238,0,0,0.25) 0%, transparent 70%);
  pointer-events: none;
}

/* Pulsing glow on highlighted elements */
.pulse-glow {
  animation: pulseGlow 3s ease-in-out infinite;
}
```

## Accessibility

Always include reduced-motion support:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 180ms !important;
  }
  .anim-fade-up, .anim-slide-right, .anim-slide-left, .anim-scale-in {
    animation: fade-in 180ms ease-out both !important;
  }
}
```

## Responsive Breakpoints

```css
@media (max-width: 768px) {
  :root {
    --fs-display-xl: 1.8rem;
    --fs-display-lg: 1.4rem;
    --fs-body-lead:  1rem;
  }
  /* Stack grids to single column */
  /* Reduce padding */
  /* Hide complex navigation elements */
}

@media (max-width: 1024px) {
  /* Adjust multi-column layouts to 2 columns */
  /* Vertical flow diagrams instead of horizontal */
}
```

## Section Divider

Subtle gradient line used between sections:

```css
.section-divider {
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(238,0,0,0.18), rgba(238,0,0,0.35), rgba(238,0,0,0.18), transparent);
  margin: var(--space-2xl) 0;
}
```
