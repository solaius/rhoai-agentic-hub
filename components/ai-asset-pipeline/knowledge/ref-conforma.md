---
type: reference
title: "Conforma -- machine-readable policy engine for artifact promotion"
description: Open-source policy engine that gates artifact promotion against attestations -- separates "neutral observer" (Tekton Chains attestation) from "policy enforcer" (Conforma gate); machine-readable enterprise contracts; more flexible than JFrog's approval workflows.
resource: https://github.com/conforma/conforma
tags: [ai-asset-pipeline, policy, supply-chain, conforma]
components: [ai-asset-pipeline]
timestamp: 2026-08-03
source: conforma.dev docs + session research 2026-08-02
---

Policy-as-code engine that works with Konflux to gate artifact
promotion. Key architectural principle: the build pipeline (Tekton
Chains) is the "neutral observer" that attests what happened; Conforma
is the separate "policy enforcer" that decides whether the attestation
is acceptable.

For the AI asset pipeline, Conforma would enforce policies like:
- "Only promote skills that passed SkillSpector scanning"
- "Only promote MCP servers with OWASP MCP Top 10 clean scans"
- "Require cosign signature from a trusted builder before catalog entry"
- "Block artifacts without SBOMs from production registries"

Machine-readable policies are more flexible than JFrog's approval
workflows and fully open source.

Docs: https://conforma.dev/
