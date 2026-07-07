# Red Hat Blog Creation Guide

A practical guide for the AI BU (OpenShift AI) team to write and publish effective blog posts on the Red Hat blog and Red Hat Developer blog. Combines the official Red Hat editorial process with writing best practices learned from strong examples in the AI space.

---

## Part 1: The Red Hat Blog Process

### Two Blogs, Two Audiences

Red Hat has two primary marketing blogs. Know which one fits your content before you start writing.

| | Red Hat Blog | Red Hat Developer Blog |
|---|---|---|
| **URL** | redhat.com/en/blog | developers.redhat.com/blog |
| **Audience** | IT decision makers, leaders, architects, procurement | Practitioners: developers, SREs, data scientists, platform engineers |
| **Reader's question** | "Can I do that? Why should I do that?" | "How do I do that?" |
| **Tone** | Opinionated thought leadership, strategic insights | Hands-on tutorials, code-level detail |
| **Format** | Problem/solution narratives, industry perspective | Step-by-step walkthroughs, implementation guides |

**Rule of thumb**: If your post explains *why* something matters, it's a Red Hat blog post. If it shows *how* to do it with code, it's a Developer blog post.

### Step-by-Step Process

#### 1. Plan Your Post

- Align with [Red Hat editorial topics and quarterly themes](https://docs.google.com/spreadsheets/d/1BrJb4Bk_fV7nj4Ce3fBck_B5IlQJXRuka4i_44fJ-F4/edit?gid=0#gid=0)
- AI is an "always on" editorial theme — you don't need to wait for a specific quarter
- Coordinate with the [AI BU Team Content calendar](https://docs.google.com/spreadsheets/d/1KwtmhvvkMEJtPSMMnzkZ-YZmxT-VU3snsksFFDcxKNQ/edit?gid=1514415139#gid=1514415139) and [AI BU Editorial Calendar](https://docs.google.com/presentation/d/1IZoz6rE_f7BfuT5Xolo04ffGdAtuAA9A-KszT0BTeD8/edit)
- AI BU marketing contacts: Aom Sinonpat, Carlos Condado, Addie Stevens

#### 2. Complete Prerequisites

Before writing:
- [ ] Complete the [Writing for Red Hat course](https://training-lms.redhat.com/sso/saml/auth/rhlpint?RelayState=deeplinkoffering%3D56373121) (required annually)
- [ ] Review the [Red Hat editorial handbook](https://docs.google.com/document/d/12dfc6LpVbMsRag3NtjvPfPXEX4JBFOf0tbsQYx1iUfM/edit)
- [ ] [Request access to Workfront](https://docs.google.com/forms/d/e/1FAIpQLSe9C4OA4KS0L0db2PcuKxKCFMSqT9g-rTYc3YoBwlBHnjqb-Q/viewform) if you don't have it

#### 3. Write Your Post

Use the [blog template](https://docs.google.com/document/d/1my7gbY0USazBvK_J9RWOKw2xtQj85gkenmR-9uQSWf0/edit) — copy it to the top of your Google Doc draft. The template includes the submission form fields that the editorial team needs.

#### 4. Get Reviews

Before submitting:
- [ ] At least one SME/peer review
- [ ] Review by appropriate product group — check the [blog reviewer list](https://docs.google.com/spreadsheets/d/1BrJb4Bk_fV7nj4Ce3fBck_B5IlQJXRuka4i_44fJ-F4/edit?gid=0#gid=0)
- [ ] If mentioning a customer: approved by [Customer Reference Team](mailto:customer-reference@redhat.com)
- [ ] If mentioning analyst material: approved by [Analyst Relations](https://docs.google.com/document/d/1wO--pIETL0vh26wlFS4jdIdXueYVeQLLB_GDNgbgtFE/edit) (allow 7 days)

#### 5. Submit Through Workfront

- Submit via the [Workfront request form](https://redhat.my.workfront.com/requests/new?activeTab=tab-new-helpRequest&projectID=6512f72900190b3c6aa8beae18734f6e&path=657a0c1000a1772dc84498f277e9d49d)
- Submissions are reviewed by the intake team on **Tuesdays**
- Track progress in the [Workfront dashboard](https://experience.adobe.com/#/@redhat/so:redhat-Production/workfront/dashboard/6581defb002fbdd785a75229bca18ee3/detail)

#### 6. Promote Your Post

- Add to [Employee Advocacy](https://redhat.advocacy.sproutsocial.com/current) (most effective internal promotion)
- Share on LinkedIn and social media
- Use the [Organic Promotion Guide](https://docs.google.com/document/d/159__350WH1pAPbxomGhOZ6QqyeOOCcoxrvP3Q-Q-cYs/edit)

#### 7. Measure Performance

- Check stats at [red.ht/content-toolbox](http://red.ht/content-toolbox) (VPN required)
- You'll receive automated 1-month and 3-month performance reports from Workfront
- KPIs: Google Clicks, Unique Visitors, Opportunity Value, Won Value

---

## Part 2: Writing Powerful Blog Posts

### The Three-Step Outline Method

1. **Write one sentence describing the problem your post solves.** This is your thesis. Example: "How to enforce tool-level authorization for AI agents without rewriting agent code."
2. **Write down the three most important points.** These become your H2 headings. If you have more than three, you probably have enough for a series.
3. **Write two or three paragraphs under each point.** Keep paragraphs short and focused.

Then: write your title at the bottom, and copy-paste the first paragraph under it. You've just established a thesis, SEO-friendly subheadings, and a tight introduction.

### Anatomy of a Strong Red Hat Blog Post

Drawing from high-performing examples in the AI space:

#### Opening: Hook the Reader in the First Paragraph

The opening must answer "what's in it for me?" immediately. Two proven patterns:

**Pattern A — Lead with the tension** (used by Adel Zaalouk):
> "The AI agent world is messy. Teams are reaching for LangChain, LlamaIndex, CrewAI, AutoGen, or building custom solutions from scratch. Good. That's how it should be during the creative phase. But once an agent leaves a developer's laptop..."

This works because it validates the reader's experience, then pivots to the problem.

**Pattern B — Lead with the cost** (used by Christopher Nuland):
> "Every token costs something. Whether it's dollars on a cloud API or watts on your GPU, the question isn't if you should route LLM requests intelligently, but how fast you can start."

This works because it names a pain the reader already feels, then promises a solution.

**What to avoid**: Don't open with company boilerplate, product announcements divorced from reader value, or vague statements about "the future of AI."

#### Structure: Let Headers Tell the Story

Each H2 heading should work as a standalone argument. A reader skimming only the headers should understand the core message.

**Good example** (from the BYOA blog):
- "What Red Hat AI provides"
- "Repurposing cloud-native to agent-native"
- "Making agents safer and ready for production"
- "Governing tool calls at scale"

**For Developer blogs**, use action-oriented step headers:
- "Step 1: Set up your local model"
- "Step 2: Get your cloud API key"
- "Step 3: Write your router config"

#### Technical Depth: Show, Don't Just Tell

- Include architecture diagrams showing system boundaries and data flow
- Use code blocks with real, runnable examples (not pseudocode)
- Include benchmark data or performance numbers when available — readers trust posts backed by evidence
- For the Developer blog: every code block should be copy-pasteable and produce the expected result
- Reference specific CRDs, API endpoints, CLI commands, and config fields

#### Voice and Tone

Red Hat's brand voice is: **open, authentic, helpful, and brave**.

| Do | Don't |
|---|---|
| Write in first person ("I", "we") | Use passive voice ("it was determined") |
| Be direct and opinionated | Hedge everything with "might" and "could" |
| Use concrete language ("Automate any tool across any environment") | Use vague marketing language ("Streamline your tech setup") |
| Admit tradeoffs and limitations honestly | Claim your solution is perfect for everything |
| Use "you" to address the reader directly | Use "one" or "users" abstractly |

**The Red Hat style is**: Clear, concise, conversational, credible, and compelling.

**Use contractions aggressively.** Write "you've", "we're", "it's", "couldn't", "we'll", "that's", "curation's" — the editor converts nearly every formal construction to a contraction. Default to contractions everywhere except when emphasis or formality is needed. If you find yourself writing "It is" or "We are", rewrite to "It's" or "We're".

**Use Oxford commas.** Red Hat editorial uses the serial comma (e.g., "identity, policy, and governance" not "identity, policy and governance"). The editorial team will add them if you omit them.

#### Word Count Guidelines

| Length | Best For | Example |
|---|---|---|
| 500-600 words | Project updates, announcements, news | Quick capability announcement |
| 600-800 words | Regular features, interviews, roundups | Product comparison, FAQ |
| 800-1,300 words | How-tos, tutorials, getting-started guides | Step-by-step with screenshots |
| 1,300-2,000 words | In-depth topic coverage, extensive tutorials | Deep architecture walkthrough |
| 2,000+ words | Break into a multi-part series | Submit each part as a separate Workfront request |

### Formatting Best Practices

#### Document Design
- **Use cascading headings** (H2, H3, H4) — never H1 (reserved for page title)
- **Use H3 for named sub-items** under H2 sections — when listing tiers, categories, or named items, each gets its own H3 heading. Never use bold text as a substitute for heading structure. Bold is for emphasis within a paragraph, not for section titles.
- **Use sentence case** for all titles and headings (only capitalize proper nouns)
- **Expand acronyms on first use** — write "Model Context Protocol (MCP)" on first mention, then "MCP" after. No unexplained acronyms.
- **Break up walls of text** with headings, bullet points, numbered lists, whitespace
- **Bold key terms** and use italics for emphasis — never use underlined text (implies hyperlinks)
- **Lowercase preview/maturity states** — "developer preview", "technical preview", "general availability" are descriptive states, not product names. Don't capitalize them.
- **Limit images to 10 or fewer** — no animated GIFs (accessibility)
- **All images must have alt text** — for Developer blog, also add captions

#### Code Blocks
- Use monospace font for inline code and code blocks — **do not use backticks** (the editorial team has to delete them)
- Format code blocks as monospace text in Google Docs
- Ensure code is real, runnable, and produces the expected output
- Include terminal output separately from commands

#### Tables
- Keep tables simple — used only as actual data tables, not formatting hacks
- Simple formatting renders well in Drupal's CSS

#### Links and References
- Link to Red Hat product pages on first mention
- Use internal links (redhat.com pages) as primary CTAs
- Link to upstream project repos (GitHub) where relevant
- Check links with `site:redhat.com [topic]` to find existing content to link to
- Use [official Red Hat product names](https://docs.google.com/spreadsheets/d/1DLS_lS3VKidgZIvcLmLp9BoiqptkvqHWfe1D5FD2kfk/edit?gid=1987148185#gid=1987148185) — always verify naming

### Calls to Action (CTAs)

Every blog post needs at least one CTA. Blog posts are a content marketing tool — after reading, what should the reader do?

**Good CTA options:**
- Product trial (e.g., [Try Red Hat OpenShift AI](https://www.redhat.com/en/technologies/cloud-computing/openshift/openshift-ai/trial))
- Related webinar or e-book
- Learning path or tutorial
- GitHub repo to try
- Product page for more info

**Placement:**
- Primary CTA: near the top, linked (not bolded — link styling is sufficient visual emphasis)
- Secondary CTA: mid-article, linked
- Closing CTA: in your conclusion

**CTA rules:**
- Primary CTA must link to something in the Red Hat site system
- External links (GitHub, upstream projects) are fine as secondary CTAs
- Never make "visit our booth" the primary CTA for event-related posts

### SEO Essentials

- **Target 1-2 keywords** — integrate naturally, don't stuff
- **Front-load keywords in your headline** — "MCP Gateway security" not "How we thought about security for our MCP Gateway project"
- **Write a meta title** (50-60 characters) and **meta description** (150-160 characters)
- Use the [Metadata Assistant](http://red.ht/content-toolbox) to generate drafts (edit what it produces)
- **Create a custom URL** — Drupal defaults are poor; make it concise with your target keyword

### Series Strategy

If your topic needs more than 2,000 words, plan a series.

**Two approaches:**
1. **Submit all parts together** — editorial team schedules and interlinks them. Best for sequential tutorials or multi-part stories.
2. **Submit individually** — posts are related but independent. Best for concept explorations.

Each post in a series should work as a standalone entry point. Never promise an upcoming post to readers unless it's already scheduled in Drupal.

---

## Part 3: Pre-Submission Checklist

Use this checklist before submitting through Workfront:

### Content Quality
- [ ] Post answers "what's in it for the reader?"
- [ ] Clear thesis/problem statement in the first paragraph
- [ ] Three or fewer main points, each with a strong H2 heading
- [ ] Written in first person, conversational tone
- [ ] No jargon, hyperbole, or unsupported claims
- [ ] Original content (not published elsewhere)
- [ ] All product names match the [Official Product Names List](https://docs.google.com/spreadsheets/d/1DLS_lS3VKidgZIvcLmLp9BoiqptkvqHWfe1D5FD2kfk/edit?gid=1987148185#gid=1987148185)
- [ ] Features/capabilities discussed are at least in tech preview state

### Structure and Formatting
- [ ] Sentence case for all titles and headings
- [ ] Cascading headings (H2 -> H3 -> H4, no H1)
- [ ] Short paragraphs with ample whitespace
- [ ] Code in monospace font (no backticks)
- [ ] 10 or fewer images, all with alt text
- [ ] No animated GIFs
- [ ] All links working and correct

### CTAs and SEO
- [ ] At least one CTA linking to Red Hat site system content
- [ ] Primary CTA near the top, bolded and linked
- [ ] Meta title (50-60 chars) and meta description (150-160 chars) drafted
- [ ] Target keyword(s) in headline and first paragraph
- [ ] Custom URL slug planned (concise, keyword-rich)

### Reviews and Approvals
- [ ] Reviewed by at least one SME/peer
- [ ] Reviewed by relevant product group (see [reviewer list](https://docs.google.com/spreadsheets/d/1BrJb4Bk_fV7nj4Ce3fBck_B5IlQJXRuka4i_44fJ-F4/edit?gid=0#gid=0))
- [ ] Customer mentions approved by Customer Reference Team
- [ ] Analyst material approved by AR team (7-day lead time)
- [ ] Completed [Writing for Red Hat course](https://training-lms.redhat.com/sso/saml/auth/rhlpint?RelayState=deeplinkoffering%3D56373121) within the last year

### Promotion Plan
- [ ] Plan to add to Employee Advocacy after publication
- [ ] LinkedIn / social media post drafted
- [ ] Internal stakeholders notified

---

## Part 4: Blog Examples from the AI BU

### Example 1: Red Hat Blog — Thought Leadership

**"Operationalizing 'Bring Your Own Agent' on Red Hat AI, the OpenClaw edition"**
- Author: Adel Zaalouk (Senior Principal Product Manager)
- URL: https://www.redhat.com/en/blog/operationalizing-bring-your-own-agent-red-hat-ai-openclaw-edition
- Type: Series kickoff / thought leadership

**What makes it effective:**
- **Clear thesis in paragraph 1**: Validates the reader's experience ("messy agent world"), then pivots to the real problem (production readiness gap)
- **Strong conceptual framing**: "BYOA" principle stated early and reinforced throughout — the reader leaves with a memorable mental model
- **Layered technical depth**: Covers identity, sandboxing, policy, observability, gateway, lifecycle — each as a self-contained section that proves the platform story
- **Infrastructure-first security narrative**: "Prompt injection may influence what the agent wants to do. It does not get to change what the platform allows the agent to do." — this kind of crisp, quotable line sticks
- **Series architecture**: Each planned post is self-contained; readers can jump to their current problem
- **Closing with upstream links**: Ties every capability back to open source projects, reinforcing Red Hat's open source credibility

### Example 2: Red Hat Developer Blog — Hands-On Tutorial

**"Getting started with the vLLM Semantic Router project's Athena release"**
- Author: Christopher Nuland (Principal Technical Marketing Manager)
- URL: https://developers.redhat.com/articles/2026/03/25/getting-started-vllm-semantic-router-athena-release
- Type: Getting-started tutorial

**What makes it effective:**
- **Opening hook**: "Every token costs something" — names the cost pain immediately
- **Clear prerequisites section**: Tells the reader exactly what they need before starting
- **Numbered step-by-step flow**: Steps 1-6 are sequential, each building on the last
- **Real config, real code**: Every YAML block and curl command is copy-pasteable and produces real output
- **Benchmark data**: "86% of requests stayed local" — concrete numbers build trust
- **Latency table**: P50/P99 data shows the reader this was actually measured, not hand-waved
- **"Where to go from here" section**: Acknowledges this is the basic config and points to advanced features, inviting the reader to go deeper
- **Clean closing**: Restates the value proposition in one line: "Your tokens are expensive. Manage them strategically."

---

## Reference Links

### Editorial Resources
- [Red Hat Editorial Handbook](https://docs.google.com/document/d/12dfc6LpVbMsRag3NtjvPfPXEX4JBFOf0tbsQYx1iUfM/edit)
- [Blog Template (Make a Copy)](https://docs.google.com/document/d/1my7gbY0USazBvK_J9RWOKw2xtQj85gkenmR-9uQSWf0/edit)
- [12 Blog Article Templates](https://docs.google.com/document/d/1bxDQUIn84XxaX6CMiNzvoHU9-clLSpouiun5q0rzYxE/edit)
- [Red Hat Corporate Style Guide](https://docs.google.com/document/d/1UI2wHjF-9uPEo7Dnt-nugQXuIMQUgTQv_QOUXL1x8zE/edit)
- [Official Product Names List](https://docs.google.com/spreadsheets/d/1DLS_lS3VKidgZIvcLmLp9BoiqptkvqHWfe1D5FD2kfk/edit?gid=1987148185#gid=1987148185)
- [Writing for Red Hat Takeaway Guide](https://docs.google.com/document/d/1tVsQi-Wh3EAdBHOm7QIOhv-vFnkuxDlSBtMybIddIPc/edit)
- [Web Content Optimization Checklist](https://docs.google.com/document/d/1byalHClsyEHAsOUT0kdGfvCiMt9zHuRM_wGt4BLeWdY/edit)
- [Red Hat Brand Standards](https://www.redhat.com/en/about/brand/standards) — see Brand Standards Quick Reference below

### Red Hat Brand Standards — Quick Reference

The official brand standards at https://www.redhat.com/en/about/brand/standards govern all Red Hat visual output. Key sub-pages relevant to blog and HTML/visual asset creation:

| Sub-Page | URL Path | Use For |
|---|---|---|
| **Color** | [/color](https://www.redhat.com/en/about/brand/standards/color) | Full palette: primary, neutrals, extended families |
| **Typography** | [/typography](https://www.redhat.com/en/about/brand/standards/typography) | Red Hat Display, Text, Mono font families and usage |
| **Logo** | [/logo](https://www.redhat.com/en/about/brand/standards/logo) | Logo usage, clear space, do/don't rules |
| **Personality** | [/personality](https://www.redhat.com/en/about/brand/standards/personality) | Brand voice attributes, tone guidance |
| **Standard Icons** | [/icons/standard-icons](https://www.redhat.com/en/about/brand/standards/icons/standard-icons) | General-purpose Red Hat icons |
| **Technology Icons** | [/icons/technology-icons](https://www.redhat.com/en/about/brand/standards/icons/technology-icons) | Product and technology iconography |
| **UI Icons** | [/icons/ui-icons](https://www.redhat.com/en/about/brand/standards/icons/ui-icons) | Interface icons for web/app use |
| **Illustration** | [/illustration](https://www.redhat.com/en/about/brand/standards/illustration) | Illustration style and usage |
| **Photography** | [/photography](https://www.redhat.com/en/about/brand/standards/photography) | Photo selection and treatment |
| **The Hat** | [/the-hat](https://www.redhat.com/en/about/brand/standards/the-hat) | Fedora hat mark usage |
| **Resources** | [/resources](https://www.redhat.com/en/about/brand/standards/resources) | Downloadable assets, templates |

#### Color Palette Summary

**Primary**:
- Red Hat Red: `#EE0000` (primary brand color)
- Dark Red: `#A60000`, `#5F0000`, `#3F0000`
- Light Red: `#F56E6E`, `#F9A8A8`, `#FBC5C5`, `#FCE3E3`, `#FEF0F0`

**Neutrals** (critical for dark UI/diagrams):
- Black/near-black: `#151515`, `#1F1F1F`, `#212427`, `#292929`
- Dark gray: `#383838`, `#4F5255`, `#6A6E73`
- Medium gray: `#8C8C8C`, `#A3A3A3`, `#B8BBBE`
- Light gray: `#C7C7C7`, `#D2D2D2`, `#E0E0E0`, `#F0F0F0`, `#F2F2F2`
- White: `#FFFFFF`

**Extended families** (for data visualization, diagrams, supporting elements):
- Blue: `#003366` / `#004D99` / `#0066CC` (interactive) / `#4394E5` / `#73BCF7` / `#92C5F9` / `#B9DAFC` / `#E0F0FF`
- Teal: `#003333` / `#004D4D` / `#147878` / `#37A3A3` / `#63BDBD` / `#9AD8D8` / `#DAF2F2`
- Purple: `#1B0D33` / `#21134D` / `#3D2785` / `#5E40BE` / `#876FD4` / `#B6A6E9` / `#D0C5F4` / `#ECE6FF`
- Green: `#183301` / `#204D00` / `#3D7317` / `#63993D` / `#87BB62` / `#AFDC8F` / `#D1F1BB` / `#E9F7DF`
- Orange: `#4C1405` / `#731F00` / `#B1380B` / `#F0561D` / `#F4784A` / `#F89B78` / `#FBD5C0`
- Yellow: `#54330B` / `#96640F` / `#B98412` / `#DCA614` / `#FFCC17` / `#FFE072` / `#FFF4CC`

#### Typography Summary

| Font Family | Role | Weights | Google Fonts |
|---|---|---|---|
| **Red Hat Display** | Headings, display text, hero elements | 400, 500, 600, 700, 900 | [Link](https://fonts.google.com/specimen/Red+Hat+Display) |
| **Red Hat Text** | Body copy, UI text, paragraphs | 400, 500, 600, 700 | [Link](https://fonts.google.com/specimen/Red+Hat+Text) |
| **Red Hat Mono** | Code, technical content, terminal output | 400, 500, 600 | [Link](https://fonts.google.com/specimen/Red+Hat+Mono) |

All three are open source and available on Google Fonts. For HTML assets, use the Google Fonts import:
```html
<link href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@400;500;600;700;900&family=Red+Hat+Text:wght@400;500;600;700&family=Red+Hat+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

### Submission and Tracking
- [Workfront Request Form](https://redhat.my.workfront.com/requests/new?activeTab=tab-new-helpRequest&projectID=6512f72900190b3c6aa8beae18734f6e&path=657a0c1000a1772dc84498f277e9d49d)
- [Workfront Access Request](https://docs.google.com/forms/d/e/1FAIpQLSe9C4OA4KS0L0db2PcuKxKCFMSqT9g-rTYc3YoBwlBHnjqb-Q/viewform)
- [Publishing Schedule Dashboard](https://experience.adobe.com/#/@redhat/so:redhat-Production/workfront/dashboard/6581defb002fbdd785a75229bca18ee3/detail)
- [Blog Reviewer List](https://docs.google.com/spreadsheets/d/1BrJb4Bk_fV7nj4Ce3fBck_B5IlQJXRuka4i_44fJ-F4/edit?gid=0#gid=0)

### AI BU Specific
- [AI BU Team Content Calendar](https://docs.google.com/spreadsheets/d/1KwtmhvvkMEJtPSMMnzkZ-YZmxT-VU3snsksFFDcxKNQ/edit?gid=1514415139#gid=1514415139)
- [AI BU Editorial Calendar](https://docs.google.com/presentation/d/1IZoz6rE_f7BfuT5Xolo04ffGdAtuAA9A-KszT0BTeD8/edit)
- [Red Hat AI Blog Channel](https://www.redhat.com/en/blog/channel/red-hat-ai)
- [Red Hat AI Blog (RHOAI filtered)](https://www.redhat.com/en/blog/channel/red-hat-ai?f[0]=taxonomy_topic_tid:75501&f[1]=taxonomy_product_tid:80251)

### Promotion and Measurement
- [Employee Advocacy](https://redhat.advocacy.sproutsocial.com/current)
- [Organic Promotion Guide](https://docs.google.com/document/d/159__350WH1pAPbxomGhOZ6QqyeOOCcoxrvP3Q-Q-cYs/edit)
- [Content Toolbox / Data Explorer](http://red.ht/content-toolbox)
- [Red Hat Blog Health Check](https://docs.google.com/spreadsheets/d/1zhoBWL8dd7vq_x6bwj30V086tRm4gt6H30q9ypgJuTs/edit?gid=920737092#gid=920737092)
- [Blog Contributors Slack Channel](https://redhat.enterprise.slack.com/archives/C06A5CPTNCR)
- Editorial team email: editorial-team@redhat.com
