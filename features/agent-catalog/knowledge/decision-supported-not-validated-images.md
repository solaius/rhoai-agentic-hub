---
type: decision
title: Maintained catalog images are "supported", not "validated"
description: 2026-07-10 — in RHOAI "validated" already means vendor-provided images Red Hat certifies but the vendor maintains (NVIDIA Triton); catalog images Red Hat maintains are "supported".
decided: 2026-07-10
timestamp: 2026-07-16
tags: [agent-catalog, terminology, support]
features: [mcp-catalog]
---

**Context.** The AIPCC ADR (GitLab rhel-ai/core/team-docs MR 224) calls its
agent-runtime base images "validated". In RHOAI, "validated and tested"
already denotes vendor-provided images that Red Hat certifies but the vendor
maintains (e.g. NVIDIA Triton) — Daniele Zonca. Reusing the word for images
Red Hat itself builds and maintains would blur the support boundary.

**Decision** (Peter Double, with Daniele Zonca's rationale; 2026-07-10
supported-images meeting). Catalog harness/starter-kit images that Red Hat
builds and maintains are **supported images**. "Validated" stays reserved for
the vendor-maintained certification pattern. The same terminology applies to
MCP server handling (OCP MCP servers, the coming OpenShift AI MCP).

**Consequences.** A limited set of maintained baseline images with a support
matrix ("works with vLLM / responses API / …") rather than end-to-end
framework support; skills ship at most as "tested with these models —
mileage may vary" (accepted same meeting as the baseline); Daniele Zonca to
comment on the
[AIPCC ADR](/features/agent-catalog/knowledge/ref-aipcc-agent-base-images-adr.md)
to reconcile its "validated" language.
