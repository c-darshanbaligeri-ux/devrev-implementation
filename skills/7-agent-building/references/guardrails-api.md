# Configuring Agent Guardrails via API

> **Note:** Agent Studio is currently in beta for Dev0. Until the UI exposes guardrail configuration, use the internal API endpoints described below.

> **Source:** Schemas extracted from `devrev/api-specs` → `specs/next/openapi-internal-general.yaml`

## ⚠️ Critical: GET response ≠ POST/PUT request shape

The **read** (`ai-agents.get`) and **write** (`ai-agents.create` / `ai-agents.update`) guardrail schemas are **asymmetric**:

| Operation | `topic_boundary` fields | Example |
|---|---|---|
| **GET** response | Nested under `topic_boundary: {}` | `{ "topic_boundary": { "topic_name": "...", "description": "..." } }` |
| **CREATE** request | **Flat** — at the same level as `type` | `{ "topic_name": "...", "description": "..." }` |
| **UPDATE** request | **Flat** — at the same level as `type` | `{ "topic_name": "...", "description": "..." }` |

If you copy a guardrail object from a GET response and send it back in a POST, the API will return:
```
{ "type": "invalid_field", "message": "Bad Request", "debug_message": "Invalid field: topic_boundary" }
```

Always use the **flat** format in write requests.

---

## Overview

Guardrails are **not first-class resources** with standalone CRUD endpoints. They are **embedded** in AI agent and AI agent version payloads. Only one guardrail type exists today (`topic_boundary`), but the schema uses a discriminated union and is designed for extensibility.

Retrieval behavior (**FetchObjectContext**, **HybridSearch**, NL2SQL) is configured elsewhere (goal, instructions, skills, knowledge). When you ship a full agent design, search-like skills should name **HybridSearch** where applicable, and **FetchObjectContext** must be covered when object ids appear.

---

## Schemas

### `agent-guardrail` (GET response only)

Full OpenAPI schema name: `agent-guardrail`

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | `agent-guardrail-type` | ✅ | `"topic_boundary"` — the guardrail type |
| `applies_to` | `array[agent-guardrail-applies-to]` | ✅ | `["input"]`, `["output"]`, or `["input", "output"]` |
| `default_message` | `string` (text) | — | Message returned when the guardrail fails |
| `enabled` | `boolean` | — | Whether the guardrail is active |
| `topic_boundary` | `topic-boundary-guardrail` | — | **Nested** config (present in GET responses when `type` = `"topic_boundary"`) |

> ⚠️ The `topic_boundary` nested object is **read-only shape** — it appears in GET responses but is **rejected** by the write API. Use the flat format below for writes.

#### Enum: `agent-guardrail-type`

```
enum: ["topic_boundary"]
```

#### Enum: `agent-guardrail-applies-to`

```
enum: ["input", "output"]
```

### `topic-boundary-guardrail` (nested in GET only)

Full OpenAPI schema name: `topic-boundary-guardrail`

| Field | Type | Description |
|---|---|---|
| `topic_name` | `string` (text) | The name of the topic |
| `description` | `string` (text) | The description of the topic boundary defining what is allowed for the agent within this topic |

### `set-ai-agent-guardrail` (CREATE and UPDATE requests — **flat format**)

Full OpenAPI schema name: `set-ai-agent-guardrail`

A **discriminated union** on `type`. When `type = "topic_boundary"`, the `topic-boundary-guardrail` fields (`topic_name`, `description`) are merged **at the top level** — NOT nested.

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | `set-ai-agent-guardrail-type` | — | `"none"` or `"topic_boundary"` |
| `applies_to` | `array[ai-agent-guardrail-apply-to]` | ✅ | Specifies the stages where the guardrail is enforced |
| `default_message` | `string` (text) | — | The default message when the guardrail fails |
| `enabled` | `boolean` | ✅ | Whether the guardrail is enabled |
| `topic_name` | `string` (text) | — | **Flat** — topic name (only when `type = "topic_boundary"`) |
| `description` | `string` (text) | — | **Flat** — topic boundary description (only when `type = "topic_boundary"`) |

#### Enum: `set-ai-agent-guardrail-type`

```
enum: ["none", "topic_boundary"]
```

#### Enum: `ai-agent-guardrail-apply-to`

```
enum: ["input", "output"]
```

---

## API Endpoints

### Create AI Agent

```
POST /internal/ai-agents.create
Operation: ai-agents-create
```

Request schema: `ai-agents-create-request`

Guardrails field:
```yaml
guardrails:
  type: array           # ← flat array, NOT wrapped in {"set": [...]}
  description: Guardrails for the AI agent.
  items:
    $ref: set-ai-agent-guardrail
  maxItems: 16
```

### Update AI Agent

```
POST /internal/ai-agents.update
```

Request schema: `ai-agents-update-request`

Guardrails field:
```yaml
guardrails:
  $ref: ai-agents-update-request-guardrails   # ← wrapped object, NOT a flat array
```

Where `ai-agents-update-request-guardrails`:
```yaml
properties:
  set:
    type: array
    description: Sets AI agent guardrails to the provided guardrails.
    items:
      $ref: set-ai-agent-guardrail
    maxItems: 16
```

> **Key difference:** CREATE accepts a plain array; UPDATE requires the `{ "set": [...] }` wrapper object.

### Get AI Agent

```
POST /internal/ai-agents.get
Operation: ai-agents-get
```

Response includes `ai-agent.guardrails` → `agent-guardrail[]` (nested format)

### Create AI Agent Version

```
POST /internal/ai-agents.versions.create
Operation: ai-agents-versions-create
```

Request schema: `ai-agents-versions-create-request`

