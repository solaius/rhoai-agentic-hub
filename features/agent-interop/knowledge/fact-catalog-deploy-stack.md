---
type: fact
title: 5-layer catalog deploy experience
description: Jehlum's proposed catalog experience stack — sandbox (OpenShell), harness packaging (connected/disconnected), platform integration (MCP/model/tracing), skills, deploy UX — everything except platform integration targets 3.6 EA1.
timestamp: 2026-07-12
tags: [agent-interop, agent-catalog, deploy-ux, architecture]
features: [agent-interop, agent-catalog]
source: Slack group DM Jehlum/Adel/Peter ~2026-07-12
review_after: 2026-10-12
---

Jehlum's bottom-to-top model for the catalog deploy experience
(post-Daniele meeting, ~2026-07-12):

1. **Sandbox runtime** — OpenShell provides the base execution layer.
   Adel adds: also want the UX around it (RHAIRFE-2310).
2. **Harness packaging** — two paths:
   - *Connected*: platform pulls the harness binary at runtime (users
     get latest), layered on top of the sandbox runtime.
   - *Disconnected*: AIPCC ships a baked image with harness included
     (accepted version lag) — skips step 1.
3. **Platform integration** — RHOAI MCP (or per-component MCP servers)
   deployed cluster-wide via operator. Harness connects to model
   discovery for MaaS models, MaaS key generation, MLflow tracing,
   EvalHub without manual config.
4. **Skills** — platform skills shipped in the harness reference the
   MCP layer above. Tested against the 5 models from the
   model-validation initiative. Adel: "shipped in the harness" UX
   still needs discussion; want to express "I want to use this skill
   in the catalog for my harness/agent" (RHAIRFE-2310 scope).
5. **Deploy UX** — catalog card, configure model endpoint +
   repo/workspace, one-click provision: sandbox + harness +
   MCP/credential injection, ready environment. Templates are
   extensible; non-template agents also in catalog. Templates expose
   configurable variables (RHAIRFE-2310 for BYO-type experience).

**Timeline**: everything except layer 3 (platform integration) targets
3.6 EA1. The connected path (layer 2) needs confirmation and tracking
with AIPCC + OpenShell team.
