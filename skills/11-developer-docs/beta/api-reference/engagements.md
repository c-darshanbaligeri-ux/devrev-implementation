# Engagements

Source: <https://developer.devrev.ai/beta/api-reference/engagements>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/engagements.count` | [count](#count) |
| POST | `/engagements.count` | [count-post](#count-post) |
| POST | `/engagements.create` | [create](#create) |
| POST | `/engagements.delete` | [delete](#delete) |
| GET | `/engagements.get` | [get](#get) |
| POST | `/engagements.get` | [get-post](#get-post) |
| GET | `/engagements.list` | [list](#list) |
| POST | `/engagements.list` | [list-post](#list-post) |
| POST | `/engagements.update` | [update](#update) |

<a id="count"></a>

## `GET /engagements.count`

**Count Engagements**

Source: <https://developer.devrev.ai/beta/api-reference/engagements/count>

Counts the engagement records.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `external_ref` | no | `array<string>` | Filters for meetings with the provided external_refs. |
| `members` | no | `array<string>` | Filters for engagement of the provided members. |
| `parent` | no | `array<string>` | Filters for engagements with the provided parent. |
| `type` | no | `array<engagement-type>` | Filters for engagement of the provided types. |

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
curl -X GET "https://api.devrev.ai/engagements.count"
```

<details><summary>Example 200 response</summary>

```json
{
  "count": 0
}
```

</details>


<a id="count-post"></a>

## `POST /engagements.count`

**Count Engagements (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/engagements/count-post>

Counts the engagement records.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `array<engagement-type>` | Filters for engagement of the provided types. |
| `external_ref` | no | `array<string>` | Filters for meetings with the provided external_refs. |
| `members` | no | `array<string>` | Filters for engagement of the provided members. |
| `parent` | no | `array<string>` | Filters for engagements with the provided parent. |

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
curl -X POST "https://api.devrev.ai/engagements.count" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "count": 0
}
```

</details>


<a id="create"></a>

## `POST /engagements.create`

**Create Engagement**

Source: <https://developer.devrev.ai/beta/api-reference/engagements/create>

Creates a new engagement record.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `artifacts` | no | `array<string>` | The IDs of the artifacts to associate with the engagement. |
| `description` | no | `string` | The description of the engagement.<br>*Format: text* |
| `engagement_type` | no | `string` | The type of engagement.<br>*Value in: "call" \| "default" \| "email" \| "linked_in" \| "offline"* |
| `external_ref` | no | `string` | External Reference for the engagement.<br>*Format: text* |
| `external_url` | no | `string` | External URL for the engagement.<br>*Format: text* |
| `members` | yes | `array<string>` | IDs of the users that were part of the engagement.<br>*Items: 1 <= items <= 50* |
| `parent` | no | `string` | The parent object ID in which the engagement was created. Currently, only accounts and opportunities are supported.<br>*Format: id* |
| `parents` | no | `array<string>` | The parent object IDs to which the engagement is associated. Currently, only accounts and opportunities are supported. |
| `scheduled_date` | yes | `string` | The date and time when the engagement was scheduled.<br>*Format: date-time* |
| `tags` | no | `array<set-tag-with-value>` | Tags associated with the engagement. |
| `title` | yes | `string` | The title of the engagement.<br>*Format: text* |

### Response codes

- `201` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/engagements.create" \
  -H "Content-Type: application/json" \
  -d '{
    "members": [
      "DEVU-12345"
    ],
    "scheduled_date": "2023-01-01T12:00:00.000Z",
    "title": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "engagement": {
    "created_by": {
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
    },
    "created_date": "2023-01-01T12:00:00.000Z",
    "display_id": "string",
    "id": "string",
    "modified_by": {
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
    },
    "modified_date": "2023-01-01T12:00:00.000Z",
    "object_version": 0,
    "description": "string"
  }
}
```

</details>


<a id="delete"></a>

## `POST /engagements.delete`

**Delete Engagement**

Source: <https://developer.devrev.ai/beta/api-reference/engagements/delete>

Deletes the engagement record.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The engagement ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/engagements.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="get"></a>

## `GET /engagements.get`

**Get Engagement**

Source: <https://developer.devrev.ai/beta/api-reference/engagements/get>

Gets the engagement record.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The engagement ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/engagements.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "engagement": {
    "created_by": {
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
    },
    "created_date": "2023-01-01T12:00:00.000Z",
    "display_id": "string",
    "id": "string",
    "modified_by": {
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
    },
    "modified_date": "2023-01-01T12:00:00.000Z",
    "object_version": 0,
    "description": "string"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /engagements.get`

**Get Engagement (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/engagements/get-post>

Gets the engagement record.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The engagement ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/engagements.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "engagement": {
    "created_by": {
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
    },
    "created_date": "2023-01-01T12:00:00.000Z",
    "display_id": "string",
    "id": "string",
    "modified_by": {
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
    },
    "modified_date": "2023-01-01T12:00:00.000Z",
    "object_version": 0,
    "description": "string"
  }
}
```

</details>


<a id="list"></a>

## `GET /engagements.list`

**List Engagements**

Source: <https://developer.devrev.ai/beta/api-reference/engagements/list>

Lists the engagement records.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `external_ref` | no | `array<string>` | Filters for meetings with the provided external_refs. |
| `limit` | no | `integer` | The maximum number of engagements to return.<br>*Format: int32* |
| `members` | no | `array<string>` | Filters for engagement of the provided members. |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `parent` | no | `array<string>` | Filters for engagements with the provided parent. |
| `sort_by` | no | `array<string>` | Fields to sort the engagements by and the direction to sort them. |
| `type` | no | `array<engagement-type>` | Filters for engagement of the provided types. |

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
curl -X GET "https://api.devrev.ai/engagements.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "engagements": [
    {
      "created_by": {
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
      },
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {
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
      },
      "modified_date": "2023-01-01T12:00:00.000Z",
      "object_version": 0,
      "description": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="list-post"></a>

## `POST /engagements.list`

**List Engagements (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/engagements/list-post>

Lists the engagement records.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `array<engagement-type>` | Filters for engagement of the provided types. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `external_ref` | no | `array<string>` | Filters for meetings with the provided external_refs. |
| `limit` | no | `integer` | The maximum number of engagements to return.<br>*Format: int32* |
| `members` | no | `array<string>` | Filters for engagement of the provided members. |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `parent` | no | `array<string>` | Filters for engagements with the provided parent. |
| `sort_by` | no | `array<string>` | Fields to sort the engagements by and the direction to sort them. |

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
curl -X POST "https://api.devrev.ai/engagements.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "engagements": [
    {
      "created_by": {
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
      },
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {
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
      },
      "modified_date": "2023-01-01T12:00:00.000Z",
      "object_version": 0,
      "description": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="update"></a>

## `POST /engagements.update`

**Update Engagement**

Source: <https://developer.devrev.ai/beta/api-reference/engagements/update>

Updates the engagement record.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `artifacts` | no | `engagements-update-request-artifact-ids` |  |
| `description` | no | `string` | Updates the description of the engagement.<br>*Format: text* |
| `external_ref` | no | `string` | External Reference for the engagement.<br>*Format: text* |
| `external_url` | no | `string` | Updates the external URL for the engagement.<br>*Format: text* |
| `id` | yes | `string` | The engagement ID.<br>*Format: id* |
| `members` | no | `engagements-update-request-members` |  |
| `parents` | no | `engagements-update-request-parents` |  |
| `scheduled_date` | no | `string\|null` | Updates the date and time when the engagement was scheduled.<br>*Format: date-time* |
| `tags` | no | `engagements-update-request-tags` |  |
| `title` | no | `string` | Updates the title of the engagement.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/engagements.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "engagement": {
    "created_by": {
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
    },
    "created_date": "2023-01-01T12:00:00.000Z",
    "display_id": "string",
    "id": "string",
    "modified_by": {
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
    },
    "modified_date": "2023-01-01T12:00:00.000Z",
    "object_version": 0,
    "description": "string"
  }
}
```

</details>
