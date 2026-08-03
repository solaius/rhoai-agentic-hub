---
title: "Agent Registry research — requirements refresh (2026-08)"
description: Requirements refresh driven by Adel's product scoping doc (P1-P11 customer validation) and Jiri Danek's three design questions (versioning, dependency permanence, visibility scoping) — independent industry validation of problem tiers, external evidence on the three open questions, and eight gap requirements not in P1-P11.
timestamp: 2026-08-03
lens: requirements
review_after: 2026-11-03
---

Requirements-lens refresh for the [Agent Registry](/components/agent-registry/index.md),
triggered by two new inputs: Adel Zaalouk's product scoping doc
([ref](/components/agent-registry/knowledge/ref-agent-registry-scoping-gdoc.md),
2026-08-03) defining 11 customer-validated problems, and three open design
questions from Jiri Daněk's review. Continues the series from
[10-requirements](/components/agent-registry/research/10-requirements.md)
(2026-07-16), which remains the comprehensive regulatory/fleet/persona/governance
baseline — this refresh targets the gaps, not a redo.

## 1. Independent validation of P1-P11 customer problems

The P1-P11 problem taxonomy is strongly validated by 2026 industry surveys,
with remarkably consistent priority ordering.

### 1.1 P2 ("no visibility of what's running") confirmed as #1

Gartner's "Six Steps to Manage AI Agent Sprawl" (Apr 2026) names "Build
Centralized Agent Inventory" as Step 2 of its foundational playbook —
directly confirming that inventory/visibility is the foundational
enterprise requirement. Gravitee's State of AI Agent Security 2026
reports only 18% of organizations maintain a current complete inventory
of AI agents. The 82% shadow-agent discovery stat (already in doc 10
from HFS/Zenity) is independently confirmed by Gravitee.

Evidence grade: **strong** (Gartner, Gravitee, CSA — three independent
sources, consistent finding).

### 1.2 P4 (shadow IT) may be UNDERWEIGHTED at Tier 1

Forrester named AI agent threats the #1 CISO risk for 2026 — personal
agents operate as "shadow operators" outside IAM controls. AvePoint's
State of AI 2026 reports 88.4% had an AI agent-related security breach
and 89.5% had a GenAI security breach in 2025. CSA identifies a
perception-reality gap: 68% of orgs *claim* high visibility yet 82%
discover unknown agents when they actually look.

The scoping doc places P4 in Tier 1 alongside P1-P3-P5-P6. The external
evidence suggests shadow-agent governance may deserve even higher
framing — it is the attack vector, not just an inventory problem.

Evidence grade: **strong** (Forrester, AvePoint, CSA — three independent
sources; Forrester's #1 CISO risk is a notable elevation).

### 1.3 P7-P9 (FSI production blockers) confirmed by regulatory developments

The financial-services problems (CVE blast radius, accountability, policy
visibility) align with regulatory developments that postdate the July
requirements doc:

- Treasury's Financial Services AI Risk Management Framework (FS AI RMF,
  Feb 2026) contains 230 control objectives spanning model governance,
  agent lifecycle, and accountability chains.
- The April 2026 interagency guidance (doc 10 already noted this —
  SR 11-7 rescinded, agentic AI excluded from MRM scope) is now
  supplemented by emerging replacement frameworks: SR 26-2 and the
  forthcoming RFI on agentic AI model risk.
- NYDFS Part 500 makes AI governance a board-level accountability issue.
- Colorado AI Act effective June 30, 2026 adds state-level obligations.

Evidence grade: **strong** for the regulatory framing; **moderate** for
how fast banks adopt agentic-specific controls (the MRM habit is
established, the mandate is pending).

### 1.4 P11 (token costs) is NOT FSI-specific

The scoping doc classifies P11 as a Tier 2 FSI blocker, but industry
evidence shows per-agent cost visibility is a universal enterprise
concern:

- EY reports agentic interactions cost 30x more than chatbot interactions
  ($1.20 vs $0.04 per interaction).
- Goldman Sachs projects 24x token consumption growth by 2030.
- Uber reportedly consumed its full-year AI budget in 4 months after
  agentic adoption.
- 98% of FinOps practices now manage AI spend (State of FinOps 2026,
  via doc 10 source 13).

The registry is not a metering system, but its metadata (stable agent
identity, owner, cost-center tags) is the join key that observability
and FinOps tooling needs to attribute costs per agent. This was already
noted in doc 10 §2 — the refresh confirms it is a universal
requirement, not FSI-specific.

Evidence grade: **strong** (EY, Goldman, Gartner, FinOps survey —
multiple independent sources across sectors).

### 1.5 Problems MISSING from P1-P11

Industry evidence surfaces requirements that the P1-P11 list does not
cover:

| Missing requirement | Evidence | Grade |
|---|---|---|
| **Agent NHI (Non-Human Identity) lifecycle** | 76% do not fully govern non-human identities (Gravitee); agents still logging in as humans (Help Net Security, Jul 2026). Distinct from P8 (human accountability) — this is the agent's own credential lifecycle, rotation, and retirement. | Strong |
| **Inter-agent boundary/handoff testing** | Majority of multi-agent failures originate at agent boundaries — handoff points between agents (VentureBeat, Jun 2026). No P1-P11 item addresses interface contracts between agents. | Moderate |
| **Evaluation status as registry metadata** | 50% deployed agents that passed internal evals but failed in production (VentureBeat Pulse, Jun 2026). Only 5% fully trust automated evaluations. | Moderate |
| **Context/grounding declaration** | 57% of enterprises traced wrong answers to missing business context (VentureBeat Pulse). The registry should capture which data sources and knowledge bases an agent is connected to. | Moderate |
| **Behavioral drift detection** | Stateful agents drift from accumulated memory, not code changes. Versioning must include behavioral baselines and periodic drift checks. | Weak (emerging) |

The first three are strong enough to consider as additions to the
requirements schema. NHI lifecycle is the most urgent — it connects to
the interop domain's SPIFFE/SPIRE identity work and has direct
regulatory implications (NIST agent inventory guidance explicitly calls
for "permissions they hold" and "who authorized their deployment").

## 2. Agent versioning for non-deterministic systems

Jiri's question: how to version agents when LLM behavior is sensitive to
prompt changes? The industry has converged on a "four-layer versioning"
model and eval-gated promotion, but has NOT solved SemVer for AI agents.

### 2.1 Four layers, not one

CIO.com's "Why Versioning AI Agents Is the CIO's Next Big Challenge"
(2026) identifies four interdependent layers that each require
independent version tracking: **code**, **prompt template(s)**, **model
version**, and **tool/API contracts**. Changing any single layer shifts
behavior. Traditional SemVer is insufficient because the relationship
between input change magnitude and output change magnitude is
non-linear and non-deterministic.

MLflow 3.x has implemented this with two primitives:
- **LoggedModel** — captures complete application state (code refs,
  configurations, dependencies, evaluation data) in one versioned entity.
  Designed for compliance and incident-response traceability.
- **Prompt Registry** — immutable prompt versions with aliases
  ("production"/"staging"), commit messages, timestamps, and evaluation
  scores per version. Git-inspired design.

Evidence grade: **strong** (CIO.com, MLflow docs, Anthropic engineering
blog — three independent sources, consistent model).

### 2.2 Eval-gated promotion replaces version numbering

The emerging practice is **eval-gated promotion**: versions are not
promoted based on code review alone but must pass behavioral evaluation
suites against golden datasets. This replaces the question "is this a
major or minor version bump?" with "did this change pass the promotion
gate?"

- Anthropic's agent evaluation methodology: start with fast iteration,
  add narrow evals (concision, file edits), then complex evals
  (over-engineering detection); value compounds over the lifecycle.
