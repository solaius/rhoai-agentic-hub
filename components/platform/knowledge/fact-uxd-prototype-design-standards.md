---
type: fact
title: RHOAI dashboard design standards from UXD prototype
description: Key design standards extracted from the UXD prototype (3.6 branch) -- page shell structure (#prototype wrapper, pf-m-fill container), CSS patterns (#f2f2f2 canvas, 16px border-radius cards, 24px content margins), .design/ folder spec for design history and rationale.
timestamp: 2026-08-03
tags: [platform, uxd, design, css, patternfly]
components: [platform]
review_after: 2026-11-03
source: https://gitlab.cee.redhat.com/uxd/prototypes/rhoai (branch 3.6), app.css + live computed styles
---

Design standards extracted from the UXD RHOAI prototype, confirmed against
both the source CSS (`src/app/app.css`) and live computed styles on the
deployed site.

## Page shell structure

The prototype uses a `#prototype` wrapper div scoping all custom CSS:
```
#prototype
  .pf-v6-c-page
    header.pf-v6-c-masthead (prototype banner -- dark, #1b1d21)
    header.pf-v6-c-masthead (RHOAI masthead -- #f2f2f2)
    .pf-v6-c-page__sidebar.pf-m-expanded
    .pf-v6-c-page__main-container.pf-m-fill
      main.pf-v6-c-page__main
```

Key CSS from `app.css`:
```css
#prototype .pf-v6-c-page__main-container.pf-m-fill {
  --pf-v6-c-page__main-container--BackgroundColor: #ffffff;
  background: #ffffff !important;
}
```

## Color palette

| Element | Color | Notes |
|---|---|---|
| Masthead background | `#f2f2f2` (`rgb(242,242,242)`) | Same as sidebar |
| Sidebar background | `#f2f2f2` | Seamless blend with masthead |
| Content area background | `#ffffff` | White, with 16px border-radius |
| Home page canvas | `#f2f2f2` | Cards are white on grey |
| Card border (detail page) | `1px solid #e5e7eb` (`rgb(229,231,235)`) | 0.667px in computed |
| Card border-radius | `16px` | All cards |
| Content area border-radius | `16px` | Top-left rounded corner |
| Content area margin | `0 24px 0 0` | Right margin; bottom varies |

## Typography and spacing

| Element | Value |
|---|---|
| Page title (h1) | 24px, weight 500 |
| Section heading (h2) | 20px, weight 500 |
| Nav link | 14px, padding 8px 16px, border-radius 6px |
| Nav link color | `#4d4d4d` (`rgb(77,77,77)`) |
| Detail field label | 14px, weight 500, color `#6b7280` |
| Page section padding | 16px 20px |
| Toggle group margin | 16px 0 24px |

## Modal (Deploy/Register pattern)

| Property | Value |
|---|---|
| Class | `pf-v6-c-modal-box pf-m-md` |
| Width | 840px, max-width calc(100% - 32px) |
| Border-radius | 24px |
| Box-shadow | `rgba(41,41,41,0.15) 0px 10px 20px` |
| Header padding | 24px 24px 8px |
| Body padding | 8px 24px 0 |
| Footer padding | 24px |
| Title | 20px, weight 500 |

## Nav patterns

- No blue left border on active items (PF6 `::before` pseudo-element
  hidden)
- Hover: rounded rectangle (border-radius 6px), PF6 native hover
- Expandable sections: chevron right (collapsed) -> rotated 90deg
  (expanded)
- Review badge: `pf-v6-c-label pf-m-blue pf-m-outline pf-m-compact`
  at font-size 10px

## .design/ folder convention

The UXD repo uses a `.design/` folder at the root for structured design
context. Each feature gets a subfolder with `design-history.md` (chrono
record of design evolution, rationale, stakeholder feedback). Product-wide
guidelines live under `.design/product/`.
