---
type: fact
title: "Running the rfe-creator pipeline on this Windows machine"
description: Windows quirks for the rfe-creator/assess-rfe plugin pipeline - python vs python3, fcntl-blocked ID allocation, /tmp mapping to C:\tmp, explicit --schema-type, and plugin-cache script paths.
tags: [tooling, rfe, windows, plugins]
timestamp: 2026-07-10
status: current
---

Learned during the first full rfe pipeline runs (2026-07-10, RHAIRFE-2630..2643).
The plugin's scripts assume Linux; on this machine:

- **`python3` is not on PATH**: every skill/script says `python3`; run
  `python` instead (also patched inside `fetch-architecture-context.sh`
  logic when replicating it by hand).
- **`next_rfe_id.py` cannot run** (`ModuleNotFoundError: fcntl`). Allocate
  RFE IDs by scanning `artifacts/rfe-tasks/` for the highest `RFE-NNN` and
  continuing the sequence; safe when no parallel split/create is running.
- **`/tmp` in the scripts lands at `C:\tmp`** (Windows Python, not the Git
  Bash `/tmp`): `prep_assess.py` writes `C:\tmp\rfe-assess\single\`, and
  agents must be given the `C:\tmp` form of `{DATA_FILE}`/`{RUN_DIR}`.
- **`frontmatter.py set/read` needs `--schema-type rfe-review` explicitly**
  for files referenced by Windows backslash paths; the forward-slash path
  auto-detection never matches.
- **Plugin scripts run from the plugin cache** (`~/.claude/plugins/cache/
  opendatahub-skills/<plugin>/<version>/scripts/`) with the hub repo as
  cwd; `artifacts/` and `tmp/` resolve against the hub. Pass absolute
  plugin paths into subagent prompts.
- **Windows Python prints CRLF**: shell loops reading python output must
  strip the trailing `\r` before using values in comparisons (bit
  doctor.sh section 2; same pattern latent in section 8).

Doctor section 2 verifies the plugins are installed at all
(enabled-but-not-installed was the original failure; see
[fact-hub-build-operational-gotchas](/memory/facts/fact-hub-build-operational-gotchas.md)
for other machine gotchas).
