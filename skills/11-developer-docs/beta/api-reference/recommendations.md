# Recommendations

Source: <https://developer.devrev.ai/beta/api-reference/recommendations>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/recommendations.chat.completions` | [chat-completions](#chat-completions) |
| POST | `/recommendations.get-reply` | [get-reply](#get-reply) |

<a id="chat-completions"></a>

## `POST /recommendations.chat.completions`

**Completions Recommendations Chat**

Source: <https://developer.devrev.ai/beta/api-reference/recommendations/chat-completions>

Returns a response for the chat conversation.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `max_tokens` | no | `integer` | The maximum number of tokens that can be generated in the chat completion.<br>*Format: int32* |
| `messages` | yes | `array<chat-completions-request-message>` | A list of messages comprising the conversation so far.<br>*Items: 1 <= items* |
| `stop_sequences` | no | `array<string>` | Sequences where the API will stop generating further tokens. Maximum of 4 sequences are supported. Defaults to none. |
| `stream` | no | `boolean` | If set, partial message deltas will be sent. Defaults to false. |
| `temperature` | no | `number` | What sampling temperature to use. Value can be between 0 and 2 and defaults to 1.0. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>*Format: float* |
| `top_p` | no | `number` | An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. For openai: Between 0 and<br>1. Defaults to 1.0.<br>*Format: float* |

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
curl -X POST "https://api.devrev.ai/recommendations.chat.completions" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "assistant"
      }
    ]
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "text_response": "string"
}
```

</details>


<a id="get-reply"></a>

## `POST /recommendations.get-reply`

**Get-Reply Recommendations**

Source: <https://developer.devrev.ai/beta/api-reference/recommendations/get-reply>

Gets a reply for a user query.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `language` | no | `string` | The language in which Turing should operate. The language should be passed in IETF BCP 47 format. If not specified, defaults to en-US.<br>*Format: text* |
| `query` | yes | `string` | The query string.<br>*Format: text*<br>*Length: 1 <= length <= 10000* |

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
curl -X POST "https://api.devrev.ai/recommendations.get-reply" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "reply": "string",
  "sources": [
    {
      "type": "article",
      "display_id": "string",
      "id": "string",
      "article_type": "article",
      "resource": {
        "artifacts": [
          {
            "display_id": "string",
            "id": "string",
            "file": {
              "type": "string",
              "name": "string",
              "size": 0
            }
          }
        ],
        "url": "string"
      },
      "sync_metadata": {
        "external_reference": "string",
        "last_sync_in": {
          "status": "failed",
          "sync_unit": {
            "display_id": "string",
            "id": "string",
            "external_sync_unit_name": "string",
            "external_system_id": "string",
            "external_system_name": "string",
            "external_system_type": "adaas",
            "is_archived": true,
            "name": "string",
            "sync_run": {
              "mode": "initial",
              "progress": {
                "state": "completed"
              },
              "reserved_rate_limit_percentage": 0
            },
            "sync_type": "manual"
          }
        },
        "origin_system": "string"
      },
      "title": "string"
    }
  ]
}
```

</details>
