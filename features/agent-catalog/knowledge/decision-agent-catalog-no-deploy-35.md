---
type: decision
title: No deploy button in 3.5 — catalog links out to GitHub
description: AgentDev sync 2026-07-09 — 3.5 ships a read-only catalog (no deploy, no agent-card discovery, no rich detail page); agents table discovers AgentSandbox CRs; deployment moves to 3.6.
decided: 2026-07-09
timestamp: 2026-07-16
tags: [agent-catalog, 3.5, scope]
features: [agent-interop]
---

**Context.** Starter kits are not built images — images would come from AIPCC
(RHAIRFE-2443) and don't exist for all harnesses. Peter Double's 2026-07-08
question in #forum-ai-asset-management ("if starter kits are not built
images… is there no deployment from catalog?") forced the call; Adel Zaalouk:
"having a deploy button in the catalog wouldn't mean much if there is nothing
to deploy in 3.5." It was also simply too late in the 3.5 cycle (Bill
Murdock, 2026-07-10).

**Decision** (AgentDev sync: Adel Zaalouk, Peter Double, Aakanksha Duggal,
Bill Murdock; ratified by Gage Krumbach and Andrew Ballantyne). RHOAI 3.5
ships: catalog cards for starter kits that link out to their GitHub repos —
no deploy button, no agent-card (`/.well-known/agent-card.json`) discovery,
no rich detail page; plus a read-only agents table discovering AgentSandbox
CRs carrying the `openshell.ai/managed-by` label. Starter kits ship without
images. Deployment from the catalog stays alive for 3.6.

**Consequences.** Nothing ships in 3.5 that must be maintained (no images);
the deploy-backend discussion (OpenShell Go SDK, supported images) moves
wholly to 3.6; dashboard/BFF work continues unchanged (Alessio Pragliola:
"no changes/delays from our side"); 3.5-deployed sandboxes become read-only
"ghost" agents under 3.6 OpenShell — no migration path (Gage Krumbach option
2b, 2026-07-09; Derek Carr closed the adoption question 2026-07-14: OpenShell
cannot adopt resources it did not spawn).
