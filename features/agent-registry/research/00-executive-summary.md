---
title: Agent Registry Research - Executive Summary
description: Synthesis of all agent ecosystem research into actionable findings for the MLflow Agent Registry RFC and RHOAI agent governance strategy.
source: ai-asset-registry/agents/agent-registry/research/00-executive-summary.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Registry Research - Executive Summary

**Date**: 2026-04-24
**Author**: Peter Double (Principal PM - MCP & AI Asset Registries)
**Purpose**: Synthesize all agent ecosystem research into actionable findings for the MLflow Agent Registry RFC and RHOAI agent governance strategy.

---

## The Bottom Line

The AI agent market is projected to grow from $7.8B to $52.6B by 2030 (44-46% CAGR), and enterprises are already deploying multi-agent systems. Yet no open-source platform offers a dedicated agent registry. AWS launched the first hyperscaler Agent Registry in April 2026, validating the market need, but it is proprietary and cloud-locked. The A2A protocol has achieved critical mass (150+ orgs, 22K+ stars, IBM ACP merged into A2A in August 2025, Linux Foundation governance), establishing a de facto standard for agent interoperability. MLflow has model, prompt, and skill registries but no agent registry. The `mlflow.agents` namespace exists but is empty. No competing proposals exist in the MLflow GitHub. This creates a first-mover opportunity for Red Hat.

Red Hat should submit an upstream MLflow RFC defining `RegisteredAgent` / `AgentVersion` entities following the proven Entity+Version pattern, with a plugin-based discovery interface that keeps Kubernetes-specific integration downstream. This positions RHOAI to deliver agent governance as a natural extension of existing registry capabilities, differentiated by open-source foundations, Kubernetes-native runtime integration through kagenti, cross-registry composition tracking (agents referencing models, tools, prompts, skills, and other agents), and SPIFFE-based workload identity. The immediate priority is securing the MLflow namespace before a competitor does.

## Research Documents

| # | Document | What It Covers |
|---|----------|----------------|
| 01 | [Agent Ecosystem Analysis](01-agent-ecosystem.md) | Agent definitions, 12 frameworks, composition patterns, AgentCard as metadata standard |
| 02 | [Standards and Protocols](02-standards-and-protocols.md) | MCP/A2A/Oracle protocol stack, AAIF governance, NIST initiative, design principles |
| 03 | [Kagenti and Kubernetes](03-kagenti-and-kubernetes.md) | Three K8s agent projects, kagenti architecture, MLflow integration patterns |
| 04 | [Agent Management Landscape](04-agent-management-landscape.md) | AWS/IBM/Google/Microsoft/Salesforce platforms, 5 OSS platforms, market gaps |
| 05 | [MLflow Upstream Strategy](05-mlflow-upstream.md) | Entity+Version pattern, Skills Registry precedent, RFC process, Red Hat contributors |
| 06 | [RHOAI Context and Patterns](06-rhoai-context.md) | MCP/skills pattern reuse, agent-specific differences, stakeholder open questions |

## Key Findings

1. **"Agent" has three distinct meanings the registry must serve.** Agent-as-code (development artifact), agent-as-service (running endpoint), and agent-as-record (governance metadata) each require different registry capabilities. The MLflow RFC should define the agent-as-record primitives; agent-as-service discovery belongs in the plugin layer.

2. **A2A AgentCard is the de facto agent metadata standard.** Adopted by AWS, Google, IBM BeeAI, kagenti, and Microsoft, AgentCard provides structured capability descriptions, authentication requirements, and endpoint information. The MLflow `RegisteredAgent` schema should align with AgentCard fields to enable seamless round-tripping between registry records and runtime discovery.

3. **The three-layer protocol stack is stabilizing.** MCP handles agent-to-tool communication, A2A handles agent-to-agent communication, and Oracle Agent Spec handles declarative definitions. All three are governed by AAIF under the Linux Foundation (Red Hat is a Gold member). This stability de-risks building registry infrastructure on these standards.

4. **Agents are composite assets with unique dependency graphs.** An agent may reference models, tools, prompts, guardrails, knowledge sources, and other agents. No existing registry tracks these cross-asset composition relationships. This is the single most valuable capability the MLflow Agent Registry can provide and the strongest differentiator for RHOAI's cross-registry approach.

