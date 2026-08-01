---
title: Skills Registry — Packaging Analysis
description: Analysis of packaging format options for AI skills in RHOAI -- creation, distribution, consumption, scanning, and governance.
source: ai-asset-registry/skills/skills-registry/strategy/packaging-analysis.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Skills Registry — Packaging Analysis

## Purpose

This document analyzes packaging format options for AI skills in RHOAI. Packaging is one of the most important open questions for the skills registry — it determines how skills are created, distributed, consumed, scanned, and governed.

This document does not prescribe a single format. It presents the landscape, tradeoffs, and considerations to inform a decision with stakeholders.

---

## The Two Concerns

Packaging discussions conflate two distinct concerns:

1. **Manifest format** — how a skill is described (metadata, capabilities, dependencies, instructions)
2. **Distribution format** — how a skill is moved from producer to consumer (stored, transported, resolved)

These can be mixed and matched. A SKILL.md manifest can be distributed as an OCI artifact. A Python package can contain a YAML manifest. The choices are independent.

---

## Manifest Format Options

### SKILL.md (Agent Skills Specification)

**What it is**: An open standard published by Anthropic (December 2025), adopted by OpenAI Codex, Google Gemini CLI, GitHub Copilot, VS Code. A directory containing a `SKILL.md` file with YAML frontmatter + markdown instructions, plus optional `scripts/`, `references/`, and `assets/` subdirectories.

**Structure**:
```
my-skill/
  SKILL.md              # Required: frontmatter + instructions
  scripts/
    setup.sh            # Optional: executable scripts
    validate.py
  references/
    api-spec.yaml       # Optional: reference docs
  assets/
    icon.png            # Optional: visual assets
```

**SKILL.md format**:
```markdown
---
name: email-assistant
description: Email management capabilities for AI agents
version: 1.2.0
---

# Email Assistant

## Instructions
[Markdown instructions for the agent consuming this skill]

## Resources
[References to external tools, APIs, MCP servers]
```

**Strengths**:
- Emerging de facto standard across major agent platforms
- Human-readable, version-controllable in git
- Progressive disclosure model (metadata at startup, instructions on demand, resources during execution)
- Lightweight — no tooling required to create
- Multi-file support via directory structure
- Aligns with how the Databricks prototype stores skills (markdown as MLflow artifacts)
- MLflow's own `mlflow/skills` repo already uses this format

**Weaknesses**:
- Limited structured metadata in frontmatter — no standard fields for dependencies, auth requirements, resource limits, or governance
- No formal schema validation — frontmatter is freeform YAML
- No integrity verification (no hashes, signatures)
- No dependency declaration mechanism
- Specification is young (December 2025) and still evolving

**Assessment**: Strong starting point for skill content and instructions. Insufficient alone for enterprise governance metadata — needs to be wrapped in a richer registry record or distribution format.

---

### Custom RHOAI Skill Descriptor (YAML/JSON)

**What it is**: A richer, structured manifest designed for enterprise governance. Would include governance metadata, dependency declarations, packaging references, and security context beyond what SKILL.md provides.

**Example**:
```yaml
apiVersion: registry.rhoai.io/v1alpha1
kind: Skill
metadata:
  name: email-assistant
  version: 1.2.0
  description: Email management capabilities for AI agents
  provider: Red Hat
  license: Apache-2.0
spec:
  capabilities:
    - name: send_email
      description: Compose and send emails
      readOnly: false
    - name: search_inbox
      description: Search emails by query
      readOnly: true
  packaging:
    type: mcp-server
    transport: streamable-http
  dependencies:
    - type: mcp-server
      name: email-tools-server
      version: ">=1.0.0"
  requirements:
    authentication:
      - type: oauth2
        scopes: [email.read, email.send]
  content:
    skillMd: ./SKILL.md          # Reference to SKILL.md content
    scripts: ./scripts/
```

**Strengths**:
- Full governance metadata in a structured, validatable schema
- Dependency declarations with version constraints
- Packaging type and consumption model explicit
- Can reference SKILL.md for content while adding governance wrapper
- Aligns with Kubernetes manifest patterns (familiar to Platform Engineers)

**Weaknesses**:
- Custom format — no external adoption
- Additional overhead for skill authors
- Risk of Red Hat-specific lock-in
- No ecosystem tooling

**Assessment**: Useful as a governance metadata schema that the RHOAI layer manages. Could wrap SKILL.md content rather than replacing it. Should not be required at the upstream MLflow level — governance metadata lives in RHOAI's extension layer (as tags or structured metadata).

---

### OpenAPI Specification

**What it is**: Industry-standard REST API description format. Semantic Kernel can import OpenAPI specs directly as plugins.

**Strengths**:
- Industry standard with mature tooling
- Rich metadata (operations, parameters, security schemes, schemas)
- Language-agnostic
- Already supported by Semantic Kernel for plugin import

**Weaknesses**:
- REST-only (no streaming, no bidirectional, no CLI, no script-based skills)
- Verbose for simple skills
- No agent-specific metadata (behavioral hints, examples, framework compatibility)
- Describes APIs, not capabilities

