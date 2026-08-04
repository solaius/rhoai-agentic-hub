---
type: fact
title: RFC strategy evolved -- user journeys before technical details
description: New MLflow RFC strategy (2026-08-04) -- submit user-journey-only RFC first, get cross-company alignment (RH + Databricks + AWS), then technical implementation RFC; evolved from the July RFC split approach.
timestamp: 2026-08-04
tags: [skills-registry, mlflow, upstream, rfc, databricks]
components: [skills-registry, agent-registry]
source: Internal Sync on Agent/Skill Registries 2026-08-04
---

Matt Prahl proposed a new RFC strategy after the initial skill RFC delays:

1. First create an RFC that covers **user journeys only** -- no technical
   details. Examples: "I need to find a skill -- how do I do that?" or
   "My agent needs to find a skill -- how does it do that?"
2. Get alignment across Red Hat, Databricks, and potentially AWS on
   those user journeys.
3. Only then do a technical implementation RFC.

This evolved from the [RFC split](/components/skills-registry/knowledge/fact-skills-rfc-split-databricks.md)
approach (July 2026) where both RFCs were submitted in parallel.
The new insight is that **vision misalignment is the root blocker** --
Databricks and Red Hat have different customer bases driving different
governance priorities, and technical RFC review friction is a symptom.

Humair confirmed: once user-journey buy-in is secured, Databricks is
willing to compromise on implementation details and phasing (as seen
with traces and skills registry phase 1).
