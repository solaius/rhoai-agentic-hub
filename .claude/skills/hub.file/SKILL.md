---
name: hub.file
description: Intake an external source (Google Doc, PDF, URL, GitHub repo, meeting transcript) as a typed knowledge entry in the right feature partition - creating the partition on first use. Successor to add-knowledge-source. Use when the user says "add this doc", "file this source", "add this transcript", or shares a link to incorporate.
---

# hub.file

Input: the source (URL or file) + whatever context the user gave.

1. Pick the feature: read features/features.yaml. If nothing fits, propose a
   new partition (id, title, one-line description); on approval append it to
   features.yaml and create ONLY the subdirectories this filing needs — never
   all five empty (see /conventions/layout.md).
2. Normalize the resource URI per /conventions/uris.md (strip /edit suffixes,
   query params, fragments).
3. Write features/<f>/knowledge/ref-<slug>.md:
   type: reference · title · description (one line, written for someone
   deciding whether to open it) · resource · tags · timestamp: today.
   Body (3-6 lines): why it matters, what's inside, what to read first.
4. Transcripts: raw file → features/<f>/work/transcripts/ (gitignored); the
   ref- entry points at the source system. Decisions/questions the user
   confirms from it become additional decision-/question- entries.
5. NDA-adjacent → restricted/features/<f>/knowledge/ (same shapes).
6. `python scripts/hub_index.py` && `python scripts/hub_lint.py` (0 errors).
7. Commit: `git add -A && git commit -m "know(<f>): file <slug>"` && `git push`.
