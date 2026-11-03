# Keyrings

Source: <https://developer.devrev.ai/api-reference/keyrings>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/keyrings.authorize` | [create-callback](#create-callback) |
| POST | `/keyrings.authorize` | [create-callback-post](#create-callback-post) |

<a id="create-callback"></a>

## `GET /keyrings.authorize`

**Authorize Keyrings**

Source: <https://developer.devrev.ai/api-reference/keyrings/create-callback>

OAuth2 authorization callback.

**Required scopes:**

- `keyring:read`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `code` | yes | `string` | Code to exchange for an access token.<br>*Format: text* |
| `state` | yes | `string` | State value given to the authorization request.<br>*Format: text* |

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
curl -X GET "https://api.devrev.ai/keyrings.authorize?code=string&state=string"
```


<a id="create-callback-post"></a>

## `POST /keyrings.authorize`

**Authorize Keyrings (POST)**

Source: <https://developer.devrev.ai/api-reference/keyrings/create-callback-post>

OAuth2 authorization callback.

**Required scopes:**

- `keyring:read`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `code` | yes | `string` | Code to exchange for an access token.<br>*Format: text* |
| `state` | yes | `string` | State value given to the authorization request.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/keyrings.authorize" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "string",
    "state": "string"
  }'
```
