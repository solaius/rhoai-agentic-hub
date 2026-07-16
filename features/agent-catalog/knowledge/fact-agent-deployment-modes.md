---
type: fact
title: Agent deployment modes (Mode 1 / Mode 2) and the declarative harness
description: Mode 1 = bring-your-own image + sidecars by contract; Mode 2 = platform-owned deploy of supported harness images with declarative binding to the platform registries; agentic API surface underneath.
timestamp: 2026-07-16
tags: [agent-catalog, modes, declarative-harness, architecture]
features: [agent-interop, agent-registry]
---

Adel Zaalouk's framework (packaging meeting 2026-06-01):

- **Mode 1 — bring your own agent.** Developer builds the image and the
  Deployment; the platform points the agent-runtime CR at it and attaches
  sidecars: SPIFFE/SPIRE identity, token exchange/scoping, MLflow tracing via
  platform-set env vars. The contract is documentation (don't hardcode
  telemetry/tracing endpoints; take config from env).
- **Mode 2 — platform-owned.** Off-the-shelf harnesses (OpenCode, OpenClaw,
  Hermes, Claude Code…) deployed by the platform from supported images with
  known entry points; the user supplies only configuration ("user harness"
  vs "builder harness"). **Binding** connects that declared configuration to
  the platform inventories — skills registry, MCP registry, model catalog —
  the declarative harness (RHAIRFE-2310 declarative agent deployment,
  RHAIRFE-2309 platform binding;
  [proposal doc](/features/agent-interop/knowledge/ref-declarative-harness-proposal-gdoc.md)).
  Cloning the repo and editing code moves you to Mode 1 (Ann Marie Fred:
  Mode 2 is ops-lifecycle only; template building is dev-lifecycle —
  Backstage's territory).

Underneath, the platform implements an **agentic API surface** — Anthropic
Messages API and OpenAI (responses) API — so harnesses run against platform
models with runtime model-name translation.

Catalog vs registry in this frame (Adel): the catalog is where you discover
seeds/templates; a configured, deployed instance (same seed, different
model/MCP/skills) is a **version** that belongs in the agent registry —
[agent-registry](/features/agent-registry/index.md) scope, backend targeted
3.6 EA2 (RHAISTRAT-1436). Bill Murdock flagged the full declarative binding
as "extremely ambitious" for 3.6.
