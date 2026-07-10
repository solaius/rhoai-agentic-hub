---
type: fact
title: Stakeholder map — supporting cast
description: Names, roles, and one-line context for roughly 80 people mentioned once or twice in the old registry, grouped by area, who didn't warrant a standalone person entry.
timestamp: 2026-07-06
tags: [platform, stakeholders, people]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §11, §13 (as of 2026-07-05)
---
Grouped rather than given individual `person-` entries — see the R2 batch 4 MANIFEST for the split criterion (recurring/cross-referenced/authored-artifact/signatory/workstream-lead → individual; single-mention role tag → here). For the ~29 people who cleared that bar, see the `person-*.md` entries across each feature's `knowledge/`. Peter Double (owner of this whole initiative) is deliberately excluded from both this map and the individual entries — see the manifest.

### MCP Gateway & ecosystem engineering
| Name | Role/Area | Notes |
|---|---|---|
| Andrew Block | MCP Gateway on OpenShift | |
| Andrew Mackenzie | MCP Gateway delivery/packaging | Flagged the OCP 5.0 deployment plan as urgently needing to be nailed down — see [question-ocp5-olm-dependency-removal.md](/features/platform/knowledge/question-ocp5-olm-dependency-removal.md) |
| Craig Brookes | MCP Gateway engineering | |
| David Martin | MCP Gateway verification/testing | |
| Matthias Weßendorf | Gen MCP engineering | |
| Nader Ziada | Gen MCP engineering (ex-Knative Serverless) | |
| Shane Utt | Guardrails | |
| Jose Gonzalez | Partnership Ecosystem (under Matt Dorn); partner MCP containerization | Manually adapted partner containers for 3.4 (rebase to UBI, labels, licenses) |
| waldirio | Field | Participated in an MCP implementation troubleshooting thread |

