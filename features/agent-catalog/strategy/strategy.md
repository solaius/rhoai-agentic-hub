---
title: "Agent Catalog — strategy"
description: The living strategy for the agent storefront — starter-kit templates in 3.5, supported-images deploy via OpenShell in 3.6 EA1, registry hand-off, the gaps that need owners, and the candidate jiras.
timestamp: 2026-07-16
status: current
review_after: 2026-09-14
source: hub.strategy pilot run 2026-07-16 — inputs, knowledge partition (intake + verified research atoms), research 00-05, jira-snapshot (37 issues, swept 2026-07-16), roadmap/strategy profiles, agent-registry + agent-interop siblings
---

## The brief

The Agent Catalog is the agent storefront in AI Hub — third catalog on the
Model → MCP pattern, kubeflow/hub backend. **The bet: a small catalog of
things Red Hat actually supports, deployable disconnected, beats
hyperscaler listing counts — support is the product.** 3.5 DP ships
read-only: RH-curated starter-kit cards linking out to GitHub (no deploy —
[decided 2026-07-09](/features/agent-catalog/knowledge/decision-agent-catalog-no-deploy-35.md));
OpenAPI merged, BFF in build, field set final. Next milestone: 3.5 DP out,
then 3.6 EA1 deploy through the OpenShell Go SDK — which is still
pre-merge upstream, the single load-bearing risk. The live fights: which
harnesses become supported images (and who owns them), and whether Deploy
registers.

## What

