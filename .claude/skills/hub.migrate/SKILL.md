---
name: hub.migrate
description: Bring content over from the old ai-asset-registry repo (read-only source), reshaped to hub conventions - typed entries, canonical URIs, re-timestamped, restricted content routed out, all through the inline gate. Use when the user says "migrate X", "bring over X from the old repo", or when current work touches an old-repo artifact. Also drives the M3 monolith decomposition sessions.
---

# hub.migrate

OLD = C:/Users/peter/code/rh/ai-asset-registry — read-only, never edit it.

## Migrate-on-touch (single item)
1. Locate and read the content in OLD.
2. Reshape per hub conventions: split prose into typed entries
   (decision-/fact-/ref-/person-/question-), or move whole documents into
   features/<f>/{research|strategy|enablement}/ when they have standalone
   value as documents. Story-shaped old-repo content (strategy, pillars,
   connective write-ups) routes to narrative/{knowledge|strategy}/. Every
   derived entry gets `source:` (old repo path or origin URL) and
   `timestamp:` today; likely-stale content additionally gets
   `review_after:` (today + 30d) and a body note saying what to re-verify.
3. Disclosure pass: SKUs, pricing, internal agreements, customer specifics →
   restricted/ mirror. When unsure, ask — this repo is public.
4. Present the whole batch through the inline gate (numbered list, same
   interaction as hub.consolidate step 4).
5. Published HTML artifacts: copy sources into
   features/<f>/enablement/<artifact>/ (or narrative/enablement/ for
   cross-feature ones), add an artifact.md descriptor (type: artifact,
   features: spread), and add the manifest entry via hub.publish. Old URLs
   keep serving from the old repo — never delete there.
6. `python scripts/hub_index.py` && `python scripts/hub_lint.py`; commit
   `migrate(<f>): <what> from ai-asset-registry`; push.

## M3 — monolith decomposition (seeded, multi-session)
Target: OLD/docs/knowledge-registry.md (13 sections). Destination map:
design spec §7.3
(OLD/docs/superpowers/specs/2026-07-05-rhoai-agentic-hub-design.md).
Per session: pick 1-3 sections → extract typed entries → gate → commit.
Fixed routing: §6 release timeline → memory/profiles/roadmap.md (profile
update, not an entry); §6 SKU/pricing + support agreement → restricted/;
§12 source index → ref- entries in their features. Track progress with a
log.md line per session: `**Update** — monolith §N (<name>) migrated`.

## One-time ~/.claude seed (part of M3)
Read C:/Users/peter/.claude/projects/C--Users-peter-code-rh-ai-asset-registry/memory/*.md
and propose still-true items through the gate (most become memory facts or
preference-profile edits). Log when done — that store then retires naturally.
