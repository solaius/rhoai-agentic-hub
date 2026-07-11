---
rfe_id: RHAIRFE-2642
title: Ready-made memory integrations for agent harnesses and frameworks
priority: Normal
size: L
status: Submitted
parent_key: RFE-009
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory) · Phase: RHOAI 3.7 Tech Preview
**Split from:** RFE-009

## Summary

The framework-agnostic memory service (RHAIRFE-2630) is only as adoptable as its integrations. AI engineers working in the major agent harnesses and frameworks need platform memory to work out of the box in their tool of choice, without writing per-harness glue code, and to participate in each harness's native workflow so memory is present when the harness assembles context rather than only through manual tool calls. The integrations must be versioned and maintained alongside the service so an upgrade does not silently break harness users.

## Problem Statement

Each agent harness and framework has its own native way of extending behavior and wiring in memory. Today an engineer adopting the platform memory service writes custom integration code per harness, and the harness-native conveniences users expect (memory available when the harness assembles context, not only through manual tool invocation) are absent. Because each harness and framework moves independently and quickly, integrations that are not versioned and maintained with the service drift out of compatibility, so a memory-service upgrade can break harness users without warning.

## Affected Customers

- **Infineon**: running AutoGen, LangChain, and LangGraph simultaneously. A memory service that requires per-framework custom integration multiplies their cost by three and undermines the single-governance-layer requirement that brought them to the platform.
- Every 3.6 Dev Preview pilot moving from the playground to their own harness at Tech Preview: without ready-made integrations, each pilot re-implements the same glue code before it can adopt governed memory.

## Business Justification

- The parent Outcome's central promise is framework-agnostic memory ("an agent's memory survives a framework switch"). Ready-made integrations are what make that promise real at adoption time. Without them the promise holds only for teams willing to build glue code, which re-creates the duplicated-effort problem the Outcome exists to remove.
- Per-harness custom integration is precisely the cost that turned a single-governance-layer requirement into a triple cost for a multi-framework account. Shipping the integrations collapses that cost back to one and protects the single-control-plane reason customers chose the platform.

## User Scenarios

1. As an AI engineer adopting platform memory in my existing framework, I enable it through the framework's native memory interface and my agent reads and writes governed memory without any custom integration code.
2. As an engineer whose agent runs in a harness that assembles its own context, I get platform memory participating in that assembly step, so relevant memory is present automatically rather than only when I make an explicit tool call.
3. As an engineer on a team that upgrades the memory service, my harness integration keeps working across the upgrade because the integration is versioned and maintained with the service.

## Acceptance Criteria

- [ ] An engineer can enable platform memory in each supported major harness and framework without writing custom integration code.
- [ ] Memory participates in each supported harness's native workflow: available when the harness assembles context, not only through manual tool invocation.
- [ ] The integrations are versioned, documented, and maintained with the memory service, so a service upgrade does not silently break harness users.

## Success Criteria

- At Tech Preview (RHOAI 3.7 timeframe), an engineer in any supported harness goes from zero to working governed memory in under an hour, without custom code.
- A framework switch between two supported harnesses preserves memory and requires no integration work.

## Scope

### In Scope
- Ready-made, native-workflow memory integrations for the platform memory service across the supported set of major agent harnesses and frameworks, versioned and maintained with the service.

### Out of Scope
- The framework-agnostic memory service and its API surface (RHAIRFE-2630), which these integrations consume.
- Memory effectiveness on smaller self-hosted models, including shipped guidance and assets for that model tier (split into a separate RFE).

## Open Questions

- What is the exact supported target list at Tech Preview, and for each target is native context participation achievable or does it degrade to a tool or MCP integration where the harness manages memory internally?
