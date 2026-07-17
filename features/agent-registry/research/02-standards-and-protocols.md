---
title: Agent Registry Research - Agent Standards & Protocols
description: Deep technical analysis of the standards informing the agent registry data model and discovery architecture.
source: ai-asset-registry/agents/agent-registry/research/02-standards-and-protocols.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Registry Research - Agent Standards & Protocols

> Superseded 2026-07-16 in part by [07-upstream](07-upstream.md) — A2A is v1.0.1 with four official extensions and dual-version card advertising; ARD (Google+Microsoft) now formalizes federated discovery; the AAIF three-layer framing stands.

**Date**: 2026-04-24
**Author**: Peter Double (Principal PM - MCP & AI Asset Registries)
**Purpose**: Deep technical analysis of the standards that inform the agent registry data model and discovery architecture.

---

## 1. The Three-Layer Protocol Stack

The agentic AI ecosystem has converged on a layered protocol architecture. Industry consensus -- reinforced by the co-governance of both protocols under the Linux Foundation's Agentic AI Foundation (AAIF) -- treats MCP and A2A as complementary layers rather than competing alternatives.

### The Stack

| Layer | Protocol | Purpose | Created By | Date | Governance |
|---|---|---|---|---|---|
| **Agent-to-Tool** | MCP (Model Context Protocol) | Standardized access to tools, data sources, and external services | Anthropic | November 2024 | AAIF / Linux Foundation (Dec 2025) |
| **Agent-to-Agent** | A2A (Agent-to-Agent Protocol) | Discovery, delegation, and coordination between autonomous agents | Google | April 2025 | AAIF / Linux Foundation (Jun 2025) |
| **Agent Definition** | Oracle Agent Spec | Framework-agnostic declarative agent definitions | Oracle | October 2025 | Open source (Apache 2.0) |

MCP provides the *vertical integration* layer -- how an individual agent connects to external capabilities. A2A provides the *horizontal coordination* layer -- how agents discover and collaborate with each other. Oracle's Agent Spec sits alongside both, providing a *declarative definition* layer for how agents are specified before deployment.

As DigitalOcean's technical comparison summarizes: "MCP connects agents to tools. A2A connects agents to other agents" ([DigitalOcean, A2A vs MCP](https://www.digitalocean.com/community/tutorials/a2a-vs-mcp-ai-agent-protocols), 2026). Google explicitly positions A2A as a companion to MCP, not a replacement ([A2A Protocol: A2A and MCP](https://a2a-protocol.org/latest/topics/a2a-and-mcp/), 2026).

### Why This Matters for the Registry

An Agent Registry must understand all three layers:

- **MCP layer**: Track which MCP servers (tools) an agent uses -- this is the MCP Registry's domain, but the Agent Registry cross-references it.
- **A2A layer**: The AgentCard is the canonical metadata format for describing agent capabilities. The registry adopts this as its base schema.
- **Definition layer**: Pre-deployment agent definitions (Oracle Agent Spec, LangGraph graphs, CrewAI YAML) represent the governed artifact before deployment.

The [01-agent-ecosystem](01-agent-ecosystem.md) document established that "agent" spans three meanings: agent-as-code, agent-as-service, and agent-as-record. The protocol stack maps directly: Agent Spec governs agent-as-code, A2A governs agent-as-service, and the registry provides agent-as-record linking both.

---

## 2. A2A Protocol Deep Dive

The Agent-to-Agent (A2A) protocol is the most consequential standard for Agent Registry design. Released by Google on April 9, 2025, with support from over 50 enterprise partners, A2A defines how autonomous agents discover each other, exchange tasks, and coordinate outcomes -- regardless of vendor, framework, or platform.

