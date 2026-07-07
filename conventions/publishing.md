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
- `audience: internal` is schema-reserved for a future GitLab Pages target;
  v1 publishes `public` only.
- CI (`publish.yml`) pushes to `solaius/rhoai-agentic-hub-pages` and
  regenerates that repo's landing `index.html` from manifest titles and
  descriptions. The pages repo holds built artifacts only — no knowledge.
- Use the `hub.publish` skill; publishing is a disclosure decision and gets an
  inline confirm.
- Each enablement artifact is a self-contained directory —
  `features/<f>/enablement/<slug>/` with index.html as its entry point;
  assets live inside it.

Live root: https://solaius.github.io/rhoai-agentic-hub-pages/
