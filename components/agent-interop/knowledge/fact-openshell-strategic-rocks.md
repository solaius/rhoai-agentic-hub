---
type: fact
title: OpenShell strategic rocks (R1-R8)
description: 8 mission-driven strategic priorities for OpenShell with sequencing -- Immediate (R4+R1+R3+R3b), Next (R5+R2), Then (R7), Continuous (R6+R8). Weekly cadence per rock.
timestamp: 2026-08-03
tags: [agent-interop, openshell, strategy, rocks]
review_after: 2026-10-01
source: gitlab.cee.redhat.com/azaalouk/openshell-strategy/rocks/ (Jul 28)
---

## The 8 rocks

| Rock | Mission statement | Key outcome |
|------|------------------|-------------|
| **R1** | OpenShell is easy to consume | SDKs (Python/Go/TS), warm pools, blackbox images, policy presets, sub-second cold start |
| **R2** | OpenShell composes with the ecosystem, not competes | Agent Substrate positioning, kubernetes-sigs/agent-sandbox relationship, Providers v2 |
| **R3** | Agents never touch a raw secret | Provider credential lifecycle, credential bifurcation (trusted/untrusted in same sandbox) |
| **R3b** | Sandboxes have verifiable identity and scoped access | SPIFFE token exchange, inbound caller auth, protocol-aware policy (A2A/MCP) |
| **R4** | Supervisor and agent are separate security domains | Binary split (proxy/runtime/sandbox crates), sidecar topology |
| **R5** | OpenShell's core is stable and reliable | HA, stable gRPC API, consistent data model, management APIs, downstream CI |
| **R6** | Red Hat teams choose OpenShell because it works | Internal dogfooding -- Full Send, Ansible AO, RHOAI Dashboard, OpenClaw |
| **R7** | OpenShell is shippable as a supported Red Hat product | Operator, UBI10 images, Konflux pipeline, NVIDIA telemetry removal, CLI distribution, database selection |
| **R8** | Coding agent harnesses work end-to-end on OpenShell | Harness integration validation (Claude Code, Codex, OpenCode, Gemini CLI, OpenClaw) |

## Sequencing (as of Jul 28, 2026)

**Immediate (R4 + R1 + R3 + R3b):** Binary split (blocks operator,
provenance, OCP acceptance). In parallel, consumption surface (SDKs,
file transfer, blackbox images, SSH proxy, policy presets). Credential
lifecycle + bifurcation. SPIFFE identity + token exchange.

**Next (R5 + R2):** Stabilize core (HA, data model, management APIs).
Define ecosystem positioning (Agent Substrate, agent-sandbox SIG).

**Then (R7):** Productization (operator, images, telemetry, disconnected,
multi-arch). Depends on R4 (binary split) and R5 (stable APIs).

**Continuous (R6 + R8):** Dogfooding runs every week. Harness validation
alongside R1 and R4 -- every horizontal capability tested against a
real harness integration.

## Key sequencing change (Jun 12)

R1 moved from "Next" to "Immediate" based on T1 evidence: 5 teams
blocked on SDK gaps. Every major framework ships a sandbox provider
interface. If OpenShell is harder to consume than E2B, it loses the
integration.

## Operational risks (Jul 15 Core Team sync)

- Taylor leaving with no backfill (networking expertise gap)
- Fragmented internal calls (multiple forums discussing OpenShell in isolation)
- NVIDIA GitHub org migration stalled (CI visibility, downstream complexity)
- CAP 972 suspend/resume needs urgent Red Hat input
- OASIS attestation standard imminent (identity model R3b impact)

Full rock detail in strategy repo: `rocks/r1-*.md` through `rocks/r8-*.md`
