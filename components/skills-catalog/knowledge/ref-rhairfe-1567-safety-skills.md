---
type: reference
title: "RHAIRFE-1567: Reusable safety skills in the Skills Catalog"
description: RFE for publishing reusable safety primitives (content moderation, PII detection, toxicity filtering) as versioned, framework-agnostic catalog entries with accuracy metrics; Stakeholder review; customer-validated demand from accounts concerned about responsible AI maturity.
timestamp: 2026-08-02
resource: https://redhat.atlassian.net/browse/RHAIRFE-1567
tags: [skills-catalog, rfe, safety, guardrails]
components: [skills-catalog]
---

RFE proposing that safety capabilities (content moderation, PII
detection, toxicity filtering) be published as reusable, versioned
skills in the catalog rather than implemented as one-off integrations
per agent.

Status: Stakeholder review. Customer-validated demand from accounts
evaluating alternative platforms for responsible AI capabilities.

Key acceptance criteria: at least 2 reusable safety skills with
versioning and accuracy metrics, consumable by any agent runtime
without framework-specific integration, platform engineer curation
controls with quality thresholds.

Connects to the guardrails and responsible AI story -- safety skills
in the catalog would provide governed, tested building blocks that
complement the AI Gateway's runtime guardrails.
