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

## History
- 2026-07-05 — **Creation** at hub seed, from the design-brainstorm session.
