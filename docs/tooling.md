# Tooling & CI reference

Everything mechanical about keeping the hub healthy: the CLIs, the library
behind them, the doctor, the tests, and what CI enforces. Python 3.11+ and
the two deps in `scripts/requirements.txt` (`pyyaml`, `pytest`) are all it
takes.

## The commands

| command | does | run it when |
|---|---|---|
| `python scripts/hub_status.py` | morning brief — stale entries, open questions, unanswered qa, JTBD without evidence, enablement dirs missing a descriptor, a log-rotation reminder, the recent log tail, and last-push CI state (via `gh`); informational, always exits 0 | start of a session — where does the hub need attention |
| `python scripts/hub_lint.py` | structure + schema lint; exit 1 on errors, warnings never fail | before pushing; after hand-editing entries |
| `python scripts/hub_index.py` | regenerate every generated file (`index.md`s + `views/`) | after **any** entry add/edit — always before committing |
| `python scripts/hub_index.py --check` | verify generated files are current (what CI runs) | to reproduce a "stale index" CI failure |
| `python scripts/hub_index.py --rotate-log` | move previous-year `memory/log.md` sections into `memory/log-archive/<year>.md`, then reindex; incompatible with `--check` (exits 2 if both are given) | when `hub_status.py` flags rotation as due |
| `python scripts/hub_publish.py --check` | validate `publish/manifest.yaml` (schema, sources exist, duplicate dests) | after manifest changes |
| `python scripts/hub_publish.py --pages-dir <clone> [--hub-sha <sha>]` | apply the manifest to a pages-repo clone (what `publish.yml` runs) | to inspect locally what would ship |
| `python scripts/hub_publish.py --check-links --pages-dir <clone>` | verify internal link integrity of the pages clone; exit 1 on broken links | runs in `publish.yml` between the apply step and the push — reproduce a broken-link CI failure locally |
| `python scripts/hub_jira.py --check` | Jira connectivity/auth probe (doctor section 4 runs it) | setup; auth debugging |
| `python scripts/hub_jira.py --try-jql '<jql>'` | scope discovery: result count + sample rows | hub.jira-sweep step 2 |
| `python scripts/hub_jira.py --sweep <feature> --out <dir>` | proposed snapshot + ref candidates into `<dir>` (repo untouched) | driven by hub.jira-sweep |
| `python scripts/hub_jira.py --sync --out <dir>` | diff stored scopes + watched keys against live Jira | driven by hub.jira-sync |
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
| `jira.py` | async Jira REST client (pm-toolkit port): Cloud basic / DC bearer auth from `JIRA_*` env, JQL search with pagination, 429 retry, ADF→text, unauthenticated `probe_public`; write methods ported but unused by the hub.jira-* skills |
| `jiramap.py` | the snapshot contract: whitelisted `issue_row`, byte-stable `build_snapshot`, `validate` (lint), `diff` (sync), `watched_keys` (ref-/jtbd backlinks) |
| `disclosure.py` | local-first disclosure lint (`scan_repo`) — see "The disclosure lint" below |
| `status.py` | `build_brief` — assembles the morning-brief sections `hub_status.py` prints |
| `logrotate.py` | `rotate_log` — moves previous-year `memory/log.md` sections into `memory/log-archive/<year>.md` |

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

## The disclosure lint

`hub_lint.py` runs `hublib/disclosure.py` alongside the schema lint:

- **Restricted patterns (errors, local-first).** An OPTIONAL, gitignored
  `restricted/lint-patterns.txt` — one case-insensitive regex per line, `#`
  comments allowed — is scanned over `features/*/enablement/**/*.html`,
  `narrative/enablement/**/*.html`, and all public knowledge entries. A match
  is an ERROR naming the file:line and the pattern's line number (never its
  text). CI never sees the pattern file, so this net only exists on machines
  that carry `restricted/` — the pre-commit hook (doctor section 10) is its
  enforcement point. An invalid regex is skipped with a warning; the rest of
  the net still applies.
- **Generic heuristics (warnings, CI-visible).** `schema.RESTRICTED_HINTS`
  (SKU/pricing/NDA phrasing, dollar figures, signed-agreement phrasing) warns
  on knowledge-entry bodies (as before) and now also on enablement HTML.

## The doctor

`scripts/doctor.sh` is idempotent — safe to run any time. `check` never
writes; `setup` performs the fixes. Every FAIL line prints its own
remediation command. Sections:

| # | checks | setup mode fixes |
|---|---|---|
| 1 | python + pyyaml + pytest + httpx importable | `pip install -r scripts/requirements.txt` |
| 2 | `.claude/settings.json` declares the ODH skills marketplace | — (tracked file; confirm installs with `/plugin`) |
| 3 | auto-memory scratch redirect (`autoMemoryDirectory` → `memory/.scratch/`) | writes `.claude/settings.local.json`, creates `memory/.scratch/` |
| 4 | `restricted/.env` exists with required keys (`JIRA_*`) + live Jira reachability (`hub_jira.py --check`, WARN when offline); sources it so later sections see the `CTRACK_*` overrides and MCP secrets | — (secrets are copied between machines by hand, never generated) |
| 5 | pages repo cloned alongside (optional convenience) | — |
| 6 | structure: lint + index `--check` pass | — (points you at `hub_index.py`) |
| 7 | customer tracker: rhai-tracker MCP registered in `.mcp.json`, deps installed, server env present (tracker checkout defaults to `../rhai-customer-tracker`, override with `CTRACK_DIR`) | writes `.mcp.json`, installs deps, scaffolds the server `.env` |
| 8 | slack + google-workspace servers present in the Claude config (`$CLAUDE_CONFIG_DIR/.claude.json`, else `~/.claude.json` — profile-dependent) | writes server definitions + secrets from `restricted/.env` (config backed up to `*.bak` first) |
| 9 | slack MCP runtime: podman **engine** installed (vs Desktop-only), machine running, image pulled; token presence/expiry reminder — skipped entirely when slack isn't in play | starts the podman machine, pre-pulls the image (the engine install stays manual — admin `winget`; see [/docs/mcp-servers.md](/docs/mcp-servers.md)) |
| 10 | git pre-commit hook — check verifies install state (marker `# hub-doctor pre-commit v1`) | installs a hook running `hub_lint.py` + `hub_index.py --check`, backing up any foreign hook to `pre-commit.bak`; bypass deliberately with `git commit --no-verify` |

After `setup` on a fresh machine, **restart Claude Code** — the auto-memory
redirect, `.mcp.json`, and the MCP servers are all read at startup. MCP
server details, secrets, and troubleshooting:
[/docs/mcp-servers.md](/docs/mcp-servers.md).

## Tests

`scripts/tests/` covers each module (`test_frontmatter`, `test_schema`,
`test_indexer`, `test_publisher`, `test_disclosure`, `test_status`,
`test_logrotate`) with fixture repos built in `conftest.py`.
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
