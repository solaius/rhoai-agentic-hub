---
name: blog-create
description: Create Red Hat blog posts or review existing drafts through a multi-agent pipeline with iterative quality improvement, staged under a feature's enablement/ directory. Use this skill whenever the user wants to write a blog post, create blog content, draft a Red Hat blog, review a blog draft, improve a blog post, or says things like "write a blog about X", "I need a blog post", "review my blog draft", "help me with a blog", "create a developer blog", or "blog about [topic]". Also use when the user shares a Google Doc or draft and wants it turned into a polished Red Hat blog post. Producing a draft does not publish it — sharing happens through the Red Hat blog submission process (Workfront), and any HTML preview only goes public via hub.publish. Benefits from Google Workspace MCP (Google Docs) and Playwright (JS-rendered Red Hat blog pages for research).
---

# blog-create

A multi-agent blog creation and review skill for Red Hat blog posts (redhat.com/blog and developers.redhat.com/blog). Handles two modes — creating blogs from scratch and reviewing existing drafts — through a unified pipeline with iterative quality improvement via four specialized sub-agent reviewers.

## Why This Skill Exists

Writing a strong Red Hat blog post requires balancing technical depth, editorial compliance, brand voice, visual communication, and narrative structure. No single pass catches everything. This skill uses four independent reviewers — each with a focused lens — to iteratively improve drafts until they meet a quality bar. The human stays in the loop at defined checkpoints, and all artifacts are versioned so nothing is lost.

## Before You Start

Load into context — they ground the entire workflow:

1. **`/memory/index.md`** — always-loaded tier: current hub state, active work, recent decisions, roadmap. Read this immediately, before Phase 1.
2. **`references/blog-creation-guide.md`** (this skill) — Red Hat editorial process, writing patterns, formatting rules, brand standards, examples. Read this immediately too.
3. **The target feature's `features/<f>/knowledge/index.md`** — stakeholders, decisions, open questions for the product area this blog covers. This can only be loaded once Phase 1 has identified the feature (see Feature Routing below) — read it before Phase 2 Abstract, and again fresh at each Phase 4 review cycle for the Content reviewer.

These are living documents. Read them fresh every time — don't rely on cached knowledge.

## Workflow Overview

```
Phase 1: Qualify → Phase 2: Abstract → Phase 3: Draft → Phase 4: Review Loop → Phase 5: Finalize
```

Each phase has a clear exit condition. Do not advance to the next phase until the current phase's exit condition is met.

## Phase 1: Qualify

**Purpose**: Gather requirements through conversational questions to establish the blog's goal, audience, structure, and source material.

**How**: Read `references/qualifying-questions.md` for the full question framework and adaptive logic.

**Inputs to gather**:
- Blog type (Red Hat Blog vs Developer Blog)
- Core thesis (what single problem does this post solve?)
- Target audience
- Products/projects involved
- Source material (drafts, docs, links, or start from scratch)
- Demo/code component (yes/no)
- Series context (standalone or part of series)
- CTA target
- Timing/event tie-in

**Shortcut path**: If the user provides a Google Doc link or substantial notes upfront, fetch and analyze the content, auto-fill extractable answers, present findings, and only ask about gaps.

**Existing draft review mode**: If the user provides an existing draft to review (not create from scratch), use the shortened qualifying flow — read the draft, infer blog type/audience/thesis, confirm with user, and only ask about gaps. If the draft already lives under a `features/<feature>/enablement/` path, infer the feature from that path instead of asking.

**Feature routing**: Based on the products/topics discussed, determine which feature partition in `features/features.yaml` this blog belongs to (e.g., MCP server governance/lifecycle → `mcp-registry`; runtime traffic policy/entitlements → `mcp-gateway`; partner/community server catalog → `mcp-ecosystem`; strategy or industry perspective with no single product → `platform`). Present the proposed feature and artifact slug for user confirmation:

```
features/<feature>/enablement/blog-<topic-short>/
```

If no existing feature fits, don't invent a partition — hand off to `hub.file` (it creates new feature partitions in `features/features.yaml`), then resume qualifying once it exists.

**Exit condition**: User confirms the qualifying summary.

Output format for qualifying summary:

