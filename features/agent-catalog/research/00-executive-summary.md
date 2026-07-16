---
title: "Agent Catalog research — executive summary"
description: Living synthesis of the 5-lens deep sweep (2026-07-16) — the market pattern validates our sequencing, the wedge is disconnected+supported+governed, and the 3.6 deploy path rests on one unmerged SDK.
timestamp: 2026-07-16
review_after: 2026-10-16
---

# Agent Catalog research — executive summary

First research run for the partition: **deep, 5 lenses, 2026-07-16**, all lenses completed, plus an adversarial verification pass (20 load-bearing claims checked: 18 confirmed, 2 corrected — IBM catalog GA date, Google GA phrasing). No lens gaps to retry.

## The series

| Doc | Lens | One line |
|---|---|---|
| [01-landscape](/features/agent-catalog/research/01-landscape.md) | landscape | Taxonomy (template gallery / marketplace / registry), vendor-by-vendor state of the art, deploy-UX and curation patterns |
| [02-upstream](/features/agent-catalog/research/02-upstream.md) | upstream | kubeflow/hub agent plugin, starter kits repo, OpenShell + agent-sandbox, A2A 1.0, MLflow RFC stream, harness upstreams |
| [03-architecture](/features/agent-catalog/research/03-architecture.md) | architecture | RHOAI platform baseline (rhoai-3.5-ea.2 snapshot), per-feature integration map, 3.6 deploy reference path, risks |
| [04-requirements](/features/agent-catalog/research/04-requirements.md) | requirements | Disconnected, supportability, licensing, personas, governance/regulation, day-zero enablement — evidence-graded |
| [05-competitive](/features/agent-catalog/research/05-competitive.md) | competitive | Hyperscaler/IBM/NVIDIA/Databricks moves, analyst view, honest wedge-vs-behind positioning |

## What the sweep establishes

**1. Our sequencing is the industry pattern — we're just late to it.** Every major vendor now runs the same three-layer split the hub already models: template gallery (copy code) → deployable store (install/deploy with a trust gate) → registry of versioned running instances. Microsoft's Foundry "agent catalog" is *exactly* RHOAI 3.5's shape (curated code samples, GitHub link-out, no deploy button), and Databricks ships the same catalog→MLflow-registry architecture we plan. The 2026-07-09 no-deploy decision has direct precedent. But the lag is real: Agent Garden shipped at Next '25, AWS launched with 900+ listings July 2025, IBM's 150-agent catalog has been GA since May 2025. The urgency framing in the 06-01 packaging meeting ("everyone has a registry now") is directionally correct (01, 05).

**2. The wedge is narrow, real, and time-boxed: open + portable + supported + governed + disconnected.** Nobody ships vendor-supported, self-run harness images — the market sells managed runtimes instead. NVIDIA's free-blueprints/paid-AI-Enterprise-support tier proves the model sells; IBM (on OpenShift, air-gap documented) is the only other on-prem catalog and it monetizes the layer above ours. Registries are now directly monetized (Agent 365 $15/user/mo), making an infra-priced registry a TCO argument. Erosion warning: Gemini is already GA on air-gapped GDC (Secret/TS) — "hyperscalers can't do disconnected" is no longer safely true (05).

**3. Requirements resolve the staleness-vs-disconnected debate in favor of disconnected.** Air-gapped/regulated segments prohibit runtime fetching outright — stale-but-mirrored beats fresh-but-fetching; the fix is self-contained images + a published refresh cadence, and the Container Health Index makes that cadence externally graded. OpenCode needs patch-level work (upstream issues open) to disable self-update; four of five open harness candidates self-update in some form. Licensing is now fact, not risk: Claude Code redistribution is license-prohibited; Codex CLI is Apache-2.0 (correcting the meeting-note assumption that it's proprietary); BYOL/Containerfile is the industry pattern for the proprietary ones (04, 02).

**4. The 3.6 deploy path has one load-bearing unmerged dependency.** BFF → OpenShell Go SDK: PR #2271 (first of a six-PR series, sandbox client only) was still open on 2026-07-16, against an alpha (v0.0.x) runtime whose Kubernetes/OpenShift support is explicitly experimental (privileged SCC, TLS disabled, evaluation-only). Binding (RHAIRFE-2309/2310) is the only step with no MCP Catalog precedent — a deploy-without-binding descope is the likely fallback. Also confirmed: the upstream CRD kind is `Sandbox` (agents.x-k8s.io), not `AgentSandbox` — the product-discussion name should be reconciled against live cluster objects (02, 03).

**5. Product schema and upstream schema have quietly diverged.** kubeflow/hub PR #2907 demoted `protocol`, `models`, and `imageVersion` to free-form `customProperties` — the exact fields the 2026-07-02 field-finalization decision made load-bearing ("communication protocol" multi-value, optional "tested models", image version priority). Not a contradiction (they ride customProperties), but filtering on them has no typed upstream contract — worth an explicit check with the dashboard/backend teams (02).

**6. Governance evidence supports "Deploy always registers, reconcile the rest."** EU AI Act transparency applies 2 Aug 2026 (one cycle from 3.6); NIST AI RMF GV-1.6 and CSA's agentic profile expect per-agent accountability records; no surveyed vendor exposes "Register" as a catalog verb — registration is a deploy side-effect plus discovery/reconciliation for out-of-band deployments (matching the ODH ADR #142 direction and Andrew Ballantyne's GitOps objection). The deploy flow is uniquely positioned to capture owner metadata at deploy time (04, 01).

**7. What separates starter kits from "glorified quick starts" is the golden-path checklist.** One-command run against platform defaults, support matrix + sizing, pre-wired binding (or documented copy-paste config if binding slips), and an eval hook. Jehlum's platform-skills bootstrap is the highest-leverage enablement item; catalog trust is empirically fragile (Port 2025: 3% full trust in portal metadata) — card accuracy is a requirement, not polish (04).

## Recommended follow-ups (not auto-run)

- **jira-gap lens** — the one lens not in this run's scope; the domain jira block exists, and crossing RHAISTRAT actives against these findings would surface blind spots (e.g., no downstream item for Sandbox-naming reconciliation or the upstream customProperties divergence). Retry: `hub.research agent-catalog jira-gap`.
- **hub.jira-sweep agent-catalog** — set up the stored Jira scope for the partition (RHAISTRAT-1740/1697/1742/1758/1349/1792 + RHAIRFE-2443).
- Track for the next refresh: OpenShell Go SDK PR series merge state; AIPCC ADR (MR 224) resolution; Forrester ADP Wave (Q4 2026) inclusion; Google extending air-gapped GDC to the agent platform; MLflow RFC-0008 review outcome.

## Verification

Two adversarial verification agents (2026-07-16) checked 20 load-bearing claims against primary sources: 18 confirmed, 2 corrected in the docs (IBM Think 2025 GA date; Google "launched" vs "GA"), plus precision notes applied (PR #2907 also demoted imageVersion; agent.yaml path convention; OpenShell OpenShift install caveats; EU AI Act Article 50(2) marking-deadline nuance).