5. **MLflow's Entity+Version pattern is proven and predictable.** `RegisteredModel`/`ModelVersion`, `Prompt`/`PromptVersion`, `Skill`/`SkillVersion` all follow the same architecture. The Skills Registry MVP validated using dedicated database tables rather than tag-based hacks on `ModelVersion`. The agent registry should follow this pattern with `RegisteredAgent`/`AgentVersion` and dedicated tables.

6. **Pre-deployment and post-deployment are both required.** Varsha's earlier proposal covered only post-deployment agent discovery. A complete registry must also handle pre-deployment governance: versioning agent definitions, tracking composition, enforcing policies before agents reach production. The MLflow RFC addresses pre-deployment; kagenti integration addresses post-deployment.

7. **AWS validated the registry-as-MCP-server pattern.** AWS Bedrock Agent Registry exposes registered agents as MCP server resources, enabling AI assistants to discover and invoke agents through the same protocol used for tools. This pattern should inform the RHOAI catalog surface design.

8. **Kagenti provides Kubernetes-native agent runtime, but MLflow must remain platform-agnostic.** Kagenti's operator, AgentCard CRD, SPIFFE/SPIRE identity, and Istio Ambient mesh integration are powerful for RHOAI. However, the upstream MLflow RFC must define an `AgentDiscoveryProvider` plugin interface with `mlflow.agent_discovery` entry points, keeping Kubernetes as one discovery source among Docker, cloud services, static configurations, and SaaS platforms.

9. **No open-source platform has a dedicated agent registry.** LangSmith, CrewAI, AutoGen, Semantic Kernel, and Haystack all lack registry capabilities for agents. The five enterprise platforms surveyed (AWS, IBM, Google, Microsoft, Salesforce) are all proprietary. MLflow with an agent registry would be the first open-source solution.

10. **Governance is the enterprise differentiator, not features.** IBM watsonx leads with deepest governance (100+ prebuilt agents, regulatory compliance). AWS leads with hybrid search and first-mover advantage. Google leads with the A2A reference implementation. But none offer open-source, auditable governance with Kubernetes-native identity. RHOAI can own this space.

11. **Seven of ten MCP registry patterns transfer to agents, but three do not.** Agents differ from MCP servers in fundamental ways: they are running services with endpoints, they have dual state (governance record plus runtime status), they use diverse protocols (A2A, MCP, HTTP, gRPC), they require capability-based discovery, and they need cryptographic identity. The registry design must accommodate these differences rather than forcing agents into the MCP model.

12. **The MLflow namespace is unoccupied and the RFC design-approval process typically takes several weeks.** Red Hat has active contributors (Matt Prahl with 20+ PRs, Edson Tirelli as Databricks liaison, Dan Kuc on registry engineering). No competing agent registry proposals exist. Moving quickly is more important than perfecting the design, since the plugin architecture allows iteration without breaking the core API.

## Competitive Positioning

| Competitor | Strength | RHOAI Differentiator |
|------------|----------|---------------------|
| AWS AgentCore | First-mover agent registry, hybrid search, registry-as-MCP-server pattern | Open-source MLflow foundation; no cloud lock-in; cross-registry composition |
| IBM watsonx | Deepest governance, 100+ prebuilt agents, regulatory compliance focus | Kubernetes-native identity (SPIFFE); open governance model; community-driven |
| Google Gemini Platform | ADK ecosystem, API Registry, A2A reference implementation | Multi-cloud/hybrid deployment; not tied to single model provider |
| Microsoft | Agent Framework 1.0, 75K+ GitHub stars combined, broad developer reach | Dedicated registry (Microsoft has none); enterprise governance layer |
| Salesforce | A2A in production at 150+ orgs, MuleSoft Agent Fabric | General-purpose platform; not restricted to CRM/sales domain |

**RHOAI's combined differentiators**: open-source MLflow foundation, Kubernetes-native runtime via kagenti, cross-registry composition tracking (agents to models to tools to prompts to skills), SPIFFE workload identity, and hybrid/multi-cloud deployment without cloud provider lock-in.

## Architecture Patterns Worth Adopting

**From internal projects (MCP and Skills registries):**
- Entity+Version with dedicated database tables (not tag-based ModelVersion overlay)
- Plugin-based discovery providers with standard entry points (`mlflow.agent_discovery`)
- Separation of upstream primitives (registration, versioning, search) from downstream governance (policy enforcement, approval workflows, audit trails)
- Metadata-first approach: store the agent record; defer runtime concerns to plugins