```markdown
## Blog Qualifying Summary

- **Blog type**: [Red Hat Blog / Red Hat Developer Blog]
- **Thesis**: [one sentence]
- **Audience**: [target readers]
- **Products**: [list]
- **Feature**: [feature id from features/features.yaml]
- **Output path**: features/[feature]/enablement/blog-[topic-short]/
- **Source material**: [list of sources]
- **Demo**: [Yes/No — details if yes]
- **Series**: [Standalone / Part N of series name]
- **CTA**: [target action]
- **Timing**: [event/release or none]
```

## Phase 2: Abstract

**Purpose**: Create a written contract for what the blog will contain, ensuring alignment before drafting begins.

Create the output directory structure:

```bash
# Create the blog artifact folder and subfolders
mkdir -p features/<feature>/enablement/blog-<topic-short>/drafts/reviews
```

Write `features/<feature>/enablement/blog-<topic-short>/abstract.md` containing:

- Thesis statement
- Target audience
- Blog type
- Key points (3 maximum)
- Products/projects involved
- CTA
- Source materials referenced
- Proposed section outline (H2 headings that tell the story)
- Series context (if applicable)
- Qualifying summary (embedded at the bottom)

**For existing draft review mode**: Generate the abstract FROM the existing draft rather than before it. The abstract describes what the draft contains and what it should become.

**Exit condition**: User approves the abstract.

## Phase 3: Draft

**Purpose**: Produce the first version of the blog post.

### From scratch
Generate v1 based on:
- The approved abstract
- Source materials (fetched via Google Workspace MCP or Playwright MCP)
- The feature's `knowledge/index.md` and `/memory/index.md` for grounding
- Fresh web research (use Playwright for Red Hat blogs — they are JS-rendered and WebFetch cannot parse them)

### Target word count
Reference the word count guidelines from `references/blog-creation-guide.md` and aim for the appropriate range based on blog type and topic depth. Typical ranges: 500-600 words for announcements, 800-1300 for tutorials, 1300-2000 for deep dives. If the topic needs more than 2000 words, propose a series split during qualifying.

### From existing content
User-provided draft or notes become v1 raw material. Copy the user's content as-is to `drafts/v1.md` — do not restructure yet (the review loop handles improvement). Note: the first review cycle will likely produce low formatting scores because the raw content hasn't been adapted to Red Hat editorial conventions yet. This is expected — the review loop is designed to improve iteratively.

### Image placeholders
Include image placeholders where visuals would aid understanding. Each placeholder follows this format:

```markdown
--------------------
**[Image Placeholder N: <short description>]**

**Placement rationale**: [Why an image belongs here, what it helps the reader understand]

**Image generation prompt**: [Detailed prompt including:
- Exact content/composition to depict
- Red Hat brand colors (#EE0000, #A30000, #151515 dark / #F0F0F0 light)
- Clean, modern style, not overloaded, not clip art
- Specific aspect ratio (hero: 16:9, inline: 4:3, diagram: 16:9 wide)
- Visual hierarchy and key callouts]

**Alt text**: [Descriptive, accessible alt text]

--------------------
```

The `--------------------` separators before and after make image placeholders visually distinct from body text, ensuring reviewers and editors can locate them easily during review.

Refer to `references/blog-creation-guide.md` Brand Standards Quick Reference for the full color palette, typography, and illustration style guidance.

### Draft conventions
- Follow all formatting rules from `references/blog-creation-guide.md`
- Sentence case headings, no H1 in body, cascading H2/H3/H4
- No backticks for code, use monospace indication
- Use Oxford commas (serial comma before "and" in lists of three or more)
- First person voice, Red Hat brand tone (open, authentic, helpful, brave)
- Use contractions aggressively ("you've", "we're", "it's", "couldn't", "we'll", "curation's", "here's", "that's"). The editor converts nearly every formal construction to a contraction. Default to contractions everywhere except when deliberate emphasis demands the uncontracted form (e.g., "That is the state of..." for rhetorical weight). After drafting, scan for any remaining "It is", "We are", "You have", "Here is", "That is" and contract them unless the emphasis is intentional.
- CTA near top (linked to Red Hat site, not bolded) and in closing. CTA link text should not be bold — the link styling is sufficient.

#### AI writing avoidance

LLM-generated prose has recognizable patterns that erode reader trust. The draft must read as if a human wrote it. Specific rules:

