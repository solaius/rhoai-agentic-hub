---
type: reference
title: "Agent Improvement RFC — PR #1"
description: Nehanth's two-part MLflow RFC for self-healing agents — trace-aware webhook events (Part 1) and a coding-agent-driven improvement workflow (Part 2).
timestamp: 2026-08-07
tags: [agent-ops, mlflow, self-healing, upstream]
components: [skills-registry]
uri: github:Nehanth/agent-improvement-rfc#1
resource: github:Nehanth/agent-improvement-rfc/pull/1
---

PR by Nehanth Narendrula (App Dev team). Two documents following the
mlflow/rfcs template, ready to lift into that process once an enhancement
issue is filed.

- **Part 1 — Trace-Aware Webhook Events**: extends MLflow's 15 registry/budget
  webhook events with four observability-side events (eval threshold breach,
  issue detection created/updated, trace errored). No new background services.
- **Part 2 — Improvement Workflow**: Improve tab in the experiment UI. Connect
  a repo, issue detection diagnoses failures against source, a coding agent
  (OpenCode bundled, any harness pluggable) opens a PR with trace evidence.
  Human reviews everything. Fixed failures become regression eval datasets.

Builds on existing MLflow capabilities: tracing, automatic evaluations, issue
detection, prompt registry, MLflow Assistant, MCP server, job executor
framework (RFC-0002). Registry integration (MCP RFC-0004, Skill Registry
PR #26, Extended Skill Bundles PR #27) enables component-level diagnosis
as those land.
