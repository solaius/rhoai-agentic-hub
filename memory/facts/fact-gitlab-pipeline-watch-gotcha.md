---
type: fact
description: When watching fork CI after a push, verify the pipeline's sha matches the pushed commit before trusting its status -- querying pipelines?per_page=1 right after a push races pipeline creation and returns the PREVIOUS run's success
timestamp: 2026-08-05
status: current
---

Hit 2026-08-05 during the #16 prototype work: after pushing a fix commit to
the UXD fork, a status watcher queried
`GET /projects/<id>/pipelines?ref=<branch>&per_page=1` ~30s after the push,
got the PREVIOUS commit's already-succeeded pipeline, and reported the
preview "deployed" while the real build was still pending. The owner loaded
a stale preview as a result.

Rule for anything watching fork CI (hub.prototype pushes especially):

1. After `git push`, resolve the pipeline by BOTH ref and sha -- list
   pipelines and match `sha` to the pushed commit; if no matching pipeline
   exists yet, wait and re-list (creation can lag the push).
2. Only then poll that pipeline id to completion.
3. Never report a preview URL as updated without the sha-matched pipeline
   reaching `success`.

Fork webpack builds take ~7-9 minutes once a runner picks them up; a
success in under a minute is a red flag that the wrong pipeline was
sampled.
