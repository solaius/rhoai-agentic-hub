---
type: reference
title: Agent Registry Product -- Scoping/Discussion (Adel Zaalouk)
description: Adel Zaalouk's product scoping doc for Agent Registry in RHOAI -- defines scope (discover/register/audit), customer problems (P1-P11), competitive landscape, phased delivery (3.5/3.6/3.7+), A2A schema adoption, MLflow backend, catalog-as-view, what we don't build, and connection to Skills/MCP registries and OpenShell.
resource: https://docs.google.com/document/d/1hqW1HrqWJw7R90irulIIAxTy-_vP7eM7g_IsNbbNmkE
timestamp: 2026-08-03
tags: [agent-registry, product-scope, a2a, mlflow]
components: [agent-catalog, agent-interop, skills-registry]
---
Comprehensive product scoping document authored by Adel Zaalouk. Key sections:

- **TL;DR** -- registry as governed inventory; catalog is read-only view;
  A2A schema as metadata format; MLflow backend; templates reduce shadow IT;
  11 customer-validated problems from 10+ enterprise customers.
- **What We're Enabling** -- single pane of glass for agent definitions AND
  runtime state; registry vs. deployments view distinction.
- **Customer Problems** -- Tier 1 foundation (P1-P6: duplication, visibility,
  safety, shadow IT, routing, templates) and Tier 2 FSI production blockers
  (P7-P11: CVE blast radius, accountability, policy visibility, cross-cluster,
  cost). See restricted/ for customer names and quotes.
- **End Behaviors** -- Discover, Register, Audit as the three user journeys.
- **What We Build** -- discover (search by capability/owner/namespace/skill),
  register (SDK/CLI/UI, runtime state reflection, template-driven onboarding),
  audit (queryable metadata, ownership chains, vulnerability blast radius).
- **What We Don't Build** -- deployment system, observability platform,
  per-agent cost management, cross-cluster federation (MVP), shadow IT
  auto-detection (MVP), proprietary identity system, proprietary metadata format.
- **Competitive Landscape** -- Google (GA, most mature), AWS (preview),
  Microsoft (Agent 365 GA), IBM (Agentic Control Plane), Databricks (Unity
  Catalog), OSS (Solo.io, AGNTCY, NANDA, ARD). Gap: no self-hosted hybrid
  agent registry across clouds and edge.
- **Phased Delivery** -- 3.5 (templates, metadata schema, MLflow MCP Registry),
  3.6 (Agent Registry RFC + RHOAI implementation + dashboard + template onboarding),
  3.7+ (shadow IT, policy enforcement, cross-cluster, federation).
- **Reviewer comments** -- Jiri Danek raised versioning for non-deterministic
  systems, dependency permanence, visibility scoping, and the zombie agent paradox.

Cross-references:
- [ref-agent-registry-mocks](/components/agent-registry/knowledge/ref-agent-registry-mocks.md)
- [ref-skills-scoping-gdoc](/components/skills-registry/knowledge/ref-skills-scoping-gdoc.md)
- [fact-agent-registry-product-scope](/components/agent-registry/knowledge/fact-agent-registry-product-scope.md)
- [decision-agent-catalog-is-registry-view](/components/agent-registry/knowledge/decision-agent-catalog-is-registry-view.md)
