# Qualifying Questions Framework

This reference defines the question flow for Phase 1 (Qualify). Questions are asked one at a time, adapting based on prior answers. The goal is to gather enough context to write a strong abstract — no more, no less.

## Question Flow

Ask these questions conversationally, one per message. Adapt based on answers — skip questions that have already been answered by prior context or source material.

### Q1: Blog Type

**Ask**: "Is this for the Red Hat Blog or the Red Hat Developer Blog? Or not sure?"

| Answer | Next action |
|---|---|
| Red Hat Blog | Note: thought leadership tone, IT decision-maker audience |
| Developer Blog | Note: hands-on tutorial tone, practitioner audience |
| Not sure | Ask them to describe the content briefly; recommend based on: if it explains *why* → Red Hat Blog; if it shows *how* with code → Developer Blog |

### Q2: Core Thesis

**Ask**: "What single problem does this post solve for the reader? Try to say it in one sentence."

**Why this matters**: This becomes the first paragraph's anchor. If the user can't state it in one sentence, the blog probably covers too much ground — help them narrow it down or consider a series.

**If they struggle**: Offer framing prompts:
- "After reading this post, the reader will be able to..."
- "The problem this post addresses is..."
- "If I had to tweet the value of this post, I'd say..."

### Q3: Target Audience

**Ask**: "Who is the primary reader?" Offer choices:
- IT decision makers / architects
- Platform engineers / SREs
- Application developers
- Data scientists / ML engineers
- Security/compliance teams
- Other (describe)

**Adaptive follow-ups**:
- If Developer Blog: "What prerequisites should the reader have? What runtime environment will they need?"
- If Red Hat Blog: "What business context or strategic framing should we set up? Are there market trends or competitive pressures to reference?"

### Q4: Products and Projects

**Ask**: "Which Red Hat products or open source projects are involved?"

**Validation**: Cross-reference against the [Official Product Names List](https://docs.google.com/spreadsheets/d/1DLS_lS3VKidgZIvcLmLp9BoiqptkvqHWfe1D5FD2kfk/edit?gid=1987148185#gid=1987148185) and the target feature's `knowledge/index.md` (plus `/memory/index.md` for current-state facts like roadmap dates). Use official names only.

**Feature routing**: Based on products/topics, propose a feature from `features/features.yaml`:

| Products/Topics | Suggested Feature |
|---|---|
| MCP servers, lifecycle, governance, data model, Lifecycle Operator | `mcp-registry` |
| Runtime MCP traffic policy, Envoy/RHCL gateway, entitlements | `mcp-gateway` |
| MCP server building, partner/community catalog, ecosystem tooling | `mcp-ecosystem` |
| Agent registry, agent catalog/starter kits, agentic base images, Kagenti | `agent-registry` |
| Skills registry, upstream MLflow collaboration, plugin marketplace | `skills-registry` |
| Agent memory/knowledge, Feast/MemoryHub/OGX proposals | `agent-memory` |
| Agent operations, observability, SDLC oversight, AgentOps | `agent-ops` |
| Prompt/agent iteration studio, playground UX | `gen-ai-studio` |
| Cross-cutting AI Gateway, AI Hub UI, org-wide strategy, industry perspective, or anything spanning multiple products | `platform` |

Present the proposed feature and topic-short slug for user confirmation: "I'd suggest filing this under `features/mcp-gateway/enablement/blog-mcp-gateway-openclaw/`. Does that work, or would you prefer a different feature?"

If no existing feature fits, don't invent one — hand off to `hub.file` (it creates new feature partitions in `features/features.yaml`), then resume once it exists.

### Q5: Source Material

**Ask**: "What source material do you have?"

| Answer | Action |
|---|---|
| "I have a draft/notes" | Ask for content or Google Doc link. Fetch via Google Workspace MCP or read from provided path. |
| "I have reference docs" | Ask for links/IDs. Fetch each. |
| "Start from scratch" | Note: will rely on the feature's `knowledge/` and `research/`, `/memory/`, and web research. |

**In all cases**: Offer to scan related material automatically: "I can also scan this feature's `knowledge/` and `research/` directories for related material on [topic]. Want me to do that?"

**For Google Doc links**: Extract the Doc ID from the URL and use `mcp__google-workspace__get_doc_as_markdown`.

### Q6: Demo or Code Component

**Ask**: "Does this post include a demo, code walkthrough, or hands-on component?"

| Answer | Follow-up |
|---|---|
| Yes | "What language/framework? What environment does the reader need? Any prerequisites to install?" |
| No | Skip — move to Q7 |

### Q7: Series Context

**Ask**: "Is this a standalone post or part of a series?"

| Answer | Follow-up |
|---|---|
| Part of a series | "Which part? Are there links to prior posts? What does each part cover?" |
| Standalone | Skip — move to Q8 |

### Q8: Call to Action

**Ask**: "What should the reader do after reading? What's the primary CTA?"

**Suggest options** based on products mentioned:
- Try [Product] (link to trial page)
- Explore the [GitHub repo]
- Read the [related doc/guide]
- Watch the [webinar/demo]
- Join the [community/Slack]

Remind: "The primary CTA should link to something on redhat.com — GitHub repos and upstream projects work great as secondary CTAs."

### Q9: Timing and Events

**Ask**: "Is this tied to a specific event, release, or date?"

| Answer | Follow-up |
|---|---|
| Yes | "Which event/release? What's the target publication date? Any embargo considerations?" |
| No | Skip — qualifying complete |

## Brief Mode

If the user provides a dense one-paragraph brief that already covers most qualifying answers (e.g., "Red Hat Blog about MCP Gateway security for platform engineers, thesis is how to enforce tool-level auth without rewriting agent code, products are MCP Gateway and OpenShift AI, standalone, no demo, CTA is try RHOAI"), extract all answers from the brief and present the qualifying summary for confirmation. Only ask about genuinely missing information — don't re-ask questions the brief already answered.

This respects experienced users who know what they want and don't need to be walked through 9 sequential questions.

## Shortcut Path

When the user provides a Google Doc link or substantial content upfront:

1. **Fetch and analyze** the content
2. **Auto-fill** extractable answers:
   - Thesis: infer from intro/abstract
   - Products: extract product mentions
   - Audience: infer from tone and depth
   - Blog type: infer from format (tutorial vs thought leadership)
   - CTA: check for existing calls to action
   - Series: check for series references
3. **Present findings**: "Based on your doc, here's what I've gathered..."
4. **Only ask about gaps** — skip questions that have clear answers from the source

## Existing Draft Review Mode

When reviewing an existing draft (not creating from scratch):

1. Read the draft in full
2. Infer: blog type, thesis, audience, products, structure
3. Present inferences to user for confirmation
4. Ask only about: CTA (if not clear), series context (if not clear), and feature (infer from the draft's existing path if it already lives under a `features/<feature>/enablement/` directory; otherwise ask, same as Q4)
5. Proceed with shortened qualifying summary

## Exit Condition

Present the qualifying summary for user confirmation:

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

User must confirm before proceeding to Phase 2 (Abstract).
