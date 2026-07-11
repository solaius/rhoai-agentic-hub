---
type: profile
description: "Roadmap: MCP Registry DP misses 3.5 stable; Catalog TP + Registry TP + integration push to RHOAI 3.6 EA1; full RHOAI/MCP release train through GA"
timestamp: 2026-07-11
status: current
valid_from: 2026-07-11
review_after: 2026-08-10
source: owner statement 2026-07-11 (Registry/Catalog re-plan); previously ai-asset-registry/docs/knowledge-registry.md §6 (as of 2026-07-05); phased-sequencing context from ai-asset-registry/docs/knowledge-review/overview/roadmap.md (as of 2026-07-05)
---
- **RHOAI 3.5** — MCP Gateway deployment in RHOAI (documented external dependency per RHAISTRAT-1937); MCPLO TP (target Jul 24, 2026, flagged on risk); Agent registries. MCP Registry Dev Preview will NOT land in 3.5 stable (owner, 2026-07-11).
- **RHOAI 3.6 EA1** — the push: MCP Catalog TP + MCP Registry TP together, alongside Catalog-Registry integration (RHAISTRAT-2027). Jira fixversions being re-targeted to match.
- **RHOAI 3.6** — component GAs formalized against it (RHAISTRAT-1993/1994/1995; code freeze Oct 23, 2026). MCP Gateway GA rides RHCL 1.5 (Oct 2026).
- **OCP 5.0** — future. MCP Servers + MCP Gateway included.
- Related Jira: RHAIRFE-1370 (main), RHAIRFE-1457 (gateway in RHOAI), RHAIRFE-1456 (lifecycle operator in RHOAI); RHAISTRAT-2027 (integration, 3.6 EA1).

**Phased sequencing** (from the old repo's separate roadmap doc, `docs/knowledge-review/overview/roadmap.md`): Phase 1 = MCP Registry (3.5 DP, above). Phase 2 = Agent & Skills Registry — already in flight today as the separate `agent-registry` and `skills-registry` partitions, not a literal joint "phase 2" effort. Phases 3-4 as originally planned (a unified plugin framework spanning all asset types; full supply-chain/federation automation; notebooks, pipelines, and evaluators as registry assets) described the cross-cutting "AI Asset Registry" product framework — that partition was itself removed as a dead proposal in R2 batch 2, and this hub currently tracks each asset type as its own partition rather than building one unifying registry product. **Per owner ruling**: this unified-registry ambition is dormant, not doctrine — historical planning intent, not a current direction, but not closed off either; the owner may return to it if it comes up. Treat Phases 3-4 as inactive — neither a live commitment nor a permanently killed idea.

**Staleness flag**: no fresh 3.5 dates were provided as of this update (2026-07-06). RHOAI 3.4's Apr 10, 2026 code-freeze date has already passed (see History) with its ship status not reconfirmed this pass — treat the targets above as last-known, not verified current.

## History
- 2026-07-11 - **Update** - Registry/Catalog re-plan (owner statement during the Management hub refresh): prior value "RHOAI 3.5 - MCP Registry Dev Preview; ... hardening, registry integration, gateway configuration" superseded. Registry DP misses 3.5 stable; Catalog TP + Registry TP + Catalog-Registry integration (RHAISTRAT-2027) all target 3.6 EA1; Jira fixversions still show 3.5 on some items pending re-targeting. Both published hubs corrected the same day. (source: owner, 2026-07-11)
- 2026-07-06 — **Update** — added phased-sequencing context from `docs/knowledge-review/overview/roadmap.md` (R2 batch 5); per owner ruling, the original Phase 3-4 "unified AI Asset Registry" framing is dormant historical planning intent — not a current direction, but not closed off — rather than dead or doctrine. (source: R2 batch 5 apply — owner ruling)
- 2026-07-06 — **Update** — resolved label conflict: monolith §6 named the RHOAI 3.5 row "(TP target)" while describing its content as "MCP Registry Dev Preview" — resolved to Dev Preview per owner ruling, matching this hub's established 3.5 = Dev Preview framing (CLAUDE.md; this profile's own prior value). (source: R2 batch 3 apply — owner ruling)
- 2026-07-06 — **Update** — relegated completed/passed milestones out of the active body: "RHOAI 3.0 GA — Nov 2025. Baseline release." (completed — GA shipped) and "RHOAI 3.4 DP — Apr 10, 2026 code freeze. MCP Catalog DP (5 partner + 2 community MCPs), MCP Guardrail DP, Summit demo, Kubeflow GA." (code-freeze date passed as of this update; presumably shipped, not reconfirmed this pass — see staleness flag above). (source: R2 batch 3 apply — profile finalization, body carries current/future only)
- 2026-07-06 — **Update** — superseded: "MCP Registry: RHOAI 3.5 Dev Preview target. Related Jira: RHAIRFE-1370 (main), RHAIRFE-1457 (gateway in RHOAI), RHAIRFE-1456 (lifecycle operator in RHOAI). Full release timeline: seeded from the monolith at M3 (see plan runbooks)." (source: R2 batch 3 — full release timeline merged in from knowledge-registry.md §6)
- 2026-07-05 — **Creation** at hub seed; values carried from old repo.
