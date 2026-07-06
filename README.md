# rhoai-agentic-hub

Peter Double's working hub for Red Hat OpenShift AI PM work (MCP registry &
gateway, agent registry, agent memory, skills, gen-ai studio): knowledge,
project memory, enablement artifacts, and the skills that keep it all
organized — built for humans **and** agents to operate.

- **New here (human)?** Read this page, then [docs/setup.md](docs/setup.md)
  to get a machine working, then [docs/working-here.md](docs/working-here.md)
  for the daily loop.
- **New here (agent)?** Read [AGENTS.md](AGENTS.md) first — it is the map.
- **What is this repo, conceptually?** The intentionally-designed successor to
  [ai-asset-registry](https://github.com/solaius/ai-asset-registry). Design
  spec and charter live there under `docs/superpowers/specs/` (2026-07-05).

## Layout in one breath

`features/<feature>/` holds all content for one feature area in an identical
skeleton (`knowledge/ research/ strategy/ enablement/ work/`); `memory/` holds
working context (current state, preferences, log); `conventions/` is the
rulebook; `views/` and every `index.md` are generated — never hand-edited;
`publish/manifest.yaml` is the only path to the public pages site;
`restricted/` (gitignored) mirrors the layout for NDA content.

Published artifacts: https://solaius.github.io/rhoai-agentic-hub-pages/
