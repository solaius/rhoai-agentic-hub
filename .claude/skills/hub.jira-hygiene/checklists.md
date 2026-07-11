# Jira hygiene checklists

Reference for hub.jira-hygiene. Adapted from pm-toolkit's
jira-hygiene-template.md. Judge the `--audit` dump against the checklist that
matches the issue's type. Report Pass / Fail / Warning per line, never guess.

## Hierarchy

RHAISTRAT Outcome
  -> RHAISTRAT Feature (`[Feat]` prefix)
       -> RHAIENG Epic
            -> Story / Task
RHAIRFE Feature Request is the intake form. It is cloned into a RHAISTRAT
Feature when it is accepted, and the two stay linked by a Cloners link.

## All issues

- Summary reads as a clear statement, not a fragment.
- Description is structured, not a single paragraph dump.
- Assignee, Priority and Status are set.

## RHAIRFE Feature Request

- Description carries the four sections: Problem Statement, Business Alignment,
  Proposed Solution, Acceptance Criteria.
- If accepted: an "is cloned by" link to a RHAISTRAT Feature.
- Labels do not include `<release>-committed` (that is set on the STRAT side).

## RHAISTRAT Feature (11 checks)

1. Summary starts with `[Feat]`.
2. Parent is a RHAISTRAT Outcome. Judge from `parent.type` (the dump's
   `parent` is an object with `key`, `type`, `summary`, not a bare key). If
   `parent` is null, Fail: no parent set.
3. A Cloners link back to the originating RHAIRFE.
4. Blocks / Depends links present where the work has real ordering.
5. At least one child RHAIENG Epic. Judge from the `children` list (entries
   with `type: Epic`). If `children_lookup` is not `ok`, report this check
   as Warning with "child lookup unavailable", never Fail.
6. A Documents link to a `[ccs]` doc task. Judge from the link record's own
   `summary` field (each entry in `links` carries the linked issue's
   summary, not just its key/type/status).
7. Fix Version set.
8. Components set.
9. Labels carry a maturity tag (`DP` / `TP` / `GA`) and a release tag
   (`<release>-candidate` or `<release>-committed`).
10. A Feature Refinement Doc link at the top of the description.
11. GA only: a Platform Refinement Review link. Remote links (Confluence
    etc.) are not in the `--audit` dump - Jira issue links are, remote links
    are not fetched. Judge this only from the description text if a link
    is quoted there; otherwise report Warning with "remote links are not in
    the audit dump, verify by hand". Never Fail on this item.

## Maturity-chain features (DP / TP / GA)

Trigger (derivable from the dump, apply automatically - do not ask): this
section applies, LAYERED ON TOP of the RHAISTRAT Feature checklist above
(both apply together, this does not replace it), when the dump's `summary`
contains `[DP]`, `[TP]`, or `[GA]` (or a bare `DP` / `TP` / `GA` stage
suffix), OR when `labels` contains `DP`, `TP`, or `GA`.

- Stage suffix in the summary (`[DP]`, `TP`, `GA`).
- A Depends link to the prior stage's feature.

## RHAIENG Epic

- Parent is a RHAISTRAT Feature. Judge from `parent.type`.
- Has child Stories or Tasks. Judge from the `children` list (entries with
  `type: Story` or `type: Task`). If `children_lookup` is not `ok`, report
  this check as Warning with "child lookup unavailable", never Fail.
- `[design]` prefix for UX epics, `[ccs Epic]` for docs epics.

## House style

- Inclusive language.
- No em dashes.