A2A reached v1.0 in early 2026, marking its first production-ready release. As of April 2026, the protocol has over 150 participating organizations, 22,000+ GitHub stars, and production deployments inside Azure AI Foundry and Amazon Bedrock AgentCore ([Stellagent, A2A one-year retrospective](https://stellagent.ai/insights/a2a-protocol-google-agent-to-agent), April 2026).

### 2.1 AgentCard Specification

The AgentCard is the foundational metadata structure -- the "business card" that every A2A-compatible agent publishes. It is a JSON document typically hosted at `/.well-known/agent-card.json` under the agent's base URL ([A2A Specification](https://a2a-protocol.org/latest/specification/), 2026).

#### AgentCard Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Unique identifier for the agent |
| `name` | string | Yes | Human-readable name |
| `description` | string | Yes | Functional description of the agent |
| `version` | string | Yes | Agent version (provider-defined format) |
| `provider` | `AgentProvider` | Yes | Organization info: `organization`, `url` |
| `capabilities` | `AgentCapabilities` | Yes | Feature flags: `streaming`, `pushNotifications`, `stateTransitionHistory`, `extended_agent_card` |
| `skills` | `AgentSkill[]` | No | Structured capability declarations (see Section 2.2) |
| `interfaces` | `AgentInterface[]` | Yes | Protocol bindings with URLs and version info (see Section 2.5) |
| `securitySchemes` | map of `SecurityScheme` | Yes | Authentication methods (OAuth2, Bearer, ApiKey, Basic) |
| `security` | array | Yes | Required security scheme references with scopes |
| `defaultInputModes` | `string[]` | No | Default accepted media types (e.g., `application/json`, `text/plain`) |
| `defaultOutputModes` | `string[]` | No | Default produced media types |
| `documentationUrl` | string | No | URL to agent documentation |
| `iconUrl` | string | No | URL to agent icon |
| `extensions` | `AgentExtension[]` | No | Supported protocol extensions |
| `signatures` | `AgentCardSignature[]` | No | JWS digital signatures for verification (see Section 2.3) |

**Source**: [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/), April 2026.

#### Discovery Mechanism

Agents expose their AgentCard at a well-known URL path: `https://<base_url>/.well-known/agent-card.json`. This path was updated from `/.well-known/agent.json` in v0.3 based on IANA feedback ([A2A What's New in v1.0](https://a2a-protocol.org/latest/whats-new-v1/), 2026).

Agents may also support an *extended Agent Card* accessible only after authentication, indicated by `capabilities.extended_agent_card: true`. Clients retrieve the extended card via the `GetExtendedAgentCard` operation, which may return additional skills or configuration details not present in the public card. This two-tier model is relevant for registries that need to store both public and authenticated metadata.

### 2.2 AgentSkill Structure

Each `AgentSkill` describes a distinct capability the agent can perform. Skills are the unit of discoverability -- clients search for agents by matching skill descriptions, tags, and supported modes.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Unique skill identifier (e.g., `create_burger_order`) |
| `name` | string | Yes | Human-readable skill name |
| `description` | string | Yes | What this skill does |
| `tags` | `string[]` | No | Keywords/categories for discovery and routing |
| `examples` | `string[]` | No | Example prompts or usage scenarios |
| `inputModes` | `string[]` | No | Accepted content types (overrides agent default) |
| `outputModes` | `string[]` | No | Produced content types (overrides agent default) |

**Source**: [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/), April 2026; [Google A2A Codelab](https://codelabs.developers.google.com/intro-a2a-purchasing-concierge), 2026.

Example from Google's A2A Codelab:

```python
skill = AgentSkill(
    id="create_burger_order",
    name="Burger Order Creation Tool",
    description="Helps with creating burger orders",
    tags=["burger order creation"],
    examples=["I want to order 2 classic cheeseburgers"],
)
```

**Registry implication**: AgentSkill is deliberately lightweight -- it has no parameter schemas, no typed input/output definitions, and no formal contract. This contrasts with MCP tools, which have full JSON Schema definitions for parameters. An Agent Registry may need to extend AgentSkill with optional parameter schemas for governance purposes, or cross-reference MCP tool definitions where skills map to tool invocations.

Varsha's upstream proposal already defines an extended `AgentSkill` with an additional `parameters: list[SkillParameter]` field -- an important governance extension over the base A2A spec (see [agent-registry-upstream-proposal.md](/features/agent-registry/strategy/upstream-proposal.md)).

### 2.3 Signed Agent Cards (JWS)

Signed Agent Cards are arguably the most important enterprise feature in A2A v1.0. Without cryptographic signatures, an attacker could stand up a fake AgentCard and redirect other agents into a card forgery attack. Signed Agent Cards make decentralized discovery viable for production systems.

#### Specification

Agent Cards MAY be digitally signed using JSON Web Signature (JWS) as defined in RFC 7515 to ensure authenticity and integrity. The `AgentCardSignature` object follows the JWS JSON format:

| Field | Type | Required | Description |
|---|---|---|---|
| `protected` | string | Yes | Base64url-encoded JSON object containing the JWS Protected Header (`alg`, `typ`, `kid`, optional `jku`) |
| `signature` | string | Yes | Base64url-encoded signature value |
| `header` | object | No | JWS Unprotected Header (JSON, not base64url-encoded) |

**Source**: [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/), April 2026; RFC 7515 (JSON Web Signature).

#### Canonicalization Requirement

Before signing, the AgentCard content MUST be canonicalized using the JSON Canonicalization Scheme (JCS) as defined in RFC 8785. This ensures consistent signature generation and verification across different JSON implementations, regardless of field ordering, whitespace, or Unicode normalization.

#### Signing Process

1. Construct a JSON object with required header parameters (`alg`, `typ`, `kid`) and optional parameters (`jku` for key URL)
2. Construct the JWS Signing Input: `ASCII(BASE64URL(UTF8(JWS Protected Header)) || '.' || BASE64URL(JWS Payload))`
3. Sign the input using the specified algorithm and private key
4. Base64url-encode the resulting signature bytes

#### Registry Implications

JWS-signed AgentCards have direct implications for the Agent Registry:

- **Trust verification**: The registry can verify an agent's identity before admitting it, rejecting cards with invalid or missing signatures
- **Integrity assurance**: Signed cards guarantee that agent metadata hasn't been tampered with between publication and registration
- **Certificate chain**: The `jku` (JSON Web Key URL) parameter enables key discovery, supporting PKI-based trust hierarchies
- **Alignment with kagenti**: The kagenti platform already verifies JWS signatures on AgentCards before caching them in AgentCard CRD status. The MLflow plugin reads pre-verified cards, inheriting kagenti's trust validation

### 2.4 Task Lifecycle

A2A models agent interactions as stateful Tasks with a well-defined state machine. This lifecycle is critical for registry-level health monitoring and status tracking.

#### Task States

| State | Category | Description |
|---|---|---|
| `TASK_STATE_SUBMITTED` | Active | Task has been submitted, awaiting processing |
| `TASK_STATE_WORKING` | Active | Agent is actively processing the task |
| `TASK_STATE_INPUT_REQUIRED` | Interrupted | Agent needs additional input from the client |
| `TASK_STATE_AUTH_REQUIRED` | Interrupted | Authentication is required before proceeding |
| `TASK_STATE_COMPLETED` | Terminal | Task completed successfully |
| `TASK_STATE_FAILED` | Terminal | Task failed during processing |
| `TASK_STATE_CANCELED` | Terminal | Task was canceled by the client |
| `TASK_STATE_REJECTED` | Terminal | Agent rejected the task |
| `TASK_STATE_UNKNOWN` | Terminal | State is unknown |

**Source**: [A2A Task Lifecycle](https://a2a-protocol.org/latest/topics/life-of-a-task/), 2026; [DeepWiki A2A Task State Management](https://deepwiki.com/a2aproject/A2A/2.5-task-lifecycle-and-state-management), 2026.

Note: v1.0 changed enum values from kebab-case (e.g., `"completed"`) to SCREAMING_SNAKE_CASE (e.g., `"TASK_STATE_COMPLETED"`) for ProtoJSON compliance.

#### State Transition Rules

```
submitted --> working --> completed (terminal)
    |            |------> failed (terminal)
    |            |------> canceled (terminal)
    |            |------> input_required --> working (resumed)
    |                                   --> canceled (terminal)
    |-------> rejected (terminal)
    |-------> auth_required --> working (authenticated)
                           --> rejected (auth failed)
```

**Key design principles**:
- **Immutability**: Once a task reaches a terminal state, it cannot restart. Subsequent interactions must create a new task within the same `contextId`.
- **Context continuity**: The `contextId` groups related tasks across complex multi-turn interactions, enabling stateful conversations.
- **Deterministic transitions**: Tasks follow well-defined paths through the state machine, with no ambiguous or undocumented transitions.

**Registry implication**: The task lifecycle maps to agent health monitoring. A registry can observe task completion rates, failure patterns, and `input_required` frequency to assess agent reliability and surface health metrics.

### 2.5 Multi-Tenancy and Multi-Protocol Bindings

A2A v1.0 introduced two enterprise-critical features that directly impact registry design.

#### Multi-Tenancy

A `tenant` field was added to all request messages, enabling a single endpoint to securely host multiple agents per tenant. This is essential for SaaS providers serving different agents per organizational context.

The registry must support tenant-scoped agent discovery -- querying for agents visible to a specific tenant, not just globally registered agents.

#### Multi-Protocol Bindings

The `supportedInterfaces` field in the AgentCard declares the agent's available protocol bindings. Each `AgentInterface` specifies:

| Field | Type | Description |
|---|---|---|
| `url` | string | Service endpoint URL |
| `protocolBinding` | string | Transport protocol (`JSONRPC`, `GRPC`, `HTTP`) |
| `protocolVersion` | string | A2A protocol version (e.g., `"1.0"`) |

Agents list interfaces in preference order -- the first entry is the preferred binding. Clients parse `supportedInterfaces` sequentially and select the first transport they support.

**Binding requirements**: All supported protocols MUST provide the same set of operations, return semantically equivalent results, map errors consistently, and support the same authentication schemes declared in the AgentCard.

Official bindings use the `https://a2a-protocol.org/bindings/` URI prefix. Custom bindings are supported but must comply with all binding requirements in the specification.

**Registry implication**: The registry stores the full `supportedInterfaces` array, enabling clients to query agents by protocol binding (e.g., "find all agents supporting gRPC") and facilitating routing decisions based on available transports.

### 2.6 Version History

The A2A protocol has evolved rapidly from initial draft to production-ready standard:

| Date | Version | Key Changes |
|---|---|---|
| April 9, 2025 | v0.1.0 | Initial announcement at Google Cloud Next. JSON-RPC 2.0 over HTTP, AgentCards, Tasks, SSE streaming. 50+ launch partners. |
| ~May 2025 | v0.2 | Authentication enhancements: formal `securitySchemes` and `security` fields in AgentCard. OpenAPI-aligned auth methods. |
| June 23, 2025 | -- | Donated to Linux Foundation. Founding members: AWS, Cisco, Google, Microsoft, Salesforce, SAP, ServiceNow. |
| July 30, 2025 | v0.3.0 | Stability release. gRPC support, signed Agent Cards (initial), IANA-compliant well-known path (`agent-card.json`), Python SDK improvements. Backward compatibility commitment starts. |
| August 2025 | -- | IBM's ACP merged into A2A under LF AI & Data (see Section 4). |
| Early 2026 | v1.0 | Production-ready. Three-layer architecture (Protobuf canonical model, abstract operations, protocol bindings). Unified Part type. SCREAMING_SNAKE_CASE enums. Multi-tenancy. JWS-signed Agent Cards with RFC 8785 canonicalization. OAuth 2.0 modernization (Device Code, PKCE). Version negotiation. |

**Sources**: [A2A Releases](https://github.com/a2aproject/A2A/releases); [A2A What's New in v1.0](https://a2a-protocol.org/latest/whats-new-v1/); [A2A v1.0 Announcement](https://a2a-protocol.org/latest/announcing-1.0/); [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade), 2025.

The v1.0 release represents a significant architectural maturation. The elevation of `a2a.proto` (Protocol Buffers) as the normative specification source ensures protocol neutrality and provides a deterministic evolution path. This is important for registry implementers -- the Protobuf definitions serve as a machine-readable schema that registries can validate against.

---

## 3. MCP Relationship

Understanding how MCP and A2A intersect is essential for designing a registry that governs agents without duplicating the MCP Registry's concerns. The [01-agent-ecosystem](01-agent-ecosystem.md) document established the abstraction ladder: agents sit at the top, skills/capabilities below, and tools/functions at the base. MCP operates at the tool/function layer; A2A operates at the agent/skill layer.

### 3.1 MCP Tools vs. A2A Skills

MCP tools and A2A skills describe agent capabilities at different levels of abstraction:

| Dimension | MCP Tool | A2A AgentSkill |
|---|---|---|
| **Granularity** | Atomic function with typed parameters | High-level capability description |
| **Schema** | Full JSON Schema for inputs and outputs | No parameter schema; free-text description, tags, examples |
| **Execution model** | Deterministic API call with structured I/O | Multi-turn, potentially stateful task delegation |
| **Discovery** | Listed by MCP server in `tools/list` response | Listed in AgentCard `skills[]` array |
| **Invocation** | Direct `tools/call` with typed arguments | `SendMessage` initiating a stateful Task |
| **State** | Stateless (each call is independent) | Stateful (task lifecycle with transitions) |

**Source**: [LlamaIndex: Skills vs MCP Tools](https://www.llamaindex.ai/blog/skills-vs-mcp-tools-for-agents-when-to-use-what), 2026; [Layered.dev: MCP vs Agent Skills](https://layered.dev/mcp-vs-agent-skills/), 2026.

The key insight is that MCP tools are *primitives* -- a calculator, a database query, a file read -- while A2A skills are *compositions* -- "help me file an expense report," which internally may invoke multiple MCP tools. An A2A skill often wraps one or more MCP tool invocations behind an opaque agent boundary.

### 3.2 The Complementary Architecture

In a production multi-agent system, both protocols operate simultaneously:

```
[Client Application]
     |
     |-- A2A --> [Agent A: Expense Manager]
                    |
                    |-- MCP --> [Receipts Database Server]
                    |-- MCP --> [Accounting API Server]
                    |-- A2A --> [Agent B: Approval Workflow]
                                   |
                                   |-- MCP --> [HR System Server]
                                   |-- MCP --> [Notification Server]
```

Agent A is *discoverable* via its AgentCard (A2A layer). Its *internal capabilities* are powered by MCP servers (MCP layer). Agent A *delegates* to Agent B via A2A when it needs approval workflow expertise that it doesn't possess.

### 3.3 Registry Implications

The MCP Registry and Agent Registry are complementary, governing different layers of the stack:

| Registry | Governs | Metadata Standard | Lifecycle Focus |
|---|---|---|---|
| **MCP Registry** | MCP servers (tool providers) | MCP server capabilities, tool definitions, resource templates | Server availability, tool schema validation, trust certification |
| **Agent Registry** | Agents (autonomous services) | A2A AgentCard, skills, security, provider | Agent governance, composition tracking, skill discovery, identity verification |

The cross-reference between them is critical: an agent record in the Agent Registry should reference the MCP servers it depends on, and an MCP server record should know which agents consume its tools. This composition graph is the unique value proposition identified in the [01-agent-ecosystem](01-agent-ecosystem.md) document's Section 6.3.

---

## 4. Agentic AI Foundation (AAIF)

The Agentic AI Foundation (AAIF) is the governance body for both MCP and A2A, making it the single most important organizational factor for standard stability and long-term adoption.

### 4.1 Formation and Structure

AAIF was formed on December 9, 2025, as a directed fund under the Linux Foundation. The "directed fund" model minimizes upfront complexity -- rather than establishing a separate legal entity, AAIF operates within LF's nonprofit infrastructure, leveraging existing legal, accounting, and event capabilities ([Linux Foundation AAIF Announcement](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation), December 2025).

The founding projects were:
- **Model Context Protocol (MCP)** -- donated by Anthropic
- **goose** -- donated by Block
- **AGENTS.md** -- contributed by OpenAI

### 4.2 Membership

**Platinum Members** (governing board representation): Amazon Web Services, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI.

**Gold Members** (original): Adyen, Arcade.dev, Cisco, Datadog, Docker, Ericsson, IBM, JetBrains, Okta, Oracle, Runlayer, Salesforce, SAP, Shopify, Snowflake, Temporal, Tetrate, Twilio.

**Gold Members** (added February 2026): Akamai, American Express, Autodesk, Circle, Diagrid, Equinix, Global Payments, Hitachi, Huawei, Infobip, JPMorgan Chase, Keycard, Lenovo, **Red Hat**, ServiceNow, TELUS, UiPath, Workato.

As of April 2026, AAIF has grown to over 170 member organizations -- more than double the membership CNCF had at the same stage of its existence ([AAIF 97 New Members](https://www.linuxfoundation.org/press/agentic-ai-foundation-welcomes-97-new-members), February 2026).

**Source**: [AAIF Members](https://aaif.io/members/), April 2026; [OpenAI AAIF Blog](https://openai.com/index/agentic-ai-foundation/), December 2025; [Block AAIF Blog](https://block.xyz/inside/block-anthropic-and-openai-launch-the-agentic-ai-foundation), December 2025.

### 4.3 Leadership

- **Governing Board Chair**: David Nalley (Director of Developer Experience, AWS)
- **Executive Director**: Mazin Gilbert (PhD in neural networks, MBA from Wharton, previously at Google)
- **Technical Steering Committee**: Representatives from major member organizations; formal project lifecycle policy with three stages (Growth, Impact, Emeritus)

### 4.4 IBM ACP Merger into A2A

The merger of IBM's Agent Communication Protocol (ACP) into A2A is a significant consolidation event. IBM Research launched ACP in March 2025 to power its BeeAI Platform. The BeeAI project and ACP were donated to the Linux Foundation later that month. When A2A was announced in April 2025, the teams recognized alignment and began exploring convergence.

In August 2025, IBM officially announced that ACP would merge into A2A under the Linux Foundation umbrella. Key aspects of the merger ([LF AI & Data Blog](https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/), August 2025):

- **Unified governance**: Kate Blair joined the A2A Technical Steering Committee on behalf of IBM, alongside representatives from Google, Microsoft, AWS, Cisco, Salesforce, ServiceNow, and SAP
- **Technology integration**: ACP innovations incorporated into A2A's specification
- **Migration support**: Clear paths for existing ACP users to transition to A2A
- **BeeAI adoption**: The BeeAI platform now uses A2A natively; agents built with the BeeAI framework use the `A2AServer` adapter

The ACP merger eliminated A2A's largest potential competitor, making A2A the de facto standard for agent-to-agent communication. For registry design, this consolidation means the registry only needs to support A2A as the primary agent communication protocol, rather than hedging across multiple competing standards.

### 4.5 Implications for Standard Stability

AAIF's governance provides several assurances relevant to registry design decisions:

- **Neutral ownership**: Neither Google nor Anthropic controls the standards unilaterally; Linux Foundation governance ensures multi-stakeholder input
- **Adoption momentum**: 170+ members and production deployments at AWS, Microsoft, Salesforce, SAP, and ServiceNow indicate the standards are not experimental
- **Co-evolution**: MCP and A2A being governed under the same foundation ensures they evolve in coordination rather than diverging
- **Red Hat participation**: Red Hat joined as a Gold Member in February 2026, giving us direct input into standard evolution -- important for ensuring the Agent Registry aligns with upstream direction

---

## 5. Other Agent Standards

Beyond MCP, A2A, and AAIF, several other standards efforts are relevant to Agent Registry design. These standards address gaps that MCP and A2A do not cover -- declarative agent definitions, government evaluation frameworks, semantic interoperability, and security governance.

### 5.1 Oracle Open Agent Specification (Agent Spec)

Oracle's Open Agent Specification is a framework-agnostic declarative language for defining agentic systems. Released in October 2025 and published as open source under the Apache 2.0 license, Agent Spec provides a portable representation for agent configurations -- analogous to what ONNX did for ML models ([Oracle Blog: Introducing Agent Spec](https://blogs.oracle.com/ai-and-datascience/introducing-open-agent-specification), 2025).

#### Key Characteristics

- **Declarative definitions**: Agents are defined in JSON or YAML, specifying name, system prompt, LLM configuration, inputs/properties (with templating support), tools, and capabilities
- **Runtime adapters**: The specification separates agent *definition* from agent *execution*. Runtime adapters transform Agent Spec configurations into framework-specific representations. Supported runtimes include WayFlow (Oracle's reference runtime), LangGraph, AutoGen, and CrewAI
- **SDK support**: PyAgentSpec (Python) and tsagentspec (TypeScript)
- **Templated properties**: Agent definitions support dynamic variables (e.g., `"You are an expert in {{domain_of_expertise}}"`) using JSON Schema for input validation
- **Recent integrations**: Oracle, Google, and CopilotKit have jointly released an integration connecting Agent Spec (agent definition) with AG-UI (frontend streaming) and A2UI (agent-described UI), demonstrating the spec's composability ([Oracle Blog: AG-UI Integration](https://blogs.oracle.com/ai-and-datascience/announcing-ag-ui-integration-for-agent-spec), 2026)

**Source**: [GitHub: oracle/agent-spec](https://github.com/oracle/agent-spec); [Oracle Agent Spec Docs](https://oracle.github.io/agent-spec/), 2026.

#### Registry Relevance

Agent Spec addresses the "agent-as-code" representation identified in [01-agent-ecosystem](01-agent-ecosystem.md) Section 1. Where A2A's AgentCard describes a *running agent service*, Agent Spec describes an *agent definition before deployment*. The MLflow Agent Registry RFC should support storing Agent Spec configurations as pre-deployment artifacts, complementing A2A AgentCards as post-deployment metadata.

Oracle is a Gold Member of AAIF, which increases the likelihood of convergence between Agent Spec and the broader AAIF ecosystem over time.

### 5.2 NIST AI Agent Standards Initiative

On February 17, 2026, NIST's Center for AI Standards and Innovation (CAISI) announced the AI Agent Standards Initiative -- the first US government program dedicated explicitly to interoperability and security standards for agentic AI systems ([NIST Announcement](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure), February 2026).

#### Three Strategic Pillars

1. **Facilitating industry-led standards development**: NIST hosts technical convenings, conducts gap analyses, and produces voluntary guidelines to inform standardization. The emphasis is on facilitating, not creating standards.
2. **Fostering community-led open source protocol development**: Identifying and reducing barriers to interoperable agent protocols, with NSF investing in open-source agent ecosystems.
3. **Advancing research**: Fundamental research into agent authentication, identity infrastructure, and security evaluations.

#### Key Deliverables (2026)

| Deliverable | Status | Description |
|---|---|---|
| RFI on AI Agent Security | Closed March 9, 2026 | Ecosystem input on threats and mitigations |
| Identity & Authorization Concept Paper | Closed April 2, 2026 | NCC0E enterprise use cases for agent identity; asks whether existing standards (OAuth, SPIFFE, OIDC) suffice or new ones are needed |
| Sector-Specific Listening Sessions | April 2026 | Healthcare, financial services, education -- gathering sector-specific adoption barriers |

**Source**: [NIST AI Agent Standards Initiative](https://www.nist.gov/caisi/ai-agent-standards-initiative), 2026; [WorkOS NIST Explainer](https://workos.com/blog/nist-ai-agent-standards-initiative-explained), 2026.

#### NIST's Role: Integrator, Not Creator

NIST explicitly positions itself as a convener and facilitator rather than a direct standard creator. It does not compete with A2A, MCP, or IEEE P2894. Instead, NIST builds an "umbrella framework" that provides unified security baselines, interoperability level assessments, and compliance certification pathways above existing protocol-level standards ([Meta Intelligence: NIST Agent Standards](https://www.meta-intelligence.tech/en/insight-nist-agent-standards), 2026).

#### Registry Relevance

NIST's identity and authorization work directly impacts Agent Registry design. The NCC0E concept paper's question -- whether existing identity standards (OAuth, SPIFFE, OIDC) suffice for AI agents -- aligns with the registry's need for identity verification. The registry should track which identity mechanism each agent uses and verify credentials against NIST-aligned standards. The voluntary guidelines NIST publishes in 2026 are expected to appear in compliance frameworks and vendor questionnaires by 2027.

### 5.3 IEEE P2894

IEEE P2894 focuses on the semantic interoperability of agent capability descriptions. Originally scoped as a "Guide for an Architectural Framework for Explainable AI," recent sources (2025-2026) reference P2894 in the context of AI agent interoperability -- specifically cross-organization semantic alignment of agent capabilities.

NIST positions IEEE P2894 as a supplementary standard for Level 4 federated interoperability, particularly in cross-organization agent semantic alignment. This addresses a gap that A2A's AgentSkill descriptions alone cannot fill: ensuring that when Agent A describes a skill as "financial analysis" and Agent B describes a skill as "fiscal reporting," a registry or discovery system can determine whether these represent overlapping or distinct capabilities.

#### Registry Relevance

Semantic interoperability is a long-term concern for registries operating at scale. In the near term, skill discovery relies on keyword matching and tag-based filtering. As agent ecosystems grow, ontology-based semantic matching (aligned with IEEE P2894's direction) will become necessary for accurate discovery across organizational boundaries. This is covered in upcoming documents.

### 5.4 Oasis Security Agentic Access Management (AAM) Framework

The Agentic Access Management (AAM) Framework, published by Oasis Security in collaboration with Sequoia Capital and leading CISOs (originally November 2025, updated March 2026), addresses the security governance gap for AI agents operating with autonomous access to enterprise systems ([Oasis AAM Framework](https://www.oasis.security/blog/agentic-access-management-framework), 2026).

#### Five Core Governance Principles

1. **Assign ownership**: Every agent must have a human owner accountable for its actions
2. **Scope least privilege**: Agents receive only the minimum access needed for their task
3. **Prefer federation over static secrets**: Use ephemeral, scoped identities per session rather than long-lived credentials
4. **Monitor actions**: Capture every session -- intent, policy, identity, activity, and expiration
5. **Retire fast**: Decommission agent access immediately when no longer needed

#### Key Capabilities

- **Just-in-time (JIT) session identities**: Ephemeral, scoped credentials per task session with automatic teardown
- **Intent-aware policy**: Deterministic enforcement with inline approvals based on agent intent
- **PAM-style controls**: Privilege elevation that is time-bound, policy-driven, and context-dependent
- **Full session audit**: Every session captures intent, policy decisions, identity, activity, and expiration for compliance

#### Registry Relevance

The AAM Framework's principles translate directly to Agent Registry governance fields:

| AAM Principle | Registry Field / Behavior |
|---|---|
| Assign ownership | `owner` or `provider.organization` on agent record |
| Scope least privilege | Skills and tool access declarations; policy enforcement at deployment |
| Prefer federation | `identity` field (SPIFFE, JWS), `securitySchemes` from AgentCard |
| Monitor actions | Integration with tracing (MLflow Tracing) and audit logging |
| Retire fast | Lifecycle state management: `DEPRECATED` -> `ARCHIVED` / `REMOVED` |

---

## 6. Standards Implications for the Registry

Synthesizing the protocol and standards analysis above, the following design principles emerge for the upstream MLflow Agent Registry RFC.

### 6.1 A2A AgentCard as Canonical Agent Metadata Format

The AgentCard should be adopted as the canonical metadata schema for agent records in the registry. The evidence is strong:

- **Industry adoption**: AWS Agent Registry validates against the A2A schema. kagenti uses AgentCard as the source of truth. Microsoft Agent Framework 1.0 ships native A2A support. Google ADK is the reference implementation. IBM BeeAI supports A2A natively after the ACP merger.
- **AAIF governance**: Both MCP and A2A are governed by the same foundation, ensuring co-evolution.
- **150+ organizations**: No alternative agent metadata format has comparable adoption.

The registry should store the full AgentCard as-is for A2A-native agents, and map non-A2A agents (e.g., OpenAI-compatible endpoints, custom protocols) into AgentCard-compatible records with appropriate extensions.

### 6.2 JWS-Signed Cards for Trust and Verification

The registry should:

- **Store signatures**: Persist JWS signatures alongside agent metadata for audit and re-verification
- **Verify on ingestion**: Validate JWS signatures when agents are registered, rejecting cards with invalid signatures (configurable policy)
- **Track verification status**: Expose `verified: bool` and `identity: string` fields as Varsha's proposal defines
- **Support certificate hierarchies**: Store `jku` (JSON Web Key URL) references for PKI-based trust chains
- **Align with kagenti**: Leverage kagenti's existing JWS verification for Kubernetes-sourced agents rather than re-implementing

### 6.3 Multi-Protocol Support

The registry must not assume all agents speak A2A. The `protocol` enum in Varsha's proposal (`a2a`, `openai-compatible`, `custom`) is the right starting point, but should be extended to support the full `supportedInterfaces` array from A2A, enabling:

- Protocol-based agent queries (e.g., "find all gRPC-capable agents")
- Routing decisions based on available transports
- Version negotiation tracking (which A2A version does each agent support?)

### 6.4 Compatibility with Oracle Agent Spec

For pre-deployment governance, the registry should support:

- Storing Agent Spec configurations (JSON/YAML) as versioned artifacts
- Linking Agent Spec definitions to their deployed AgentCard instances (the "deployment link" described in [01-agent-ecosystem](01-agent-ecosystem.md) Section 3)
- Validating that deployed agents match their registered definitions (drift detection)

### 6.5 Alignment with NIST Evaluation Framework

As NIST develops its evaluation and certification framework, the registry should prepare for:

- **Identity compliance fields**: Recording which identity standard (OAuth, SPIFFE, OIDC) each agent uses
- **Security posture scoring**: Storing security evaluation results aligned with NIST's emerging criteria
- **Sector-specific metadata**: Supporting domain-specific governance fields (e.g., HIPAA compliance status for healthcare agents)
- **Audit trail**: Maintaining a complete history of agent metadata changes, identity verifications, and lifecycle transitions

### 6.6 Standards Coverage Matrix

The following matrix maps each standard to the Agent Registry concerns it addresses:

| Registry Concern | A2A | MCP | Agent Spec | NIST | IEEE P2894 | Oasis AAM |
|---|---|---|---|---|---|---|
| Agent identity & metadata | Primary | -- | Complementary | Evaluation | -- | Ownership |
| Capability discovery | AgentSkill | Tool listing | Declarative defs | -- | Semantic alignment | -- |
| Trust & verification | JWS signatures | -- | -- | Identity standards | -- | JIT identity |
| Protocol bindings | supportedInterfaces | Client/server | Runtime adapters | Interop levels | Cross-org semantics | -- |
| Security governance | securitySchemes | OAuth (draft) | -- | Security baselines | -- | AAM principles |
| Lifecycle management | Task states | -- | -- | Evaluation criteria | -- | Retire fast |
| Composition tracking | skills[] | tools[], resources[] | Agent definitions | -- | -- | Access scoping |
| Multi-tenancy | tenant field | -- | -- | -- | -- | -- |

---

## 7. References

### A2A Protocol

- A2A Protocol Specification: [a2a-protocol.org/latest/specification](https://a2a-protocol.org/latest/specification/)
- A2A Protocol v1.0 Announcement: [a2a-protocol.org/latest/announcing-1.0](https://a2a-protocol.org/latest/announcing-1.0/)
- A2A What's New in v1.0: [a2a-protocol.org/latest/whats-new-v1](https://a2a-protocol.org/latest/whats-new-v1/)
- A2A Task Lifecycle: [a2a-protocol.org/latest/topics/life-of-a-task](https://a2a-protocol.org/latest/topics/life-of-a-task/)
- A2A and MCP: [a2a-protocol.org/latest/topics/a2a-and-mcp](https://a2a-protocol.org/latest/topics/a2a-and-mcp/)
- A2A Agent Discovery: [a2a-protocol.org/latest/topics/agent-discovery](https://a2a-protocol.org/latest/topics/agent-discovery/)
- A2A Custom Protocol Bindings: [a2a-protocol.org/latest/topics/custom-protocol-bindings](https://a2a-protocol.org/latest/topics/custom-protocol-bindings/)
- A2A GitHub Repository: [github.com/a2aproject/A2A](https://github.com/a2aproject/A2A)
- A2A GitHub Releases: [github.com/a2aproject/A2A/releases](https://github.com/a2aproject/A2A/releases)
- AgentCard Concepts: [agent2agent.info/docs/concepts/agentcard](https://agent2agent.info/docs/concepts/agentcard/)
- A2A One-Year Retrospective (Stellagent): [stellagent.ai/insights/a2a-protocol-google-agent-to-agent](https://stellagent.ai/insights/a2a-protocol-google-agent-to-agent)
- Google A2A Codelab: [codelabs.developers.google.com/intro-a2a-purchasing-concierge](https://codelabs.developers.google.com/intro-a2a-purchasing-concierge)
- Google Cloud Blog (A2A Upgrade): [cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade](https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade)
- DeepWiki A2A Task Lifecycle: [deepwiki.com/a2aproject/A2A/2.5-task-lifecycle-and-state-management](https://deepwiki.com/a2aproject/A2A/2.5-task-lifecycle-and-state-management)
- A2A v0.3 Specification: [a2a-protocol.org/v0.3.0/specification](https://a2a-protocol.org/v0.3.0/specification/)

### MCP Protocol

- MCP Specification (2025-11-25): [modelcontextprotocol.io/specification/2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- MCP GitHub: [github.com/modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol)

### MCP vs. A2A Comparisons

- DigitalOcean (A2A vs MCP): [digitalocean.com/community/tutorials/a2a-vs-mcp-ai-agent-protocols](https://www.digitalocean.com/community/tutorials/a2a-vs-mcp-ai-agent-protocols)
- Auth0 (MCP vs A2A): [auth0.com/blog/mcp-vs-a2a](https://auth0.com/blog/mcp-vs-a2a/)
- LlamaIndex (Skills vs MCP Tools): [llamaindex.ai/blog/skills-vs-mcp-tools-for-agents-when-to-use-what](https://www.llamaindex.ai/blog/skills-vs-mcp-tools-for-agents-when-to-use-what)
- Layered.dev (MCP vs Agent Skills): [layered.dev/mcp-vs-agent-skills](https://layered.dev/mcp-vs-agent-skills/)

### Agentic AI Foundation (AAIF)

- AAIF Home: [aaif.io](https://aaif.io/)
- AAIF Members: [aaif.io/members](https://aaif.io/members/)
- AAIF Formation Announcement (Linux Foundation): [linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- AAIF 97 New Members: [linuxfoundation.org/press/agentic-ai-foundation-welcomes-97-new-members](https://www.linuxfoundation.org/press/agentic-ai-foundation-welcomes-97-new-members)
- OpenAI AAIF Blog: [openai.com/index/agentic-ai-foundation](https://openai.com/index/agentic-ai-foundation/)
- Block AAIF Blog: [block.xyz/inside/block-anthropic-and-openai-launch-the-agentic-ai-foundation](https://block.xyz/inside/block-anthropic-and-openai-launch-the-agentic-ai-foundation)
- Anthropic MCP Donation: [anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)

### IBM ACP Merger

- ACP Joins Forces with A2A (LF AI & Data): [lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data](https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/)
- IBM ACP Overview: [ibm.com/think/topics/agent-communication-protocol](https://www.ibm.com/think/topics/agent-communication-protocol)
- IBM ACP Research: [research.ibm.com/projects/agent-communication-protocol](https://research.ibm.com/projects/agent-communication-protocol)

### Oracle Agent Spec

- GitHub Repository: [github.com/oracle/agent-spec](https://github.com/oracle/agent-spec)
- Documentation: [oracle.github.io/agent-spec](https://oracle.github.io/agent-spec/)
- Oracle Blog (Introduction): [blogs.oracle.com/ai-and-datascience/introducing-open-agent-specification](https://blogs.oracle.com/ai-and-datascience/introducing-open-agent-specification)
- Oracle Blog (AG-UI Integration): [blogs.oracle.com/ai-and-datascience/announcing-ag-ui-integration-for-agent-spec](https://blogs.oracle.com/ai-and-datascience/announcing-ag-ui-integration-for-agent-spec)
- PyAgentSpec Docs: [oracle.github.io/agent-spec/development/agentspec](https://oracle.github.io/agent-spec/development/agentspec/index.html)

### NIST AI Agent Standards Initiative

- NIST Announcement: [nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure)
- NIST Initiative Page: [nist.gov/caisi/ai-agent-standards-initiative](https://www.nist.gov/caisi/ai-agent-standards-initiative)
- WorkOS Explainer: [workos.com/blog/nist-ai-agent-standards-initiative-explained](https://workos.com/blog/nist-ai-agent-standards-initiative-explained)
- CSA Research Note: [labs.cloudsecurityalliance.org/research/csa-research-note-nist-ai-agent-standards-20260416-csa-style](https://labs.cloudsecurityalliance.org/research/csa-research-note-nist-ai-agent-standards-20260416-csa-style/)

### IEEE P2894

- Meta Intelligence (NIST + IEEE P2894): [meta-intelligence.tech/en/insight-nist-agent-standards](https://www.meta-intelligence.tech/en/insight-nist-agent-standards)
- IEEE PES MAS Working Group: [site.ieee.org/pes-mas/agent-technology/standards-and-interoperability](https://site.ieee.org/pes-mas/agent-technology/standards-and-interoperability/)

### Oasis Security AAM Framework

- AAM Framework: [oasis.security/blog/agentic-access-management-framework](https://www.oasis.security/blog/agentic-access-management-framework)
- AAM Overview: [oasis.security/agentic-access-management](https://www.oasis.security/agentic-access-management)
- Introducing AAM: [oasis.security/blog/introducing-oasis-agentic-access-management](https://www.oasis.security/blog/introducing-oasis-agentic-access-management)

### Internal References

- Agent Ecosystem & Terminology: [01-agent-ecosystem.md](01-agent-ecosystem.md)
- Varsha's Agent Registry Proposal: [agent-registry-upstream-proposal.md](/features/agent-registry/strategy/upstream-proposal.md)
- Knowledge Registry: [docs/knowledge-registry.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-registry.md)

### RFCs and Standards

- RFC 7515 (JSON Web Signature): [tools.ietf.org/html/rfc7515](https://tools.ietf.org/html/rfc7515)
- RFC 8785 (JSON Canonicalization Scheme): [tools.ietf.org/html/rfc8785](https://tools.ietf.org/html/rfc8785)
- RFC 8628 (OAuth 2.0 Device Authorization Grant): [tools.ietf.org/html/rfc8628](https://tools.ietf.org/html/rfc8628)
