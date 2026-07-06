---
name: hub.publish
description: Add or update an entry in publish/manifest.yaml to ship an artifact to the public pages site (solaius.github.io/rhoai-agentic-hub-pages). Publishing is a disclosure decision - inline confirm required. Use when the user says "publish this deck/site/page", "make this public", or after an enablement artifact is ready to go live. Also use for removals - "unpublish this", "take this down", "remove from the site".
---

# hub.publish

1. Identify the artifact source — it must live under
   features/<f>/enablement/… (move it there first if not).
2. Draft the manifest entry: source · dest (URL slug — a CONTRACT, never
   changed after shipping; short and stable, e.g. `mcp-gateway/rhcl/`) ·
   audience (`public`; `internal` is schema-reserved and not published in v1)
   · title · description.
3. DISCLOSURE GATE (before ANY manifest edit):
   - Adding/updating: show the entry and state the resulting URL
     `https://solaius.github.io/rhoai-agentic-hub-pages/<dest>` — this
     becomes world-readable. Wait for explicit OK.
   - REMOVING an entry: intentional link breakage — the published copy is
     deleted on the next publish run and old links 404. Confirm twice:
     first the intent, then re-confirm naming the exact dest. Only then edit.
4. Append/update the entry in publish/manifest.yaml, then verify:
   `python scripts/hub_publish.py --check` (must print "manifest valid").
5. Commit + push:
   `git add publish/ features/ && git commit -m "publish: <title>" && git push`
6. Watch CI: `gh run watch --repo solaius/rhoai-agentic-hub --exit-status`,
   then verify live (Pages lag ~1-2 min):
   `curl -sI https://solaius.github.io/rhoai-agentic-hub-pages/<dest> | head -1`
   → 200 for adds/updates; → 404 for a removal.
7. Report the outcome: the live URL for adds/updates, or the confirmed 404
   for removals.
