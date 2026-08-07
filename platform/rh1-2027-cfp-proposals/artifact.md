---
type: artifact
title: Red Hat One 2027 — CFP Proposal Candidates
description: 11-slide deck presenting 7 deep-technical CFP proposals for RH1 2027, updated per Rosa Guntrip's guidance (deep technical content for hands-on-keyboard roles, not GTM).
timestamp: 2026-08-05
components: [platform, agent-interop, ai-gateway, mcp-gateway, agent-registry, skills-catalog]
---

Slide deck for internal review. Presents 7 deep-technical Red Hat One 2027 CFP
proposals with full submission-ready abstracts, grounded in customer demand (34
accounts), competitive intelligence, and strategic research across the RHOAI
agentic portfolio. Updated per Rosa Guntrip (BU lead) guidance: deep technical
content targeting Consultants, Architects, TAMs, SSAs, SAAs — not GTM topics.
Labs excluded from submission mix. Deadline: August 7, 2026.

## Submission Form Fields

### #1 — From Prototype to Production: Securing and Governing Agents on Red Hat AI
- **Format:** Breakout 45m / Interactive 45m
- **Technical Proficiency:** Technical, advanced
- **Primary Audience:** Technical specialist
- **Industries:** Financial services, Government/public sector
- **Why this format:** The live attack-and-defend demo is the centerpiece — a breakout gives the presenter control over pacing through the three security layers with a dramatic before/after arc. The interactive variant works because attendees can bring their own threat scenarios to test against the model, turning passive learning into hands-on application. A panel would dilute the demo impact; a lab would require environment provisioning that isn't ready.

### #2 — From Discovery to Production: The Complete MCP Ecosystem
- **Format:** Breakout 45m
- **Technical Proficiency:** Technical, intermediate
- **Primary Audience:** Technical specialist
- **Industries:** Financial services, Telecommunications
- **Why this format:** The value is a guided end-to-end walkthrough — Catalog to Operator to Gateway to Studio — where the live demo practically runs itself. A breakout lets the presenter narrate the architectural decisions at each stage (why stateless HTTP, why Kubernetes-native routing) while showing them in action. An interactive or lab format adds complexity without adding insight — attendees need to see the governed flow, not configure it themselves.

### #3 — What Enterprises Are Really Asking About Agents
- **Format:** Panel 45m
- **Technical Proficiency:** Technical, introductory
- **Primary Audience:** Technical seller
- **Industries:** Financial services, Telecommunications, Manufacturing
- **Why this format:** A panel is the only format that delivers on the premise — real field practitioners sharing technical war stories from 34 customer engagements across 11 verticals. A single-speaker breakout would be one person's perspective; a panel surfaces the pattern across verticals and naturally generates the "I saw that too" moments that make content sticky. The second half opens to audience Q&A, turning attendees' own customer scenarios into live coaching. The format also naturally satisfies the Global Sales co-speaker requirement.

### #4 — Red Hat AI Reference Architecture: The Agentic Stack
- **Format:** Breakout 45m / Interactive 120m
- **Technical Proficiency:** Technical, intermediate
- **Primary Audience:** Technical specialist
- **Industries:** Financial services, Telecommunications, Manufacturing
- **Why this format:** The 45-min breakout covers the eight-layer architecture as a guided walkthrough — efficient for attendees who need the mental model. The 120-min interactive is the stronger format: after the architecture walkthrough, attendees whiteboard a real customer scenario, mapping requirements to layers and identifying gaps. That hands-on design exercise is the highest-value activity for architects and consultants who will be designing these stacks for customers.

### #5 — Agent Fleet Lifecycle: Registry, Immutability, and Discovery
- **Format:** Breakout 45m
- **Technical Proficiency:** Technical, advanced
- **Primary Audience:** Technical specialist
- **Industries:** Financial services, Government/public sector
- **Why this format:** This is a deep technical architecture session — OCI packaging formats, cryptographic verification chains, federated discovery protocols. A breakout gives the presenter room to go deep on each layer without time pressure from audience interaction. The statistics (82% found unknown agents, 47% monitored) set up the problem; the architecture walkthrough is the answer. An interactive format would fragment the narrative; the content is too specialized for a panel.

### #6 — AI Supply Chain Under Attack
- **Format:** Breakout 45m
- **Technical Proficiency:** Technical, advanced
- **Primary Audience:** Technical specialist
- **Industries:** Financial services, Government/public sector
- **Why this format:** The session extends a mental model attendees already have (container trust pipelines) into a new domain (AI supply chain). A breakout works because the narrative is linear — threat landscape, then Konflux build pipeline, then scanning, then trust tier distribution — and each section builds on the previous. The live scan catching a malicious skill is a controlled demo moment, not an interactive exercise. Attendees leave with the "AI chapter" of the trust story they already know how to tell.

### #7 — Agent Observability: Tracing Multi-Agent Workflows in Production
- **Format:** Breakout 45m / Interactive 45m
- **Technical Proficiency:** Technical, intermediate
- **Primary Audience:** Technical delivery
- **Industries:** Financial services, Telecommunications
- **Why this format:** The breakout walks through a real distributed trace spanning orchestrator agents, specialist agents, MCP tool calls, and Gateway policy decisions — showing how to read the trace and diagnose silent failures. The interactive variant works because tracing is inherently hands-on: attendees can walk through trace data, identify the failure point in a multi-agent workflow, and build alerting rules. Both formats deliver day-one patterns; the interactive version builds muscle memory.
