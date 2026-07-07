---
name: customer-feedback-sync
description: Sync customer tracking data from the local HTML interest tracker to the shared Google Sheet via the rhai-tracker MCP. Use when the user says "sync the tracker", "push to the sheet", "update the shared tracker", "sync customers to gdrive", "compare local vs remote tracker", "diff the trackers", or wants to review what's changed between the local HTML tracker and the team's centralized Google Sheet. Also use when the user has updated the local HTML tracker and wants those changes reflected in the shared sheet, or when they want to see which customers are in one tracker but not the other. Pushing is a disclosure decision to a shared cross-PM system — gated, never automatic.
---

# Customer Feedback Sync

Compares the local HTML customer interest tracker against the shared Google Sheet (rhai-tracker MCP) and pushes new or updated customer data from local to remote.

## Data Sources

- **Local**: `restricted/features/platform/work/customer-tracker/customer-interest-tracker.html`
  — static HTML file with interest matrices, customer details, themes, and
  action items. Restricted/gitignored (NDA content) — see
  [memory.md gate item 5](/conventions/memory.md).
- **Remote**: Google Sheet
  `https://docs.google.com/spreadsheets/d/1Mquc6DUWbtcFisCLDeVMsiPbpeVi-zbIwd4PGGH07mY`
  — centralized team tracker using the rhai-tracker MCP schema, shared across
  PMs. This is the actual cross-machine, cross-PM source of truth; the local
  HTML file is this machine's working copy.

## Prerequisites

- **`rhai-tracker` MCP server connected** — registered in this repo's root
  `.mcp.json` (gitignored, machine-specific) and wired up by `hub.doctor`
  (`bash scripts/doctor.sh setup`, section 7). That setup step clones the
  sibling `c-track` repo (the actual tracker app + MCP server, kept as its own
  repo — it is shared team tooling, not hub content), installs its Node
  dependencies, and scaffolds its `server/.env`. A restart of Claude Code is
  required after the MCP server is registered or changed — see `hub.doctor`.
  Provides `list_interactions`, `batch_import_interactions`, etc.
- **`google-workspace` MCP server connected** (for reading sheet values
  directly if needed)
- **Local HTML tracker exists** at the path above — if not, run
  `customer-feedback-ingest` first to create it

## Workflow

### Phase 1: Read Both Sources

1. **Read the local HTML tracker** — parse all customer rows from:
   - Interest Matrix (`<tbody>` rows with 20 capability columns)
   - Extended Interest Areas (7 more columns)
   - Customer Detail & Key Requirements (contacts, status, timeline, requirements, meetings)
   - Cross-Customer Themes
   - Open Action Items

2. **Read the remote sheet** — use `list_interactions` filtered to the target component (default: `Agentic`) to get all existing rows. This returns the rhai-tracker schema: customerCompany, contactName, fieldContactName, industryVertical, geo, customerType, mainAIUseCase, toolsOfChoice, environment, painPoints, featureFeedback, futureWishlist, pmComments, status.

### Phase 2: Diff

Compare the two datasets by `customerCompany` name. Produce three categories:

| Category | Meaning |
|----------|---------|
| **New** | In local tracker but not in remote sheet (for this component) |
| **Updated** | In both, but local has newer/richer data |
| **Remote-only** | In remote sheet but not in local tracker (flag, don't delete) |

For **Updated** detection, compare these fields and flag when local has more content:
- contactName / fieldContactName — local has names not in remote
- painPoints — local has requirements not captured in remote
- featureFeedback — local has feedback not in remote
- futureWishlist — local has items not in remote list
- pmComments — local has meeting notes or context not in remote
- status — local status is different from remote

When detecting updates, the comparison is directional — local is the source of truth for MCP/agentic customer data. If local has *more* content than remote, that's an update. If remote has content that local doesn't, that's fine (another PM may have added it). The `batch_import_interactions` upsert merges on `customerCompany + component`, so pushing an update won't erase fields that only exist in the remote.

For text fields (painPoints, featureFeedback, pmComments), do a substring check — if the remote already contains the local text (or vice versa), it's not a meaningful update. Only flag changes where the local has substantively new information.

### Phase 3: Present Diff to User

Show a clear summary table (customer names below are placeholders illustrating
the shape — use the real names from the actual restricted tracker):

```
## Sync Summary: Local → Sheet (Agentic)

### New Customers (3)
| Customer            | Industry | Status | Key Interests |
|----------------------|------|--------|---------------|
| Acme Manufacturing    | Mfg  | Eval   | MCP Registry, Zero Trust, Sandboxing |
| ...                   | ...  | ...    | ... |

### Updated Customers (2)
| Customer         | Changed Fields | Details |
|-------------------|---------------|---------|
| Stark Communications | pmComments, painPoints | New meeting notes from 2026-06-08 |
| ...                | ... | ... |

### Remote-Only (not in local tracker) (1)
| Customer               | Component | Notes |
|-------------------------|-----------|-------|
| Massive Dynamic Capital | Agentic   | May be tracked by another PM |
```

This table is the gate artifact for Phase 4 — see Push Gate below before
acting on it.

### Phase 4: Push Approved Changes

Use `batch_import_interactions` with `defaultComponent` set to the target component. The MCP does upsert — it matches on `customerCompany + component` and merges, so existing data won't be lost.

## Push Gate (before ANY write to the shared sheet)

Pushing writes into a system other PMs read and rely on — treat it with the
same discipline as `hub.publish`'s disclosure gate, even though this doesn't
go through `publish/manifest.yaml`:

1. **Show the diff table** from Phase 3 in full — every new and updated
   customer, with the changed fields called out.
2. **State plainly** that this writes to the shared cross-PM Google Sheet,
   not just local state.
3. **Wait for explicit confirmation.** "Push all N changes" or an explicit
   subset ("just Acme Manufacturing and Wayne Banking") both count. Silence,
   a topic change, or an ambiguous reply do not — ask again rather than
   assume.
4. **If the user selects a subset**, read the exact list back before calling
   `batch_import_interactions` so there's no ambiguity about what ships.
5. **Never delete or overwrite.** The upsert-merge behavior (Phase 2) means a
   push can only add/enrich rows, never remove remote-only data — that
   safety property is why this gate can be a single confirm rather than the
   two-step confirm `hub.publish` uses for removals. If a future need arises
   to *remove* a customer from the shared sheet, that is out of scope for
   this skill and needs its own explicit, separately-confirmed path.
6. **After pushing**, report the outcome precisely: counts created vs.
   updated, and which customers — the same "report the outcome" discipline
   `hub.publish` uses for its live-URL confirmation.
7. **New customer intel is restricted-bar content** (customer-named, per
   [memory.md gate item 5](/conventions/memory.md)) even once it lives in the
   external sheet — never quote real customer specifics into a `hub.capture`
   entry, a commit message, or anything else that lands in this repo's public
   tree while doing this work.

## Field Mapping: HTML → rhai-tracker

This is the core transformation. For each customer row in the HTML tracker:

| rhai-tracker Field | Source in HTML |
|-------------------|---------------|
| `customerCompany` | Customer name from first `<td>` (e.g., "Acme Manufacturing", "Initech Facilities (Contoso)" — placeholders; use the real name) |
| `contactName` | `<span class="client-detail">` text from Interest Matrix row |
| `fieldContactName` | `<span class="client-detail">` text from Customer Detail row (the "Account:" line) |
| `industryVertical` | Infer from context or `<span class="client-detail">` (map to enum — see below) |
| `geo` | Infer from customer context (default NA for US companies, APAC for NZ/AU, EMEA for EU) |
| `customerType` | Default "SSA" unless context says otherwise |
| `mainAIUseCase` | Synthesize from Key Requirements — the 1-2 line summary of what they want |
| `toolsOfChoice` | Extract tool/product names mentioned in requirements (Devin, Windsurf, Konveyor, etc.) |
| `environment` | Infer if mentioned (air-gapped, GCP, AWS, Azure, on-prem) |
| `painPoints` | Blockers, concerns, and problems from Key Requirements bullets |
| `featureFeedback` | Capability interests with interest levels from the Interest Matrix (critical/primary areas) |
| `futureWishlist` | Wishlist items — features they want that don't exist yet |
| `pmComments` | Status/Timeline text + Meeting list + Action Items for this customer |
| `status` | Map HTML tag → rhai-tracker status (see below) |

### Status Mapping

| HTML Tag | rhai-tracker Status |
|----------|-------------------|
| `PROD` | `Evaluating` |
| `PoC` | `Evaluating` |
| `ENGAGED` | `Discovery` |
| `EVAL` (with substantive detail) | `Evaluating` |
| `EVAL` (minimal context) | `Lead` |

### Industry Mapping

| Context Clues | industryVertical |
|--------------|-----------------|
| Bank, financial services, trading | Banking & Financial Services |
| Telco, carrier, network, 5G | Telco |
| Defense, aerospace, military, government | Federal |
| Manufacturing, hardware, facility mgmt | Manufacturing |
| Insurance, healthcare, pharma | Insurance & Healthcare |
| Retail, e-commerce | Retail |
| Media, entertainment, streaming | Media & Entertainment |
| University, research, education | Research & Education |
| Energy, utilities, oil & gas | Energy & Utilities |

### Interest Level Symbols

When building `featureFeedback`, translate HTML symbols into readable text:

```
★ (&#9733;) → "(critical)" — blocking requirement
● (&#9679;) → "(primary)" — active requirement
○ (&#9675;) → "(secondary)" — mentioned interest
— (&#8212;) → omit — not discussed
```

Include only areas where the customer showed primary or critical interest. Secondary interests can go into `futureWishlist` if they represent future wants.

## Component Selection

Default to **Agentic** for customers tracked in this HTML file (MCP/agentic use cases). If the user specifies a different component, use that instead. The valid components are:

- Project Navigator
- AutoX
- AI Platform
- D2MA
- Agentic
- Inferencing

If a customer's interests clearly span multiple components (e.g., a telecom
account has Inferencing interests alongside Agentic), note this in
`pmComments` but only create one row per sync under the target component. The user can run a second sync for a different component if needed.

