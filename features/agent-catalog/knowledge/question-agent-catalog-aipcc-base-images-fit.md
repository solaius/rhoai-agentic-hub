---
type: question
title: Will AIPCC base images fit the catalog's needs?
description: AIPCC is building agent-runtime base images for 3.6 (GitLab ADR MR 224), but catalog contents change constantly and AIPCC is out of the loop; Daniele Zonca to comment on the ADR.
status: open
timestamp: 2026-07-16
tags: [agent-catalog, 3.6, aipcc, images]
---

AIPCC is proceeding with base images for agent runtimes per an ADR
([GitLab MR 224](/features/agent-catalog/knowledge/ref-aipcc-agent-base-images-adr.md),
targeting 3.6). Bill Murdock doubts they'll meet catalog needs: catalog
contents change constantly, AIPCC is out of the loop, and base images are
meant to be built on — if they don't fit, someone else must deliver images
that do. The ADR's "validated" wording also conflicts with the
[supported/validated terminology ruling](/features/agent-catalog/knowledge/decision-supported-not-validated-images.md).
Daniele Zonca agreed (2026-07-10) to comment on the ADR while there's time
before 3.6. PMs currently lack access to the GitLab repo.
