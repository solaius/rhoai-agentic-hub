---
name: hub.doctor
description: Set up or health-check this machine for the hub — python deps, ODH marketplace wiring, auto-memory scratch redirect (autoMemoryDirectory), restricted/.env credentials, structure lint, and the MCP servers (rhai-tracker, slack + google-workspace, the slack podman runtime). Use on a new machine, after cloning, or when anything seems broken ("check my environment", "is my setup right", "run the doctor"), and for anything blocking an MCP server — "slack tools aren't loading", "is the slack mcp installed correctly", "invalid_auth", "install podman for slack", "google workspace mcp isn't connected". check = read-only, setup = writes.
---

# hub.doctor

1. Health check (read-only): `bash scripts/doctor.sh check`
2. Fix mode: `bash scripts/doctor.sh setup` — installs deps, creates
   memory/.scratch/, writes .claude/settings.local.json, registers
   rhai-tracker in .mcp.json, writes the slack + google-workspace server
   definitions **with secrets from restricted/.env** into the Claude config
   (backed up to *.bak first), starts the podman machine, pre-pulls the
   slack-mcp image.
3. **Run check first; never run setup without explicit user confirmation** —
   section 8 writes real credentials into the active profile's Claude
   config. Show what check found, then ask.
4. Report every section's OK/WARN/FAIL with the printed remediation. If
   setup wrote anything (autoMemoryDirectory, .mcp.json, MCP servers) or
   started the podman machine, tell the user to **RESTART Claude Code** —
   MCP servers and settings load at startup; nothing hot-loads.
5. Checks the script cannot do from bash — handle conversationally:
   - Marketplace plugins actually installed: have the user run /plugin and
     confirm rfe-creator appears; if not, the workspace trust prompt was
     probably declined — reopen the repo and accept it.
   - Section 8 "not configured" on a machine that used to work usually
     means the wrong Claude profile ($CLAUDE_CONFIG_DIR) — the section
     prints which config file it inspected; confirm the profile before
     re-running setup.
   - Slack tools returning `invalid_auth` = expired session tokens. Walk
     the user through slack-token-extractor and the SLACK_MCP_* →
     SLACK_* rename (docs/mcp-servers.md), update restricted/.env, re-run
     setup, restart.
   - Podman engine missing: hand the user the winget command to run in an
     **admin** terminal — winget's UAC prompt fails silently when driven
     from a non-elevated shell, so don't retry it from here.
   - Never echo secret values into the chat; the script writes them into
     config files only.

Guides: docs/mcp-servers.md (slack + google-workspace, incl. a hand-run
container smoke test for "config green but slack still won't load");
docs/tooling.md (doctor section-by-section reference).
