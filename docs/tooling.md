# Tooling & CI reference

Everything mechanical about keeping the hub healthy: the CLIs, the library
behind them, the doctor, the tests, and what CI enforces. Python 3.11+ and
the two deps in `scripts/requirements.txt` (`pyyaml`, `pytest`) are all it
takes.

## The commands

| command | does | run it when |
|---|---|---|
| `python scripts/hub_lint.py` | structure + schema lint; exit 1 on errors, warnings never fail | before pushing; after hand-editing entries |
| `python scripts/hub_index.py` | regenerate every generated file (`index.md`s + `views/`) | after **any** entry add/edit — always before committing |
| `python scripts/hub_index.py --check` | verify generated files are current (what CI runs) | to reproduce a "stale index" CI failure |
| `python scripts/hub_publish.py --check` | validate `publish/manifest.yaml` (schema, sources exist, duplicate dests) | after manifest changes |
| `python scripts/hub_publish.py --pages-dir <clone> [--hub-sha <sha>]` | apply the manifest to a pages-repo clone (what `publish.yml` runs) | to inspect locally what would ship |
| `bash scripts/doctor.sh [check\|setup]` | machine health check (`check`, read-only, default) or fix mode (`setup`) | new machine; anything environmental feels off |
| `python -m pytest scripts/tests -v` | the test suite for all of the above | when changing anything in `scripts/` |

The single most common failure: edit an entry, forget
`python scripts/hub_index.py`, push → CI red on `--check`. Regenerate after
*all* edits, as the last step before committing. (One deliberate exception
inside `--check`: `views/stale-facts.md` is time-dependent, so freshness of
that one file is not gated — reindex runs refresh it.)

## The library — `scripts/hublib/`

| module | responsibility |
|---|---|
| `frontmatter.py` | markdown + YAML frontmatter parsing (`parse`, `load_file`), LF-normalized, `FrontmatterError` on malformed input |
| `schema.py` | `lint_repo()` and `validate_manifest()`; owns the type vocabularies, filename-prefix map, skeleton contract, canonical-URI patterns, and the line budgets |
| `indexer.py` | deterministic generation of every `index.md` and `views/` file from frontmatter; the `<!-- generated … -->` marker; `write_all` / `check` |
| `publisher.py` | manifest-driven publishing into a pages clone: copy plan, unpublish-on-removal via `.publish-snapshot.json`, landing `index.html` generation; hardened against path traversal, `dest` type swaps, and escapes from the pages root |

All linter findings are `"<relpath>: <message>"` strings, returned as
`(errors, warnings)` — errors fail CI, warnings inform.

**Errors** (build-failing): malformed frontmatter; missing base fields
(`type`, `description`, `timestamp`); unknown `type`; filename prefix
missing or disagreeing with `type`; missing type-specific required fields
(`decision→decided`, `reference→resource`, `person→role,org`); bad status
enums; non-canonical `resource:` for known domains; skeleton violations
(unknown dirs, files directly under a feature); `AGENTS.md` over 150 lines;
`memory/index.md` over 200 lines; manifest problems (missing fields, bad
audience, `..` paths, missing source, duplicate dest).

**Warnings** (informational): broken repo-root links (dangling links are
allowed — they mark not-yet-written knowledge); unknown `resource:` domains;
`status: superseded` without a `superseded_by` pointer; the
restricted-content heuristic matching tracked files.

`restricted/`, when present locally, is linted with the same rules — so NDA
content stays convention-clean even though CI never sees it.

## The doctor

`scripts/doctor.sh` is idempotent — safe to run any time. `check` never
writes; `setup` performs the fixes. Every FAIL line prints its own
remediation command. Sections:

| # | checks | setup mode fixes |
|---|---|---|
| 1 | python + pyyaml + pytest importable | `pip install -r scripts/requirements.txt` |
| 2 | `.claude/settings.json` declares the ODH skills marketplace | — (tracked file; confirm installs with `/plugin`) |
| 3 | auto-memory scratch redirect (`autoMemoryDirectory` → `memory/.scratch/`) | writes `.claude/settings.local.json`, creates `memory/.scratch/` |
| 4 | `restricted/.env` exists with required keys (`JIRA_*`); sources it — minus the deliberately-excluded LLM-provider credentials — so later sections see the `CTRACK_*` overrides and MCP secrets | — (secrets are copied between machines by hand, never generated) |
| 5 | pages repo cloned alongside (optional convenience) | — |
| 6 | structure: lint + index `--check` pass | — (points you at `hub_index.py`) |
| 7 | customer tracker: rhai-tracker MCP registered in `.mcp.json`, deps installed, server env present (tracker checkout defaults to `../rhai-customer-tracker`, override with `CTRACK_DIR`) | writes `.mcp.json`, installs deps, scaffolds the server `.env` |
| 8 | slack + google-workspace servers present in the Claude config (`$CLAUDE_CONFIG_DIR/.claude.json`, else `~/.claude.json` — profile-dependent) | writes server definitions + secrets from `restricted/.env` (config backed up to `*.bak` first) |
| 9 | slack MCP runtime: podman **engine** installed (vs Desktop-only), machine running, image pulled; token presence/expiry reminder — skipped entirely when slack isn't in play | starts the podman machine, pre-pulls the image (the engine install stays manual — admin `winget`; see [/docs/mcp-servers.md](/docs/mcp-servers.md)) |

After `setup` on a fresh machine, **restart Claude Code** — the auto-memory
redirect, `.mcp.json`, and the MCP servers are all read at startup. MCP
server details, secrets, and troubleshooting:
[/docs/mcp-servers.md](/docs/mcp-servers.md).

## Tests

`scripts/tests/` covers each module (`test_frontmatter`, `test_schema`,
`test_indexer`, `test_publisher`) with fixture repos built in `conftest.py`.
The publisher tests include the safety regressions (traversal-escaping
dests, dir⇄file type swaps, `dest: "."`); the indexer tests pin the
generator's convergence (running it twice changes nothing) and the
stale-facts exclusion. Add a regression test with any behavior fix.

## CI

Two workflows in `.github/workflows/`:

- **`validate.yml`** — every push and PR: install deps → `pytest` →
  `hub_lint.py` → `hub_index.py --check` → `hub_publish.py --check`.
  Green means: entries conform, generated files are current, budgets hold,
  the manifest is shippable.
- **`publish.yml`** — pushes to `main` only: checks out this repo and the
  pages repo (via the `PAGES_PUSH_TOKEN` secret), applies the manifest,
  commits to the pages repo as `hub-publish-bot` (skipping when nothing
  changed). Details and token setup: [/docs/publishing.md](/docs/publishing.md).

What CI is deliberately checking for you: hand-edited generated files,
schema drift, index staleness, budget overruns (`AGENTS.md` ≤150 lines,
`memory/index.md` ≤200), broken manifests, and regressions in the scripts
themselves.
