---
name: hub.intake
description: Guided multi-source intake — onboard a new feature area or bulk-add sources to an existing one. Accepts a topic plus any pile of sources (URLs, Google Docs, Slack permalinks, Jira/RFE links, transcripts, pasted notes), routes to a home, files ref- entries, extracts typed entries through a batch gate, and offers a hub.research kickoff. Use when the user says "add a new feature <x>", "onboard <topic>", "intake these", "here's everything on <topic>", or drops multiple sources at once. A single source → hub.file is the faster path.
---

# hub.intake

Input: topic + sources (URLs, GDocs, Slack permalinks, Jira/RFE links,
transcript files, pasted text) from the prompt. Ask ONCE, upfront, for
anything obviously missing (no topic, or no sources and no facts to
file) — then run the flow without further questions until the gate.

1. ROUTE HOME: match the topic against features/features.yaml;
   story-shaped (pillar/cross-feature narrative) → narrative/. No fit →
   propose a new partition (id, title, one-line description) per
   hub.file step 1; the features.yaml append and subdirectory creation
   (ONLY what this intake needs) ride the step-4 gate with every other
   write — there is no separate partition-approval moment. A NEW partition also gets a
   starter knowledge/fact-<id>-overview.md (what it is, current status,
   key links) built from the user's basic info. RHOAI-feature overviews
   link the RHOAI architecture repo
   (/features/platform/knowledge/ref-opendatahub-architecture-context-repo.md)
   under key links.
2. FILE SOURCES: each source per hub.file steps 2-5 — canonical URI
   (/conventions/uris.md), ref- entry with a load-bearing one-line
   description, transcripts → <home>/work/transcripts/ (gitignored) with
   a tracked ref- pointing at the source system, NDA-adjacent →
   restricted/ mirror. Jira/RFE links: ref- entry with the URL only
   (field ingestion arrives with the Jira hub skills, backlog #2).
   Unreachable source (paywall, auth, dead link): still draft the ref-
   (the pointer is real knowledge), mark its gate line `fetch failed`.
   MCP down → say so, offer pasted content, point at hub.doctor check.
3. EXTRACT: read the fetchable sources; draft typed entries for what is
   inside — fact-, decision-, question-, person-, qa- (dedupe per
   hub.capture step 2 — recurrence appends to asks:, never duplicates).
   Multi-feature material keeps the primary home and declares
   `features: [ids]`. Draft in the session/scratchpad — no repo writes
   before the gate.
4. BATCH GATE: one table — every proposed write, one line:
   `path: description [public|restricted] [new|update]`. Full content on
   request. Approve/edit/reject per line; nothing touches the repo
   before OK. Customer names/deal context → restricted/ sibling; dollar
   figures and agreement language never go to tracked files.
5. On OK: write the approved files, run `python scripts/hub_index.py`,
   then `python scripts/hub_lint.py` (0 errors — fix the written
   content, not the scripts). Commit:
   `git add -A && git commit -m "intake(<home>): <topic>"` && `git push`.
6. OFFER RESEARCH: suggest `hub.research <home>` with a lens set fitted
   to what intake revealed (unknown competitive space → competitive;
   heavy technical sources → architecture + upstream; scoping gaps →
   requirements). Never auto-run.
