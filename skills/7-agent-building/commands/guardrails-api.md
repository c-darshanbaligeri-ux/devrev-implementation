# /guardrails-api — Configuring Agent Guardrails via API

> **Note:** Agent Studio is currently in beta for Dev0. Until the UI exposes guardrail configuration, use the internal API endpoints described below.

> **Source:** Schemas extracted from `devrev/api-specs` → `specs/next/openapi-internal-general.yaml`

## Overview

Guardrails are **not first-class resources** with standalone CRUD endpoints. They are **embedded** in AI agent and AI agent version payloads. Only one guardrail type exists today (`topic_boundary`), but the schema uses a discriminated union and is designed for extensibility.

Retrieval behavior (**FetchObjectContext**, **HybridSearch**, NL2SQL) is configured elsewhere (goal, instructions, skills, knowledge). When you ship a full agent design, see `/agent-create` and `CLAUDE.md` — search-like skills should name **HybridSearch** where applicable, and **FetchObjectContext** must be covered when object ids appear.

## Schemas

### `agent-guardrail` (read response)

Full OpenAPI schema name: `agent-guardrail`

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | `agent-guardrail-type` | ✅ | `"topic_boundary"` — the guardrail type |
| `applies_to` | `array[agent-guardrail-applies-to]` | ✅ | `["input"]`, `["output"]`, or `["input", "output"]` |
| `default_message` | `string` (text) | — | Message returned when the guardrail fails |
| `enabled` | `boolean` | — | Whether the guardrail is active |
| `topic_boundary` | `topic-boundary-guardrail` | — | Config (present when `type` = `"topic_boundary"`) |

#### Enum: `agent-guardrail-type`

```
enum: ["topic_boundary"]
```

#### Enum: `agent-guardrail-applies-to`

```
enum: ["input", "output"]
```

### `topic-boundary-guardrail`

Full OpenAPI schema name: `topic-boundary-guardrail`

| Field | Type | Description |
|---|---|---|
| `topic_name` | `string` (text) | The name of the topic |
| `description` | `string` (text) | The description of the topic boundary defining what is allowed for the agent within this topic |

### `set-ai-agent-guardrail` (write/create/update)

Full OpenAPI schema name: `set-ai-agent-guardrail`

A **discriminated union** on `type`:

| Discriminator | Maps to schema |
|---|---|
| `"none"` | `empty` (removes the guardrail) |
| `"topic_boundary"` | `topic-boundary-guardrail` |

Common fields:

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | `set-ai-agent-guardrail-type` | — | `"none"` or `"topic_boundary"` |
| `applies_to` | `array[ai-agent-guardrail-apply-to]` | ✅ | Specifies the stages where the guardrail is enforced |
| `default_message` | `string` (text) | — | The default message when the guardrail fails |
| `enabled` | `boolean` | ✅ | Whether the guardrail is enabled |

#### Enum: `set-ai-agent-guardrail-type`

```
enum: ["none", "topic_boundary"]
```

#### Enum: `ai-agent-guardrail-apply-to`

```
enum: ["input", "output"]
```

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
  type: array
  description: Guardrails for the AI agent.
  items:
    $ref: set-ai-agent-guardrail
  maxItems: 16
```

### Update AI Agent

```
POST /internal/ai-agents.update  (operation inferred from schema)
```

Request schema: `ai-agents-update-request`

Guardrails field:
```yaml
guardrails:
  $ref: ai-agents-update-request-guardrails
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

### Get AI Agent

```
GET /internal/ai-agents.get
Operation: ai-agents-get
```

Response includes `ai-agent.guardrails` → `agent-guardrail[]`

### Create AI Agent Version

```
POST /internal/ai-agents.versions.create
Operation: ai-agents-versions-create
```

Request schema: `ai-agents-versions-create-request`

Guardrails field:
```yaml
guardrails:
  type: array
  description: Guardrails for the agent version.
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
  $ref: ai-agents-versions-update-request-guardrails
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
GET /internal/ai-agents.versions.get
Operation: ai-agents-versions-get
```

Response includes `ai-agent-version.guardrails` → `agent-guardrail[]`

## Where Guardrails Appear in Payloads

| Context | Schema Path | Max Items |
|---|---|---|
| Read AI Agent | `ai-agent.guardrails` → `agent-guardrail[]` | — |
| Read AI Agent Version | `ai-agent-version.guardrails` → `agent-guardrail[]` | — |
| Create AI Agent | `ai-agents-create-request.guardrails` → `set-ai-agent-guardrail[]` | **16** |
| Create AI Agent Version | `ai-agents-versions-create-request.guardrails` → `set-ai-agent-guardrail[]` | — |
| Update AI Agent | `ai-agents-update-request-guardrails.set` → `set-ai-agent-guardrail[]` | **16** |
| Update AI Agent Version | `ai-agents-versions-update-request-guardrails.set` → `set-ai-agent-guardrail[]` | **16** |

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
      "topic_boundary": {
        "topic_name": "Product Support",
        "description": "Only answer questions about DevRev product features, pricing, integrations, and troubleshooting. Do not discuss competitors, internal company information, or off-topic subjects."
      }
    }
  ]
}
```

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
        "topic_boundary": {
          "topic_name": "Documentation Only",
          "description": "Only respond to questions that can be answered from the knowledge base articles."
        }
      }
    ]
  }
}
```

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

## Feature Flag Control (archon-policy)

Guardrail behavior is controlled by feature flags in `neuron.rego`:

| Flag | Description |
|---|---|
| `agent_guardrails_enabled` | Whether guardrails are evaluated. Default: `true` in prod. Can be disabled per org/agent. |
| `override_model_name_provider_map` | Override the model used for guardrail evaluation using the `"agent_guardrails"` key. |

See `/feature-flags` for the full archon-policy reference and update workflow.

## Key Takeaways

1. **No standalone endpoints** — guardrails live inside agent/version CRUD payloads
2. **Only `topic_boundary` today** — but the discriminated union on `type` suggests more types coming
3. **Enforce on input, output, or both** — use `applies_to` to control which stages
4. **Max 16 guardrails** per agent on create and update
5. **To remove**: set `type` to `"none"` in the update payload's `guardrails.set` array
6. **Update uses a wrapper**: agent update wraps guardrails in `{ "set": [...] }`, not a flat array

## Related Commands

- `/feature-flags` — Full archon-policy guide including `neuron.rego` agent config
- `/agent-create` — Creating a new agent (includes guardrails in the design phase)
- `/agent-improve` — Improving existing agent configuration
