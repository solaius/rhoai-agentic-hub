---
type: decision
title: Catalog deploy restricted to platform-built (supported) images
description: 2026-06-01 packaging meeting — the deploy MVP only deploys images Red Hat builds (Mode 2); Mode 1 bring-your-own is documentation-only at first; proprietary harnesses ship as Containerfiles.
decided: 2026-06-01
timestamp: 2026-07-16
tags: [agent-catalog, packaging, modes]
features: [agent-interop]
---

**Context.** The packaging meeting (2026-06-01) worked through what an agent
package is and who can deploy what. Deploying customer-supplied images means
the platform can't guarantee entry points, env-var contracts, or that the
thing works at all (Ann Marie Fred: clone + edit the repo and you're in
Mode 1 — a dev-lifecycle problem, Backstage's job, not the catalog's).

**Decision.** The catalog's deploy MVP deploys only images the platform team
builds ("validated" then, renamed
[supported 2026-07-10](/features/agent-catalog/knowledge/decision-supported-not-validated-images.md))
— starter-kit images built to behave like Mode 2 plus off-the-shelf harness
images with known entry points. Mode 2 (platform-owned deployment) is the
default; Mode 1 (bring-your-own) is served by documentation and GitHub links
initially. Harnesses that can't be redistributed (e.g. Claude Code) ship as
Containerfiles the customer builds.

**Consequences.** Building/maintaining supported images becomes the critical
path for deployment (originally 3.5, now 3.6 per the
[no-deploy-in-3.5 decision](/features/agent-catalog/knowledge/decision-agent-catalog-no-deploy-35.md));
ownership of that packaging is
[still open](/features/agent-catalog/knowledge/question-agent-catalog-ownership-packaging.md);
the UI deploy path stays stable while the backend (BFF → OpenShell) evolves.
Mode definitions: [fact-agent-deployment-modes](/features/agent-catalog/knowledge/fact-agent-deployment-modes.md).
