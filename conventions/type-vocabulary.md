# Type vocabulary

## Knowledge entries (`features/*/knowledge/`)

| `type` | filename prefix | it is | extra required fields |
|---|---|---|---|
| `decision`  | `decision-` | a made call (ADR-lite: Context → Decision → Consequences) | `decided` |
| `fact`      | `fact-`     | a durable domain fact/status | — |
| `reference` | `ref-`      | pointer-out to an external source | `resource` (canonical, see [uris.md](/conventions/uris.md)) |
| `person`    | `person-`   | stakeholder/contact | `role`, `org` |
| `question`  | `question-` | open question/risk | `status: open\|answered` |
| `qa`        | `qa-`       | a **field** question with our canonical answer; `asks:` list of `{date, by, context?}` records recurrence (`by`: customer\|partner\|sales\|ssa\|pm\|eng\|exec\|other) | `status: open\|answered`, `asks` |
| `jtbd`      | `jtbd-`     | a job to be done ("When …, I want …, so I can …"); execution status stays in Jira (`jira:` field) | `persona` (locked list), `status: candidate\|validated\|delivered\|retired` |

`question-` = **our** open product questions, tracked to resolution.
`qa-` = **the field's** answered questions, tracked for reuse/recurrence.
Don't merge them. `persona` locked list (source of truth:
[fact-personas.md](/features/platform/knowledge/fact-personas.md); extend both
together): `ai-engineer` · `platform-engineer` · `agentops-admin` ·
`business-consumer` · `data-scientist` · `cluster-admin` · `rhoai-admin`.

## Narrative entries (`narrative/knowledge/` only)

| `type` | filename prefix | it is | extra required fields |
|---|---|---|---|
| `pillar` | `pillar-` | an RHAI strategic pillar | — |
| `story`  | `story-`  | a cross-feature narrative connecting features to customer value; optional `pillar:` root-path link | `features` (non-empty) |

Narrative knowledge also accepts the standard vocabulary above.

## Artifact descriptors (`*/enablement/<slug>/artifact.md`)

| `type` | filename | it is |
|---|---|---|
| `artifact` | exactly `artifact.md`, inside the slug dir | makes a deck/write-up indexable (`views/artifacts.md`); optional `features:`; publish state is derived from the manifest, never stored |

## Cross-references (`features:`)
Any knowledge entry or artifact descriptor may declare `features: [ids…]` —
validated against `features/features.yaml` (unknown id = lint **error**; the
routing table is closed, unlike dangling links). The indexer renders the
backlinks: per-feature `## Connections` sections plus the views.

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
deciding whether to open the file), `timestamp` (ISO date), optional `tags`,
optional `title` (display name — indexes fall back to the filename stem).

## Validity fields (changeable facts; local OKF extensions)
`status: current|superseded` · `valid_from` · `superseded_by: /path/to/entry.md`
· `review_after: <ISO date>`. Never delete a superseded entry.
Optional provenance: `source:` (URL, meeting, or session reference).
Note: `question` entries use their own `status` enum (`open|answered`);
the `current|superseded` validity lifecycle does not apply to questions.
