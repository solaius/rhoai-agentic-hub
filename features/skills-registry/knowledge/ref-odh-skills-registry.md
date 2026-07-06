---
type: reference
title: ODH skills-registry (plugin marketplace)
description: The org plugin marketplace this hub consumes shared skills from — registry.yaml → marketplace.json/catalog.md
resource: https://github.com/opendatahub-io/skills-registry
tags: [skills, marketplace, tooling]
timestamp: 2026-07-06
---
Central registry aggregating Claude Code plugins across opendatahub-io; also a
cross-harness skill catalog. This hub's `.claude/settings.json` wires it via
extraKnownMarketplaces (see /conventions/ and the design spec D8). Read
ARCHITECTURE.md first; registry.yaml is the source of truth.
