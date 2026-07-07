# Customer tracker

Pointer only — there is no customer data in this file or anywhere in the
public tree. This directory exists so the skills that use it have somewhere
public to point to.

## What this is

Peter tracks customer interest in MCP/agentic AI work (which accounts are
evaluating what, status, requirements, action items) in two places:

1. A local HTML interest tracker + its source meeting transcripts — this
   machine's working copy, restricted (NDA customer data), never tracked.
2. A shared Google Sheet, reachable through the `rhai-tracker` MCP server —
   the actual cross-PM, cross-machine source of truth. Other Red Hat AI PMs
   read and write this sheet independently of this hub.

## Where the real data lives

`restricted/features/platform/work/customer-tracker/` (gitignored, local-only,
mirrors this same path under `restricted/` per
[conventions/layout.md](/conventions/layout.md)):

- `customer-interest-tracker.html` — the tracker itself
- `transcripts/` — source meeting transcriptions it's built from

If that directory doesn't exist on this machine yet, it hasn't been created
here — run `customer-feedback-ingest` to start it from a first source.

## Skills that operate on it

| skill | does |
|---|---|
| `customer-feedback-ingest` | adds/updates a customer from a transcript, email, Jira ticket, or pasted notes |
| `customer-feedback-refresh` | audits the tracker for staleness, missing sources, and accuracy |
| `customer-feedback-sync` | diffs the local tracker against the shared Google Sheet and pushes approved changes (gated — see the skill's Push Gate) |

## MCP setup

The `rhai-tracker` MCP server is provided by a separate sibling repo
(`c-track` — shared team tooling, not hub content) and registered in this
repo's root `.mcp.json` (gitignored, machine-specific). Run
`bash scripts/doctor.sh check` (`hub.doctor`) to see its status and
`setup` to wire it up; restart Claude Code afterward for the MCP connection
to take effect.
