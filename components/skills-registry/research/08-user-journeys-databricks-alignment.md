---
title: User Journeys for Databricks Alignment
description: User-journey synthesis for 2026-08-07 Databricks PM sync -- bridging the enterprise governance gap with anonymized customer evidence, agent-first UX patterns, and concrete recommendations for vision doc and UI mockups.
timestamp: 2026-08-04
lens: requirements
review_after: 2026-11-04
---

# User Journeys for Databricks Alignment

**Purpose**: Prepare for Thursday 2026-08-07 PM sync with Databricks PM Adam and tech lead Yuki by synthesizing user journeys that bridge the governance gap between Red Hat's enterprise customer base and Databricks' current Unity Catalog approach.

**Context**: Matt Prahl's new RFC strategy is to present user-journey-only content FIRST (no technical details) to get alignment before technical RFCs. Databricks needs: (1) a "couple-page" vision doc tied to anonymized customer feedback, (2) UI mockups showing agent-first (not experiment-first) UX shift, (3) clear user journey paths.

**The Disconnect**: Databricks doesn't hear the same governance problems from their customers because Unity Catalog already provides data governance. Red Hat's enterprise customer base is "very conservative and very focused on governance" (Matt Prahl). The vision doc needs to bridge this gap by showing WHY AI asset governance matters for enterprises that don't have Unity Catalog.

---

## Executive Summary

This document synthesizes user journeys for AI skills governance that Red Hat's enterprise customers demand but Databricks' Unity Catalog customers may not experience. It provides:

1. **The enterprise governance gap** -- why skills governance is a first-order concern for regulated industries
2. **Seven core user journeys** -- persona-driven paths showing governance touchpoints
3. **Agent-first UX shift** -- how MLflow should evolve from experiment-centric to agent-centric
4. **Customer evidence themes** -- anonymized patterns from Red Hat's enterprise conversations
5. **Vision doc structure** -- what to bring to Thursday's sync
6. **Mockup recommendations** -- specific UI concepts that demonstrate the shift

---

## 1. The Enterprise Governance Gap

### Why Databricks Doesn't See This Problem

**Databricks customers have Unity Catalog**, which provides:
- Centralized data governance
- Fine-grained access control
- Cross-workspace lineage tracking
- Built-in compliance and audit trails

When Databricks customers build agents, Unity Catalog already governs the data layer. Skills and tools are seen as "just code" -- governed through existing DevOps pipelines.

### Why Red Hat Customers Face a Different Reality

**Red Hat's enterprise customer base** (financial services, healthcare, government, telecommunications) operates under constraints Databricks' customer base may not:

1. **No centralized data platform**: Many customers run fragmented data infrastructure across on-prem and multi-cloud. No Unity Catalog equivalent.

2. **Regulatory compliance burden**: EU AI Act (effective August 2, 2026), financial services regulations (SOX, GDPR, GLBA), healthcare (HIPAA), government (FedRAMP, NIST), telecom (critical infrastructure designation).

3. **Shadow AI sprawl**: Customers report developers building agents using ungoverned skills from public sources (ClawHub, LangChain Hub, random GitHub repos). IT has zero visibility into what's running.

4. **Conservative risk posture**: "Very conservative and very focused on governance" -- customers demand audit trails, approval workflows, and provenance for every AI asset before production deployment.

5. **Supply chain security requirements**: Post-ClawHub crisis (12-20% malicious skills, CVE-2026-25253 RCE vulnerability), enterprises demand scanning, verification, and signing infrastructure for AI assets identical to software packages (npm, PyPI).

### The Market Opportunity

