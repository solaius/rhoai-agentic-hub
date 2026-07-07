# HTML Preview Generation Guide

This guide explains how to convert a finalized blog post (`final.md`) into a branded HTML preview using the template at `assets/blog-template.html`.

## Process Overview

1. Read the template from `assets/blog-template.html`
2. Extract metadata from `final.md` (title, subtitle, author, etc.)
3. Convert the markdown body content to HTML elements
4. Replace all `{{PLACEHOLDER}}` tokens with actual values
5. Write the result to `features/<feature>/enablement/blog-<topic-short>/index.html`

## Template Placeholders

| Placeholder | Source | Example |
|---|---|---|
| `{{TITLE}}` | H1 heading from the blog post | The MCP Catalog is here |
| `{{SUBTITLE}}` | Line immediately after the H1 (bold/italic text) | Your agents need tools... |
| `{{META_DESCRIPTION}}` | From `seo.md` if available, otherwise generate a 150-160 char summary | Red Hat OpenShift AI 3.4 introduces... |
| `{{PRODUCT_LABEL}}` | Primary product from the qualifying summary | Red Hat OpenShift AI |
| `{{AUTHOR}}` | Byline from the blog submission form | Peter Double |
| `{{DATE}}` | Publication month/year from the submission form | April 2026 |
| `{{READ_TIME}}` | Calculate: word count / 200, round up, format as "N min read" | 6 min read |
| `{{YEAR}}` | Current year for the copyright footer | 2026 |
| `{{BREADCRUMBS}}` | Build from blog type and topic (see below) | `<a href="#">Red Hat Blog</a>...` |
| `{{BODY_CONTENT}}` | Converted markdown body (see conversion rules below) | Full HTML article content |

## Breadcrumb Construction

Build breadcrumbs from the blog type and topic area:

```html
<!-- Red Hat Blog example -->
<a href="#">Red Hat Blog</a>
<span class="sep">/</span>
<a href="#">Red Hat AI</a>
<span class="sep">/</span>
<span>Topic Name</span>

<!-- Developer Blog example -->
<a href="#">Red Hat Developer Blog</a>
<span class="sep">/</span>
<a href="#">AI/ML</a>
<span class="sep">/</span>
<span>Topic Name</span>
```

The middle breadcrumb should reflect the product area. The final breadcrumb (plain `<span>`, not a link) is the short topic name.

## Markdown to HTML Conversion Rules

Convert the blog body content (everything after the H1 title and subtitle in `final.md`) into HTML elements using these mappings:

### Basic Elements

| Markdown | HTML |
|---|---|
| `## Heading` | `<h2>Heading</h2>` |
| `### Heading` | `<h3>Heading</h3>` |
| Paragraph text | `<p>Paragraph text</p>` |
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` | `<em>italic</em>` |
| `[text](url)` | `<a href="url">text</a>` |
| `**[text](url)**` | `<strong><a href="url">text</a></strong>` |
| Bulleted list | `<ul><li>...</li></ul>` |
| Numbered list | `<ol><li>...</li></ol>` |

### Special Elements

#### CTA Links (bold links to Red Hat properties)
Bold links that serve as calls-to-action keep the same `<strong><a>` structure. The CSS handles the styling.

#### Tier/Group Headers (bold lead-in paragraphs before lists)
When a bold paragraph introduces a list of items by category (e.g., "**Three Red Hat MCP servers** connect your agents..."), render it as:

```html
<p class="tier-header">Three Red Hat MCP servers connect your agents...</p>
```

#### Pull Quotes / Taglines
For emphasized standalone statements that serve as pull quotes:

```html
<div class="tagline">The statement text here.</div>
```

#### Series Callout
If the blog mentions being part of a series, wrap the series note in:

```html
<div class="series-callout">
  This is the first post in a series on...
</div>
```

Place it at the end of the article, before the closing `</article>` tag.

#### Code Blocks
For code samples (common in developer blog posts):

```html
<pre><code>code content here</code></pre>
```

Inline code uses `<code>inline</code>`.

### Image Placeholders

Convert image placeholder blocks from the draft into styled placeholder cards. Each placeholder in the markdown looks like:

```
--------------------
**[Image Placeholder N: description]**
...
**Alt text**: descriptive text
--------------------
```

Convert to:

```html
<div class="image-placeholder">
  <div class="ph-icon">
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg>
  </div>
  <div class="ph-title">Image N: description</div>
  <div class="ph-alt">Alt text content here</div>
</div>
```

When a placeholder describes a structured diagram (e.g., a comparison table, tier breakdown, architecture layers), render it as an actual HTML diagram instead of a placeholder card. Use the appropriate CSS classes:

```html
<!-- Multi-column comparison diagram -->
<div class="tier-diagram">
  <div class="tier-diagram-title">Diagram Title</div>
  <div class="tier-columns">
    <div class="tier-col">
      <div class="tier-col-header rh">Column Header</div>
      <div class="tier-col-item">Item 1</div>
      <div class="tier-col-item">Item 2</div>
    </div>
    <!-- more columns... -->
  </div>
</div>
```

Column header color classes: `rh` (Red Hat Red #EE0000), `partner` (Blue #0066CC), `community` (Green #3D7317), `neutral` (Gray #6A6E73).

### Actual Images

When real images are available (replacing placeholders), use:

```html
<!-- Simple image -->
<img src="path/to/image.png" alt="Descriptive alt text">

<!-- Image with caption -->
<figure>
  <img src="path/to/image.png" alt="Descriptive alt text">
  <figcaption>Caption text here</figcaption>
</figure>
```

## Read Time Calculation

```
read_time = ceil(word_count / 200)
```

Count words in the body content only (exclude submission form, image generation prompts, placement rationale). Round up. Format as `N min read`.

## Quality Checklist

Before writing the HTML file, verify:

- [ ] All `{{PLACEHOLDER}}` tokens have been replaced (search for `{{` to confirm)
- [ ] All markdown links converted to `<a>` tags with correct `href`
- [ ] No raw markdown syntax remains in the HTML
- [ ] Image placeholders converted to `.image-placeholder` cards or rendered diagrams
- [ ] Series callout present if the blog is part of a series
- [ ] CTA links are bold (`<strong><a>`)
- [ ] No em dashes in the content
- [ ] H1 title only appears in the hero, not in the article body
- [ ] Subtitle only appears in the hero, not in the article body
- [ ] Blog submission form and checklist are excluded
