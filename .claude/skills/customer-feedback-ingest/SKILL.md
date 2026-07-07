---
name: customer-feedback-ingest
description: Use when adding a new customer or updating an existing customer in the customer interest tracker from a meeting transcription, email thread, Jira ticket, pasted notes, or any source containing customer requirements/interests. Also use when the user says "add this customer", "update the tracker", "ingest this feedback", or shares a new transcription file. All tracker content is restricted (NDA customer data) — this skill only ever writes under restricted/.
---

# Customer Feedback Ingest

Extracts customer interests from a source and adds/updates the customer in the restricted tracker.

## Tracker Location

`restricted/features/platform/work/customer-tracker/customer-interest-tracker.html`

This file lives in the `restricted/` mirror (gitignored, NDA content — see
[memory.md gate item 5](/conventions/memory.md) and the
[restricted/ convention](/conventions/layout.md#restricted)). All source
transcriptions live in
`restricted/features/platform/work/customer-tracker/transcripts/` (named
`transcripts/`, not `transcriptions/`, to match the hub-wide `work/transcripts/`
convention used by every other feature).

The public pointer to this content —
[features/platform/work/customer-tracker/README.md](/features/platform/work/customer-tracker/README.md)
— explains what the tracker is and where the real data lives, for anyone who
finds the empty path in the public tree. It has no customer data in it.

If the restricted directory or the tracker file doesn't exist yet on this
machine, create them as part of the first ingest (see Process step 4) rather
than treating a missing file as an error.

## Source Types

1. **Transcription file** — read from
   `restricted/features/platform/work/customer-tracker/transcripts/`
2. **Email thread** — fetch via Google Workspace MCP (`search_gmail_messages` +
   `get_gmail_thread_content`)
3. **Pasted text** — user pastes content directly
4. **Jira ticket** — fetch via the REST API using the Jira credentials in
   `restricted/.env` (`JIRA_SERVER` / `JIRA_USER` / `JIRA_TOKEN` — see
   `docs/setup.md`)

## Extraction Checklist

From each source, extract:

- **Customer name** and parent company (e.g., "Initech Facilities (parent:
  Contoso Industries)" — a placeholder pattern; use the real name in the
  actual restricted tracker, never in this skill file or in any example you
  add here)
- **Contacts** — names, titles, roles (CTO, architect, PM, etc.)
- **Status** — one of: `ENGAGED`, `EVAL`, `PoC`, `PROD`
- **Interest areas** — map to tracker column headers (see Column Map below)
- **Interest level** per area — `star` (critical/blocking), `filled` (primary), `open` (secondary/mentioned), `dash` (not discussed)
- **Key requirements** — bullet list with bold lead and context
- **Action items** — what, who owns it, status
- **Meeting dates** — with duration and format (in-person, virtual, email)

## Column Map (Interest Matrix)

These are the exact columns in the tracker. Map extracted interests to these:

| Column | What counts |
|--------|------------|
| MCP Gateway | Gateway deployment, virtual MCPs, envoy, RHCL |
| MCP Catalog | Catalog UI, discovery, pre-loaded MCPs |
| MCP Registry | MLflow registry, versioning, governance, spec compliance |
| Lifecycle Operator | MCPLO, deploy/upgrade/monitor MCP servers |
| Zero Trust / OAuth | OAuth 2.0, PKCE, Keycloak, IDP federation, Okta |
| Token Exchange | JWT exchange, short-lived tokens, per-hop tokens |
| Audit Trail / OBO | On-behalf-of, audit logging, agent identity chain |
| Dynamic Client Reg | Self-registration, dynamic client reg with human-in-loop |
| Virtual MCPs / Tool Agg | Virtual MCP servers, tool aggregation behind one endpoint |
| Tool Filtering | Subset tools per role/use-case, RBAC on tools |
| Progressive Disclosure | Tool search, contextual tool surfacing |
| Registry Spec Compliance | MCP Registry Spec, IDE marketplace integration |
| Inference Gateway | Model serving, MAS, external models, VLLM/LLMD |
| AI Grid / Edge | Edge inference, location-aware routing, NVIDIA AI Grid |
| Token Metering | Chargeback, showback, per-user/per-model token tracking |
| Rate Limiting | Quotas, rate limits, subscription tiers |
| Agent Ops | Tracing, evaluation, observability, drift detection |
| Skills / Agent Registry | Skills registry, agent registry, agent catalog |
| Sandboxing | OpenShell, sandbox containers, agentic safety |
| Ingestion Pipeline | Supply chain scanning, signing, certification, partner onboarding |

## Extended Interest Areas (second matrix)

| Column | What counts |
|--------|------------|
| Agent Memory | Context management, enterprise brain, memory-over-MCP |
| Guardrails | Safety guardrails, red teaming, content filtering |
| Cost Controls / Chargeback | Per-engineer spend visibility, billing, chargeback mechanisms |
| Per-User Quota Mgmt | Individual API keys, per-user token quotas |
| Model Routing (cost-aware) | Route to cheaper/local models transparently |
| Context Analysis | Custom context analysis frameworks, prompt analysis |
| Co-Engineering | Joint PoC, co-engineering proposals |

## HTML Symbols

```
&#9733;  = star    — critical / blocking requirement
&#9679;  = filled  — primary interest / active requirement
&#9675;  = open    — mentioned / secondary interest
&#8212;  = dash    — not discussed
```

## Status Tags

```html
<span class="tag tag-poc">PoC</span>
<span class="tag tag-production">PROD</span>
<span class="tag tag-eval">EVAL</span>
<span class="tag tag-engaged">ENGAGED</span>
```

## Process

1. **Read the source** — transcription, email, or pasted text
2. **Read the current tracker** — check if customer already exists
3. **Extract interests** using the checklist above
4. **If new customer:**
   - Add row to Interest Matrix `<tbody>` (match column order exactly)
   - Add row to Extended Interest Areas `<tbody>`
   - Add detail row to Customer Detail table
   - Update summary cards (Active Customers count, Meetings Tracked count)
   - Add to Cross-Customer Themes rows where applicable
   - Add action items to the Action Items table
   - If the tracker file or its parent directories don't exist yet, create
     `restricted/features/platform/work/customer-tracker/` (and
     `transcripts/` alongside it) first — this is expected on a fresh machine,
     not an error condition
5. **If existing customer:**
   - Update interest symbols (only upgrade: dash→open→filled→star, never downgrade)
   - Append new requirements to their detail bullet list
   - Add new action items
   - Update status tag if escalated (EVAL→PoC→PROD)
   - Update meeting list with new meeting
6. **Confirm changes** with the user before finalizing. This is a direct
   write to restricted/ content, not a `hub.capture` write to the tracked
   memory/knowledge store — there is no lint/reindex step and nothing to
   commit to the public repo — but the same discipline applies: show what
   you're about to add or change, wait for the OK, then write.
7. **Knowledge-capture handoff** — if the source material also surfaced a
   durable, non-customer-specific product decision or fact (a gap in the MCP
   Registry spec, a roadmap date change, a competitive signal that
   generalizes beyond this one account), offer `hub.capture` for that item
   separately. Anonymize or generalize it first — the tracker row keeps the
   customer attribution in `restricted/`; the captured knowledge entry should
   only carry customer specifics if it is itself filed under `restricted/`
   (apply the same public/restricted call `hub.capture` would make).

## Related skills

- `customer-feedback-refresh` — periodic audit of this same tracker for
  staleness and accuracy.
- `customer-feedback-sync` — pushes tracker updates to the shared
  cross-PM Google Sheet via the `rhai-tracker` MCP. Run it after a batch of
  ingests if the changes should be visible to other PMs before your next
  scheduled sync.
