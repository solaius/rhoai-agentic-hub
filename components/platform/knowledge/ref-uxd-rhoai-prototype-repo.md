---
type: reference
title: UXD RHOAI prototype repo (GitLab, branch 3.6)
description: UXD team's RHOAI prototype repo -- React/PF6 source for all dashboard pages; the canonical reference for page layout, nav, cards, modals, and CSS patterns; deployed at pages.redhat.com; branch tracks the current release (3.6 as of Aug 2026).
timestamp: 2026-08-03
tags: [platform, uxd, prototype, design, patternfly]
resource: https://gitlab.cee.redhat.com/uxd/prototypes/rhoai
components: [platform]
review_after: 2026-11-03
source: https://gitlab.cee.redhat.com/uxd/prototypes/rhoai
---

UXD team's canonical RHOAI prototype environment.

## Access

- **Repo**: https://gitlab.cee.redhat.com/uxd/prototypes/rhoai
- **Current branch**: `3.6` (default; UXD creates a new branch per release)
- **Deployed**: https://rhoai-deploy-playground-ux-921ee2.pages.redhat.com
- **Visibility**: public (no auth needed for git clone or API)
- **API access**: `curl -sk` (self-signed cert); see memory ref-gitlab-cee-access for config

## Stack

- React 18 + TypeScript + PatternFly 6
- Webpack build (dev/prod configs)
- GitLab Pages deployment

## Repo structure

| Path | What it holds |
|---|---|
| `.design/` | Design context: features/, product/, personas/, key_decisions.md, design-history per feature |
| `src/app/` | Page components: AIHub, GenAIStudio, Settings, DevelopTrain, ObserveMonitor, Projects, Home, etc. |
| `src/app/app.css` | Global CSS overrides -- the source of truth for prototype styling patterns |
| `src/components/` | Shared React components |
| `src/data/` | Mock data for the prototype |
| `src/app/AppLayout/` | Page shell layout (masthead, sidebar, content container) |
| `src/app/routes.tsx` | All prototype routes |

## How to use

For hub.prototype work, this repo provides:
1. **CSS patterns** -- extract computed styles from the deployed site or read `app.css` directly via the GitLab API
2. **Page structure** -- each `src/app/<Feature>/` folder shows the React component composition for that page
3. **Design rationale** -- `.design/features/<name>/design-history.md` explains why UX decisions were made
4. **Mock data shapes** -- `src/data/` and `src/mockData/` show the data structures the UI expects

GitLab API for raw file access:
```
curl -sk "https://gitlab.cee.redhat.com/api/v4/projects/155361/repository/files/<url-encoded-path>/raw?ref=3.6"
```
