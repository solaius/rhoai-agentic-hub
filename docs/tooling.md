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
| `python scripts/hub_jira.py --audit <KEY>` | structured YAML dump of one issue (links, components, labels, fix versions, description) | driven by hub.jira-hygiene, read-only |
| `python scripts/hub_triage.py --scan <feature> --out <dir>` | fetch the feature's open Feature Requests, flag/classify/suggest, render the browser report + `rows-<feature>.json` into `<dir>` (repo untouched) | driven by hub.jira-triage step 2; read-only |
| `python scripts/hub_triage.py --plan <decisions.json> --rows <rows.json>` | render the gate table from an exported decisions file; zero network calls | driven by hub.jira-triage step 4; read-only |
| `python scripts/hub_triage.py --apply <decisions.json> --rows <rows.json> --feature <f> --out <dir>` | the only mode that writes: applies labels/comments/transitions to Jira, writes the proposed `triage-log-<feature>.yaml` into `<dir>` | driven by hub.jira-triage step 5; **writes to Jira** |
| `python scripts/hub_env.py --check` | report whether `~/.bashrc` sources the hub's `restricted/.env` and whether `JIRA_*` actually reach this shell (doctor section 4 runs it) | "the `rfe.*` skills cannot see my Jira credentials" |
| `python scripts/hub_env.py --setup` | back up `~/.bashrc`, remove the retired `ai-asset-registry` block, write or repair the hub block; idempotent, refuses to touch a profile whose markers are malformed | driven by `doctor.sh setup`; rarely by hand |
| `python scripts/hub_slack.py --check` | probe the Slack xoxc/xoxd tokens against `auth.test` (doctor section 9 runs it) | Slack MCP tools misbehaving: registration is not validity, and the tokens expire |
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
| `publisher.py` | manifest-driven publishing into a pages clone: copy plan, unpublish-on-removal via `.publish-snapshot.json` (v2: `{source, hash, published, badge}`), landing `index.html` rendered from `publish/landing-template.html` (grouped by area, NEW/UPDATED badges); hardened against path traversal, `dest` type swaps, and escapes from the pages root |
| `jira.py` | async Jira REST client (pm-toolkit port): Cloud basic / DC bearer auth from `JIRA_*` env, JQL search with pagination, 429 retry, ADF→text, unauthenticated `probe_public`; `add_label` (atomic add, the only write call site - see [/memory/facts/fact-jira-write-surface.md](/memory/facts/fact-jira-write-surface.md)), `add_comment`, `transition_issue` are used by `hub.jira-triage`; `update_issue` and `create_issue` remain dead code, zero call sites repo-wide |
| `jiramap.py` | the snapshot contract: whitelisted `issue_row`, byte-stable `build_snapshot`, `validate` (lint), `diff` (sync), `watched_keys` (ref-/jtbd backlinks) |
| `triage.py` | pure functions (`flag_staleness`, `classify_rfe`, `suggest_action`), the RFE fetch, transition resolution (`resolve_transition`), `plan_decisions` (gate table), and `apply_decisions` (labels via atomic add, comments, close/approve transitions) |
| `triage_html.py` | renders the self-contained triage report; no network, no repo writes |
| `refresh.py` | refresh-site config find/load/validate (work/refresh-<slug>.yaml); findings fold into lint_repo |
| `disclosure.py` | local-first disclosure lint (`scan_repo`) over enablement HTML, public knowledge entries, and generated views/indexes — see "The disclosure lint" below |
| `shellenv.py` | the `~/.bashrc` contract: `load_env` (the shared `restricted/.env` reader `hub_jira.py` and `hub_slack.py` both use), plus pure transforms over profile text (`render_block`, `scan`, `apply`). `apply` raises `MalformedProfile` rather than guessing at a profile whose hub markers are unbalanced or out of order: an earlier version silently ate user lines on the next run |
| `slack.py` | Slack `auth.test` probe: `(kind, message)`, always `ok` or `warn`, never `fail`, so an offline machine still reaches `0 fail`. Survives a non-JSON 200 response (a captive portal or corporate proxy) rather than crashing the doctor |
| `doctorio.py` | the `kind<TAB>message` protocol `doctor.sh` parses with `IFS=$'\t'`: `one_line` (collapses TAB/CR/LF) and `say`. The single emit boundary for `hub_env.py` and `hub_slack.py`, so untrusted strings (Slack response fields, raw `~/.bashrc` lines) cannot corrupt the parser |
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
| 2 | `.claude/settings.json` declares the ODH skills marketplace AND every `enabledPlugins` entry is actually installed in the profile's plugin cache (enabled-but-not-installed means `/rfe.create`, `/assess-rfe` etc. silently don't exist); when installs are missing, verifies the installer's clone path works (github ssh key or https rewrite) | applies the `git config --global url."https://github.com/".insteadOf "git@github.com:"` rewrite when ssh to github is dead (the installer clones over ssh); the install itself stays interactive: `/plugin` inside Claude Code, then `/reload-plugins` |
| 3 | auto-memory scratch redirect (`autoMemoryDirectory` → `memory/.scratch/`) | writes `.claude/settings.local.json`, creates `memory/.scratch/` |
| 4 | `restricted/.env` exists with required keys (`JIRA_*`) + live Jira reachability (`hub_jira.py --check`, WARN when offline); sources it so later sections see the `CTRACK_*` overrides and MCP secrets; then shell wiring: does `~/.bashrc` source `restricted/.env` so `JIRA_*` reaches every shell (`hub_env.py`, WARN when not wired or when the retired `ai-asset-registry` block is still present) | secrets: none (copied between machines by hand, never generated); shell wiring: `hub_env.py --setup` writes/repairs the hub's `~/.bashrc` block and removes the retired `ai-asset-registry` one (backs up to `~/.bashrc.bak` first) |
| 5 | pages repo cloned alongside (optional convenience) | — |
| 6 | structure: lint + index `--check` pass | — (points you at `hub_index.py`) |
| 7 | customer tracker: rhai-tracker MCP registered in `.mcp.json`, deps installed, server env present (tracker checkout defaults to `../rhai-customer-tracker`, override with `CTRACK_DIR`). A missing clone is a WARN, not a FAIL: only the customer-feedback skills need it, so a machine that does not do that work still reaches `0 fail` | writes `.mcp.json`, installs deps, scaffolds the server `.env` |
| 8 | slack + google-workspace servers present in the Claude config (`$CLAUDE_CONFIG_DIR/.claude.json`, else `~/.claude.json` — profile-dependent) | writes server definitions + secrets from `restricted/.env` (config backed up to `*.bak` first) |
| 9 | slack MCP runtime: podman **engine** installed (vs Desktop-only), machine running, image pulled; token presence/expiry reminder (all of section 9, including the auth probe, is skipped entirely when slack isn't in play); then an auth probe (`hub_slack.py --check`) that calls Slack's `auth.test` with the xoxc/xoxd tokens, WARN on failure (they're per-login session tokens that don't travel between machines) | starts the podman machine, pre-pulls the image (the engine install stays manual, admin `winget`; see [/docs/mcp-servers.md](/docs/mcp-servers.md)) |
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