According to [Gartner (May 2026)](https://www.gartner.com/en/newsroom/press-releases/2026-05-26-gartner-says-applying-uniform-governance-across-ai-agents-will-lead-to-enterprise-ai-agent-failure), "applying uniform governance across AI agents will lead to enterprise AI agent failure" -- but **half of enterprise ERP vendors will launch autonomous governance modules** combining explainable AI, automated audit trails, and real-time compliance monitoring.

The competition is already shipping:
- **AWS Agent Registry** (preview April 2026): Cedar-based policy engine, semantic search, three-persona governance model
- **Google Cloud API Registry** (integrated into Vertex AI Agent Builder): centralized tool governance preventing "shadow AI" tool sprawl
- **IBM watsonx.governance AI Asset Discovery**: automatically discovers unmanaged AI agents, tools, MCP servers across environments; uses semantic similarity to link discovered assets to governance workflows
- **JFrog Agent Skills Registry**: scan-verify-sign pipeline with cryptographic provenance

**Red Hat's differentiation**: Open source, on-prem, multi-cloud skills governance for customers who don't have (and won't adopt) a cloud provider's unified platform.

---

## 2. Core User Journeys

These seven journeys show **why governance matters**, not just **what** the technical solution is. Each includes persona, trigger, steps, value delivered, and governance touchpoints.

### Journey 1: Skill Discovery by an Agent Developer

**Persona**: AI Engineer building a customer service agent  
**Context**: Needs a sentiment analysis skill; finds 47 options across GitHub, ClawHub, LangChain Hub  
**Problem**: No way to know which is safe, maintained, compliant, or approved by IT

**User journey**:
1. Developer searches MLflow registry: "sentiment analysis skill"
2. Registry returns results filtered by: **Trust tier** (verified publisher vs. community), **Security scan status** (passed/failed/pending), **Organizational approval** (IT-approved / under review / not approved)
3. Developer sees at-a-glance: "3 IT-approved skills, 12 community skills pending review, 8 failed security scan"
4. Selects IT-approved skill with highest adoption (usage metrics visible)
5. Views skill detail page: description, parameters, dependencies, security scan results, approval workflow history, usage examples
6. One-click install into agent project with version pinning

**Governance touchpoints**:
- Trust tier badges (analogous to [VS Code Marketplace verified publishers](https://code.visualstudio.com/docs/configure/extensions/extension-runtime-security))
- Automated security scanning (analogous to [JFrog's scan-verify-sign pipeline](https://jfrog.com/blog/agent-skills-new-ai-packages/))
- Organizational approval status (analogous to [AWS AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html))

**Value delivered**: Developer gets compliant skill in minutes instead of waiting weeks for IT review of 47 options.

---

### Journey 2: Shadow AI Discovery by IT Security

**Persona**: Security Architect auditing AI asset usage  
**Context**: Compliance audit requires inventory of all AI agents and their capabilities  
**Problem**: Developers deployed 23 agents across 8 teams; IT has zero visibility into what skills they're using

**User journey**:
1. Security architect runs AI asset discovery scan (analogous to [IBM watsonx.governance AI Asset Discovery](https://www.ibm.com/new/announcements/ai-asset-discovery-in-watsonx-governance))
2. Registry auto-discovers 23 agents, 47 skills, 12 MCP servers across dev/staging/prod
3. For each discovered asset, registry uses semantic similarity to match against known records
4. Registry flags: 14 skills not in registry (shadow AI), 6 skills failed security scan but deployed, 3 skills from deprecated publishers
5. Architect views impact report: which agents use flagged skills, which environments, which teams own them
6. One-click workflow: notify teams, create Jira tickets, enforce policy (block further deploys until remediated)

**Governance touchpoints**:
- Automated discovery (prevents "you can't govern what you can't see")
- Risk classification (EU AI Act requires risk tiering; [compliance deadline Dec 2027](https://artificialintelligenceact.eu/))
- Audit trails (every discovery event logged with timestamp, user, action taken)

**Value delivered**: IT gains visibility into shadow AI within hours instead of never. Compliance audit passes.

---

### Journey 3: Skill Publication with Approval Workflow

**Persona**: Data Scientist publishing a new RAG skill  
**Context**: Built a domain-specific RAG skill for customer support; wants to share across organization  
**Problem**: IT requires security scan, architecture review, and VP approval before any AI asset goes to production

**User journey**:
1. Data scientist packages skill using Agent Skills specification (SKILL.md format) -- already emerging as [de facto standard](https://agentskills.io/specification) (adopted by Anthropic, OpenAI, Google, GitHub, VS Code)
2. Uploads to MLflow registry via CLI: `mlflow skills publish ./customer-support-rag --tier=internal`
3. Registry automatically triggers:
   - Code scanning (malware detection, secret scanning, dependency vulnerabilities)
   - Prompt injection detection (tests skill against OWASP LLM Top 10)
   - Metadata validation (required fields, version format, license)
4. Security scan passes → workflow moves to "Pending Architecture Review" state
5. Platform architect reviews skill design, dependencies, resource requirements → approves with note "limit to 4 CPU cores"
6. Workflow moves to "Pending VP Approval" (policy: all internal-tier skills require VP sign-off)
7. VP approves → skill moves to "Approved" state, visible to organization
8. Registry auto-generates audit trail document for compliance team

**Governance touchpoints**:
- Multi-stage approval workflows (analogous to [Salesforce Agentforce governance](https://www.girikon.com/blog/salesforce-agentforce-a-step-by-step-maintenance-guide-in-2026/))
- Policy-driven automation (analogous to [AWS Cedar policy engine](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html))
- Immutable audit logs (EU AI Act Article 12 requires technical documentation and record-keeping)

**Value delivered**: Data scientist publishes once; approval workflow runs automatically; compliance artifact generated; skill available to 500+ developers across organization.

---

### Journey 4: Skill Consumption in an Agent Runtime

**Persona**: Autonomous customer service agent (runtime system)  
**Context**: Agent needs to dynamically discover and load skills at runtime based on conversation context  
**Problem**: Agent has access to 200+ skills; needs to filter by approved-only, match capability to intent, load with correct version

**User journey**:
1. Customer asks: "What's my order status?"
2. Agent runtime sends semantic query to MLflow registry: "retrieve customer order status from CRM"
3. Registry returns skills filtered by:
   - Organizational approval = Approved
   - Security scan status = Passed
   - Capability match (semantic similarity > 0.85)
   - Agent's IAM role has permission to use skill
4. Registry returns 2 matching skills with metadata: name, description, parameters, version, dependencies
5. Agent selects skill based on cost (token usage) and performance (p95 latency from observability data)
6. Agent loads skill version `1.2.3` with lockfile-based dependency resolution (deterministic, reproducible)
7. Skill executes; result returned; **agent execution trace logs skill name, version, parameters, result to MLflow Tracking**

**Governance touchpoints**:
- Dynamic discovery with policy enforcement (only approved skills discoverable)
- IAM-based access control (analogous to [Google Vertex AI agent identity](https://cloud.google.com/blog/products/ai-machine-learning/new-enhanced-tool-governance-in-vertex-ai-agent-builder))
- Full lineage tracking (which agent, which skill version, when, what input/output)

**Value delivered**: Agent operates autonomously within governance guardrails. IT has full audit trail. No human in the loop required for approved skills.

---

### Journey 5: Skill Lifecycle Management Post-Vulnerability

**Persona**: Platform Engineer responding to CVE in a skill dependency  
**Context**: Security scanner flags CVE-2026-XXXXX in a Python library used by 12 skills across 6 production agents  
**Problem**: Need to understand blast radius, notify teams, coordinate patching, verify remediation

**User journey**:
1. Security scanner detects CVE in `requests==2.31.0` (fictional example)
2. Registry shows dependency graph: 12 skills depend on vulnerable library
3. Registry shows impact graph: 6 production agents use those 12 skills
4. Platform engineer views affected teams, agents, environments in a single dashboard
5. Engineer marks vulnerable skills as "Deprecated - Security Vulnerability" with CVE link
6. Registry auto-generates notifications: email to skill owners, Slack alerts to agent teams, Jira tickets for remediation
7. Skill owners publish patched versions; registry re-scans; CVE cleared
8. Engineer reviews adoption metrics: 5 of 6 agents upgraded, 1 still on vulnerable version
9. Engineer escalates final team; manually disables deprecated skill version via policy

**Governance touchpoints**:
- Dependency tracking (analogous to npm/PyPI lockfiles with [vulnerability scanning](https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html))
- Lifecycle state management (Approved → Deprecated → Archived)
- Forced deprecation enforcement (block usage of specific versions via policy)

**Value delivered**: Platform engineer remediates enterprise-wide vulnerability in hours instead of weeks. Full visibility into adoption and compliance.

---

### Journey 6: Skill Provenance Verification for Compliance Audit

**Persona**: Compliance Officer preparing for EU AI Act audit  
**Context**: EU AI Act Article 17 (Dec 2027 deadline) requires documentation of "quality management system" for high-risk AI  
**Problem**: Auditors will ask: "How do you ensure AI skills used in production are from verified sources and haven't been tampered with?"

**User journey**:
1. Compliance officer generates audit report for production agents
2. Report shows: 47 skills used across 23 production agents
3. For each skill, registry provides provenance chain:
   - Publisher identity (verified GitHub org, PGP key)
   - Publication timestamp and original artifact hash
   - Security scan results (date, scanner version, findings)
   - Cryptographic signature (analogous to [JFrog provenance](https://jfrog.com/blog/agent-skills-new-ai-packages/) or [Sigstore](https://www.docker.com/blog/oci-artifacts-for-ai-model-packaging/))
   - Approval workflow history (who approved, when, rationale)
   - All versions ever used in production (immutable audit log)
4. Officer exports report as PDF with embedded signatures
5. Auditor verifies: all skills from verified publishers, all scanned, all approved, no tampering (hash verification)

**Governance touchpoints**:
- Cryptographic signing (analogous to Docker Content Trust, npm provenance)
- Immutable audit logs (append-only, tamper-evident)
- Publisher verification (analogous to [VS Code Marketplace verified publisher badges](https://code.visualstudio.com/docs/configure/extensions/extension-runtime-security))

**Value delivered**: Compliance officer passes audit. Regulator sees documented quality management system meeting EU AI Act requirements.

---

### Journey 7: Multi-Team Skill Reuse with Organizational Scoping

**Persona**: Team Lead for Customer Support AI team  
**Context**: Built 5 high-quality skills for customer service; wants to share with Sales and Product teams but not externally  
**Problem**: Public registries (ClawHub, LangChain Hub) make everything public; need internal sharing with access control

**User journey**:
1. Team lead publishes skill with organizational scope: `@redhat-cx/ticket-classification`
2. Skill is visible only to users within `redhat-cx` organization (IAM integration)
3. Sales team searches registry, finds `@redhat-cx/ticket-classification`, requests access
4. Registry sends approval request to Customer Support team lead
5. Team lead reviews request, approves Sales team's service account
6. Sales team installs skill; registry logs cross-team usage
7. Product team later forks skill, creates `@redhat-product/ticket-classification-v2`
8. Registry tracks lineage: Product skill derived from Customer Support skill

**Governance touchpoints**:
- Organizational scoping (analogous to [npm @org/package scoping](https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html))
- IAM-based access control with approval workflow
- Cross-team usage visibility (who's using what skills, where)

**Value delivered**: Inner-source skill sharing with governance. Teams reuse instead of reinvent. IT has full visibility.

---

## 3. Agent-First UX Shift

### The Current MLflow UX Model (Experiment-Centric)

**Current structure** (based on [MLflow UI patterns research](https://medium.com/aimstack/exploring-mlflow-experiments-with-a-powerful-ui-238fa2acf89e)):
- Left sidebar: flat list of experiments
- Main panel: table of runs within selected experiment
- Primary actions: compare runs, view metrics/parameters, create new experiment
- **Navigation paradigm**: experiment → run → metrics

**Problems at scale**:
- [GitHub issue #16400](https://github.com/mlflow/mlflow/issues/16400): "As the number of experiments grows, it becomes quite hard to navigate through the current UI"
- No hierarchical organization (proposed dot-notation grouping: `team.project.experiment`)
- Filtering by tags not possible
- Not visually appealing for non-technical stakeholders
- [Pagination issues](https://github.com/mlflow/mlflow/issues/8010): UI stops scaling because all experiments fetched on page load

### The Agent-First UX Model

**Proposed structure** (synthesized from [agent-first UX patterns](https://agentic-design.ai/patterns/ui-ux-patterns) and [Google/AWS agent platforms](https://cloud.google.com/products/agent-builder)):

**Primary navigation**: Agents (not Experiments)
- Top-level: Agent catalog (card-based browsing, semantic search)
- Agent detail view: shows capabilities (skills), performance (traces), governance (approval status)
- Secondary: Skills registry (separate top-level section)
- Tertiary: Experiments (for ML model development; still exists but not primary)

**Key UX patterns to adopt**:

1. **Transparency & Decision Visibility** ([Agentic UX pattern](https://hatchworks.com/blog/ai-agents/agent-ux-patterns/))
   - Decision logs, not just action logs
   - Show WHY the agent did something (which skill it chose, why, what alternatives were considered)

2. **Control Surfaces for Autonomous Systems** ([Microsoft Design for Agents](https://microsoft.design/articles/ux-design-for-agents/))
   - Start/stop controls for agents
   - Approval gates at every autonomy level
   - Rollback capabilities
   - Activity logs showing ongoing agent processes

3. **Progressive Delegation** ([Eleken Agentic UX patterns](https://www.eleken.co/blog-posts/agentic-ux-examples))
   - User's approval history sets the pace of autonomy expansion
   - First time agent uses a new skill → requires approval
   - After N successful uses → auto-approve for this agent/user pair

4. **Status & Activity Indicators**
   - Real-time view of: what agents are running, what skills they're using, what resources they're consuming
   - Intervention points where user can redirect without starting over
   - History of decisions made with visible undo

5. **Multi-Agent Coordination Patterns** ([Salesforce Agentic Experience Design](https://www.salesforce.com/blog/ux-shift-to-agentic-experience-design/))
   - Workflows showing agent handoffs
   - Collaborative task execution across agents
   - Transparent orchestration (which agent did what, when, why)

### Why Chat-First UX Fails for Governance

From [Hatchworks Agent UX research](https://hatchworks.com/blog/ai-agents/agent-ux-patterns/):

> "The problem is that the interface was designed for conversation, not delegation and oversight. Hiding agent reasoning and actions behind a chat interface erodes trust when mistakes happen and leaves users unable to intervene effectively."

**What's needed instead**:
- Structured views showing agent state, skill inventory, decision history
- Control panels (not just chat boxes) for managing agent behavior
- Audit trails in tabular/timeline format (not buried in chat logs)

---

## 4. Customer Evidence Themes (Anonymizable)

These patterns emerged from Red Hat customer conversations. Anonymized for Databricks sharing:

### Theme 1: Self-Built Skill Registries

**Pattern**: 3 customers (financial services, telecommunications, government) have built internal skill/tool registries because no product solution exists that meets their governance requirements.

**Customer quote** (paraphrased): "We can't use public skill catalogs. We built our own internal registry with approval workflows because we're a regulated entity. Every AI asset needs to go through the same supply chain security process as software packages."

**Why Unity Catalog doesn't solve this**: These customers don't have Databricks; they run multi-cloud or on-prem infrastructure. Even if they adopted Databricks, Unity Catalog governs data/models, not skills/tools.

### Theme 2: Speed Imperative

**Pattern**: Customers taking on competitors' work streams and building capabilities themselves when product teams can't deliver fast enough.

**Customer quote** (paraphrased): "We need to get to Developer Preview fast, GA when it's ready. We're losing competitive deals to AWS/Google because they have agent governance stories and we don't."

**Implication**: Customer willingness to adopt early/incomplete solutions if it demonstrates commitment to the problem space.

### Theme 3: Generic Skills Are Nearly Impossible

**Pattern** (from [Josh Salomon conversation](https://app.tactiq.io/...)): Customers need highly customized skills for their domain, but starting from zero is expensive. They want a **customization framework** more than a library of generic skills.

**Customer quote** (paraphrased): "We don't need 1,000 generic skills. We need 10 domain-specific skills that we can customize for our business rules, connect to our systems, and deploy with confidence they'll be maintained."

**What this means for governance**: Skills aren't static artifacts -- they evolve. Registry needs to support forking, versioning, lineage tracking as skills get customized.

### Theme 4: Observability Value Tied to Agents, Not Skills

**Pattern** (from Ann Marie Fred, 2026-08-04 sync): "The main thing for traces value is association with the agent, not the skill. Accuracy of skill inventory is hard; knowing what agent did what is high value."

**Implication**: Agent-first UX is validated by customer observability requirements. Customers want to ask: "What did this agent do? What skills did it use? Did it behave as expected?" Not: "Where are all my skills deployed?"

### Theme 5: Governance as Competitive Differentiator

**Pattern**: Red Hat's enterprise customers see governance as a **requirement for adoption**, not a nice-to-have. Lack of governance is a blocker to production deployment.

**Customer quote** (paraphrased): "We can run experiments with ungoverned tools, but we can't deploy to production without audit trails, approval workflows, and provenance. That's not optional for us."

**Why this matters**: Governance is not slowing down adoption -- **lack of governance** is slowing down adoption for this customer segment.

---

## 5. What the Vision Doc Should Contain

For Thursday's Databricks PM sync, the vision doc should cover:

### Section 1: The Problem (One Page)

- **Target customer segment**: Regulated enterprises (financial services, healthcare, government, telecom) with multi-cloud/on-prem infrastructure
- **The pain**: Shadow AI sprawl, no visibility into agent capabilities, compliance requirements (EU AI Act Dec 2027 deadline), supply chain security risks (ClawHub crisis as proof point)
- **Why Unity Catalog doesn't solve it**: UC governs data; skills/tools are ungoverned code artifacts proliferating across teams
- **Customer evidence**: "3 customers built their own registries because no product solution exists" (anonymized)

### Section 2: Core User Journeys (One Page)

Pick 3-4 journeys from Section 2 that resonate most:
- **Skill Discovery by Agent Developer** (easiest to visualize)
- **Shadow AI Discovery by IT Security** (proves value of governance)
- **Skill Lifecycle Management Post-Vulnerability** (shows operational maturity)
- **Skill Provenance Verification for Compliance Audit** (ties to EU AI Act deadline)

Present each as: Persona → Problem → Journey → Value

### Section 3: The Solution (Half Page)

- **Agent-first MLflow**: Extend MLflow with agent/skill registry as first-class entities (not just experiments/models)
- **Open standards**: Built on Agent Skills spec (SKILL.md), MCP Registry spec, OCI artifacts
- **Differentiation**: Open source, on-prem/multi-cloud, integrated observability (MLflow Tracking for agent traces)
- **What we're NOT proposing**: Replacing Unity Catalog, competing with Databricks downstream, or forcing a specific implementation

### Section 4: What We Need from Databricks (Quarter Page)

- **Alignment on user journeys**: Do these resonate with Databricks' roadmap for MLflow GenAI adoption?
- **RFC path forward**: User-journey RFC first, then technical implementation RFC
- **Databricks perspective**: Does Databricks see value in aligning MLflow upstream with Unity Catalog agent/skill capabilities? (Adel's question)

**Total length**: 2.5 pages. Fits "couple-page" request. Heavy on visuals (journey diagrams).

---

## 6. What the Mockups Should Show

### Mockup 1: Agent-First Home Screen

**Replaces**: Flat experiment list  
**Shows**: 
- Top section: "My Agents" (card-based layout, 6 agents visible)
- Each agent card shows: name, status (running/stopped), capabilities count (e.g., "8 skills"), last activity timestamp, health indicator (green/yellow/red based on traces)
- Quick actions: Start, Stop, View Traces, Edit
- Right sidebar: "Recommended Skills" based on agent's current capabilities
- Search bar: semantic search across agents and skills (not just text match)

**UX pattern**: Analogous to [Google Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder) home screen

---

### Mockup 2: Skills Registry with Governance Filters

**Replaces**: N/A (new section)  
**Shows**:
- Left sidebar: filters for Trust Tier (Verified / Community), Approval Status (Approved / Pending / Rejected), Security Scan (Passed / Failed / Pending), Category (RAG / Code Execution / Web Search / ...)
- Main panel: skills grid (card-based)
- Each skill card shows: name, publisher, trust badge, security scan badge, approval status badge, usage count, last updated
- Top bar: semantic search "Find skills that can..." with autocomplete
- Sort options: Most Used, Recently Updated, Highest Rated, IT Recommended

**UX pattern**: Analogous to [VS Code Marketplace](https://code.visualstudio.com/docs/configure/extensions/extension-runtime-security) with governance overlays

---

### Mockup 3: Skill Detail Page with Approval Workflow

**Replaces**: N/A (new section)  
**Shows**:
- Header: skill name, version selector (dropdown), publisher info, trust badge
- Tabs: Overview, Security, Lineage, Usage, Versions
- **Overview tab**: description, parameters, dependencies, installation command, usage examples
- **Security tab**: scan results (passed/failed tests), CVE history, signature verification status, last scan date
- **Lineage tab**: graph showing skill dependencies (other skills, MCP servers, models it calls)
- **Usage tab**: which agents use this skill (table), adoption trend over time (line chart), p95 latency from traces
- **Versions tab**: all published versions with changelog, deprecation notices, adoption metrics per version
- Bottom section: "Approval Workflow" timeline showing: Submitted → Security Scan Passed → Architecture Review (approved by Jane Doe, 2026-08-01) → VP Approval (approved by John Smith, 2026-08-02) → Deployed

**UX pattern**: Combines [GitHub package page](https://github.com/) detail + [Salesforce approval workflow visualization](https://www.girikon.com/blog/salesforce-agentforce-a-step-by-step-maintenance-guide-in-2026/)

---

### Mockup 4: Agent Trace View with Skill Attribution

**Replaces**: Current MLflow Tracking run view  
**Shows**:
- Timeline view of agent execution (vertical timeline on left)
- Each timeline entry shows: timestamp, event type (User Query / Skill Invocation / Agent Response), duration
- Expandable timeline entries:
  - User Query: shows full prompt
  - Skill Invocation: shows skill name, version, parameters passed, result returned, latency, token cost
  - Agent Response: shows final output
- Right sidebar: "Skills Used in This Trace" (list of skills with usage count)
- Bottom panel: "Decision Log" showing why agent chose each skill (analogous to [decision visibility pattern](https://hatchworks.com/blog/ai-agents/agent-ux-patterns/))
- Filter controls: show only failed invocations, show only skills above cost threshold, show only unapproved skills (governance filter)

**UX pattern**: Analogous to [Databricks Agent Tracing UI](https://www.databricks.com/product/managed-mlflow) but with skill-level attribution and governance overlays

---

### Mockup 5: Shadow AI Discovery Dashboard

**Replaces**: N/A (new capability)  
**Shows**:
- Top KPI cards: "47 Skills Discovered", "14 Ungoverned (30%)", "6 Failed Security Scan", "3 From Deprecated Publishers"
- Main panel: table of discovered skills with columns: Skill Name, Source (GitHub / ClawHub / Unknown), Used By (agent names), Environment (dev/staging/prod), Security Status, Approval Status
- Row actions: "Approve & Import", "Flag for Review", "Block Deployment"
- Right sidebar: "Impact Analysis" for selected skill showing: 3 agents use this skill, 12 production executions last 7 days, 2 teams own those agents
- Bulk actions: Select all ungoverned → Notify teams, Select all failed scans → Block deployment

**UX pattern**: Analogous to [IBM watsonx.governance AI Asset Discovery](https://www.ibm.com/new/announcements/ai-asset-discovery-in-watsonx-governance)

---

## 7. Sources

### Enterprise AI Governance Requirements
- [Gartner: Applying Uniform Governance Across AI Agents Will Lead to Failure](https://www.gartner.com/en/newsroom/press-releases/2026-05-26-gartner-says-applying-uniform-governance-across-ai-agents-will-lead-to-enterprise-ai-agent-failure) (May 2026)
- [AI Agents in Enterprise: Market Survey of McKinsey, PwC, Deloitte, Gartner](https://www.klover.ai/ai-agents-in-enterprise-market-survey-mckinsey-pwc-deloitte-gartner/)
- [Witness AI: EU AI Act Compliance Checklist 2026](https://witness.ai/blog/eu-ai-act-compliance-checklist-2026/)
- [Sentra: EU AI Act Compliance for Enterprise AI Deployers](https://sentra.io/learn/eu-ai-act-compliance-what-enterprise-ai-deployers-need-to-know)

### MLflow UX Patterns
- [GitHub Issue #16400: Hierarchical Organization of Experiments in MLflow UI](https://github.com/mlflow/mlflow/issues/16400)
- [Exploring MLflow Experiments with a Powerful UI](https://medium.com/aimstack/exploring-mlflow-experiments-with-a-powerful-ui-238fa2acf89e)
- [GitHub Issue #8010: Experiment Pagination in UI](https://github.com/mlflow/mlflow/issues/8010)

### Competitor Agent/Skill Governance
- [Google: Enhanced Tool Governance in Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/new-enhanced-tool-governance-in-vertex-ai-agent-builder)
- [Google Vertex AI Agent Builder Documentation](https://cloud.google.com/products/agent-builder)
- [AWS Agent Registry Preview Announcement](https://aws.amazon.com/about-aws/whats-new/2026/04/aws-agent-registry-in-agentcore-preview/)
- [AWS AgentCore Policy Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [IBM watsonx.governance AI Asset Discovery](https://www.ibm.com/new/announcements/ai-asset-discovery-in-watsonx-governance)
- [JFrog Agent Skills Registry Blog](https://jfrog.com/blog/agent-skills-new-ai-packages/)

### Agent-First UX Patterns
- [Agentic Design: UI/UX & Human-AI Interaction Patterns](https://agentic-design.ai/patterns/ui-ux-patterns)
- [Salesforce: UX Paradigm Shift to Agentic Experience Design](https://www.salesforce.com/blog/ux-shift-to-agentic-experience-design/)
- [Hatchworks: Agent UX Patterns - Chat-First UX Fails](https://hatchworks.com/blog/ai-agents/agent-ux-patterns/)
- [Microsoft Design: UX Design for Agents](https://microsoft.design/articles/ux-design-for-agents/)
- [Eleken: 6 Agentic UX Design Patterns with Real-World Examples](https://www.eleken.co/blog-posts/agentic-ux-examples)

### Databricks & Unity Catalog
- [Databricks: Manage Model Lifecycle in Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/)
- [MLflow on Databricks](https://docs.databricks.com/aws/en/mlflow/)
- [Databricks: Agent Tracing & AI Observability Tools](https://www.databricks.com/product/managed-mlflow)

### Emerging Standards
- [Agent Skills Specification (SKILL.md)](https://agentskills.io/specification)
- [VS Code: Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Docker: OCI Artifacts for AI Model Packaging](https://www.docker.com/blog/oci-artifacts-for-ai-model-packaging/)

### Supply Chain Security
- [OWASP: NPM Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html)
- [VS Code: Extension Runtime Security](https://code.visualstudio.com/docs/configure/extensions/extension-runtime-security)

---

## Next Steps

1. **Monday 2026-08-05**: Draft 2.5-page vision doc based on Section 5 structure
2. **Tuesday 2026-08-06**: Create mockups (wireframes acceptable; high-fidelity if time permits) based on Section 6
3. **Wednesday 2026-08-07 AM**: Review with Matt Prahl and Humair Khan
4. **Thursday 2026-08-07 PM**: Databricks PM sync with Adam and Yuki

**Goal for Thursday**: Secure alignment on user journeys. If successful, proceed to technical RFC. If not, understand Databricks' customer base differences and adjust positioning.
