---
type: fact
description: "audience: internal in publish/manifest.yaml deploys to this repo's gh-pages (solaius.github.io/rhoai-agentic-hub) via publish.yml; interim until protected GitLab Pages; public artifacts must not link into internal dests (lint-enforced); knowledge hubs are internal-audience by owner ruling 2026-07-11"
timestamp: 2026-07-12
status: current
---

One manifest, two publish targets. `audience: public` entries still deploy
to the dedicated `solaius/rhoai-agentic-hub-pages` repo. `audience: internal`
entries deploy, via the same `publish.yml` run, to this repo's own
`gh-pages` branch: `https://solaius.github.io/rhoai-agentic-hub/`. Each
target is its own git clone with its own `.publish-snapshot.json`, so
NEW/UPDATED badges and removal detection work per target without cross-talk.

This is the interim form of backlog #13: the originally envisioned host was
a protected, VPN'd GitLab Pages instance. That tail stays open. Accepted
caveat in the meantime: this repo is public, so the internal target carries
no real access control, only reduced discoverability (unlisted, unlinked
from the public site).

`hub_lint.py` enforces the boundary: a public-audience artifact linking into
an internal dest is a lint ERROR (0 tolerance, same severity class as
restricted-pattern leaks). Internal artifacts may link out to public ones
freely, using absolute public URLs for anything outside the internal target.

Owner ruling 2026-07-11: all knowledge hubs (existing and pre-staged) are
`audience: internal`, GA-readout-class detail that does not belong on the
public site. The two hubs that were public (RHCL/Gateway, Management)
flipped to internal the same day; the three component hubs built afterward
(Catalog, MCPLO, Registry) entered the manifest as internal from their first
commit.

See [[fact-hub-network-standard-sections]] for the sections each hub now
carries. Spec:
[/docs/specs/2026-07-11-component-hub-buildout-design.md](/docs/specs/2026-07-11-component-hub-buildout-design.md).