- **Use em dashes sparingly and without spaces.** Em dashes are legitimate punctuation for emphasis or asides, but AI text overuses them. Limit to 1-2 per post. Prefer commas, colons, or sentence breaks for most cases. The AI tell is density (every paragraph), not presence. When using em dashes, close them up with no surrounding spaces: "today—promising" not "today — promising".
- **No marketing tropes.** Avoid "That changes today", "We are pleased to announce", "In today's fast-paced world", "game-changer", "at the end of the day". These phrases signal AI or committee-written content.
- **No filler transitions.** Avoid "Moreover", "Furthermore", "Additionally", "It's worth noting that", "It goes without saying". Use direct connections or start a new thought.
- **Vary sentence structure.** AI text tends toward parallel constructions (three bullet points of identical rhythm, two-sentence paragraphs repeating the same pattern). Break the symmetry.
- **Be specific over vague.** Replace "it simplifies things" with what specifically gets simpler and how. Replace "it's faster" with the actual mechanism.
- **Write conversationally, not formally.** The editor rewrites stiff constructions into natural speech. "That is the state of MCP adoption" becomes "That's the state of MCP adoption." "You have tried it" becomes "You've tried it." Write as if speaking to a colleague, not presenting to a committee.
- **Soften absolute claims.** Prefer "focused primarily on" over "was focused on", "a significant step" over "the first step". Absolute claims invite contradiction; hedged claims are more credible and accurate.
- **Use "but" for explicit contrast.** When juxtaposing a positive and negative, add "but" rather than relying on the comma alone. "promising protocol, but painful deployment" is clearer than "promising protocol, painful deployment".
- **Soften reader-directed assumptions.** Instead of accusatory "You download a container image of unknown provenance", write "Often, this means downloading a container image of unknown provenance." The reader is more receptive when not directly blamed.
- **Prefer active voice in descriptions.** "focus solely on discovery" reads better than "are discovery surfaces". Restructure passive or nominalized constructions into active verbs.
- **Write complete questions.** "Are you attending Red Hat Summit?" not "Attending Red Hat Summit?" — sentence fragments read as informal notes, not polished prose.

#### Product name conventions

The Red Hat editorial team enforces specific capitalization and naming rules:

- **Lowercase component descriptors.** Names like "MCP catalog", "AI hub", "MCP lifecycle operator", "MCP gateway" use lowercase for the generic descriptor. They are not trademarked product names — "catalog", "hub", "operator", "gateway" are common nouns.
- **Lowercase branded portfolio names.** "Red Hat AI portfolio" — "portfolio" is a common noun descriptor, not a trademarked name. Same pattern as "catalog", "hub", "operator".
- **Full name on first mention, shorten after.** First mention: "Red Hat OpenShift AI". Subsequent: "OpenShift AI". Never abbreviate to acronyms like "RHOAI" in published content.
- **Lowercase preview/maturity states.** "developer preview", "technical preview", "general availability" — these are descriptive states, not product names. Don't capitalize them.
- **Capitalize product-specific terms.** "Ansible Playbooks" (product term), not "Ansible playbooks". Check product documentation for which terms are capitalized.
- **Title capitalization after colons.** In headings, capitalize the first word after a colon: "The MCP catalog: From discovery to deployment" (not "from").

#### Heading structure

- **Use H3 for named sub-items under H2 sections.** When listing tiers, categories, or named items under an H2, each item gets its own H3 heading rather than a bold paragraph lead-in. Example: under "## MCP servers ready to use", use "### Red Hat MCP servers", "### Technology partner MCP servers", "### Community MCP servers" — not bold text pretending to be headings.
- **Use H3 for sub-sections within H2 sections.** Under "## Building the enterprise MCP ecosystem", use "### AI quickstarts", "### Ecosystem growth", "### Enterprise governance" — not bold paragraph openers.
- **Never use bold text as a substitute for heading structure.** If content deserves a visual break and a scannable label, it deserves an H3. Bold is for emphasis within a paragraph, not for section titles.
- **Use bullet lists with bold labels for short grouped items.** When a section has 3-5 items that are each 1-3 sentences (too short for H3 headings, but needing structure), use a bulleted list with bold labels: "- **AI quickstarts**: We're working with partners..." This is the right format for future-looking items, grouped capabilities, or items that don't warrant their own sub-section.

#### Acronyms and first mentions