**Assessment**: Useful as an import source — the registry should be able to create skill records from OpenAPI specs. Not suitable as the primary skill manifest format because many skills are not REST APIs.

---

## Distribution Format Options

### MLflow Artifact Store (Direct)

**What it is**: Store skill content (SKILL.md directory, files, etc.) directly in MLflow's artifact store (S3, Azure Blob, GCS, local filesystem, PVC).

**How it works**: `mlflow.register_skill()` uploads the skill content as an artifact. `mlflow.load_skill()` downloads it. Versioning, storage, and retrieval handled by MLflow infrastructure.

**Strengths**:
- Zero additional infrastructure — uses what MLflow already has
- Aligned with how Databricks prototype works ("markdown as MLflow artifacts")
- Consistent with Prompt Registry (prompts stored as artifacts)
- Supports any content format (packaging-agnostic)
- Versioning built in (MLflow version numbers)

**Weaknesses**:
- No standardized content signing or verification beyond what the artifact store provides
- No manifest validation at the storage level
- No cross-registry distribution protocol (skills live in one MLflow instance)
- No OCI ecosystem tooling (scanning, signing, mirroring)

**Assessment**: The right choice for upstream MLflow. Simple, consistent, and packaging-agnostic. RHOAI can add governance on top.

---

### OCI Artifacts

**What it is**: Store skill content as OCI artifacts (not containers) in an OCI-compatible registry (Quay, Docker Hub, Artifactory, ECR, etc.). Uses the OCI Image Spec v1.1 `artifactType` field for non-container content.

**How it works**: Skill content is pushed to an OCI registry with a custom media type (e.g., `application/vnd.redhat.ai.skill.v1`). Metadata layers describe the content. ORAS CLI/SDK handles push/pull.

**Example**:
```bash
# Push a skill directory as an OCI artifact
oras push quay.io/rhoai/skills/email-assistant:1.2.0 \
  --artifact-type application/vnd.redhat.ai.skill.v1 \
  ./email-assistant/:application/vnd.redhat.ai.skill.content

# Pull
oras pull quay.io/rhoai/skills/email-assistant:1.2.0
```

**Strengths**:
- Leverages existing enterprise registry infrastructure (Quay, Artifactory)
- Built-in content signing (cosign, Sigstore, Docker Content Trust)
- Built-in vulnerability scanning (Quay, Clair, Trivy)
- Built-in SBOM support (attached as referrer artifacts)
- Built-in mirroring and distribution across air-gapped environments
- Immutable content hashes (SHA-256 digests)
- Aligns with Red Hat's container-first strategy
- Docker, JFrog, and cloud providers converging on OCI for AI artifacts
- Namespace governance via registry access controls

**Weaknesses**:
- "Heavy" for individual skills that are just a markdown file and a few scripts (Hunter Gerlach, Ann Marie Fred)
- OCI tooling (ORAS) is less familiar to AI/ML practitioners than pip/npm
- "Not consumable" in OCI format — an agent can't directly consume an OCI artifact without extraction (Ann Marie Fred)
- Requires OCI registry infrastructure (additional dependency if not already present)
- No standard `artifactType` for AI skills — would need to be defined

**Assessment**: Strong for distribution and governance (signing, scanning, mirroring). Excessive for simple skills. Best positioned as the distribution format for enterprise/production skills — the RHOAI governance layer packages skills as OCI artifacts when they need enterprise supply chain guarantees. Not required for all skills.

---

### Container Images

**What it is**: Package the skill as a runnable container image (for server-side skills backed by MCP servers or HTTP services).

**Strengths**:
- Complete runtime isolation
- Existing enterprise infrastructure (Quay, Kubernetes, OpenShift)
- Familiar to Platform Engineers
- Proven scanning, signing, and distribution pipeline

**Weaknesses**:
- Only makes sense for server-side skills — client-side skills are not containers
- Heavyweight — minutes to build and pull vs. seconds for a SKILL.md
- Container skills are really MCP servers — already governed by the MCP Registry

**Assessment**: Not a general skill packaging format. Skills backed by MCP servers should be governed as MCP servers in the MCP Registry, with the skill registry holding a reference to the MCP server.

---

### Python Packages (pip)

**What it is**: Distribute skills as pip-installable Python packages.

**Strengths**:
- Familiar to Python developers (most AI/ML practitioners)
- Dependency management via pip/poetry
- Versioning via PyPI/SemVer
- Distribution via PyPI or private indexes

**Weaknesses**:
- Python-only
- No governance metadata standard
- No cross-language support
- pip packages are not skill-aware (no standard manifest)

**Assessment**: Relevant as an import source — skills distributed as Python packages should be registerable. Not suitable as the canonical format because skills must be language-agnostic.

---

### Git Repositories

**What it is**: Skills stored in git repositories, versioned via git tags/branches.

**Strengths**:
- Natural for developers
- Built-in versioning, branching, collaboration
- Supports any content structure
- GitHub/GitLab ecosystem for discovery

