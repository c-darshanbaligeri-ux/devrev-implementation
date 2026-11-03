# Record Templates

Source: <https://developer.devrev.ai/beta/api-reference/record-templates>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/record-templates.get` | [record-template-get](#record-template-get) |
| POST | `/record-templates.get` | [record-template-get-post](#record-template-get-post) |

<a id="record-template-get"></a>

## `GET /record-templates.get`

**Get Record Template**

Source: <https://developer.devrev.ai/beta/api-reference/record-templates/record-template-get>

Gets a record template object.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the record template.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/record-templates.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "record_template_info": {
    "record_template": {
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
      "custom_fields": [
        {
          "field_name": "string",
          "field_value": null
        }
      ],
      "description": "string",
      "leaf_type": "string",
      "name": "string",
      "shared_with": [
        {
          "member": {
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
          "role": {
            "display_id": "string",
            "id": "string",
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
          }
        }
      ],
      "state": "active",
      "stock_fields": [
        {
          "field_name": "string",
          "field_value": null
        }
      ],
      "subtype": "string"
    },
    "stale_fields": [
      {
        "field_name": "string",
        "field_value": null
      }
    ]
  }
}
```

</details>


<a id="record-template-get-post"></a>

## `POST /record-templates.get`

**Get Record Template (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/record-templates/record-template-get-post>

Gets a record template object.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the record template.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/record-templates.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "record_template_info": {
    "record_template": {
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
      "custom_fields": [
        {
          "field_name": "string",
          "field_value": null
        }
      ],
      "description": "string",
      "leaf_type": "string",
      "name": "string",
      "shared_with": [
        {
          "member": {
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
          "role": {
            "display_id": "string",
            "id": "string",
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
          }
        }
      ],
      "state": "active",
      "stock_fields": [
        {
          "field_name": "string",
          "field_value": null
        }
      ],
      "subtype": "string"
    },
    "stale_fields": [
      {
        "field_name": "string",
        "field_value": null
      }
    ]
  }
}
```

</details>
