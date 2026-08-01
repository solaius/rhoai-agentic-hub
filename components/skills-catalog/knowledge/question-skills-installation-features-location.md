---
type: question
title: Where do skill installation features live -- catalog, registry, or both?
status: open
description: Open question needing its own STRAT -- skill installation could live in catalog (marketplace.json, npx), registry (APM, LOLA, mlflow CLI), or both. Different flows for catalog-sourced vs registry-sourced skills.
timestamp: 2026-07-30
tags: [skills-catalog, skills-registry, installation, packaging]
components: [skills-catalog, skills-registry]
source: Ramesh catalog-vs-registry GDoc TODO + Skills Registry/Catalog meeting 2026-07-23 + Ann Marie Fred architectural strategy GDoc (July 2026)
---

From Ramesh's catalog-vs-registry document: "We need to do more work to
decide whether it's better for the Skills Catalog or the Skills Registry
to offer skill-installation features." Marked as a TODO needing its own
STRAT.

**Current plan distribution**:

| Method | Where | Status |
|---|---|---|
| marketplace.json | Catalog plan | Planned |
| npx | Catalog plan | Planned |
| APM | Registry plan (RFC-0008 plugin) | In RFC |
| LOLA | Registry plan (RFC-0008 plugin) | In RFC |
| Git pull from source repo | Not our responsibility | N/A |
| Git pull from RHOAI-managed source | Catalog plan | Planned |
| mlflow CLI (calls APM/LOLA) | Registry plan | In RFC |
| oras pull (OCI artifact) | Neither -- manual | Possible |

**Full installer comparison** (from Ann Marie Fred's architectural
strategy, July 2026):

All methods below work today IF the final verified skill is in a Git
repo. OCI-only skills require `oras pull` which none of the standard
installers support yet.

1. **Git clone + copy** -- harness-specific commands to clone and copy
   into the config directory. Restart required. No additional tooling.
2. **Marketplace install** -- publish to `marketplace.json` on a Git
   server, install via harness command (e.g. `/plugin install
   skill@org`). No restart needed.
3. **npx skills add** -- community tool that hides harness differences.
   Supports multi-harness install (`--agent claude-code --agent codex`).
   Restart may be needed.
4. **APM (Microsoft)** -- `apm install org/skill` or manifest-based
   `apm install`. Hides harness differences. Databricks prefers this.
5. **LOLA (Red Hat)** -- `lola mod add <repo>; lola install <skill>` or
   manifest-based `lola sync`. No active maintainers as of July 2026;
   may be archived unless AAET commits.
6. **oras pull** -- extracts skill from OCI artifact to config
   directory. Only option for OCI-only distribution. Harness-specific.
7. **MLflow CLI extension** -- `mlflow skills-registry install
   --name <skill> --alias production --harness claude-code`. Calls out
   to LOLA/APM/npx. Also supports OCI and bundle install. Requires
   registry RFC merge.

**Strategic position** (Ann Marie): do not prevent users from using any
of these. Choose one for RH agent-deploying automation and guarantee it
via E2E testing. Which one is still an open design question.

**Complication**: if the catalog ships before the registry, catalog
needs its own install path. If both ship, users may need to install
from either source. Making skills always go through the registry before
install ("push to registry, then install from there") would unify the
path but adds friction.

Edson's comment: installation is orthogonal to governance needs.

Also feeds into how agent installation will happen.

**Related**: [ref-skills-architectural-strategy-gdoc](/components/skills-catalog/knowledge/ref-skills-architectural-strategy-gdoc.md)
