---
type: fact
title: OpenShell TP scope (3.6 EA1/EA2)
description: Technology Preview deliverables for 3.6 EA1 (Sep 17) and EA2 (Oct 15) -- 12 upstream beta gates, 11 downstream deliverables, deferred items, RFEs needing STRATs. Upstream Beta Sep 15 is the critical gate.
timestamp: 2026-08-03
tags: [agent-interop, openshell, tp, scope, rfe]
components: [agent-interop]
review_after: 2026-09-17
source: gitlab.cee.redhat.com/azaalouk/openshell-strategy/technology-preview-3.6.md (Jul 28)
---

## Upstream beta gates (must land by Sep 15)

High-risk items flagged:

| Item | Upstream issue | Risk |
|------|---------------|------|
| Multi-tenancy (workspaces) | #1722, #1980 | No assignee on RFC |
| HA on Kubernetes | #1021 | **High**: assignee (TaylorMutch) leaving, needs handoff |
| Sandbox log collection | #1922 | **Risk**: same assignee leaving |
| Warm pools | #1879 | Not in milestone, Derek confirmed beta requirement |
| Stable gRPC API | #1613, #1955 | Stale |

Items with open PRs (risk reduced as of Jul 28): credential storage
drivers (#2454), warm pools (#2460), blackbox images (#2476), HA (#2489).

## Downstream TP deliverables (Red Hat ships in 3.6 EA1)

| Deliverable | RFE | Depends on beta |
|-------------|-----|-----------------|
| UBI10 container images (Gateway, Supervisor, Sandbox, CLI) via Konflux | RHAIRFE-2443 / RHAISTRAT-2067 | No |
| Downstream build pipeline, weekly images, NVIDIA telemetry removal | RHAIRFE-2679 | No |
| OpenShell operator | RHAIRFE-2572 / RHAISTRAT-1752 | Yes (multi-tenancy, HA) |
| Go SDK upstream push | RHAIRFE-2623 | No |
| Identity: SPIFFE token exchange with Keycloak | RHAIRFE-2567 | Yes (Gordon's PR) |
| Identity: inbound caller auth | RHAIRFE-2568 | Yes (#2143) |
| Identity: protocol-aware inbound policy | RHAIRFE-2569 | Yes (#2144) |
| OTEL tracing into managed MLflow | RHAIRFE-794 | No |
| Downstream CI for upstream PRs on OCP | Needs RFE | No |
| Declarative agent deployment | RHAIRFE-2310 / RHAISTRAT-2148 | Yes (operator, images) |
| Governed execution environments (admin UI) | RHAIRFE-2984 | Yes (workspaces) |

## RFEs needing STRATs

RHAIRFE-2623 (Go SDK), RHAIRFE-2567 (identity delegation),
RHAIRFE-2568 (inbound caller auth), RHAIRFE-2569 (protocol-aware policy),
RHAIRFE-2984 (governed execution environments).

## RFEs still needed

Multi-tenancy (workspaces), stable gRPC API, downstream CI for OCP,
database selection (decision doc).

## Deferred past TP

3.6 EA2 or GA: TypeScript SDK, SSH/non-HTTP proxy, phantom token
beyond inference, credential driver (Vault/K8s), policy hierarchy,
OpenShift internal OAuth mismatch, disconnected install, multi-arch,
pluggable IdP, GitOps policy-as-code, harness gateway sandboxing.

Post-3.6: TEE (SGX/TDX), graduated autonomy, scheduled execution,
event log/crash recovery, memory integrity, inference content
inspection, config/skill attestation (Sigstore), outbound DLP,
sub-agent sandbox hierarchy.

Full detail in strategy repo: `technology-preview-3.6.md`
