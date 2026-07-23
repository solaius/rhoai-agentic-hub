---
type: fact
title: Ann Marie's deploy-from-catalog POC proposal
description: POC plan — pre-built agent image + MLflow skill bundle (install-bundle from RFC PR #26) + env vars for model config + catalog deploy into OpenShell; co-engineering with ET; without RFC #26, init containers or per-combination image builds required.
timestamp: 2026-07-11
tags: [agent-catalog, poc, skills, mlflow, deploy-ux]
features: [agent-catalog, skills-registry]
source: Slack group DM Ann Marie/Andrew/Gage ~2026-07-11
review_after: 2026-10-11
---

Ann Marie Fred proposed co-engineering a POC with ET (~2026-07-11) for
the most complex deploy-from-catalog scenario:

1. **Pre-built agent image** that expects a skill bundle passed in a
   specified way.
2. **Environment variables** to configure model connection info (and
   skill bundle name, if RFC PR #26 lands).
3. **Agent catalog UX** where you select an image, select a skill
   bundle, select a model, and deploy into OpenShell.

**With MLflow skills RFC PR #26** (`mlflow skills install-bundle`):
the skill bundle name is just another env var; the pre-built image
runs `install-bundle` before starting the agent. Clean path.

**Without RFC PR #26**: a skills catalog alone is not very useful —
you'd need either:
- A new container image per harness + skill combination, or
- Init-container magic to replicate what `install-bundle` would do.

Ann Marie wants the POC to use the underlying MLflow technology
planned for catalog/registry, but acknowledged a POC could gloss over
that piece if needed. ET team is "not above vibe coding" a POC where
the registry is just a YAML file.

See [ref-mlflow-rfc-0008](/features/agent-registry/knowledge/ref-mlflow-rfc-0008.md)
for RFC PR #26 status.
