---
title: "Skills Catalog research -- competitive refresh: skills lifecycle models"
description: "No competitor manages the full skill lifecycle end-to-end; NVIDIA leads on verification depth, Google on state-machine clarity, and the market lacks a unified intake-to-deprecation model -- the gap RHOAI can own with Konflux + OCI + MLflow + Kubeflow Hub"
timestamp: 2026-08-06
lens: competitive
review_after: 2026-11-06
supersedes_context: "Deepens competitive coverage from 05 with lifecycle-focused analysis across all major vendors"
---

# Skills lifecycle models: competitive analysis

This document examines how each major competitor handles the skills lifecycle --
from intake through verification, versioning, deprecation, and partner
onboarding. Where doc 05 mapped features and positioning, this refresh maps
the **operational lifecycle** that determines whether skills are trustworthy,
maintainable, and governable at enterprise scale.

The analysis covers ten platforms across six lifecycle dimensions, culminating
in a comparison matrix and key findings for RHOAI differentiation.


## 1. NVIDIA Verified Skills

NVIDIA operates the most mature trust pipeline in the market, with an 8-stage
verification process and the industry's deepest scanning technology.

### 1.1 Intake/onboarding

Skills originate in **source repositories owned by NVIDIA product teams**,
not through a public submission portal. Third-party contributions flow through
the NeMo Agent Toolkit plugin lifecycle: partners apply via GitHub issue or
PR, build against an NVIDIA template with toolkit liaison support, and undergo
layout/license/naming/smoke-test validation before indexing.
([docs.nvidia.com/nemo/agent-toolkit](https://docs.nvidia.com/nemo/agent-toolkit/latest/extend/third-party-plugins.html))

Format: SKILL.md (agentskills.io open spec) with optional scripts/,
references/, assets/ directories. Same format works across Claude Code, Codex,
Cursor, and other agents.

### 1.2 Verification/validation

Every verified skill passes an **8-stage sequential pipeline**:

1. Source repository (product team repo)
2. Human and automated review (policy checks, compliance)
3. **SkillSpector security scanning** -- 68 vulnerability patterns across 17
   categories including prompt injection (5 patterns), data exfiltration (4),
   supply chain (6), tool misuse (3), MCP least-privilege (4), and MCP tool
   poisoning (4). Uses two-stage analysis: fast static checks (regex, AST,
   taint tracking, YARA, live CVE lookup) plus optional LLM semantic analysis
   achieving 87% precision.
4. Evaluation (future: trigger accuracy, task completion rate, token efficiency)
5. Skill card generation (machine-readable YAML/JSON trust metadata)
6. Cryptographic signing (detached `skill.oms.sig` using OpenSSF Model Signing)
7. Cataloging (indexed in NVIDIA/skills GitHub repository)
8. Daily synchronization from source repositories

([developer.nvidia.com/blog/nvidia-verified-agent-skills](https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/);
[docs.nvidia.com/skills/scanning-agent-skills](https://docs.nvidia.com/skills/scanning-agent-skills);
[github.com/nvidia/skillspector](https://github.com/nvidia/skillspector))

### 1.3 Versioning

SemVer convention aligned with agentskills.io. The entire skill directory
(SKILL.md, scripts, assets) is signed as a unit with a detached OMS signature.
Version updates propagate via daily sync from source repositories. Skill cards
document version history.

### 1.4 Deprecation/removal

**Not formally documented.** The NeMo plugin lifecycle supports deprecation
via archival notification, but there are no explicit lifecycle states beyond
Draft and Published. Governance relies on Git repository maintenance and
partner communication rather than formal state transitions. This is a
notable gap for the market's most mature trust pipeline.

### 1.5 Partner/ISV onboarding

NVIDIA Partner Network (NPN) provides broader ecosystem access. The NeMo
Agent Toolkit uses a 7-step plugin lifecycle (apply, develop, submit, list,
verify, maintain, deprecate/archive). Future distribution planned via Hermes
Skillhub and Clawhub partner channels (not yet live). No separate ISV
certification program for skills specifically.
([nvidia.com/en-us/about-nvidia/partners](https://www.nvidia.com/en-us/about-nvidia/partners/))

### 1.6 Lifecycle states

Draft (working copy, editable) --> Published (frozen snapshot, immutable,
signed). No formal Deprecated or Archived states. Subsequent edits create a
new Draft --> Published cycle.


## 2. JFrog Agent Skills Registry

JFrog positions itself as the **trust layer and control plane** for agent
skills, applying its proven artifact lifecycle management to the skills domain.

### 2.1 Intake/onboarding

Skills stored as Artifactory artifacts in Skills Repositories. Upload via
JFrog CLI (`jf agent skills publish`). Version is read from SKILL.md
frontmatter; CLI auto-increments to next minor SemVer if absent (defaults to
0.1.0). NVIDIA integration validated using cuOpt as first packaged skill.
([jfrog.com/ai-catalog/skills-registry](https://jfrog.com/ai-catalog/skills-registry/);
[docs.jfrog.com/artifactory/docs/jf-skills](https://docs.jfrog.com/artifactory/docs/jf-skills))

### 2.2 Verification/validation

JFrog AI Catalog automatic processing: Xray scans for malicious intent,
vulnerabilities, and compliance risks. Detects data exfiltration, arbitrary
code execution, and indirect prompt injection. Cryptographic signing for
integrity verification. Project-scoped permissions with approval workflows
before agents access skills.
([jfrog.com/blog/agent-skills-new-ai-packages](https://jfrog.com/blog/agent-skills-new-ai-packages/))

### 2.3 Versioning

SemVer via SKILL.md version field. Auto-increment on upload. Update mechanism:
`jf agent skills update` targets skill name + harness. On update failure,
previous install restored from temporary backup (`.skill-backup/`). Rollback
is automatic on failure.

### 2.4 Deprecation/removal

No skill-specific deprecation workflow. Relies on artifact-level Cleanup
Policies (custom rules for removing stale binaries) and Smart Archiving
(transfer to Archive instance for regulatory compliance). Lifecycle-stage
scoping can limit retention to specific stages (e.g., remove DEV artifacts
older than 2 weeks). Note: Release Lifecycle Management itself has a
published end-of-life date of January 31, 2028.
([docs.jfrog.com/administration/docs/retention-policies](https://docs.jfrog.com/administration/docs/retention-policies))

### 2.5 Partner/ISV onboarding

NVIDIA partnership validated for Artifactory as skills registry. JFrog AI
Catalog acts as control plane for NVIDIA OpenShell. No separate ISV
certification program for skills. Ecosystem integrations with Cursor and
GitHub mentioned.

### 2.6 Lifecycle states

Release Lifecycle Management progression: DEV --> INT --> STG --> PROD with
configurable approval requirements per stage. Evidence collection generates
signed metadata at every action. Xray can block promotion if policy violations
found. Skills Registry (feature preview) will align with the same project-scoped
approval model. Subscription tier gating: promotion requires Pro+, Xray policy
gating requires Enterprise X+, distribution requires Enterprise+.
([docs.jfrog.com/governance/docs/release-lifecycle-management](https://docs.jfrog.com/governance/docs/release-lifecycle-management))


## 3. AWS AgentCore

AWS provides the most structured registry-record lifecycle with explicit
approval workflows and a clear terminal deprecation state.

### 3.1 Intake/onboarding

Four skill source pathways: (1) AWS pre-built skills selected via glob
patterns from the Agent Toolkit; (2) Git clone from any HTTPS repository
(private repos use credential ARN); (3) Amazon S3 fetch (max 1 GB); (4)
filesystem path on the harness. Registry records for organizational
discovery start in DRAFT status and flow through approval.
([docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-skills.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-skills.html))

### 3.2 Verification/validation

Skills fetched once per session on first invocation; new sessions re-fetch
for freshness. Git fetch must complete within 60 seconds. Registry record
validation includes automated checks (schema, required fields, metadata
completeness, baseline policy readiness) plus functional and safety review
(functionality, endpoint behavior, authentication, security, compliance,
responsible AI). Auto-approval option available for organizations that want
to skip manual curator review. AgentCore Evaluations (GA March 2026) provides
automated assessment including code-based Lambda evaluators. Cedar schema
validates gateway policies.
([docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-record-lifecycle.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-record-lifecycle.html))

### 3.3 Versioning

No explicit SemVer for skills. Skills referenced by source (git URL, S3 URI,
AWS skill path) without version pinning in the skill format. Registry records
have explicit revisions: editing an APPROVED record creates a new DRAFT
revision while the approved version remains discoverable. Agent versions
use numbered AgentVersion with explicit references.

### 3.4 Deprecation/removal

DEPRECATED is a **terminal state** -- can be transitioned from any status and
**cannot be undone**. To temporarily hide without deprecating, reject the
record (rejected records excluded from discovery APIs and MCP endpoint). Once
rejected, records must go through normal submit-and-approve flow again.
Note: the `bedrock-agentcore` namespace support is being discontinued
September 17, 2026, with migration to `agent-registry` namespace required.

### 3.5 Partner/ISV onboarding

ISVs access AWS Partner Network (APN) with architecture design guidance,
development credits, go-to-market funding, and co-sell support via ISV
Accelerate Program. For skills: contribute to AWS Agent Toolkit via GitHub
PR or use private S3/Git repositories.

### 3.6 Lifecycle states

DRAFT --> PENDING_APPROVAL --> APPROVED (discoverable via search APIs and MCP
endpoint). PENDING_APPROVAL can also lead to REJECTED (editable, resubmittable).
Any status can transition to DEPRECATED (terminal, irreversible). Only APPROVED
records are returned by discovery APIs.


## 4. Microsoft APM / Copilot Studio

Microsoft's approach layers APM (the dependency manager for agent skills)
on top of Copilot Studio's publish model and Partner Center's certification
pipeline. The result is the market's most complex lifecycle.

### 4.1 Intake/onboarding

APM declares dependencies in `apm.yml` (skills, prompts, instructions,
plugins, MCP servers). `apm install` resolves dependencies, scans, enforces
policy gates, integrates into target harnesses, and writes a lockfile.
Supports GitHub Copilot, Claude Code, Cursor, OpenCode, Codex, Gemini,
Windsurf, and Kiro. Copilot Studio skills are self-contained Markdown
with YAML frontmatter. MCP server packages are submitted via Partner Center
as ZIP packages with manifest, tool definitions, authentication config, and
metadata.
([microsoft.github.io/apm/concepts/lifecycle](https://microsoft.github.io/apm/concepts/lifecycle/);
[learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-certification](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-certification))

### 4.2 Verification/validation

APM install pipeline: resolve --> policy gate --> security scan (hidden
Unicode detection, content hash pinning, transitive MCP server blocking) -->
integrate --> lockfile. MCP server certification is a 5-step process:
package prep, Partner Center submission, automated validation (schema,
required fields, metadata), functional and safety review (functionality,
auth, security, compliance, responsible AI), and approval/publishing. Annual
recertification required for certified apps. Copilot plugin validation
includes responsible AI checks and certification badge on AppSource.
([learn.microsoft.com/en-us/partner-center/marketplace-offers/submit-to-appsource-via-partner-center](https://learn.microsoft.com/en-us/partner-center/marketplace-offers/submit-to-appsource-via-partner-center))

### 4.3 Versioning

Each publish creates a new ordinal version (no explicit SemVer). **No rollback
capability** -- once published, cannot restore to a previous version. Workaround:
export agent as solution before modifying. MCP server packages include a
version field; resubmission required for new tools or significant metadata
changes. APM uses lockfiles for reproducibility.

### 4.4 Deprecation/removal

No formal deprecation states. Skills can be deleted permanently from an
agent. IT admins can disable agents/plugins on user/group basis via M365
admin center and Microsoft Purview. MCP server publishers responsible for
maintaining certified experience; no explicit deprecation timeline or grace
period documented.

### 4.5 Partner/ISV onboarding

MCP server certification requires: verified publisher in Partner Center with
completed business verification, enrolled in M365 and Copilot program,
ownership of MCP server endpoint, approved auth method (OAuth2, Azure AD,
API Key via Azure Key Vault). Timeline: typically 4-6 weeks for submission
and approval; 3-4 business days for reviewer responses; 60-day compliance
window. Annual recertification.

### 4.6 Lifecycle states

Copilot Studio: DRAFT --> PUBLISHED (ordinal versions). MCP server
certification: Submitted --> Validating --> Approved --> Certified
(published to Copilot Studio, Azure Foundry, M365 admin center). APM
packages: INIT --> INSTALLED --> COMPILED --> RUNNING/AUDITED. No explicit
deprecation state across any of these; relies on publisher delisting or
admin disabling.


## 5. Google Gemini Enterprise Agent Platform

Google has the **clearest lifecycle state machine** in the market, with five
explicit states and the only continuous evaluation system documented.

### 5.1 Intake/onboarding

Single-step Skill Registry submission via Cloud Console, gcloud CLI, or REST
API. Payload: ZIP archive (500 KB compressed max, 10 MB uncompressed max)
with required SKILL.md at root plus optional scripts/, references/, assets/.
Auto-assigned to `private` publisher namespace. Requires
`roles/agentregistry.user` on GCP project. Partners submit via Google Cloud
AI Agent Ecosystem Program or list on Google Cloud Marketplace.
([docs.cloud.google.com/agent-registry/register-skills](https://docs.cloud.google.com/agent-registry/register-skills);
[cloud.google.com/blog/topics/partners/build-deploy-and-promote-ai-agents](https://cloud.google.com/blog/topics/partners/build-deploy-and-promote-ai-agents-through-the-google-cloud-ai-agent-ecosystem-program))

### 5.2 Verification/validation

All skills pass automated gates before entry: frontmatter metadata linters,
line count and directory layout checks, strict naming conventions (lowercase
alphanumeric + hyphens matching parent directory), link checkers (test every
URL to eliminate 404s), and AI-assisted checklists validating structural
patterns. **Continuous evaluation**: on-submit evaluation with author-provided
prompt suites and scoring rubrics, plus weekly recurring evaluations across
the full library to catch regressions from API changes, model updates, or
harness changes. Results classified on a 2x2 accuracy/efficiency matrix:
Ship (both good), Fix accuracy, Optimize efficiency, or Rework (both bad).
Multiple runs across different agent frameworks for statistical significance.
([cloud.google.com/blog/topics/developers-practitioners/behind-the-scenes-how-we-build-test-and-scale-google-agent-skills](https://cloud.google.com/blog/topics/developers-practitioners/behind-the-scenes-how-we-build-test-and-scale-google-agent-skills))

### 5.3 Versioning

Revision-based immutable system. Each revision is permanently archived.
`default_revision` pointer determines which version is served at runtime.
Override via Console, gcloud CLI, or REST API. No explicit SemVer -- system
is revision-based (immutable increments). Spec compliance validated by
`skills-ref validate` tool.
([docs.cloud.google.com/agent-registry/manage-skills](https://docs.cloud.google.com/agent-registry/manage-skills))

### 5.4 Deprecation/removal

**Five explicit lifecycle states** -- the clearest in the market:

| State | Behavior |
|---|---|
| Draft | Not served at runtime; downloads blocked; config freely modifiable |
| Active | Fully served and resolvable at runtime |
| Disabled | Resolution fails immediately; downloads blocked; **reversible** |
| Deprecated | Remains loadable; returns warning headers indicating sunset |
| Decommissioned | **Terminal** -- permanent, cannot revert; must pass through Deprecated first |

Deletion permanently removes skill container and all revision history
(separate from Decommissioned). Documentation recommends "extreme caution"
for Decommissioned transitions.

### 5.5 Partner/ISV onboarding

Google Cloud AI Agent Ecosystem Program (launched Nov 2024) offers three
pillars: accelerated development (direct engineering access, early tech),
go-to-market co-selling, and customer visibility via marketing and events.
Open to services partners (Accenture, Deloitte, BCG) and ISV partners
(Elastic, UKG, ThoughtSpot). Marketplace destination: AI Agent Space
(dedicated category). No published technical verification gate for partners
beyond standard Skill Registry ingestion constraints.

### 5.6 Lifecycle states

Draft --> Active --> Disabled (reversible) / Deprecated (warning headers) -->
Decommissioned (terminal). Supplementary: A2A protocol defines task states
(Pending --> In-Progress --> Completed/Failed/Canceled) with Input-Required
for interactive workflows.


## 6. Databricks Unity AI

Databricks takes a function-first approach, treating skills as Unity Catalog
functions with minimal packaging requirements but strong governance through
the catalog layer.

### 6.1 Intake/onboarding

Agent tools are Unity Catalog UDFs created via `create_python_function`
(Python callable with type hints) or `create_function` (SQL body). Registered
with catalog + schema naming. Integration via managed MCP URL or
UCFunctionToolkit wrapper. Marketplace providers apply through the Databricks
Data Partner Program or set up Private Exchange internally.
([docs.databricks.com/aws/en/agents/custom-agents/create-custom-tool](https://docs.databricks.com/aws/en/agents/custom-agents/create-custom-tool);
[docs.databricks.com/aws/en/marketplace/become-provider](https://docs.databricks.com/aws/en/marketplace/become-provider))

### 6.2 Verification/validation

MCP server Marketplace validation uses a 4-phase process: (1) independent
testing by partner; (2) 30-minute live integration review with Partner
Engineering; (3) listing creation with description, categories, docs, privacy
policy, OAuth config; (4) published listing test as consumer. Comprehensive
security review before publication. Provider policies require accurate
descriptions, authorized trademarks, and Consumer Terms of Use.
([databrickslabs.github.io/partner-architecture/data-collaboration/mcp-marketplace-validation](https://databrickslabs.github.io/partner-architecture/data-collaboration/mcp-marketplace-validation))

### 6.3 Versioning

**Mutable latest-version-wins model** -- `replace=True` overwrites existing
functions. No formal versioning constructs (no version numbers, aliases, or
SemVer). Client caches function definitions locally, so updates may not
propagate immediately. This poses significant reproducibility challenges for
production deployments.

### 6.4 Deprecation/removal

Functions are governed securables in Unity Catalog (April 2026). Can tag
functions for lifecycle management and certify or deprecate them. However,
no explicit terminal state documented (unlike Google's Decommissioned).
Governance integrates with UC's row/column-level access controls and audit
trails.

### 6.5 Partner/ISV onboarding

Databricks Data Partner Program: apply via partner page or contact
partnerops@databricks.com. MCP server integration requires enrollment as
Data Partner plus HTTP/OAuth-ready server. Integration review (30-min live
session) validates the integration before Marketplace publication. OpenSharing
protocol (June 2026, Linux Foundation) enables cross-platform AI asset
sharing with granular provider controls.
([databricks.com/blog/introducing-opensharing](https://www.databricks.com/blog/introducing-opensharing-next-evolution-delta-sharing-agentic-era))

### 6.6 Lifecycle states

Not formally specified for skills. Agent development lifecycle follows five
phases: understand use case, build initial agent, iterate on quality, align
with stakeholders, release and monitor. OpenSharing enables cross-cloud
sharing with granular controls (instruction hiding, prompt quotas, row export
limits).


## 7. Anthropic Marketplace

Anthropic created the SKILL.md specification (now the agentskills.io open
standard) and operates a curated marketplace with a growing partner network.

### 7.1 Intake/onboarding

Dual marketplace model: official marketplace (marketplace.anthropic.com,
600+ curated skills) with Anthropic-controlled review, plus community
marketplace (anthropics/claude-plugins-community) for third-party submissions.
Submit via official submission form; validate locally with
`claude plugin validate ./your-plugin`. Distribute during review via GitHub
URL using `/plugin install <repo-url>`. Review typically takes a few days.
([claude.com/platform/marketplace](https://claude.com/platform/marketplace);
[github.com/anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official))

### 7.2 Verification/validation

Automated safety screening and quality standards review before approval.
Reviewers evaluate source trust, bundled components, context cost, will-install
lists, version pinning, and managed-scope controls. Anthropic enforces
ecosystem rules including banning third-party operators violating usage
policies ("OpenClaw" enforcement). Plugins are highly trusted components
running with user privileges.
([code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins))

### 7.3 Versioning

SemVer 2.0.0 starting at 1.0.0. Major version increment required for breaking
changes (restructuring instructions, renaming commands, changing hook behavior).
Migration path required in CHANGELOG for breaking changes. Programmatic version
management via `/v1/skills` API endpoint. Console access for creating, viewing,
and upgrading skill versions.
([anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills))

### 7.4 Deprecation/removal

No published timeline for feature removal. Skills can be marked with
`@deprecated` metadata; execution appends removal date and migration
instructions. Removed skills deleted from repository with sync triggered.
`claude doctor` inspects skills for context optimization (8-12 skills optimal
before "context tax"). Commands-to-skills migration underway but no official
removal timeline.

### 7.5 Partner/ISV onboarding

Claude Partner Network (March 2026): three tracks (Consulting, Technology/ISV,
Services) backed by $100M commitment. 60-day structured onboarding with
Partner Portal access, Partner Success Manager, product roadmap briefings,
co-sell training, and technical enablement. Claude Certified Architect
certification available through Anthropic Academy (Skilljar). Role-specific
learning paths for architects, sales, and delivery teams.
([anthropic.com/news/services-track-partner-hub](https://www.anthropic.com/news/services-track-partner-hub))

### 7.6 Lifecycle states

Active (discoverable, installable) --> Deprecated (@deprecated metadata,
warning in description) --> Removed (deleted, sync triggered). No resurrection
mechanism documented.


## 8. skills.sh (Vercel)

The largest open index by volume (669K+ skills), operating a fully
decentralized GitHub-native model with Snyk partnership for security.

### 8.1 Intake/onboarding

**Zero-submission model**: create a public GitHub repo with SKILL.md; skills
automatically surface on skills.sh via install telemetry. No registry
submission process. Install via `npx skills add <github-url>` or interactive
discovery. Skills gaining traction appear on leaderboard automatically.
Set `metadata.internal: true` to hide from public discovery (WIP/internal).
([vercel.com/docs/agent-resources/skills](https://vercel.com/docs/agent-resources/skills);
[vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem))

### 8.2 Verification/validation

Snyk partnership provides real-time security scanning at installation time:
detects malicious payloads and prompt injections before installation,
"Security Verified" badge displayed, continuous re-evaluation as threat
patterns emerge. Critical-level detectors achieve 90-100% recall on confirmed
malicious skills with 0% false positive rate on legitimate skills. Working
with partners (Gen, Socket, Snyk) to audit 60,000+ skills. Flagged skills
automatically hidden from leaderboard and search.
([snyk.io/blog/snyk-vercel-securing-agent-skill-ecosystem](https://snyk.io/blog/snyk-vercel-securing-agent-skill-ecosystem/))

### 8.3 Versioning

Content-hash based rather than SemVer. `skills-lock.json` tracks installed
skill source, source type, skill path, and computed content hash. Enables
version comparison and rollback based on content. No SemVer requirement;
developers use git commits and tags while skills.sh tracks via content hash.

### 8.4 Deprecation/removal

No formal removal policy. Decentralized model: delete from GitHub, skill
disappears from public view. No removal notification mechanism. Old/unused
skills naturally fall in leaderboard rankings (anonymous telemetry-based).
Users run `npx skills remove [skill-name]` to uninstall.

### 8.5 Partner/ISV onboarding

No formal partner program. Snyk partnership for security verification.
Community-driven: skills succeed based on organic adoption and GitHub
repository quality. LobeHub integration provides secondary distribution
channel.

### 8.6 Lifecycle states

Public (listed, discoverable) --> Internal (hidden, metadata.internal: true)
--> Archived (GitHub repo archived; still installable via direct URL) -->
Removed (deleted from repo; no archive on skills.sh). No standardized
deprecated state.


## 9. Cisco DefenseClaw

Cisco focuses on the **security governance layer** rather than operating
a skill catalog, providing pre-execution scanning and runtime enforcement
for any agent runtime.

### 9.1 Intake/onboarding

Not a skills marketplace. DefenseClaw integrates as a security sidecar with
agent runtimes (primarily NVIDIA OpenShell). Skills enter through the host
runtime's onboarding process; DefenseClaw provides the admission control gate.

### 9.2 Verification/validation

Pre-execution scanning of all skills, tools, MCP servers, and LLM traffic
before admission to runtime. Components: MCP Scanner, Skills Scanner, AI Bill
of Materials (AI BoM) generator, CodeGuard static analysis. Runtime: policy
engine runs as sidecar inside OpenShell container with deny-by-default network
access, YAML policy enforcement, and privacy router for sensitive data.
([cisco-ai-defense.github.io/defenseclaw](https://cisco-ai-defense.github.io/defenseclaw/);
[blogs.cisco.com/ai/securing-enterprise-agents-with-nvidia-and-cisco-ai-defense](https://blogs.cisco.com/ai/securing-enterprise-agents-with-nvidia-and-cisco-ai-defense))

### 9.3 Versioning

Supports Draft --> Sandbox --> Publish lifecycle with version control and full
rollback support at the security policy level.

### 9.4 Deprecation/removal

Post-action lifecycle visibility confirms access removal and audit trail.
No skill-level deprecation -- operates at the policy/admission level.

### 9.5 Partner/ISV onboarding

Open-source framework (Apache-2.0). NVIDIA partnership for OpenShell
integration. No separate partner program for skills.

### 9.6 Lifecycle states

Pre-execution (scanning/admission) --> Runtime (policy enforcement,
monitoring) --> Post-action (access removal, audit trail). Operates as
an overlay on the host runtime's lifecycle.


## 10. Emerging platforms

### 10.1 Tessl Registry

Full lifecycle: Build --> Evaluate --> Distribute --> Optimize. Review
evaluations test structure against Anthropic best practices; task evaluations
run agents with/without skill on real tasks. Rollout across repos, teams,
agents automatically. Publish to Tessl Registry (team or public access).
Manifest file clarifies installed skills. Snyk partnership for scanning at
publish, browse, and install time. Data-driven optimization loop removes
poorly performing skills.
([tessl.io/blog/skills-are-software](https://tessl.io/blog/skills-are-software-and-they-need-a-lifecycle-introducing-skills-on-tessl/))

### 10.2 Smithery.ai

Central MCP server registry (6,000+ servers). CLI tools for install, update,
search, publish. Validates compatibility and dependencies. Manages versioning
and permission scope requirements. No documented deprecation policy.
([smithery.ai](https://smithery.ai/))

### 10.3 MCP specification lifecycle

SEP-2596 defines feature lifecycle: Active --> Deprecated --> Removed with
minimum 12-month deprecation window. Every deprecation requires documented
migration path. Deprecation and removal each require separate SEP proposals.
This is the only platform with a formally specified minimum deprecation
window.
([modelcontextprotocol.io/docs/2026-07-28/learn/versioning](https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning))


## 11. Lifecycle comparison matrix

This matrix compares all platforms across the six lifecycle dimensions. This
is the centerpiece of the analysis.

| Dimension | NVIDIA | JFrog | AWS AgentCore | Microsoft APM | Google Gemini | Databricks | Anthropic | skills.sh | Cisco | RHOAI (planned) |
|---|---|---|---|---|---|---|---|---|---|---|
| **Intake model** | Product-team repos; NeMo plugin PR | Artifactory upload; CLI auto-version | 4 sources: AWS pre-built, Git, S3, filesystem | apm.yml declaration; Partner Center ZIP | Single-step Skill Registry ZIP | UC function (Python/SQL); Partner Program | Form submission; GitHub PR | Zero-submission GitHub-native | Security sidecar (no catalog) | OCI push; Kubeflow Hub submission |
| **Format** | SKILL.md (agentskills.io) | SKILL.md (agentskills.io) | SKILL.md (agentskills.io) | Markdown + YAML; manifest JSON | SKILL.md (agentskills.io) | Python callable / SQL DDL | SKILL.md (agentskills.io) | SKILL.md (agentskills.io) | N/A (runtime overlay) | OCI artifact + SKILL.md |
| **Submission review** | Human + automated; 8-stage pipeline | Automated Xray scan | Automated + functional/safety; optional auto-approve | 5-step certification; annual recert | Linters + link check + AI checklists + continuous eval | 30-min live integration review | Automated safety + quality review | Zero review (Snyk scan at install) | Pre-execution admission scan | Konflux SLSA L3 build + scan |
| **Scanning depth** | SkillSpector: 68 patterns / 17 categories | Xray: malicious, CVE, compliance | Cedar policy validation; Evaluations | Hidden Unicode, hash pinning, transitive blocking | Link checking, AI-assisted structural validation | Security review (details undocumented) | Automated validation + safety screening | Snyk: 90-100% recall, 0% FPR | MCP Scanner + Skills Scanner + AI BoM + CodeGuard | Xray + SkillSpector (via NVIDIA partnership) |
| **Versioning** | SemVer; OMS-signed directory | SemVer; SKILL.md version field; auto-increment | No explicit SemVer; registry revisions | Ordinal per publish; no rollback | Immutable revisions; default_revision pointer | Mutable latest-wins; no versioning | SemVer 2.0.0; /v1/skills API | Content-hash; skills-lock.json | Policy-level version control | SemVer; OCI tags + digests |
| **Update propagation** | Daily sync from source repos | `jf agent skills update`; rollback on failure | Re-fetch per session | Resubmit for certification | Override default_revision | replace=True; client cache lag | CHANGELOG + migration path | Git commits; hash comparison | Policy updates via sidecar | OCI pull + Kubeflow Hub sync |
| **Deprecation states** | None formal (Git-level) | Cleanup Policies; Smart Archiving | DEPRECATED (terminal, irreversible) | None formal (admin disable) | Deprecated (warning headers) --> Decommissioned (terminal) | Tag + certify/deprecate (underspecified) | @deprecated metadata; removal + sync | None formal (leaderboard decay) | N/A (policy-level) | Planned: TBD |
| **Sunset period** | Not specified | Retention policy configurable | None (instant terminal) | Not specified | Required: must pass through Deprecated before Decommissioned | Not specified | Not specified | None (instant disappearance) | N/A | Planned: TBD |
| **Consumer notification** | Not documented | Not documented | Excluded from discovery APIs | Admin-controlled disabling | Warning headers on Deprecated skills | Not documented | @deprecated in description + execution output | Leaderboard disappearance only | Audit trail | Planned: TBD |
| **Partner onboarding** | NPN; 7-step NeMo plugin lifecycle | NVIDIA partnership; no ISV cert | APN; ISV Accelerate; GitHub PR | Partner Center; 4-6 week cert; annual recert | AI Agent Ecosystem Program; 3 pillars | Data Partner Program; 30-min integration review | Claude Partner Network; $100M; 60-day onboarding | None (community-driven) | Open-source (Apache-2.0) | Planned: partner verification pipeline |
| **Certification** | Skill cards (YAML/JSON) | Signed metadata per action | Registry record approval | AppSource badge; annual recert | Publisher namespace (private/public) | UC governance (row/column ACLs) | Marketplace listing | "Security Verified" badge (Snyk) | AI BoM | Planned: Red Hat certification |
| **Lifecycle states** | Draft --> Published | DEV --> INT --> STG --> PROD | DRAFT --> PENDING --> APPROVED; any --> DEPRECATED | DRAFT --> PUBLISHED; Submitted --> Certified | Draft --> Active --> Disabled --> Deprecated --> Decommissioned | Not formally specified | Active --> Deprecated --> Removed | Public --> Internal --> Archived --> Removed | Pre-exec --> Runtime --> Post-action | Planned: TBD |


## 12. Cross-cutting patterns and gaps

### 12.1 Industry convergence on SKILL.md

Seven of the ten platforms have adopted or are compatible with the
agentskills.io SKILL.md specification (originally created by Anthropic,
now an open standard). This represents significant convergence on the
packaging format even as lifecycle management diverges widely.

### 12.2 Verification is the competitive battleground

The market bifurcates into two models:

**Gate-once platforms** (most): verify at submission/intake, then trust
indefinitely. AWS, Microsoft, Anthropic, and Databricks all use this model.
UC Irvine research found 99% of real skills carry at least one flaw caught
by routine review, suggesting one-time gates are insufficient.
([arxiv.org/html/2602.12430v3](https://arxiv.org/html/2602.12430v3))

**Continuous verification platforms** (few): Google's weekly evaluation
loops, Tessl's continuous evaluation, and NVIDIA's daily sync with re-scan
represent the emerging best practice. Snyk's continuous re-evaluation of
skills.sh adds a third variant (continuous security without quality eval).

### 12.3 Deprecation is the market's weakest link

Only two platforms have explicit, documented deprecation state machines:
Google (5 states with terminal Decommissioned) and AWS (terminal DEPRECATED).
The MCP specification mandates a 12-month minimum deprecation window but
leaves implementation to platforms. Everyone else either has no formal
deprecation (NVIDIA, JFrog, Microsoft, skills.sh) or underspecified states
(Databricks, Anthropic).

Gartner's forecast of 150,000 agents per Fortune 500 by 2028 (up from <15
in 2025) makes this gap critical. Without formal deprecation, enterprises
face "zombie skill" accumulation: stale skills cluttering context windows,
increasing latency, and burning tokens.
([gartner.com/en/newsroom/press-releases/2026-04-28-gartner-identifies-six-steps](https://www.gartner.com/en/newsroom/press-releases/2026-04-28-gartner-identifies-six-steps-to-manage-artificial-intelligence-agent-sprawl))

### 12.4 Versioning model fragmentation

Three distinct versioning approaches compete:

1. **SemVer** (NVIDIA, JFrog, Anthropic): traditional, well-understood,
   requires author discipline
2. **Immutable revisions** (Google, AWS): platform-managed, automatic, no
   rollback ambiguity
3. **Content-hash** (skills.sh): decentralized, content-addressable, no
   author overhead

Databricks is an outlier with **no versioning at all** (latest-wins), which
creates significant production risk. Microsoft's ordinal-per-publish model
with no rollback is similarly problematic.

### 12.5 Partner onboarding maturity

Partner programs range from $100M investments (Anthropic) to open-source
community models (Cisco, skills.sh). The critical gap: no platform combines
technical verification with business onboarding. NVIDIA has the deepest
technical pipeline but limited business support; Anthropic and Microsoft
have the richest partner programs but lighter technical gates.

### 12.6 Proportional governance

Gartner explicitly warns that "uniform governance across all agents leads to
enterprise AI agent failure" and recommends proportional governance classifying
agents by autonomy level. No current platform implements proportional
governance for skills -- all apply the same lifecycle regardless of skill
risk level or autonomy. This is a design opportunity for RHOAI.
([gartner.com/en/newsroom/press-releases/2026-05-26-gartner-says-applying-uniform-governance](https://www.gartner.com/en/newsroom/press-releases/2026-05-26-gartner-says-applying-uniform-governance-across-ai-agents-will-lead-to-enterprise-ai-agent-failure))


## 13. RHOAI differentiation opportunities

Red Hat's planned stack (Konflux SLSA L3 + OCI artifacts + MLflow registry +
Kubeflow Hub catalog) is unique in combining all four layers. No competitor
does this. The lifecycle analysis reveals five specific differentiation plays:

1. **End-to-end lifecycle state machine**: Google has the clearest states but
   no build provenance. NVIDIA has the deepest scanning but no formal
   deprecation. RHOAI can be the first to define a complete state machine
   from intake through decommission with SLSA L3 provenance at every
   transition.

2. **Continuous verification with provenance**: Combine NVIDIA SkillSpector
   scanning (via partnership) with Konflux hermetic builds and Conforma policy
   engine for the market's only continuously-verified, provenance-tracked
   skill pipeline.

3. **Proportional governance**: Implement Gartner's proportional governance
   recommendation at the skill level -- classify skills by autonomy/risk
   level and apply proportional lifecycle controls. No competitor does this.

4. **OCI-native versioning with rollback**: Use OCI tags + digests for
   SemVer with content-addressable immutability. Unlike Google's revision
   model (proprietary), OCI is an open standard. Unlike skills.sh's
   content-hash (no ecosystem), OCI has universal registry support.

5. **Federated deprecation with sunset periods**: Define minimum sunset
   periods (borrowing from MCP's 12-month model), warning headers (borrowing
   from Google), and consumer notification (gap everywhere). Apply across
   federated registries using ARD.


## Key findings

1. No competitor manages the full skill lifecycle from intake through
   deprecation with provenance at every stage -- this is the gap RHOAI can
   own by combining Konflux, OCI, MLflow, and Kubeflow Hub.

2. NVIDIA leads on verification depth (68 patterns, 17 categories, OMS
   signing) but has no formal deprecation states, making its lifecycle
   incomplete for enterprise governance.

3. Google has the market's clearest lifecycle state machine (five explicit
   states with terminal Decommissioned) and the only documented continuous
   evaluation system, but lacks build provenance and supply-chain signing.

4. AWS provides the most structured registry approval workflow with an
   explicit terminal DEPRECATED state, but its skills themselves have no
   versioning -- a significant gap for reproducibility.

5. Microsoft has the most complex lifecycle (APM + Copilot Studio + Partner
   Center certification) but no rollback capability and no formal deprecation
   states, creating operational risk at scale.

6. Databricks has no formal skill versioning (latest-wins model) and
   underspecified deprecation, despite strong governance in Unity Catalog
   -- the lifecycle gap contradicts the platform's governance positioning.

7. Seven of ten platforms have converged on the agentskills.io SKILL.md
   specification for packaging, but lifecycle management remains fragmented
   across SemVer, immutable revisions, content-hash, and no-versioning
   models.

8. Deprecation is the market's weakest lifecycle dimension: only Google
   and AWS have explicit deprecation states, and only the MCP specification
   mandates a minimum sunset period (12 months) -- Gartner's 150K
   agents-per-enterprise forecast makes this gap critical.

9. No platform implements proportional governance for skills despite
   Gartner's explicit warning that uniform governance leads to enterprise AI
   agent failure -- classifying skills by autonomy/risk level is an unmet
   design opportunity.

10. The verification market bifurcates into gate-once (most platforms) and
    continuous (Google, Tessl, NVIDIA daily sync), with UC Irvine research
    showing 99% of skills carry at least one flaw -- continuous verification
    is the emerging enterprise requirement.

11. Partner onboarding programs range from $100M investments (Anthropic
    Claude Partner Network) to zero structure (skills.sh), but no platform
    combines deep technical verification with structured business onboarding
    -- the combination is a differentiation opportunity.

12. Red Hat's unique ability to combine SLSA L3 provenance (Konflux),
    content-addressable immutable versioning (OCI), artifact lifecycle
    management (MLflow), and catalog UX (Kubeflow Hub) positions RHOAI
    to define the first complete, open-standards-based skill lifecycle
    for the enterprise market.
