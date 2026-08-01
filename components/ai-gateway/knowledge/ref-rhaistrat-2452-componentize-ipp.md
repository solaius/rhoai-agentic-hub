---
type: reference
title: Componentize IPP (Inference Payload Processing)
description: Feature to extract IPP from MaaS deployment ownership and re-parent it under AI Gateway Operator as a sub-component -- kustomize manifest vendoring, same pattern as batch-gateway.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-2452
tags: [ai-gateway, ipp, operator, deployment]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Moves IPP deployment manifests and CRDs from the MaaS repository to
ai-gateway-payload-processing under config/, mirroring the standard
RHOAI component layout. AI Gateway Operator manages IPP lifecycle via
AIGateway.spec.inferencePayloadProcessing.managementState
(Managed/Removed), using the same pattern already used for
batch-gateway. MaaS retains a soft dependency (Degraded status when
IPP unavailable) but no longer deploys or patches IPP resources.
