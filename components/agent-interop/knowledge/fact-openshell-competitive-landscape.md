---
type: fact
title: OpenShell competitive landscape
description: 11 competitors analyzed (E2B, Modal, Cloudflare, Docker, ACA, KARS, AHP, Lynx, CubeSandbox, OneCLI, Substrate); OpenShell is the only system covering isolation+behavioral+credentials; per-binary policy is the unique differentiator.
timestamp: 2026-08-03
tags: [agent-interop, openshell, competitive, positioning]
review_after: 2026-10-15
source: gitlab.cee.redhat.com/azaalouk/openshell-strategy/competitive_positioning/ (Jul 2026, v0.0.90)
---

## Core differentiator

The "which binary opened that socket?" question. No other system provides
per-binary network policy via HTTP CONNECT proxy + `/proc` inspection +
SHA-256 TOFU. This plus credential-free inference routing, L7 TLS MITM
inspection, and denial intelligence (aggregation + mechanistic mapper +
policy proposals) is unique to OpenShell.

## Competitor positioning (one-liners)

| Competitor | Positioning line |
|------------|-----------------|
| **E2B** | "They set the cold start bar (78ms); we set the security bar." |
| **Modal** | "Modal owns GPU density ($4.65B). We own what happens inside the sandbox." |
| **Cloudflare** | "They solve DX (Flue SDK + V8 isolates); we solve compliance." |
| **Docker Sandboxes** | "Great for your laptop. OpenShell is what compliance requires for production." |
| **Microsoft ACA** | "Can AGT tell you which binary made that HTTP request?" |
| **Microsoft KARS** | "KARS is the starting point. OpenShell is the upgrade." |
| **Microsoft AHP** | "UX protocol, not security protocol. Complementary." |
| **Tigera Lynx** | "If we ship fleet governance first, competitor. If we don't, partner." |
| **Tencent CubeSandbox** | "Answers 'how fast can I boot?' not 'what is the agent doing inside?'" |
| **OneCLI** | "Covers same 4 paths. Ask: what happens when the agent reads .env directly?" |
| **Agent Substrate** | "Which gate is the customer stuck at?" (gate 1 security vs gate 3 scale) |

## Layer coverage matrix

No competitor covers more than 2 of the 3 critical layers. OpenShell
covers all three: isolation + behavioral security + credential management.

| Layer | OpenShell | Docker | Cloudflare | E2B | Modal | ACA | Others |
|-------|-----------|--------|------------|-----|-------|-----|--------|
| Kernel isolation | Landlock, seccomp | MicroVM | V8/VM | Firecracker | gVisor | Hyper-V | varies |
| Per-binary policy | OPA/Rego + /proc | -- | -- | -- | -- | -- | -- |
| Credential security | Proxy + SPIFFE + STS | Proxy injection | Bindings | BYOC | N/A | Entra + MCP GW | varies |
| L7 inspection | TLS MITM | -- | -- | -- | -- | -- | Lynx (Cedar) |
| Denial intelligence | Aggregation + mapper | -- | -- | -- | -- | -- | -- |

## Strategic implications

- Docker is the closest competitor in depth (5-layer defense-in-depth)
  but lacks per-binary policy and targets laptop, not production K8s
- Lynx (Tigera) is a potential partner or competitor depending on who
  ships fleet governance first
- E2B and Modal set the cold-start and scale expectations that OpenShell
  must match (warm pools, sub-second startup)
- KARS is MIT-licensed and K8s-native -- watch for enterprise adoption
  as a "good enough" lightweight alternative

Full per-competitor deep dives in the strategy repo:
`competitive_positioning/<name>-vs-openshell.md`
