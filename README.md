# rhoai-agentic-hub

A file-based knowledge hub that turns PM work into organized, searchable, publishable knowledge — operated by humans and agents together.

This is a system, not a personal repo. All PM work (decisions, research, strategy, enablement) lives in one place under a consistent filing rule: **component × type**. Files plus conventions plus AI skills equal a system that stays organized over time without manual maintenance. Built for humans and agents as co-equal operators. This repo is **public** — NDA content lives only in the gitignored `restricted/` tree, and nothing ships to the public pages site without an explicit manifest entry.

## The hub today

| metric | count |
|---|---|
| Component areas | 15 |
| Knowledge entries | 444 |
| Research documents | 80 |
| Published artifacts | 20 |

## Three paths in

| you want to know | start here |
|---|---|
| What problems does this solve? | [docs/capabilities.md § Problems](docs/capabilities.md#problems-this-solves) |
| What does a day look like? | [docs/capabilities.md § Day in the life](docs/capabilities.md#a-day-in-the-life) |
| What can it do? | [docs/capabilities.md § Capabilities](docs/capabilities.md#capabilities) |

## Getting started

Ready to try it? The [setup guide](docs/setup.md) gets you running in 30 minutes.

## Deep dives

| doc | answers |
|---|---|
| [docs/capabilities.md](docs/capabilities.md) | what the hub can do, and which PM problems each capability solves |
| [docs/architecture.md](docs/architecture.md) | how the whole system fits together, and why |
| [docs/setup.md](docs/setup.md) | new machine to working, in 30 minutes or less |
| [docs/working-here.md](docs/working-here.md) | the daily loop: filing, capturing, publishing |
| [docs/memory.md](docs/memory.md) | the two-tier memory system and the gate |
| [docs/skills.md](docs/skills.md) | every skill — when to use it, what it does, what's gated |
| [docs/publishing.md](docs/publishing.md) | manifest to CI to public pages site, end to end |
| [docs/tooling.md](docs/tooling.md) | scripts, linter, indexer, doctor, tests, CI |
| [docs/mcp-servers.md](docs/mcp-servers.md) | the MCP servers skills rely on — Slack, Google Workspace, rhai-tracker |
| [docs/enhancements.md](docs/enhancements.md) | the hub's own improvement backlog |
| [docs/history.md](docs/history.md) | lineage: charter, build, migration from the old repo |
| [conventions/](conventions/) | the normative rulebook the linter enforces |

## For agents

Agents: read [AGENTS.md](AGENTS.md) then `memory/index.md`.

## Links

- **Published artifacts:** https://solaius.github.io/rhoai-agentic-hub-pages/
- **Pages repo** (built output only): https://github.com/solaius/rhoai-agentic-hub-pages
- **Predecessor** (read-only source material): https://github.com/solaius/ai-asset-registry
