---
type: fact
title: Skills registry RFC split into two per Databricks request
description: Bill splitting original skills registry RFC into 2 separate RFCs and PRs per Databricks request; second RFC is lightweight (intro + user journeys only, no field-level API detail). Outline agreed with Databricks.
timestamp: 2026-07-23
tags: [skills-registry, mlflow, upstream, rfc]
features: [skills-registry]
review_after: 2026-09-23
source: Skills Registry/Catalog meeting 2026-07-23
---

At Databricks' request, Bill Murdock is splitting the original single
skills registry RFC into two separate RFCs with two separate PRs:

**RFC-0008 (Phase 1)**: already submitted (PR #26). Contains the
full data model, API, and UI spec. Outline agreed with Databricks;
currently in review with Matt and Homeir.

**RFC-0009 (Phase 2)**: covers harness adapters, install, import, lock
file. Being submitted soon.

Key change in approach: the second RFC (and all future RFCs including
agent registry) follow a lightweight format -- intro and user journeys
only, no field-level API detail. This format was adopted after the
first RFC's scope caused Databricks to request major changes and a
split. "They were particularly put off by the fact that it takes so
long to just load the GitHub page" (Bill, referring to comment volume).