- **Expand acronyms on first use.** Write "[Model Context Protocol (MCP)](link)" on first mention, then "MCP" after. The reader should never encounter an unexplained acronym.
- **Apply this to protocol names, product components, and industry terms.** MCP, CTA, CRD, RAG, LLM — all need expansion on first use. "retrieval-augmented generation (RAG)", not just "RAG". Product names like "Red Hat OpenShift AI" follow the product name convention (full name first, shortened after) and do not need parenthetical acronyms.
- **Article agreement with expanded acronyms.** When a linked acronym expands to its full name, the article ("a" or "an") must agree with the first word of the expansion, not the acronym. Write "a [Model Context Protocol (MCP)](link) server" (because "Model" starts with a consonant), not "an [Model Context Protocol (MCP)](link) server". If the link text shows only the acronym, use the article that matches the acronym's pronunciation: "an MCP server".

#### Numerals and formatting

- **Use numerals in running text.** "3 tiers", "4 stages", "10 servers" — not "three tiers". Exception: spell out numbers at the start of a sentence or in a bold lead-in phrase ("Three Red Hat MCP servers connect...").
- **Break dense paragraphs into structured lists.** If a paragraph contains 3+ qualifying details or capabilities, restructure as a bulleted list with bold category labels. The editor restructures dense prose into scannable lists. For example, "validated for enterprise deployment, with production-grade connectivity, on-cluster hosting and scanned images" becomes:
  - **Production-grade connectivity**: streamable HTTP transport
  - **Secure hosting**: images built on UBI, scanned for vulnerabilities
  - **Automated deployment**: the operator creates Kubernetes resources
- **Use "with" instead of colons for qualifying details.** "validated for enterprise deployment, with production-grade connectivity" reads better than "validated for enterprise deployment: production-grade connectivity".
- **Use "including" to introduce elaborating lists.** Prefer "capabilities that production deployments demand, including supply chain controls" over colon-separated constructions. Colons work for short, punchy items; "including" and "with" work better for flowing prose.
- **Hyphenate compound adjectives before nouns.** "first-class citizens", "identity-aware routing", "production-ready path", "enterprise-grade security". The hyphen clarifies that the two words modify the noun together. No hyphen when the compound comes after the verb: "the routing is identity aware".

#### Preview status transparency

Always state preview/TP status explicitly in the body text, not just in a header or footnote. Example: "Note that as of OpenShift AI 3.4, MCP lifecycle operator is available as developer preview, and MCP gateway is available as technical preview." Readers need to know what they can actually use today.

When introducing a product with a preview state inline, use lowercase in a parenthetical: "We're introducing the MCP catalog (now in developer preview)" — not "in Developer Preview". The parenthetical form is less disruptive to reading flow than a separate sentence.

#### Competitive references

- **Never link to competitors.** If competitors need to be mentioned for positioning context (e.g., naming alternative catalogs), use their names as plain text without hyperlinks. Linking gives them SEO credit and sends readers away.
- **Do not name unconfirmed future capabilities.** When referencing roadmap items, use generic descriptions ("additional AI asset types") rather than specific names ("agents, skills, guardrails") unless officially announced.

#### Precision

- **Don't aggregate counts when tiers tell the story.** If there are three Red Hat servers, five partner servers, and two community servers, say that, not "10 servers". The tier structure is the message.
- **Be precise about automation vs manual steps.** Especially for Developer Preview features, do not imply seamless end-to-end automation if there are manual steps. Describe what each component actually does ("the Operator deploys it on your cluster... From there, the Gateway handles runtime connectivity") rather than conflating them into a single magic action.

**Exit condition**: `drafts/v1.md` written to disk.

## Phase 4: Review Loop

**Purpose**: Iteratively improve the draft through parallel sub-agent review until quality threshold is met.

### How the review loop works

Read `references/scoring.md` for full scoring rules, pass criteria, and iteration controls.

For each iteration:

1. **Spawn four reviewer sub-agents in parallel** using the Agent tool. Each reviewer receives:
   - Current draft (`drafts/vN.md`)
   - Abstract (`abstract.md`)
   - Blog creation guide (`references/blog-creation-guide.md`)
   - Their specific rubric (one of `references/reviewer-architect.md`, `references/reviewer-content.md`, `references/reviewer-formatting.md`, `references/reviewer-image.md`)
   - The qualifying summary (embedded in abstract)
   - **Content reviewer only**: also receives the target feature's `knowledge/index.md` (plus any other feature partitions whose products are discussed in the draft) and `/memory/index.md` for fact-checking

   **Sub-agent prompt template** (adapt per reviewer — replace all `<PLACEHOLDERS>`):

   ```
   You are the [Architect/Content/Formatting/Image] reviewer for a Red Hat blog post.

   Review the draft against your rubric and the blog creation guide. Score each dimension 1-10, multiply by its weight, and provide specific line-level feedback with corrections.

   Read these files:
   - Draft: features/<feature>/enablement/blog-<topic-short>/drafts/v<N>.md
   - Abstract: features/<feature>/enablement/blog-<topic-short>/abstract.md
   - Blog creation guide: .claude/skills/blog-create/references/blog-creation-guide.md
   - Your rubric: .claude/skills/blog-create/references/reviewer-<type>.md
   [Content reviewer only:
   - Feature knowledge index(es): features/<feature>/knowledge/index.md (+ any other relevant feature's knowledge/index.md)
   - Hub memory index: /memory/index.md]

   Write your review to: features/<feature>/enablement/blog-<topic-short>/drafts/reviews/v<N>-<type>.md

   Follow the output format specified in your rubric exactly.
   ```

2. **Collect all four reviews** from `drafts/reviews/vN-*.md`

3. **Aggregate scores** per `references/scoring.md`:
   - Architect: 30%, Content: 30%, Formatting: 20%, Image: 20%
   - Check pass criteria: overall >= 8.0, no dimension below 6.0
   - Update `drafts/reviews/score-summary.md`

4. **If passed**: Present to user for approval. Skip to Phase 5 on approval.

5. **If not passed**: Revise the draft:
   - First, read all four review files from the current iteration (`drafts/reviews/vN-architect.md`, `vN-content.md`, `vN-formatting.md`, `vN-image.md`) to understand the full picture
   - Fix any dimension below 6.0 first (blockers)
   - Address lowest-scoring dimension across all agents
   - Resolve conflicting feedback using blog type as tiebreaker
   - Apply quick wins (editorial compliance fixes)
   - Include brief changelog at top of new draft version
   - Write revised draft as `drafts/v(N+1).md` — never overwrite previous versions

6. **Repeat** until pass or checkpoint.

### Iteration controls

- **Max 3 autonomous iterations** before mandatory human checkpoint
- **At checkpoint, user chooses**:
  - **Continue**: 3 more autonomous iterations
  - **Steer**: Provide guidance, then 3 more iterations
  - **Accept**: Override threshold, proceed to finalize
  - **Abandon**: Keep all drafts and reviews, stop
- **Hard ceiling**: 9 iterations (3 checkpoints)
- **Early exit**: If draft passes before checkpoint, present immediately for user approval

### Near-miss rule

If overall >= 7.5 and only one dimension is between 5.0-5.9, flag as "conditional pass" at human checkpoint. User decides whether to accept or iterate.

## Phase 5: Finalize

**Purpose**: Produce submission-ready artifacts and close the loop.

### Sequence

1. **Strip internal changelog** from the passing draft version

2. **Pre-fill blog submission form** template at top of draft:
   - Publication type, byline (defaults to Peter Double — overridable during qualifying), reviewers needed, image checklist, pre-submission checklist

3. **Write `final.md`**: Submission form + clean draft in `features/<feature>/enablement/blog-<topic-short>/final.md`

4. **Generate `seo.md`** in `features/<feature>/enablement/blog-<topic-short>/seo.md`:
   - Meta title (50-60 chars, keywords front-loaded)
   - Meta description (150-160 chars, action-oriented)
   - Primary and secondary keywords
   - Suggested URL slug
   - Internal link suggestions

5. **Generate `index.html`**: Create a branded HTML preview of the blog post.
   - Read the template from `assets/blog-template.html`
   - Read the conversion guide from `references/html-preview-guide.md`
   - Extract metadata from `final.md` (title, subtitle, author, date, product label)
   - Convert the markdown body to HTML following the guide's conversion rules
   - Replace all `{{PLACEHOLDER}}` tokens in the template
   - Render structured image placeholders as actual HTML diagrams when the content describes a table or comparison; otherwise render as placeholder cards
   - Write to `features/<feature>/enablement/blog-<topic-short>/index.html`
   - This step is equivalent to running the `blog-mockup` skill against `final.md` — use that skill directly if you only want the preview without the rest of Finalize

   **This does not make anything public.** The preview HTML sits in the tracked repo like any other enablement artifact, but publishing is a separate, explicit decision — see Publishing below.