Guardrails field:
```yaml
guardrails:
  type: array           # ← flat array (same as ai-agents.create)
  items:
    $ref: set-ai-agent-guardrail
```

### Update AI Agent Version

```
POST /internal/ai-agents.versions.update
Operation: ai-agents-versions-update
```

Request schema: `ai-agents-versions-update-request`

Guardrails field:
```yaml
guardrails:
  $ref: ai-agents-versions-update-request-guardrails   # ← {"set": [...]} wrapper
```

Where `ai-agents-versions-update-request-guardrails`:
```yaml
properties:
  set:
    type: array
    description: Sets AI agent guardrails to the provided guardrails.
    items:
      $ref: set-ai-agent-guardrail
    maxItems: 16
```

### Get AI Agent Version

```
POST /internal/ai-agents.versions.get
Operation: ai-agents-versions-get
```

Response includes `ai-agent-version.guardrails` → `agent-guardrail[]` (nested format)

---

## Where Guardrails Appear in Payloads

| Context | Schema Path | Format | Max Items |
|---|---|---|---|
| Read AI Agent | `ai-agent.guardrails` → `agent-guardrail[]` | Nested `topic_boundary` | — |
| Read AI Agent Version | `ai-agent-version.guardrails` → `agent-guardrail[]` | Nested `topic_boundary` | — |
| Create AI Agent | `ai-agents-create-request.guardrails` → `set-ai-agent-guardrail[]` | **Flat array** | **16** |
| Create AI Agent Version | `ai-agents-versions-create-request.guardrails` → `set-ai-agent-guardrail[]` | **Flat array** | — |
| Update AI Agent | `ai-agents-update-request-guardrails.set` → `set-ai-agent-guardrail[]` | **`{"set": [...]}` wrapper + flat** | **16** |
| Update AI Agent Version | `ai-agents-versions-update-request-guardrails.set` → `set-ai-agent-guardrail[]` | **`{"set": [...]}` wrapper + flat** | **16** |

---

## Examples

### Create an Agent with a Topic Boundary Guardrail

```json
POST /internal/ai-agents.create

{
  "name": "support-agent",
  "goal": "Help customers with product support questions",
  "guardrails": [
    {
      "type": "topic_boundary",
      "applies_to": ["input", "output"],
      "enabled": true,
      "default_message": "I can only help with product support questions. Please rephrase your request.",
      "topic_name": "Product Support",
      "description": "Only answer questions about DevRev product features, pricing, integrations, and troubleshooting. Do not discuss competitors, internal company information, or off-topic subjects."
    }
  ]
}
```

> ✅ `topic_name` and `description` are **flat** — at the same level as `type`, `applies_to`, `enabled`.
> ❌ Do NOT nest them: `"topic_boundary": { "topic_name": "...", "description": "..." }` — this will fail.

### Update Guardrails on an Existing Agent

```json
POST /internal/ai-agents.update

{
  "id": "<agent-id>",
  "guardrails": {
    "set": [
      {
        "type": "topic_boundary",
        "applies_to": ["input"],
        "enabled": true,
        "default_message": "Please ask a question related to our documentation.",
        "topic_name": "Documentation Only",
        "description": "Only respond to questions that can be answered from the knowledge base articles."
      }
    ]
  }
}
```

> ✅ Wrapped in `{ "set": [...] }` (not a flat array).
> ✅ `topic_name` and `description` are **flat**.

### Remove a Guardrail (set type to "none")

```json
POST /internal/ai-agents.update

{
  "id": "<agent-id>",
  "guardrails": {
    "set": [
      {
        "type": "none",
        "applies_to": ["input", "output"],
        "enabled": false,
        "default_message": ""
      }
    ]
  }
}
```

### GET Response (for reference — do not copy directly into POST)

A GET response returns guardrails in the **nested** format. This shape is **read-only** and cannot be sent back in a write request:

```json
{
  "agent": {
    "guardrails": [
      {
        "type": "topic_boundary",
        "applies_to": ["input"],
        "enabled": true,
        "default_message": "...",
        "topic_boundary": {
          "topic_name": "Documentation Only",
          "description": "Only respond to questions..."
        }
      }
    ]
  }
}
```

To convert a GET response guardrail for use in an UPDATE payload:
```python
# Python conversion helper
def get_to_set_guardrail(g):
    flat = {
        "type": g["type"],
        "applies_to": g["applies_to"],
        "enabled": g.get("enabled", True),
        "default_message": g.get("default_message", ""),
    }
    if g.get("topic_boundary"):
        flat["topic_name"] = g["topic_boundary"].get("topic_name", "")
        flat["description"] = g["topic_boundary"].get("description", "")
    return flat
```

---

## Feature Flag Control (archon-policy)

Guardrail behavior is controlled by feature flags in `neuron.rego`:

| Flag | Description |
|---|---|
| `agent_guardrails_enabled` | Whether guardrails are evaluated. Default: `true` in prod. Can be disabled per org/agent. |
| `override_model_name_provider_map` | Override the model used for guardrail evaluation using the `"agent_guardrails"` key. |

See [feature-flags.md](feature-flags.md) for the full archon-policy reference and update workflow.

---

## Key Takeaways

1. **No standalone endpoints** — guardrails live inside agent/version CRUD payloads
2. **GET ≠ POST shape** — GET returns nested `topic_boundary`, POST/UPDATE require flat fields
3. **Only `topic_boundary` today** — the discriminated union on `type` suggests more types coming
4. **CREATE uses flat array; UPDATE uses `{"set": [...]}`** — different wrapping per operation
5. **Enforce on input, output, or both** — use `applies_to` to control which stages
6. **Max 16 guardrails** per agent on create and update
7. **To remove**: set `type` to `"none"` in the update payload's `guardrails.set` array
