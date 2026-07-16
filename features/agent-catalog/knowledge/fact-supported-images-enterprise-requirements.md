---
type: fact
title: Enterprise requirements on supported images (air-gap, security, licensing)
description: Air-gapped segments prohibit runtime fetch outright (staleness debate resolves toward disconnected); supported images inherit Health Index/CVE/Konflux obligations; Claude Code redistribution is license-prohibited, Codex/Goose are Apache-2.0; EU AI Act transparency lands 2026-08-02.
timestamp: 2026-07-16
tags: [agent-catalog, requirements, disconnected, licensing, security]
features: [agent-interop]
review_after: 2026-10-16
source: 5-lens research sweep 2026-07-16 (04-requirements; adversarially verified)
---

From the [requirements research](/features/agent-catalog/research/04-requirements.md)
(evidence-graded, verified):

- **Air-gap resolves the staleness debate.** Regulated/air-gapped customers
  prohibit runtime fetching categorically — every image must be on the
  oc-mirror list, updates arrive on signed media, and stale-but-mirrored
  beats fresh-but-fetching. Self-contained images with self-update disabled
  are a hard requirement (OpenCode needs patch-level work — upstream issues
  #16117/#20027); "harnesses go stale in a month" is a demo problem, not an
  enterprise blocker.
- **Supported images inherit Red Hat's security machinery automatically**:
  Container Health Index A–F grading (staleness becomes externally visible),
  Critical/Important CVE fix policy, Konflux SBOM/SLSA/signing. This
  quantifies the cost behind
  [ownership-packaging](/features/agent-catalog/knowledge/question-agent-catalog-ownership-packaging.md)
  and sets the bar for the
  [AIPCC base images](/features/agent-catalog/knowledge/question-agent-catalog-aipcc-base-images-fit.md).
- **Licensing is fact, not risk**: Claude Code's license prohibits
  modification/redistribution (all-rights-reserved, Anthropic Commercial
  Terms); Codex CLI and Goose are Apache-2.0 — Codex is NOT proprietary
  (correcting the meeting-note assumption). The viable proprietary-harness
  pattern is BYOL/Containerfile (customer builds inside their firewall),
  which is also air-gap compatible.
- **Regulatory clock**: EU AI Act transparency obligations apply from
  2026-08-02 (one release cycle from 3.6); NIST AI RMF GV-1.6 + CSA's
  agentic profile expect per-agent accountability records — evidence for
  "deploy always registers, reconcile the rest" on the
  [register-vs-deploy question](/features/agent-catalog/knowledge/question-agent-catalog-register-vs-deploy.md).
- **Catalog trust is fragile** (Port 2025: 3% of engineers fully trust
  portal metadata) — card accuracy (dead links, wrong model claims) is a
  requirement, not polish.
