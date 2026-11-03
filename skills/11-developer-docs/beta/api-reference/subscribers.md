# Subscribers

Source: <https://developer.devrev.ai/beta/api-reference/subscribers>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/subscribers.get` | [get](#get) |
| POST | `/subscribers.get` | [get-post](#get-post) |
| GET | `/subscribers.list` | [list](#list) |
| POST | `/subscribers.list` | [list-post](#list-post) |
| POST | `/subscribers.update` | [update](#update) |

<a id="get"></a>

## `GET /subscribers.get`

**Get Subscriber**

Source: <https://developer.devrev.ai/beta/api-reference/subscribers/get>

Gets the requesting user's subscriber status for an object.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The object's ID.<br>*Format: id* |

### Response codes

- `200` — `application/json`
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
curl -X GET "https://api.devrev.ai/subscribers.get?id=ISS-12345"
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="get-post"></a>

## `POST /subscribers.get`

**Get Subscriber (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/subscribers/get-post>

Gets the requesting user's subscriber status for an object.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The object's ID.<br>*Format: id* |

### Response codes

- `200` — `application/json`
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
curl -X POST "https://api.devrev.ai/subscribers.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ISS-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="list"></a>

## `GET /subscribers.list`

**List Subscribers**

Source: <https://developer.devrev.ai/beta/api-reference/subscribers/list>

Lists subscribers of an object.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The object's ID.<br>*Format: id* |
| `cursor` | no | `string` | The cursor to resume iteration from, otherwise if not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of subscribers to return. If not set or `<= 0`, then this defaults to `50`.<br>*Format: int32* |

### Response codes

- `200` — `application/json`
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
curl -X GET "https://api.devrev.ai/subscribers.list?id=ISS-12345"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "users": [
    {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /subscribers.list`

**List Subscribers (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/subscribers/list-post>

Lists subscribers of an object.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from, otherwise if not provided, then iteration starts from the beginning.<br>*Format: text* |
| `id` | yes | `string` | The object's ID.<br>*Format: id* |
| `limit` | no | `integer` | The maximum number of subscribers to return. If not set or `<= 0`, then this defaults to `50`.<br>*Format: int32* |

### Response codes

- `200` — `application/json`
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
curl -X POST "https://api.devrev.ai/subscribers.list" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ISS-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "users": [
    {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    }
  ]
}
```

</details>


<a id="update"></a>

## `POST /subscribers.update`

**Update Subscriber**

Source: <https://developer.devrev.ai/beta/api-reference/subscribers/update>

Updates subscribers on the object.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The object's ID.<br>*Format: id* |
| `subscribers` | no | `subscribers-update-request-subscribers` |  |

### Response codes

- `200` — `application/json`
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
curl -X POST "https://api.devrev.ai/subscribers.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ISS-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>
