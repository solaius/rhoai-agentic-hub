---
name: hub.doctor
description: Set up or health-check this machine for the hub — python deps, ODH marketplace wiring, auto-memory scratch redirect (autoMemoryDirectory), restricted/.env credentials, structure lint. Use on a new machine, after cloning, or when anything seems broken ("check my environment", "is my setup right", "run the doctor"). check = read-only, setup = writes.
---

# hub.doctor

1. Health check (read-only): `bash scripts/doctor.sh check`
2. Fix mode (installs deps, creates memory/.scratch/, writes
   .claude/settings.local.json): `bash scripts/doctor.sh setup`
3. Report every section's OK/WARN/FAIL with the printed remediation. If setup
   wrote autoMemoryDirectory, tell the user to RESTART Claude Code for the
   redirect to take effect.
4. Checks the script cannot do from bash — do conversationally:
   - Marketplace plugins actually installed: have the user run /plugin and
     confirm rfe-creator appears; if not, the workspace trust prompt was
     probably declined — reopen the repo and accept it.
   - Slack / podman / rhai-tracker MCP sections are NOT yet ported from the
     old repo-doctor. If needed, port them on-touch from
     C:/Users/peter/code/rh/ai-asset-registry/.claude/skills/repo-doctor/.
