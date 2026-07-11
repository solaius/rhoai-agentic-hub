---
type: fact
description: "The 21 heuristic warnings introduced by the enhancement + trust batches were owner-triaged (18 on 2026-07-10, 3 on 2026-07-11): all benign — don't re-triage unless the flagged lines change"
timestamp: 2026-07-11
status: current
review_after: 2026-10-10
---
The enhancement batch (2026-07-09) extended the generic `RESTRICTED_HINTS`
heuristic to enablement HTML, surfacing 18 warnings across 9 files. All 18
were triaged benign on 2026-07-10:

- **11** public market/funding figures in the agent-memory series and
  architecture-options deck ($24M Series A, Harvey $5B valuation, $62M+
  consolidation stat ×7, $150B analyst projection) — industry data, not
  deal terms; these artifacts already passed the migration disclosure scrub.
- **6** JavaScript `"$1"` regex-replacement tokens in the
  registry-ui-prototype syntax highlighter (both index.html and the v0.1
  mockup).
- **1** illustrative `$500` policy example in the authz-audit explainer.

The published-site trust batch (2026-07-10) widened the net to entry
frontmatter and generated views; its 3 new warnings were triaged benign on
2026-07-11:

- `features/agent-memory/knowledge/person-jonathan-zarecki.md` (frontmatter)
  and its propagation `views/people.md:7`: signed-agreement phrasing in a
  person entry describing a public-in-repo signoff role.
- `features/mcp-ecosystem/enablement/management-hub/govern/entitlement.html:91`:
  the heuristic matches the owner's own supersession-caveat wording
  ("signed agreement still says"), added at the owner's direction.

They persist as accepted warnings in `hub_lint` output by design (warnings
never fail the build). Re-triage only if the flagged lines change or new
warnings join them — compare against this list first.
