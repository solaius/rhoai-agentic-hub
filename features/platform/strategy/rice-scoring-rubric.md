---
title: RICE scoring rubric for RHAI
description: The full RICE (Reach x Impact x Confidence / Effort) prioritization rubric for RHAISTRAT/RHOAISTRAT Jira projects — load-bearing methodology read directly by the rice-strats skill.
source: ai-asset-registry/docs/knowledge-review/strategy/rice-scoring-rubric.md (as of 2026-07-05), originally from https://docs.google.com/document/d/199os238m6oHDEUlJB7mPCx8lothFern3LO2wfjnPsuc/edit (Arjay Hinek)
timestamp: 2026-07-06
review_after: 2026-08-05
---

> **Status**: REFERENCE — the established process for RHAISTRAT and RHOAISTRAT Jira projects. This is a load-bearing methodology document: the `rice-strats` skill (currently in the old `ai-asset-registry` repo at `.claude/skills/rice-strats/`) reads this rubric directly to calibrate scoring. **When `rice-strats` is ported into this hub (R4 runbook, pull-driven), it must repoint its rubric read to this file** (`/features/platform/strategy/rice-scoring-rubric.md`) instead of the old repo path.

## Formula

**RICE Score = (Reach × Impact × Confidence) / Effort**

PMs and UX confer on Reach, Impact, and Confidence. Engineering delivery leads and partners with significant effort impact are consulted for the Effort score. RICE scores are automatically calculated by Jira once all four fields are entered — the "Prioritization" tab appears on a Feature as soon as any RICE field has an entry.

## Scoring components

### Reach (market)

How many people will be affected in a given time period.

| Score | Meaning |
|---|---|
| 1 | Very few users (niche request) |
| 3 | Small user group (<10% of users) |
| 5 | Moderate user group (10-30% of users) |
| 8 | Large group (30-70% of users) |
| 13 | Nearly all users (>70%) — game changer for the industry |

### Impact (customer/system)

How much this will benefit those affected or contribute to the goal.

| Score | Meaning |
|---|---|
| 1 | Minimal (small QoL improvement) |
| 3 | Low (slight improvement in workflow or minor feature) |
| 5 | Medium (noticeable productivity or revenue gain) |
| 8 | High (major pain point solved, new capability) |
| 13 | Massive (game-changer, strategic differentiator) or non-negotiable (legal requirement) |

Impact should also capture (per William Caban's feedback): **pain level** (are we solving a common pain?), **blocking other work** (is this blocking other initiatives?), and **addressing a new market** (does this open traction or new markets?).

### Confidence

How certain you are of your Reach and Impact estimates.

| Score | Meaning |
|---|---|
| 50% | Mostly hypothesis or guesswork about reach and impact |
| 75% | Some data but still assumptions (think 75-90%) |
| 100% | Strong evidence/data validated by analytics or customer feedback (think >90%) |

Confidence applies only to Reach and Impact — the Effort score accounts for uncertainty independently.

### Effort

High-level relative effort estimate, provided by people who work directly with the delivery teams — never treated as a commitment. RHAI uses relative scoring (not person-months) to avoid obscuring complexity, dependencies, and unknowns.

| Score | Meaning |
|---|---|
| 1 | Low effort — few unknowns, reasonable scope, one team in a sprint |
| 2 | Medium effort — some unknowns, may involve a couple of teams, may be more than a sprint |
| 3 | Medium+ — some unknowns, cross-team effort, may require feature story mapping once prioritized |
| 5 | High effort — multiple unknowns, multiple teams, will likely require feature story mapping |
| 8 | Massive effort — multiple unknowns and dependencies, likely connected to work outside our organization, will absolutely require feature story mapping and likely broken into additional features |
| 13 | Too large to responsibly estimate — must be broken into smaller features |

## How to apply

1. List the features you want to prioritize.
2. Assign Reach, Impact, Confidence, and Effort values in the Jira "Prioritization" tab (available on RHAISTRAT and RHOAISTRAT projects).
3. Jira automatically calculates the RICE score once all four fields are entered.
4. Rank by RICE score (highest = highest priority).
5. Add a Jira comment starting with **"RICE SCORE JUSTIFICATION:"** documenting the rationale for each score.

### Worked example

| Feature | Reach | Impact | Confidence | Effort | RICE score |
|---|---|---|---|---|---|
| Feature A | 8 | 3 | 75% | 5 | 3.6 |
| Feature B | 3 | 1 | 50% | 3 | 0.5 |

Feature A (3.6) ranks higher than Feature B (0.5).

## Key reviewer feedback

- **Jenn Giardino**: Confidence levels need clearer examples — what constitutes "strong evidence"? One customer vs. multiple CAI/field-team insights?
- **Jeremy Eder**: the original "500"-style Reach values were replaced with relative Fibonacci sizing to prevent gaming.
- **Dana Gutride**: the Effort rubric should account for very large effort by a single team, not only multi-team work.

## In this hub

- Field mappings and how the `rice-strats` skill applies this rubric against live Jira tickets: `CLAUDE.md` (RICE Scoring Fields section) in the old `ai-asset-registry` repo — pending its own port under R4.
- Author: [person-arjay-hinek.md](/features/platform/knowledge/person-arjay-hinek.md).
- Reviewer feedback authors also appear in [fact-stakeholder-map.md](/features/platform/knowledge/fact-stakeholder-map.md) (RICE rubric reviewers section).