- Confident AI documents release gates that run changed prompts against
  benchmark datasets before promotion, with calibrated thresholds to
  approve/hold/reject.
- BuildMVPFast describes a 5-stage production pipeline: pre-merge
  behavioral regression → staging deploy → shadow mode (24h) → canary
  (5%→25%) → full rollout with 48h monitoring.

Evidence grade: **moderate** (vendor guidance + practitioner blogs;
no industry standard yet).

### 2.3 Registry implications

- The metadata schema must capture independent version identifiers for
  code, prompt template(s), model, and tool contracts — not just
  "agent version 1.2.3." MLflow's LoggedModel pattern is the reference.
- Eval-gated promotion should be a registry-enforced workflow with
  promotion aliases (draft/staging/production) and evaluation score
  requirements before promotion.
- In regulated contexts (FSI, EU AI Act), any prompt change that alters
  decision-making behavior must be treated as a version change with full
  audit trail.
- SemVer does NOT map cleanly to non-deterministic systems. The industry
  has accepted this and works around it with eval scores and behavioral
  baselines. No settled answer exists to Jiri's core question — the
  registry should version at four layers and gate on evals, not try to
  define what constitutes a "patch" vs. "minor" vs. "major" for a prompt
  change.

### 2.4 Status update for question-agent-versioning-nondeterministic

