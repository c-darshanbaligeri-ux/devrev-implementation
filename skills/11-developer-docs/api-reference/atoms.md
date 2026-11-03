# Atoms

Source: <https://developer.devrev.ai/api-reference/atoms>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/atoms.get` | [get](#get) |
| POST | `/atoms.get` | [get-post](#get-post) |

<a id="get"></a>

## `GET /atoms.get`

**Get Atom**

Source: <https://developer.devrev.ai/api-reference/atoms/get>

Gets the specified object.

**Required scopes:** Depends on the object type identified by the `id` field. Pattern: `{object_type}:read` — e.g. `issue:read`, `ticket:read`.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the object to get.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/atoms.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "atom": {
    "type": "account",
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
    "display_name": "string",
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
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "domains": [
      "string"
    ],
    "external_refs": [
      "string"
    ],
    "owned_by": [
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
    ],
    "primary_account": {
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "tags": [
      {
        "tag": {
          "display_id": "string",
          "id": "string",
          "name": "string",
          "style_new": {
            "color": "string"
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
          }
        },
        "value": "string"
      }
    ],
    "tier": "string",
    "websites": [
      "string"
    ]
  }
}
```

</details>


<a id="get-post"></a>

## `POST /atoms.get`

**Get Atom (POST)**

Source: <https://developer.devrev.ai/api-reference/atoms/get-post>

Gets the specified object.

**Required scopes:** Depends on the object type identified by the `id` field. Pattern: `{object_type}:read` — e.g. `issue:read`, `ticket:read`.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the object to get.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/atoms.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "atom": {
    "type": "account",
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
    "display_name": "string",
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
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "domains": [
      "string"
    ],
    "external_refs": [
      "string"
    ],
    "owned_by": [
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
    ],
    "primary_account": {
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "tags": [
      {
        "tag": {
          "display_id": "string",
          "id": "string",
          "name": "string",
          "style_new": {
            "color": "string"
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
          }
        },
        "value": "string"
      }
    ],
    "tier": "string",
    "websites": [
      "string"
    ]
  }
}
```

</details>
