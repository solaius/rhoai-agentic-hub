---
type: fact
description: "Removing leaked content from this repo takes TWO filter-repo passes (a path purge misses the entry description, which hub_index propagates into tracked generated views), and a force-push does NOT purge the blob from GitHub"
timestamp: 2026-07-11
status: current
---
Learned the hard way on 2026-07-11, remediating an internal strategy doc that
reached the public repo through a concurrent session's intake and was already
pushed. The doc itself is now in `restricted/`; what follows is only the
mechanics, which generalize to any future leak here.

## A path-only history purge is INSUFFICIENT in this repo

`git filter-repo --path <entry> --invert-paths` removes the entry from every
commit and then reports clean. It is not clean. Every knowledge entry carries a
`description` in its frontmatter, and `hub_index.py` propagates that
description verbatim into TRACKED GENERATED files:

- `views/decisions.md` (and the other views)
- `features/<f>/index.md`
- `features/<f>/knowledge/index.md`

Those generated files are a second copy of the sensitive sentence, in files the
path filter never touches. After pass 1 the entry showed 0 hits, but
`git grep <string> $(git rev-list --all)` still found the description in three
generated files.

**So: always run a second pass.** `git filter-repo --replace-text <rules>` with
a `literal:<the description>==>[redacted]` rule. Then verify with
`git grep` across `git rev-list --all`, not just `git log -- <path>`.

The general rule: **purge the string, not just the path.** Anything that shows
up in a generated view has more than one home.

## A force-push does NOT purge content from GitHub

After the rewrite succeeded and `main` was verifiably clean, the file was still
served in full from the orphaned commit:

    gh api "repos/<owner>/<repo>/contents/<path>?ref=<orphaned-sha>"
    -> returns the complete file

Force-pushing makes old commits unreachable from a branch. It does not delete
the objects. GitHub keeps them and serves them at their direct SHA URL
indefinitely, and that SHA survives in reflogs, CI logs, and notification
emails. Only a GitHub Support garbage-collection request actually removes them.

Owner ruling 2026-07-11: **do not send that request; the exposure is accepted.**
The repo had 0 forks, so GitHub's object store is the only remaining copy. Do
not re-raise this without new information.

## Order of operations that worked

1. Move the entry to `restricted/<same path>` (gitignored), `git rm` the
   tracked copy.
2. `python scripts/hub_index.py` so the generated views drop it. Inbound links
   go dangling, which conventions allow.
3. `hub_lint.py` must reach 0 errors before committing. Commit normally: the
   pre-commit gate should now PASS on its own. See
   [[fact-never-bypass-disclosure-gate]].
4. `git bundle create <backup> --all` BEFORE any rewrite.
5. filter-repo pass 1 (path), pass 2 (replace-text on the description).
6. Re-add `origin` (filter-repo strips it deliberately), force-push, re-run the
   suite and watch CI.

Related: [[fact-concurrent-session-git-hygiene]] (the leak arrived via a
concurrent session in the shared checkout).
