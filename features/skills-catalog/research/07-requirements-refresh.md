---
title: "Skills Catalog research -- requirements refresh"
description: Updates 04-requirements with initial content list questions, partner verification program (NVIDIA 8-stage pipeline, JFrog registry), installation UX decision (7 methods, OCI artifacts proposal), skill card/eval standardization, signature verification architecture (Sigstore/in-toto), marketplace syndication (8 marketplaces, ARD spec), metadata governance (inherent vs external split), and EU AI Act Article 50 enforcement (Aug 2 2026, 3 days away).
timestamp: 2026-07-30
lens: requirements
review_after: 2026-10-30
supersedes_context: "Updates 04-requirements (2026-07-23) with initial content list, partner verification, installation UX, skill cards, evaluations, signature verification, marketplace syndication, and metadata governance requirements"
---

# Skills Catalog research -- requirements refresh

## 1. Initial content list requirements

Ann Marie Fred's architectural strategy GDoc surfaces the first concrete
content question: "What is the initial list of skills that we intend to
have in our Catalog? See also: catalog.redhat.com/en/ai/skills -- will
these lists be the same?" Catherine Weeks asks who defines what goes into
the public domain. Ann Marie confirms Peter Double handles partnerships.

The 04-requirements doc established 15-20 skills across 4 categories as
minimum viable content. The new questions refine this:

- **Overlap with catalog.redhat.com/en/ai/skills**: These are the
  Summit 2026 subscription-backed skill packs. The Skills Catalog should
  surface these but is not limited to them -- community and partner
  skills expand the catalog beyond what ships on catalog.redhat.com.
- **Public domain decision authority**: Peter Double for partnerships,
  but the decision of which RH-authored skills enter the public catalog
  vs remain subscription-only needs a formal owner (RHAISTRAT-1940 PM
  gap persists).
- **Trusted repos pipeline**: Ann Marie flags that a Konflux-based
  trusted repos pipeline for ingesting partner content is "not yet
  planned -- epic-sized." This is a 3.7+ dependency, not 3.6.

Cold-start evidence from marketplace research reinforces the 04 finding:
marketplaces that skip single-player utility and jump to empty
two-sided marketplaces fail 4x more often. Cap synthetic/placeholder
supply at 30%, convert to real supply within 60 days.

## 2. Partner verification program

NVIDIA's Verified Agent Skills (launched May 22, 2026) is the reference
implementation. Their eight-stage pipeline: source repository, human and
automated review, SkillSpector security scanning, evaluation, skill card
generation, cryptographic signing, cataloging, daily sync.

