# Publishing — manifest to public site, end to end

Philosophy: **nothing is public unless `publish/manifest.yaml` names it.**
The allowlist inverts the old repo's model (where the whole repo deployed to
Pages and secrecy depended on remembering to exclude things). Here the
failure mode is *forgot to publish*, never *leaked by default*. Rules:
[/conventions/publishing.md](/conventions/publishing.md).

Publishing is also **decoupled**: this repo holds knowledge; built artifacts
ship to a separate public repo,
[solaius/rhoai-agentic-hub-pages](https://github.com/solaius/rhoai-agentic-hub-pages),
which GitHub Pages serves at
<https://solaius.github.io/rhoai-agentic-hub-pages/>. This repo could go
private or move hosts without breaking a single published URL.

## End to end

1. **Build** the artifact as a self-contained directory:
   `features/<feature>/enablement/<slug>/` with `index.html` as the entry
   point and all assets inside it (usually via `presentation-create`).
2. **Allowlist** it with the `hub.publish` skill — publishing is a
   disclosure decision, so the skill restates exactly what becomes public
   and takes an inline confirm before writing the manifest entry.
3. **Push to `main`.** Two workflows react:
   - `validate.yml` re-checks the manifest (`hub_publish.py --check`:
     schema, sources exist, no duplicate dests) along with everything else.
   - `publish.yml` checks out both repos, runs
     `hub_publish.py --pages-dir pages-repo --hub-sha $GITHUB_SHA`, and
     pushes the result to the pages repo as `hub-publish-bot` (no-op commit
     is skipped when nothing changed).
4. **The publisher applies the manifest**: copies each `source` to its
   `dest` in the pages clone, removes previously-published copies whose
   manifest entries were deleted, regenerates the landing `index.html` from
   manifest titles/descriptions, and records the state in
   `.publish-snapshot.json` (the snapshot is how it distinguishes "entry
   removed → unpublish" from "never published", and how it warns when a
   shipped `dest` changes).
5. **GitHub Pages** rebuilds the site from the pages repo. The artifact is
   live at `https://solaius.github.io/rhoai-agentic-hub-pages/<dest>`.

## The manifest

```yaml
- source: features/mcp-registry/enablement/mcp-registry-catalog-deck/  # repo-relative; dir or file
  dest: mcp-registry/catalog-deck/       # URL path on the pages site
  audience: public                       # public | internal
  title: MCP Registry & Catalog          # landing-page card title
  description: Slide deck covering ...   # landing-page card text
```

| field | rules |
|---|---|
| `source` | repo-relative, must exist, no `..` — a directory (published as a site path, `index.html` is the entry) or a single file |
| `dest` | URL path in the pages repo. **A contract once shipped** — never change it after publication (people hold the link); the snapshot diff warns if you try |
| `audience` | `public` is the only live target; `internal` is schema-reserved for a future VPN GitLab Pages target |
| `title`, `description` | what the generated landing page shows for this artifact |

**Removing an entry removes the published copy** on the next publish run —
that is the intended unpublish path, not an accident to guard against.

## One-time setup: `PAGES_PUSH_TOKEN`

`publish.yml` pushes to the pages repo with a repository secret:

1. Create a **fine-grained PAT** (github.com → Settings → Developer
   settings) scoped to **only** `solaius/rhoai-agentic-hub-pages`, with
   repository permission **Contents: Read and write**. Set an expiry you
   are willing to rotate on.
2. Set the secret from a real terminal:
   `gh secret set PAGES_PUSH_TOKEN --repo solaius/rhoai-agentic-hub` and
   paste the token **at the hidden prompt**.

**Never put the token value in a command line.** Argv leaks into shell
history, process listings, and session transcripts; a token that has
appeared there is burned — revoke it and mint a new one. Also beware:
`gh secret set` accepts empty stdin without complaint, silently storing an
empty secret (the symptom is an auth failure in the publish run — re-set it
interactively).

## Verifying and troubleshooting

- **Watch the runs:** `gh run list --repo solaius/rhoai-agentic-hub` (both
  workflows run on pushes to `main`).
- **Publish run green but URL 404s:** the pages repo's own Pages build runs
  after the bot's push — check
  `https://github.com/solaius/rhoai-agentic-hub-pages/actions`. First
  deploys of a new `dest` can take an extra minute.
- **Pages build wedged in "building" for >10 minutes** (has happened):
  kick it with
  `gh api -X POST repos/solaius/rhoai-agentic-hub-pages/pages/builds`.
- **`remote: Permission denied` / 401 in the publish run:** the PAT
  expired or was revoked — regenerate and re-set the secret as above.
- **`duplicate dest` or `source does not exist` in validate:** fix the
  manifest; `python scripts/hub_publish.py --check` reproduces locally.
- **Inspect what would ship:** clone the pages repo alongside and run
  `python scripts/hub_publish.py --pages-dir ../rhoai-agentic-hub-pages`
  locally, then `git -C ../rhoai-agentic-hub-pages diff` — same code path
  CI uses.
