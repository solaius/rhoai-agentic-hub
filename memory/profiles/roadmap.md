---
type: profile
description: "Roadmap: MCP Registry targets RHOAI 3.5 Dev Preview; full RHOAI/MCP release train through GA"
timestamp: 2026-07-06
status: current
valid_from: 2026-07-06
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §6 (as of 2026-07-05)
---
- **RHOAI 3.5** — MCP Registry Dev Preview; Agent registries; MCP Gateway deployment in RHOAI; hardening, registry integration, gateway configuration.
- **RHOAI GA** — end of CY26 target. Full GA of the MCP ecosystem.
- **OCP 5.0** — future. MCP Servers + MCP Gateway included.
- Related Jira: RHAIRFE-1370 (main), RHAIRFE-1457 (gateway in RHOAI), RHAIRFE-1456 (lifecycle operator in RHOAI).

**Staleness flag**: no fresh 3.5 dates were provided as of this update (2026-07-06). RHOAI 3.4's Apr 10, 2026 code-freeze date has already passed (see History) with its ship status not reconfirmed this pass — treat the targets above as last-known, not verified current.

## History
- 2026-07-06 — **Update** — resolved label conflict: monolith §6 named the RHOAI 3.5 row "(TP target)" while describing its content as "MCP Registry Dev Preview" — resolved to Dev Preview per owner ruling, matching this hub's established 3.5 = Dev Preview framing (CLAUDE.md; this profile's own prior value). (source: R2 batch 3 apply — owner ruling)
- 2026-07-06 — **Update** — relegated completed/passed milestones out of the active body: "RHOAI 3.0 GA — Nov 2025. Baseline release." (completed — GA shipped) and "RHOAI 3.4 DP — Apr 10, 2026 code freeze. MCP Catalog DP (5 partner + 2 community MCPs), MCP Guardrail DP, Summit demo, Kubeflow GA." (code-freeze date passed as of this update; presumably shipped, not reconfirmed this pass — see staleness flag above). (source: R2 batch 3 apply — profile finalization, body carries current/future only)
- 2026-07-06 — **Update** — superseded: "MCP Registry: RHOAI 3.5 Dev Preview target. Related Jira: RHAIRFE-1370 (main), RHAIRFE-1457 (gateway in RHOAI), RHAIRFE-1456 (lifecycle operator in RHOAI). Full release timeline: seeded from the monolith at M3 (see plan runbooks)." (source: R2 batch 3 — full release timeline merged in from knowledge-registry.md §6)
- 2026-07-05 — **Creation** at hub seed; values carried from old repo.
