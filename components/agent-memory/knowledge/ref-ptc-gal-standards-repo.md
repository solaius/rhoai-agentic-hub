---
type: reference
title: "ptc-gal-standards (Wes Jackson's LF standards project)"
description: Wes Jackson's project proposing Linux Foundation standards for agent provenance (where did information come from?) and authority granting (how do I grant an agent permission to act?).
resource: https://github.com/wjatx/ptc-gal-standards
tags: [agent-memory, standards, security, provenance]
timestamp: 2026-08-07
source: shared in agent memory team sync 2026-08-06
---
Two documents:
- [lf-standards-brief.md](https://github.com/wjatx/ptc-gal-standards/blob/main/lf-standards-brief.md) -- formal standards brief
- [sci-fi-primer.md](https://github.com/wjatx/ptc-gal-standards/blob/main/sci-fi-primer.md) -- accessible narrative version

Relevant to agent memory because memory is a strong injection path --
provenance (where did this memory come from?) and authority (what can
this agent do with these memories?) are complementary to the RBAC
controls in MemoryHub. Agent security projects like Praxis, OSAC, and
Sago are recognizing memory as tainted-by-default; deterministic
system-written metadata (not agent-written) is the mitigation path.
