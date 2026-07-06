---
type: fact
description: "OLD ai-asset-registry repo: repo-doctor deliberately excludes LLM-provider credentials from the shell env"
timestamp: 2026-07-06
status: current
source: old repo memory (originSessionId 3f4d9c13-c9d3-493c-9762-aaf9a6be15f2), migrated 2026-07-06
review_after: 2026-08-05
---
Describes the OLD `ai-asset-registry` repo's tooling, not this hub — check whether this hub's own doctor skill needs the same guard when its R4 MCP-server sections land.

Peter's directive (2026-07-05): that repo's `repo-doctor` must NOT set up LLM-provider credentials, because anyone running it already has working LLM access in Claude Code/Cursor — exporting these would hijack that auth. Its `~/.bashrc` env block sources `rhoai-restricted/.env` but then `unset`s `CLAUDE_CODE_USE_VERTEX`, `ANTHROPIC_VERTEX_PROJECT_ID`, `CLOUD_ML_REGION`, `GOOGLE_APPLICATION_CREDENTIALS`, `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`. The Vertex/gcloud ADC connectivity check was removed from its section 7. `check` detects the old blanket-export block and `setup` rewrites it in place.

Don't re-add LLM-provider vars to anything persisted to shell/Claude config, in that repo or this hub. See [fact-repo-doctor-tracker-gap-old-repo.md](/memory/facts/fact-repo-doctor-tracker-gap-old-repo.md).
