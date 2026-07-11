# Publishing conventions

Nothing is public unless it has an entry in `publish/manifest.yaml`
(allowlist; the failure mode is *forgot to publish*, never *leaked by
default*). Entries:

    - source: features/mcp-gateway/enablement/rhcl-hub/   # repo-relative; dir or file
      dest: mcp-gateway/rhcl/                             # URL path in the pages repo
      audience: public                                    # public | internal
      title: MCP Gateway Knowledge Hub
      description: Zero-to-hero enablement site for RHCL

Rules:
- `dest` slugs are contracts — never change one after it ships (the publish
  script warns via its snapshot diff). Removing a manifest entry removes the
  published copy on the next publish run — that is the explicit intent path.
- Two publish targets, one manifest: `audience: public` ships to the
  `solaius/rhoai-agentic-hub-pages` repo (world-readable); `audience: internal`
  ships to this repo's own `gh-pages` branch at
  `https://solaius.github.io/rhoai-agentic-hub/` (interim hosting until a
  protected GitLab Pages target exists; accepted caveat: this repo is public,
  so the interim internal target is not access-controlled). Each target clone
  keeps its own `.publish-snapshot.json`, badges, and generated landing page.
  Public artifacts must never link into an internal dest, this is
  lint-enforced (`hub_lint.py` fails the build on a public-to-internal link).
  Internal artifacts that link to a public dest must use the absolute public
  URL (`https://solaius.github.io/rhoai-agentic-hub-pages/<dest>/`), not a
  relative path, since the two targets are different repos and different
  sites. Internal-to-internal (hub-to-hub) links stay relative.
- CI (`publish.yml`) pushes to `solaius/rhoai-agentic-hub-pages` and
  regenerates that repo's landing `index.html` from manifest titles and
  descriptions. The pages repo holds built artifacts only — no knowledge.
- Use the `hub.publish` skill; publishing is a disclosure decision and gets an
  inline confirm.
- Each enablement artifact is a self-contained directory —
  `features/<f>/enablement/<slug>/` with index.html as its entry point;
  assets live inside it.

Live root: https://solaius.github.io/rhoai-agentic-hub-pages/ (public) ·
https://solaius.github.io/rhoai-agentic-hub/ (internal, interim)

## Landing page + snapshot (v2)

The pages-site landing page is rendered from `publish/landing-template.html`
(tracked; self-contained inline CSS): artifacts grouped by area (feature
`title` from features/features.yaml, routing-table order, Narrative last),
one card per artifact, NEW/UPDATED badges for artifacts published or changed
in the last 14 days. Badge state lives in `.publish-snapshot.json` (v2:
`{dest: {source, hash, published, badge}}`); v1 snapshots migrate on the
first run with no false badges.
