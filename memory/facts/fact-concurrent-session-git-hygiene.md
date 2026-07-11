---
type: fact
description: "Concurrent agent sessions in one clone contaminate each other two ways — shared main-checkout index (plain git commit sweeps another session's pre-staged files) and nested-worktree visibility; guards: per-session worktrees, clean-tree check before work, git diff --cached --stat before every commit"
timestamp: 2026-07-10
status: current
---
On 2026-07-09/10 two agent sessions worked this repo simultaneously
(hub.intake build on main; enhancement batch in a `.claude/worktrees/`
worktree) and contaminated each other through two distinct mechanisms:

1. **Shared main-checkout index.** `git commit` commits the whole index,
   not just the files staged this turn. The batch session's in-flight
   `scripts/hub_index.py` was pre-staged in the main checkout; the intake
   session's later `git add .gitignore && git commit` swept it into
   `f9a1e31`, publishing a half-feature with a broken import — CI red
   until revert `ef4cc49`. Worktrees have separate indexes; the main
   checkout's index persists across sessions.
2. **Nested-worktree visibility.** Worktrees under `.claude/worktrees/`
   live inside the main checkout's directory tree, so another session's
   file searches (Glob) can land edits there. The intake session's
   research-lint edits appeared as uncommitted changes inside the batch
   worktree and were swept into its first commit by a file-level
   `git add` (caught in review, recommitted clean as `2e690bc`).

**Standing guards:**
- One worktree per session; `.claude/worktrees/` is gitignored (`f9a1e31`).
- Verify `git status --porcelain` is clean before starting work and
  before dispatching any subagent.
- **Commit with pathspecs, always**: `git commit -m "..." -- <your paths>`
  commits only those paths, so files another session staged physically
  cannot ride along. Inspection alone (`git diff --cached --stat` before
  committing) is NOT a sufficient guard: in scripted command chains the
  commit runs before anyone reads the stat. Recurred 2026-07-10 even
  after the add -A ban (`b6f8b6a` swept a management-hub refresh batch
  mid-staging; content was gate-approved so no rollback, but the commit
  message misattributes it). All hub.* skills now prescribe the
  pathspec-commit form.
- Controllers cross-check each task commit's `git show --stat` against
  the task's expected file list.
