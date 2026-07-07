# Scoring & Iteration Rules

This reference defines how individual reviewer scores are aggregated, what constitutes a passing draft, and how the review iteration loop is controlled.

## Score Aggregation

Each reviewer produces a normalized score (1-10) from their weighted dimension scores. These are aggregated with the following weights:

| Reviewer | Weight | Rationale |
|---|---|---|
| **Architect** | 30% | Structure is the skeleton — a poorly structured post can't be saved by good content |
| **Content** | 30% | Substance is why the reader stays — accuracy and voice are equally critical |
| **Formatting** | 20% | Important but more fixable — the editorial team can catch some of these |
| **Image** | 20% | Enhances but doesn't make or break — images can be improved post-review |

**Overall score formula**:

```
overall = (architect * 0.30) + (content * 0.30) + (formatting * 0.20) + (image * 0.20)
```

## Pass Criteria

A draft passes when ALL of the following are true:

1. **Overall weighted average >= 8.0**
2. **No individual dimension (across ANY reviewer) scores below 6.0**

Both conditions must be met. A draft with an overall 8.5 but one dimension at 5.0 does not pass.

### Near-Miss Rule

If the overall score is >= 7.5 AND only ONE dimension across all reviewers is between 5.0 and 5.9:

- Flag as **"conditional pass"** at the next human checkpoint
- Present the specific dimension that's below floor
- User decides: accept as-is, or iterate to fix that one dimension
- This prevents infinite loops over a single stubborn dimension that may be a matter of taste

## Iteration Controls

### Autonomous Iterations

- **Maximum 3 autonomous iterations** before a mandatory human checkpoint
- During autonomous iterations, the main agent revises the draft based on reviewer feedback without asking the user
- Each iteration produces a new versioned draft (`v1` → `v2` → `v3`)

### Human Checkpoints

At each checkpoint (after iterations 3, 6, and 9), present the user with:

1. Current scores (per-agent and overall)
2. Score trend (improving, plateauing, or declining)
3. The specific dimensions that are preventing a pass
4. Four options:

| Option | Effect |
|---|---|
| **Continue** | 3 more autonomous iterations |
| **Steer** | User provides specific guidance, then 3 more autonomous iterations |
| **Accept** | Override the threshold — proceed to finalize with current draft |
| **Abandon** | Stop the process. Keep all drafts and reviews on disk. |

### Hard Ceiling

- **9 total iterations** (3 checkpoints) is the absolute maximum
- After 9 iterations, present the best-scoring version and ask the user to Accept or Abandon
- Rationale: diminishing returns after 9 iterations. If the draft hasn't passed by then, the problem is likely in the requirements (abstract), not the execution

### Early Exit

- If a draft passes (overall >= 8.0, all dimensions >= 6.0) BEFORE reaching a checkpoint, present it to the user immediately
- Don't wait for the checkpoint — passing early is the happy path
- User can still request another iteration even after a pass

## Revision Strategy

When revising between iterations, follow this priority order:

1. **Fix blockers first**: Any dimension below 6.0 gets addressed before anything else. These are hard failures.
2. **Biggest impact next**: Address the lowest-scoring dimension across all four reviewers. This typically moves the overall score the most.
3. **Resolve conflicts**: If reviewers give conflicting feedback (e.g., Architect says "add more detail" while Content says "too verbose"), use the blog type as tiebreaker:
   - Developer Blog → favor the more detailed/technical suggestion
   - Red Hat Blog → favor the more strategic/concise suggestion
4. **Quick wins last**: Editorial compliance fixes (heading case, Oxford commas, product names) are easy and reliable. Apply them in every iteration.
5. **Include changelog**: Add a brief changelog at the top of each new draft version listing what changed and why. This changelog is stripped during finalization.

### Changelog Format

At the top of each draft v2+:

```markdown
<!-- CHANGELOG — will be removed during finalization
v[N] changes:
- [Dimension]: [What changed and why]
- [Dimension]: [What changed and why]
-->
```

## Score Summary File

After every review cycle, update `drafts/reviews/score-summary.md`:

```markdown
# Score Summary: [Blog Topic]

## Current Status: [IN PROGRESS / PASSED / CONDITIONAL PASS / ACCEPTED / ABANDONED]

| Version | Architect | Content | Formatting | Image | Overall | Status |
|---|---|---|---|---|---|---|
| v1 | [score] | [score] | [score] | [score] | [overall] | [status] |
| v2 | [score] | [score] | [score] | [score] | [overall] | [status] |
| ... | | | | | | |

## Dimensions Below Floor (current version)
[List any dimensions below 6.0 across all reviewers, with the reviewer name and dimension name]

## Trend
[Per-agent trend: improving ↑, stable →, declining ↓]
[Note if any agent's score has plateaued for 2+ iterations]

## Checkpoint History
[Record each human checkpoint decision: Continue/Steer/Accept/Abandon + any steering guidance provided]
```

## Example Score Calculation

Given these reviewer normalized scores:
- Architect: 7.8
- Content: 8.2
- Formatting: 8.5
- Image: 7.0

Overall = (7.8 × 0.30) + (8.2 × 0.30) + (8.5 × 0.20) + (7.0 × 0.20)
        = 2.34 + 2.46 + 1.70 + 1.40
        = **7.90**

Result: **Below threshold** (7.90 < 8.0). Check individual dimensions — if all are >= 6.0, this is close and likely passes on the next iteration. If any dimension is below 6.0, that's the priority fix.
