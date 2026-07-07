---
title: AI Skills Ecosystem Research
description: Landscape analysis of how AI skills are defined, packaged, composed, and governed across frameworks, protocols, and emerging standards.
source: ai-asset-registry/skills/skills-registry/research/01-skills-ecosystem.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# AI Skills Ecosystem Research

**Date**: 2026-04-15
**Author**: Peter Double (Principal PM - MCP)
**Purpose**: Comprehensive landscape analysis of how AI skills are defined, packaged, composed, and governed across frameworks, protocols, and emerging standards. Informs the Skills registry design within the AI Asset Registry proposal for RHOAI.

---

## Table of Contents

1. [Terminology Map: What is a "Skill"?](#1-terminology-map)
2. [Framework-by-Framework Analysis](#2-framework-analysis)
3. [Packaging Formats](#3-packaging-formats)
4. [Metadata and Schemas](#4-metadata-and-schemas)
5. [Skill Composition Patterns](#5-skill-composition)
6. [Standards and Emerging Protocols](#6-standards-and-protocols)
7. [Implications for RHOAI Skills Registry](#7-implications)

---

## 1. Terminology Map: What is a "Skill"? <a id="1-terminology-map"></a>

The term "skill" has no single industry-standard definition. Different frameworks use overlapping terminology with subtle but important distinctions:

| Framework / Protocol | Primary Term | Definition | Granularity |
|---|---|---|---|
| **LangChain** | Tool | A callable function with name, description, and typed args_schema. The atomic unit of agent capability. | Single function |
| **LangGraph** | Tool (via ToolNode) | LangChain tools wrapped in a graph node for stateful workflow orchestration. | Single function in a graph |
| **CrewAI** | Tool | "A skill or function that agents can utilize to perform various actions." Explicitly equates tools and skills. | Single function |
| **AutoGen (Microsoft)** | Tool | "Code that can be executed by an agent to perform actions." Inherits from BaseTool with auto-generated JSON schemas. | Single function |
| **Semantic Kernel (Microsoft)** | Plugin (formerly "Skill") | A **group of functions** exposed to AI. Renamed from "skills" to "plugins" in 2023. A plugin contains multiple KernelFunctions. | Collection of functions |
| **OpenAI Function Calling** | Tool / Function | A function definition with name, description, and JSON Schema parameters. | Single function |
| **OpenAI Agents SDK** | Tool | Five types: function tools, hosted tools, local runtime tools, agents-as-tools, experimental codex tool. | Single function or agent |
| **Anthropic/Claude** | Tool | Client-side or server-side tool with name, description, input_schema (JSON Schema). Supports strict mode, input_examples, deferred loading. | Single function |
| **Llama Stack (Meta)** | Tool / Tool Group | Tools organized into "tool groups" that can be registered together. Supports built-in, MCP-sourced, and custom tools. | Single function, grouped |
| **MCP (Model Context Protocol)** | Tool | A server-exposed capability with name, description, inputSchema, and behavioral annotations. Part of a server that may expose many tools. | Single function within a server |
| **A2A (Agent-to-Agent, Google)** | Skill | An explicit first-class concept. AgentSkill is a structured metadata object within an AgentCard describing what an agent can do. | Agent-level capability |
| **Kubernetes / RHOAI** | (none yet) | No standard term. MCP servers are the closest managed unit. | Server-level |

### Key Insight: The Abstraction Ladder

```
Agent (highest level)
  |-- Skills (A2A sense: agent-level capabilities)
        |-- Plugins (Semantic Kernel sense: groups of functions)
              |-- Tools/Functions (atomic callable units)
                    |-- MCP Tools (protocol-level tool definitions)
```

**"Skill" means different things at different levels of this stack.** In CrewAI, a skill equals a tool. In Semantic Kernel, a skill (now plugin) is a collection of tools. In A2A, a skill is an agent-level capability that may involve multiple tools, models, and workflows internally.

For the RHOAI registry, the most useful definition is likely the **Semantic Kernel / A2A level**: a skill is a **named, versioned, reusable capability** that may be composed of one or more tools, prompts, and configurations.

---

## 2. Framework-by-Framework Analysis <a id="2-framework-analysis"></a>

### 2.1 LangChain / LangGraph

**Definition**: A tool is a function with metadata that an LLM can invoke.

**Core metadata fields** (from `BaseTool` class):
- `name`: Unique tool identifier
- `description`: "Used to tell the model how/when/why to use the tool"
- `args_schema`: Pydantic BaseModel defining typed input parameters
- `return_direct`: Whether to return result directly to user (skip further LLM reasoning)
- `response_format`: "content" or "content_and_artifact"
- `handle_tool_error`: Error handling strategy (bool, string, or callable)
- `tags`: List of strings for categorization
- `metadata`: Dict for callback/tracking metadata
- `extras`: Provider-specific fields (e.g., cache_control, deferred loading)

**Tool creation patterns**:
```python
# Decorator approach
@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"Sunny in {city}"

# Class-based approach
class WeatherTool(BaseTool):
    name = "get_weather"
    description = "Get weather for a city"
    args_schema = WeatherInput  # Pydantic model
    
    def _run(self, city: str) -> str:
        return f"Sunny in {city}"
```

**Packaging**: Tools are Python classes/functions distributed via pip packages. No standardized manifest format. LangChain Hub provides community sharing but no formal packaging spec.

**Composition**: LangGraph wraps tools in `ToolNode` for graph-based orchestration. Tools compose through agent graphs, not through a skill-level abstraction.

### 2.2 CrewAI

**Definition**: "A tool in CrewAI is a skill or function that agents can utilize to perform various actions." Explicitly treats tools and skills as synonymous.

**Core metadata**:
- `name`: Tool identifier
- `description`: Purpose description (critical for agent selection)
- `args_schema`: Pydantic BaseModel for input validation

**Tool creation**:
```python
# Decorator method
@tool
def my_tool(argument: str) -> str:
    """Description of what the tool does."""
    return "result"

# Class-based method
class MyTool(BaseTool):
    name: str = "my_tool"
    description: str = "What this tool does"
    args_schema: Type[BaseModel] = MyToolInput
    
    def _run(self, argument: str) -> str:
        return "result"
```

**Composition**: Agents receive tool collections. CrewAI also has "knowledge" (RAG sources) and "apps" as separate concepts alongside tools. No formal skill composition or dependency mechanism.

### 2.3 AutoGen (Microsoft)

**Definition**: "Tools are code that can be executed by an agent to perform actions."

**Architecture**: All tools inherit from `BaseTool`. The `FunctionTool` class wraps Python functions, using type annotations for automatic JSON schema generation.

**Tool categories**:
- `FunctionTool` - Custom Python functions
- `PythonCodeExecutionTool` - Code execution via Docker
- `LocalSearchTool` / `GlobalSearchTool` - GraphRAG integration
- `mcp_server_tools` - MCP protocol integration
- `HttpTool` - REST API requests
- `LangChainToolAdapter` - LangChain interoperability

**Schema structure**: Auto-generated JSON object with name, description, and parameters (properties, required, types derived from function signatures).

### 2.4 Semantic Kernel (Microsoft)

**Definition**: A **plugin** (formerly "skill") is "a group of functions that can be exposed to AI apps and services." This is the only major framework that uses a collection-level abstraction above individual functions.

**Key distinction**: "Not all AI SDKs have an analogous concept to plugins (most just have functions or tools). In enterprise scenarios, however, plugins are valuable because they encapsulate a set of functionality that mirrors how enterprise developers already develop services and APIs."

**Plugin sources** (three import methods):
1. **Native code** - Class with `@kernel_function` decorated methods
2. **OpenAPI specification** - Import from Swagger/OpenAPI 2.0, 3.0, 3.1
3. **MCP Server** - Import tools from MCP servers as plugins

**Function metadata**:
- `KernelFunction` attribute with name
- `Description` attribute for semantic descriptions
- Parameter types with `Description` annotations
- Auto-generated JSON Schema for complex input types
- Return type schema (experimental, via filters)

**Plugin structure**:
```python
class LightsPlugin:
    @kernel_function(name="get_lights", 
                     description="Gets a list of lights and their current state")
    async def get_lights(self) -> list[LightModel]:
        return self._lights

    @kernel_function(name="change_state",
                     description="Changes the state of the light")
    async def change_state(self, change_state: LightModel) -> LightModel:
        # implementation
```

**OpenAPI plugin import** - Semantic Kernel can consume any OpenAPI spec and auto-generate plugins:
```python
await kernel.add_plugin_from_openapi(
    plugin_name="lights",
    openapi_document_path="https://example.com/v1/swagger.json"
)
```

**MCP plugin import**:
```python
async with MCPStdioPlugin(
    name="Github",
    description="Github Plugin",
    command="docker",
    args=["run", "-i", "--rm", "ghcr.io/github/github-mcp-server"],
) as github_plugin:
    kernel.add_plugin(github_plugin)
```

**Historical note**: Semantic Kernel originally used "skills" as its primary term, then renamed to "plugins" to align with industry terminology. This rename is instructive for RHOAI -- even Microsoft found "skill" too ambiguous and adopted "plugin" for the collection-level concept.

### 2.5 OpenAI Function Calling / Agents SDK

**Function calling format** (industry standard adopted by many):
```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "City name or zip code"
        }
      },
      "required": ["location"]
    }
  }
}
```

**Agents SDK tool types**:
1. **Function tools** - Python functions via `@function_tool` decorator
2. **Hosted OpenAI tools** - web_search, file_search, code_execution, image_generation
3. **Local runtime tools** - ComputerTool, ShellTool, ApplyPatchTool
4. **Agents as tools** - Agents exposed as callable tools
5. **Hosted MCP tools** - Remote MCP server integration

**Advanced features**:
- `strict_json_schema`: Enforce schema conformance
- `is_enabled`: Dynamic enable/disable
- `needs_approval`: Human-in-the-loop control
- `timeout_seconds` / `timeout_behavior`: Execution limits
- `tool_input_guardrails` / `tool_output_guardrails`: Safety filters
- Deferred loading via `@function_tool(defer_loading=True)` with `ToolSearchTool`
- Tool namespaces for grouping related functions

### 2.6 Anthropic/Claude

**Tool definition format**:
```json
{
  "name": "get_weather",
  "description": "Get the current weather in a given location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"]
      }
    },
    "required": ["location"]
  }
}
```

**Additional metadata fields**:
- `input_examples`: Array of example inputs (validated against schema)
- `strict`: Guarantee schema conformance
- `cache_control`: Prompt caching optimization
- `defer_loading`: Load tool definitions on demand
- `allowed_callers`: Access control

**Two execution models**:
- **Client tools** - Your code executes, Claude returns `tool_use` blocks
- **Server tools** - Anthropic executes (web_search, code_execution, web_fetch, tool_search)

### 2.7 Llama Stack (Meta)

**Architecture**: Tools organized into **Tool Groups** that can be registered together with a Llama Stack server.

**Tool categories**:
- Built-in tools (brave_search, wolfram_alpha, code_interpreter, etc.)
- MCP-backed tools (proxy to MCP servers)
- Custom function tools (user-defined)

**Registration pattern**: Tools are registered as groups with the Llama Stack server, which makes them available to agents. The server maintains a tool registry that agents can query.

---

## 3. Packaging Formats <a id="3-packaging-formats"></a>

### 3.1 Python Packages (pip)

**Most common format today.** Tools/skills distributed as pip-installable packages.

- **LangChain**: `pip install langchain-community` (tools bundled in community packages)
- **CrewAI**: `pip install crewai-tools` (official tool collection)
- **Semantic Kernel**: `pip install semantic-kernel[mcp]` (plugins via extras)

**Advantages**: Familiar to developers, dependency management via pip, version pinning.
**Limitations**: Python-only, no standardized manifest, no governance metadata, no cross-language support.

### 3.2 npm Packages

**Primary format for MCP servers** built in TypeScript/JavaScript.

- MCP reference servers: `npx -y @modelcontextprotocol/server-memory`
- Community servers: Distributed via npm registry

**Advantages**: Ecosystem maturity, version management, familiar to Node developers.
**Limitations**: JavaScript/TypeScript only, no governance metadata.

### 3.3 Container Images (OCI)

**Containerized MCP servers** distributed as Docker/OCI images.

Example MCP server configuration:
```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "ghcr.io/github/github-mcp-server"]
    }
  }
}
```

**OCI Artifacts (non-container content)**:
- OCI Image Spec v1.1 added `artifactType` field for non-container artifacts
- Custom media types like `application/vnd.ai.skill.v1+json` could be defined
- ORAS (OCI Registry As Storage) provides CLI/SDK for pushing arbitrary artifacts
- No dedicated artifact manifest type -- existing image manifest repurposed with `artifactType`
- `subject` field enables associating metadata (signatures, attestations) with artifacts

**Advantages**: Language-agnostic, runtime isolation, existing enterprise infrastructure (registries, scanning, signing).
**Limitations**: Heavier-weight than needed for simple tool definitions, no standardized skill manifest layer.

### 3.4 OpenAPI Specifications

**Used by Semantic Kernel** to import APIs as plugins directly from Swagger/OpenAPI specs.

```json
{
  "openapi": "3.0.1",
  "info": { "title": "Light API", "version": "v1" },
  "paths": {
    "/Light": {
      "get": {
        "summary": "Retrieves all lights",
        "operationId": "get_all_lights",
        "responses": { ... }
      }
    }
  }
}
```

**Metadata mapping**: operationId -> function name, summary -> description, request/response schemas -> parameter/return schemas, security schemes -> auth requirements.

**Advantages**: Industry standard, language-agnostic, rich metadata, existing tooling.
**Limitations**: REST-only (no streaming, no bidirectional), verbose, no agent-specific metadata.

### 3.5 MCP Server Packages (via MCP Registry)

The **MCP Registry** (registry.modelcontextprotocol.io) defines a formal `server.json` schema:

```go
// Key fields from MCP Registry types
type Package struct {
    RegistryType         string    // "npm", "pypi", "oci", "nuget", "mcpb"
    RegistryBaseURL      string    // Package registry URL
    Identifier           string    // Package name/download URL
    Version              string    // Specific version (no ranges)
    FileSHA256           string    // Integrity hash
    RunTimeHint          string    // Runtime suggestion ("npx", "uvx", etc.)
    Transport            Transport // stdio, streamable-http, sse
    RuntimeArguments     []Argument
    PackageArguments     []Argument
    EnvironmentVariables []KeyValueInput
}

type Transport struct {
    Type      string           // "stdio", "streamable-http", "sse"
    URL       string           // For HTTP transports
    Headers   []KeyValueInput
    Variables map[string]Input
}

type Repository struct {
    URL       string   // Source browsing URL
    Source    string   // "github", etc.
    ID        string   // Repo identifier
    Subfolder string   // Path within monorepo
}
```

**Namespace ownership** verified via:
- GitHub OAuth / OIDC (for `io.github.username/`)
- DNS verification (for custom domains)
- HTTP verification (for custom domains)

**Advantages**: Formal schema, integrity verification, multiple package manager support, namespace governance.
**Limitations**: MCP-server-specific, doesn't cover non-MCP skills.

### 3.6 Markdown/YAML Manifests

Some tools/skills are defined entirely as declarative files:

- **Semantic Kernel prompt functions**: YAML config + Jinja2/Handlebars template
- **Claude Code skills**: Markdown files with structured instructions
- **GitHub Copilot instructions**: `.github/copilot-instructions.md`

**Example (Semantic Kernel prompt function)**:
```yaml
name: SummarizeText
description: Summarize the given text
template: |
  Summarize the following text in {{$style}} style:
  {{$input}}
template_format: handlebars
input_variables:
  - name: input
    description: The text to summarize
    is_required: true
  - name: style
    description: The summarization style
    default: concise
```

**Advantages**: Human-readable, version-controllable, low overhead.
**Limitations**: No runtime isolation, no dependency management, no integrity verification.

### 3.7 Packaging Format Comparison

| Format | Language Agnostic | Governance Ready | Distribution | Runtime Isolation | Dependency Mgmt |
|---|---|---|---|---|---|
| Python packages (pip) | No | No | PyPI | No | Yes (pip) |
| npm packages | No | No | npm registry | No | Yes (npm) |
| Container images (OCI) | Yes | Partial | OCI registries | Yes | Yes (container) |
| OCI artifacts | Yes | Partial | OCI registries | No | No |
| OpenAPI specs | Yes | No | URLs/files | No | No |
| MCP Registry packages | Partial | Yes | MCP Registry | Varies | Varies |
| Markdown/YAML | Yes | No | Git repos | No | No |
| Custom zip bundles | Yes | No | Custom | No | Manual |

---

## 4. Metadata and Schemas <a id="4-metadata-and-schemas"></a>

### 4.1 Common Metadata Fields Across Frameworks

Every framework requires at minimum:

| Field | Required By | Description |
|---|---|---|
| **name** | All | Unique identifier, typically `snake_case` |
| **description** | All | Semantic description for LLM understanding |
| **input_schema** | All | Parameter definitions (JSON Schema or Pydantic) |

Beyond these universals, frameworks diverge significantly:

### 4.2 MCP Tool Schema (the most formal spec)

```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City name or zip code"
      }
    },
    "required": ["location"]
  },
  "annotations": {
    "title": "Weather Lookup",
    "readOnlyHint": true,
    "destructiveHint": false,
    "idempotentHint": true,
    "openWorldHint": true
  }
}
```

**Tool Annotations** (unique to MCP, all are hints not guarantees):

| Annotation | Type | Default | Meaning |
|---|---|---|---|
| `title` | string | - | Human-readable display title |
| `readOnlyHint` | boolean | false | Tool does not modify its environment |
| `destructiveHint` | boolean | true | Tool may perform destructive updates (meaningful only when readOnly=false) |
| `idempotentHint` | boolean | false | Repeated calls with same args have no additional effect |
| `openWorldHint` | boolean | true | Tool interacts with external/open world (vs. closed/internal domain) |

**Security note**: "Clients MUST consider tool annotations to be untrusted unless they come from trusted servers."

### 4.3 A2A AgentSkill Schema

The A2A protocol defines the most complete "skill" metadata of any standard:

```protobuf
message AgentSkill {
  string id = 1;           // REQUIRED - Unique skill identifier
  string name = 2;         // REQUIRED - Human-readable name
  string description = 3;  // REQUIRED - What this skill does
  repeated string tags = 4;           // REQUIRED - Categorization tags
  repeated string examples = 5;      // Usage examples
  repeated string input_modes = 6;   // Supported input content types
  repeated string output_modes = 7;  // Supported output content types
  repeated SecurityRequirement security_requirements = 8;
}
```

**AgentCard** (containing skills):
```protobuf
message AgentCard {
  string name = 1;                     // REQUIRED
  string description = 2;              // REQUIRED
  repeated AgentInterface supported_interfaces = 3;  // REQUIRED
  AgentProvider provider = 4;
  string version = 5;                  // REQUIRED
  optional string documentation_url = 6;
  AgentCapabilities capabilities = 7;  // REQUIRED
  map<string, SecurityScheme> security_schemes = 8;
  repeated SecurityRequirement security_requirements = 9;
  repeated string default_input_modes = 10;   // REQUIRED
  repeated string default_output_modes = 11;  // REQUIRED
  repeated AgentSkill skills = 12;            // REQUIRED
  repeated AgentCardSignature signatures = 13;
  optional string icon_url = 14;
}
```

**Discovery**: Agents publish AgentCards at `https://{domain}/.well-known/agent-card.json`.

### 4.4 OpenAI Function Definition Schema

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get weather for a location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": { "type": "string" }
      },
      "required": ["location"]
    },
    "strict": true
  }
}
```

### 4.5 Anthropic/Claude Tool Schema

```json
{
  "name": "get_weather",
  "description": "Get the current weather in a given location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": { "type": "string", "description": "City and state" },
      "unit": { "type": "string", "enum": ["celsius", "fahrenheit"] }
    },
    "required": ["location"]
  },
  "input_examples": [
    { "location": "San Francisco, CA", "unit": "fahrenheit" }
  ],
  "strict": true,
  "cache_control": { "type": "ephemeral" }
}
```

### 4.6 Metadata Comparison Matrix

| Metadata Category | MCP | A2A | OpenAI | Anthropic | Semantic Kernel | LangChain |
|---|---|---|---|---|---|---|
| **Name** | Yes | Yes (id + name) | Yes | Yes | Yes | Yes |
| **Description** | Yes | Yes | Yes | Yes | Yes (via decorator) | Yes |
| **Input Schema** | JSON Schema | Implicit (modes) | JSON Schema | JSON Schema | Auto-generated | Pydantic |
| **Output Schema** | No formal | modes only | No | No | Experimental | No |
| **Behavioral hints** | Yes (annotations) | No | No | No | No | No |
| **Examples** | No | Yes | No | Yes (input_examples) | No | No |
| **Tags/Categories** | No | Yes (required) | No | No | No | Yes (tags) |
| **Auth requirements** | No (server-level) | Yes | No | No | Yes (via OpenAPI) | No |
| **Version** | No (server-level) | Yes (card-level) | No | No | No | No |
| **Security/Signing** | No | Yes (AgentCardSignature) | No | No | No | No |
| **I/O Content Types** | No | Yes (modes) | No | No | No | No |
| **Strict mode** | No | No | Yes | Yes | No | No |
| **Error handling** | Yes (isError) | No | No | No | No | Yes |

---

## 5. Skill Composition Patterns <a id="5-skill-composition"></a>

### 5.1 Tools-in-a-Plugin (Semantic Kernel)

The simplest composition: group related functions into a named plugin.

```
Plugin: "EmailPlugin"
  |- send_email(to, subject, body)
  |- read_inbox(folder, count)
  |- search_email(query, date_range)
  |- draft_email(to, subject, body)
```

Functions within a plugin share a namespace and can share state via dependency injection. The plugin is the unit of registration with the kernel.

### 5.2 Tool Groups (Llama Stack)

Similar to Semantic Kernel plugins -- tools registered as a named group with the Llama Stack server. Built-in groups include search tools, code interpreter tools, etc. Custom tool groups can be defined and registered.

### 5.3 Agent-as-Tool (OpenAI Agents SDK)

An entire agent can be exposed as a tool to another agent, enabling hierarchical composition:

```python
research_agent = Agent(name="researcher", tools=[web_search, file_search])
writing_agent = Agent(
    name="writer",
    tools=[research_agent.as_tool()]  # Agent becomes a tool
)
```

This pattern enables skill composition at the agent level without requiring a formal skill abstraction.

### 5.4 MCP Server Composition

An MCP server exposes multiple tools as a unit. Composition happens at the server level:

```
MCP Server: "database-tools"
  |- query(sql)
  |- insert(table, data)
  |- update(table, id, data)
  |- schema(table)
```

Multiple MCP servers can be connected to a single client, creating a flat tool namespace. There is no formal mechanism for declaring dependencies between servers.

### 5.5 Skill Chains (Emerging Pattern)

No framework has formalized skill chains, but the pattern exists informally:

1. **Sequential**: Tool A output feeds Tool B input (LangGraph edges)
2. **Conditional**: Different tools selected based on intermediate results (LangGraph branching)
3. **Parallel**: Multiple tools invoked simultaneously (AutoGen parallel execution)
4. **Nested**: Agent-as-tool patterns (OpenAI Agents SDK)

### 5.6 Skill Packs (Concept, Not Yet Standardized)

The RHOAI asset-types document identifies "Skill Packs" as a future asset type: "Grouped capabilities (multiple skills) - Packaging and governance beyond individual skills."

No framework currently provides a formal "skill pack" abstraction. The closest equivalents:
- **Semantic Kernel plugins** (function groups)
- **npm scoped packages** (e.g., `@modelcontextprotocol/server-*`)
- **CrewAI tool collections** (`crewai-tools` package)
- **Llama Stack tool groups**

### 5.7 Dependency Declarations

**No framework currently supports formal skill-to-skill dependencies.** The closest patterns:

- **Python package dependencies**: pip requirements can express tool package dependencies
- **Container image layering**: OCI images can layer skill runtime on base images
- **MCP server composition**: Multiple servers composed at the client level (no server-to-server dependencies)
- **A2A protocol**: Agents can discover and invoke other agents, creating implicit dependencies

---

## 6. Standards and Emerging Protocols <a id="6-standards-and-protocols"></a>

### 6.1 MCP (Model Context Protocol) - Anthropic

**Status**: Most mature tool-level protocol. Spec version 2025-03-26.
**Scope**: Server-to-client protocol for exposing tools, resources, and prompts.
**Spec URL**: https://modelcontextprotocol.io/specification/

**Key features**:
- JSON-RPC 2.0 over stdio, SSE, or streamable HTTP
- Tool listing with pagination (`tools/list`)
- Tool invocation (`tools/call`)
- Dynamic tool list updates (`notifications/tools/list_changed`)
- Tool annotations (behavioral hints)
- Multi-modal results (text, image, audio, embedded resources)

**Registry**: registry.modelcontextprotocol.io (v0.1, under API freeze)
- Namespace ownership verification (GitHub, DNS, HTTP)
- Package format support: npm, pypi, oci, nuget, mcpb
- Transport configuration (stdio, streamable-http, sse)
- SHA-256 integrity hashes

**What MCP does NOT cover**:
- Skill-level abstraction (MCP tools are atomic functions)
- Skill composition or dependencies
- Skill versioning (tools versioned at server level)
- Skill lifecycle management
- Cross-server tool relationships

### 6.2 A2A (Agent-to-Agent Protocol) - Google

**Status**: Active development. Protobuf-based specification. Repo: github.com/a2aproject/A2A
**Scope**: Agent-to-agent communication and capability discovery.
**Relationship to MCP**: Complementary. "A2A complements MCP by enabling agents to collaborate with each other." MCP = tool-level integration, A2A = agent-level collaboration.

**Key features**:
- AgentCard discovery via `.well-known/agent-card.json`
- AgentSkill as first-class metadata concept
- JSON-RPC 2.0 over HTTPS
- Streaming via SSE, push notifications
- AgentCard signing and verification
- Task-based interaction model
- Curated registries for agent discovery

**What A2A provides that MCP doesn't**:
- Skill-level metadata (tags, examples, I/O modes)
- Agent-level versioning and identity
- Digital signatures for capability cards
- Multi-modal content type negotiation
- Security requirement declarations per skill

**What A2A does NOT cover**:
- Skill packaging or distribution
- Skill lifecycle management
- Skill composition within an agent

### 6.3 OpenAI Function Calling Format

**Status**: De facto industry standard. Adopted by OpenAI, Azure OpenAI, and many compatible providers.
**Scope**: Tool definition schema for LLM function calling.

**The format** (`type: "function"` with `function.name`, `function.description`, `function.parameters` as JSON Schema) has become the lingua franca. Most frameworks can convert their tool definitions to this format for LLM consumption.

### 6.4 OpenAPI / Swagger

**Status**: Mature industry standard (OpenAPI 3.0/3.1).
**Scope**: REST API description.
**Relevance**: Semantic Kernel can import OpenAPI specs directly as plugins. This is the most enterprise-friendly approach because organizations already have OpenAPI specs for their APIs.

### 6.5 No Unified "Skills Specification" Exists

**There is no equivalent of the MCP specification for skills.** The landscape is fragmented:

| Layer | Standards | Maturity |
|---|---|---|
| Tool definitions | OpenAI function format, MCP tools, JSON Schema | Converging |
| Tool protocol | MCP (tool-level) | Mature |
| Agent protocol | A2A (agent-level) | Early |
| Skill packaging | None | Gap |
| Skill registry | None (MCP Registry covers servers, not skills) | Gap |
| Skill composition | None | Gap |
| Skill lifecycle | None | Gap |

### 6.6 Other Relevant Initiatives

- **OASIS CACAO** (Collaborative Automated Course of Action Operations): Security-focused workflow standard, not AI-specific but shares composition concepts
- **W3C Web of Things**: Thing Description format has parallels to skill descriptions
- **CNCF**: No AI skill standard, but OCI/container standards apply to packaging
- **MLflow**: Has prompt registry and model registry, no skill registry. Collaboration target for RHOAI.
- **Kubeflow Hub** (formerly Model Registry): Focused on models, could be extended

---

## 7. Implications for RHOAI Skills Registry <a id="7-implications"></a>

### 7.1 Definition: What Should RHOAI Call a "Skill"?

Based on this research, a skill in the RHOAI context should be defined as:

> **A named, versioned, reusable AI capability** that encapsulates one or more tools, prompts, configurations, and/or agent behaviors into a governed unit that can be discovered, evaluated, and attached to agents or workflows.

This aligns with:
- A2A's `AgentSkill` (capability-level, not function-level)
- Semantic Kernel's `Plugin` (collection of functions)
- The RHOAI asset-types document definition

It is explicitly **above** the MCP tool level and **below** the full agent level.

### 7.2 Proposed Skill Metadata Schema (Synthesized)

Drawing from all frameworks and protocols analyzed:

```yaml
# Proposed RHOAI Skill Descriptor
apiVersion: registry.rhoai.io/v1alpha1
kind: Skill
metadata:
  name: "email-assistant"
  version: "1.2.0"
  description: "Email management capabilities for AI agents"
  tags: ["email", "communication", "productivity"]
  provider:
    organization: "Red Hat"
    url: "https://redhat.com"
  documentation_url: "https://docs.example.com/email-assistant"
  icon_url: "https://assets.example.com/email-icon.png"
  
spec:
  # What the skill can do (A2A-inspired)
  capabilities:
    - id: "send_email"
      name: "Send Email"
      description: "Compose and send emails"
      input_modes: ["text/plain", "application/json"]
      output_modes: ["text/plain"]
      examples: ["Send an email to team@example.com about the meeting"]
      annotations:  # MCP-inspired
        readOnly: false
        destructive: false
        idempotent: false
        openWorld: true
    - id: "search_inbox"
      name: "Search Inbox"
      description: "Search emails by query"
      input_modes: ["text/plain"]
      output_modes: ["application/json"]
      annotations:
        readOnly: true
  
  # How the skill is packaged
  packaging:
    type: "mcp-server"  # or "openapi", "python-package", "oci-image", "container"
    registry: "registry.modelcontextprotocol.io"
    identifier: "io.redhat/email-assistant"
    version: "1.2.0"
    sha256: "abc123..."
    transport:
      type: "streamable-http"
      url: "https://mcp.example.com/email"
  
  # What the skill needs
  requirements:
    authentication:
      - type: "oauth2"
        scopes: ["email.read", "email.send"]
    resources:
      cpu: "100m"
      memory: "256Mi"
    dependencies:
      - kind: Skill
        name: "identity-provider"
        version: ">=1.0.0"
      - kind: Model
        name: "text-generation"
        minCapability: "function-calling"
  
  # Governance
  governance:
    lifecycle_state: "active"  # draft, active, deprecated, archived
    certification: "red-hat-certified"
    trust_tier: "partner"  # red-hat, partner, community, untrusted
    security_review: "2026-03-01"
    license: "Apache-2.0"
```

### 7.3 Key Design Decisions for RHOAI

| Decision | Options | Recommendation |
|---|---|---|
| **Granularity** | Tool-level vs. plugin/skill-level vs. agent-level | Skill-level (groups of tools), with tool-level metadata within |
| **Packaging MVP** | OCI artifacts vs. MCP servers vs. Python packages | MCP servers first (aligned with MCP Registry work), OCI for non-MCP |
| **Metadata format** | Custom vs. extend A2A AgentSkill vs. extend MCP | Custom schema synthesizing MCP annotations + A2A skill fields |
| **Discovery** | Registry API vs. `.well-known` vs. both | Registry API primary, `.well-known` for federated discovery |
| **Composition** | Formal dependency graph vs. loose references | Loose references MVP, formal dependencies later |
| **Versioning** | SemVer at skill level | Yes, with compatibility ranges for dependencies |

### 7.4 Gaps This Registry Would Fill

Based on the research, no existing system provides:

1. **Skill-level governance**: Authentication, trust tiers, certification, security review
2. **Cross-framework skill registry**: Framework-agnostic skill metadata
3. **Skill lifecycle management**: Draft -> active -> deprecated -> archived
4. **Skill composition declarations**: Formal dependency and composition metadata
5. **Skill packaging standards**: Unified packaging across MCP, OpenAPI, Python, OCI
6. **Enterprise skill discovery**: Role-based access, organizational policies, audit trails

### 7.5 Reference Links

| Resource | URL |
|---|---|
| MCP Specification | https://modelcontextprotocol.io/specification/2025-03-26/ |
| MCP Registry | https://registry.modelcontextprotocol.io |
| A2A Protocol | https://github.com/a2aproject/A2A |
| A2A Documentation | https://a2a-protocol.org |
| Semantic Kernel Plugins | https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/ |
| OpenAI Function Calling | https://platform.openai.com/docs/guides/function-calling |
| Anthropic Tool Use | https://docs.anthropic.com/en/docs/build-with-claude/tool-use |
| CrewAI Tools | https://docs.crewai.com/concepts/tools |
| AutoGen Tools | https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/components/tools.html |
| OpenAI Agents SDK | https://openai.github.io/openai-agents-python/tools/ |
| OCI Image Spec 1.1 | https://opencontainers.org |
| ORAS (OCI Artifacts) | https://oras.land |
| LangChain Tools | https://docs.langchain.com |
