---
type: fact
description: Operational gotchas hit while building this hub — gh secret set silent-empty-secret, GitHub Pages first-build wedge, PAT-in-argv leak
timestamp: 2026-07-06
status: current
source: old repo memory rhoai-agentic-hub-effort.md (originSessionId b1b3529d-fecf-4f61-9547-2b2d8441c8e7), migrated 2026-07-06
---
Extracted from the old repo's build-tracking memory (the rest of that file is superseded by this hub's own `memory/profiles/now.md`, which tracks current state more accurately — see the R2 batch 4 MANIFEST for the full disposition).

Three gotchas worth keeping: (1) `gh secret set` run via non-interactive passthrough stored an EMPTY secret once — set PATs from a real terminal, not piped. (2) The first GitHub Pages build can wedge in "building" state — `gh api -X POST repos/<pages-repo>/pages/builds` unwedges it. (3) A PAT pasted as a command argument leaked (visible in argv) and had to be revoked/re-issued — token values must never appear in argv.
