---
name: hub.file
description: Intake an external source (Google Doc, PDF, URL, GitHub repo, meeting transcript) as a typed knowledge entry in the right feature partition - creating the partition on first use. Successor to add-knowledge-source. Use when the user says "add this doc", "file this source", "add this transcript", or shares a link to incorporate.
---

# hub.file

Input: the source (URL or file) + whatever context the user gave.

1. Pick the home: story-shaped sources (pillars, cross-feature narrative,
   strategy-spine material) → narrative/knowledge/. Otherwise pick the
   feature: read features/features.yaml. If nothing fits, propose a
   new partition (id, title, one-line description); on approval append it to
   features.yaml and create ONLY the subdirectories this filing needs — never
   all five empty (see /conventions/layout.md). Multi-feature sources keep a
   primary home and declare `features:` cross-refs.
2. Normalize the resource URI per /conventions/uris.md (strip /edit suffixes,
   query params, fragments).
3. Write features/<f>/knowledge/ref-<slug>.md — or
   narrative/knowledge/ref-<slug>.md when step 1 routed to narrative/:
   type: reference · title · description (one line, written for someone
   deciding whether to open it) · resource · tags · timestamp: today.
   Body (3-6 lines): why it matters, what's inside, what to read first.
4. Transcripts: raw file → features/<f>/work/transcripts/ (or
   narrative/work/transcripts/; both gitignored); the
   ref- entry points at the source system. Decisions/questions the user
   confirms from it become additional decision-/question- entries.
5. NDA-adjacent → the restricted/ mirror of the chosen home —
   restricted/features/<f>/knowledge/ or restricted/narrative/knowledge/
   (same shapes).
6. DISCLOSURE CONFIRM: show one line — file → <path>: <description>
   [public|restricted] — and wait for OK (this repo is public).
7. `python scripts/hub_index.py` && `python scripts/hub_lint.py` (0 errors).
8. Commit: stage the filed entry (+ features.yaml if a partition was
   created) plus regenerated indexes/views explicitly, NEVER `git add -A`
   (shared checkout, see fact-concurrent-session-git-hygiene); check
   `git diff --cached --stat`, then
   `git commit -m "know(<f>): file <slug>"` && `git push`.