**From market (AWS, A2A, kagenti):**
- Registry-as-MCP-server: expose registered agents as MCP resources for AI-assisted discovery (AWS pattern)
- AgentCard as the interchange format between registry records and runtime endpoints (A2A standard)
- Operator + CRD pattern for Kubernetes-native lifecycle management (kagenti architecture)
- Hybrid integration model: Pull (watch CRDs for changes), Push (webhook on registration), or Hybrid (both) for connecting registry to runtime platforms
- SPIFFE/SPIRE for cryptographic workload identity rather than API key rotation (kagenti security model)
- Capability-based discovery: search by what agents can do, not just by name or tag (A2A AgentCard capability fields)

## Recommended Next Steps

### Immediate (Weeks 1-2)
- Submit the MLflow RFC defining `RegisteredAgent` / `AgentVersion` entities with the Entity+Version pattern and `AgentDiscoveryProvider` plugin interface
- Engage Edson Tirelli (Databricks liaison) and Matt Prahl on timing and review process
- Align the `RegisteredAgent` schema fields with A2A AgentCard to minimize impedance mismatch
- Circulate this research summary with RHOAI PM and engineering leadership (Adam Bellusci, Landon LaSmith, kagenti team) for alignment

### Short-Term (Weeks 3-8)
- Implement the kagenti `AgentDiscoveryProvider` plugin as the first concrete discovery source
- Build RHOAI governance extensions on top of upstream primitives: approval workflows, policy enforcement, audit logging
- Define the cross-registry composition schema linking agents to their constituent models, tools, prompts, skills, and sub-agents
- Coordinate with the kagenti team on AgentCard CRD alignment with the MLflow schema

### Medium-Term (Weeks 9-16)
- Deliver cross-registry composition tracking in the RHOAI UI, showing full dependency graphs for registered agents
- Implement A2A AgentCard import/export so agents discovered at runtime can be registered, and registered agents can publish AgentCards
- Build catalog surface for agent discovery, following the registry-as-MCP-server pattern validated by AWS
- Contribute upstream MLflow CLI/SDK commands (`mlflow.agents.register()`, `mlflow.agents.load()`, `mlflow.agents.search()`)

## Open Questions for Stakeholder Input

1. **Schema scope for the MLflow RFC**: Should the upstream `RegisteredAgent` include composition references (links to models, tools, prompts) or should composition tracking be a downstream RHOAI extension only?
2. **AgentCard alignment depth**: Should `RegisteredAgent` fields map 1:1 to A2A AgentCard, or should MLflow define its own schema with an AgentCard export function?
3. **Dual-state management**: How should the registry handle the gap between a registered agent definition (pre-deployment) and a discovered running agent (post-deployment)? Are these the same entity at different lifecycle stages or separate entities with references?
4. **Kagenti coupling**: Kagenti is targeting RHOAI 3.5 Tech Preview. Should the agent registry timeline be coupled to kagenti readiness, or should the registry ship independently with static/manual registration first?
5. **Multi-agent composition governance**: When an agent orchestrates sub-agents, should the registry enforce that all sub-agents are also registered? What happens when a sub-agent version changes?
6. **Testing and validation**: No agent testing framework standards exist. Should RHOAI define testing metadata fields in the registry, or defer to emerging standards (NIST AI Agent Standards Initiative, expected 2026-2027)?
7. **Plugin architecture feedback**: Databricks requested revisions to the plugin architecture proposal. What specific concerns need to be addressed before resubmission?

## File Index

| File | Description |
|------|-------------|
| [00-executive-summary.md](00-executive-summary.md) | This document -- synthesis of all research findings |
| [01-agent-ecosystem.md](01-agent-ecosystem.md) | Agent definitions, frameworks, composition patterns, metadata standards |
| [02-standards-and-protocols.md](02-standards-and-protocols.md) | Protocol stack (MCP/A2A/Oracle), governance bodies, design principles |
| [03-kagenti-and-kubernetes.md](03-kagenti-and-kubernetes.md) | Kubernetes agent projects, kagenti architecture, MLflow integration |
| [04-agent-management-landscape.md](04-agent-management-landscape.md) | Enterprise and OSS platform survey, market sizing, competitive gaps |
| [05-mlflow-upstream.md](05-mlflow-upstream.md) | MLflow registry patterns, namespace analysis, RFC strategy |
| [06-rhoai-context.md](06-rhoai-context.md) | RHOAI pattern reuse, agent-specific differences, open questions |
