---
name: hub.capture
description: Capture one durable item (decision, date/status change, preference, feedback, link) into the hub's memory or knowledge store the moment it surfaces mid-session. Use when the user says "capture this", "remember this", "note that down", or when a durable fact surfaces that future sessions will need. Gated - one-line inline confirm, then direct commit.
---

# hub.capture

Input: the item, from the user's words or session context.

1. Classify with the boundary rule (/conventions/memory.md): working context
   (state, preference, feedback, process fact) → memory store; domain
   knowledge (a colleague would look it up) → features/<f>/knowledge/;
   NDA-adjacent → the restricted/ mirror of the same location.
2. Determine the write:
   - Profile-shaped (roadmap/strategy/status/preference change): EDIT the
     profile in place — new current value, prepend the old value to
     `## History` with date + source, bump `timestamp` and `valid_from`.
   - Atomic: NEW file — `memory/facts/fact-<slug>.md` or
     `features/<f>/knowledge/<prefix><slug>.md`, frontmatter per
     /conventions/type-vocabulary.md.
   - Knowledge entry whose feature partition doesn't exist yet → hand off to
     hub.file (it creates partitions).
3. Show ONE line: `capture → <path>: <description> [public|restricted]`
   (full content on request). Wait for the user's OK.
4. On OK:
   a. Write the file / apply the profile edit.
   b. Append to memory/log.md under today's `## YYYY-MM-DD` heading (create
      it at the TOP of the body if absent): `- **Creation|Update** — <one line>`.
   c. Run `python scripts/hub_index.py`.
   d. Commit: `git add -A && git commit -m "mem: capture <slug>"`.
      (Restricted files are gitignored and won't be staged — correct.)
5. On reject: discard everything, no writes.

A capture takes seconds. Do not expand it into a conversation.
