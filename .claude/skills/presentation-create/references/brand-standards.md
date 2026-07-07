# Red Hat Brand Standards Reference

Official brand standards at https://www.redhat.com/en/about/brand/standards govern all Red Hat visual output. This reference summarizes the key elements for HTML presentation creation.

## Brand Standards Sub-Pages

| Sub-Page | URL | Use For |
|---|---|---|
| **Color** | [/color](https://www.redhat.com/en/about/brand/standards/color) | Full palette: primary, neutrals, extended families |
| **Typography** | [/typography](https://www.redhat.com/en/about/brand/standards/typography) | Red Hat Display, Text, Mono font families and usage |
| **Logo** | [/logo](https://www.redhat.com/en/about/brand/standards/logo) | Logo usage, clear space, do/don't rules |
| **Personality** | [/personality](https://www.redhat.com/en/about/brand/standards/personality) | Brand voice attributes, tone guidance |
| **Standard Icons** | [/icons/standard-icons](https://www.redhat.com/en/about/brand/standards/icons/standard-icons) | General-purpose Red Hat icons |
| **Technology Icons** | [/icons/technology-icons](https://www.redhat.com/en/about/brand/standards/icons/technology-icons) | Product and technology iconography |
| **UI Icons** | [/icons/ui-icons](https://www.redhat.com/en/about/brand/standards/icons/ui-icons) | Interface icons for web/app use |
| **Illustration** | [/illustration](https://www.redhat.com/en/about/brand/standards/illustration) | Illustration style and usage |
| **The Hat** | [/the-hat](https://www.redhat.com/en/about/brand/standards/the-hat) | Fedora hat mark usage |
| **Resources** | [/resources](https://www.redhat.com/en/about/brand/standards/resources) | Downloadable assets, templates |

## Color Palette

### Primary

- **Red Hat Red**: `#EE0000` — primary brand color, use for accents, CTAs, highlighted states
- Dark Red scale: `#A60000`, `#5F0000`, `#3F0000`
- Light Red scale: `#F56E6E`, `#F9A8A8`, `#FBC5C5`, `#FCE3E3`, `#FEF0F0`

### Neutrals (critical for dark UI presentations)

- Black/near-black: `#151515`, `#1F1F1F`, `#212427`, `#292929`
- Dark gray: `#383838`, `#4F5255`, `#6A6E73`
- Medium gray: `#8C8C8C`, `#A3A3A3`, `#B8BBBE`
- Light gray: `#C7C7C7`, `#D2D2D2`, `#E0E0E0`, `#F0F0F0`, `#F2F2F2`
- White: `#FFFFFF`

### Extended Families (for data visualization, diagrams, color-coding)

| Family | Dark | Medium | Primary | Light | Lightest |
|---|---|---|---|---|---|
| **Blue** | `#003366` | `#004D99` | `#0066CC` | `#4394E5` | `#73BCF7` |
| **Teal** | `#003333` | `#004D4D` | `#147878` | `#37A3A3` | `#63BDBD` |
| **Purple** | `#1B0D33` | `#21134D` | `#3D2785` | `#5E40BE` | `#876FD4` |
| **Green** | `#183301` | `#204D00` | `#3D7317` | `#63993D` | `#87BB62` |
| **Orange** | `#4C1405` | `#731F00` | `#B1380B` | `#F0561D` | `#F4784A` |
| **Yellow** | `#54330B` | `#96640F` | `#B98412` | `#DCA614` | `#FFCC17` |

### Semantic Color Usage in Presentations

| Element | Color | Hex |
|---|---|---|
| Labels, eyebrows, active state | Red Hat Red | `#EE0000` |
| MCP/ecosystem components | Teal | `#009596` |
| Features, capabilities, interactive | Blue | `#0066CC` / `#4394E5` |
| Success, GA, production | Green | `#3E8635` |
| Warnings, manual processes | Orange/Yellow | `#F4B400` |
| Governance, policy | Purple | `#6753AC` |
| Borders (subtle) | Dark gray | `#333333` |
| Card backgrounds (elevated) | Near-black | `#1a1a1a` |
| Canvas background | Black | `#151515` |
| Primary text | White | `#FFFFFF` |
| Secondary text | Light gray | `#D2D2D2` |
| Muted text | Medium gray | `#8A8A8A` |

## Typography

| Font Family | Role | Weights | Google Fonts |
|---|---|---|---|
| **Red Hat Display** | Headings, display text, hero elements | 400, 500, 600, 700, 800, 900 | [Link](https://fonts.google.com/specimen/Red+Hat+Display) |
| **Red Hat Text** | Body copy, paragraphs, content | 400, 500, 600, 700 | [Link](https://fonts.google.com/specimen/Red+Hat+Text) |
| **Red Hat Mono** | Code, labels, tags, technical content | 400, 500, 600 | [Link](https://fonts.google.com/specimen/Red+Hat+Mono) |

### Typography Hierarchy in Presentations

| Level | Font | Size | Weight | Usage |
|---|---|---|---|---|
| Display XL | Red Hat Display | 2.8rem | 800 | Hero titles |
| Display LG | Red Hat Display | 2rem | 700 | Section titles |
| H2 | Red Hat Display | 1.5rem | 700 | Subsection headings |
| Body Lead | Red Hat Text | 1.15rem | 400 | Introductory paragraphs |
| Body | Red Hat Text | 0.95rem | 400 | Content text |
| Label | Red Hat Mono | 0.7rem | 600-700 | Section labels, tags (uppercase) |
| Small | Red Hat Mono | 0.6rem | 400 | Timestamps, secondary labels |

## Logo Usage

For HTML presentations, the Red Hat logo is typically placed:
- **Header**: Stylized "RH" square + product name in the navigation bar
- **Hero section**: Small logo in top-right corner, opacity 0.7-0.85
- **Footer/last slide**: Full Red Hat logo or author attribution

### Logo Selection Guide

| Background | Logo Variant | Example Placement |
|---|---|---|
| Dark (`#151515`, `#1a1a1a`) | **A-Reverse** (red hat + white text) | Nav bar, dark hero, footer |
| Light (`#FFFFFF`, `#F0F0F0`) | **A-Standard** (red hat + black text) | Light header, content area |
| Red (`#EE0000`) | **A-White** (all white) | Red hero banner, CTA sections |
| Any (small space) | **Hat Icon - Red** | Favicon-sized, decorative |

### Logo A — Reverse (red hat + white text, for dark backgrounds)

The default for dark-themed presentations. Red fedora with white wordmark.

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 613 145" height="32">
  <path fill="#e00" d="M127.47,83.49c12.51,0,30.61-2.58,30.61-17.46a14,14,0,0,0-.31-3.42l-7.45-32.36c-1.72-7.12-3.23-10.35-15.73-16.6C124.89,8.69,103.76.5,97.51.5,91.69.5,90,8,83.06,8c-6.68,0-11.64-5.6-17.89-5.6-6,0-9.91,4.09-12.93,12.5,0,0-8.41,23.72-9.49,27.16A6.43,6.43,0,0,0,42.53,44c0,9.22,36.3,39.45,84.94,39.45M160,72.07c1.73,8.19,1.73,9.05,1.73,10.13,0,14-15.74,21.77-36.43,21.77C78.54,104,37.58,76.6,37.58,58.49a18.45,18.45,0,0,1,1.51-7.33C22.27,52,.5,55,.5,74.22c0,31.48,74.59,70.28,133.65,70.28,45.28,0,56.7-20.48,56.7-36.65,0-12.72-11-27.16-30.83-35.78"/>
  <path fill="#e00" d="M160,72.07c1.73,8.19,1.73,9.05,1.73,10.13,0,14-15.74,21.77-36.43,21.77C78.54,104,37.58,76.6,37.58,58.49a18.45,18.45,0,0,1,1.51-7.33l3.66-9.06A6.43,6.43,0,0,0,42.53,44c0,9.22,36.3,39.45,84.94,39.45,12.51,0,30.61-2.58,30.61-17.46a14,14,0,0,0-.31-3.42Z"/>
  <path fill="#fff" d="M579.74,92.8c0,11.89,7.15,17.67,20.19,17.67a52.11,52.11,0,0,0,11.89-1.68V95a24.84,24.84,0,0,1-7.68,1.16c-5.37,0-7.36-1.68-7.36-6.73V68.3h15.56V54.1H596.78v-18l-17,3.68V54.1H568.49V68.3h11.25Zm-53,.32c0-3.68,3.69-5.47,9.26-5.47a43.12,43.12,0,0,1,10.1,1.26v7.15a21.51,21.51,0,0,1-10.63,2.63c-5.46,0-8.73-2.1-8.73-5.57m5.2,17.56c6,0,10.84-1.26,15.36-4.31v3.37h16.82V74.08c0-13.56-9.14-21-24.39-21-8.52,0-16.94,2-26,6.1l6.1,12.52c6.52-2.74,12-4.42,16.83-4.42,7,0,10.62,2.73,10.62,8.31v2.73a49.53,49.53,0,0,0-12.62-1.58c-14.31,0-22.93,6-22.93,16.73,0,9.78,7.78,17.24,20.19,17.24m-92.44-.94h18.09V80.92h30.29v28.82H506V36.12H487.93V64.41H457.64V36.12H439.55ZM370.62,81.87c0-8,6.31-14.1,14.62-14.1A17.22,17.22,0,0,1,397,72.09V91.54A16.36,16.36,0,0,1,385.24,96c-8.2,0-14.62-6.1-14.62-14.09m26.61,27.87h16.83V32.44l-17,3.68V57.05a28.3,28.3,0,0,0-14.2-3.68c-16.19,0-28.92,12.51-28.92,28.5a28.25,28.25,0,0,0,28.4,28.6,25.12,25.12,0,0,0,14.93-4.83ZM320,67c5.36,0,9.88,3.47,11.67,8.83H308.47C310.15,70.3,314.36,67,320,67M291.33,82c0,16.2,13.25,28.82,30.28,28.82,9.36,0,16.2-2.53,23.25-8.42l-11.26-10c-2.63,2.74-6.52,4.21-11.14,4.21a14.39,14.39,0,0,1-13.68-8.83h39.65V83.55c0-17.67-11.88-30.39-28.08-30.39a28.57,28.57,0,0,0-29,28.81M262,51.58c6,0,9.36,3.78,9.36,8.31S268,68.2,262,68.2H244.11V51.58Zm-36,58.16h18.09V82.92h13.77l13.89,26.82H292l-16.2-29.45a22.27,22.27,0,0,0,13.88-20.72c0-13.25-10.41-23.45-26-23.45H226Z"/>
</svg>
```

### Logo A — Standard (red hat + black text, for light backgrounds)

Red fedora with black wordmark. Use when the page has white or light gray sections.

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 613 145" height="32">
  <path fill="#e00" d="M127.47,83.49c12.51,0,30.61-2.58,30.61-17.46a14,14,0,0,0-.31-3.42l-7.45-32.36c-1.72-7.12-3.23-10.35-15.73-16.6C124.89,8.69,103.76.5,97.51.5,91.69.5,90,8,83.06,8c-6.68,0-11.64-5.6-17.89-5.6-6,0-9.91,4.09-12.93,12.5,0,0-8.41,23.72-9.49,27.16A6.43,6.43,0,0,0,42.53,44c0,9.22,36.3,39.45,84.94,39.45M160,72.07c1.73,8.19,1.73,9.05,1.73,10.13,0,14-15.74,21.77-36.43,21.77C78.54,104,37.58,76.6,37.58,58.49a18.45,18.45,0,0,1,1.51-7.33C22.27,52,.5,55,.5,74.22c0,31.48,74.59,70.28,133.65,70.28,45.28,0,56.7-20.48,56.7-36.65,0-12.72-11-27.16-30.83-35.78"/>
  <path d="M160,72.07c1.73,8.19,1.73,9.05,1.73,10.13,0,14-15.74,21.77-36.43,21.77C78.54,104,37.58,76.6,37.58,58.49a18.45,18.45,0,0,1,1.51-7.33l3.66-9.06A6.43,6.43,0,0,0,42.53,44c0,9.22,36.3,39.45,84.94,39.45,12.51,0,30.61-2.58,30.61-17.46a14,14,0,0,0-.31-3.42Z"/>
  <path d="M579.74,92.8c0,11.89,7.15,17.67,20.19,17.67a52.11,52.11,0,0,0,11.89-1.68V95a24.84,24.84,0,0,1-7.68,1.16c-5.37,0-7.36-1.68-7.36-6.73V68.3h15.56V54.1H596.78v-18l-17,3.68V54.1H568.49V68.3h11.25Zm-53,.32c0-3.68,3.69-5.47,9.26-5.47a43.12,43.12,0,0,1,10.1,1.26v7.15a21.51,21.51,0,0,1-10.63,2.63c-5.46,0-8.73-2.1-8.73-5.57m5.2,17.56c6,0,10.84-1.26,15.36-4.31v3.37h16.82V74.08c0-13.56-9.14-21-24.39-21-8.52,0-16.94,2-26,6.1l6.1,12.52c6.52-2.74,12-4.42,16.83-4.42,7,0,10.62,2.73,10.62,8.31v2.73a49.53,49.53,0,0,0-12.62-1.58c-14.31,0-22.93,6-22.93,16.73,0,9.78,7.78,17.24,20.19,17.24m-92.44-.94h18.09V80.92h30.29v28.82H506V36.12H487.93V64.41H457.64V36.12H439.55ZM370.62,81.87c0-8,6.31-14.1,14.62-14.1A17.22,17.22,0,0,1,397,72.09V91.54A16.36,16.36,0,0,1,385.24,96c-8.2,0-14.62-6.1-14.62-14.09m26.61,27.87h16.83V32.44l-17,3.68V57.05a28.3,28.3,0,0,0-14.2-3.68c-16.19,0-28.92,12.51-28.92,28.5a28.25,28.25,0,0,0,28.4,28.6,25.12,25.12,0,0,0,14.93-4.83ZM320,67c5.36,0,9.88,3.47,11.67,8.83H308.47C310.15,70.3,314.36,67,320,67M291.33,82c0,16.2,13.25,28.82,30.28,28.82,9.36,0,16.2-2.53,23.25-8.42l-11.26-10c-2.63,2.74-6.52,4.21-11.14,4.21a14.39,14.39,0,0,1-13.68-8.83h39.65V83.55c0-17.67-11.88-30.39-28.08-30.39a28.57,28.57,0,0,0-29,28.81M262,51.58c6,0,9.36,3.78,9.36,8.31S268,68.2,262,68.2H244.11V51.58Zm-36,58.16h18.09V82.92h13.77l13.89,26.82H292l-16.2-29.45a22.27,22.27,0,0,0,13.88-20.72c0-13.25-10.41-23.45-26-23.45H226Z"/>
</svg>
```

### Logo A — White (all white, for red or dark colored backgrounds)

All-white logo for use on red hero banners or colored section backgrounds.

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 613 145" height="32">
  <path fill="#fff" d="M127.47,83.49c12.51,0,30.61-2.58,30.61-17.46a14,14,0,0,0-.31-3.42l-7.45-32.36c-1.72-7.12-3.23-10.35-15.73-16.6C124.89,8.69,103.76.5,97.51.5,91.69.5,90,8,83.06,8c-6.68,0-11.64-5.6-17.89-5.6-6,0-9.91,4.09-12.93,12.5,0,0-8.41,23.72-9.49,27.16A6.43,6.43,0,0,0,42.53,44c0,9.22,36.3,39.45,84.94,39.45M160,72.07c1.73,8.19,1.73,9.05,1.73,10.13,0,14-15.74,21.77-36.43,21.77C78.54,104,37.58,76.6,37.58,58.49a18.45,18.45,0,0,1,1.51-7.33C22.27,52,.5,55,.5,74.22c0,31.48,74.59,70.28,133.65,70.28,45.28,0,56.7-20.48,56.7-36.65,0-12.72-11-27.16-30.83-35.78"/>
  <path fill="#fff" d="M579.74,92.8c0,11.89,7.15,17.67,20.19,17.67a52.11,52.11,0,0,0,11.89-1.68V95a24.84,24.84,0,0,1-7.68,1.16c-5.37,0-7.36-1.68-7.36-6.73V68.3h15.56V54.1H596.78v-18l-17,3.68V54.1H568.49V68.3h11.25Zm-53,.32c0-3.68,3.69-5.47,9.26-5.47a43.12,43.12,0,0,1,10.1,1.26v7.15a21.51,21.51,0,0,1-10.63,2.63c-5.46,0-8.73-2.1-8.73-5.57m5.2,17.56c6,0,10.84-1.26,15.36-4.31v3.37h16.82V74.08c0-13.56-9.14-21-24.39-21-8.52,0-16.94,2-26,6.1l6.1,12.52c6.52-2.74,12-4.42,16.83-4.42,7,0,10.62,2.73,10.62,8.31v2.73a49.53,49.53,0,0,0-12.62-1.58c-14.31,0-22.93,6-22.93,16.73,0,9.78,7.78,17.24,20.19,17.24m-92.44-.94h18.09V80.92h30.29v28.82H506V36.12H487.93V64.41H457.64V36.12H439.55ZM370.62,81.87c0-8,6.31-14.1,14.62-14.1A17.22,17.22,0,0,1,397,72.09V91.54A16.36,16.36,0,0,1,385.24,96c-8.2,0-14.62-6.1-14.62-14.09m26.61,27.87h16.83V32.44l-17,3.68V57.05a28.3,28.3,0,0,0-14.2-3.68c-16.19,0-28.92,12.51-28.92,28.5a28.25,28.25,0,0,0,28.4,28.6,25.12,25.12,0,0,0,14.93-4.83ZM320,67c5.36,0,9.88,3.47,11.67,8.83H308.47C310.15,70.3,314.36,67,320,67M291.33,82c0,16.2,13.25,28.82,30.28,28.82,9.36,0,16.2-2.53,23.25-8.42l-11.26-10c-2.63,2.74-6.52,4.21-11.14,4.21a14.39,14.39,0,0,1-13.68-8.83h39.65V83.55c0-17.67-11.88-30.39-28.08-30.39a28.57,28.57,0,0,0-29,28.81M262,51.58c6,0,9.36,3.78,9.36,8.31S268,68.2,262,68.2H244.11V51.58Zm-36,58.16h18.09V82.92h13.77l13.89,26.82H292l-16.2-29.45a22.27,22.27,0,0,0,13.88-20.72c0-13.25-10.41-23.45-26-23.45H226Z"/>
</svg>
```

### Hat Icon — Red (fedora only, no text)

The standalone fedora mark for small spaces. Per brand guidelines, the hat should always appear in red when used without the wordmark.

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 145" height="28">
  <path fill="#e00" d="M127.47,83.49c12.51,0,30.61-2.58,30.61-17.46a14,14,0,0,0-.31-3.42l-7.45-32.36c-1.72-7.12-3.23-10.35-15.73-16.6C124.89,8.69,103.76.5,97.51.5,91.69.5,90,8,83.06,8c-6.68,0-11.64-5.6-17.89-5.6-6,0-9.91,4.09-12.93,12.5,0,0-8.41,23.72-9.49,27.16A6.43,6.43,0,0,0,42.53,44c0,9.22,36.3,39.45,84.94,39.45M160,72.07c1.73,8.19,1.73,9.05,1.73,10.13,0,14-15.74,21.77-36.43,21.77C78.54,104,37.58,76.6,37.58,58.49a18.45,18.45,0,0,1,1.51-7.33C22.27,52,.5,55,.5,74.22c0,31.48,74.59,70.28,133.65,70.28,45.28,0,56.7-20.48,56.7-36.65,0-12.72-11-27.16-30.83-35.78"/>
</svg>
```

### CSS Hat Mark (lightweight alternative)

For nav bars where loading the full SVG is unnecessary, the "RH" square mark works well:

```css
.hat {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: var(--rh-red);
  color: white;
  font-family: var(--font-sans);
  font-weight: 800;
  font-size: 0.65rem;
  border-radius: 4px;
}
```

## Design System Reference

The product UI (not presentations) uses **PatternFly** (https://www.patternfly.org/) — Red Hat's open source design system. Presentations don't use PatternFly components directly but share the same color palette and font families.
