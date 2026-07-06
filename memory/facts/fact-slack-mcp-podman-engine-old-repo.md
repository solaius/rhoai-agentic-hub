---
type: fact
description: "OLD ai-asset-registry repo: Slack MCP needs the podman ENGINE CLI installed + machine started on Windows, not just Podman Desktop"
timestamp: 2026-07-06
status: current
source: old repo memory (originSessionId d0aa6999-adb1-4dea-be60-2bb922db0abb), migrated 2026-07-06
review_after: 2026-08-05
---
Describes the OLD `ai-asset-registry` repo's tooling — relevant when this hub's doctor skill grows its own Slack MCP check (R4).

That repo's `slack` MCP server launches `podman run … quay.io/redhat-ai-tools/slack-mcp` over stdio. On Windows this needs the podman ENGINE CLI (`winget install --id RedHat.Podman -e`, needs an elevated terminal — UAC fails silently, exit 1602, if driven from an automated shell), which is a separate install from Podman Desktop (the GUI). Podman Desktop alone gives no `podman.exe` — the MCP silently fails to load, no tools appear. `bootstrap.sh` section 7 ("Slack MCP runtime (podman)") checks engine/machine/image and was fixed 2026-07-05 to catch this (previously section 6 only checked the server was *configured*, not runnable).

Smoke-test handshake requires `LOGS_CHANNEL_ID` present (empty string OK); env keys are `SLACK_XOXC_TOKEN`/`SLACK_XOXD_TOKEN` (not `SLACK_MCP_*`). Requires restarting Claude Code after engine install — MCP servers and PATH only load at launch. See [fact-repo-doctor-tracker-gap-old-repo.md](/memory/facts/fact-repo-doctor-tracker-gap-old-repo.md).
