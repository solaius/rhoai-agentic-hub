---
type: fact
title: deploymentModel is a customProperty with a parsing gap
description: deploymentModel is a kubeflow/hub customProperty (not typed) with a parsing gap -- agent.yaml top-level key silently ignored by the Go struct; only 2/15 kits set it (langflow flow-import, openclaw config-driven); config-driven and flow-import are fundamentally different deploy mechanisms (container vs platform-instance import).
timestamp: 2026-07-24
tags: [agent-catalog, metadata, schema, deploy, customProperties]
review_after: 2026-10-24
---
Verified against kubeflow/hub source (PR #2907, entity_mappings_agent.go,
property_options.go):

- `deploymentModel` is NOT in the typed field set (`name, source_id,
  displayName, description, readme, framework, labels, logo,
  repositoryUrl, env, artifacts`). It appears in filter_options as
  `deploymentModel.string_value` -- the `.string_value` suffix is the
  definitive marker of a customProperty (the `FullName` method appends
  it only when `IsCustomProperty = true`).
- **Parsing gap**: agent.yaml files in agentic-starter-kits set
  `deploymentModel: flow-import` as a top-level YAML key, but the Go
  struct `yamlAgent` has no `DeploymentModel` field -- Go's YAML
  unmarshaller silently ignores it. To reach the API, it must be in the
  `customProperties:` block with MetadataValue structure. The production
  metadata image resolves this (the filter_options response returns real
  data), but the starter-kits repo's top-level placement is inconsistent
  with the parser and a new contributor following the pattern would
  silently lose the field.
- Only 2 of 15 kits set it: langflow (`flow-import`), openclaw
  (`config-driven`). The other 13 omit it (implicitly config-driven).

**Semantics**:
- `config-driven` = standalone container (Dockerfile, FastAPI on port
  8000, agent-card, env-var config). Deploys via OpenShell Go SDK /
  AgentSandbox CR. The 3.6 reference path.
- `flow-import` = portable flow definition imported into a pre-existing
  platform instance (Langflow). No standalone container, no port 8000.
  Infrastructure-level env vars (POSTGRES_USER, etc.) instead of agent
  env vars (API_KEY, MODEL_ID). Completely different deploy mechanism.

See
[research doc 06](/features/agent-catalog/research/06-requirements-deployment-model-metadata.md)
for full analysis and the 3.6 contract recommendation.
