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
2. Parent is a RHAISTRAT Outcome.
3. A Cloners link back to the originating RHAIRFE.
4. Blocks / Depends links present where the work has real ordering.
5. At least one child RHAIENG Epic.
6. A Documents link to a `[ccs]` doc task.
7. Fix Version set.
8. Components set.
9. Labels carry a maturity tag (`DP` / `TP` / `GA`) and a release tag
   (`<release>-candidate` or `<release>-committed`).
10. A Feature Refinement Doc link at the top of the description.
11. GA only: a Platform Refinement Review link.

## Maturity-chain features (DP / TP / GA)

- Stage suffix in the summary (`[DP]`, `TP`, `GA`).
- A Depends link to the prior stage's feature.

## RHAIENG Epic

- Parent is a RHAISTRAT Feature.
- Has child Stories or Tasks.
- `[design]` prefix for UX epics, `[ccs Epic]` for docs epics.

## House style

- Inclusive language.
- No em dashes.
