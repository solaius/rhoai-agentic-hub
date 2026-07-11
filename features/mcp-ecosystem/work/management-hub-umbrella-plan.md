# Management hub umbrella plan (component-hub build-out)

- **Owner ruling 2026-07-10:** dedicated hubs will be built for the MCP
  Catalog, MCP Lifecycle Operator, and MCP Registry; the Management hub
  becomes the umbrella (cross-component story, referencing them). Slugs
  confirmed and pre-staged in the hub's nav/coming-soon pattern:
  `mcp-catalog/hub/`, `mcp-lifecycle-operator/hub/`, `mcp-registry/hub/`.
- Distilled from the 2026-07-10 design/content review run alongside the
  hub's first `hub.refresh-site` refresh. Apply-now items (12) shipped with
  that refresh; this doc preserves the structural plan.

## Devolution map (page -> destiny once component hubs exist)

Stays (umbrella): index (component directory + timeline), what-is (cross-
component story), ecosystem-architecture (merge candidate with
component-integration), personas, value-prop, end-to-end-setup (reframed:
integration scenarios with mechanics thinned to component-hub links),
component-integration, entitlement (best-of-network subscription matrix;
RHCL skus stub already points here), roadmap (matrix, trimmed), jira-tracker
(rescoped to outcome rollup).

Mostly moves: component-overview (Catalog card -> Catalog hub, MCPLO card ->
MCPLO hub, Registry card -> Registry hub; page becomes a Component
Directory), operator-installation (MCPLO install -> MCPLO hub; Gateway/
Keycloak/Vault -> RHCL; keeps the two-tier model + cross-component version
matrix), configuration-reference (MCPServer CRD -> MCPLO hub; Gateway CRDs ->
RHCL; keeps integration-seam artifacts: dashboard patches,
gen-ai-aa-mcp-servers ConfigMap, namespace label, ownership table).

Splits: reference, customer-stories, competitive, summit-feedback (RHCL
copy wins on the shared Gateway stories/asks), troubleshooting (seam issues
stay), security-model (overview stays, wristband/Vault depth -> RHCL),
lifecycle-flow (7-stage flow stays; Registry governance tables -> Registry
hub), gaps, open-questions (Registry Qs -> Registry hub, partner/catalog Qs
-> Catalog hub, AI Gateway Qs -> link RHCL).

Post-devolution umbrella: ~12-14 pages.

## Sequenced build plan (B-items)

1. Slugs + order: DECIDED. Order: Catalog first (shipped, most seed
   content), then MCPLO (shipped, entitlement questions active), then
   Registry (launches as a design-decision record, grows into the 3.5 DP
   hub in August).
2. Seed each component hub from BOTH parents in one pass: RHCL's
   govern/{catalog,registry,lifecycle-operator}.html (freshest facts, kept
   refreshed by hub.refresh-site) + this hub's component-overview section +
   build/plan fragments per the map above. One move, not two, avoids a
   second divergence window.
3. Per-hub launch conversion (x3): flip comingSoon in nav.js HUB_NETWORK;
   convert coming-soon badges to links (landing card, component directory,
   reference); thin the Management pages listed as moves/split for that
   component; thin the corresponding RHCL govern page to a gateway-vantage
   summary + link.
4. Convert component-overview into the Component Directory page (after all
   three hubs exist).
5. Merge ecosystem-architecture + component-integration into one umbrella
   architecture page (independent; cleanest during 6).
6. Restructure the IA to the umbrella shape (Ecosystem / Components /
   Choose & Integrate / Sell / Plan & Govern) + build the "which component
   do I need?" decision guide (after depth devolves).
7. Reciprocal-link pass across the whole hub network, last.

Dependency chain: 1 -> 2 -> 3 (per component) -> 4/6 -> 7; 5 independent.
Each new hub ships with its own work/refresh-<slug>.yaml so hub.refresh-site
covers it from day one.
