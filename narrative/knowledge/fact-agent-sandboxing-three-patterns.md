---
type: fact
title: "Three patterns for agent sandboxing"
description: "Adel's three sandboxing patterns: (1) whole-process micro-VM isolation, (2) per-session/sub-agent isolation, (3) developer SDK-level primitives. OpenShell is the upstream project."
timestamp: 2026-07-08
source: Power 90 session 2026-07-08
features: [agent-ops]
tags: [narrative, security, sandboxing]
---
From Adel's Power 90 presentation, agent sandboxing has three patterns:

**Pattern 1 — Whole-process sandbox:** put the entire agent process in a
micro-VM (Kata Containers). Pros: strong hardware isolation. Cons: single
point of failure — if the agent process fails, so does the execution
environment. Suitable for stringent security use cases.

**Pattern 2 — Per-session/sub-agent isolation:** the agent loop can spin
up separate processes for sessions, sub-agents, and tool execution — each
in its own sandbox. Avoids single point of failure. The agent session is
a "flavor" of the agent (class vs instance analogy). Key questions: how
to carve execution environments per session, how to sandbox tool
execution separately from the agent itself.

**Pattern 3 — Developer SDK-level:** if the developer has code control,
they can use sandboxing primitives via SDK/API directly. For those
without control, fall back to patterns 1 or 2.

**OpenShell** is the upstream project implementing all three patterns.
Started with process-level sandboxing (syscall filtering, file
permissions, DNS/URL whitelisting, network policy) and is growing to
support session-level and SDK-level primitives. OpenClaw natively supports
OpenShell today. Planned for product integration end of 2026.

Existing platform primitives reused: SCCs, SELinux, network policies,
Kata Containers (sandbox containers since 2021).
