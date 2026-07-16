---
type: fact
description: "doctor setup bakes Slack/Google secrets from restricted/.env into ~/.claude.json, so the MCP servers keep working when .env later breaks — masking the breakage; never run setup while .env is unreadable"
timestamp: 2026-07-16
status: current
---
`doctor setup` (section 8) copies the Slack and google-workspace secrets
OUT of `restricted/.env` and INTO the MCP server definitions in
`~/.claude.json`. From then on the MCP servers read the baked copies at
startup — not `.env` live.

Two operational consequences (both observed 2026-07-16, when machine B's
`.env` turned out to be git-crypt ciphertext — see
[[fact-restricted-git-crypt-sync]]):

1. **Breakage is masked.** Slack and Google MCP kept working perfectly for
   days on a machine whose `.env` was unreadable — a full Slack sweep ran
   fine. Only live readers failed (rfe.* JIRA_* env vars, doctor probes,
   future setup runs). "MCP works" says nothing about `.env` health.
2. **Never run `doctor setup` while `.env` is broken** — setup would
   regenerate the MCP definitions FROM the broken file and overwrite the
   working baked config. Fix `.env` first (doctor `check` now fails loud
   on the ciphertext case), then re-run setup only if secrets actually
   changed.

Corollary: rotated Slack session tokens (xoxc/xoxd) require BOTH updating
`restricted/.env` AND re-running `doctor setup` + Claude restart — editing
`.env` alone changes nothing for the running MCP servers.