Evidence added. The answer is "don't try to SemVer prompts — version at
four layers and gate promotions on eval scores." Adel's response
("prompts might be too ephemeral, it could be models, MCP servers... we
have a prompt registry") aligns with the four-layer model. Status
remains **open** — the specific RHOAI implementation design is needed.

## 3. Dependency permanence for live agent registries

Jiri's question: the npm/left-pad problem for live services — how to
prevent cascading breaks when skill/MCP server owners deprecate
dependencies that running agents rely on.

### 3.1 No existing registry solves this

The critical finding: **no existing agent registry (AWS, Google,
Databricks, Solo.io) documents enforcement of dependency immutability
between agents.** Every vendor handles internal versioning — versioned
records, deprecation lifecycle, approval workflows — but none prevents
cascading breaks from dependency deprecation. The gap is at the
inter-entity level: "Agent X depends on Skill v1.2.3; the skill owner
deprecates v1.2.3; Agent X breaks in production."

Evidence grade: **moderate** (absence of evidence from vendor docs;
confirmed by reviewing AWS, Google, Databricks, and Solo.io registry
documentation — none documents this enforcement).

### 3.2 The OCI digest-pinning model applies

The best available pattern comes from container registries: OCI
registries enforce immutability via content-addressable storage where
each artifact has a SHA256 digest. Tags may be mutable, but digests are
forever. Production workloads pin to digests, not tags.

Sakura Sky's agent lifecycle management framework (2026) explicitly
proposes immutable agent artifacts with byte-level hashes for
auditability — a "deprecation layer" that includes version pinning,
migration tracking, and sunset verification. Auditors inspect the
registry, not code repos.

DevSecOps School's dependency-pinning architecture: lockfile → CI
resolves → build image → tag with digest → GitOps manifests reference
digest → OPA gate verifies. This translates to: agent registration →
dependency manifest pins exact skill/MCP digests → deprecation of
a pinned dependency blocked while the agent is ACTIVE → migration
pathway offered.

Evidence grade: **strong** for the pattern (OCI, DevSecOps norms);
**moderate** for its application to agent registries (Sakura Sky is
the best agent-specific source, but it is a single practitioner blog).

### 3.3 MLflow's alias model is a partial answer

MLflow 3.15.0's MCP Registry adds semantic-versioned configs with
promotable aliases for MCP servers. The pattern: a skill owner can
promote new versions without breaking existing consumers who pin to
exact version numbers. But alias governance (who can move the
"production" alias?) needs policy enforcement that doesn't exist yet.

Evidence grade: **moderate** (MLflow docs — first-party but new).

### 3.4 Registry implications

- **Dependency manifests** (analogous to lockfiles) should pin exact
  version hashes, not mutable aliases. An agent's registration record
  should declare its skill and MCP server dependencies at exact versions.
- **Deprecation must be negotiated, not unilateral**: when a skill owner
  wants to deprecate v1.2.3, the registry should identify all ACTIVE
  agents pinned to that version and either block deprecation or force a
  migration acknowledgment. This is the key differentiator — no
  competitor has it.
- **Immutable artifacts are table stakes for FSI**: the Sakura Sky
  lifecycle model (build layer produces immutable artifact, deprecation
  layer tracks migration) aligns with FSI audit expectations.

### 3.5 Status update for question-agent-dependency-permanence

Evidence added. The answer is "adopt OCI digest-pinning semantics +
negotiated deprecation." Status remains **open** — the specific
enforcement mechanism (block deprecation? force migration window?
snapshot dependencies?) needs design work.

## 4. Visibility scoping in multi-tenant agent registries

Jiri's question: should the registry enforce visibility scopes
(team-local/org-wide/public) to prevent accidental coupling from global
discovery?

### 4.1 Three architectural patterns exist

The industry shows three distinct approaches, each with a reference
implementation:

1. **Build-time visibility rules (Bazel model)**: explicit visibility
   specifiers (public/private/package-level/subpackage-level), default
   is private, package_group for shared visibility. Deprecation
   restricts to current consumers.
2. **Runtime namespace/RBAC scoping (Kubernetes model)**: tenant
   isolation via namespaces, policy-enforced at the API layer.
   TrueFoundry's MCP Registry architecture demonstrates the "no global
   list-all path" principle — queries are always tenant-scoped at the
   data-access layer.
3. **Discovery-tier model (Backstage)**: APIs are public (available to
   any component), restricted (allowed consumers only), or private
   (within their system). First-class visibility scoping for service
   discovery.

Evidence grade: **strong** (Bazel docs, Backstage docs, TrueFoundry
architecture — three independent, well-documented systems).

### 4.2 Vendor registry approaches

- **Microsoft Agent 365** (Jun 2026): centralized registry with per-agent
  device-level detection, Entra ID Governance for agent entitlements,
  shadow agent detection across managed endpoints. Visibility is
  identity-scoped (Entra ID).
- **Databricks Unity AI Gateway** (Jun 2026): four-level namespace
  (metastore.catalog.schema.table), identity-aware on-behalf-of token
  passing. Cost slicing by endpoint tags, request tags, identity,
  model/provider.
- **Google Cloud**: dynamically maintained registry for tenant
  identification, Permissions and Access Boundaries (PAB) Policy limits
  agent resource access, Model Armor for PII masking.

All three use identity-based scoping (who you are determines what you
see), not explicit visibility labels (the Bazel approach). The RHOAI
registry likely needs both: visibility metadata in the agent record
AND runtime RBAC enforcement in the registry API.

Evidence grade: **strong** (primary vendor documentation).

### 4.3 The Bazel deprecation-visibility pattern

Particularly relevant to Jiri's concern: Bazel's deprecation-visibility
interaction. When deprecating a target, Bazel restricts its visibility
to current consumers to prevent new dependencies — existing users can
still build, but new dependents cannot add a dependency on the
deprecated target. This maps 1:1 to the agent registry: when deprecating
an agent or skill, restrict discoverability to current consumers to
prevent new accidental coupling.

### 4.4 Registry implications

- **Three-tier visibility (public/restricted/private) as agent record
  metadata**: the Backstage model maps cleanly. Default should be
  "restricted" (discoverable within the owning workspace/namespace),
  with explicit opt-in to "public" (org-wide discoverable).
- **Tenant-scoped queries must be the architectural default**: the
  TrueFoundry "no list-all path" principle should be enforced at the
  data-access layer, not just the API layer. An unscoped discovery
  query should be impossible.
- **Deprecation restricts visibility to current consumers**: the Bazel
  pattern applied — once deprecated, new dependencies cannot form, but
  existing consumers see the agent until they migrate.

### 4.5 Status update for question-agent-visibility-scoping

Evidence added. The answer is "yes — three-tier visibility
(public/restricted/private) as metadata, with RBAC enforcement and
Bazel-style deprecation-visibility interaction." Status remains
**open** — the default visibility level and its relationship to
Kubernetes namespace RBAC needs design work.

## Sources

1. [Gartner — Six Steps to Manage AI Agent Sprawl (Apr 2026)](https://www.gartner.com/en/newsroom/press-releases/2026-04-28-gartner-identifies-six-steps-to-manage-artificial-intelligence-agent-sprawl)
2. [Gravitee — State of AI Agent Security 2026](https://www.gravitee.io/state-of-ai-agent-security)
3. [Forrester — AI agent threats named #1 CISO risk 2026](https://www.cybersecurity-insiders.com/forrester-2026-ai-agent-threats-ciso-risk/)
4. [CSA — Shadow AI Agent Problem (Apr 2026)](https://cloudsecurityalliance.org/blog/2026/04/28/the-shadow-ai-agent-problem-in-enterprise-environments)
5. [EY — Agentic AI Token Costs (2026)](https://www.ey.com/en_us/insights/ai/agentic-ai-token-costs)
6. [AvePoint — State of AI 2026](https://www.avepoint.com/shifthappens/reports/artificial-intelligence-report-2026)
7. [VentureBeat — Enterprise evaluation gap (Jun 2026)](https://venturebeat.com/orchestration/enterprise-ai-is-entering-an-evaluation-gap-agents-are-gaining-autonomy-faster-than-companies-can-verify-them)
8. [CIO.com — Why Versioning AI Agents Is the CIO's Next Big Challenge](https://www.cio.com/article/4056453/why-versioning-ai-agents-is-the-cios-next-big-challenge.html)
9. [MLflow — Version Tracking for Agents](https://mlflow.org/docs/latest/genai/version-tracking/)
10. [MLflow — Prompt Registry](https://mlflow.org/docs/latest/genai/prompt-registry/)
11. [Anthropic — Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
12. [BuildMVPFast — Agent Versioning and Rollback (Apr 2026)](https://www.buildmvpfast.com/blog/agent-versioning-rollback-production-ai-update-zero-downtime-2026)
13. [Confident AI — CI/CD for AI Agents (2026)](https://www.confident-ai.com/knowledge-base/compare/best-ci-cd-tools-testing-ai-agents-before-production-2026)
14. [Sakura Sky — Agent Lifecycle Management (2026)](https://www.sakurasky.com/blog/missing-primitives-for-trustworthy-ai-part-11/)
15. [DevSecOps School — Dependency Pinning Guide (2026)](https://devsecopsschool.com/blog/dependency-pinning/)
16. [Container-Registry.com — Tag Immutability](https://container-registry.com/docs/user-manual/images/tags/tag-immutability/)
17. [Backstage — System Model (API visibility)](https://backstage.io/docs/features/software-catalog/system-model/)
18. [TrueFoundry — Centralized MCP Registry Architecture](https://www.truefoundry.com/blog/centralized-mcp-registry-architecture)
19. [Microsoft Agent 365 — What's New June 2026](https://techcommunity.microsoft.com/blog/agent-365-blog/whats-new-in-agent-365-%E2%80%93-june-2026/4535107)
20. [Databricks — Unity AI Gateway (DAIS 2026)](https://www.databricks.com/blog/ai-governance-data-ai-summit-2026-whats-new-unity-ai-gateway)
21. [Bazel — Visibility Rules](https://bazel.build/concepts/visibility)
22. [CreateOS — AI Agent Versioning (Jun 2026)](https://createos.sh/blogs/ai-agent-versioning)
