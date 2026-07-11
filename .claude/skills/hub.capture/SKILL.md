---
name: hub.capture
description: Capture one durable item (decision, date/status change, preference, feedback, link) into the hub's memory or knowledge store the moment it surfaces mid-session. Use when the user says "capture this", "remember this", "note that down", or when a durable fact surfaces that future sessions will need. Gated - one-line inline confirm, then direct commit.
---

# hub.capture

Input: the item, from the user's words or session context.

1. Classify with the boundary rule (/conventions/memory.md): working context
   (state, preference, feedback, process fact) → memory store; domain
   knowledge (a colleague would look it up) → features/<f>/knowledge/;
   story-shaped (pillar, cross-feature narrative — wrong under any single
   feature) → narrative/knowledge/; a field question someone asked us →
   qa- entry (dedupe rule in step 2); a user job for UX/Docs → jtbd- entry
   (persona from the locked list, evidence: links); NDA-adjacent → the
   restricted/ mirror of the same location. Entries touching multiple
   features declare `features: [ids]`.
2. Determine the write:
   - Profile-shaped (roadmap/strategy/status/preference change): EDIT the
     profile in place — new current value, prepend the old value to
     `## History` with date + source, bump `timestamp` and `valid_from`.
   - Atomic: NEW file — `memory/facts/fact-<slug>.md`,
     `features/<f>/knowledge/<prefix><slug>.md`, or — story-shaped —
     `narrative/knowledge/<prefix><slug>.md`, frontmatter per
     /conventions/type-vocabulary.md.
   - Knowledge entries: first check the feature partition exists in
     features/features.yaml; if it doesn't → hand off to hub.file (it
     creates partitions).
   - qa entries: BEFORE creating, grep existing `qa-*` for the same
     question; on a match, append a dated item to its `asks:` list
     (`by:` role bucket) and refresh the answer if knowledge moved —
     never a duplicate entry. A pasted Slack permalink goes in `source:`.
     Asker identity (customer/partner name, deal context) → the restricted
     sibling; the public entry keeps only the role bucket.
3. Show ONE line: `capture → <path>: <description> [public|restricted]`
   (full content on request). Wait for the user's OK.
4. On OK:
   a. Write the file / apply the profile edit.
   b. Append to memory/log.md under today's `## YYYY-MM-DD` heading (create
      it at the TOP of the body if absent): `- **Creation|Update** — <one line>`.
   c. Run `python scripts/hub_index.py`.
   d. Run `python scripts/hub_lint.py` — 0 errors required; fix the captured
      file (not the scripts) if it reports errors.
   e. Commit with explicit paths, NEVER `git add -A` (the checkout is
      shared across concurrent sessions; a sweep commits their in-flight
      files, see memory/facts/fact-concurrent-session-git-hygiene.md):
      `git add <files written/edited in 4a/4b> memory/index.md
      features/index.md "features/*/index.md"
      "features/*/knowledge/index.md" narrative/index.md
      narrative/knowledge/index.md views/`, check
      `git diff --cached --stat` for anything this capture did not write,
      then `git commit -m "mem: capture <slug>"`.
      (Restricted files are gitignored and won't be staged — correct.)
5. On reject: discard everything, no writes.

Note: captures reach the remote at the next consolidate/file/publish push —
push explicitly if another machine needs them sooner.

A capture takes seconds. Do not expand it into a conversation.
