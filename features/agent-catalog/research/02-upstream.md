---
title: "Agent catalog upstream — kubeflow/hub, OpenShell, A2A, starter kits, MLflow"
description: What actually exists upstream under the RHOAI Agent Catalog — repo-by-repo maturity, activity, and governance for the catalog backend, starter kits, runtime, protocols, and registry RFCs.
timestamp: 2026-07-16
lens: upstream
review_after: 2026-10-16
---

The RHOAI Agent Catalog sits on a stack that is real and active at every layer, but with very uneven maturity: a weeks-old catalog plugin in [kubeflow/hub](https://github.com/kubeflow/hub), a fast-moving starter-kit repo, an alpha NVIDIA runtime whose Go SDK is literally mid-review this week, a 1.0 Linux Foundation protocol (A2A), and an MLflow registry RFC that is still a draft. Detail per target below.

## 1. kubeflow/hub — the catalog backend

[kubeflow/hub](https://github.com/kubeflow/hub) is the Kubeflow umbrella repo for the Model Registry and its catalog services — "a single pane of glass" for model/artifact metadata, plus a federated Model Catalog Service, a Kubernetes controller + CSI driver, and a React UI with a Go BFF. Apache-2.0, ~177 stars / 188 forks, Go 57% / TypeScript 29% / Python 10%, self-declared **alpha** status, 37 releases with v0.3.12 current (July 2026). It is explicitly maintained by Red Hat with the Kubeflow community, with a published commitment of 12+ months' notice before ending maintenance — so the governance risk for the catalog backend is low, but the API maturity is not (the agent catalog API is `v1alpha1`).

The agent catalog is a June–July 2026 work burst, now largely merged with no open agent PRs at time of writing — scaffolding ([#2887](https://github.com/kubeflow/hub/pull/2887)), the UI gallery and filters ([#2934](https://github.com/kubeflow/hub/pull/2934)), and middleware path plumbing ([#2969](https://github.com/kubeflow/hub/pull/2969)), driven by Al-Pragliola, Philip-Carneiro, ppadti, and dbasunag. The two schema-defining PRs:

- [PR #2907](https://github.com/kubeflow/hub/pull/2907) (merged 2026-07-03) rationalized the agent OpenAPI schema: typed, server-side-filterable fields are `name, source_id, displayName, description, readme, framework, labels, logo, repositoryUrl, env, artifacts`; `agentType` was deleted (it was always `starter_kit`); **`models`, `protocol`, and `imageVersion` moved into a free-form `customProperties` map**, and `publishedDate` was dropped (redundant with epoch timestamps). So the three fields the product surfaces as "communication protocol", "tested models", and "image version" are *not* first-class in the upstream schema — they ride in customProperties (filterability of the typed list comes via named-query plumbing added in the same PR).
- [PR #2928](https://github.com/kubeflow/hub/pull/2928) (merged 2026-07-07) added `GET /api/agent_catalog/v1alpha1/agents/{id}/artifacts` with a `template-artifact` type that stores the kit's agent.yaml deployment spec as a JSON-encoded string in the DB — this is the endpoint the 3.6 deploy flow reads templates from. Review (lugi0) flagged missing unit tests, broken pagination, and raw-SQL divergence from model-catalog patterns; all were fixed pre-merge, but it signals the plugin's youth.

**Not verified:** any formal agent-catalog roadmap document upstream — the direction is only legible from the PR stream.

## 2. red-hat-data-services/agentic-starter-kits — the 3.5 content

[agentic-starter-kits](https://github.com/red-hat-data-services/agentic-starter-kits) is Red Hat's "production-ready starter kits for building and deploying AI agents on Red Hat OpenShift" — Apache-2.0, small footprint (23 stars / 22 forks) but genuinely active (643 commits, Python 69.5%). The [`agents/` tree](https://github.com/red-hat-data-services/agentic-starter-kits/tree/main/agents) holds **12 framework directories**: `a2a, autogen, claude-code, codex, crewai, google` (ADK), `langflow, langgraph, llamaindex, openclaw, opencode, vanilla_python`. LangGraph is the deepest (ReAct, Agentic RAG, ReAct + DB memory, human-in-the-loop); the `a2a/` kit is a LangGraph + CrewAI multi-agent system; and the four harness kits (Claude Code and OpenClaw "on OpenShift", Codex CLI and OpenCode "on OpenShell") show the harness-as-catalog-entry direction already landing in this repo. Supporting structure: shared `components/` (auth), an `evals/` harness with an EvalHub adapter, cross-agent HTTP behavioral tests, `infrastructure/llm-d/` for inference routing, and `sandboxes/base/` — an **OpenShell base container image**, confirming OpenShell as the intended runtime substrate.

A kit ([CrewAI websearch template](https://github.com/red-hat-data-services/agentic-starter-kits/tree/main/agents/crewai/templates/websearch_agent)) ships `agent.yaml`, Dockerfile, pyproject.toml, Makefile, Helm `values.yaml`, src/, tests/, evalhub/, and a playground, with MLflow tracing wired in. (Layout note: `agent.yaml` sits at `agents/<framework>/templates/<template_name>/agent.yaml`, not at the kit root — kit roots hold `deployment/`, `examples/`, `templates/`, `README.md`; some templates also carry an `AgentRuntime.yaml`.) The [agent.yaml](https://raw.githubusercontent.com/red-hat-data-services/agentic-starter-kits/main/agents/crewai/templates/websearch_agent/agent.yaml) top-level keys readable this pass: `name`, `displayName`, `framework`, `description`, `labels`, `logo` (base64 SVG inline), and `env` (required: `API_KEY, BASE_URL, MODEL_ID`; optional: `PORT, CONTAINER_IMAGE`). **Not verified:** `protocol` and tested-`models` fields in this particular file — consistent with PR #2907 treating both as optional customProperties rather than schema-required. The claim that only the CrewAI and LangGraph kits implement A2A is consistent with the repo layout (the `a2a/` kit is exactly those two frameworks) but this pass did not enumerate every kit's server code to prove the negative.

## 3. OpenShell + Kubernetes agent-sandbox — the 3.6 runtime

[NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell) is "the safe, private runtime for autonomous AI agents": a Gateway (control-plane API), policy-enforced Sandboxes, a Policy Engine (filesystem/network/process constraints), and a Privacy Router for model API calls. Apache-2.0, ~7.7k stars, Rust ~90%, **74 releases with v0.0.85 in July 2026** — very fast cadence, but self-described **alpha** ("single-player mode"). Kubernetes support is explicitly experimental ("expect rough edges and breaking changes"), via a [Helm chart on GHCR](https://github.com/NVIDIA/OpenShell/blob/main/deploy/helm/openshell/README.md), and [OpenShift installation is documented by NVIDIA](https://docs.nvidia.com/openshell/kubernetes/openshift) — itself flagged evaluation-only (privileged SCC, TLS disabled).

The Kubernetes story layers on [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox), a SIG Apps project (3.2k stars, 14 releases, latest v0.5.1) whose **Sandbox CRD** gives isolated, stateful singleton workloads stable identity, persistent storage, and lifecycle management, with gVisor/Kata isolation options. Per [NVIDIA's Kubernetes setup docs](https://docs.nvidia.com/openshell/kubernetes/setup), OpenShell's K8s compute driver requires the agent-sandbox controller and installs the `sandboxes.agents.x-k8s.io` CRD in `agent-sandbox-system`. **Not verified:** an "AgentSandbox" CR kind or the `openshell.ai/managed-by` label upstream — the SIG kind is `Sandbox` in the `agents.x-k8s.io` group, so the AgentSandbox naming in product context may be a downstream/product-layer convention worth confirming against the actual cluster objects.

The **Go SDK** is real but not merged. [Issue #2044](https://github.com/NVIDIA/OpenShell/issues/2044) (rhuss, opened 2026-06-29) proposed a client-go-conventions SDK — typed sub-clients, watch primitives, fake client — arguing "the Kubernetes world runs on Go." It closed into [PR #2271](https://github.com/NVIDIA/OpenShell/pull/2271), "add Go SDK foundation, types, and sandbox client (A)": the **first of a six-PR series**, landing in `sdk/go/`, still **open in review as of 2026-07-16** (a 14-finding principal-engineer review by russellb, mostly addressed; Config wiring and advanced watch deferred to later PRs). A fully functional personal-repo SDK exists: [rhuss/openshell-sdk-go](https://github.com/rhuss/openshell-sdk-go) — v0.2.2 (2026-06-30), Apache-2.0 with NVIDIA copyright headers, full sub-client surface (Sandbox, Exec, Provider, Service, File, Health, Policy) plus OIDC auth and a fake client. Anything RHOAI 3.6 builds on this SDK is building on a pre-merge, pre-1.0 dependency; the sandbox client is the only fully implemented resource in PR A.

## 4. A2A and the agent-description standards field

[a2aproject/A2A](https://github.com/a2aproject/A2A) is the strongest-governed piece of the stack: a **Linux Foundation** project (Google-contributed), Apache-2.0, 24.8k stars, latest release **v1.0.1 (2026-05-28)**. The [specification](https://a2a-protocol.org/latest/specification/) (1.0) defines three transport bindings (JSON-RPC 2.0, gRPC, HTTP+REST), an `A2A-Version` header, an async-first task lifecycle (submitted → working → terminal states, plus input-required/auth-required interrupts), and the **AgentCard**: provider info, an `AgentSkill` array of declared capabilities, capability flags (streaming, push notifications), interface/endpoint declarations, security schemes (API key, HTTP auth, OAuth2, OIDC, mTLS), and an optional cryptographic signature — discovered at `/.well-known/agent-card.json`. This is the runtime capability surface the catalog's static agent.yaml does *not* capture; the two describe the same agent at different lifecycle stages.

Adjacent standards, briefly:
- **OASF** ([agntcy/oasf](https://github.com/agntcy/oasf), 323 stars, 35 releases, Apache-2.0): AGNTCY's schema system for agent capabilities/metadata built on a "record" object annotated with skills and domains, OCSF-inspired, schema server hosted by Outshift by Cisco; its directory tooling can import from MCP/A2A formats. (AGNTCY's Linux Foundation affiliation is widely reported but wasn't stated on the repo page fetched this pass.)
- **AGENTS.md** ([agents.md](https://agents.md/)): a "README for agents" convention — freeform markdown instructions for coding agents, no required fields, 60k+ projects, created by OpenAI/Amp/Google Jules/Cursor/Factory and now stewarded by the **Agentic AI Foundation under the Linux Foundation**. It is repo-level instruction context, not a manifest — a different layer from agent.yaml or agent cards.
- **OpenSharing** ([Linux Foundation announcement, 2026-06-10](https://www.linuxfoundation.org/press/linux-foundation-announces-opensharing-project-to-standardize-ai-asset-and-data-exchange)): Databricks-contributed evolution of Delta Sharing into a vendor-neutral protocol for exchanging **agent skills, AI models, and unstructured data** across platforms. Brand new, but directly relevant as a future cross-org distribution channel for exactly the assets the Agent Catalog and MLflow registry hold.

There is no single winning agent-manifest standard: agent.yaml (catalog/deploy-time), A2A agent card (runtime), OASF records (registry/directory), and OpenSharing (exchange) each own a slice.

## 5. MLflow — the skills/agent registry RFC stream

[mlflow/rfcs](https://github.com/mlflow/rfcs) is MLflow's design-decision repo (enhancement issue → `ready` triage → RFC PR → accept/reject/defer). The live item is [PR #26, RFC-0008 "MVP Skill Registry (Phase 1)"](https://github.com/mlflow/rfcs/pull/26) — **draft, opened 2026-07-14** by jwm4 (Bill Murdock; affiliation isn't displayed on the PR). It proposes a metadata-first registry of **skills and skill bundles** with versioning, lifecycle stages, and aliases; harness-agnostic content retrieval from Git/OCI/ZIP/MLflow artifacts; installation delegated to package-manager plugins; and `mlflow.skill_context()` tracing integration. Two things matter for agent cataloging: (1) the scope was **deliberately narrowed from a broader proposal (PR #10) per discussion with Databricks maintainers** — subagents, hooks, and MCP server references are explicitly deferred to a Phase 2 RFC that will "extend bundles" toward agent-shaped entities; (2) it aligns with the already-established RFC-0004 MCP Registry pattern, so MLflow is accreting registries (MCP → skills → bundles/agents) one entity type at a time. Net: an MLflow-backed *agent* registry is at least two RFC cycles away; skills-only Phase 1 is unmerged draft. **Not verified:** the exact date of the phase-split decision (the Slack discussion predates the PR; the PR itself is dated 2026-07-14).

## 6. Harness candidate upstreams (brief)

| Harness | License | Scale | Latest release | Cadence / update | Container/deploy |
|---|---|---|---|---|---|
| [sst/opencode](https://github.com/sst/opencode) | MIT | 186k stars | v1.18.3, 2026-07-16 | 841 releases — near-daily; script install w/ `$OPENCODE_INSTALL_DIR` | CLI + desktop beta; no first-class container story in README (the starter kit supplies one) |
| [block/goose](https://github.com/block/goose) | Apache-2.0 | 51.3k stars | v1.43.0, 2026-07-14 | 143 releases; stable channel installer | Desktop/CLI/API; Docker referenced; MCP extensions (70+); governed under **AAIF/Linux Foundation** |
| [openclaw/openclaw](https://github.com/openclaw/openclaw) | MIT | 383k stars | date-tagged stable/beta/dev channels | **self-updates** via `openclaw update --channel` | docker-compose shipped; sandboxes non-main sessions via Docker/SSH/**OpenShell** backends; "treat inbound DMs as untrusted input" |
| [NousResearch/hermes-agent](https://github.com/nousresearch/hermes-agent) | MIT | 216k stars | v0.18.2, 2026-07-08 | 21 releases; **self-creates and self-improves skills** at runtime | local, Docker, SSH, Singularity, Modal, Daytona backends; Nous Research governed |
| [badlogic/pi-mono](https://github.com/badlogic/pi-mono) (pi) | MIT | 71.8k stars | v0.80.8, 2026-07-16 | 245 releases; `pi update --self` hardened with `--ignore-scripts` | interactive/JSON/RPC/SDK modes; Docker, micro-VM (Gondolin), and **OpenShell** isolation |

Self-update behavior (OpenClaw channels, Hermes skill self-creation, pi self-update) is the catalog-governance friction point: an image-pinned catalog entry and a self-mutating harness pull in opposite directions. Proprietary notes: **Claude Code** is proprietary Anthropic software (distributed, not open source). **Codex CLI** is *not* proprietary — [openai/codex](https://github.com/openai/codex) is Apache-2.0 (98.8k stars, v0.144.5, 2026-07-16, Rust); the models behind it are the proprietary part. **Antigravity** (Google) was not verified this pass; treat as proprietary until checked. **Not verified:** OpenClaw's prior names — the README only references "Molty" as inspiration.

## 7. Kagenti — the old path

The [Kagenti org](https://github.com/kagenti) remains **active, not abandoned**: [kagenti/kagenti](https://github.com/kagenti/kagenti) (282 stars, v0.6.1 on 2026-06-25, 4,854 commits, no deprecation notice) positions itself as a "framework-neutral, scalable, and secure platform for deploying and orchestrating AI agents" on A2A + MCP, with a UI, installer (Kind/OpenShift), identity/auth bridge, and an MCP gateway now hosted under the Kuadrant org. Governance is IBM-led (kagenti-maintainers googlegroup); several org repos (adk, agentic-control-plane, plugins-adapter) are archived. [opendatahub-io/agents-operator](https://github.com/opendatahub-io/agents-operator) — the former RHOAI deployment path — is a fork of kagenti/kagenti-operator and still shows active development (1,309 commits, 2 stars), with **AgentRuntime and AgentCard CRs**, SPIFFE workload identity, OAuth2/Keycloak, signature-verified agent-to-agent trust, and MLflow tracing. What stays relevant even after the OpenShell pivot: the AgentCard-as-CR pattern, the SPIFFE/Keycloak identity model, and the Kuadrant MCP gateway — none of which the OpenShell path currently replaces.

## Candidate knowledge atoms

- The upstream agent catalog schema ([kubeflow/hub PR #2907](https://github.com/kubeflow/hub/pull/2907), merged 2026-07-03) demoted `protocol` and `models` to free-form `customProperties`; only name/displayName/description/framework/labels/logo/env/artifacts are typed and filterable — product filtering on protocol/tested-models has no typed upstream contract.
- agent.yaml is served to deploy flows via `GET /agents/{id}/artifacts` as a `template-artifact` JSON string ([kubeflow/hub PR #2928](https://github.com/kubeflow/hub/pull/2928), merged 2026-07-07), on a `v1alpha1` API in an alpha-status repo.
- The OpenShell Go SDK is pre-merge: [PR #2271](https://github.com/NVIDIA/OpenShell/pull/2271) (first of six, sandbox client only) was still in review 2026-07-16; the only complete implementation is the rhuss prototype at v0.2.2 — 3.6 is building on an unreleased dependency of an alpha (v0.0.x) runtime.
- Upstream, the sandbox CRD is `Sandbox` in `agents.x-k8s.io` ([kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox), v0.5.1); the "AgentSandbox" kind and `openshell.ai/managed-by` label used in product context were not found upstream and should be confirmed against live cluster objects.
- MLflow's registry stream is skills-only and draft ([RFC-0008, PR #26](https://github.com/mlflow/rfcs/pull/26), 2026-07-14); agent-shaped entities (subagents, hooks, MCP refs in bundles) are explicitly deferred to a Phase 2 RFC — an MLflow agent registry is not imminent.
- Four of five open harness candidates ship self-update mechanisms (OpenClaw channels, Hermes runtime skill self-creation, pi `update --self`, opencode installer), which conflicts with image-pinned catalog governance; Codex CLI is Apache-2.0 (not proprietary as commonly assumed), while Claude Code is.

## Verification

Adversarial fact-check pass, 2026-07-16 (10 load-bearing claims): all 10 confirmed against primary sources. Notable confirmations: upstream sandbox CRD kind is `Sandbox` in `agents.x-k8s.io` with zero matches for `AgentSandbox` in either NVIDIA/OpenShell or kubernetes-sigs/agent-sandbox (OpenShell's k8s driver hardcodes `SANDBOX_KIND = "Sandbox"`); OpenShell Go SDK PR #2271 explicitly "first PR in a 6-PR decomposition", still open 2026-07-16. Precision fixes applied in place (imageVersion also demoted in PR #2907; agent.yaml path; SDK phrasing; OpenShift-install experimental caveats).

## Sources

1. [kubeflow/hub](https://github.com/kubeflow/hub)
2. [kubeflow/hub PR #2907 — agent schema rationalization](https://github.com/kubeflow/hub/pull/2907)
3. [kubeflow/hub PR #2928 — artifacts endpoint](https://github.com/kubeflow/hub/pull/2928)
4. [kubeflow/hub agent PRs listing](https://github.com/kubeflow/hub/pulls?q=is%3Apr+agent)
5. [red-hat-data-services/agentic-starter-kits](https://github.com/red-hat-data-services/agentic-starter-kits) (+ [agents/ tree](https://github.com/red-hat-data-services/agentic-starter-kits/tree/main/agents), [CrewAI websearch kit](https://github.com/red-hat-data-services/agentic-starter-kits/tree/main/agents/crewai/templates/websearch_agent), [agent.yaml](https://raw.githubusercontent.com/red-hat-data-services/agentic-starter-kits/main/agents/crewai/templates/websearch_agent/agent.yaml))
6. [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell) (+ [Helm chart README](https://github.com/NVIDIA/OpenShell/blob/main/deploy/helm/openshell/README.md))
7. [NVIDIA OpenShell Kubernetes setup docs](https://docs.nvidia.com/openshell/kubernetes/setup) and [OpenShift docs](https://docs.nvidia.com/openshell/kubernetes/openshift)
8. [OpenShell issue #2044 — Go SDK proposal](https://github.com/NVIDIA/OpenShell/issues/2044)
9. [OpenShell PR #2271 — Go SDK foundation](https://github.com/NVIDIA/OpenShell/pull/2271)
10. [rhuss/openshell-sdk-go](https://github.com/rhuss/openshell-sdk-go)
11. [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox)
12. [a2aproject/A2A](https://github.com/a2aproject/A2A)
13. [A2A protocol specification](https://a2a-protocol.org/latest/specification/)
14. [agntcy/oasf](https://github.com/agntcy/oasf)
15. [agents.md](https://agents.md/)
16. [Linux Foundation OpenSharing announcement](https://www.linuxfoundation.org/press/linux-foundation-announces-opensharing-project-to-standardize-ai-asset-and-data-exchange) and [Databricks press release](https://www.databricks.com/company/newsroom/press-releases/databricks-announces-opensharing)
17. [mlflow/rfcs](https://github.com/mlflow/rfcs) and [RFC-0008 PR #26](https://github.com/mlflow/rfcs/pull/26)
18. [sst/opencode](https://github.com/sst/opencode)
19. [block/goose](https://github.com/block/goose)
20. [openclaw/openclaw](https://github.com/openclaw/openclaw)
21. [NousResearch/hermes-agent](https://github.com/nousresearch/hermes-agent)
22. [badlogic/pi-mono](https://github.com/badlogic/pi-mono)
23. [openai/codex](https://github.com/openai/codex)
24. [Kagenti org](https://github.com/kagenti) and [kagenti/kagenti](https://github.com/kagenti/kagenti)
25. [opendatahub-io/agents-operator](https://github.com/opendatahub-io/agents-operator)
