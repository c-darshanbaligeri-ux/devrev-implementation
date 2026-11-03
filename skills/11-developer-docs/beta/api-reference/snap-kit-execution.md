# Snap Kit Execution

Source: <https://developer.devrev.ai/beta/api-reference/snap-kit-execution>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/snap-kit-action.execute.deferred` | [snap-kit-action-execute-deferred](#snap-kit-action-execute-deferred) |

<a id="snap-kit-action-execute-deferred"></a>

## `POST /snap-kit-action.execute.deferred`

**Deferred Snap Kit Action Execute**

Source: <https://developer.devrev.ai/beta/api-reference/snap-kit-execution/snap-kit-action-execute-deferred>

Executes deferred snap-kit actions.

**Required scopes:**

- `snap_widget:write` OR `snap_widget:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `actions` | yes | `array<snap-kit-action-request>` | List of actions triggered in the request.<br>*Items: items <= 5* |
| `id` | yes | `string` | ID of the deferred snap-kit action to be executed.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/snap-kit-action.execute.deferred" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [
      {
        "type": "button",
        "action_id": "string",
        "timestamp": "2023-01-01T12:00:00.000Z",
        "value": "string"
      }
    ],
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "function_result": {
    "detail": "string",
    "status": "string"
  }
}
```

</details>
