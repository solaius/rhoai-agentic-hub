---
name: hub.enhance
description: Create, start, complete, or reprioritize hub enhancement items -- the bridge between enhancements.md (narrative) and GitHub issues (actionable tracking). Use when the user says "new enhancement", "add an enhancement", "I have an idea for the hub", "start #N", "work on #N", "build #N", "pick up #N", "complete enhancement #N", "close enhancement #N", "move #N to next/later/someday", "promote #N", "demote #N", or when an improvement idea for the hub itself surfaces mid-session. Also use when the user says "enhance", "backlog item", "hub improvement", or references enhancements.md. Every write is gated.
---

# hub.enhance

The hub tracks its own improvements in two linked systems: `docs/enhancements.md`
(the strategic narrative -- why things matter) and GitHub issues (the actionable
detail -- scope, acceptance criteria, starting points). This skill keeps them
in sync.

Input: an action (create, start, complete, or reprioritize) plus the
enhancement details, from the user's words or session context.

## Actions

Determine which action the user needs:

- **create** -- a new enhancement idea. Go to step 1.
- **start** -- begin working on an enhancement. Go to step 9.
- **complete** -- an enhancement is done. Go to step 5.
- **reprioritize** -- move an enhancement between tiers. Go to step 7.

---

## Create (steps 1-4)

### 1. Classify

Determine the enhancement's priority tier and theme labels by reading the
current `docs/enhancements.md` for context on what's already tracked.

**Priority** (mutually exclusive):
| Label | Meaning |
|---|---|
| `priority: next` | Active candidate, ready to pick up |
| `priority: later` | Data-gated or low urgency |
| _(no issue)_ | Someday -- too speculative for an issue; doc-only |

**Themes** (non-exclusive, pick all that apply -- only for Next/Later items):
| Label | Meaning |
|---|---|
| `theme: integration` | Integrating external tools/repos |
| `theme: infrastructure` | Doctor, cross-machine, env tooling |
| `theme: content` | Publishing, narrative, FAQ |
| `theme: tooling` | Agent context, search, logging, scripts |
| `theme: process` | Slack sweep, JTBD mining, multi-writer |

If the idea seems too speculative for an issue, confirm with the user
before classifying as Someday.

### 2. Draft the GitHub issue body

Skip this step for Someday items (no issue).

Write the issue body following this structure -- optimized for both human
and AI agent pickup (scope prevents drift, acceptance criteria give a
verifiable "done" signal, starting points eliminate the "where do I begin"
problem):

```
[What this is and why it matters -- context needed to understand
the problem before acting]

### Scope
- [Concrete deliverables, bulleted]
- [What's NOT in scope, if ambiguous]

### Acceptance criteria
- [ ] [Verifiable checkpoint -- something you can test/confirm]
- [ ] [Another one]

### Starting points
- `path/to/relevant/file` -- [why it matters]
- [Link to related issue/spec if relevant]
```

### 3. Draft the narrative paragraph

Write a 2-3 sentence paragraph explaining *why* this matters and what it
connects to strategically. This is NOT the issue body -- it's the strategic
framing that gives the backlog its story. Match the voice and density of
existing entries in enhancements.md.

### 4. Gate and execute

Show the user:
```
enhance → create
  priority: <tier>
  themes: <labels>
  title: <title>
  issue body: <first sentence of body, or "(someday -- no issue)">
  narrative: <the 2-3 sentence entry>
```

Wait for OK.

On OK:

  **For Next/Later items:**
  a. Create the GitHub issue FIRST to get the real number:
     `gh issue create --title "<title>" --label "enhancement"
     --label "<priority>" --label "<theme>" ... --body "<body>"`
     Parse the issue number and URL from the command output.
  b. Write the narrative entry to `docs/enhancements.md` in the correct
     tier section using the real issue number and URL:
     `**[#N Title](https://github.com/solaius/rhoai-agentic-hub/issues/N).** Narrative.`
  c. Update the `Last groomed` date in the enhancements.md header to today.
  d. Commit: `git add docs/enhancements.md` then
     `git commit -m "docs(enhancements): add #N <short title>" -- docs/enhancements.md`
  e. Push (the issue is already remote; the doc should match):
     `git push`

  **For Someday items:**
  a. Write the entry to the Someday section of `docs/enhancements.md`
     without a link: `**<Title>.** Narrative.`
  b. Update the `Last groomed` date in the enhancements.md header to today.
  c. Commit: `git add docs/enhancements.md` then
     `git commit -m "docs(enhancements): add someday item <short title>" -- docs/enhancements.md`
  d. Push: `git push`

