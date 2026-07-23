---
type: decision
title: Push skills and agent registry RFCs upstream simultaneously
description: Decision to push both skills registry (RFC-0008/0009) and agent registry RFCs to MLflow simultaneously rather than sequentially; Edson argues stop self-throttling, we have second maintainer, community calls starting.
decided: 2026-07-23
timestamp: 2026-07-23
tags: [skills-registry, agent-registry, mlflow, upstream]
features: [skills-registry, agent-registry]
review_after: 2026-09-23
source: Skills Registry/Catalog meeting 2026-07-23 + Ramesh catalog-vs-registry GDoc (Edson comment)
---

## Context

Databricks initially preferred sequential RFC submissions. Matt said
"one at a time." Red Hat had been self-throttling to one RFC in review
at a time. Skills registry RFC (originally one, now split into two) has
been in process since April.

## Decision

Push both skills and agent registry RFCs upstream simultaneously.
Bill will submit the agent registry RFC "immediately" after the second
skills RFC.

## Rationale (Edson Tirelli)

"We should stop self-throttling. Push both RFCs upstream with clear
prioritization and see how Databricks responds. Our assumption that
they can't handle both is based on a low-volume signal -- they've had
no reason to scale their review capacity to match our needs because we
haven't shown them the actual demand. Send the work, measure the
response, adjust from there."

Supporting factors: Red Hat now has a second MLflow maintainer,
community calls starting in the next couple of weeks (alternating US
and Singapore time zones), and credibility gained in the last six
months.

## Consequences

- Databricks may push back -- but that gives data to decide how to
  proceed (fork, parallel work, etc.)
- Neither RFC may ship in 3.6, but both have a shot
- Bill estimates ~60% chance skills registry lands in 3.6, ~40% agent
  registry, ~0% both (Ramesh estimates 100% for minimal agent registry)
