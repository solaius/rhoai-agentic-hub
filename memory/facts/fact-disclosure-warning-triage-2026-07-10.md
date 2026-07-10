---
type: fact
description: "The 18 HTML heuristic warnings introduced by the enhancement batch were owner-triaged 2026-07-10: all benign — don't re-triage unless the flagged lines change"
timestamp: 2026-07-10
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

They persist as accepted warnings in `hub_lint` output by design (warnings
never fail the build). Re-triage only if the flagged lines change or new
warnings join them — compare against this list first.
