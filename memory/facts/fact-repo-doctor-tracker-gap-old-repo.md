---
type: fact
description: "OLD ai-asset-registry repo: repo-doctor's bootstrap.sh reports the rhai-tracker MCP's real state (registered/deps/server-env), not just c-track-on-disk"
timestamp: 2026-07-06
status: current
source: old repo memory (originSessionId 3f4d9c13-c9d3-493c-9762-aaf9a6be15f2), migrated 2026-07-06
review_after: 2026-08-05
---
Describes the OLD `ai-asset-registry` repo's tooling (`repo-doctor` skill / `bootstrap.sh`), not this hub. Still true there as of migration; relevant when this hub's own doctor skill grows MCP-server sections (R4 runbook).

`bootstrap.sh` was fixed (2026-07-05) so section 5 no longer falsely passes when c-track is merely cloned to disk. It now reports four separate states and `setup` acts on each: (1) c-track cloned; (2) registered in `.mcp.json` — `setup` now creates the gitignored per-machine file if absent; (3) node deps — `setup` runs `npm install` in `c-track/server/`; (4) `server/.env` — `setup` scaffolds from `.env.example` (user must still fill `GOOGLE_SPREADSHEET_ID`, `GOOGLE_CLIENT_ID/SECRET`, `AI_PROVIDER`). Default `CTRACK_DIR` changed `../rh/c-track` → `../c-track`.

Old repo's tracker MCP was deferred (core repo — Jira, Slack, google-workspace MCP, skills, RFE pipeline — was fully working without it). See [fact-repo-doctor-llm-cred-exclusion-old-repo.md](/memory/facts/fact-repo-doctor-llm-cred-exclusion-old-repo.md).
