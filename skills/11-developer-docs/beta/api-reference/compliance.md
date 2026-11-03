# Compliance

Source: <https://developer.devrev.ai/beta/api-reference/compliance>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/audit-logs.fetch` | [export-audit-logs](#export-audit-logs) |
| POST | `/rev-users.delete-personal-data` | [delete-rev-users-personal-data](#delete-rev-users-personal-data) |
| POST | `/rev-users.personal-data` | [get-rev-users-personal-data](#get-rev-users-personal-data) |

<a id="export-audit-logs"></a>

## `POST /audit-logs.fetch`

**Fetch Audit Logs**

Source: <https://developer.devrev.ai/beta/api-reference/compliance/export-audit-logs>

Retrieves audit logs.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `categories` | no | `array<method-options-tag-value>` | Categories of the logs to filter by. |
| `from` | yes | `string` | Time from which logs are to be retrieved.<br>*Format: date-time* |
| `operation_types` | no | `array<export-audit-logs-request-operation-type>` | Operation type to filter the logs by. |
| `to` | yes | `string` | Time till which logs are to be retrieved.<br>*Format: date-time* |
| `users` | no | `array<string>` | A list of IDs representing the individuals whose audit logs are being requested. |

### Response codes

- `202` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `404` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/audit-logs.fetch" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "2023-01-01T12:00:00.000Z",
    "to": "2023-01-01T12:00:00.000Z"
  }'
```

<details><summary>Example 202 response</summary>

```json
{}
```

</details>


<a id="delete-rev-users-personal-data"></a>

## `POST /rev-users.delete-personal-data`

**Delete-Personal-Data Rev Users**

Source: <https://developer.devrev.ai/beta/api-reference/compliance/delete-rev-users-personal-data>

Deletes data of a contact.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `email` | yes | `string` | Email of the contact.<br>*Format: text* |

### Response codes

- `202` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `404` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/rev-users.delete-personal-data" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "string"
  }'
```

<details><summary>Example 202 response</summary>

```json
{}
```

</details>


<a id="get-rev-users-personal-data"></a>

## `POST /rev-users.personal-data`

**Personal-Data Rev Users**

Source: <https://developer.devrev.ai/beta/api-reference/compliance/get-rev-users-personal-data>

Retrieves data of a contact.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `email` | yes | `string` | Email of the contact.<br>*Format: text* |

### Response codes

- `202` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `404` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/rev-users.personal-data" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "string"
  }'
```

<details><summary>Example 202 response</summary>

```json
{}
```

</details>