| release | scope | status |
|---|---|---|
| 3.5 DP | Read-only catalog: starter-kit cards from [agentic-starter-kits](/features/agent-catalog/knowledge/ref-agentic-starter-kits-repo.md) → GitHub link-out; read-only deployments view (sandbox-CR discovery); YAML catalog source baked for disconnected; no deploy button, no agent-card discovery, no admin UI ([scope](/features/agent-catalog/knowledge/fact-agent-catalog-35-scope.md)) | In build — OpenAPI merged 2026-07-03 (kubeflow/hub #2907), [field set final 2026-07-02](/features/agent-catalog/knowledge/decision-agent-catalog-35-field-set.md), BFF show-and-tell ~2026-07-17 |
| 3.6 EA1 | Deploy from the detail page, [supported images only](/features/agent-catalog/knowledge/decision-agent-catalog-deploy-supported-images-only.md): BFF → OpenShell Go SDK; declarative binding (RHAIRFE-2309/2310) aspirational — descope path is deploy-with-manual-config ([direction](/features/agent-catalog/knowledge/fact-agent-catalog-36-supported-images.md)) | Planned — SDK pre-merge upstream |
| 3.6 EA2+ | Agent Registry — work starts here at the earliest, multi-release to DP (~3.7 EA1 directional); a configured deployed instance becomes a registry version, and deploy-time registration is the registry's rich discovery path ([sibling](/features/agent-registry/knowledge/fact-agent-registry.md)). Deployment itself is a separate workstream both features consume | Not started (RHAISTRAT-1436 unscheduled, agent-registry scope) |
| Later | Harness playground/chat ([question](/features/agent-catalog/knowledge/question-agent-catalog-harness-playground-integration.md)), purpose-built agents, eval/validated tier (RHAISTRAT-1792) | Deferred |

**Boundaries.** Not the runtime (sandboxing/identity/deploy mechanics →
[agent-interop](/features/agent-interop/index.md)); not
versioning/governance of deployed agents →
[agent-registry](/features/agent-registry/index.md); UI/backend pattern
sibling → [mcp-catalog](/features/mcp-catalog/index.md). This partition
owns the catalog surface: starter kits as content, metadata schema,
discovery UX, the supported-images program, release train.

## Why

The platform ships agent runtime primitives (sandbox, identity, tracing)
but no governed path from "what agents exist?" to "one is running" — the
agentic story is incomplete without the discover→deploy front door the
model and MCP catalogs already provide. Jobs: day-zero start for the
ai-engineer, a curated golden path for the platform-engineer, the
inventory seed for the agentops-admin
([personas](/features/platform/knowledge/fact-personas.md), [requirements
research](/features/agent-catalog/research/04-requirements.md)).

Market ([position](/features/agent-catalog/knowledge/fact-agent-catalog-market-position.md)):
our template→deployable→registry sequencing is the industry pattern
(Microsoft's Foundry catalog IS our 3.5 shape; Databricks ships our
catalog→MLflow-registry architecture) — validated, and 12–18 months
behind first movers. The wedge is what no cloud vendor ships: **supported,
self-run harness images on an open, disconnected-capable platform with
governance built in** — NVIDIA's free-blueprints/paid-support tier proves
the model sells; IBM (on OpenShift) is the coopetitor above our layer.
Analysts reward exactly this posture (Gartner's agent-washing backlash,
Forrester's governance-decides finding). The wedge is time-boxed — Gemini
already runs GA air-gapped — so it must be claimed in the 3.6 cycle, and
EU AI Act transparency (2026-08-02) makes deploy-seeded inventory a
regulatory tailwind ([enterprise requirements](/features/agent-catalog/knowledge/fact-supported-images-enterprise-requirements.md)).

## Where we stand

Decisions, in order:
[supported-images-only deploy MVP](/features/agent-catalog/knowledge/decision-agent-catalog-deploy-supported-images-only.md)
(2026-06-01) · YAML catalog source for disconnected (2026-06-08, in
[3.5 scope](/features/agent-catalog/knowledge/fact-agent-catalog-35-scope.md)) ·
no admin UI in 3.5 (2026-06-18/22) ·
[3.5 field set](/features/agent-catalog/knowledge/decision-agent-catalog-35-field-set.md)
(2026-07-02) ·
[no deploy in 3.5](/features/agent-catalog/knowledge/decision-agent-catalog-no-deploy-35.md)
(2026-07-09) ·
["supported", not "validated"](/features/agent-catalog/knowledge/decision-supported-not-validated-images.md)
(2026-07-10).

Delivery: backend live in kubeflow/hub (spec #2907 merged, agent.yaml via
the artifacts endpoint #2928 — [upstream schema](/features/agent-catalog/knowledge/fact-agent-catalog-upstream-schema.md));
dashboard/BFF build started post-merge; 12 framework kit directories with
agent.yaml gaps closing; [deployment-modes model](/features/agent-catalog/knowledge/fact-agent-deployment-modes.md)
(Mode 1/Mode 2 + binding) agreed. Research: 5 lenses, adversarially
verified ([00-executive-summary](/features/agent-catalog/research/00-executive-summary.md)).

## Gaps & risks

1. **OpenShell Go SDK is a single unmerged dependency** — PR series A-of-6
   open, alpha runtime, OpenShift install evaluation-only; the whole 3.6
   deploy path rides it. Descope decision needed by EA1 planning if it
   slips ([research 02](/features/agent-catalog/research/02-upstream.md)).
2. **Supported harness set undecided** — licensing is now fact (Claude
   Code prohibited, Codex Apache-2.0), 4/5 open candidates self-update
   against image pinning ([question](/features/agent-catalog/knowledge/question-agent-catalog-supported-harness-set.md)).
3. **Nobody owns the image treadmill** — Health Index grading, CVE SLAs,
   Konflux attestation all attach automatically; ownership is "AgentDev
   near-term" only ([question](/features/agent-catalog/knowledge/question-agent-catalog-ownership-packaging.md)).
4. **AIPCC base-image fit unresolved** — ADR targets 3.6 while catalog
   contents churn ([question](/features/agent-catalog/knowledge/question-agent-catalog-aipcc-base-images-fit.md)).
5. **Register-vs-deploy stance open platform-wide** — evidence favors
   "deploy always registers, reconcile the rest," and the re-baselined
   registry proposal now names deploy-time registration its rich path —
   the two features need the same answer ([question](/features/agent-catalog/knowledge/question-agent-catalog-register-vs-deploy.md)).
6. **Product↔upstream schema divergence** — protocol/models/imageVersion
   are untyped customProperties upstream; the filter UX has no typed
   contract ([fact](/features/agent-catalog/knowledge/fact-agent-catalog-upstream-schema.md)).
7. **Sandbox-vs-AgentSandbox naming unconfirmed** — upstream kind is
   `Sandbox`; the product shorthand needs reconciling against live
   cluster objects before the deployments view hardens.
8. **Starter kits vs quick starts boundary** — the golden-path checklist
   (one-command run, sizing, eval hook, pre-wired binding) is what keeps
   kits from being "glorified quick starts" ([question](/features/agent-catalog/knowledge/question-agent-catalog-quickstarts-overlap.md));
   card accuracy is a requirement, not polish (catalog trust is fragile).

## Jira map

| strategy element | keys | status |
|---|---|---|
| Catalog surface (3.5) | [RHAISTRAT-1740](/features/agent-catalog/knowledge/ref-rhaistrat-1740.md) (Feature) | In Progress |
| Agent Hub UI umbrella | [RHAISTRAT-1697](/features/agent-catalog/knowledge/ref-rhaistrat-1697-agent-hub-ui.md) (Outcome) | In Progress — framing predates the OpenShell pivot |
| Deploy-write path (3.6) | [RHAISTRAT-1742](/features/agent-catalog/knowledge/ref-rhaistrat-1742-deploy-from-ai-hub.md) (Feature) | In Progress |
| Deployments view (3.5) | [RHAISTRAT-1758](/features/agent-catalog/knowledge/ref-rhaistrat-1758-agent-deployments-view.md) (Feature) | In Progress |
| Supported images / runtime compat | [RHAISTRAT-1349](/features/agent-catalog/knowledge/ref-rhaistrat-1349-runtime-compatibility.md) (Outcome) + RHAIRFE-2443 | In Progress — image-tier naming predates the supported ruling |
| Eval / validated tier (later) | [RHAISTRAT-1792](/features/agent-catalog/knowledge/ref-rhaistrat-1792-agent-eval-starter-kit.md) (Feature) | Refinement |
| Declarative binding | RHAIRFE-2309 / RHAIRFE-2310 | shared with [agent-interop](/features/agent-interop/index.md) |
| Backend delivery stream | RHOAIENG AI Hub component (~30 items in the [snapshot](/features/agent-catalog/work/jira-snapshot.yaml)) | flowing — spec/artifacts/labels work largely Resolved |

Every strategic ref reconciles to a strategy element above; no orphaned
strategy element carries zero Jira coverage except the candidates below.

### Candidate jiras

1. **Sandbox contract reconciliation** — the deployments view discovers a
   CR whose upstream kind is `Sandbox` (agents.x-k8s.io), while product
   discussion says "AgentSandbox" + `openshell.ai/managed-by`; confirm
   and document the discovery contract → RHOAIENG (under RHAISTRAT-1697).
2. **Typed contract for filterable catalog fields** — protocol / tested
   models / image version ride untyped customProperties; either type them
   upstream (kubeflow/hub) or specify the downstream filter contract →
   RHAIRFE.
3. **Deploy-time owner metadata** — capture business/technical owner at
   deploy to seed the registry's accountability record (EU AI Act / NIST
   RMF / CSA profile; the registry's WEBHOOK-registration path needs a
   producer) → RHAIRFE.
4. **Supported-images program definition** — committed harness list,
   refresh cadence, CVE ownership, BYOL/Containerfile posture for
   proprietary harnesses → RHAISTRAT (or expand RHAISTRAT-1349 scope).
5. **Disconnected catalog UX for 3.5** — link-out cards in enclaves (dim
   unreachable GitHub links, document behavior) → RHOAIENG.

## Watchlist

| trigger | where | if it fires |
|---|---|---|
| OpenShell Go SDK PR series merges (A-of-6 open 2026-07-16) | NVIDIA/OpenShell | 3.6 EA1 deploy de-risks; if still open at EA1 planning, force the manual-config descope decision |
| AIPCC base-images ADR resolves (MR 224) | internal GitLab | gap 4 closes; reconcile its "validated" wording with the supported ruling |
| MLflow RFC-0008 skills Phase 1 review lands | mlflow/rfcs #26 | registry timeline firms; Phase 2 opens agent-shaped entities |
| Forrester Agentic Development Platforms Wave (Q4 2026) | analyst | inclusion window — positioning artifacts must exist before cutoff |
| Air-gapped GDC extends from Gemini models to the agent platform | competitive | wedge narrows to open+governed; sharpen messaging |
| BFF show-and-tell (~2026-07-17) and the 3.5 EA freezes | internal | first live checkpoint on the 3.5 shape |

## History

- 2026-07-16 — **Refresh** (hub.strategy, same day) — registry hand-off
  re-timed per owner: work starts 3.6 EA2 at the earliest, multi-release
  to DP (~3.7 EA1 directional); was "backend 3.6 EA2". Deployment noted
  as its own workstream consumed by catalog and registry. (source:
  /memory/profiles/roadmap.md History, owner 2026-07-16)
- 2026-07-16 — **Creation** (hub.strategy pilot run) — synthesized from
  the same-day intake (4 transcripts, 2 GDocs, 2 Slack channels), the
  adversarially-verified 5-lens research series, and the 37-issue Jira
  sweep. Register: PM working doc per the owner's 2026-07-16 ruling.
