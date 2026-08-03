---
type: question
title: How to version agents with non-deterministic LLM behavior?
description: SemVer breaks for LLM-driven agents -- a "minor" prompt tweak can completely alter behavior; the registry must decide what constitutes a version bump (prompts, models, temperature, tools) and when evaluation pipelines prove backwards compatibility.
status: open
timestamp: 2026-08-03
tags: [agent-registry, versioning, semver]
source: https://docs.google.com/document/d/1hqW1HrqWJw7R90irulIIAxTy-_vP7eM7g_IsNbbNmkE (Jiri Danek comment)
---
Raised by Jiri Danek in the scoping doc review. LLM behavior is highly
sensitive to phrasing -- a seemingly minor prompt tweak can completely alter
an agent's behavior (Hyrum's Law). Traditional SemVer (patch/minor/major)
doesn't map cleanly to prompt changes, model swaps, or temperature adjustments.

Adel's response: "It depends on what you choose to version. Prompts might be
too ephemeral, depending on the task really. It could be models, MCP servers...
We have a prompt registry as well, so that will likely connect to it."

Open sub-questions:
- What constitutes a "breaking change" for an agent? Model swap? Prompt change?
  Tool addition/removal?
- Should any change to system prompt, model, or temperature default to a major
  version bump until evaluation proves backwards compatibility?
- How does the prompt registry connect to agent versioning?
- What role do evaluation pipelines play in validating version compatibility?
