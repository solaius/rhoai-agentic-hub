---
type: fact
title: OpenShell architecture
description: Supervisor-based sandbox model (no sidecar), kernel-level isolation (Landlock/seccomp/netns), driver model, gateway-centric; three-crate decomposition (proxy/runtime/sandbox).
timestamp: 2026-07-11
tags: [agent-interop, openshell, architecture]
review_after: 2026-09-11
source: GDoc "OpenShell Crate Decomposition", GDoc "Strategic Assessment" section 4, OpenShell RFC 0001
---

## Core model

OpenShell uses a **supervisor-based** architecture (no sidecar injection):

- **Supervisor** runs inside the sandbox alongside the agent
- **Driver model**: infrastructure-specific behavior behind explicit
  interfaces (compute, credentials, identity, sandbox identity)
- **Gateway-centric**: outgoing inference through the gateway; other
  outgoing requests through the supervisor proxy
- **Outbound-initiated**: supervisors connect to the gateway, not the
  other way around

## Isolation stack

- **Landlock LSM** -- filesystem restrictions (Linux 5.13+)
- **seccomp BPF** -- syscall filtering
- **Network namespaces** -- agent gets its own network stack
- **In-process OPA** (regorus, Rust) -- L4 TCP + L7 HTTP enforcement,
  hot-reloadable policies on running sandboxes
- Deny-by-default: proxy starts in deny-all mode

## Crate decomposition (RFC #1305)

Three crates forming a V-shaped dependency tree:

| Crate | Function | Size | Deployable standalone? |
|-------|----------|------|----------------------|
| **openshell-proxy** | Network policy enforcement (OPA, TLS interception, credential injection, inference routing) | ~12k lines (70%) | Yes (sidecar, standalone egress filter) |
| **openshell-runtime** | Linux process isolation (Landlock, seccomp, namespace, SSH) | ~4k lines | No (library only) |
| **openshell-sandbox** | Thin composition glue (gRPC to gateway, wires proxy + runtime) | ~3k lines | Yes (single-container, status quo) |

Proxy and runtime have **zero dependency** on each other.

## Deployment topologies

- **Topology A (status quo)**: single container, proxy + runtime in-process
- **Topology B**: gVisor/Kata sidecar -- proxy in trusted pod, agent in
  gVisor/Kata RuntimeClass (no elevated privileges needed)
- **Topology C**: standalone egress filter -- proxy only, no runtime

## Credential flow (key principle)

Usable credentials **never enter the sandbox**. Agent makes a request;
proxy intercepts at network layer; evaluates against OPA policy; if
allowed, injects credentials into request headers. Agent never sees
plaintext credentials.
