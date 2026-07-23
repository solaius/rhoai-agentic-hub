---
type: reference
title: LOLA — universal skill package manager (Red Hat Product Security)
description: Red Hat Product Security's universal AI skill package manager — convention-based auto-discovery, federated marketplace, multi-assistant install. Must-have for Red Hat in the MLFlow skills registry plugin architecture.
resource: https://github.com/LobsterTrap/lola
timestamp: 2026-07-23
tags: [skills-registry, lola, red-hat, packaging]
features: [skills-registry]
---

"Write Agent Skills once, use everywhere." Convention-based
auto-discovery (no manifest file needed), federated marketplace model
(official marketplace at RedHatProductSecurity/lola-market), `.lola-req`
for version constraints. Installs across Claude Code, Copilot, Cursor,
Gemini CLI, OpenCode. 109 stars, v0.7.0 (Jul 2026), Apache-2.0.

Maintained by Igor Brandao (mrbrandao) and Katie Mulliken (SecKatie)
under Red Hat Product Security. Explicitly named in MLFlow RFC-0008
(PR #26) as a reference package manager plugin alongside APM. The
RPM-to-DNF analogy: "your skill is the RPM, LOLA is the DNF."

Red Hat maintaining both LOLA (the installer) and authoring RFC-0008
(the registry) creates a vertically integrated skills distribution
story.

See [fact-skills-packaging-landscape](/features/skills-registry/knowledge/fact-skills-packaging-landscape.md)
for comparative analysis.
