---
type: reference
title: "[Outcome] Implementation of Consistent Agentic APIs"
description: Outcome delivering multi-protocol agentic API layer (OpenAI Responses, Anthropic Messages, Google Interactions) against a single Red Hat inference backend; In Progress.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-1073
tags: [ai-gateway, outcome, agentic-api]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Parent Outcome for the consistent agentic API surface that Praxis
implements. Covers OpenAI API conformance (Completions, Responses,
tool calling), Anthropic Messages protocol, Google Interactions
protocol, agent SDK compatibility (Claude Code, Codex, LangGraph),
and sandboxed container execution. Absorbed RHAISTRAT-1347 (Anthropic
Messages) and RHAISTRAT-1348 (Google Interactions). Links to
RHAISTRAT-1054 (Responses API TP) and RHAISTRAT-1217 (Responses
API parity).
