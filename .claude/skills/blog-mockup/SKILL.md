---
name: blog-mockup
description: Quickly generate a Red Hat branded HTML mockup of any blog content, staged under a feature's enablement/ directory. Use this skill when the user wants to preview a blog post, create an HTML mockup, see what a blog looks like rendered, visualize blog content, or says things like "mockup this blog", "preview this as HTML", "show me what this looks like as a Red Hat blog", "render this blog post", or "create an HTML preview". Works with markdown files, Google Docs, pasted text, or any content the user provides. This is a lightweight alternative to the full blog-create pipeline when you just need a visual preview without the review loop. Building the preview does not publish it — hand off to hub.publish only on explicit request (previews of unreviewed drafts default to unpublished).
---

# blog-mockup

Generate a Red Hat branded HTML preview of any blog content. This is a quick, single-pass skill for visualizing blog posts. It does not run the review pipeline or create abstracts. Use `blog-create` for the full creation and review workflow.

## When to Use This vs blog-create

| Scenario | Skill |
|---|---|
| Writing a new blog from scratch | `blog-create` |
| Reviewing/improving an existing draft | `blog-create` |
| Quick visual preview of any content | `blog-mockup` |
| Rendering a `final.md` as HTML | `blog-mockup` |
| Previewing a Google Doc as a Red Hat blog | `blog-mockup` |
| "What would this look like as a blog?" | `blog-mockup` |

## Inputs

The skill accepts blog content from any of these sources:

1. **A markdown file path** (e.g., `features/mcp-registry/enablement/blog-mcp-catalog/final.md`)
2. **A Google Doc link** (fetch via `mcp__google-workspace__get_doc_as_markdown` with user `pedouble@redhat.com`)
3. **Pasted text** directly in the conversation
4. **A URL** (fetch via Playwright for JS-rendered pages, WebFetch otherwise)

## Workflow

### Step 1: Get the content

Read or fetch the blog content from whatever source the user provides.

### Step 2: Determine the output location

- **If the source is already inside a feature's `enablement/` directory** (e.g., a `final.md` from a prior `blog-create` run), write the preview as `index.html` alongside it — no further questions needed.
- **Otherwise** (pasted text, a URL, a Google Doc, or a markdown file that isn't yet filed anywhere), determine which feature partition in `features/features.yaml` this content belongs to — infer from the topic and confirm, or ask if it's unclear. Output goes to `features/<feature>/enablement/blog-<topic-short>/index.html`, creating the directory if it doesn't exist yet. If no existing feature fits, don't invent one — hand off to `hub.file`, then resume once it exists.
- **If the user explicitly wants a throwaway preview with no repo footprint** (a quick one-off look, nothing meant to be filed or kept), honor that and ask where to save it instead of filing it under `features/`.

### Step 3: Extract metadata

From the content, extract or infer:

| Field | How to find it |
|---|---|
| **Title** | The H1 heading, or the first prominent heading |
| **Subtitle** | Bold/italic text immediately after the title, or first sentence |
| **Author** | If present in a submission form or byline; default to "Peter Double" |
| **Product label** | Primary product mentioned (e.g., "Red Hat OpenShift AI") |
| **Date** | From submission form or current month/year |
| **Read time** | `ceil(word_count / 200)` formatted as "N min read" |

If metadata cannot be inferred, ask the user. If only the title is ambiguous, ask about the title and use sensible defaults for the rest.

### Step 4: Read the template and guide

- Read the HTML template from `.claude/skills/blog-create/assets/blog-template.html`
- Read the conversion guide from `.claude/skills/blog-create/references/html-preview-guide.md`

The blog-mockup skill shares these assets with blog-create. The conversion guide explains how to transform markdown to HTML elements, handle image placeholders, build breadcrumbs, and use the available CSS classes.

### Step 5: Convert content to HTML

Follow the conversion rules in `.claude/skills/blog-create/references/html-preview-guide.md` to transform the blog body into HTML. Key points:

- Convert markdown headings, paragraphs, lists, links, bold/italic to their HTML equivalents
- Use `class="tier-header"` for bold lead-in paragraphs that introduce categorized lists
- Use `class="tagline"` for pull-quote callouts
- Use `class="series-callout"` for series context notes
- Render image placeholders as `.image-placeholder` cards, or as actual HTML diagrams (`.tier-diagram`) when the placeholder describes a structured comparison
- Strip any blog submission forms, checklists, or process metadata from the content
- Exclude the H1 title and subtitle from the body (they go in the hero section)

### Step 6: Assemble and write

Replace all `{{PLACEHOLDER}}` tokens in the template with actual values and write the output file to the path determined in Step 2.

### Step 7: Confirm and offer next steps

Tell the user where the file is and suggest they open it in a browser. Then:

- **Publishing**: writing the file does not make it public. If the user wants it live, hand off to `hub.publish` — but treat this as a real disclosure decision, not a rubber stamp: a preview of an unpublished, unreviewed blog draft becomes world-readable the moment it's added to `publish/manifest.yaml`. Default to NOT publishing; only proceed on explicit request, and confirm the user actually means the preview itself (as opposed to the underlying Red Hat blog process, which is separate and unaffected by anything in this repo).
- **Capture durable side-knowledge**: if generating this preview surfaced a decision or fact worth keeping beyond the artifact itself, offer `hub.capture` for that one item.

## Important Notes

- Do not include blog submission forms, pre-submission checklists, or review metadata in the HTML output
- The H1 title and subtitle belong only in the hero section, not repeated in the article body
- Verify no `{{` placeholder tokens remain in the final HTML
- No em dashes in the rendered content
- If the content has no image placeholders, that is fine; skip image handling
