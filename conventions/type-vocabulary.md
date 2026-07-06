# Type vocabulary

## Knowledge entries (`features/*/knowledge/`)

| `type` | filename prefix | it is | extra required fields |
|---|---|---|---|
| `decision`  | `decision-` | a made call (ADR-lite: Context → Decision → Consequences) | `decided` |
| `fact`      | `fact-`     | a durable domain fact/status | — |
| `reference` | `ref-`      | pointer-out to an external source | `resource` (canonical, see [uris.md](/conventions/uris.md)) |
| `person`    | `person-`   | stakeholder/contact | `role`, `org` |
| `question`  | `question-` | open question/risk | `status: open\|answered` |

## Memory files (`memory/`)

| `type` | it is |
|---|---|
| `profile`    | volatile current-state, one file per subject, updated in place |
| `fact`       | dated atomic working fact (process decision, learning) |
| `preference` | how Peter works |
| `feedback`   | guidance given to agents (keep the why) |

`fact` exists in both stores — the boundary rule in
[memory.md](/conventions/memory.md) decides *where*; the schema is shared.

## Base fields (every entry, both stores)
`type`, `description` (one line — feeds indexes; write it for a reader
deciding whether to open the file), `timestamp` (ISO date), optional `tags`.

## Validity fields (changeable facts; local OKF extensions)
`status: current|superseded` · `valid_from` · `superseded_by: /path/to/entry.md`
· `review_after: <ISO date>`. Never delete a superseded entry.
Optional provenance: `source:` (URL, meeting, or session reference).
