---
type: fact
description: "How to access gitlab.cee.redhat.com (Red Hat internal GitLab) — git sslVerify config, curl API with -sk, WebFetch limitation; known repos include uxd/prototypes/rhoai"
timestamp: 2026-08-03
status: current
---
Red Hat internal GitLab (`gitlab.cee.redhat.com`) uses a CA chain not in
the system trust store. Three access methods:

## Git over HTTPS (works)
Configured globally, scoped to this host only:
```
git config --global http.https://gitlab.cee.redhat.com/.sslVerify false
```
Clone, fetch, ls-remote all work. Initial handshakes can be slow (~20s) —
use generous timeouts.

## GitLab REST API via curl (works)
```
curl -sk "https://gitlab.cee.redhat.com/api/v4/projects/<url-encoded-path>/..."
```
`-sk` skips cert verification. Unauthenticated access works for
public-visibility projects. For private projects, add a `PRIVATE-TOKEN`
header.

Useful endpoints:
- Project info: `/api/v4/projects/uxd%2Fprototypes%2Frhoai`
- File tree: `/api/v4/projects/<id>/repository/tree?ref=<branch>&per_page=50`
- Raw file: `/api/v4/projects/<id>/repository/files/<url-encoded-path>/raw?ref=<branch>`
- Branches: `/api/v4/projects/<id>/repository/branches`

## WebFetch (does NOT work)
WebFetch rejects the self-signed cert chain with no override option.
Use `curl -sk` instead for fetching page or API content.

## Known repos
- `uxd/prototypes/rhoai` — UXD team's RHOAI prototypes (default branch:
  `3.6`, topics: pages). Frontend prototype app with `.design/`, `src/`,
  `scripts/`, `public/`, `worker/`. Last activity 2026-07-31.
