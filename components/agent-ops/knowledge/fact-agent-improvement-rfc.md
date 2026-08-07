---
type: fact
title: Agent Improvement RFC — overview
description: Two-part MLflow RFC for self-healing agents — Part 1 adds trace-aware webhook events for eval thresholds, issue detection, and trace errors; Part 2 adds an Improve tab with coding-agent-driven diagnosis and fix workflow (failing traces to PRs).
timestamp: 2026-08-07
tags: [agent-ops, mlflow, self-healing, upstream, webhooks]
components: [skills-registry]
review_after: 2026-10-07
source: https://github.com/Nehanth/agent-improvement-rfc/pull/1
---

## Part 1 — Trace-Aware Webhook Events

MLflow's webhook system has 15 event types, all on the registry/budget side.
The observability side (tracing, auto-eval, issue detection) cannot notify
anyone of anything. Part 1 adds four events using the existing webhook
delivery engine:

- `trace_assessment.threshold_breached` — rolling average of judge scores
  crosses a user-defined threshold (configurable window size + cooldown)
- `trace_issue.created` / `trace_issue.updated` — issue detection saves
  new or updated findings
- `trace.errored` — a trace completes in an error state

No new background services. Each event fires from a write path that already
exists (score save, detection run completion, trace save).

## Part 2 — Improvement Workflow

An **Improve** tab in the experiment UI. The loop:

1. **Connect repo** — URL + access token (one-time setup)
2. **Trigger** — Part 1 events, a user-set schedule, or manual
3. **Detect** — issue detection runs scoped to triggering traces (existing
   pipeline, as a job under RFC-0002)
4. **Diagnose** — analysis job pins issues to code in the connected repo
5. **Fix** — coding agent receives diagnosis + failing traces, edits files,
   MLflow handles branch/commit/push/PR (harness never sees repo token)
6. **Review** — human reviews PR; reviewer comments loop back to agent
   (capped rounds); merge resolves issue in MLflow
7. **Regress** — failing traces become an evaluation dataset via
   `merge_records()`

Default harness: OpenCode (MIT, open source). Pluggable for Claude Code,
Codex, or custom. Inference runs on user's own model access (AI Gateway or
provider keys) — MLflow never runs managed inference for fixes. Nothing
merges without human review.

## Prompt drift path

When diagnosis points at a prompt rather than code, the fix path uses
MLflow's existing `optimize_prompts()` + prompt registry instead of a
coding agent. New prompt version registered with before/after scores.
Same pattern extends to skills via the Skill Registry once it lands.

## Registry integration (future)

As MCP Registry (RFC-0004), Skill Registry (PR #26), Extended Skill
Bundles (PR #27), and an eventual agent registry land, MLflow knows an
agent's composition. Diagnosis can then name the component (MCP server,
skill, or agent code) and route fixes to the right repo/registry.

## Key design decisions

- No auto-merge — every fix ends as a PR with human review
- No managed inference — MLflow never proxies fix generation
- Harness contract is small — harness edits files and exits; MLflow
  handles git, secrets, and the PR
- Server-side fix execution stays opt-in until RFC-0002 remote executors
  provide isolation; Copy-prompt path covers teams who want the loop today
