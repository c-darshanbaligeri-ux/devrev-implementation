# Ai Agents

Source: <https://developer.devrev.ai/beta/api-reference/ai-agents>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/ai-agents.events.execute-async` | [ai-agent-events-execute-async](#ai-agent-events-execute-async) |

<a id="ai-agent-events-execute-async"></a>

## `POST /ai-agents.events.execute-async`

**Execute-Async Ai Agents Events**

Source: <https://developer.devrev.ai/beta/api-reference/ai-agents/ai-agent-events-execute-async>

Execute an AI agent input event asynchronously.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `agent` | yes | `string` | The ID of the AI agent that will consume the event.<br>*Format: id* |
| `agent_version` | no | `string` | The ID of the agent version that will be used for the execution.<br>*Format: id* |
| `client_metadata` | no | `object` | The metadata to be sent to the client with the notifications of execution progress. |
| `context` | no | `ai-agent-event-context` | Additional metadata to be used by the AI agent for the event. |
| `event` | yes | `ai-agent-event` | An event to be processed by an AI agent. |
| `event_source_target` | no | `ai-agent-event-source-target` | The source of the event to send notifications to, of asynchronous execution progress. |
| `message_context` | no | `ai-agent-event-message-context` | The context for the message to be sent to the client. |
| `parent` | no | `string` | The ID of the parent object for this agent session. Access to agent session will be determined by access to parent.<br>*Format: id* |
| `session_object` | yes | `string` | An identifier of a session with an AI agent.<br>*Format: text* |
| `target` | no | `string` | *Value in: "event_source_target" \| "webhook_target"* |
| `webhook_target` | no | `ai-agent-webhook-target` | The source of the event to send notifications to, of asynchronous execution progress. |

### Response codes

- `200` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/ai-agents.events.execute-async" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "string",
    "event": {
      "input_message": {
        "message": "string"
      }
    },
    "session_object": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "session": {
    "display_id": "string",
    "id": "string"
  }
}
```

</details>
