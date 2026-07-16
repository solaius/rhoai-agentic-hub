---
type: fact
title: Agent Catalog 3.6 — supported images direction
description: 3.6 deployment = OpenShell Go SDK + supported harness images (OpenCode/Hermes favored; licensing flags on Claude Code/Antigravity); AIPCC base images ADR; staleness-vs-disconnected tension; skills "tested with models".
timestamp: 2026-07-16
tags: [agent-catalog, 3.6, supported-images, harnesses]
features: [agent-interop]
review_after: 2026-09-01
---

Where 3.6 deployment stands after the 2026-07-10 supported-images meeting
(Bill Murdock, Daniele Zonca, Jehlum Vitasta Pandit, Ann Marie Fred, Peter
Double) and the July forum threads:

- **Deploy path:** BFF → OpenShell Go SDK (Gage Krumbach: the SDK is "our
  blocker"; NVIDIA/OpenShell#2044; Roland Huss prototype
  rhuss/openshell-sdk-go). 3.5-deployed sandboxes remain read-only ghosts
  under 3.6 (no adoption — Derek Carr, 2026-07-14).
- **Supported images:** a limited, maintained set of harness images
  ([supported, not validated](/features/agent-catalog/knowledge/decision-supported-not-validated-images.md)).
  Candidates ([Jehlum's list](/features/agent-catalog/knowledge/ref-harness-candidates-gdoc.md)):
  OpenCode, Hermes (field interest incl. telco POCs), Codex, Pi, OpenClaw,
  Goose; Claude Code likely needs an Anthropic agreement, Antigravity a
  Google one. Peter's floor proposal: start with OpenCode + something like
  Hermes, rotating like validated models. Harness images via AIPCC =
  RHAIRFE-2443.
- **AIPCC base images:** ADR in GitLab (rhel-ai/core/team-docs MR 224,
  targeting 3.6) —
  [fit is questioned](/features/agent-catalog/knowledge/question-agent-catalog-aipcc-base-images-fit.md).
- **Bootstrap idea (Jehlum):** harness images preconfigured to work with the
  platform via a skill + the coming OpenShift AI MCP server, ideally through
  the MCP Gateway
  ([proposal](/features/agent-catalog/knowledge/ref-platform-skills-for-harnesses-gdoc.md));
  Bill flags the dual goal (platform-tools integration + initialized
  environment) as "really ambitious" for EA1. Related: an RHOAI assistant
  agent, possibly the harness backing Project Navigator.
- **Known tensions:** baked-in harnesses go stale within a month vs
  install-at-runtime breaking disconnected (self-contained images required;
  customers mirror images/NPM; skills-as-markdown could be PVC-mounted) —
  Ann Marie Fred: possibly "an unsolvable problem". OpenCode self-updates
  and may need patching/forking for disconnected. Skills ship at most as
  "tested with these models".
- **Explicitly deferred:** purpose-built plug-and-play agents (e.g. LangGraph
  RAG); anything crossing the
  [framework-support boundary](/features/agent-catalog/knowledge/question-agent-catalog-framework-support-boundary.md).

**Upstream reality check (research 2026-07-16, verified):** the Go SDK is
pre-merge — NVIDIA/OpenShell PR #2271 ("first PR in a 6-PR decomposition",
sandbox client only) was still open on 2026-07-16; the only complete
implementation is Roland Huss's personal-repo SDK (v0.2.2). OpenShell
itself is alpha (v0.0.x) with Kubernetes/OpenShift support flagged
experimental/evaluation-only (privileged SCC, TLS disabled). Naming note:
the upstream CRD kind is **`Sandbox`** in `agents.x-k8s.io`
(kubernetes-sigs/agent-sandbox) — "AgentSandbox" does not exist upstream
and appears to be product-discussion shorthand; confirm the actual kind and
the `openshell.ai/managed-by` label against live cluster objects. See
[02-upstream](/features/agent-catalog/research/02-upstream.md).
