---
title: "Deployment model metadata — config-driven vs flow-import and the catalog-to-deploy contract"
description: The deploymentModel customProperty (config-driven / flow-import) is the unstated contract between catalog and deploy — it determines WHICH mechanism deploys an agent, not just HOW; currently a customProperty with a parsing gap, not a typed field.
timestamp: 2026-07-24
lens: requirements
review_after: 2026-10-24
---

# Deployment model metadata — config-driven vs flow-import

Focused requirements-lens refresh prompted by the real `filter_options`
response (intake 2026-07-23, from the
[#openshift-ai-hub-devs thread](/features/agent-catalog/knowledge/ref-slack-ai-hub-devs-filter-options-thread.md))
surfacing a `deploymentModel.string_value` dimension with values
`config-driven` and `flow-import`. Builds on the deep 5-lens sweep
(2026-07-16); inherits the standing context from
[04-requirements](/features/agent-catalog/research/04-requirements.md).

## 1. What config-driven and flow-import mean

Two fundamentally different deployment mechanisms coexist in the 3.5
catalog under one card surface:

**config-driven** (13 of 15 starter kits, implicit default). The agent
is a standalone container: Dockerfile, FastAPI surface on port 8000,
`/.well-known/agent-card.json`, env-var configuration (API_KEY, BASE_URL,
MODEL_ID). Deployment = build OCI image, push, create pod via OpenShell Go
SDK / AgentSandbox CR. This is the
[starter-kit deploy contract](/features/agent-catalog/knowledge/fact-agent-catalog-starter-kits.md)
and what Mode 2 (platform-owned deploy) in
[fact-agent-deployment-modes](/features/agent-catalog/knowledge/fact-agent-deployment-modes.md)
targets.

**flow-import** (1 of 15: Langflow Simple Tool Calling Agent). The agent
is NOT a container. It is a portable flow-definition JSON file designed
for import into a pre-existing Langflow server instance. The required
artifacts differ entirely: no Dockerfile, no FastAPI surface, no port
8000. Instead: a `flows/` directory with flow JSON, a `Makefile` driving
`deploy-local.sh` (which starts a multi-container stack: Langflow server +
PostgreSQL + Langfuse + ClickHouse + MinIO + Redis), and infrastructure-
level env vars (POSTGRES_USER, LANGFUSE_ADMIN_PASSWORD) instead of the
standard agent env vars. The user imports the flow JSON into the Langflow
UI, not the platform's deploy wizard.

A second kit, OpenClaw, explicitly sets `deploymentModel: config-driven`.
The remaining 12 kits omit it entirely (implicitly config-driven by
directory structure).

**The distinction is not cosmetic.** config-driven agents deploy through
the OpenShell SDK pipeline (the 3.6 reference architecture in
[03-architecture](/features/agent-catalog/research/03-architecture.md) S3).
flow-import agents require a completely different mechanism: provision or
locate a Langflow instance, import the flow definition, configure the
instance's infrastructure env vars. The deploy wizard would need to
branch its entire UX and backend path based on this value.

## 2. Where deploymentModel lives in the schema

**It is a customProperty, not a typed field.** Verified against
kubeflow/hub source:

- PR #2907 (merged 2026-07-03) established the typed field set:
  `name, source_id, displayName, description, readme, framework, labels,
  logo, repositoryUrl, env, artifacts`. The Go struct `yamlAgent` in
  `catalog/internal/catalog/agentcatalog/yaml_provider.go` has no
  `DeploymentModel` field. The `agentProperties` map in
  `entity_mappings_agent.go` registers only the typed fields at
  `filter.PropertyTable` location.
- The `.string_value` suffix in the filter_options response key
  (`deploymentModel.string_value`) is the definitive marker: the
  `FullName` method in `property_options.go` appends the value-type
  suffix only for properties with `IsCustomProperty = true`. Typed
  fields (like `framework`) appear without suffix.
- No kubeflow/hub issue or PR proposes promoting `deploymentModel` to
  a typed field; no deployment-related metadata discussion exists
  upstream.

**Parsing gap.** The agentic-starter-kits agent.yaml files set
`deploymentModel: flow-import` as a top-level YAML key. But the
kubeflow/hub `yamlAgent` struct has no matching field — top-level keys
without a struct field are silently ignored by Go's YAML unmarshaller.
For the value to reach the catalog API, it must be placed in the
`customProperties:` block using the MetadataValue structure:

```yaml
customProperties:
  deploymentModel:
    metadataType: MetadataStringValue
    string_value: "flow-import"
```

The real filter_options response does return `deploymentModel.string_value`
with data, so either the production metadata image resolves this
differently (baked metadata processing outside the YAML parser path), or
the agent.yaml files in the downstream build have the correct
customProperties structure. Either way, the starter-kits repo's top-level
placement is inconsistent with how the backend would naturally consume it,
and a new kit contributor following the existing pattern would silently
lose the field.

## 3. Does the 3.6 deploy path need this as a typed contract?

**For 3.5 (no deploy): no.** As a customProperty, `deploymentModel`
appears in filter_options and can power sidebar filtering. Users who
filter to `flow-import` see Langflow; users who filter to `config-driven`
see standard agents. The card links out to GitHub either way. This is
sufficient.

**For 3.6 (deploy path): the question is WHERE the deploy mechanism reads
it.**

*Option A: consume from the artifacts endpoint.* The agent.yaml is
already served raw via `GET /agents/{id}/artifacts` (PR #2928, the
`template-artifact` JSON-encoded string). The BFF can parse the raw
agent.yaml and branch on `deploymentModel` without needing it as a typed
catalog field. This avoids an upstream schema change and mirrors how the
deploy wizard already reads env-var metadata from the artifact.

*Option B: promote to a typed field.* This requires an upstream PR to
kubeflow/hub adding `deploymentModel` to the OpenAPI schema, Go struct,
entity mappings, and datastore entry. The benefit: the catalog list/detail
API exposes it without a second artifacts fetch, and filtering on it uses
the simpler `deploymentModel = "config-driven"` syntax instead of
`deploymentModel.string_value = "config-driven"`. The cost: upstream
governance (kubeflow/hub is Red Hat-maintained but follows upstream
contribution norms).

*Option C: leave as customProperty, improve parsing.* Add a handler in
the YAML provider that maps top-level `deploymentModel` to
customProperties automatically (or document the `customProperties:` block
as the canonical location in the adding-a-new-agent guide). No schema
change, but filtering retains the `.string_value` suffix syntax.

**Recommendation: Option A for 3.6 EA1, evaluate Option B for GA.**

- The deploy wizard already fetches the artifact (agent.yaml) to read
  env-var metadata; reading `deploymentModel` from the same payload adds
  zero cost.
- For EA1, only one kit is `flow-import` (Langflow); the deploy wizard
  can reasonably descope flow-import support and deploy only config-driven
  agents, sidestepping the branching question entirely.
- If flow-import (or future deployment models like `helm-chart`,
  `operator-managed`) grows to >2 kits and the catalog list view needs
  deployment-model-aware badges or actions, promotion to a typed field
  becomes justified. That's a GA decision, not an EA1 one.

## 4. How deploymentModel maps to Mode 1 / Mode 2

From the [packaging meeting framework](/features/agent-catalog/knowledge/fact-agent-deployment-modes.md):

| Packaging mode | deploymentModel | Deploy mechanism |
|---|---|---|
| Mode 2 — platform-owned | config-driven | OpenShell Go SDK -> AgentSandbox CR -> pod (the 3.6 reference path) |
| Mode 2 — platform-owned (visual builder) | flow-import | Provision/locate Langflow instance, import flow JSON, configure infrastructure (NO OpenShell path) |
| Mode 1 — bring your own | n/a | User deploys their own image; platform attaches sidecars. Catalog does not drive deploy. |

`flow-import` is a **Mode 2 variant**, not a third mode: the platform
still owns the deploy, but the mechanism is "import into a managed
platform service" instead of "create a standalone container." This maps
to a pattern visible in the broader ecosystem: Google's Agent Garden
distinguishes "pre-built agents" (deploy as container) from
"Google-hosted agents" (activate within Vertex AI) — same discovery
surface, different deploy backend.

The implication for the catalog-to-deployments contract gap (Gage:
"there is no catalog to deployments") is that the contract is not just
"what metadata does the deploy wizard need" but "which deploy backend
does this agent use." `deploymentModel` is the routing key.

## 5. Catalog-to-deployments: typed field or artifacts endpoint?

The catalog-to-deployments gap is real (Gage confirmed: "there is no
catalog to deployments" for 3.5, and catalog vs. deployments-list
requirements are separate). For 3.6, the deploy wizard needs:

1. **Routing key**: which deploy mechanism to use (config-driven vs
   flow-import vs future modes). Source: `deploymentModel` in agent.yaml.
2. **Container contract**: port, agent-card path, user, env vars. Source:
   agent.yaml via the artifacts endpoint.
3. **Image reference**: which supported image to deploy. Source: not yet
   in agent.yaml — the current schema has no image-reference field; the
   supported-images program
   ([decision-agent-catalog-deploy-supported-images-only](/features/agent-catalog/knowledge/decision-agent-catalog-deploy-supported-images-only.md))
   implies the platform maps framework -> image, not the kit author.
4. **Env-var declarations**: what the user must configure. Source:
   `env` field in agent.yaml (already typed in the schema).

Of these, only (4) is already a typed field. (1) is a customProperty,
(2) comes from the artifact, and (3) is not in the schema at all. The
artifacts endpoint is the natural carrier for all of them — it serves
the raw agent.yaml, which can grow fields without upstream schema
changes. The typed catalog schema stays clean (discovery/filtering
fields), and the artifacts endpoint carries the deploy contract
(operational fields).

This is consistent with the broader pattern in kubeflow/hub: the
Model Catalog separates model metadata (typed, filterable) from model
artifacts (operational, served via a dedicated endpoint).

## Candidate knowledge atoms

- **fact**: `deploymentModel` is a kubeflow/hub customProperty (not a
  typed field) with a parsing gap — agent.yaml files set it as a
  top-level YAML key that the backend's Go struct silently ignores;
  it reaches the API only through the customProperties block or
  baked metadata processing. Only 2 of 15 starter kits set it
  explicitly (langflow: `flow-import`, openclaw: `config-driven`).
- **fact**: `config-driven` and `flow-import` are fundamentally different
  deploy mechanisms: config-driven = standalone container via OpenShell
  SDK (the 3.6 reference path); flow-import = portable flow definition
  imported into a pre-existing platform instance (Langflow), requiring
  no standalone container and a completely different infrastructure
  env-var pattern.
- **question**: should the 3.6 deploy wizard support flow-import agents,
  or descope to config-driven only for EA1? Supporting flow-import
  requires a second deploy backend (provision/locate a Langflow
  instance + import flow JSON) alongside the OpenShell container path.

## Sources

1. kubeflow/hub PR #2907 — agent schema rationalization, typed vs
   customProperties boundary
   (https://github.com/kubeflow/hub/pull/2907)
2. kubeflow/hub `entity_mappings_agent.go` — agentProperties map
   (typed field registration)
3. kubeflow/hub `property_options.go` — FullName method
   (customProperty suffix logic)
4. agentic-starter-kits PR #247 — metadata additions, deploymentModel
   not added
   (https://github.com/red-hat-data-services/agentic-starter-kits/pull/247)
5. agentic-starter-kits `adding-a-new-agent.md` — config-driven vs
   flow-import directory structure documentation
6. agentic-starter-kits `langflow-simple-tool-calling-agent/` — flow
   JSON, deploy-local.sh, podman-compose stack
7. kubeflow/hub PR #2928 — artifacts endpoint serving raw agent.yaml
   (https://github.com/kubeflow/hub/pull/2928)
