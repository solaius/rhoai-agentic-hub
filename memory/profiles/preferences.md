---
type: profile
description: "Preferences: inline gates, no lift-and-shift, spec-first, Windows + Git Bash"
timestamp: 2026-07-05
status: current
valid_from: 2026-07-05
---
- Memory/publishing writes go through inline approve → direct commit gates;
  every promotion gets an explicit public-vs-restricted call.
- Skill migrations are review/optimize/enhance passes — never lift-and-shift.
- Workflow: brainstorm → spec → plan → build, with section-by-section approvals.
- Environment: Windows 11, Git Bash for scripts, `python` (not python3),
  multiple machines (repo must bootstrap via hub.doctor).
- Present design content as plain text (no trailing tool calls) so it renders.
- No LLM-provider credential handling anywhere in the hub — users arrive
  with Claude Code/Cursor already configured; `restricted/.env` never
  carries such keys, and the doctor neither excludes, checks, nor writes
  them (don't port the old repo-doctor's `unset` machinery back in).

## History
- 2026-07-08 — Added the no-LLM-credential-handling rule (owner ruling; the
  exclusion machinery briefly ported with R4 wave 4 was removed same day).
- 2026-07-05 — **Creation** at hub seed, from the design-brainstorm session.
