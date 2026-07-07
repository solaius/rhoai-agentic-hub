---
title: Adversarial Memory & Context Integrity
description: Threat model for agent memory systems -- attack vectors, real-world incidents, defense taxonomy, and security architecture recommendations.
source: ai-asset-registry/agent-memory/research/11-adversarial-memory.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Adversarial Memory & Context Integrity

**Purpose:** Threat model for agent memory systems — attack vectors, real-world incidents, defense taxonomy, and security architecture recommendations for the RHOAI Agent Memory workstream.

**Date:** 2026-06-09

**Status:** EXPLORATORY — Phase 2 research. See [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345).

**Series:** Document 11 of 17 — Agent Memory & Knowledge Research
**Phase 1:** [00](00-executive-summary.md) · [01](01-landscape-and-definitions.md) · [02](02-solution-survey.md) · [03](03-memoryhub-deep-dive.md) · [04](04-technical-patterns.md) · [05](05-standards-and-protocols.md) · [06](06-ogx-memory-primitives.md) · [07](07-taxonomy-and-decomposition.md) · [08](08-rhoai-ocp-alignment.md)
**Phase 2:** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · 11 Adversarial Memory (this doc) · [12](12-benchmarking-evaluation.md) · [13](13-kv-cache-optimization.md) · [14](14-enterprise-use-cases.md) · [15](15-multi-modal-memory.md) · [16](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)

---

## Contents

