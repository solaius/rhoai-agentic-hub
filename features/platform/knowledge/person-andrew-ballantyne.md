---
type: person
title: Andrew Ballantyne
description: Dashboard architect — owns the Model→MCP→Agent catalog UI pattern, made the no-admin-UI-in-3.5 call; pushes back on forcing flows through the registry.
role: Dashboard Architect
org: RHOAI Dashboard/UI
timestamp: 2026-07-16
tags: [platform, dashboard]
features: [agent-catalog]
---
Framed the Agent Catalog as "v3" of the Model Catalog → MCP Catalog pattern
(2026-06-04); cut the agent-catalog admin/settings UI from 3.5 (2026-06-18,
reconfirmed 06-22 — MCP admin UI took priority, "Green 3.5 stable plan is
getting hefty"). In the catalog/registry/deployments platform debate, argues
GitOps/`oc apply` flows can't be policed through a registry
([open question](/features/agent-catalog/knowledge/question-agent-catalog-register-vs-deploy.md)).
