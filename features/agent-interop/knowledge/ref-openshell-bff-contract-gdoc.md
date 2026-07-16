---
type: reference
title: Dashboard BFF - AgentSandbox/OpenShell contract (Gage)
description: The contract between the dashboard BFF and AgentSandbox/OpenShell for agent deployments — 3.5 list-only discovery, 3.6 Go-SDK deploy; being coalesced into an ADR.
resource: https://docs.google.com/document/d/19fARWUCbbksRC45uCwu3sygr82p43OUDER_ijH_GfMo
tags: [agent-interop, openshell, gdoc, bff]
features: [agent-catalog]
timestamp: 2026-07-16
---

Gage Krumbach's plan (2026-07-06 forum thread): 3.5 = read-only discovery of
AgentSandbox CRs labeled `openshell.ai/managed-by`; 3.6 = deploy via the
OpenShell Go SDK. The upgrade/adoption debate it spawned was closed
2026-07-14 (OpenShell cannot adopt resources it did not spawn — Derek Carr,
NVIDIA/OpenShell#2187); Gage to coalesce the thread into an ADR.