**Weaknesses**:
- No structured metadata standard
- No governance beyond git access controls
- No signing/scanning infrastructure built in
- Requires network access to clone

**Assessment**: Natural source for skill development and collaboration. The registry should support importing skills from git repos. Not a distribution format for governed consumption.

---

## Packaging Decision Framework

Rather than choosing one format, the right approach is a layered model:

```
┌─────────────────────────────────────────────┐
│         Registry Record (MLflow)            │
│  Identity, version, tags, publish state,    │
│  aliases, governance metadata               │
│                                             │
│  artifact_ref → points to one of:           │
├─────────────────────────────────────────────┤
│  MLflow Artifact Store    │  OCI Registry   │
│  (default, simple)        │  (enterprise)   │
│  - SKILL.md directory     │  - Signed OCI   │
│  - Config files           │    artifact     │
│  - Scripts                │  - SBOM         │
│  - Any format             │  - Scan results │
├─────────────────────────────────────────────┤
│           Skill Content                     │
│  - SKILL.md (instructions, frontmatter)     │
│  - scripts/ (executable code)               │
│  - configs/ (templates, parameters)         │
│  - references/ (API specs, docs)            │
│  - MCP server reference (if MCP-backed)     │
│  - CLI tool reference (if CLI-backed)       │
└─────────────────────────────────────────────┘
```

### How this works:

1. **Development phase**: Skill authors create skills in any format (SKILL.md, Python package, OpenAPI spec, etc.)
2. **Registration phase**: Skills are registered in MLflow. The artifact is stored in MLflow's artifact store. Governance metadata is captured in tags and the RHOAI governance layer.
3. **Governance phase**: For skills that need enterprise supply chain guarantees, the RHOAI ingestion pipeline can package the skill as an OCI artifact with signing, SBOM, and scan results — and store the OCI reference alongside the MLflow record.
4. **Consumption phase**: AI engineers resolve skills from the registry. Client-side consumers download the artifact. Server-side consumers get an endpoint reference.

### What goes where:

| Concern | Where it lives |
|---------|---------------|
| Skill content (instructions, scripts, configs) | MLflow artifact store or OCI registry |
| Identity, versioning, publish state | MLflow (upstream) |
| Governance metadata (approval, certification, trust) | RHOAI governance layer (tags + structured extension) |
| Supply chain attestations (signatures, SBOM, scan results) | OCI referrer artifacts (when applicable) |
| Dependency declarations | MLflow tags (Phase 1) → Entity associations (Phase 2) |

---

## Tradeoff Summary

| Format | Best For | Not For | RHOAI Role |
|--------|----------|---------|------------|
| SKILL.md | Skill content and instructions | Enterprise governance metadata | Recommended content format |
| MLflow artifacts | Simple storage and versioning | Supply chain assurance | Default distribution for all skills |
| OCI artifacts | Enterprise distribution with signing/scanning | Simple/development skills | Governance distribution for production skills |
| Container images | Server-side MCP-backed skills | Client-side skills | Governed as MCP servers, not skills |
| Python packages | Python tool libraries | Language-agnostic governance | Import source |
| OpenAPI specs | API-based skills | Non-API skills | Import source |
| Git repos | Development and collaboration | Production distribution | Import source |

---

## Considerations for Decision

1. **SKILL.md as recommended content format**: The industry is converging. MLflow's own team uses it. Databricks prototype stores markdown. Recommending it (not requiring) positions RHOAI aligned with the ecosystem.

2. **OCI for enterprise distribution**: Red Hat has the infrastructure (Quay), tooling (cosign, ORAS), and organizational expertise. OCI artifacts are the natural enterprise distribution layer. But the "heavy" and "not consumable" concerns from Ann Marie Fred and Hunter Gerlach are real — OCI should be an option for production governance, not a requirement for all skills.

3. **MLflow artifact store as default**: Keeps the upstream story simple and consistent with prompts. No additional infrastructure required. RHOAI can wrap in OCI when needed.

4. **The packaging type field matters**: Whatever format is used, the registry record should carry a `packaging_type` tag so consumers know how to interpret the artifact. This is metadata, not format enforcement.

5. **Tooling will drive adoption**: Whichever format is recommended, tooling to create, validate, and consume skills in that format will determine actual adoption. Consider investing in a `rhoai-skill` CLI or plugin for creating well-formed skill packages.

---

## Open Questions

1. Should RHOAI recommend (not require) SKILL.md for skill content? Or stay fully format-agnostic?

2. At what governance threshold should OCI packaging be applied? (e.g., only for Partner and Red Hat tiers? Only for skills entering production registries?)

3. How should multi-format skills be handled? (e.g., a skill available as both SKILL.md and a Python package — same registry record or separate?)

4. Should RHOAI define a custom `artifactType` for OCI skill artifacts? (e.g., `application/vnd.redhat.ai.skill.v1`)

5. What tooling should RHOAI provide for skill creation and packaging? (CLI tool, VS Code extension, templates?)
