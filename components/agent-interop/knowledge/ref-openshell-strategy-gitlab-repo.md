---
type: reference
title: OpenShell strategy GitLab repo (continual strategy source)
description: "Adel Zaalouk's GitLab repo: use cases, strategic rocks, competitive positioning, roadmap milestones, TP/GA scope, and weekly reports for OpenShell/agent-interop -- the primary continual strategy source. VPN + git required (private repo)."
resource: https://gitlab.cee.redhat.com/azaalouk/openshell-strategy
timestamp: 2026-08-03
tags: [agent-interop, openshell, strategy, competitive, roadmap, gitlab]
review_after: 2026-09-15
source: direct clone via git-over-HTTPS
---

Primary continual strategy source for OpenShell productization and
agent-interop positioning. Curated by Adel Zaalouk (azaalouk@redhat.com),
last updated July 28, 2026.

## Access

Private repo -- requires Red Hat VPN. Clone via git-over-HTTPS with
`http.sslVerify false` scoped to gitlab.cee.redhat.com (see
/memory/facts/ref-gitlab-cee-access.md). No GitLab API token configured;
WebFetch does not work (cert chain).

```
git clone https://gitlab.cee.redhat.com/azaalouk/openshell-strategy.git
```

## Repo structure

| path | content |
|------|---------|
| `README.md` | Master index with structure, key milestones table, roadmap summary |
| `use-cases/use-cases.md` | 13 internal use cases (IUC-1 through IUC-13) + external validation |
| `use-cases/clusters.md` | Use cases grouped by theme: Secure Coding, Delegated Execution, Persistent Agents, Enterprise Governance |
| `use-cases/sandboxing-modes.md` | Three architectural approaches (whole agent, via APIs, execution only) |
| `use-cases/capability-baseline.md` | Current has/lacks inventory for OpenShell |
| `competitive_positioning/competitors.md` | Index of 11 competitor positioning docs with layer comparison matrix |
| `competitive_positioning/<name>-vs-openshell.md` | Per-competitor deep dives (E2B, Modal, Cloudflare, Docker, ACA, KARS, AHP, Lynx, CubeSandbox, OneCLI, Substrate) |
| `competitive_positioning/external-landscape.md` | Market archetypes and reference architectures |
| `rocks/README.md` | 8 strategic rocks (R1-R8), prioritization inputs, sequencing, operational risks |
| `rocks/r1-*.md` through `rocks/r8-*.md` | Individual rock detail with features and evidence |
| `dev-preview-3.5.md` | DP scope, upstream beta gates, productization work, RFE mapping, cross-Red Hat interest |
| `technology-preview-3.6.md` | TP scope for 3.6 EA1/EA2, upstream beta gates, downstream deliverables, deferred items |
| `weekly-reports/YYYY-MM-DD-openshell.md` | Weekly status reports (April-June 2026 archive) |

## How to use

Re-clone periodically (or `git pull` an existing checkout) to get the
latest strategy updates. Key sections to check on refresh:
- `README.md` key milestones table for date changes
- `rocks/README.md` sequencing section for priority shifts
- `technology-preview-3.6.md` for TP scope changes
- Latest `weekly-reports/` entry for current status
