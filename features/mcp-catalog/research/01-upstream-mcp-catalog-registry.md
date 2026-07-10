---
title: "Upstream — MCP catalog/registry ecosystem (July 2026)"
description: State of the official MCP registry (preview, v0.1, ≥36K records), AAIF governance, the 2026-07-28 spec RC, subregistry federation model, Kubeflow Hub's MCP Catalog, and k8s-native MCP management projects.
timestamp: 2026-07-09
lens: upstream
review_after: 2026-08-15
---

# Upstream — MCP catalog/registry ecosystem (July 2026)

Research run 2026-07-09 (`hub.research mcp-catalog upstream competitive`,
standard depth + adversarial verification). All load-bearing claims
verified against primary sources on 2026-07-09; verdicts noted inline.

## Official MCP Registry (registry.modelcontextprotocol.io)

- **Still preview, API frozen at v0.1, no GA** [verified]. Site banner:
  "currently in preview. Breaking changes or data resets may occur before
  general availability." App releases ship frequently (v1.7.9,
  2026-05-12) but the API contract hasn't moved since the 2025-10-24
  freeze. (modelcontextprotocol.io/registry/about;
  github.com/modelcontextprotocol/registry)
- **Scale: ≥36,000 total server-version records, ≥10,000 latest-version
  servers, growing** [verified by live API pagination 2026-07-09 — both
  floors, cursors not exhausted; no stats endpoint exists]. Earlier
  snapshots (9.6K in May, ~2K in April) are stale — do not cite them.
- **Moderation is deliberately minimal**: only illegal/malware/spam/
  non-functioning servers removed; quality, vulnerabilities, duplicates
  explicitly NOT policed — "pushing moderation to subregistries."
  (registry moderation-policy page)
- **Federation model**: downstream catalogs either poll the registry as
  aggregators or implement its subregistry OpenAPI spec, adding custom
  metadata under namespaced `_meta` keys (ratings, security scans).
  Host apps are told NOT to consume the official registry directly.
  (registry-aggregators page)
- **Governance**: community Registry Working Group (PulseMCP, Stacklok,
  TeamSpark, Ravenmail maintainers); above it, Anthropic donated MCP to
  the **Agentic AI Foundation** (Linux Foundation directed fund,
  co-founded Anthropic/Block/OpenAI; platinum backers incl. AWS, Google,
  Microsoft, Cloudflare, Bloomberg) on 2025-12-09 with maintainer
  continuity [verified]. The 2026 roadmap post does NOT commit to
  registry GA or server-signing standards — both "on the horizon."

## Spec churn a catalog must absorb

The **2026-07-28 release (RC since 2026-05-21, "largest revision since
launch")** [verified against draft changelog]:

- Streamable HTTP goes **stateless**: `initialize` handshake and
  `Mcp-Session-Id` removed; new mandatory `server/discover` RPC; new
  `Mcp-Method`/`Mcp-Name` headers; SSE resumability removed.
- Tool schemas open up to full JSON Schema 2020-12; `ttlMs`/`cacheScope`
  caching fields added.
- Auth: RFC 9207 `iss` validation; OAuth DCR deprecated for Client ID
  Metadata Documents. Roots/Sampling/Logging/HTTP+SSE deprecated
  (12-month window policy).
- **No server.json/registry schema changes ride along** — registry and
  spec release trains are decoupled [verified].
- Implication: a catalog certifying servers needs a stated
  **compatibility-matrix policy** across 2025-11-25 vs 2026-07-28
  servers — GA (Nov 2026) lands ~4 months after the spec flips. No RH
  statement on record. → proposed question entry.

## Kubeflow Hub — the finding of the run

**Kubeflow Hub (formerly kubeflow/model-registry; README: "Red Hat
drives the project's development") shipped an MCP Catalog in Feb 2026**
[verified: repo redirect, README text, PR merge dates]:

- PR #2213 "feat(mcp): introduce mcp catalog openapi spec" (merged
  2026-02-16) — `McpServer`/`McpTool` entities,
  `/api/mcp_catalog/v1alpha1/*` endpoints (v1alpha1, NOT v1 — early
  maturity signal).
- PR #2269 source-label filtering (merged 2026-02-26); catalog landing
  page + tools-section UI work in March 2026.
- Pattern mirrors Hub's Model Catalog (YAML/HuggingFace sources,
  federated discovery) — and the timing (Feb build → May RHOAI 3.4 DP
  announcement) plus RH stewardship strongly suggests **this is the
  RHOAI MCP Catalog's upstream implementation**. Neither project's docs
  state the relationship. → proposed question entry (confirm + document).
