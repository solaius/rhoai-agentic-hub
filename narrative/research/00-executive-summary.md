---
title: "Narrative research: executive summary"
description: "Living synthesis of the agentic strategy narrative research series — competitive positioning and enterprise requirements as of 2026-07-10."
timestamp: 2026-07-10
tags: [narrative, research, synthesis]
---

# Narrative research: executive summary

> Series home: `/narrative/research/`. Rewritten on each refresh.

## Series index

| # | Doc | Lens | Date |
|---|---|---|---|
| 01 | [Competitive landscape: agentic AI platforms](/narrative/research/01-competitive-agentic-platforms.md) | competitive | 2026-07-10 |
| 02 | [Requirements landscape: enterprise agentic AI](/narrative/research/02-agentic-requirements-landscape.md) | requirements | 2026-07-10 |

## Lens gaps

The following lenses were not run in this series. Retry invocations:

- `hub.research narrative landscape` — definitions, state of the art,
  best practices for the agentic narrative
- `hub.research narrative upstream` — OSS projects, standards, protocols
  (MCP, A2A, OGX, OpenShell, SPIFFE) driving the narrative
- `hub.research narrative architecture` — patterns, reference
  architectures, build-vs-buy decisions across the agentic stack

## Synthesis

### Market position

Red Hat AI's agentic strategy is well-positioned on the infrastructure
and operations layer — the "from metal to agents" thesis holds. The
combination of vLLM-based inference, llm-d (CNCF Sandbox), OpenShell
co-maintenance, SPIFFE-based identity, and hybrid/multi-cloud portability
via OpenShift creates a uniquely open, vendor-neutral foundation that no
competitor matches end-to-end.

**Where Red Hat leads:**
- Full-stack infrastructure ("from metal to agents")
- Open-source/standards-based approach (MCP via LF, SPIFFE via CNCF,
  OTel, vLLM, llm-d, MLflow, OpenShell)
- Hybrid/multi-cloud portability (the single largest unaddressed market)
- NVIDIA partnership depth (OpenShell co-maintainer + platform partner)
- Inference economics (the Jevons Paradox argument — no competitor makes
  this case because they profit from token consumption)

**Where gaps exist:**
- MCP ecosystem delivery timing (Databricks Unity AI Gateway and Google
  managed MCP servers are GA today; Red Hat targets 3.5-3.6)
- Agent-building developer experience (no visual builder or managed
  runtime equivalent)
- Agent evaluation maturity (Databricks CLEARS is GA; Eval Hub is planned)
- Analyst recognition (absent from 2026 Gartner MQ for AI Platforms)

### Enterprise requirements

The enterprise market has crossed from "can we build agents?" to "can we
trust, govern, and operate them?" The top blockers are non-technical:
governance (only 21% have mature models), data readiness (only 15%
prepared), and cost control (22% report negative ROI at 12 months).
88% of agent pilots never reach production.

**The economic picture has crystallized:** The Jevons Paradox for tokens
is empirically confirmed — per-token costs dropped 90% but consumption
grew 1,001% (Jan 2025–Apr 2026). Average enterprise AI budgets grew from
$1.2M (2024) to $7M (2026). Uber burned through its entire 2026 AI
budget by April. Self-hosted inference is shifting from cost optimization
to structural necessity.

**Regulatory urgency:** EU AI Act high-risk provisions enforceable August
2, 2026. Recitals 99-100 explicitly address multi-agent architectures.
Open-source models with published documentation qualify for certain
exemptions — directly benefits Red Hat.

### JTBD hypothesis assessment

The 7 existing JTBDs are well-aligned with the top enterprise
requirements. Three gaps were identified:

1. **Agent fleet management at scale** — current JTBDs cover individual
   agents; enterprises need centralized registry with shadow-agent
   discovery, lifecycle management, Guardian Agent capabilities, and
   emergency revocation. All hyperscalers launched fleet services in 2026.
2. **Agentic AI cost control** — JTBD #4 focuses on inference
   performance but the dominant 2026 conversation is cost governance:
   budget controls, model routing, per-agent cost attribution. The
   Tokenomics Foundation launched for this gap.
3. **Data/context readiness** — every analyst cites data quality as a
   top-3 blocker. 60% of RAG failures trace to freshness, not retrieval.
   The knowledge layer agents depend on maps to no current JTBD.

### Strategic implications

1. **Accelerate MCP ecosystem delivery** — consider phased GA (Gateway
   first) to stop enterprise standardization on competitor approaches.
2. **Tell the SPIFFE identity story** — the only standards-based,
   portable agent identity. Market before AWS's proprietary approach
   becomes the default.
3. **Lean into the cost story** — the Jevons Paradox argument is unique
   and resonant. No competitor makes it.
4. **Position OpenShift AI as the production runtime for OpenShell** —
   leverage the co-maintainer relationship.
5. **Pursue analyst recognition** — submit for Gartner MQ once the full
   AgentOps + MCP + Eval Hub stack is GA.

## Recommended follow-ups

- **Deeper competitive drill-down:** per-competitor feature comparison
  tables for specific deal positioning (suggested: `hub.research
  narrative competitive` at deep depth)
- **Upstream lens:** detailed mapping of OSS projects (MCP spec roadmap,
  A2A protocol, OGX, OpenShell, Kagenti) to the five themes
- **JTBD evidence collection:** run the three gap JTBDs through customer
  tracker and qa data to validate/invalidate (requires
  `customer-feedback-refresh` + JTBD mining when qa volume justifies)
- **Jira gap analysis:** once `hub.research` jira-gap lens ships
  (backlog #27b), map active Jira work against competitive findings to
  identify "NOT building" gaps
