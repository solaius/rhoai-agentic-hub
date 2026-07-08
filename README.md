# rhoai-agentic-hub

Peter Double's working hub for Red Hat OpenShift AI PM work (MCP registry &
gateway, agent registry, agent memory, skills, gen-ai studio): knowledge,
project memory, enablement artifacts, and the skills that keep it all
organized — built for humans **and** agents to operate.

This repo is **public**. NDA/restricted content lives only in the gitignored
`restricted/` mirror, and nothing reaches the public pages site without an
explicit allowlist entry — see the trust model in
[docs/architecture.md](docs/architecture.md).

## Start here

| you are | read |
|---|---|
| a human, new to the repo | this page → [docs/architecture.md](docs/architecture.md) → [docs/setup.md](docs/setup.md) → [docs/working-here.md](docs/working-here.md) |
| an agent | [AGENTS.md](AGENTS.md) — the operating protocol — then `/memory/index.md` |
| looking for the rules | [conventions/](conventions/) — short, normative, CI-backed |
| wondering why it's built this way | [docs/architecture.md](docs/architecture.md) + [docs/history.md](docs/history.md) |

## Layout in one breath

`features/<feature>/` holds all content for one feature area in an identical
skeleton (`knowledge/ research/ strategy/ enablement/ work/`); `memory/` holds
working context (current state, preferences, log); `conventions/` is the
rulebook; `views/` and every `index.md` are generated — never hand-edited;
`publish/manifest.yaml` is the only path to the public pages site;
`restricted/` (gitignored) mirrors the layout for NDA content.

## Documentation

| doc | answers |
|---|---|
| [docs/architecture.md](docs/architecture.md) | how the whole system fits together, and why |
| [docs/setup.md](docs/setup.md) | new machine → working, in ≤30 minutes |
| [docs/working-here.md](docs/working-here.md) | the daily loop: filing, capturing, publishing |
| [docs/memory.md](docs/memory.md) | the two-tier memory system and the gate |
| [docs/skills.md](docs/skills.md) | every skill — when to use it, what it does, what's gated |
| [docs/publishing.md](docs/publishing.md) | manifest → CI → public pages site, end to end |
| [docs/tooling.md](docs/tooling.md) | scripts, linter, indexer, doctor, tests, CI |
| [docs/mcp-servers.md](docs/mcp-servers.md) | the MCP servers skills rely on — Slack, Google Workspace, rhai-tracker — setup and traps |
| [docs/history.md](docs/history.md) | lineage: charter, build, migration from the old repo |
| [conventions/](conventions/) | the normative rulebook the linter enforces |

## Links

- **Published artifacts:** https://solaius.github.io/rhoai-agentic-hub-pages/
- **Pages repo** (built output only): https://github.com/solaius/rhoai-agentic-hub-pages
- **Predecessor** (read-only source material):
  https://github.com/solaius/ai-asset-registry — the charter, design spec,
  and full migration audit trail live there
