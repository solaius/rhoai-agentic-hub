@AGENTS.md

# Claude Code specifics
- Deep guides live in `/docs/` (architecture, memory, skills, publishing,
  tooling, mcp-servers, enhancements, history) — read the matching one
  before re-deriving how the hub works.
- Skills marketplace: `.claude/settings.json` wires `opendatahub-io/skills-registry`;
  accept the trust prompt on first open, then `/plugin` to verify installs.
- Auto-memory: `hub.doctor setup` points `autoMemoryDirectory` at
  `memory/.scratch/` (absolute path in `.claude/settings.local.json`,
  per machine). Your automatic saves land there and are consolidated through
  the gate — do not write tracked memory files directly.
- This repo replaces `ai-asset-registry` for daily work; that repo is
  read-only source material for `hub.migrate`.
