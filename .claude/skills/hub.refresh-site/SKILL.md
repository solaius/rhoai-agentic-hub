---
name: hub.refresh-site
description: Refresh a published enablement hub site (RHCL hub, Management hub, or any site with a work/refresh-<slug>.yaml config) from its live sources - GDocs, GitHub, Jira, Slack, and local hub entries. Sweeps for changes, proposes page-level diffs through the inline gate, applies surgical edits, bumps data-verified footers, re-runs the disclosure net, and republishes. Use when the user says "refresh the rhcl hub", "update the management hub", "refresh the site", or when data-verified dates look stale.
---

# hub.refresh-site

Config-driven successor to the old repo's update-*-hub skills. One config per
site: `features/<f>/work/refresh-<slug>.yaml` (or `narrative/work/...`),
validated by hub_lint. Never auto-commits. THE DISCLOSURE CONTRACT (step 6)
is what the old skills lacked: they swept customer names IN; this skill
keeps them OUT.

1. TARGET. Resolve the site from the request; if ambiguous, list configs
   (`features/*/work/refresh-*.yaml`, `narrative/work/refresh-*.yaml`) and
   ask. Read the config, the site's artifact.md, and the current pages.
2. STALENESS. Grep `data-verified` across the site's HTML; report per page,
   oldest first. The oldest date is the sweep-since baseline.
3. SWEEP (parallel subagents, one per source type; each returns findings as
   structured notes, never edits):
   - gdocs: google-workspace `get_doc_as_markdown` with `include_comments`
     true, `user_google_email: pedouble@redhat.com`.
   - github: `gh` CLI - releases, commits, README/doc changes since baseline.
   - jira: stored `work/jira-snapshot.yaml` plus live check via
     `python scripts/hub_jira.py` / `hublib/jira.py` (keys and jql from the
     config).
   - slack: channel history over `window_days` via the slack MCP.
   - local: the hub knowledge/research paths listed in the config.
   Any unreachable source (Slack tokens expire; VPN) degrades to a "Fetch
   failures" report section - the run continues.
4. CHANGE REPORT. Categorized: New / Changed / Confirmed-current / Fetch
   failures. Every finding names the page(s) it affects. Live source wins
   over stale page content.
5. GATE. Batch approval: apply all / by number / skip / show diff. Wait for
   the owner. Nothing is written before this.
6. APPLY + DISCLOSURE CONTRACT (non-negotiable):
   - Surgical in-place HTML edits; never rebuild a page. Keep nav.js
     SITE_MAP consistent if a page is added or retitled.
   - NEVER introduce customer or partner names, engagement pricing, or deal
     detail. Use anonymized phrasing ("large enterprise OEM customer",
     "major telecommunications provider").
   - Product naming: full name on first use per page ("RHOAI restricted use
     entitlement for OpenShift"), short form after.
   - No em dashes in newly written content.
   - Bump `data-verified` to today on every page swept-and-updated or
     swept-and-confirmed; leave unswept pages' dates alone.
   - Bump the site's artifact.md `timestamp`.
   - `python scripts/hub_lint.py` must report 0 errors before commit
     (restricted-pattern hits are hard blockers - fix content, never bypass).
7. COMMIT + REPUBLISH. Commit `refresh(<slug>): <summary>` with a bulleted
   body of applied changes; push; resolve the run id with
   `gh run list --repo solaius/rhoai-agentic-hub --workflow publish.yml --limit 1 --json databaseId -q '.[0].databaseId'`
   then `gh run watch <id> --repo solaius/rhoai-agentic-hub --exit-status`
   (publish.yml republishes and runs the link gate - CI is the link-check
   authority; local checks false-positive on cross-hub links). Report the
   live URL.
8. Offer hub.capture for a memory log line summarizing the refresh.