### MCP Registry / data model (PM & engineering)
| Name | Role/Area | Notes |
|---|---|---|
| Jon Burdo | Product Management | Connected the certification-allowlist question to RHAIRFE-294 |
| Chris Hambridge | Product Management | With Matt Prahl, raised whether MCPLO should create read-only "discovered/managed" entries — see [question-mcp-registry-state-propagation.md](/features/mcp-registry/knowledge/question-mcp-registry-state-propagation.md); also does 3.4 catalog integration/testing |
| Ju Lim | Product Management — RHOAI | |
| Mrunal Patel | MCP Server deployment/OCP integration | Position: MCP servers register post-Gateway install; ideally Gateway install is part of RHOAI |
| Matt Prahl | MLflow/Registry engineering (data model) | Co-raised the MCPLO governance-interaction question with Chris Hambridge |
| Dan Kuc | MLflow/Registry engineering | Two positions: MLflow's None/Staging/Production/Archived lifecycle states may need expansion; MCP's flow seems opposite to the model registry's (registry-first vs. catalog-first) |
| Alessio | Kubeflow plugin architecture | Genericizing the model-registry asset-type model (PR #2219) — see [fact-model-registry-kubeflow-hub.md](/features/platform/knowledge/fact-model-registry-kubeflow-hub.md) |
| Edson Tirelli | Agents/Skills | |
| Hunter Gerlach | Consulting use cases | |

### Partnership Ecosystem
| Name | Role/Area | Notes |
|---|---|---|
| Adam Bellusci | Leadership — Registry/Catalog direction | Source of the "MLflow is for registries. Kubeflow is for catalogs. We're done." framing in [decision-registry-vs-catalog.md](/features/platform/knowledge/decision-registry-vs-catalog.md) |
| Ann Murray | Pushing Snyk for AI/agent scanning | See [fact-mcp-ingestion-pipeline.md](/features/mcp-ecosystem/knowledge/fact-mcp-ingestion-pipeline.md) |
| Serob | Partnership Engineering — ingestion pipeline pieces | |
| Katie Giglio | Partner consent letters and outreach coordination | Ran the consent process for the 3.4 partner catalog |
| Tanya Heuze | Partner Ecosystem lead | |
| Hugo Rivero | Partner Ecosystem | Asked which metadata requirements are RHOAI-specific vs. part of the MCP spec |
| Paul Christensen | Partner Ecosystem — partner value proposition | |
| Alec Leschin | Business Development — partner curation, Oracle pipeline | |
| Ilan Pinto | Engineering — AI-driven SAST scanner | |
| Itamar Heim | Leadership (Partnership Ecosystem chain) | |
| Mike Evans | Leadership (Partnership Ecosystem) | |

### Marketing, messaging & comms
| Name | Role/Area | Notes |
|---|---|---|
| Ornkanya Sinonpat (Aom) | Product Marketing — blog timeline/editorial coordination for Summit | |
| Noel O'Connor | Sales/field | Raised the seller-confusion risk on IBM/RH agentic positioning — see [decision-ibm-redhat-agentic-ai-positioning.md](/features/platform/knowledge/decision-ibm-redhat-agentic-ai-positioning.md) |
| Jennifer Vargas | GTM/marketing | Warned that IBM owning "AI Governance"/"gateway" language in joint slides creates long-term seller-enablement risk — same decision as above |
| Jessie Beach | Media team — ecosystem blog writing | |
| Rosa Guntrip | PM/Marketing | Reviewed agentic messaging, suggested the 4-pillar structure — see [fact-agentic-ai-four-pillars.md](/narrative/knowledge/fact-agentic-ai-four-pillars.md) |

### Business development / ecosystem growth
| Name | Role/Area | Notes |
|---|---|---|
| Aaron Isom | Business Development — Azure contact facilitation | |
| Karl Eklund | Quickstart sponsorship and prioritization | |
| Swati Kale | Quickstart sponsorship | |
| John Gibson | Suggested Vast Data as a partner | |
| Roberto | Summit Agent Ops talk (with Younes Ben Brahim and Peter Double) | See [fact-summit-2026.md](/features/platform/knowledge/fact-summit-2026.md) |
| Roy Nissim | Co-founder of Jones, reports to Catherine Weeks | Observability, AI gateway exploration |

### RHOAI-RHCL agreement & support
| Name | Role/Area | Notes |
|---|---|---|
| Thomas Maas | Engineering Manager, RHCL | |
| Rutuja Argade | Support Manager, RHAI | Raised the OCP 4.20 upgrade-timing and ticket-workflow question — see [question-rhoai-rhcl-ocp419-gap.md](/restricted/features/mcp-gateway/knowledge/question-rhoai-rhcl-ocp419-gap.md) |
| Amana Juricic | Support Director, RHAI | Asked whether cross-team support/engineering troubleshooting scope is anticipated |
| Tomas Jochec | RHCL coordination | Driving signoffs on the support agreement |

### Field-reported MCP issues
| Name | Role/Area | Notes |
|---|---|---|
| Erwan Granger | Field/consulting | Raised the cluster-admin requirement concern — see [question-mcp-fernando-lozano-doc-gaps.md](/features/mcp-ecosystem/knowledge/question-mcp-fernando-lozano-doc-gaps.md) |

### AI Gateway F2F attendees (April 2026, Boston)
| Name | Role/Area |
|---|---|
| Nir Rozenbaum | Inference-gateway team; IPP plugin architecture, adaptive routing, model selection |
| Noy Itzikowitz | Inference-gateway team; IPP plugin optimization, API translation |
| Morgan Foster | Responses API implementation, Llama Stack decomposition, agentic loop design |
| Sébastien Han | Envoy/streaming requirements, Responses API proxy mechanics |
| Ben Browning | AI Gateway F2F attendee |
| Tyler Michael Smith | LLM-d, disaggregated serving (PD/EPD/AFD), rate limiting |
| Marius Danciu | AI Gateway F2F attendee |
| Yi Zheng | ITS Hub, Envoy re-entrance |
| Ben Bennett | AI Gateway F2F attendee |
| Sarah Coghlan | AI Gateway F2F attendee |
| Joe Fernandez | AI Gateway F2F attendee |
| Lindani Phiri | BEU tenancy strategy |
| Sam Batschelet | llm-d, adaptive routing implementation |
| Ann Marie Fred | Agent sandbox, OpenShell integration |

See [fact-ai-gateway.md](/features/platform/knowledge/fact-ai-gateway.md) and [decision-ai-gateway-f2f-architecture.md](/restricted/features/platform/knowledge/decision-ai-gateway-f2f-architecture.md).

### RICE rubric reviewers
| Name | Role/Area | Notes |
|---|---|---|
| Jenn Giardino | PM | RICE rubric reviewer, Confidence-score feedback |
| Dana Gutride | PM | RICE rubric feedback on single-team-effort scoring |
| William Caban | Engineering | Impact-scoring feedback (pain level, blocking, new market) |

See [person-arjay-hinek.md](/features/platform/knowledge/person-arjay-hinek.md) (rubric author).

### Agent memory — OCTO/ET workstream
| Name | Role/Area |
|---|---|
| Ben Capper | OCTO/ET Ireland; agent memory research (data lineage, persistent memory) |
| Ray Carroll | OCTO/ET; agent memory research, guardrails/governance perspective |
| Kateryna Romashko | OCTO/ET; agent memory research participant |

See [person-ryan-cook.md](/features/agent-memory/knowledge/person-ryan-cook.md) and [person-sanjeev-rampal.md](/features/agent-memory/knowledge/person-sanjeev-rampal.md) (workstream leads).

### Agent memory — Feast team & workstream participants
| Name | Role/Area |
|---|---|
| Amita Sharma | Feast team; strategy session participant |
| Nikhil Kathole | Feast team; strategy session participant |
| Nehanth Narendrula | Agent memory workstream; Mem0 investigation, deployed example on OpenShift AI |
| Isaiah Stapleton | Agent memory team; OpenClaw and memory systems |
| Khaled Sulayman | Agent memory workstream; memory scoping questions |

See [question-feast-mem0-pluggable-storage.md](/features/agent-memory/knowledge/question-feast-mem0-pluggable-storage.md).

### RHOAI restricted use entitlement for OpenShift / OLS
| Name | Role/Area | Notes |
|---|---|---|
| Joshua Wilson | Engineering, OLS | Raised the RHOAI restricted use entitlement pricing/paywall concern for OLS's MCP features — already captured in [ref-rhoai-limited-mcp-lifecycle-faq.md](/restricted/features/mcp-registry/knowledge/ref-rhoai-limited-mcp-lifecycle-faq.md) |

### Agent starter kits & base images
| Name | Role/Area | Notes |
|---|---|---|
| Nick Ommen | Engineering — agent starter kits | |
| Aakanksha Duggal | Engineering — agent starter kits; OpenCode starter kit scope | |
| Justin Sun | Engineering — container images for agent harnesses | |
| Doug Hellmann | Engineering | Raised the product ID, UBI version, and dependency questions — see [question-agentic-base-images-ubi-version.md](/features/agent-registry/knowledge/question-agentic-base-images-ubi-version.md) and [question-agentic-base-images-product-id.md](/features/agent-registry/knowledge/question-agentic-base-images-product-id.md) |
| Kamesh | Engineering — repo structure for starter kits | Suggested the omnigent meta-harness approach — see [ref-omnigent-repo.md](/features/agent-registry/knowledge/ref-omnigent-repo.md) |
| Adam Miller | Engineering — building Hummingbird agent image versions | |

### Docs & content strategy
| Name | Role/Area |
|---|---|
| Jennifer Ciroli | Content Strategist (RHOAI); docs strategy, content journeys, JTBDs |
| Donagh Brennan | Content Strategist (RHAII and Agentic) |
| Ignacio Lago | Product Operations; manages Lifecycle and Supported Configurations pages |

See [person-manuela-ansaldo.md](/features/platform/knowledge/person-manuela-ansaldo.md) (docs program lead).
