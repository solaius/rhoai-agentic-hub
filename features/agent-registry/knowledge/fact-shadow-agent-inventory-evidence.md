---
type: fact
title: Shadow-agent inventory — the best-evidenced fleet requirement
description: 82% of orgs running discovery found unknown agents; 67% of non-human identities were created outside IAM visibility; discovery tooling is now a commercial category (Zenity, WitnessAI, Microsoft free tier) — the unlinked-instance registry state is the direct answer.
timestamp: 2026-07-16
tags: [agent-registry, requirements, fleet-management]
---
The strongest-graded fleet-management evidence in the requirements lens
([research/10-requirements](/features/agent-registry/research/10-requirements.md),
market detail in [research/08-landscape](/features/agent-registry/research/08-landscape.md)):
82% unknown-agent discovery rates; 24.4% a2a-visibility (Gravitee); 67%
of non-human identities created unseen by IAM; Fortune-50 field data of
150k agent-linked resources with 82% of agents built by non-developers
(Zenity). Shadow-agent discovery is now a commercial category (Zenity —
Gartner Cool Vendor, WitnessAI, Oasis, Lasso, plus Microsoft's free-tier
detection). Registry consequence: the **unlinked instance** (discovered,
never governed) is a first-class state with an "adopt into governance"
path — this directly strengthens
[jtbd-manage-agent-fleet](/narrative/knowledge/jtbd-manage-agent-fleet.md).
Revocation nuance vs the JTBD's "revoke in seconds": the registry is the
*lookup*; enforcement lives in the identity/gateway plane, and registry
sync latency must never sit inside the revocation path.