- `kubeflow/mcp-server` (KEP-936, the repo given at intake as
  "upstream") is unrelated to catalog work: an MCP server wrapping
  Kubeflow Trainer ops, 23 tools, no releases [verified]. Likely a
  pasted-wrong-repo; it remains a catalog-entry candidate.

## Adjacent k8s-native MCP management (coopetition surface)

- **ToolHive (Stacklok)** — registry server aggregates Git/K8s/upstream
  registries/internal APIs into named catalogs; Sigstore signing +
  GitHub attestations; v1.2.0 (~Apr 2026) **dropped its native format
  for the official server.json schema** (extended via `_meta`).
  **Co-maintained by Red Hat** [verified — stated on stacklok.com AND
  developers.redhat.com; GitHub MAINTAINERS files lag the announcement].
- **kagent kmcp** — MCPServer CRD + lifecycle controller (v0.3.0, May
  2026) — functional overlap with MCPLO.
- **kgateway v2.0** — gateway-side MCP tool registry with auto
  discovery/registration — overlap with MCP Gateway.
- **Docker** — `docker/mcp-registry` submission repo → Docker-built,
  signed (provenance+SBOM) images on Docker Hub `mcp` namespace;
  explicitly independent of the official registry.
- **GitHub MCP Registry** — publish once via `mcp-publisher` CLI to the
  official registry; auto-appears in GitHub's surface (by-design
  no-duplication with official registry).

## Catalog-vs-registry, upstream's words

Official ecosystem layering: **official registry** (canonical metadata;
"metaregistries host metadata, not code") → **subregistries** (ETL +
annotations + curation) → **package registries** (npm/PyPI/Docker Hub —
the code). Docker's split: registry = intake pipe, catalog = "curated
collection of verified MCP servers" storefront. Read against RH: the
mcp-catalog/mcp-registry split maps cleanly, except RH's registry does
MORE than upstream's term implies (certification/lifecycle/trust) —
upstream's registry explicitly disclaims scanning and defers trust to
subregistries. RH's catalog is, in upstream vocabulary, a subregistry
with a deployment path.

## Gaps (upstream → RH plan)

1. **No stated federation posture** with the official registry
   (aggregator vs subregistry spec vs neither). → question entry.
2. **No RH publisher/namespace presence found** in the official or
   GitHub registries (not exhaustively confirmed — worth a direct
   check before TP).
3. **Signing/provenance is competitor table stakes** (Docker, ToolHive)
   but has no spec-level standard to inherit — the enterprise-tier
   trust story needs an explicit stated chain.
4. **Spec-version compatibility policy** unstated (see above).
5. **Kubeflow Hub relationship undocumented** (see above).

## Sources

Primary fetches: modelcontextprotocol.io registry pages (about,
aggregators, moderation), draft changelog + RC and roadmap blog posts,
github.com/modelcontextprotocol/registry, kubeflow/hub (README, PRs
2213/2269), kubeflow/community#936, kubeflow/mcp-server,
docker/mcp-registry + docs.docker.com catalog docs, github.blog MCP
registry post, kagent-dev/kmcp, docs.stacklok.com registry schema +
updates, stacklok.com/download, developers.redhat.com ToolHive article,
anthropic.com + linuxfoundation.org AAIF posts, live registry API
pagination (2026-07-09). Search-only: kgateway.dev, CNCF spotlight.