1. [Why Memory Security is a Distinct Problem](#1-why-memory-security-is-a-distinct-problem)
2. [OWASP ASI06 — Memory & Context Poisoning](#2-owasp-asi06--memory--context-poisoning)
3. [Attack Taxonomy](#3-attack-taxonomy)
4. [Real-World Incidents](#4-real-world-incidents)
5. [Non-Adversarial Degradation Threats](#5-non-adversarial-degradation-threats)
6. [Defense Taxonomy](#6-defense-taxonomy)
7. [The Mnemonic Sovereignty Framework](#7-the-mnemonic-sovereignty-framework)
8. [RHOAI Implications and Architecture Recommendations](#8-rhoai-implications-and-architecture-recommendations)
9. [Open Questions for the Review Gate](#9-open-questions-for-the-review-gate)
10. [Sources](#10-sources)

---

## 1. Why Memory Security is a Distinct Problem

**REFERENCE** — Stateless LLM applications have a bounded threat surface: an attacker can manipulate a single request-response pair, but the damage does not persist. Once the context window closes, the attack is over. Memory changes this calculus fundamentally.

When an agent retains state across sessions — episodic logs, semantic facts, procedural preferences, shared organizational context — three new properties emerge that create security concerns absent in stateless systems:

1. **Persistence.** A single successful injection can corrupt all future reasoning. The attack and its effect are temporally decoupled — the injection happens in February, the damage manifests in April, and the attacker is long gone.

2. **Propagation.** In multi-agent systems, poisoned memory can spread through shared memory stores, inter-agent messages, and tool arguments. A single compromised agent can contaminate downstream agents that never encountered the original malicious input.

3. **Implicit trust.** Agents trust their own memories. There is no external reference to validate against — the memories *are* the agent's reality. This makes poisoned beliefs operationally indistinguishable from legitimate context.

These properties map directly to the memory lifecycle from [04 Technical Patterns](04-technical-patterns.md) §1: `read-before-reasoning -> reason-and-plan -> act -> observe -> write-after-acting -> loop`. Every phase of this loop is an attack surface when memory is persistent and writable at runtime.

**Relationship to prior documents.** This document extends the governance analysis in [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md) §5 (cross-cutting governance dimension) and the RHOAI alignment in [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md) §2.1 (registry-as-governance). Where doc 07 treats governance as a design requirement, this document treats it as a *security* requirement — driven by concrete attack vectors rather than compliance abstractions.

---

## 2. OWASP ASI06 — Memory & Context Poisoning

**REFERENCE** — The OWASP Top 10 for Agentic Applications (2026) is a peer-reviewed framework developed with input from over 100 security researchers. ASI06 is the sixth entry, focused on memory and context poisoning.

### 2.1 Classification and Severity

ASI06 builds on three entries from the OWASP LLM Top 10 (2025):
- **LLM01:2025** — Prompt Injection (the root input-manipulation vector)
- **LLM04:2025** — Data and Model Poisoning (the training-time analogue)
- **LLM08:2025** — Vector and Embedding Weaknesses (the retrieval-layer substrate)

ASI06 extends these by focusing on *persistent corruption that propagates across sessions, agents, and tenants*. The distinction is critical: LLM01 describes a single-turn exploit; ASI06 describes the same exploit achieving indefinite persistence through the memory layer.

### 2.2 The Full OWASP ASI Top 10 (2026)

For context, the complete agentic threat landscape:

| # | Risk | Memory Relevance |
|---|---|---|
| ASI01 | Agent Goal Hijack | Memory poisoning is a *mechanism* for goal hijack |
| ASI02 | Tool Misuse & Exploitation | MemMorph shows tool hijacking *via* memory poisoning |
| ASI03 | Agent Identity & Privilege Abuse | Cross-scope memory bleed enables privilege escalation |
| ASI04 | Agentic Supply Chain Compromise | Poisoned dependencies can inject memories at install time |
| ASI05 | Unexpected Code Execution | Poisoned procedural memory can encode unsafe code patterns |
| **ASI06** | **Memory & Context Poisoning** | **Primary entry — this document** |
| ASI07 | Insecure Inter-Agent Communication | Memory propagation across agents |
| ASI08 | Cascading Agent Failures | Memory corruption can cascade through agent graphs |
| ASI09 | Human-Agent Trust Exploitation | Poisoned memory undermines human oversight |
| ASI10 | Rogue Agents | Persistent memory compromise can create rogue behavior |

### 2.3 Industry Adoption

ASI06 has achieved rapid industry adoption:
- **Microsoft** agent-governance-toolkit has an open issue for ASI06 detection mechanisms (strategic priority Q3 2026)
- **NVIDIA** Safety and Security Framework references the OWASP Agentic Threat Modelling Guide
- **AWS** prescriptive guidance recommends memory isolation policies and anomaly detection for agentic memory operations
- **Microsoft SDL for AI** (February 2026) specifically calls out AI memory protections and RBAC for multi-agent environments
- **OWASP Agent Memory Guard** project provides the reference implementation (see Section 6.1)

---

## 3. Attack Taxonomy

**EXPLORATORY** — This section catalogs six primary attack vectors against agent memory systems, organized by attack mechanism and escalating in sophistication. Each vector is grounded in published research.

### 3.1 SpAIware — Persistent Memory Injection via Prompt Injection

**Source:** Rehberger (2024), published in *Future Generation Computer Systems* (ACM Digital Library).

**Mechanism.** The attacker embeds instructions in places the agent will read on the user's behalf — a shared document, a markdown file in a repository, a webpage summarized via a browser tool, or a PDF. When the agent processes this content, it writes attacker-controlled instructions to its own long-term memory. Once stored, those instructions re-execute in every future conversation.

**Attack chain:**
1. Attacker plants instructions in an untrusted document
2. User asks agent to summarize or analyze the document
3. Agent's memory feature stores attacker instructions as "learned preferences"
4. All future sessions inherit the poisoned instructions
5. Continuous data exfiltration, biased responses, or workflow hijacking ensues

**Key property:** The attack is *one-to-many* — a single exposure produces ongoing compromise across all future sessions. The poisoned memory persists until manually discovered and removed.

**Demonstrated against:** ChatGPT (May-September 2024), Gemini (February 2025), Claude (April 2026).

### 3.2 PoisonedRAG — Knowledge Corpus Poisoning

**Source:** Zou et al. (2024), USENIX Security 2025. Code: [GitHub](https://github.com/sleeepeer/PoisonedRAG).

**Mechanism.** The attacker injects a small number of malicious texts into the knowledge database of a RAG system to force the LLM to generate an attacker-chosen target answer for an attacker-chosen target question. The attack is formulated as an optimization problem: craft texts that satisfy both a *retrieval condition* (the text is retrieved for the target question) and a *generation condition* (the LLM produces the target answer given the poisoned context).

**Key results:**
- 90% attack success rate with only 5 malicious texts injected into a corpus of millions
- Effective in both black-box and white-box settings
- Existing defenses (perplexity-based detection, query rewriting, increasing retrieval count) are insufficient

**Memory relevance.** PoisonedRAG targets the *semantic memory* and *knowledge* layers of the doc-07 decomposition ([07](07-taxonomy-and-decomposition.md) §4.1, Subsystems 1 and 3). Any RHOAI memory system that stores agent knowledge in a vector database is vulnerable to this class of attack. The follow-up work Poisoned-MRAG extends the concept to multimodal RAG systems.

### 3.3 MINJA — Memory INJection Attack via Query-Only Interaction

**Source:** Dong et al. (2025), NeurIPS 2025. arXiv: [2503.03704](https://arxiv.org/abs/2503.03704).

**Mechanism.** MINJA demonstrates that an attacker can inject malicious records into an agent's memory bank *solely by interacting with the agent via queries and observing outputs* — no direct memory access, no elevated privileges, no trigger injection into other users' queries. The attack introduces a sequence of bridging steps to link the victim query to malicious reasoning steps, using a progressive shortening strategy that gradually removes the indication prompt so the malicious record persists cleanly.

**Key results:**
- 98.2% injection success rate
- 76.8% attack success rate
- Validated across diverse agent architectures

**Why this matters for RHOAI.** MINJA's threat model is realistic for enterprise deployments: the attacker is a normal user of the system with no special privileges. Any multi-tenant RHOAI memory service where users share a memory store (even at different scope tiers) is potentially vulnerable. The attack is particularly severe in high-stakes domains — the arXiv paper [2601.05504](https://arxiv.org/abs/2601.05504) validates MINJA against Electronic Health Record (EHR) agents using clinical data.

### 3.4 MemoryGraft — Procedural Poisoning via Experience Retrieval

**Source:** Srivastava & He (December 2025). arXiv: [2512.16962](https://arxiv.org/abs/2512.16962).

**Mechanism.** Unlike SpAIware (which poisons factual memory) and MINJA (which poisons reasoning chains), MemoryGraft targets *procedural* memory — the agent's learned patterns of successful behavior. The attacker implants malicious "successful experiences" (benign-appearing documentation embedding unsafe procedures disguised as validated best practices) into the agent's long-term memory via standard ingestion channels (README files, project documentation, code comments).

**Key property — procedural vs. factual poisoning.** Defense strategies that focus exclusively on factual verification will miss procedural poisoning entirely. The agent does not "know wrong things" — it has "learned bad habits." A poisoned system might skip validation steps, run remote scripts, or insert backdoors into generated code, all while believing it is following established best practices.

**Key results:**
- Poisoned records account for ~48% of retrieved experiences on matching tasks
- Increasing retrieval k from 1 to 5 raised poisoned retrieval proportion from ~32% to ~55%
- Both lexical (BM25) and embedding (FAISS) retrieval strategies are vulnerable
- Validated on MetaGPT's DataInterpreter agent with GPT-4o

### 3.5 MemMorph — Tool Hijacking via Memory Poisoning

**Source:** Zhang et al. (May 2026). arXiv: [2605.26154](https://arxiv.org/abs/2605.26154).

**Mechanism.** MemMorph is the first attack that biases *tool selection* by poisoning memory. Rather than dictating tool invocation directly, it injects a small number of crafted records disguised as technical facts, incident reports, and operational policies. These reshape the agent's contextual perception, leading it to autonomously infer and select the attacker's preferred tool. Records are generated in three CoALA-taxonomy styles: factual, episodic, and policy.

**Key results:**
- Up to 85.9% attack success rate with only 3 injected records
- Outperforms the strongest baseline by up to 25%
- Retains potency under 3 representative defenses — even the best defense (Memory Auditor) only reduces ASR by 23.7%, leaving over half the tasks compromised

**RHOAI relevance.** MemMorph is directly relevant to the MCP ecosystem: if an agent uses memory to learn tool preferences and a poisoned memory entry steers it toward a malicious MCP server instead of the legitimate one, the attacker achieves remote code execution through a governance bypass. This reinforces the doc-08 argument that memory governance and MCP governance must be architecturally coupled ([08](08-rhoai-ocp-alignment.md) §2.2).

### 3.6 Sleeper Memory Poisoning — Dormant Triggers

**Source:** arXiv: [2605.15338](https://arxiv.org/abs/2605.15338) (May 2026). Industry analysis: Christian Schneider (2026), StellarCyber (2026).

**Mechanism.** The attacker plants instructions that are *dormant* — they sit in the memory store without being retrieved or activated until a specific trigger condition is met (a date, a keyword, a user role, a task type). The temporal decoupling between injection and activation makes detection extremely difficult: security monitoring at injection time sees nothing suspicious, and monitoring at activation time sees a legitimate-looking retrieval from trusted memory.

**Key properties:**
- Attack and execution are temporally decoupled (injection in February, damage in April)
- Traditional monitoring sees nothing suspicious at any single point in time
- Triggers embedded in one agent stage propagate via recurrent updates: memory persistence rate 77.97%, planning persistence 43.58%, tool-use persistence 60.28%

**Defense complexity.** Sleeper attacks are resistant to point-in-time evaluation. The Agent Security Bench evaluated 27 attack/defense combinations across 400+ tools and found an 84.30% average attack success rate. AgentPoison maintains over 80% success at under 0.1% poison rate. Time-To-Live (TTL) enforcement of 30 days on untrusted memory categories is the most effective practical mitigation identified to date.

### 3.7 Attack Surface Summary

| Attack Vector | Memory Type Targeted | Attacker Privilege | Persistence | Detection Difficulty |
|---|---|---|---|---|
| SpAIware | All (via prompt injection) | User-level (document access) | Cross-session | Medium — memory content inspection |
| PoisonedRAG | Semantic / Knowledge | Corpus write access | Permanent until corpus cleaned | High — blends with legitimate content |
| MINJA | Episodic / Semantic | Query-only (no write access) | Cross-session | Very High — no direct memory manipulation |
| MemoryGraft | Procedural | Document ingestion channel | Cross-session, cross-agent | Very High — indistinguishable from good practices |
| MemMorph | Tool preferences (procedural) | Memory write or ingestion | Cross-session | High — semantically fluent records |
| Sleeper Poisoning | Any | Varies | Dormant until triggered | Extreme — temporally decoupled |

---

## 4. Real-World Incidents

**REFERENCE** — The following incidents are drawn exclusively from public disclosures. No confidential engagement details are included.

### 4.1 ChatGPT Memory Exploits (2024-2025)

| Date | Incident | Impact | Remediation |
|---|---|---|---|
| May 2024 | Rehberger reports memory injection via prompt injection to OpenAI | Ticket closed as "model safety issue, not security" | None initially |
| Sep 2024 | SpAIware end-to-end exploit demonstrated — persistent data exfiltration beyond single chat session | Arbitrary data exfiltration across all future sessions | OpenAI patches ChatGPT v1.2024.247; exfiltration vector closed |
| Oct 2025 | ChatGPT Atlas "Tainted Memories" — CSRF flaw allows injection into persistent memory via browser | Cross-device, cross-session persistence; malware deployment possible | LayerX Security disclosure; OpenAI patch |
| Nov 2025 | HackedGPT — Tenable identifies 7 critical vulnerabilities including persistent memory injection | 0-click attacks; silent exfiltration without user interaction; several flaws persist in ChatGPT-5 | Partial remediation; some flaws still present |

### 4.2 Google Gemini Memory Exploits (2025-2026)

| Date | Incident | Impact | Remediation |
|---|---|---|---|
| Feb 2025 | Rehberger demonstrates document-based memory injection in Gemini | False memories persist across sessions ("user is 102 years old, believes in flat earth") | Google acknowledgment; mitigation deployed |
| Aug-Nov 2025 | SafeBreach demonstrates voice assistant memory poisoning via WhatsApp, Slack, SMS, Signal | Long-term memory poisoning propagating across all user devices; scheduled surveillance established | Google VRP confirmation; content classifier updates deployed Nov 2025 |
| Jan 2026 | Gemini calendar data exfiltration via routine invitations (Miggo) | Private meeting details copied to attacker-visible events | Google patch |
| 2025-2026 | Russian threat actor uses jailbroken Gemini with persistent memory for credential cracking and crypto theft | Memory file auto-reloaded at session start; AI self-reinforced its own jailbreak over time; 29 WordPress admin accounts compromised | TrendAI disclosure May 2026 |

### 4.3 Anthropic MCP Vulnerabilities (2025)

Three prompt injection vulnerabilities were identified in Anthropic's official Git server for MCP (mcp-server-git). An attacker only needed to influence what an AI assistant reads — such as a malicious README file — to trigger the vulnerabilities. No credentials or system access were required. Anthropic accepted the reports in September 2025 and released fixes in December 2025.

**Pattern.** The MCP vulnerability is architecturally identical to the MemoryGraft attack pattern: a poisoned repository artifact (README) influences agent behavior through a standard ingestion channel. This validates the threat model for any system that auto-ingests project documentation.

### 4.4 MemoryTrap — Cisco Research on Claude Code (2026)

Cisco researchers discovered the "MemoryTrap" vulnerability in Claude Code, where a routine developer workflow — clone a repository, let the agent help, approve a dependency installation — could result in persistent prompt injection. Once malicious content reached trusted surfaces (memory, hooks, configuration), the attacker influenced not just one response but all future reasoning. OWASP cited this as a canonical example of ASI06.

### 4.5 Pattern Analysis

Across all documented incidents, the attack chain follows a consistent four-step pattern:

```
1. PLANT    — Attacker embeds instructions in a document/repo/message the agent will process
2. INGEST   — Agent processes the content via a standard workflow (summarize, analyze, browse)
3. PERSIST  — Agent's memory feature stores the malicious instructions as legitimate context
4. ACTIVATE — All future sessions inherit and execute the poisoned instructions
```

No exotic exploits are required. The fundamental problem — that LLMs cannot reliably distinguish data from instructions — remains an open research question. Every vendor (OpenAI, Google, Anthropic) has shipped mitigations, but none are comprehensive.

---

## 5. Non-Adversarial Degradation Threats

**EXPLORATORY** — Not all memory integrity threats require an adversary. Two categories of degradation emerge from normal operation and are architecturally significant for RHOAI.

### 5.1 Context Rot — Gradual Quality Degradation

**Source:** Redis (December 2025), Chroma (2026), MindStudio (April 2026), Paulsen (2025), Veseli et al. (2025).

Context rot is performance degradation that occurs as context grows over time, even without malicious input. It manifests through:

- **Positional bias ("lost in the middle").** Models work best when relevant information is at the beginning or end of context; they struggle when it is buried in the middle (Stanford, 2024). Paulsen (2025) showed degradation across task types with far fewer tokens than expected. Veseli et al. (2025) found that beyond 50% context utilization, performance degrades by distance from the end.
- **Error compounding.** Each agent response becomes part of the context for the next. Small mistakes get baked into context and compound — a 2% accuracy degradation per reasoning step produces ~40% failure rates over a 20-step workflow. MemU reports that 65% of enterprise AI agent failures in 2025 were attributed to context drift, not context exhaustion.
- **Summarization laundering.** Compression/summarization — the standard scaling lever for long-running agents — is itself part of the attack surface. Summaries strip the nuance that safety classifiers need, effectively laundering unsafe content into trusted context.

**Memory lifecycle impact.** Context rot creates a *non-adversarial analogue* to sleeper poisoning: no attacker is needed, but the agent's behavior drifts unsafe over time simply because of accumulated context. The Cloud Security Alliance formalized "Cognitive Degradation Resilience" as a distinct safety property in late 2025.

### 5.2 Temporal Memory Contamination — Longitudinal Safety Drift

**Source:** Al-Tawaha et al. (May 2026, arXiv: 2605.17830), Lin et al. (April 2026, arXiv: 2604.16548).

Three recent arXiv papers converge on a finding that is complementary to adversarial memory poisoning: *memory-equipped agents drift unsafe as benign context accumulates, even when no adversarial actor is involved.* This is what the literature calls "temporal memory contamination."

Key findings:
- Memory-enabled agents consistently exceed the NullMemory (no-memory) baseline in safety violation rates across eight memory architectures
- Safety is a property of the trajectory (the accumulated memory state), not of any individual prompt-response pair
- A memory snapshot can pass every existing benchmark and the agent can still drift unsafe after enough sessions accumulate
- Single-turn or single-session red-team harnesses are blind to this class of failure

**RHOAI implication.** Any RHOAI memory system that lacks longitudinal safety evaluation is vulnerable to this class of degradation. Point-in-time compliance checks are necessary but not sufficient. The RFE-M6 audit trail must support trajectory-level analysis, not just individual write-event logging.

### 5.3 Cross-Boundary Bleed — Information Leaking Between Scopes

**Source:** Giskard (2025), OpenClaw/Mem0 (2026), arXiv: 2512.04668 (MAMA framework).

Cross-boundary bleed occurs when memory state leaks between isolation boundaries — between users in a multi-tenant system, between agent instances, or between organizational scopes. This can happen without any adversarial intent:

- **Session isolation failure.** When context, cache, or memory state bleeds between user sessions, authentication and authorization controls become irrelevant. Under OWASP LLM02:2025 (Sensitive Information Disclosure).
- **Namespace conflation.** When multiple agents share a memory store under a single userId, memories from unrelated contexts contaminate each other (documented in the OpenClaw/Mem0 project).
- **Multi-agent propagation.** The MAMA framework (arXiv: 2512.04668) shows that PII leakage in multi-agent systems concentrates in internal channels (inter-agent messages, shared memory) rather than in final user-facing outputs.

**Scope tier relevance.** The doc-07 decomposition ([07](07-taxonomy-and-decomposition.md) §4.1) defines scope tiers (session/agent/user/team/workspace/organizational). Cross-boundary bleed is a failure of scope enforcement. The multi-scope memory isolation pattern — where every memory write is tagged with identity scopes (user_id, agent_id, run_id, org_id) — is the primary defense, but requires strict enforcement at the storage layer, not just the API layer.

---

## 6. Defense Taxonomy

**EXPLORATORY** — Organized by the phase of the memory lifecycle they protect, following the Write-Store-Retrieve-Execute-Share-Forget framework from the Mnemonic Sovereignty survey.

### 6.1 Write-Phase Defenses — Integrity at Ingestion

**OWASP Agent Memory Guard** (OWASP Foundation, 2026) provides the reference implementation for write-phase defense. It screens every read and write to an agent's memory, blocking prompt injection, secret leakage, and integrity tampering before they corrupt agent behavior.

| Defense | Mechanism | Effectiveness | Status |
|---|---|---|---|
| **Prompt injection detection** | Pattern-matching and classifier-based detection of injection markers in incoming content | Catches known patterns; misses novel formulations | Deployed (Agent Memory Guard v0.2.1) |
| **Cryptographic integrity baselines** | SHA-256 hashing of memory entries; mismatch detection on immutable fields | Deterministic detection of out-of-band tampering | Deployed (Agent Memory Guard) |
| **Write-side sanitization** | Classifier applied *before* content enters memory; sanitizes summaries as well as raw content | Closes the summarization-laundering channel | Recommended (Temporal Contamination research) |
| **Protected-key enforcement** | YAML-defined rules preventing modification of identity-critical keys (e.g., `identity.user_id`) | Prevents identity-based attacks | Deployed (Agent Memory Guard) |
| **Size and rate anomaly detection** | Flags rapid-change churn and anomalous entry sizes | Catches brute-force injection attempts | Deployed (Agent Memory Guard) |

**Roadmap:** Agent Memory Guard Q3 2026 (v0.4.0) targets ML-based anomaly detection and vector-store protection. Q4 2026 (v1.0.0) targets multi-agent security.

### 6.2 Store-Phase Defenses — Integrity at Rest

| Defense | Mechanism | Effectiveness |
|---|---|---|
| **Scope isolation** | Memory partitioned by trust level; per-tenant namespaces with strict access boundaries | Prevents cross-boundary bleed; required for multi-tenancy |
| **Immutable audit trails** | Append-only log of all memory writes with cryptographic integrity | Enables forensic traceback; EU AI Act compliance |
| **Time-To-Live (TTL) enforcement** | 30-day TTL on untrusted memory categories | Bounds sleeper-attack activation window |
| **Memory provenance tracking** | Source-class tagging on every memory entry (user-authored, agent-generated, ingested-from-document, shared-from-agent) | Enables trust-differentiated retrieval and audit |
| **Snapshot and rollback** | Point-in-time snapshots enabling rollback to known-good state | Enables recovery from detected poisoning |

### 6.3 Retrieve-Phase Defenses — Integrity at Read

| Defense | Mechanism | Effectiveness |
|---|---|---|
| **Trust-aware retrieval** | Temporal decay applied to older entries; filtering based on provenance before memories reach context | Reduces impact of aged poisoned entries |
| **Bayesian trust models** | Trust scores assigned to memory entries; scores decay for unverified or anomalous inputs | SuperLocalMemory: 72% trust degradation detection rate, 10.6ms median search latency |
| **Retrieval scope enforcement** | Queries restricted to authorized scope tiers; RBAC at the retrieval layer | Prevents cross-scope information leakage |
| **Read-side sanitization** | Classifier applied to retrieved memories before they enter the context window | Catches poisoned content at the last gate before reasoning |

### 6.4 Execute-Phase Defenses — Integrity at Runtime

| Defense | Mechanism | Effectiveness |
|---|---|---|
| **Independent tool monitoring** | Monitor tool calls at the execution layer, not via model text output | Detects MemMorph-class tool hijacking regardless of model explanations |
| **Memory quarantine** | Before acting on security-sensitive historical memory, validate against authoritative sources | Prevents sleeper activation for critical decisions |
| **Policy engine separation** | YAML-defined policies mapping findings to actions: allow, redact, quarantine, block | Enables declarative security policy without code changes |

### 6.5 Post-Hoc Defenses — Auditing and Forensics

**MemAudit** (Tan et al., May 2026, arXiv: [2605.23723](https://arxiv.org/abs/2605.23723)) provides the most rigorous post-hoc defense framework published to date:

- **Counterfactual memory influence scoring** — measures each memory's causal contribution to harmful outputs via replay-based intervention
- **Memory consistency graph** — identifies structurally anomalous memories within the broader memory store using graph-based analysis
- **Fusion approach** — combines causal evidence with global anomaly scoring to identify suspicious memories without requiring oracle poison labels

**Results:** Reduces MINJA QA attack success from 70% to 0%, and RAP attack success from 83.3% to 0%.

**Limitation:** MemAudit is a *post-hoc* tool — it identifies poisoned memories after harmful behavior has been observed. It does not prevent the initial poisoning. A complete defense requires both write-time prevention (Section 6.1) and post-hoc auditing.

### 6.6 Defense Maturity Assessment

| Defense Category | Maturity | Production-Ready? | RHOAI Urgency |
|---|---|---|---|
| Prompt injection detection | Medium | Partial — catches known patterns | High (RFE-M3) |
| Cryptographic integrity | Medium | Yes — SHA-256 baseline | High (RFE-M3) |
| Scope isolation | Medium | Yes — namespace-based | Critical (RFE-M3) |
| Immutable audit trail | Low-Medium | Emerging — no standard format | Critical (RFE-M6) |
| TTL enforcement | Medium | Yes — straightforward | Medium (RFE-M3) |
| Memory provenance | Low | Research stage | High (RFE-M6) |
| ML-based anomaly detection | Low | Research stage (Q3 2026 target) | Medium (Phase 2+) |
| Post-hoc causal auditing | Low | Research stage | Medium (Phase 2+) |
| Longitudinal safety evaluation | Very Low | No standard methodology | High (RFE-M6) |

---

## 7. The Mnemonic Sovereignty Framework

**REFERENCE** — Lin, Li, & Chen (April 2026, arXiv: [2604.16548](https://arxiv.org/abs/2604.16548)).

### 7.1 Core Argument

The Mnemonic Sovereignty survey reframes agent memory security from a collection of point defenses to a *governance problem over persistent state.* The core argument: the qualitative properties of agent memory — statefulness, persistence, and propagation — create attack and governance challenges that are fundamentally distinct from prompt injection and RAG poisoning. Memory is not an add-on cache; it is the *mutable, cross-session, propagating epistemic core* of autonomous systems.

### 7.2 Memory Lifecycle Framework

The survey organizes analysis around six phases cross-tabulated against four security objectives:

| Phase | Integrity | Confidentiality | Availability | Governance |
|---|---|---|---|---|
| **Write** | Injection prevention, input validation | PII/secret filtering | Rate limiting, anti-churn | Write authorization |
| **Store** | Tamper detection, cryptographic baseline | Encryption at rest, scope isolation | Redundancy, backup | Retention policy |
| **Retrieve** | Trust-aware filtering, anomaly scoring | Scope-bounded queries, RBAC | Retrieval latency SLOs | Read authorization |
| **Execute** | Tool monitoring, quarantine | Output filtering | Graceful degradation | Action authorization |
| **Share** | Propagation integrity | Cross-agent access control | Bandwidth management | Share authorization |
| **Forget/Rollback** | Deletion verification | Erasure completeness (GDPR) | Recovery from poisoning | Erasure authorization |

### 7.3 Nine Governance Primitives

The survey identifies nine governance primitives that should be addressed explicitly in the agent's architecture:

1. **Writability** — which actors can write to which memory scopes
2. **Read authorization** — which actors can read from which scopes
3. **Audit** — every write emits an inspectable, tamper-evident record
4. **Forget** — the ability to erase specific memories (GDPR right to be forgotten)
5. **Rollback** — the ability to revert to a known-good state
6. **Provenance** — source attribution for every memory entry
7. **Scope** — hierarchical isolation of memory by organizational boundary
8. **Propagation control** — rules governing memory sharing between agents
9. **Expiration** — TTL-based lifecycle management

**Critical finding:** No published memory architecture currently covers all nine primitives. This is the gap RHOAI should aim to close.

### 7.4 Relationship to RHOAI Decomposition

The Mnemonic Sovereignty framework maps cleanly onto the doc-07 cross-cutting governance dimension ([07](07-taxonomy-and-decomposition.md) §4.1):

| Mnemonic Sovereignty Primitive | RHOAI Decomposition Component | RFE |
|---|---|---|
| Writability, Read authorization | Cross-cutting: Governance & Scope — RBAC | RFE-M3 |
| Audit | Cross-cutting: Governance & Scope — Audit | RFE-M6 |
| Forget, Rollback | Cross-cutting: Governance & Scope — Erasure | RFE-M6 |
| Provenance | Cross-cutting: Governance & Scope — Provenance | RFE-M6 |
| Scope | Cross-cutting: Governance & Scope — Scope tiers | RFE-M3 |
| Propagation control | Subsystem 1: Multi-agent coordination | RFE-M9 |
| Expiration | Cross-cutting: Governance & Scope — Lifecycle | RFE-M3 |

---

## 8. RHOAI Implications and Architecture Recommendations

**PROPOSED** — Research recommendations for the review gate, not decided RHOAI design.

### 8.1 Threat-to-RFE Mapping

Every attack vector in Section 3 maps to specific RFE roadmap items. This table identifies which RFEs must address which threats:

| Attack Vector | Primary Defense Required | RFE(s) | Phase |
|---|---|---|---|
| SpAIware | Write-side injection detection, memory content screening | RFE-M3 (governance) | 1 — 3.6 |
| PoisonedRAG | Corpus integrity validation, retrieval filtering | RFE-M3 + Knowledge Sources | 1 — 3.6 |
| MINJA | Anomaly detection on memory writes, trust scoring | RFE-M3 + RFE-M6 (audit) | 1-2 — 3.6/3.7 |
| MemoryGraft | Procedural memory validation, provenance tracking | RFE-M6 (provenance) | 2 — 3.7+ |
| MemMorph | Tool selection auditing, memory-MCP coupling | RFE-M5 (MCP integration) + RFE-M6 | 1-2 — 3.6/3.7 |
| Sleeper Poisoning | TTL enforcement, longitudinal safety evaluation | RFE-M3 (TTL) + RFE-M6 (audit) | 1-2 — 3.6/3.7 |
| Context Rot | Context engineering, compression safeguards | RFE-M4 (context engineering) | 1 — 3.6 |
| Cross-Boundary Bleed | Scope isolation, namespace enforcement | RFE-M3 (scope tiers) | 1 — 3.6 |
| Temporal Contamination | Longitudinal evaluation, write-side gating | RFE-M6 (trajectory audit) | 2 — 3.7+ |

### 8.2 Security Architecture Recommendations

**Recommendation 1 — Adopt the Mnemonic Sovereignty governance primitives as the security requirements baseline for RFE-M3.**

The nine primitives (writability, read authorization, audit, forget, rollback, provenance, scope, propagation control, expiration) should be the checklist against which the governance layer is designed. No published memory architecture covers all nine; RHOAI has the opportunity to be the first enterprise platform to do so.

**Recommendation 2 — Make the audit trail (RFE-M6) a GA gate, not a Phase 2 nice-to-have.**

The audit trail is not just a compliance requirement — it is the foundation for post-hoc forensics (MemAudit-class tools), longitudinal safety evaluation (temporal contamination detection), and regulatory compliance (EU AI Act requires 10-year audit trails for high-risk AI systems). Without it, every other defense is blind after the fact. The [strategy document](/features/agent-memory/strategy/agent-memory-strategy.md) §6.1 already recommends this; this document provides the threat-model justification.

**Recommendation 3 — Implement defense-in-depth across the memory lifecycle.**

No single defense is sufficient. The architecture should layer defenses across all six lifecycle phases:

```
Write:     Injection detection + PII screening + rate limiting
Store:     Cryptographic integrity + scope isolation + TTL + provenance tagging
Retrieve:  Trust-aware filtering + scope enforcement + read-side sanitization
Execute:   Independent tool monitoring + memory quarantine for critical actions
Share:     Propagation access control + integrity verification
Forget:    Verified erasure + snapshot/rollback capability
```

**Recommendation 4 — Separate the memory security layer from the memory substrate.**

Following the Agent Memory Guard architecture pattern: the security layer should be a *screening layer* that wraps the memory substrate (PostgreSQL+pgvector, or whatever backend RFE-M8 selects). This separation allows:
- Security policy updates without substrate changes
- Multiple substrates under one security framework
- Declarative policy (YAML-defined rules) rather than imperative security code
- Independent security certification

**Recommendation 5 — Require provenance tagging on all memory writes from Day 1.**

Every memory entry must carry source-class provenance: user-authored, agent-generated, ingested-from-document, shared-from-agent, system-generated. This is cheap to implement at write time and extremely expensive to retrofit. Provenance is the foundation for trust-differentiated retrieval, forensic traceback, and the Mnemonic Sovereignty governance model. Deferring it to Phase 2 creates a "provenance debt" that compounds with every memory entry written without attribution.

**Recommendation 6 — Integrate memory security with MCP governance.**

The MemMorph attack (Section 3.5) demonstrates that memory poisoning can hijack tool selection. In the RHOAI context, this means a poisoned memory entry could steer an agent toward a malicious MCP server. The MCP Registry's governance tracks (lifecycle, approval, verification, certification) from [08](08-rhoai-ocp-alignment.md) §2.2 must be coupled with memory governance: tool selection decisions should be auditable against both the MCP server's governance state and the memory entries that influenced the selection.

### 8.3 Regulatory Compliance Mapping

| Regulation | Memory Security Requirement | RHOAI RFE |
|---|---|---|
| **EU AI Act** (Aug 2026) | 10-year audit trails for high-risk AI; logging of AI system behavior | RFE-M6 |
| **GDPR** | Right to be forgotten applies to explicit agent memory stores | RFE-M6 (erasure primitives) |
| **HIPAA** | Patient data in clinical agent memory must be isolated and auditable | RFE-M3 (scope isolation) + RFE-M6 |
| **CCPA** | Consumer data protection applies to memory-stored PII | RFE-M3 (PII screening) |
| **NIST AI RMF** | Risk management for AI systems including memory integrity | Cross-cutting |

**Tension to flag.** GDPR's right to be forgotten requires memory deletion on request. The EU AI Act requires 10-year audit trails. These two requirements are in tension for memory systems that store personal data. The resolution — delete the memory content but retain a tamper-evident audit record that *a deletion occurred* — must be designed into RFE-M6 from the start.

---

## 9. Open Questions for the Review Gate

| ID | Question | Blocking |
|---|---|---|
| Q-S1 | Should the RHOAI memory security layer adopt the OWASP Agent Memory Guard architecture directly, or build an independent implementation aligned with the same threat model? | RFE-M3 design |
| Q-S2 | What is the minimum viable provenance schema? Source-class tag only, or full chain-of-custody (who wrote, when, from what source, via what agent)? | RFE-M3, RFE-M6 |
| Q-S3 | How should the audit trail handle the GDPR/EU AI Act tension (right to forget vs. 10-year retention)? | RFE-M6 design |
| Q-S4 | Should memory entries carry cryptographic signatures (per-entry SHA-256) at the substrate level, or is this the screening layer's responsibility? | RFE-M3, RFE-M8 |
| Q-S5 | What longitudinal safety evaluation methodology should RHOAI adopt for temporal contamination detection? No standard exists. | RFE-M6 test framework |
| Q-S6 | How should the memory-MCP governance coupling (Recommendation 6) be implemented — at the registry level, the gateway level, or both? | RFE-M5, MCP Registry |
| Q-S7 | Should TTL enforcement be a platform default (all untrusted memory expires after N days) or a policy-configurable option? What is the right default N? | RFE-M3 |
| Q-S8 | Does the RHOAI threat model include state-sponsored adversaries (per the Gemini/Russian actor incident), or is the baseline limited to opportunistic attackers? This affects the depth of defense required. | Architectural scope |

---

## 10. Sources

### Academic Papers

| Ref | Citation | Link |
|---|---|---|
| [S1] | Rehberger, J. (2024). "SpAIware: Uncovering a novel AI attack vector through persistent memory in LLM applications and agents." *Future Generation Computer Systems*, Vol. 174. | [ACM DL](https://dl.acm.org/doi/10.1016/j.future.2025.107994) |
| [S2] | Zou, W. et al. (2024). "PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of LLMs." USENIX Security 2025. | [arXiv:2402.07867](https://arxiv.org/abs/2402.07867) |
| [S3] | Dong, Z. et al. (2025). "MINJA: Memory Injection Attacks on LLM Agents via Query-Only Interaction." NeurIPS 2025. | [arXiv:2503.03704](https://arxiv.org/abs/2503.03704) |
| [S4] | Devarangadi Sunil, B. et al. (2026). "Memory Poisoning Attack and Defense on Memory Based LLM-Agents." | [arXiv:2601.05504](https://arxiv.org/abs/2601.05504) |
| [S5] | Srivastava, S. & He, H. (2025). "MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval." | [arXiv:2512.16962](https://arxiv.org/abs/2512.16962) |
| [S6] | Zhang, X. et al. (2026). "MemMorph: Tool Hijacking in LLM Agents via Memory Poisoning." | [arXiv:2605.26154](https://arxiv.org/abs/2605.26154) |
| [S7] | (2026). "Hidden in Memory: Sleeper Memory Poisoning in LLM Agents." | [arXiv:2605.15338](https://arxiv.org/abs/2605.15338) |
| [S8] | Tan, Z. et al. (2026). "MemAudit: Post-hoc Auditing of Poisoned Agent Memory via Causal Attribution and Structural Anomaly Detection." | [arXiv:2605.23723](https://arxiv.org/abs/2605.23723) |
| [S9] | Lin, Z., Li, C. & Chen, K. (2026). "A Survey on the Security of Long-Term Memory in LLM Agents: Toward Mnemonic Sovereignty." | [arXiv:2604.16548](https://arxiv.org/abs/2604.16548) |
| [S10] | Al-Tawaha et al. (2026). "Remembering More, Risking More: Longitudinal Safety Risks in Memory-Equipped LLM Agents." | [arXiv:2605.17830](https://arxiv.org/abs/2605.17830) |
| [S11] | Liu, J. et al. (2025). "Topology Matters: Measuring Memory Leakage in Multi-Agent LLMs." (MAMA framework) | [arXiv:2512.04668](https://arxiv.org/abs/2512.04668) |

### Industry & Standards Sources

| Ref | Citation | Link |
|---|---|---|
| [I1] | OWASP. "Top 10 for Agentic Applications (2026)." ASI06: Memory & Context Poisoning. | [OWASP GenAI](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/) |
| [I2] | OWASP. "Memory Is a Feature. It Is Also an Attack Surface." (May 2026). | [OWASP Blog](https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/) |
| [I3] | OWASP. "Agent Memory Guard" project. | [OWASP Foundation](https://owasp.org/www-project-agent-memory-guard/) |
| [I4] | OWASP. "AI Agent Security Cheat Sheet." | [Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) |
| [I5] | Help Net Security. "OWASP Agent Memory Guard: Stop AI agents from being weaponized through their own memory." (June 2026). | [HelpNetSecurity](https://www.helpnetsecurity.com/2026/06/01/owasp-agent-memory-guard/) |
| [I6] | Palo Alto Networks Unit 42. "New Prompt Injection Attack Vectors Through MCP Sampling." | [Unit 42](https://unit42.paloaltonetworks.com/model-context-protocol-attack-vectors/) |
| [I7] | Tenable. "HackedGPT: Seven Critical Vulnerabilities." (November 2025). | [Australian Cyber Security](https://australiancybersecuritymagazine.com.au/hackedgpt-seven-critical-vulnerabilities-expose-chatgpt-to-data-theft-and-persistent-hijacking/) |
| [I8] | SafeBreach. "Exploiting Gemini via Prompt Injection." (2025). | [SafeBreach](https://www.safebreach.com/blog/gemini-voice-assistant-prompt-injection-exploit/) |
| [I9] | Infosecurity Magazine. "Prompt Injection Bugs Found in Official Anthropic Git MCP Server." | [Infosecurity](https://www.infosecurity-magazine.com/news/prompt-injection-bugs-anthropic/) |
| [I10] | Redis. "Context rot explained (& how to prevent it)." (December 2025). | [Redis Blog](https://redis.io/blog/context-rot/) |
| [I11] | Giskard. "Cross Session Leak: LLM security vulnerability & detection guide." | [Giskard](https://www.giskard.ai/knowledge/cross-session-leak-when-your-ai-assistant-becomes-a-data-breach) |
| [I12] | Mem0. "AI Memory Security: Best Practices and Implementation." (2026). | [Mem0](https://mem0.ai/blog/ai-memory-security-best-practices) |
| [I13] | O'Reilly. "Why Multi-Agent Systems Need Memory Engineering." (February 2026). | [O'Reilly Radar](https://www.oreilly.com/radar/why-multi-agent-systems-need-memory-engineering/) |
| [I14] | LLM-Hacking. "Temporal memory contamination: longitudinal safety drift." | [LLM-Hacking](https://www.llm-hacking.com/hacks/temporal-memory-contamination.md/) |
| [I15] | Schneider, C. "Memory poisoning in AI agents: exploits that wait." (2026). | [Blog](https://christian-schneider.net/blog/persistent-memory-poisoning-in-ai-agents/) |

### RHOAI Internal References

| Ref | Citation |
|---|---|
| [R1] | [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md) — Governance & Scope cross-cutting dimension, Subsystem decomposition |
| [R2] | [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md) — MCP Registry governance pattern, registry-as-governance principle |
| [R3] | [04 Technical Patterns](04-technical-patterns.md) — Memory lifecycle loop, scope/tenancy/governance patterns |
| [R4] | [RFE Roadmap](/features/agent-memory/strategy/rfe-roadmap.md) — RFE-M3 (governance layer), RFE-M6 (audit trail) |
| [R5] | [Agent Memory Strategy](/features/agent-memory/strategy/agent-memory-strategy.md) §6.1 — Audit trail sequencing recommendation |
