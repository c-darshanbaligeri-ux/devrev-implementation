# Other

Source: <https://developer.devrev.ai/beta/api-reference/other>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/ping` | [ping](#ping) |
| POST | `/ping` | [ping-post](#ping-post) |

<a id="ping"></a>

## `GET /ping`

**Ping**

Source: <https://developer.devrev.ai/beta/api-reference/other/ping>

Pings the DevRev service.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `devrev_partition` | no | `string` | DevRev partion ID. For example, dvrv-us-1 for the us-east-1 region.<br>*Format: text* |

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
curl -X GET "https://api.devrev.ai/ping"
```

<details><summary>Example 200 response</summary>

```json
{
  "timestamp": "2023-01-01T12:00:00.000Z"
}
```

</details>


<a id="ping-post"></a>

## `POST /ping`

**Ping (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/other/ping-post>

Pings the DevRev service.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `devrev_partition` | no | `string` | DevRev partion ID. For example, dvrv-us-1 for the us-east-1 region.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/ping" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "timestamp": "2023-01-01T12:00:00.000Z"
}
```

</details>