On reject: discard everything, no writes.

---

## Complete (steps 5-6)

### 5. Gather completion info

Read `docs/enhancements.md` and identify the item by its issue number.
Ask the user for:
- A short outcome summary (what was delivered)
- Link to spec/plan if one exists
- Confirm the issue should be closed

If the user provides this information upfront (e.g. "close #1, we shipped
it, spec at docs/specs/..."), skip the questions and proceed to the gate.

### 6. Gate and execute

Show the user:
```
enhance → complete #N <title>
  outcome: <summary>
  closes: github issue #N
  moves to: docs/enhancements-complete.md under ## YYYY-MM-DD
```

Wait for OK.

On OK:
  a. Remove the entry from `docs/enhancements.md`.
  b. Update the `Last groomed` date in the enhancements.md header to today.
  c. Add a completion entry to `docs/enhancements-complete.md` under
     today's `## YYYY-MM-DD` heading. If no heading for today exists,
     create it at the TOP of the completed items (before the most recent
     existing date heading). Match the existing format:
     `**#N <Title>.** <Outcome summary> ([/docs/specs/<spec>](/docs/specs/<spec>)).`
  d. Close the GitHub issue: `gh issue close <N>`
  e. Commit with explicit paths:
     `git add docs/enhancements.md docs/enhancements-complete.md` then
     `git commit -m "docs(enhancements): complete #N <short title>" -- docs/enhancements.md docs/enhancements-complete.md`
  f. Push: `git push`

On reject: discard everything.

---

## Reprioritize (steps 7-8)

### 7. Determine the move

Read `docs/enhancements.md` and identify the item. Determine the target
tier (Next, Later, or Someday).

Moves that cross the issue boundary require extra work:
- **To Someday**: close the GitHub issue (too speculative for tracking),
  rewrite the entry to remove the issue link.
- **From Someday to Next/Later**: create a GitHub issue first (follow
  steps 2-3 to draft the body and narrative), then write the entry with
  the real issue number.
- **Between Next and Later**: swap the priority label, move the entry.

### 8. Gate and execute

Show the user:
```
enhance → reprioritize #N <title>
  from: <current tier>
  to: <target tier>
  issue: <close|create|update labels>
```

Wait for OK.

On OK:
  a. Move the entry to the target section in `docs/enhancements.md`.
  b. Handle the GitHub issue:
     - Next ↔ Later: `gh issue edit <N> --remove-label "<old priority>"
       --add-label "<new priority>"`
     - → Someday: `gh issue close <N>`, remove issue link from entry.
     - Someday →: create the issue (step 4a of create flow), rewrite
       entry with the real issue number and URL.
  c. Update the `Last groomed` date in the enhancements.md header to today.
  d. Commit: `git add docs/enhancements.md` then
     `git commit -m "docs(enhancements): reprioritize #N <short title> → <tier>" -- docs/enhancements.md`
  e. Push: `git push`

On reject: discard everything.

---

## Start (steps 9-10)

### 9. Load the enhancement context

Fetch the GitHub issue to get the full context the brainstorming skill
needs:
  `gh issue view <N> --json title,body,labels`

Read `docs/enhancements.md` for the narrative entry -- this gives the
strategic framing that the issue body alone may not convey.

### 10. Hand off to brainstorming

Invoke the `superpowers:brainstorming` skill with the enhancement context
pre-loaded. Frame the handoff so brainstorming has everything it needs
without the user re-explaining:

> Starting work on enhancement #N: **<title>**
>
> **Strategic context** (from enhancements.md):
> <the narrative paragraph>
>
> **Scope and acceptance criteria** (from the GitHub issue):
> <the issue body>

The brainstorming skill takes over from here. Its output flows into the
standard pipeline (spec -> plan -> implement). Hub.enhance is not involved
again until the work is complete (use the **complete** action then).
