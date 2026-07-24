---
type: question
title: Should 3.6 EA1 deploy support flow-import agents or descope to config-driven only?
description: flow-import agents (Langflow) require a completely different deploy backend (provision/locate a platform instance + import flow JSON) alongside the OpenShell container path -- should 3.6 EA1 support both or descope?
status: open
timestamp: 2026-07-24
tags: [agent-catalog, deploy, 3.6, flow-import]
---
The 3.6 deploy wizard targets config-driven agents via BFF -> OpenShell Go
SDK -> AgentSandbox CR -> pod. flow-import agents (currently only Langflow)
need a fundamentally different mechanism: provision or locate a Langflow
instance, import the flow definition JSON, and configure infrastructure-
level env vars.

Supporting both in EA1 means two deploy backends, two wizard UX branches,
and two sets of env-var handling. Supporting only config-driven in EA1 is
lower-risk (13 of 15 kits are config-driven, including all harness kits)
and defers the visual-builder-platform integration question.

If descoped, flow-import agents remain browse-only in the catalog (card
links to GitHub, same as 3.5) -- no broken UX, just no deploy button on
those cards.

Raised by
[research doc 06](/features/agent-catalog/research/06-requirements-deployment-model-metadata.md).
Related:
[question-agent-catalog-register-vs-deploy](/features/agent-catalog/knowledge/question-agent-catalog-register-vs-deploy.md),
[fact-deployment-model-metadata-gap](/features/agent-catalog/knowledge/fact-deployment-model-metadata-gap.md).