6. **Update `drafts/reviews/score-summary.md`** with final status

7. **Offer Google Doc creation** (optional):
   - If yes: create via `mcp__google-workspace__create_doc` with submission form + draft content using `pedouble@redhat.com`
   - If no: skip, local artifacts are complete

8. **Reindex**: Run `python scripts/hub_index.py` (regenerates `features/<feature>/index.md` if anything about the feature changed; safe no-op otherwise — the generated index links to `enablement/` as a whole, it doesn't enumerate individual artifacts, so this step is a formality, not a registration step)

9. **Capture durable side-knowledge**: If qualifying, drafting, or review surfaced anything a colleague would want to find later — a new stakeholder, a positioning decision, a fact the draft depends on — offer `hub.capture` for that one item. This is NOT the place to register the blog post itself as a knowledge entry; the artifact is already discoverable at its `enablement/` path, and there is no per-post registry to update (unlike the old repo's knowledge-registry.md, the hub has no manual index of examples).

10. **Present completion summary**:

```markdown
## Blog Complete: [Title]

### Artifacts
- Abstract: [path]
- Final draft: [path]
- HTML preview: [path]
- SEO metadata: [path]
- Iterations: [N] drafts, [N*4] reviews
- Google Doc: [link] (if created)

### Final Scores
| Agent | Score |
|---|---|
| Architect | [score] |
| Content | [score] |
| Formatting | [score] |
| Image | [score] |
| **Overall** | **[score]** |

### Image Placeholders ([N] total)
[list with descriptions — these need generation/sourcing]

### Next Steps
1. Generate/source images using prompts in the draft
2. Copy to Google Docs (if not already done)
3. Get SME/peer reviews from: [names]
4. Submit through Workfront request form
5. Prepare Employee Advocacy post for promotion
```

## Publishing

Writing `final.md` and `index.html` into the enablement directory does not share or publish anything:

- **The written blog itself** ships through the Red Hat editorial process — Workfront submission, SME/peer review, then redhat.com or developers.redhat.com. That process is external to this repo; this skill's job ends at producing a submission-ready `final.md`.
- **The HTML preview** (`index.html`) is a local visualization aid, not a publication. Treat publishing it to the hub's public site as a real disclosure decision: a preview of an unpublished, unreviewed blog draft becomes world-readable the moment it's added to `publish/manifest.yaml`. Default to NOT publishing it. Only hand off to `hub.publish` if the user explicitly asks to make the preview public (for example, to share a look-and-feel check with a stakeholder) — and even then, confirm that's actually what they want versus just opening the file locally or sharing the Google Doc.
- **Sharing the draft** with reviewers/stakeholders normally means the Google Doc (Phase 5 Step 7) or the Red Hat blog process itself, not a hub-published page.

## Tool Usage Reference

| Task | Tool |
|---|---|
| Fetch Google Docs | `mcp__google-workspace__get_doc_as_markdown` (user: pedouble@redhat.com) |
| Fetch web pages / Red Hat blogs | Playwright (`browser_navigate` + `browser_run_code`) — Red Hat blogs are JS-rendered |
| General web research | Playwright or WebSearch |
| Create Google Doc | `mcp__google-workspace__create_doc` (user: pedouble@redhat.com) |
| Spawn reviewer sub-agents | Agent tool with subagent_type unset (general-purpose) |
| Read/write files | Read, Write, Edit tools |
| Search project files | Glob, Grep tools |
| Publish the HTML preview | `hub.publish` (only on explicit request — see Publishing above) |
| Capture durable side-knowledge | `hub.capture` |
| Create a new feature partition | `hub.file` (when no existing feature fits) |

## Important Reminders

- **Never overwrite drafts** — always create a new version file (v1, v2, v3...)
- **Reviews are also versioned** — `vN-architect.md`, `vN-content.md`, etc.
- **Read `/memory/index.md` and the feature's `knowledge/index.md` fresh** every session — they're living documents
- **Use Playwright, not WebFetch** for Red Hat blog URLs — they require JavaScript rendering
- **Brand standards matter** — reference the Brand Standards Quick Reference in `references/blog-creation-guide.md` for colors, typography, and illustration style
- **The abstract is a contract** — if the draft diverges significantly from the abstract, flag it before continuing
- **Producing a draft is not publishing it** — see Publishing above