**Requirements for a verified partner skill** (from Ann Marie's doc):
permissive OSS license, skill card, signed in-toto attestation, security
scans completed, optionally evaluations, published to a public repo with
restricted update access. RH could run verification for partners as a
value-add service.

**Landscape context**:
- SkillSpector scans 68 vulnerability patterns across 17 categories
  including agent-specific risks (prompt injection, trigger abuse,
  excessive agency, tool poisoning). Grounded in OWASP LLM Top 10 and
  MITRE ATLAS. Open source, Apache-licensed.
- Snyk's Feb 2026 audit: 3,984 skills scanned, 36.8% had at least one
  security flaw, 13.4% critical. "Agent Skills in the Wild" (Liu et al.)
  across 42,447 skills: 1 in 4 has a real vulnerability, 1 in 20
  appears intentionally malicious.
- JFrog launched Agent Skills Registry as part of AI Catalog -- stores
  skill bundles in Artifactory, scans on upload, enforces approval
  workflows, integrates with NVIDIA NemoClaw runtime. JFrog is the
  enterprise governance reference.
- SkillCheck (independent): validates against the agentskills.io spec
  with OWASP Agentic Top 10 checks, CI-gateable via GitHub Actions.
- Workday Agent Passport: tests agents against OWASP LLM Top 10, NIST
  AI RMF, MITRE ATLAS before production deployment.

**Red Hat differentiation opportunity**: Publish Tekton pipelines and
GitHub Actions for partners to run verification in their own CI/CD
(Ann Marie's doc). This avoids the JFrog lock-in model while providing
the same trust guarantees. Konflux integration is the natural home.

## 3. Installation UX requirements

Ann Marie's doc identifies seven installation methods: git clone+copy,
marketplace.json, npx skills add, APM, LOLA, oras (OCI), MLflow CLI.
Strategic requirement: don't prevent any method; choose one for RH
automation; guarantee via E2E testing.

**Landscape context for each method**:

| Method | Status (July 2026) | Notes |
|---|---|---|
| git clone + copy | Universal baseline | Works everywhere, disconnected-friendly |
| marketplace.json | Harness-specific | Claude Code, Cursor native format |
| npx skills add | De facto standard | 20K+ GitHub stars, 27+ agents, 410K+ installs |
| APM | Agent-specific | Requires harness plugin support |
| LOLA | At risk | No active maintainers as of July 2026 (Ann Marie) |
| oras pull (OCI) | Emerging spec | Draft 0.1.0, Red Hat's strongest differentiation |
| MLflow CLI | Registry-coupled | Bill Murdock: MLflow has agent eval capabilities |

**OCI artifacts as distribution**: The OCI proposal (Thomas Vitale,
April 2026) specifies packaging skills as OCI artifacts, distributing
via any OCI-compliant registry (Harbor, Zot, GHCR, Quay). Key
properties: registry-agnostic, content-addressable, signable via
Cosign/Sigstore, minimal client burden (ORAS CLI sufficient). Reference
implementations exist (Arconia CLI, skills-oci, skillctl, KitOps).

**Recommendation**: For 3.6 TP, instructional UX remains correct (04
finding holds). For 3.7+, OCI artifact distribution via Quay is the
Red Hat-native path and maps to existing disconnected infrastructure
(oc-mirror, Quay). LOLA should be deprioritized given maintainer risk.

## 4. Skill card requirements

NVIDIA's skill card is the reference implementation but is not yet
standardized. Contents: publisher, license, known risks, outputs/work
products, evaluations per harness, dependencies, verification status.

**Landscape context**:
- NVIDIA released a skill card template and generator for community
  adoption. Machine-readable format enables automated policy enforcement
  (e.g., reject skills calling unapproved external APIs).
- Skilldex (academic) adds compiler-style conformance scoring against
  the agentskills.io spec with line-level diagnostics.
- No cross-vendor standard exists yet. The card format is NVIDIA's
  de facto standard but not governed by agentskills.io or any
  standards body.

**Catalog display requirement**: The catalog should display skill card
information (Ann Marie's doc). For 3.6 TP, this means rendering
available card fields in the detail view. For 3.7+, ingesting
machine-readable cards from partner submissions.

## 5. Skill evaluation requirements

NVIDIA runs evaluations in CI/CD and publishes results in skill cards:
trigger accuracy, task completion rate, token efficiency per harness.
Current datasets are "extremely small" -- more like functional tests
than robust evaluations (Ann Marie's doc, citing Bill Murdock).

**Landscape context**:
- SkillsBench (Feb 2026): the benchmark for measuring skill efficacy.
  Paired evaluation (vanilla vs skills-augmented). Key finding already
  captured in 04: curated +16.6pp, focused 2-3 modules best.
- "Agent Skill Evaluation and Evolution" survey (Jun 2026): identifies
  four evolution paradigms (execution feedback, trajectory distillation,
  compression, RL) and six benchmark categories.
- Anthropic's skill-creator (Mar 2026): added evals, A/B testing, and
  benchmark mode -- pass rate, elapsed time, token usage per eval set.
- Enterprise evaluation requires dual metrics: trajectory (how the
  agent reasons) + outcome (does it complete the task).
- Skill developers must provide test sets (Bill Murdock). Minimum: 3-5
  representative queries covering should-trigger, should-not-trigger,
  and edge cases.

**Requirement**: For 3.6, evaluations are metadata-only (display scores
if available, no runtime evaluation). For 3.7+, define a standard eval
format that skill authors submit alongside SKILL.md. Align with
SkillsBench methodology where possible.

## 6. Signature verification architecture

Ann Marie's doc outlines a three-step progression: (1) CLI validation
tool, (2) agent images that automate install + validation, (3) disable
non-verified installation. NVIDIA signs the skill/card/eval/benchmark
tuple as a unit.

**Landscape context**:
- NVIDIA uses the OpenSSF Model Signing standard with detached
  `skill.oms.sig` covering every file in the skill directory.
- Sigstore (Cosign + Fulcio + Rekor) is the dominant signing
  infrastructure. Keyless signing via OIDC tokens from CI providers.
  Short-lived certificates, transparency log.
- In-toto attestation framework: signed JSON binding claims to
  artifacts via cryptographic hashes. SLSA Provenance is the most
  deployed predicate type. Cosign has native in-toto support.
- OCI Distribution Spec v1.1 Referrers API enables Cosign signatures
  and in-toto attestations as first-class OCI metadata.

**Red Hat alignment**: Cosign/Sigstore is already the Red Hat signing
infrastructure for container images. Extending to skill artifacts via
OCI distribution creates a unified trust chain: same tools, same
transparency log, same verification workflow. This is the strongest
technical argument for OCI artifact distribution of skills.

**Requirement for 3.6**: Display signing status in catalog UI (signed
vs unsigned badge). Verification is informational, not enforced.
**3.7+**: CLI verification tool, admission policy integration,
enforcement mode.

## 7. Marketplace syndication requirements

Ann Marie's doc: follow NVIDIA's lead -- get RH skills listed in
Skills.sh, Codex plugin, Claude Code plugin, ClawHub, Hermes Hub.

**Landscape context**:
- 8 major marketplaces exist (up from 1 in Dec 2025). Expected to
  consolidate to 3-4 dominant platforms within a year.
- Skills.sh (Vercel): 83,627 skills, 8M+ installs, 18 agents supported.
  De facto package manager via `npx skills`.
- SkillsMP: 1.5M+ indexed skills (largest by catalog size).
- Multi-marketplace syndication is the winning strategy: publish the
  same capability across 4+ marketplaces with platform-specific tuning.
- Google's Agentic Resource Discovery (ARD) spec (Jun 2026): an open
  protocol for publishing/discovering AI capabilities via
  `ai-catalog.json` at `/.well-known/`. Co-authored with Microsoft and
  Hugging Face, backed by Amazon, Cisco, GitHub, Salesforce, Snowflake,
  NVIDIA. V0.9 draft, adoption currently near zero.

**Red Hat opportunity**: Publishing an `ai-catalog.json` on
catalog.redhat.com is low-cost and positions RH as an early ARD
adopter. Syndication to Skills.sh and the Codex/Claude Code plugin
directories reaches the developer audience directly.

**Requirement**: Syndication is a 3.7+ concern. For 3.6, focus on the
catalog itself. Post-3.6, define a syndication pipeline that publishes
skill metadata to at minimum Skills.sh and the ARD format.

## 8. Metadata governance requirements

Roland Huss challenges the content/metadata split (Ann Marie's doc).
The question: which metadata lives where? Inherent metadata (version,
trigger, name) in frontmatter vs external metadata (signature, eval
scores, verification status) in registry. Skills are "more like tar
files than markdown files" -- SKILL.md + supporting markdown + scripts.
Bundle = tar of tars.

**Landscape context**:
- Academic taxonomy (ResearchGate, 2026): four-layer skill anatomy --
  declarative, interface, execution, metadata. Five distribution models:
  Open Marketplace, Enterprise Bundle, SDK-Bundled, Self-Hosted,
  Hybrid Overlay.
- Skilldex proposes the "skillset" abstraction: bundled collection of
  related skills with shared assets enforcing cross-skill behavioral
  coherence.
- JFrog stores skill bundles as Artifactory artifacts with
  project-scoped approval and versioning.
- OCI artifact spec naturally separates content (the artifact blob)
  from metadata (OCI manifest annotations, Referrers for signatures
  and attestations).

**Recommendation**: The OCI model resolves Roland's challenge cleanly.
Inherent metadata (SKILL.md frontmatter, skill card) lives inside the
artifact. External metadata (signatures, attestations, eval scores,
verification status) attaches via OCI Referrers API. The catalog
aggregates both into its display. This separation maps to Red Hat's
existing container image governance model.

## 9. EU AI Act Article 50 -- enforcement imminent

Article 50 transparency obligations take effect August 2, 2026 -- three
days from this writing. The 04 doc flagged this; the requirement is now
urgent rather than upcoming.

Key enforcement details:
- Applies to ALL AI systems interacting with people, not just high-risk.
- Open-source AI systems are NOT exempt from Article 50.
- Fines up to 15M EUR or 3% of worldwide annual turnover.
- AI agents explicitly in scope: "where a provider can't reliably
  predict whether an agent will interact with a human, the safer path
  is to disclose its nature whenever plausible."
- Transitional period: systems on-market before Aug 2 get until Dec 2
  2026 for machine-readable marking (Article 50(2)).

**Catalog requirement**: Skill cards should include an
`eu_ai_act_scope` field indicating whether the skill generates
user-facing outputs that trigger Article 50 disclosure. This is
metadata the catalog can display and that enterprise policies can
filter on.

## Key findings

1. **Content list is the open question**: Who decides what enters the public catalog vs subscription-only remains unresolved. RHAISTRAT-1940 PM gap persists as the top risk.
2. **Partner verification has a reference architecture**: NVIDIA's 8-stage pipeline + SkillSpector + skill cards. Red Hat should publish Tekton pipelines for partners rather than building a proprietary gate.
3. **Installation UX: OCI is the strategic path**: Seven methods exist; OCI artifact distribution via Quay is Red Hat's strongest differentiation and maps to existing disconnected infrastructure. LOLA has maintainer risk.
4. **Skill cards are de facto but not standardized**: NVIDIA owns the reference implementation. Catalog should display card data from 3.6 TP onward.
5. **Evaluation is metadata-only for 3.6**: Runtime evaluation is 3.7+. Minimum eval format: 3-5 queries per skill covering trigger/no-trigger/edge.
6. **Signature verification maps to existing Sigstore infra**: Cosign + in-toto + OCI Referrers = unified trust chain with container images. Display-only for 3.6, enforcement for 3.7+.
7. **Marketplace syndication is 3.7+ but ARD is worth watching**: Google's ARD spec (v0.9) has major backers but near-zero adoption. Low-cost `ai-catalog.json` on catalog.redhat.com is a positioning move.
8. **OCI resolves the metadata governance debate**: Inherent metadata inside the artifact, external metadata (signatures, evals) via Referrers API. Maps to Red Hat's existing container governance model.
9. **EU AI Act Article 50 is 3 days away**: Skills generating user-facing outputs are in scope. Catalog metadata should flag this. Open-source is not exempt.
