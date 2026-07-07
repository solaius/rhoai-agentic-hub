---
title: RHOAI 3.4 E2E Usability Findings — RFE Alignment & Gap Analysis
description: Task-based usability study findings (5 MLOps/AI Platform Engineers, June 2026) across model deployment, Playground, RAG, and MCP tool calling, mapped to RFE alignment and gaps.
source: ai-asset-registry/gen-ai-studio/usability-findings/rhoai-3.4-usability-report.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# RHOAI 3.4 E2E Usability Findings — RFE Alignment & Gap Analysis

> **Source study**: [E2E Usability Findings — Deployment → AI Playground](https://docs.google.com/presentation/d/1GRVPO34oUhFXvlikCBJ-czBMCStX0fJPz6B03xFBPZ4/)
> **Researcher**: Yingzhao Zhou (UX Research)
> **Study date**: June 2026 (on RHOAI 3.4 GA cluster)
> **Participants**: 5 MLOps / AI Platform Engineers from enterprise organizations
> **Method**: Task-based usability evaluation with think-aloud protocol
> **Scope**: Model deployment → Playground access → RAG configuration → MCP tool calling → cross-component navigation
> **Report author**: Peter Double (Principal PM)
> **Report date**: 2026-06-24

---

## Executive Summary

The usability study uncovered **20 evaluative findings** (usability issues) and **5 generative user needs** (strategic insights). Mapping these against existing Jira tickets reveals:

- **8 findings** have existing RFE/STRAT coverage (full or partial)
- **12 evaluative findings** and **3 user needs** have **no existing RFE** — representing gaps in our backlog
- The 3 critical findings all affect the **first-time user journey** — the path from deploying a model to getting value in the playground

This report categorizes every finding, aligns it to existing Jira coverage where it exists, and proposes new RFEs where gaps remain. New RFEs are prioritized at the end.

---

## Part 1: Evaluative Findings (Usability Issues)

### CRITICAL Findings

---

#### C1. Broken deployment-to-playground wayfinding

**Severity**: Critical
**Participants affected**: P1, P2, P4
**Area**: Cross-component (Deployment → Gen AI Studio)

**What was observed**: After successfully deploying a model, users expected a natural path to the playground. Instead, they had to independently discover the playground with no guidance. Multiple participants spent several minutes searching, creating a high barrier to entry.

**Recommendations from study**:
1. Guided next-step prompt after deployment completion to accelerate the first "aha" moment
2. Expand Gen AI Studio navigation by default so the playground entry point is visible without clicking
3. Add a direct "Open in Playground" action on the deployment success screen and in the model's action menu

**Existing Jira coverage**: **NONE**

**RFE needed**: Yes — **NEW RFE: Deployment-to-Playground Guided Navigation**
> After model deployment completes successfully, users need a contextual next-step that guides them to the Gen AI Studio playground with the deployed model pre-selected. This should include: (1) a "Try in Playground" CTA on the deployment success view, (2) an "Open in Playground" action in the model's dropdown menu on the serving list, and (3) expanding the Gen AI Studio nav section by default so the playground entry point is visible without extra clicks.
>
> **Components**: `AI Core Dashboard`, `Gen AI Studio`, `UXD`
> **Labels**: `ai-studio`, `playground`, `model-serving`, `dashboard-crimson-scrum`, `3.6-candidate`, `must-do`, `uxd-agentic`

---

#### C2. Opaque deployment progress and errors

**Severity**: Critical
**Participants affected**: P1, P2, P3, P4, P5 (all 5)
**Area**: Deployment / Model Serving

**What was observed**: Users cannot diagnose deployment issues within the RHOAI dashboard. No stage feedback (e.g., "downloading image", "starting container", "running health checks"). Error details (OOM, timeout, probe failures) only appear in OpenShift console logs. All 5 participants were forced to context-switch to CLI or the OpenShift console for basic troubleshooting.

**Recommendations from study**:
1. Surface deployment stages as a progress stepper within the deployment detail view
2. Surface pod events and logs info in the deployment UI
3. Auto-refresh deployment status, or provide a visible refresh control

**Existing Jira coverage**: **PARTIAL**
- [RHOAIENG-15568](https://redhat.atlassian.net/browse/RHOAIENG-15568) — "Implement Improved Serving Statuses - Phase 1" (Story, Backlog). Investigation outcome: focus on conditions reported by deployment resources for InferenceServices. Engineering ticket, not a product RFE.

**RFE needed**: Yes — **NEW RFE: Deployment Progress Visibility and Error Surfacing**
> Currently deployment is a black box after the user clicks "Deploy." Users need: (1) stage-based progress indicators showing what phase the deployment is in (image pull, container start, health checks), (2) pod events and error messages surfaced directly in the RHOAI UI without requiring OpenShift console access, and (3) auto-refreshing deployment status so users don't have to manually poll. RHOAIENG-15568 covers some engineering investigation but there is no product-level RFE tracking the full user experience requirement.
>
> **Components**: `AI Core Dashboard`, `UXD`
> **Labels**: `model-serving`, `ai-studio`, `dashboard-crimson-scrum`, `3.6-candidate`, `must-do`, `uxd-agentic`

---

#### C3. Undiscoverable runtime configuration for tool calling

**Severity**: Critical
**Participants affected**: P1, P2, P4 (5/5 task failure)
**Area**: Cross-component (Deployment → Playground / MCP)

**What was observed**: Users did not know that open-source models require specific vLLM runtime arguments to enable tool calling (MCP) and RAG. The UI provided no guidance, documentation, or contextual hints about these requirements. This caused task failure for **all 5 participants** — the most severe outcome in the study.

**Recommendations from study**:
- Smart defaults with auto-detection of tool calling configuration in the deployment wizard

**Existing Jira coverage**: **YES — FULLY COVERED**
- [RHAISTRAT-1472](https://redhat.atlassian.net/browse/RHAISTRAT-1472) — "AI Hub Model Serving Wizard: Surface Tool Calling Configuration During Deployment (Stage 2)" (Feature, Backlog). Surfaces tool calling config so users can enable it with a single opt-in click.
- [RHAISTRAT-2008](https://redhat.atlassian.net/browse/RHAISTRAT-2008) — "Add 'Enable Tool Calling' Support to RHOAI Serving Wizard" (Feature, Closed). Checkbox to automate CLI argument injection. **Status: Closed** — this shipped or was superseded.
- The presentation notes: "we have WIP to get this into 3.5!! 💪"

**RFE needed**: No — existing coverage is adequate. **Action**: Ensure RHAISTRAT-1472 is prioritized for 3.5 stable. The 5/5 failure rate justifies must-do priority.

---

### HIGH Findings

---

#### H1. Confusing model source identifiers

**Severity**: High
**Participants affected**: P2, P4
**Area**: Deployment / Model Serving

**What was observed**: When deploying a Hugging Face model, users struggled to choose between "URI" and "OCI" options. The terminology is ambiguous and the UI provides no guidance on when to use each. Andrew Ballantyne noted this has also been CAI and Field feedback.

**Recommendations from study**:
1. Provide explicit guidance in the deployment wizard clarifying when to use each option, with a link to docs
2. Rename "URI" to "Hugging Face URI" for clarity
3. Add examples and hints to the URI connection popup showing valid formats (oci://, hf://, pvc://) with copy-pasteable examples

**Existing Jira coverage**: **NONE**

**RFE needed**: Yes — **NEW RFE: Clarify Model Source Identifiers in Deployment Wizard**
> When deploying a model from Hugging Face, the deployment wizard presents "URI" and "OCI" options without explaining when to use each. Users need: (1) descriptive labels (e.g., "Hugging Face URI" instead of "URI"), (2) contextual guidance explaining when each option is appropriate, (3) input field examples showing valid format patterns (oci://, hf://, pvc://) with copy-pasteable samples. Reported by both usability study participants and field/CAI feedback.
>
> **Components**: `AI Core Dashboard`, `AI Hub`, `UXD`
> **Labels**: `ai-hub`, `model-serving`, `dashboard-crimson-scrum`, `3.6-candidate`, `should-do`, `uxd-agentic`

---

#### H2. Default project filter hides content

**Severity**: High
**Participants affected**: P2, P3, P4
**Area**: Project Selector (Dashboard-wide)

**What was observed**: Users expect to see all their projects on first load and then narrow down. But the platform defaults to an "AI Projects" filter that often shows an empty view — leading users to believe their projects don't exist.

**Recommendations from study**:
1. Clearly explain the difference between "AI Projects" and "All Projects"
2. Default to all projects users have access to
3. Distinguish between projects users have access to vs. projects they are responsible for

**Existing Jira coverage**: **NONE**

**RFE needed**: Yes — **NEW RFE: Default Project Selector to Show All Accessible Projects**
> The dashboard defaults to an "AI Projects" filter that frequently shows an empty view, causing users to believe their projects don't exist. Users expect to see all accessible projects on first load and then narrow down. The project selector should: (1) default to showing all projects the user has access to, (2) clearly label the difference between "AI Projects" (RHOAI-managed) and "All Projects" (namespace-level), and (3) consider distinguishing "my projects" (responsible for) from "accessible projects" (can view/use).
>
> **Components**: `AI Core Dashboard`, `UXD`
> **Labels**: `dashboard`, `ai-studio`, `dashboard-crimson-scrum`, `3.6-candidate`, `should-do`, `uxd-agentic`

---

#### H3. AI playground features not self-revealing

**Severity**: High
**Participants affected**: P4
**Area**: Gen AI Studio / Playground

**What was observed**: Essential features like the playground, MCP tools, and model configuration are buried under collapsed menus or non-intuitive buttons. Users must click through multiple layers to find functionality they expect to be immediately visible. The label "Knowledge" was used instead of the more intuitive "RAG."

**Recommendations from study**:
1. Use descriptive labels on buttons (e.g., "RAG" instead of "Knowledge")
2. Audit the navigation hierarchy to ensure high-frequency actions are reachable in 1-2 clicks

**Existing Jira coverage**: **NONE** (as a standalone finding)

**RFE needed**: Yes — **NEW RFE: Gen AI Studio Feature Discoverability Audit**
> Key playground features (MCP tools, RAG configuration, model settings) are hidden behind collapsed menus and non-intuitive button labels. Users expect high-frequency actions to be reachable in 1-2 clicks. This RFE should: (1) audit the navigation hierarchy to surface high-frequency actions, (2) use descriptive labels that match user mental models (e.g., "RAG" instead of "Knowledge"), and (3) ensure MCP tools and RAG panels are visible or clearly indicated when enabled.
>
> **Components**: `AI Core Dashboard`, `Gen AI Studio`, `UXD`
> **Labels**: `ai-studio`, `playground`, `mcp`, `rag`, `dashboard-crimson-scrum`, `3.6-candidate`, `should-do`, `uxd-agentic`

---

#### H4. Opaque tool execution in playground

**Severity**: High
**Participants affected**: P1, P4
**Area**: Gen AI Studio / Playground / MCP

**What was observed**: When a model calls a tool, the playground does not show which tool was invoked, what input was passed, or what output was returned. This makes debugging impossible — a capability that is standard in competing AI playgrounds (ChatGPT, Claude, etc.).

**Recommendations from study**:
1. Display a collapsible tool execution trace inline in the chat stream showing: tool name, input, and returned output
2. Visually differentiate tool-call steps from model-generated text

**Existing Jira coverage**: **PARTIAL**
- [RHAISTRAT-133](https://redhat.atlassian.net/browse/RHAISTRAT-133) — "Chat Metrics & Observability (Tracing) in Playground" (Feature, In Progress). Covers the broader tracing infrastructure including OTel instrumentation and MLflow trace view. However, this is about full distributed tracing, not the simpler inline tool-call visibility that users are asking for.

**RFE needed**: Yes — **NEW RFE: Inline Tool Execution Trace in Playground Chat**
> When a model invokes an MCP tool during a conversation, the playground currently shows no indication of which tool was called, what input was sent, or what output was returned. Users need a collapsible inline tool execution trace in the chat stream showing: (1) tool name, (2) input parameters, and (3) returned output. Tool-call steps should be visually differentiated from model-generated text. This is a simpler, more immediate need than the full distributed tracing in RHAISTRAT-133 — users want to see what happened in the current conversation, not navigate to a separate tracing UI.
>
> **Components**: `AI Core Dashboard`, `Gen AI Studio`, `UXD`
> **Labels**: `ai-studio`, `playground`, `mcp`, `tool-calling`, `observability`, `dashboard-crimson-scrum`, `3.6-candidate`, `must-do`, `uxd-agentic`

---

#### H5. Opaque playground creation status

**Severity**: High
**Participants affected**: P4
**Area**: Gen AI Studio / Playground

**What was observed**: When creating a playground, the system shows a loading modal with no progress feedback. Users don't know if the system is working or stuck, and don't know whether to wait or take action.

**Recommendations from study**:
1. Show a progress indicator or status message during playground creation (e.g., "Setting up Llama Stack server...")
2. If creation takes longer than expected, provide an estimated time or link to check detailed status

**Existing Jira coverage**: **NONE**

**RFE needed**: Yes — **NEW RFE: Playground Creation Progress Feedback**
> When creating a new playground, the OGX (Llama Stack) server setup displays a loading modal with no status feedback. Users need: (1) stage-based progress messages during creation (e.g., "Configuring Llama Stack server...", "Starting services...", "Ready"), and (2) a fallback message or link to detailed status if creation takes longer than expected. This is especially important because playground creation involves creating an OGX CR and waiting for the operator to reconcile, which can take 30-90 seconds.
>
> **Components**: `AI Core Dashboard`, `Gen AI Studio`, `UXD`
> **Labels**: `ai-studio`, `playground`, `llama-stack-core`, `dashboard-crimson-scrum`, `3.6-candidate`, `should-do`, `uxd-agentic`

---

### MEDIUM Findings

---

#### M1. Deployment status lag between pod events and UI

**Severity**: Medium
**Participants affected**: Not specified
**Area**: Deployment / Model Serving

**What was observed**: The UI does not reflect the actual state of deployment pods in real time. There's a lag between what's happening in the cluster and what the dashboard shows.

**Existing Jira coverage**: **PARTIAL** — [RHOAIENG-15568](https://redhat.atlassian.net/browse/RHOAIENG-15568) covers improved serving statuses.

**RFE needed**: No — covered by the broader deployment progress RFE (proposed under C2) and RHOAIENG-15568.

---

#### M2. Rigid post-deployment editing

**Severity**: Medium
**Participants affected**: Not specified
**Area**: Deployment / Model Serving

**What was observed**: After deploying a model, users cannot easily modify deployment settings. Changes require tearing down and redeploying.

**Existing Jira coverage**: **PARTIAL** — [RHAISTRAT-1921](https://redhat.atlassian.net/browse/RHAISTRAT-1921) covers OGX config changes without restart (3.6 target), but this finding is about model serving deployment settings, not OGX configuration.

**RFE needed**: Yes — **NEW RFE: Editable Model Deployment Settings Post-Deploy**
> After deploying a model, users cannot modify key settings (replicas, resource limits, runtime arguments) without tearing down and redeploying. Users need an edit capability on deployed models that applies changes in-place where possible.
>
> **Components**: `AI Core Dashboard`, `UXD`
> **Labels**: `model-serving`, `ai-studio`, `dashboard-crimson-scrum`, `3.7-candidate`, `should-do`

---

#### M3. Prefer OIDC/short-lived tokens for MCP authentication

**Severity**: Medium
**Participants affected**: Not specified
**Area**: Gen AI Studio / MCP

**What was observed**: Users in enterprise environments prefer configuring MCP authentication using OIDC and short-lived tokens rather than static, long-lived API keys/tokens.

**Existing Jira coverage**: **YES — FULLY COVERED**
- [RHAISTRAT-2085](https://redhat.atlassian.net/browse/RHAISTRAT-2085) — "Gen AI Studio: OAuth authentication for MCP Gateway endpoints" (3.6)
- [RHAIRFE-2479](https://redhat.atlassian.net/browse/RHAIRFE-2479) — OAuth authentication for MCP Gateway endpoints (RFE, Approved)
- [RHAISTRAT-2089](https://redhat.atlassian.net/browse/RHAISTRAT-2089) — Token lifecycle management for MCP Gateway connections (3.6)
- [RHAIRFE-2483](https://redhat.atlassian.net/browse/RHAIRFE-2483) — Token lifecycle management (RFE, Approved)

**RFE needed**: No — existing coverage is comprehensive. This usability finding validates the priority of the 3.6 MCP Gateway OAuth work.

---

#### M4. Missing input validation

**Severity**: Medium
**Participants affected**: Not specified
**Area**: Gen AI Studio / Playground

**What was observed**: Forms in the playground and deployment wizard lack proper input validation, allowing users to submit invalid configurations without feedback.

**Existing Jira coverage**: **NONE**

**RFE needed**: Yes — **NEW RFE: Input Validation for Gen AI Studio Configuration Forms**
> Configuration forms in Gen AI Studio (playground settings, MCP server configuration, custom endpoints) lack input validation. Users can submit invalid values without feedback, leading to cryptic runtime errors. Forms should validate inputs at submission time with clear error messages.
>
> **Components**: `AI Core Dashboard`, `Gen AI Studio`, `UXD`
> **Labels**: `ai-studio`, `playground`, `dashboard-crimson-scrum`, `3.6-candidate`, `should-do`, `uxd-agentic`

---

#### M5. Playground chat state management

**Severity**: Medium
**Participants affected**: Not specified
**Area**: Gen AI Studio / Playground

**What was observed**: Chat state behavior is unexpected — conversations may be lost on navigation, or state persists when users expect a fresh start.

**Existing Jira coverage**: **YES — COVERED**
- [RHAISTRAT-1533](https://redhat.atlassian.net/browse/RHAISTRAT-1533) — "Chat Persistence for Gen AI Studio" (3.5 candidate)
- [RHAISTRAT-1534](https://redhat.atlassian.net/browse/RHAISTRAT-1534) — "Configuration Persistence for Gen AI Studio" (In Progress, 3.5)

**RFE needed**: No — existing work addresses this.

---

#### M6. "Thinking" block clutter

**Severity**: Medium
**Participants affected**: Not specified
**Area**: Gen AI Studio / Playground

**What was observed**: When reasoning models produce chain-of-thought output, the "thinking" blocks create visual clutter in the chat, making it harder to find the actual answer.

**Existing Jira coverage**: **NONE**

**RFE needed**: Yes — **NEW RFE: Collapsible Thinking Blocks in Playground Chat**
> When reasoning models (e.g., Qwen3-Thinking) produce chain-of-thought output, the "thinking" blocks create visual clutter in the chat stream, making it hard to find the actual answer. Thinking blocks should be collapsed by default with a "Show thinking" toggle, and styled distinctly from the model's final response. (Note: multimodal work already implements this pattern for vision models — this RFE should ensure consistency across all reasoning model outputs.)
>
> **Components**: `AI Core Dashboard`, `Gen AI Studio`, `UXD`
> **Labels**: `ai-studio`, `playground`, `dashboard-crimson-scrum`, `3.6-candidate`, `should-do`, `uxd-agentic`

---

#### M7. Playground chat comparison configuration unclear

**Severity**: Medium
**Participants affected**: P5
**Area**: Gen AI Studio / Playground
**Referenced Jira**: RHAISTRAT-1914

**What was observed**: When comparing models side-by-side, the playground does not clearly display which configuration (model, temperature, RAG status) is associated with which chat pane, making it hard to interpret comparison results accurately.

**Existing Jira coverage**: **PARTIAL**
- [RHAISTRAT-2052](https://redhat.atlassian.net/browse/RHAISTRAT-2052) — "Agent Configuration Comparison in Gen AI Studio Chat Compare" (3.6) — covers the future agent comparison feature but not the current model comparison clarity issue.
- [RHAISTRAT-1914](https://redhat.atlassian.net/browse/RHAISTRAT-1914) — Referenced in the study; covers deployment of playground configs as API services.

**RFE needed**: Yes — **NEW RFE: Display Active Configuration per Chat Pane in Compare Mode**
> In side-by-side compare mode, each chat pane should display its active configuration (model name, temperature, RAG on/off, MCP tools enabled) so users can clearly interpret comparison results. Currently, there is no configuration label per pane, making it impossible to know which settings produced which output.
>
> **Components**: `AI Core Dashboard`, `Gen AI Studio`, `UXD`
> **Labels**: `ai-studio`, `playground`, `dashboard-crimson-scrum`, `3.6-candidate`, `should-do`, `uxd-agentic`

---

### LOW Findings

---

#### L1. Ambiguous deployment form labels

**Severity**: Low
**Area**: Deployment / Model Serving

**What was observed**: Deployment form labels use terminology that is ambiguous or unfamiliar to users (e.g., field names that don't clearly convey their purpose).

**Existing Jira coverage**: **NONE**
**RFE needed**: Low priority — can be bundled into a broader UX polish pass for GA. Not a standalone RFE.

---

#### L2. Misleading readiness signals

**Severity**: Low
**Area**: Deployment / Model Serving

**What was observed**: Deployment shows "ready" status before the model is actually ready to serve inference requests.

**Existing Jira coverage**: **PARTIAL** — related to [RHOAIENG-15568](https://redhat.atlassian.net/browse/RHOAIENG-15568) (improved serving statuses).
**RFE needed**: No — covered by the deployment progress work.

---

#### L3. Missing external access path

**Severity**: Low
**Area**: Deployment / Model Serving

**What was observed**: No clear guidance on how to access a deployed model from outside the cluster (external route, API endpoint).

**Existing Jira coverage**: **NONE**
**RFE needed**: Low priority — can be bundled into documentation improvements. Not a standalone RFE.

---

#### L4. Non-standard parameter scale

**Severity**: Low
**Area**: Gen AI Studio / Playground

**What was observed**: Inference parameter controls (e.g., temperature slider) use non-standard scales that don't match user expectations from other tools.

**Existing Jira coverage**: **NONE**
**RFE needed**: Low priority — UX polish item. Not a standalone RFE.

---

#### L5. RAG auto-enable bug

**Severity**: Low
**Area**: Gen AI Studio / Playground / RAG

**What was observed**: RAG enables or disables unexpectedly in certain navigation flows — a bug rather than a design issue.

**Existing Jira coverage**: Should be tracked as a **bug** (RHOAIENG), not an RFE.
**RFE needed**: No — this is a defect. File as RHOAIENG bug if not already tracked.

---

## Part 2: Generative User Needs (Strategic Insights)

---

#### G1. Users want to try a model before investing in infrastructure

**Participants**: P3
**Related Jira**: [RHAISTRAT-1935](https://redhat.atlassian.net/browse/RHAISTRAT-1935), [RHAISTRAT-1744](https://redhat.atlassian.net/browse/RHAISTRAT-1744)

**Insight**: Users expect a "business first" workflow — test whether a model solves their problem before investing in full infrastructure. The current flow forces a complete model deployment before any experimentation, which users see as wasteful if the model turns out not to meet their needs.

**Existing Jira coverage**: **YES — COVERED**
- [RHAISTRAT-1744](https://redhat.atlassian.net/browse/RHAISTRAT-1744) — "Interactive playground for evaluating AI pipelines without full deployment" (Release Pending). Supports chat-focused, read-only playground mode starting with AutoRAG.
- [RHAISTRAT-1935](https://redhat.atlassian.net/browse/RHAISTRAT-1935) — "Gen AI Studio playground must support AI Gateway as alternative to OGX" (3.7). Enables lighter-weight experimentation paths.
- [RHAISTRAT-2049](https://redhat.atlassian.net/browse/RHAISTRAT-2049) — "ExternalModel CR Support in Gen AI Studio Playground" (3.6). Enables using external models without full local deployment.

**RFE needed**: No — existing coverage addresses this need across multiple features.

---

#### G2. RAG pipeline needs go far beyond document upload

**Participants**: P2, P3

**Insight**: Users have moved past simple document upload for RAG. Their primary time is spent optimizing grounding context — custom chunking strategies, external vector store connections, chunk inspection, and connecting to enterprise data sources (SharePoint, S3). The current "scratchpad" RAG in the playground is seen as a starting point, not a solution.

**Existing Jira coverage**: **PARTIAL**
- [RHAISTRAT-1528](https://redhat.atlassian.net/browse/RHAISTRAT-1528) — "Default Vector Store for Gen AI Studio and AutoRAG" (In Progress, 3.5)
- [RHAISTRAT-1746](https://redhat.atlassian.net/browse/RHAISTRAT-1746) — "Existing Vector Store Addition/Registration" (3.7)
- [RHAISTRAT-1747](https://redhat.atlassian.net/browse/RHAISTRAT-1747) — "Multi-Vector Store Selection in Playground" (3.7)
- [RHAISTRAT-1553](https://redhat.atlassian.net/browse/RHAISTRAT-1553) — "View Source Files in Playground Chat Sources and In-line RAG Solution" (3.7)
- [RHAISTRAT-2063](https://redhat.atlassian.net/browse/RHAISTRAT-2063) — "Provide OOTB connections for Common Data Sources in UI" (New)

**Gap**: Chunking/embedding configuration and chunk inspection tooling are NOT covered by any existing RFE.

**RFE needed**: Yes — **NEW RFE: Chunking and Embedding Configuration with Chunk Inspection in Gen AI Studio**
> When users connect a vector store for RAG, they need control over how documents are chunked and embedded. Users should be able to: (1) select chunking strategy (fixed-size, semantic, recursive), (2) configure chunk size and overlap, (3) choose an embedding model, and (4) browse and inspect stored chunks to validate quality against their expectations. This is a key part of the RAG optimization workflow that users spend the most time on, and the current scratchpad upload approach doesn't address it.
>
> **Components**: `AI Core Dashboard`, `Gen AI Studio`, `RAG + Vector DB`, `UXD`
> **Labels**: `ai-studio`, `playground`, `rag`, `ai-asset-endpoints`, `dashboard-crimson-scrum`, `3.7-candidate`, `should-do`, `uxd-agentic`

---

#### G3. Context engineering is shifting from indexing to tool use

**Participants**: P2, P3

**Insight**: In regulated environments, users are shifting from manual RAG (uploading and indexing documents) to MCP-based tool use, giving models the ability to fetch data on demand from authoritative sources rather than maintaining duplicate vector stores. This represents a fundamental mental model shift — from "index everything" to "query on demand."

**Existing Jira coverage**: **PARTIAL** — MCP integration features exist ([RHAISTRAT-1678](https://redhat.atlassian.net/browse/RHAISTRAT-1678), [RHAISTRAT-1576](https://redhat.atlassian.net/browse/RHAISTRAT-1576), [RHAISTRAT-1260](https://redhat.atlassian.net/browse/RHAISTRAT-1260)) but none explicitly positions MCP as a peer context strategy to RAG within the playground UX.

**RFE needed**: Yes — **NEW RFE: Position MCP Tool Use as First-Class Context Strategy Alongside RAG**
> The playground currently treats RAG and MCP as independent features. Enterprise users in regulated environments are shifting from document-indexing RAG to on-demand MCP tool use for authoritative data access. Gen AI Studio should: (1) present MCP and RAG as peer context strategies in the playground configuration, (2) provide guidance on when each approach is appropriate (compliance, data freshness, latency), and (3) enable users to combine both strategies in a single conversation flow with clear provenance indicators.
>
> **Components**: `AI Core Dashboard`, `Gen AI Studio`, `UXD`
> **Labels**: `ai-studio`, `playground`, `mcp`, `rag`, `agentic`, `dashboard-crimson-scrum`, `3.7-candidate`, `should-do`, `uxd-agentic`

---

#### G4. Users have a different mental model of what a "validated model" is

**Participants**: P3, P5

**Insight**: Users expect "validated" to mean security assurance (no malicious code, no data exfiltration), performance benchmarks, and hardware requirements (e.g., exact RAM needed). Red Hat's validation scope may be narrower (runtime compatibility on specific hardware).

**Existing Jira coverage**: **PARTIAL**
- [RHAISTRAT-2106](https://redhat.atlassian.net/browse/RHAISTRAT-2106) — "Validated Guardrail Model Catalog with Benchmark Results" (New) — covers guardrail model validation specifically, not general model validation labeling.
- [RHAISTRAT-2105](https://redhat.atlassian.net/browse/RHAISTRAT-2105) — "Decouple Model Validation Data and Model Catalog Delivery from RHOAI Release Cadence" (New) — addresses release cadence, not validation labeling.

**Gap**: No RFE addresses the "validated" label transparency issue — making the scope of validation explicit to users.

**RFE needed**: Yes — **NEW RFE: Explicit Validation Scope Labeling for Models in AI Hub Catalog**
> Users interpret "Validated" as covering security, performance benchmarks, and hardware requirements. Red Hat's validation scope is narrower (runtime compatibility testing). The catalog should: (1) replace the broad "Validated" badge with specific scope labels (e.g., "Validated for: vLLM runtime on NVIDIA A100"), (2) surface benchmark data where available, and (3) link to detailed validation methodology documentation so users can assess the scope themselves.
>
> **Components**: `AI Hub`, `Model Validation`, `UXD`
> **Labels**: `ai-hub`, `model-serving`, `3.7-candidate`, `should-do`

---

#### G5. Hugging Face as the primary first source for models

**Participants**: P2, P3, P4

**Insight**: Users prefer Hugging Face as their first stop for model discovery (one-click availability, built-in test interfaces, transparent model metadata side by side) before moving to an internal catalog.

**Existing Jira coverage**: **PARTIAL** — HuggingFace is already a supported model source, but the UX for deploying HuggingFace models has friction (see H1 — confusing URI vs OCI).

**RFE needed**: No standalone RFE — the H1 finding (clarify model source identifiers) addresses the primary friction. The broader HuggingFace integration is already functional.

---

## Part 3: Prioritized New RFE Recommendations

Based on severity, participant impact, and strategic importance, here are the recommended new RFEs in priority order:

### Priority 1 — Must-Do (Critical severity or universal participant failure)

| # | Proposed RFE Title | Finding | Severity | Components | Key Labels | Target |
|---|---|---|---|---|---|---|
| 1 | **Deployment-to-Playground Guided Navigation** | C1 | Critical | AI Core Dashboard, Gen AI Studio, UXD | `ai-studio`, `playground`, `model-serving`, `must-do` | 3.6 |
| 2 | **Deployment Progress Visibility and Error Surfacing** | C2 | Critical | AI Core Dashboard, UXD | `model-serving`, `ai-studio`, `must-do` | 3.6 |
| 3 | **Inline Tool Execution Trace in Playground Chat** | H4 | High | AI Core Dashboard, Gen AI Studio, UXD | `ai-studio`, `playground`, `mcp`, `tool-calling`, `must-do` | 3.6 |

**Rationale**: C1 and C2 form the critical first-time user journey — if users can't get from deployment to playground, nothing else matters. H4 is high because opaque tool execution makes MCP (a strategic investment) appear broken to users, and this is table-stakes functionality in competing products.

### Priority 2 — Should-Do (High severity, multi-participant, or strategic alignment)

| # | Proposed RFE Title | Finding | Severity | Components | Key Labels | Target |
|---|---|---|---|---|---|---|
| 4 | **Clarify Model Source Identifiers in Deployment Wizard** | H1 | High | AI Core Dashboard, AI Hub, UXD | `ai-hub`, `model-serving`, `should-do` | 3.6 |
| 5 | **Default Project Selector to Show All Accessible Projects** | H2 | High | AI Core Dashboard, UXD | `dashboard`, `ai-studio`, `should-do` | 3.6 |
| 6 | **Playground Creation Progress Feedback** | H5 | High | AI Core Dashboard, Gen AI Studio, UXD | `ai-studio`, `playground`, `llama-stack-core`, `should-do` | 3.6 |
| 7 | **Gen AI Studio Feature Discoverability Audit** | H3 | High | AI Core Dashboard, Gen AI Studio, UXD | `ai-studio`, `playground`, `mcp`, `rag`, `should-do` | 3.6 |
| 8 | **Display Active Configuration per Chat Pane in Compare Mode** | M7 | Medium | AI Core Dashboard, Gen AI Studio, UXD | `ai-studio`, `playground`, `should-do` | 3.6 |

### Priority 3 — Nice-to-Do (Medium severity, strategic, or future-release candidates)

| # | Proposed RFE Title | Finding | Severity | Components | Key Labels | Target |
|---|---|---|---|---|---|---|
| 9 | **Position MCP as First-Class Context Strategy Alongside RAG** | G3 | Strategic | AI Core Dashboard, Gen AI Studio, UXD | `ai-studio`, `playground`, `mcp`, `rag`, `agentic`, `should-do` | 3.7 |
| 10 | **Explicit Validation Scope Labeling for Models** | G4 | Strategic | AI Hub, Model Validation, UXD | `ai-hub`, `model-serving`, `should-do` | 3.7 |
| 11 | **Chunking and Embedding Configuration with Chunk Inspection** | G2 | Strategic | AI Core Dashboard, Gen AI Studio, RAG + Vector DB, UXD | `ai-studio`, `playground`, `rag`, `should-do` | 3.7 |
| 12 | **Editable Model Deployment Settings Post-Deploy** | M2 | Medium | AI Core Dashboard, UXD | `model-serving`, `ai-studio`, `should-do` | 3.7 |
| 13 | **Input Validation for Gen AI Studio Configuration Forms** | M4 | Medium | AI Core Dashboard, Gen AI Studio, UXD | `ai-studio`, `playground`, `should-do` | 3.6 |
| 14 | **Collapsible Thinking Blocks in Playground Chat** | M6 | Medium | AI Core Dashboard, Gen AI Studio, UXD | `ai-studio`, `playground`, `should-do` | 3.6 |

### Already Covered (no new RFE needed)

| Finding | Covered By |
|---------|-----------|
| C3 — Undiscoverable tool calling config | [RHAISTRAT-1472](https://redhat.atlassian.net/browse/RHAISTRAT-1472), [RHAISTRAT-2008](https://redhat.atlassian.net/browse/RHAISTRAT-2008) (Closed) |
| M1 — Deployment status lag | [RHOAIENG-15568](https://redhat.atlassian.net/browse/RHOAIENG-15568) + proposed C2 RFE |
| M3 — OIDC/short-lived tokens | [RHAISTRAT-2085](https://redhat.atlassian.net/browse/RHAISTRAT-2085), [RHAISTRAT-2089](https://redhat.atlassian.net/browse/RHAISTRAT-2089) |
| M5 — Chat state management | [RHAISTRAT-1533](https://redhat.atlassian.net/browse/RHAISTRAT-1533), [RHAISTRAT-1534](https://redhat.atlassian.net/browse/RHAISTRAT-1534) |
| L2 — Misleading readiness signals | [RHOAIENG-15568](https://redhat.atlassian.net/browse/RHOAIENG-15568) |
| L5 — RAG auto-enable bug | Should be filed as RHOAIENG bug |
| G1 — Try before deploy | [RHAISTRAT-1744](https://redhat.atlassian.net/browse/RHAISTRAT-1744), [RHAISTRAT-1935](https://redhat.atlassian.net/browse/RHAISTRAT-1935), [RHAISTRAT-2049](https://redhat.atlassian.net/browse/RHAISTRAT-2049) |
| G5 — HuggingFace as primary source | Functional today; friction addressed by H1 RFE |

### Low priority — bundle into UX polish pass

| Finding | Notes |
|---------|-------|
| L1 — Ambiguous deployment form labels | Bundle into GA polish |
| L3 — Missing external access path | Documentation improvement |
| L4 — Non-standard parameter scale | UX polish |

---

## Appendix: Study Methodology Notes

- **Recruitment**: Participants were enterprise MLOps/AI Platform Engineers recruited based on their day-to-day tasks (not self-selected)
- **Environment**: RHOAI 3.4 GA cluster
- **Task flow**: Discovery (HuggingFace/catalog) → Model deployment → Gen AI Playground configuration (including RAG and MCP)
- **Limitations**: 5 participants is a small sample; findings should be weighted by the number of participants affected and corroborated by field/CAI feedback where noted
- **Full findings deck**: [Google Slides](https://docs.google.com/presentation/d/1GRVPO34oUhFXvlikCBJ-czBMCStX0fJPz6B03xFBPZ4/)
- **Related UX initiative**: [RHOAIUX-2353](https://redhat.atlassian.net/browse/RHOAIUX-2353) — Using jira-to-lo-fi-prototype skill to rapidly prototype based on RFE requirements for refinement discussions
