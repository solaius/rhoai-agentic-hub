---
type: fact
title: "R5 machine B doctor baseline (2026-07-11)"
description: "R5 cross-machine test: machine B doctor check yielded 18 ok / 1 warn / 5 fail. Slack xoxc/xoxd tokens traveled between machines (disproved the R5 prediction). Fails: plugin installs (no github ssh key), customer tracker clone, pre-commit hook."
timestamp: 2026-07-11
tags: [r5, cross-machine, doctor]
---
Machine B (desktop) doctor baseline from the R5 cross-machine continuity
test, run 2026-07-11.

**Result:** 18 ok, 1 warn, 5 fail.

**Key finding:** Slack xoxc/xoxd tokens DID travel between machines
(both were copied in restricted/.env), disproving the R5 prediction that
B would need fresh extraction. `slack auth ok: pedouble @ Red Hat`.

**WARN (1):**
- ~/.bashrc did not source restricted/.env (B had JIRA creds hardcoded
  directly in bashrc, not via the hub wiring block). Fixed by running
  `hub_env.py --setup` during the test.

**FAILs (5):**
- Plugin `rfe-creator@opendatahub-skills`: enabled but not installed (no
  github ssh key for the marketplace clone)
- Plugin `assess-rfe@opendatahub-skills`: same
- Plugin install would fail: no github ssh key and no https rewrite
- Customer tracker missing at expected path (not cloned on B)
- Pre-commit hook not installed

**Working on B without intervention:**
- Python + deps, auto-memory scratch, structure lint, indexes, Jira
  connectivity, pages repo, Slack MCP (podman + auth), Google Workspace
  MCP, Claude MCP servers all OK.
