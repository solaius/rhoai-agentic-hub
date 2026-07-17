---
type: fact
title: Regulation converges on an eight-field agent record
description: EU AI Act (Art. 26/49/50) + OMB M-25-21 + NIST GV-1.6/CSA jointly force a system of record with eight fields (identity+version, owner, purpose, risk class, lineage, deployment status, log refs, permissions); the pre/post-deployment dual structure maps 1:1 onto "approved vs running"; keep REMOVED records ≥6 months.
timestamp: 2026-07-16
tags: [agent-registry, compliance, requirements]
---
No regulation says "run an agent registry," but the overlapping regimes
effectively mandate one (evidence-graded detail:
[research/10-requirements](/features/agent-registry/research/10-requirements.md)):
**identity+version, business/technical owner + authorizer, purpose, risk
class, model/component lineage, deployment status, log references,
permissions/systems accessed**. EU specifics: providers register
high-risk systems pre-market; public-authority deployers register their
use; private deployers escape database registration but Art. 26
log-keeping (≥6 months) makes an internal inventory unavoidable —
registry implication: REMOVED-instance records retained ≥6 months.
Gartner's tiered-governance position (2026-05-26) adds: capture **risk
tier** as registry metadata — uniform governance across agents fails.
The dual pre/post-deployment structure is regulation-shaped: Annex
VIII/M-25-21 reporting needs both views.
