---
type: fact
description: Which ODH skills-registry plugins the hub consumes (verified at setup)
timestamp: 2026-07-06
status: current
source: gh api opendatahub-io/skills-registry registry.yaml, checked during hub build T4
---
Verified in the ODH registry and enabled in .claude/settings.json:
rfe-creator (rfe.*, strat.*, review skills), assess-rfe (assess-rfe,
export-rubric). Local copies of these are NOT ported to the hub.
