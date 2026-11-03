# Snap Ins

Source: <https://developer.devrev.ai/beta/api-reference/snap-ins>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/snap-ins.list` | [list](#list) |
| POST | `/snap-ins.list` | [list-post](#list-post) |
| GET | `/snap-ins.resources` | [resources](#resources) |
| POST | `/snap-ins.resources` | [resources-post](#resources-post) |
| POST | `/snap-ins.update` | [update](#update) |

<a id="list"></a>

## `GET /snap-ins.list`

**List Snap Ins**

Source: <https://developer.devrev.ai/beta/api-reference/snap-ins/list>

Lists snap-ins for a Dev organization.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of snap-ins to return. The default is '50', the maximum is '100'.<br>*Format: int32* |
| `marketplace_item.marketplace` | no | `string` | The marketplace to filter by.<br>*Format: id* |
| `marketplace_item.marketplace_item_slug` | no | `string` | The marketplace item slug to filter by.<br>*Format: text* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `service_account` | no | `array<string>` | Filter for service account associated with snap-in. |
| `snap_in_version` | no | `array<string>` | Filter for snap-in version associated with snap-in. |
| `sort_by` | no | `array<string>` | Fields to sort the snap-ins by and the direction to sort them. |

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
curl -X GET "https://api.devrev.ai/snap-ins.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "snap_ins": [
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
      "inputs_values": {}
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /snap-ins.list`

**List Snap Ins (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/snap-ins/list-post>

Lists snap-ins for a Dev organization.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of snap-ins to return. The default is '50', the maximum is '100'.<br>*Format: int32* |
| `marketplace_item` | no | `array<snap-ins-list-request-filter-marketplace-item-filter>` | Filter for marketplace-item associated with snap-in. |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `service_account` | no | `array<string>` | Filter for service account associated with snap-in. |
| `snap_in_version` | no | `array<string>` | Filter for snap-in version associated with snap-in. |
| `sort_by` | no | `array<string>` | Fields to sort the snap-ins by and the direction to sort them. |

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
curl -X POST "https://api.devrev.ai/snap-ins.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "snap_ins": [
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
      "inputs_values": {}
    }
  ]
}
```

</details>


<a id="resources"></a>

## `GET /snap-ins.resources`

**Resources Snap Ins**

Source: <https://developer.devrev.ai/beta/api-reference/snap-ins/resources>

Gets snap-in resources for a user in a snap-in.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the snap-in to get resources for.<br>*Format: id* |
| `user` | yes | `string` | The ID of the user to get resources for.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/snap-ins.resources?id=string&user=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "event_sources": {
    "property1": "string",
    "property2": "string"
  },
  "inputs": {},
  "keyrings": {
    "property1": {
      "id": "string",
      "is_expired": true,
      "secret": "string"
    },
    "property2": {
      "id": "string",
      "is_expired": true,
      "secret": "string"
    }
  },
  "snap_in_version": {
    "display_id": "string",
    "id": "string"
  }
}
```

</details>


<a id="resources-post"></a>

## `POST /snap-ins.resources`

**Resources Snap Ins (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/snap-ins/resources-post>

Gets snap-in resources for a user in a snap-in.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the snap-in to get resources for.<br>*Format: id* |
| `user` | yes | `string` | The ID of the user to get resources for.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/snap-ins.resources" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string",
    "user": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "event_sources": {
    "property1": "string",
    "property2": "string"
  },
  "inputs": {},
  "keyrings": {
    "property1": {
      "id": "string",
      "is_expired": true,
      "secret": "string"
    },
    "property2": {
      "id": "string",
      "is_expired": true,
      "secret": "string"
    }
  },
  "snap_in_version": {
    "display_id": "string",
    "id": "string"
  }
}
```

</details>


<a id="update"></a>

## `POST /snap-ins.update`

**Update Snap In**

Source: <https://developer.devrev.ai/beta/api-reference/snap-ins/update>

Updates a snap-in.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the snap-in to update.<br>*Format: id* |
| `inputs_values` | no | `object` | The updated values of the inputs. |

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
curl -X POST "https://api.devrev.ai/snap-ins.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "snap_in": {
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
    "inputs_values": {}
  }
}
```

</details>