## Error Handling

- If the local HTML tracker doesn't exist, tell the user and suggest using `customer-feedback-ingest` to create it first
- If the rhai-tracker MCP isn't connected, tell the user to run `hub.doctor`
  (`bash scripts/doctor.sh check`, then `setup` if needed — section 7 covers
  the tracker MCP specifically) and restart Claude Code; in the meantime,
  fall back to `google-workspace` MCP's `read_sheet_values` for reading and
  `modify_sheet_values` for writing (use the sheet URL above)
- If a customer name in the sheet has a slight variant (e.g., "Wayne Banking" vs "Wayne Banking (NZ)"), flag it for the user to confirm whether they're the same customer

## Example Interaction

Customer names below are placeholders illustrating the flow — the real
interaction works the same way against the actual restricted tracker.

```
User: sync the tracker to the sheet

Claude: [Reads local HTML tracker — finds 9 customers]
        [Reads remote sheet via list_interactions(component=Agentic) — finds 5 customers]
        [Presents diff:]

        ## Sync Summary: Local → Sheet (Agentic)

        ### New Customers (4)
        | Customer              | Industry | Status |
        |------------------------|----------|--------|
        | Acme Manufacturing      | Mfg      | Evaluating |
        | Globex Telecom          | Telco    | Discovery  |
        | Initech Facilities      | Mfg      | Discovery  |
        | Wayne Banking           | Banking  | Discovery  |

        ### Updated Customers (2)
        | Customer            | Changed Fields |
        |-----------------------|---------------|
        | Stark Communications   | New meeting notes |

        This pushes to the shared cross-PM sheet — push all 6 changes? Or select specific ones?

User: push all

Claude: [Calls batch_import_interactions with 6 customers, defaultComponent=Agentic]
        Done — 4 created, 2 updated.
```

## Related skills

- `customer-feedback-ingest` — the local write path this skill reads from.
- `customer-feedback-refresh` — run before a sync to clean up staleness first,
  so what ships to the shared sheet is accurate.
