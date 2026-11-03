# Metrics

Source: <https://developer.devrev.ai/beta/api-reference/metrics>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/metrics.devrev.ingest` | [devrev-ingest](#devrev-ingest) |

<a id="devrev-ingest"></a>

## `POST /metrics.devrev.ingest`

**Ingest Metrics Devrev**

Source: <https://developer.devrev.ai/beta/api-reference/metrics/devrev-ingest>

Ingest endpoint for DevRev metrics data from clients.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `metrics` | yes | `array<metrics-data>` | Metrics data received from Dev orgs.<br>*Items: 1 <= items* |

### Response codes

- `200` — empty body
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/metrics.devrev.ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": [
      {
        "account_ref": "string",
        "data_points": [
          {
            "timestamp": "2023-01-01T12:00:00.000Z",
            "value": 0.1
          }
        ],
        "name": "string"
      }
    ]
  }'
```
