---
type: fact
title: OpenShell product timeline (RHOAI integration)
description: Concrete milestones for OpenShell in RHOAI -- DP Aug 20 (3.5), upstream Beta Sep 15, TP Sep 17/Oct 15/Nov 19 (3.6 EA1/EA2/GA), OpenShell GA early 2027.
timestamp: 2026-08-03
tags: [agent-interop, openshell, timeline, roadmap]
review_after: 2026-09-15
source: gitlab.cee.redhat.com/azaalouk/openshell-strategy README.md (Jul 28)
---

## Key milestones

| Date | Milestone |
|------|-----------|
| Aug 20, 2026 | RHOAI 3.5 GA -- OpenShell **Dev Preview** |
| Aug 21, 2026 | 3.6 EA1 code freeze |
| Sep 3, 2026 | NVIDIA IT stability checkpoint |
| Sep 15, 2026 | OpenShell upstream **Beta** / NVIDIA customer zero on Astron |
| Sep 17, 2026 | RHOAI 3.6 EA1 GA |
| Oct 3, 2026 | GTC Berlin (NVIDIA presentation) |
| Oct 15, 2026 | RHOAI 3.6 EA2 GA |
| Nov 19, 2026 | RHOAI 3.6 GA |
| Early 2027 | OpenShell **GA** |

## What ships per milestone

**Dev Preview (3.5, Aug 20):** Documentation + validated upstream
experience. Pinned upstream version, install guide, enablement blog
series. No downstream images, no operator, no SDK delivery. Architect
sign-off granted Jul 22.

**Technology Preview (3.6 EA1/EA2):** Productized downstream artifacts.
UBI10 images via Konflux with weekly builds. Operator. Go SDK. Identity
(SPIFFE token exchange). Governed execution environments
(RHAIRFE-2984). Sub-second cold-start via warm pools.

**GA (3.7, early 2027):** Full support. Disconnected install, multi-arch,
pluggable IdP, GitOps policy-as-code, harness gateway sandboxing.

## Critical gate

Upstream Beta (Sep 15) is the prerequisite for TP. If Beta slips,
corresponding TP deliverables slip to 3.6 EA2 or GA. Two days between
Beta (Sep 15) and EA1 GA (Sep 17) is extremely tight.

## Dependencies

- Agent Sandbox TP readiness (KATA-4728)
- kubernetes-sigs/agent-sandbox went v1beta1 but API still changing
- Upstream Beta milestone: 21 open issues, 9 closed (as of Jul 28)
