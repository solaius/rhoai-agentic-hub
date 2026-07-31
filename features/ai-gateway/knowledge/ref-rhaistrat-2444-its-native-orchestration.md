---
type: reference
title: Native-Performance ITS Orchestration and Service Layers for Praxis Gateway Integration
description: Feature to reimplement ITS orchestration (fan-out, concurrency, retry) and HTTP service in Rust crates for Praxis-native execution -- eliminates Python from request path while keeping ITS algorithms in Python.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-2444
tags: [ai-gateway, its, praxis, rust]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Two new Rust crates: its-orchestrator (fan-out, concurrency control,
backoff/retry as a Praxis filter) and its-service (HTTP endpoint
wrapping orchestration + Python algorithm bridge). ITS algorithms
(Self-Consistency, Best-of-N) stay in Python, accessed via defined
interface. Follows the fms-guardrails-orchestrator pattern
(Axum/Tokio coordination). Clones RHAIRFE-2955.
