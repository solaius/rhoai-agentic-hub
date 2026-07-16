---
type: decision
title: 3.5 catalog field set finalized
description: Field-finalization 2026-07-02 (+ spec-doc comments) — drop agent-type; optional "tested models"; deploy button detail-page only; capabilities cut; multi-value "communication protocol"; RH-curated labels/logo via agent.yaml.
decided: 2026-07-02
timestamp: 2026-07-16
tags: [agent-catalog, metadata, schema, 3.5]
---

**Context.** The dashboard team needed a frozen OpenAPI spec before coding;
Yabbes Rajan's design walkthrough (2026-07-02, with Adel Zaalouk, Alessio
Pragliola, Luca Giorgi, Peter Double) settled each field against what
actually exists in the starter kits' agent.yaml. Follow-through in Alessio's
[3.5 spec finalization doc](/features/agent-catalog/knowledge/ref-agent-catalog-35-spec-finalization-gdoc.md)
comments (to 2026-07-06).

**Decision.**
- **Drop "agent type"/"category"** — Red Hat imposes no agent taxonomy;
  labels do the job.
- **"Tested models"** — optional, informational display name of models a kit
  was tested with; never "validated"/"verified"; actual model binding happens
  at deploy time via env var. (Supersedes the 2026-06-30 Slack call to drop
  the models section outright.)
- **Deploy button on the detail page only** (when it arrives) — consistent
  with the other catalogs' card views.
- **Capabilities cut from the template catalog** — capabilities are runtime
  data from the A2A agent card on deployed agents; template metadata exists
  for findability/filtering, the README carries understanding.
- **"Communication protocol"** (renamed from protocol), multi-value,
  comma-separated. Exact semantics (protocol you speak to the agent vs
  protocols it uses) still to be defined — open follow-up, together with
  "tools".
- **Labels + logo from agent.yaml**, RH-curated at build time (no
  customer-editable template metadata in 3.5; custom labels land on
  deployments); placeholder SVG when a logo is missing; missing fields
  render "N/A" (model-catalog precedent).
- **agent.yaml gaps fixed at source** — kits missing agent.yaml (claude-code,
  openclaw) get one; contributors write the yaml, the dashboard team (via
  Gage Krumbach) has the strongest say on format.

**Consequences.** OpenAPI spec merged 2026-07-03 (kubeflow/hub #2907), BFF
work unblocked; tested-models data requires asking each kit's contributors
(declaring it becomes part of template contribution); protocol/tools
semantics and the tags-taxonomy + logo-artwork owner remain open.
