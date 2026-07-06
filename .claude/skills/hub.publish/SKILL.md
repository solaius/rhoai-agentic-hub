---
name: hub.publish
description: Add or update an entry in publish/manifest.yaml to ship an artifact to the public pages site (solaius.github.io/rhoai-agentic-hub-pages). Publishing is a disclosure decision - inline confirm required. Use when the user says "publish this deck/site/page", "make this public", or after an enablement artifact is ready to go live.
---

# hub.publish

1. Identify the artifact source — it must live under
   features/<f>/enablement/… (move it there first if not).
2. Draft the manifest entry: source · dest (URL slug — a CONTRACT, never
   changed after shipping; short and stable, e.g. `mcp-gateway/rhcl/`) ·
   audience (`public`; `internal` is schema-reserved and not published in v1)
   · title · description.
3. DISCLOSURE GATE: show the entry and state the resulting URL
   `https://solaius.github.io/rhoai-agentic-hub-pages/<dest>` — this becomes
   world-readable. Wait for explicit OK.
4. Append/update the entry in publish/manifest.yaml, then verify:
   `python scripts/hub_publish.py --check` (must print "manifest valid").
5. Commit + push:
   `git add publish/ features/ && git commit -m "publish: <title>" && git push`
6. Watch CI: `gh run watch --repo solaius/rhoai-agentic-hub --exit-status`,
   then verify live (Pages lag ~1-2 min):
   `curl -sI https://solaius.github.io/rhoai-agentic-hub-pages/<dest> | head -1` → 200.
7. Report the live URL. If the user is REMOVING an entry: warn that the
   published copy is deleted on the next publish run and old links will 404 —
   dest removals are intentional breakage, confirm twice.
