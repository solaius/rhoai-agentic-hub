---
type: reference
title: ITS Routing via AI Gateway IPP Plugin
description: Feature to implement ITS routing as an IPP plugin in ai-gateway-payload-processing -- X-ITS-Budget header detection, Envoy internal listener fan-out to ITS Service; near-term Envoy path.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-2442
tags: [ai-gateway, its, ipp, envoy]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Near-term ITS integration on the current Envoy stack. Go plugin in
the IPP RequestProcessor pipeline, positioned after model-provider-
resolver and before api-translation. Routes ITS-enabled requests to
the ITS Service via Envoy internal listener; non-ITS requests pass
through at zero overhead. Clones RHAIRFE-2953. See also RHAISTRAT-2443
(Praxis-native filter) and RHAISTRAT-2444 (Rust orchestration layer).
