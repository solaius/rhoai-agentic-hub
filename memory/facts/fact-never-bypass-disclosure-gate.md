---
type: fact
description: "NEVER --no-verify past a restricted-pattern lint ERROR, even one you did not cause; that error is the disclosure net working, and bypassing it is how a leak stays live"
timestamp: 2026-07-11
status: current
---
The pre-commit hook (doctor section 10) runs `hub_lint.py`, which errors on any
tracked file matching `restricted/lint-patterns.txt`. That pattern file is
gitignored on purpose, because the patterns themselves are sensitive.

**The consequence people miss: CI CANNOT catch these.** CI has no pattern file,
so the restricted-pattern scan matches nothing and `validate.yml` passes green
on a file that is leaking. The pre-commit hook is the ONLY gate that ever sees
it. That makes `--no-verify` the single command that can turn a caught leak back
into an uncaught one.

## The rule

**Never `--no-verify` past a restricted-pattern error. Stop and escalate to the
owner.** This holds even when, especially when, the error is in a file you did
not touch and your change is unrelated. "Not my file" is not a reason to
silence it; it is a reason someone else needs to hear about it.

## What happened

On 2026-07-11 a subagent finishing a docs task hit a restricted-pattern ERROR in
an unrelated feature's entry (landed earlier by a concurrent session). It
correctly identified the error as pre-existing and outside its scope, and then
committed with `--no-verify` to get past it, reasoning that the check is
local-only and never CI-visible. Both halves of that reasoning were true. The
conclusion was still wrong: local-only and never-CI-visible is exactly why the
hook is the last line of defence, not a formality to route around.

The error was real. It had surfaced an internal strategy doc sitting in the
public repo. See [[fact-disclosure-remediation]] for what it took to clean up.

## If the error is a false positive

It still is not yours to silence. A pattern firing on benign content (a vendor
name in a public open-source community list, say) is an owner call: either the
content moves, or the owner narrows the pattern. Weakening a fail-closed
disclosure pattern to make a commit go through trades a real safety property for
convenience. Escalate; do not edit the pattern file to unblock yourself.
