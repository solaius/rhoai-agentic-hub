---
type: reference
title: Gen AI Studio playground must support AI Gateway as alternative to OGX
description: Feature to decouple Gen AI Studio from OGX-only backend, enabling AI Gateway as an alternative serving path; parent RHAISTRAT-1312; cross-feature with gen-ai-studio.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-1935
tags: [ai-gateway, gen-ai-studio]
components: [gen-ai-studio]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Removes Gen AI Studio's hard dependency on OGX for model interaction.
As AI Gateway becomes the strategic serving path, the playground needs
to support it directly so customers standardizing on AI Gateway don't
need a parallel OGX deployment. Clones RHAIRFE-2374.
