# Customization

Source: <https://developer.devrev.ai/api-reference/customization>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/custom-objects.count` | [custom-objects-count](#custom-objects-count) |
| POST | `/custom-objects.count` | [custom-objects-count-post](#custom-objects-count-post) |
| POST | `/custom-objects.create` | [custom-objects-create](#custom-objects-create) |
| POST | `/custom-objects.delete` | [custom-objects-delete](#custom-objects-delete) |
| GET | `/custom-objects.get` | [custom-objects-get](#custom-objects-get) |
| POST | `/custom-objects.get` | [custom-objects-get-post](#custom-objects-get-post) |
| GET | `/custom-objects.list` | [custom-objects-list](#custom-objects-list) |
| POST | `/custom-objects.list` | [custom-objects-list-post](#custom-objects-list-post) |
| POST | `/custom-objects.update` | [custom-objects-update](#custom-objects-update) |
| GET | `/schemas.aggregated.get` | [aggregated-schema-get](#aggregated-schema-get) |
| POST | `/schemas.aggregated.get` | [aggregated-schema-get-post](#aggregated-schema-get-post) |
| GET | `/schemas.custom.get` | [custom-schema-fragments-get](#custom-schema-fragments-get) |
| POST | `/schemas.custom.get` | [custom-schema-fragments-get-post](#custom-schema-fragments-get-post) |
| GET | `/schemas.custom.list` | [custom-schema-fragments-list](#custom-schema-fragments-list) |
| POST | `/schemas.custom.list` | [custom-schema-fragments-list-post](#custom-schema-fragments-list-post) |
| POST | `/schemas.custom.set` | [custom-schema-fragments-set](#custom-schema-fragments-set) |
| GET | `/schemas.stock.get` | [stock-schema-fragments-get](#stock-schema-fragments-get) |
| POST | `/schemas.stock.get` | [stock-schema-fragments-get-post](#stock-schema-fragments-get-post) |
| GET | `/schemas.stock.list` | [stock-schema-fragments-list](#stock-schema-fragments-list) |
| POST | `/schemas.stock.list` | [stock-schema-fragments-list-post](#stock-schema-fragments-list-post) |
| POST | `/schemas.subtypes.prepare-update` | [schemas-subtype-prepare-update-get](#schemas-subtype-prepare-update-get) |
| POST | `/stage-diagrams.create` | [stage-diagrams-create](#stage-diagrams-create) |
| GET | `/stage-diagrams.get` | [stage-diagrams-get](#stage-diagrams-get) |
| POST | `/stage-diagrams.get` | [stage-diagrams-get-post](#stage-diagrams-get-post) |
| GET | `/stage-diagrams.list` | [stage-diagrams-list](#stage-diagrams-list) |
| POST | `/stage-diagrams.list` | [stage-diagrams-list-post](#stage-diagrams-list-post) |
| POST | `/stage-diagrams.update` | [stage-diagrams-update](#stage-diagrams-update) |
| POST | `/stages.custom.create` | [custom-stages-create](#custom-stages-create) |
| GET | `/stages.custom.get` | [custom-stages-get](#custom-stages-get) |
| POST | `/stages.custom.get` | [custom-stages-get-post](#custom-stages-get-post) |
| GET | `/stages.custom.list` | [custom-stages-list](#custom-stages-list) |
| POST | `/stages.custom.list` | [custom-stages-list-post](#custom-stages-list-post) |
| POST | `/stages.custom.update` | [custom-stages-update](#custom-stages-update) |
| POST | `/states.custom.create` | [custom-states-create](#custom-states-create) |
| GET | `/states.custom.get` | [custom-states-get](#custom-states-get) |
| POST | `/states.custom.get` | [custom-states-get-post](#custom-states-get-post) |
| GET | `/states.custom.list` | [custom-states-list](#custom-states-list) |
| POST | `/states.custom.list` | [custom-states-list-post](#custom-states-list-post) |
| POST | `/states.custom.update` | [custom-states-update](#custom-states-update) |

<a id="custom-objects-count"></a>

## `GET /custom-objects.count`

**Count Custom Objects**

Source: <https://developer.devrev.ai/api-reference/customization/custom-objects-count>

Counts custom objects.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `leaf_type` | yes | `string` | Leaf type to filter.<br>*Format: text* |
| `filters` | no | `array<unknown>` | List of filters to apply. |

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
curl -X GET "https://api.devrev.ai/custom-objects.count?leaf_type=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "count": 0
}
```

</details>


<a id="custom-objects-count-post"></a>

## `POST /custom-objects.count`

**Count Custom Objects (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/custom-objects-count-post>

Counts custom objects.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `filters` | no | `array<unknown>` | List of filters to apply. |
| `leaf_type` | yes | `string` | Leaf type to filter.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/custom-objects.count" \
  -H "Content-Type: application/json" \
  -d '{
    "leaf_type": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "count": 0
}
```

</details>


<a id="custom-objects-create"></a>

## `POST /custom-objects.create`

**Create Custom Object**

Source: <https://developer.devrev.ai/api-reference/customization/custom-objects-create>

Creates a custom object.

**Required scopes:**

- `custom_type_fragment:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `custom_fields` | no | `object` | Custom fields of the custom object. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | Description of the custom object.<br>*Format: text*<br>*Length: length <= 65536* |
| `leaf_type` | yes | `string` | Leaf type of the custom object.<br>*Format: text* |
| `stage` | no | `string` | The stage of the custom object.<br>*Format: id* |
| `stage_validation_options` | no | `array<stage-validation-option-for-create>` | The type of stage validations options when creating a custom object. |
| `title` | no | `string` | Title of the custom object.<br>*Format: text* |
| `unique_key` | no | `string` | The unique key of the custom object.This can be used to hold an external reference to another object.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/custom-objects.create" \
  -H "Content-Type: application/json" \
  -d '{
    "leaf_type": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "custom_object": {
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
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "leaf_type": "string",
    "stage": {
      "stage": {
        "display_id": "string",
        "id": "string",
        "name": "string",
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
      "state": {
        "display_id": "string",
        "id": "string",
        "is_final": true,
        "name": "string",
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
    },
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
    "title": "string",
    "unique_key": "string"
  }
}
```

</details>


<a id="custom-objects-delete"></a>

## `POST /custom-objects.delete`

**Delete Custom Object**

Source: <https://developer.devrev.ai/api-reference/customization/custom-objects-delete>

Deletes a custom object.

**Required scopes:**

- `custom_type_fragment:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the custom object to get.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/custom-objects.delete" \
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


<a id="custom-objects-get"></a>

## `GET /custom-objects.get`

**Get Custom Object**

Source: <https://developer.devrev.ai/api-reference/customization/custom-objects-get>

Gets a custom object.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | no | `string` | The ID of the custom object to get.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/custom-objects.get"
```

<details><summary>Example 200 response</summary>

```json
{
  "custom_object": {
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
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "leaf_type": "string",
    "stage": {
      "stage": {
        "display_id": "string",
        "id": "string",
        "name": "string",
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
      "state": {
        "display_id": "string",
        "id": "string",
        "is_final": true,
        "name": "string",
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
    },
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
    "title": "string",
    "unique_key": "string"
  }
}
```

</details>


<a id="custom-objects-get-post"></a>

## `POST /custom-objects.get`

**Get Custom Object (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/custom-objects-get-post>

Gets a custom object.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | no | `string` | The ID of the custom object to get.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/custom-objects.get" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "custom_object": {
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
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "leaf_type": "string",
    "stage": {
      "stage": {
        "display_id": "string",
        "id": "string",
        "name": "string",
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
      "state": {
        "display_id": "string",
        "id": "string",
        "is_final": true,
        "name": "string",
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
    },
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
    "title": "string",
    "unique_key": "string"
  }
}
```

</details>


<a id="custom-objects-list"></a>

## `GET /custom-objects.list`

**List Custom Objects**

Source: <https://developer.devrev.ai/api-reference/customization/custom-objects-list>

Lists custom objects.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `leaf_type` | yes | `string` | Leaf type to filter.<br>*Format: text* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `filter` | no | `array<unknown>` | List of filters to apply. |
| `filters` | no | `array<unknown>` | List of filters to apply. |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |

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
curl -X GET "https://api.devrev.ai/custom-objects.list?leaf_type=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "result": [
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
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "leaf_type": "string",
      "stage": {
        "stage": {
          "display_id": "string",
          "id": "string",
          "name": "string",
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
        "state": {
          "display_id": "string",
          "id": "string",
          "is_final": true,
          "name": "string",
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
      },
      "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
      "subtype": "string",
      "sync_metadata": {
        "external_record_id": "string",
        "external_record_type": "string",
        "external_reference": "string",
        "last_sync_in": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
        "last_sync_out": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
      "title": "string",
      "unique_key": "string"
    }
  ]
}
```

</details>


<a id="custom-objects-list-post"></a>

## `POST /custom-objects.list`

**List Custom Objects (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/custom-objects-list-post>

Lists custom objects.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `filter` | no | `array<unknown>` | List of filters to apply. |
| `filters` | no | `array<unknown>` | List of filters to apply. |
| `leaf_type` | yes | `string` | Leaf type to filter.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |

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
curl -X POST "https://api.devrev.ai/custom-objects.list" \
  -H "Content-Type: application/json" \
  -d '{
    "leaf_type": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "result": [
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
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "leaf_type": "string",
      "stage": {
        "stage": {
          "display_id": "string",
          "id": "string",
          "name": "string",
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
        "state": {
          "display_id": "string",
          "id": "string",
          "is_final": true,
          "name": "string",
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
      },
      "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
      "subtype": "string",
      "sync_metadata": {
        "external_record_id": "string",
        "external_record_type": "string",
        "external_reference": "string",
        "last_sync_in": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
        "last_sync_out": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
      "title": "string",
      "unique_key": "string"
    }
  ]
}
```

</details>


<a id="custom-objects-update"></a>

## `POST /custom-objects.update`

**Update Custom Object**

Source: <https://developer.devrev.ai/api-reference/customization/custom-objects-update>

Updates a custom object.

**Required scopes:**

- `custom_type_fragment:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `custom_fields` | no | `object` | Custom fields of the custom object. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | Description of the custom object.<br>*Format: text*<br>*Length: length <= 65536* |
| `id` | yes | `string` | The ID of the custom object to update.<br>*Format: id* |
| `stage` | no | `string\|null` | Updates the stage of the custom object.<br>*Format: id* |
| `stage_validation_options` | no | `array<stage-validation-option-for-update>` | The type of stage validations options when updating the stage or the stage diagram of a custom object. |
| `title` | no | `string\|null` | Updates the title of the custom object.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/custom-objects.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "custom_object": {
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
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "leaf_type": "string",
    "stage": {
      "stage": {
        "display_id": "string",
        "id": "string",
        "name": "string",
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
      "state": {
        "display_id": "string",
        "id": "string",
        "is_final": true,
        "name": "string",
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
    },
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
    "title": "string",
    "unique_key": "string"
  }
}
```

</details>


<a id="aggregated-schema-get"></a>

## `GET /schemas.aggregated.get`

**Get Schemas Aggregated**

Source: <https://developer.devrev.ai/api-reference/customization/aggregated-schema-get>

Gets the aggregated schema.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `custom_schema_fragments` | no | `array<string>` | The custom schema fragment IDs which are to be aggregated. |
| `custom_schema_spec.apps` | no | `array<string>` | List of apps. |
| `custom_schema_spec.subtype` | no | `string` | Name of the subtype.<br>*Format: text* |
| `is_custom_leaf_type` | no | `boolean` | Whether the leaf type corresponds to a custom object. |
| `leaf_type` | no | `string` | The leaf type. Used for inferring the default stage diagram and tenant fragment ID.<br>*Format: text* |
| `stock_schema_fragment` | no | `string` | The stock schema fragment which is to be aggregated.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/schemas.aggregated.get"
```

<details><summary>Example 200 response</summary>

```json
{
  "schema": {
    "apps": [
      "string"
    ],
    "conditions": [
      {
        "effects": [
          {
            "allowed_values": [
              "string"
            ],
            "fields": [
              "string"
            ],
            "immutable": true,
            "invalid": true,
            "require": true,
            "show": true
          }
        ],
        "expression": "string"
      }
    ],
    "custom_composite_schemas": [
      {
        "description": "string",
        "fields": [
          {
            "field_type": "array",
            "description": "string",
            "is_derived": true,
            "is_filterable": true,
            "is_immutable": true,
            "is_pii": true,
            "is_required": true,
            "mfz": {},
            "name": "string",
            "oasis": {},
            "origin": "string",
            "ui": {
              "card_view": {
                "is_visible": true
              },
              "client_overrides": [
                {
                  "client_name": "string",
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_overrides": [
                    {
                      "decimal_places": 0,
                      "display_name": "string",
                      "is_groupable": true,
                      "is_hidden": true,
                      "is_required": true,
                      "order": 0,
                      "placeholder": "string",
                      "search_query": "string",
                      "tooltip": "string",
                      "use_shorthand_notation": true,
                      "view_name": "string"
                    }
                  ]
                }
              ],
              "create_view": {
                "is_hidden": true
              },
              "decimal_places": 0,
              "detail_view": {
                "is_hidden": true
              },
              "display_name": "string",
              "filter_view": {
                "is_hidden": true
              },
              "group_name": "string",
              "is_active_in_detail_view": true,
              "is_bulk_action_enabled": true,
              "is_currency_field": true,
              "is_groupable": true,
              "is_hidden": true,
              "is_hidden_during_create": true,
              "is_read_only": true,
              "is_required": true,
              "is_shown_in_summary": true,
              "is_sortable": true,
              "list_view": {
                "is_hidden": true
              },
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "summary_view": {
                "is_hidden": true
              },
              "tooltip": "string",
              "unit": "string",
              "use_shorthand_notation": true
            },
            "default_value": true
          }
        ],
        "name": "string"
      }
    ],
    "custom_fields": [
      {
        "field_type": "array",
        "description": "string",
        "is_derived": true,
        "is_filterable": true,
        "is_immutable": true,
        "is_pii": true,
        "is_required": true,
        "mfz": {},
        "name": "string",
        "oasis": {},
        "origin": "string",
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        },
        "default_value": true
      }
    ],
    "description": "string",
    "is_custom_leaf_type": true,
    "leaf_type": "string",
    "stage_diagram_id": {
      "display_id": "string",
      "id": "string",
      "name": "string",
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
    "stock_composite_schemas": [
      {
        "description": "string",
        "fields": [
          {
            "field_type": "array",
            "description": "string",
            "is_derived": true,
            "is_filterable": true,
            "is_immutable": true,
            "is_pii": true,
            "is_required": true,
            "mfz": {},
            "name": "string",
            "oasis": {},
            "origin": "string",
            "ui": {
              "card_view": {
                "is_visible": true
              },
              "client_overrides": [
                {
                  "client_name": "string",
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_overrides": [
                    {
                      "decimal_places": 0,
                      "display_name": "string",
                      "is_groupable": true,
                      "is_hidden": true,
                      "is_required": true,
                      "order": 0,
                      "placeholder": "string",
                      "search_query": "string",
                      "tooltip": "string",
                      "use_shorthand_notation": true,
                      "view_name": "string"
                    }
                  ]
                }
              ],
              "create_view": {
                "is_hidden": true
              },
              "decimal_places": 0,
              "detail_view": {
                "is_hidden": true
              },
              "display_name": "string",
              "filter_view": {
                "is_hidden": true
              },
              "group_name": "string",
              "is_active_in_detail_view": true,
              "is_bulk_action_enabled": true,
              "is_currency_field": true,
              "is_groupable": true,
              "is_hidden": true,
              "is_hidden_during_create": true,
              "is_read_only": true,
              "is_required": true,
              "is_shown_in_summary": true,
              "is_sortable": true,
              "list_view": {
                "is_hidden": true
              },
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "summary_view": {
                "is_hidden": true
              },
              "tooltip": "string",
              "unit": "string",
              "use_shorthand_notation": true
            },
            "default_value": true
          }
        ],
        "name": "string"
      }
    ],
    "stock_field_overrides": [
      {
        "is_required": true,
        "name": "string",
        "uenum_values": [
          {
            "id": 0,
            "is_deprecated": true,
            "label": "string",
            "ordinal": 0,
            "tooltip": "string"
          }
        ],
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        }
      }
    ],
    "stock_fields": [
      {
        "field_type": "array",
        "description": "string",
        "is_derived": true,
        "is_filterable": true,
        "is_immutable": true,
        "is_pii": true,
        "is_required": true,
        "mfz": {},
        "name": "string",
        "oasis": {},
        "origin": "string",
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        },
        "default_value": true
      }
    ],
    "subtype": "string",
    "subtype_display_name": "string",
    "title": "string"
  }
}
```

</details>


<a id="aggregated-schema-get-post"></a>

## `POST /schemas.aggregated.get`

**Get Schemas Aggregated (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/aggregated-schema-get-post>

Gets the aggregated schema.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `custom_schema_fragments` | no | `array<string>` | The custom schema fragment IDs which are to be aggregated. |
| `custom_schema_spec` | no | `custom-schema-spec-for-read` | Custom schemas described using identifiers |
| `is_custom_leaf_type` | no | `boolean` | Whether the leaf type corresponds to a custom object. |
| `leaf_type` | no | `string` | The leaf type. Used for inferring the default stage diagram and tenant fragment ID.<br>*Format: text* |
| `stock_schema_fragment` | no | `string` | The stock schema fragment which is to be aggregated.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/schemas.aggregated.get" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "schema": {
    "apps": [
      "string"
    ],
    "conditions": [
      {
        "effects": [
          {
            "allowed_values": [
              "string"
            ],
            "fields": [
              "string"
            ],
            "immutable": true,
            "invalid": true,
            "require": true,
            "show": true
          }
        ],
        "expression": "string"
      }
    ],
    "custom_composite_schemas": [
      {
        "description": "string",
        "fields": [
          {
            "field_type": "array",
            "description": "string",
            "is_derived": true,
            "is_filterable": true,
            "is_immutable": true,
            "is_pii": true,
            "is_required": true,
            "mfz": {},
            "name": "string",
            "oasis": {},
            "origin": "string",
            "ui": {
              "card_view": {
                "is_visible": true
              },
              "client_overrides": [
                {
                  "client_name": "string",
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_overrides": [
                    {
                      "decimal_places": 0,
                      "display_name": "string",
                      "is_groupable": true,
                      "is_hidden": true,
                      "is_required": true,
                      "order": 0,
                      "placeholder": "string",
                      "search_query": "string",
                      "tooltip": "string",
                      "use_shorthand_notation": true,
                      "view_name": "string"
                    }
                  ]
                }
              ],
              "create_view": {
                "is_hidden": true
              },
              "decimal_places": 0,
              "detail_view": {
                "is_hidden": true
              },
              "display_name": "string",
              "filter_view": {
                "is_hidden": true
              },
              "group_name": "string",
              "is_active_in_detail_view": true,
              "is_bulk_action_enabled": true,
              "is_currency_field": true,
              "is_groupable": true,
              "is_hidden": true,
              "is_hidden_during_create": true,
              "is_read_only": true,
              "is_required": true,
              "is_shown_in_summary": true,
              "is_sortable": true,
              "list_view": {
                "is_hidden": true
              },
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "summary_view": {
                "is_hidden": true
              },
              "tooltip": "string",
              "unit": "string",
              "use_shorthand_notation": true
            },
            "default_value": true
          }
        ],
        "name": "string"
      }
    ],
    "custom_fields": [
      {
        "field_type": "array",
        "description": "string",
        "is_derived": true,
        "is_filterable": true,
        "is_immutable": true,
        "is_pii": true,
        "is_required": true,
        "mfz": {},
        "name": "string",
        "oasis": {},
        "origin": "string",
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        },
        "default_value": true
      }
    ],
    "description": "string",
    "is_custom_leaf_type": true,
    "leaf_type": "string",
    "stage_diagram_id": {
      "display_id": "string",
      "id": "string",
      "name": "string",
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
    "stock_composite_schemas": [
      {
        "description": "string",
        "fields": [
          {
            "field_type": "array",
            "description": "string",
            "is_derived": true,
            "is_filterable": true,
            "is_immutable": true,
            "is_pii": true,
            "is_required": true,
            "mfz": {},
            "name": "string",
            "oasis": {},
            "origin": "string",
            "ui": {
              "card_view": {
                "is_visible": true
              },
              "client_overrides": [
                {
                  "client_name": "string",
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_overrides": [
                    {
                      "decimal_places": 0,
                      "display_name": "string",
                      "is_groupable": true,
                      "is_hidden": true,
                      "is_required": true,
                      "order": 0,
                      "placeholder": "string",
                      "search_query": "string",
                      "tooltip": "string",
                      "use_shorthand_notation": true,
                      "view_name": "string"
                    }
                  ]
                }
              ],
              "create_view": {
                "is_hidden": true
              },
              "decimal_places": 0,
              "detail_view": {
                "is_hidden": true
              },
              "display_name": "string",
              "filter_view": {
                "is_hidden": true
              },
              "group_name": "string",
              "is_active_in_detail_view": true,
              "is_bulk_action_enabled": true,
              "is_currency_field": true,
              "is_groupable": true,
              "is_hidden": true,
              "is_hidden_during_create": true,
              "is_read_only": true,
              "is_required": true,
              "is_shown_in_summary": true,
              "is_sortable": true,
              "list_view": {
                "is_hidden": true
              },
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "summary_view": {
                "is_hidden": true
              },
              "tooltip": "string",
              "unit": "string",
              "use_shorthand_notation": true
            },
            "default_value": true
          }
        ],
        "name": "string"
      }
    ],
    "stock_field_overrides": [
      {
        "is_required": true,
        "name": "string",
        "uenum_values": [
          {
            "id": 0,
            "is_deprecated": true,
            "label": "string",
            "ordinal": 0,
            "tooltip": "string"
          }
        ],
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        }
      }
    ],
    "stock_fields": [
      {
        "field_type": "array",
        "description": "string",
        "is_derived": true,
        "is_filterable": true,
        "is_immutable": true,
        "is_pii": true,
        "is_required": true,
        "mfz": {},
        "name": "string",
        "oasis": {},
        "origin": "string",
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        },
        "default_value": true
      }
    ],
    "subtype": "string",
    "subtype_display_name": "string",
    "title": "string"
  }
}
```

</details>


<a id="custom-schema-fragments-get"></a>

## `GET /schemas.custom.get`

**Get Schemas Custom**

Source: <https://developer.devrev.ai/api-reference/customization/custom-schema-fragments-get>

Gets a custom schema fragment.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the custom schema fragment.<br>*Format: id* |
| `include_sync_metadata` | no | `boolean` | Whether to include sync metadata in the response. |

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
curl -X GET "https://api.devrev.ai/schemas.custom.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "fragment": {
    "type": "app_fragment",
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
    "composite_schemas": [
      {
        "description": "string",
        "fields": [
          {
            "field_type": "array",
            "description": "string",
            "is_derived": true,
            "is_filterable": true,
            "is_immutable": true,
            "is_pii": true,
            "is_required": true,
            "mfz": {},
            "name": "string",
            "oasis": {},
            "origin": "string",
            "ui": {
              "card_view": {
                "is_visible": true
              },
              "client_overrides": [
                {
                  "client_name": "string",
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_overrides": [
                    {
                      "decimal_places": 0,
                      "display_name": "string",
                      "is_groupable": true,
                      "is_hidden": true,
                      "is_required": true,
                      "order": 0,
                      "placeholder": "string",
                      "search_query": "string",
                      "tooltip": "string",
                      "use_shorthand_notation": true,
                      "view_name": "string"
                    }
                  ]
                }
              ],
              "create_view": {
                "is_hidden": true
              },
              "decimal_places": 0,
              "detail_view": {
                "is_hidden": true
              },
              "display_name": "string",
              "filter_view": {
                "is_hidden": true
              },
              "group_name": "string",
              "is_active_in_detail_view": true,
              "is_bulk_action_enabled": true,
              "is_currency_field": true,
              "is_groupable": true,
              "is_hidden": true,
              "is_hidden_during_create": true,
              "is_read_only": true,
              "is_required": true,
              "is_shown_in_summary": true,
              "is_sortable": true,
              "list_view": {
                "is_hidden": true
              },
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "summary_view": {
                "is_hidden": true
              },
              "tooltip": "string",
              "unit": "string",
              "use_shorthand_notation": true
            },
            "default_value": true
          }
        ],
        "name": "string"
      }
    ],
    "conditions": [
      {
        "effects": [
          {
            "allowed_values": [
              "string"
            ],
            "fields": [
              "string"
            ],
            "immutable": true,
            "invalid": true,
            "require": true,
            "show": true
          }
        ],
        "expression": "string"
      }
    ],
    "deprecated": true,
    "description": "string",
    "fields": [
      {
        "field_type": "array",
        "description": "string",
        "is_derived": true,
        "is_filterable": true,
        "is_immutable": true,
        "is_pii": true,
        "is_required": true,
        "mfz": {},
        "name": "string",
        "oasis": {},
        "origin": "string",
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        },
        "default_value": true
      }
    ],
    "fragment_type": "app",
    "is_custom_leaf_type": true,
    "is_deprecated": true,
    "leaf_type": "string",
    "new_fragment_ref": {
      "type": "app_fragment",
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
    },
    "old_fragment_ref": {
      "type": "app_fragment",
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
    },
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
    "app": "string",
    "app_display_name": "string"
  }
}
```

</details>


<a id="custom-schema-fragments-get-post"></a>

## `POST /schemas.custom.get`

**Get Schemas Custom (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/custom-schema-fragments-get-post>

Gets a custom schema fragment.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the custom schema fragment.<br>*Format: id* |
| `include_sync_metadata` | no | `boolean` | Whether to include sync metadata in the response. |

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
curl -X POST "https://api.devrev.ai/schemas.custom.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "fragment": {
    "type": "app_fragment",
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
    "composite_schemas": [
      {
        "description": "string",
        "fields": [
          {
            "field_type": "array",
            "description": "string",
            "is_derived": true,
            "is_filterable": true,
            "is_immutable": true,
            "is_pii": true,
            "is_required": true,
            "mfz": {},
            "name": "string",
            "oasis": {},
            "origin": "string",
            "ui": {
              "card_view": {
                "is_visible": true
              },
              "client_overrides": [
                {
                  "client_name": "string",
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_overrides": [
                    {
                      "decimal_places": 0,
                      "display_name": "string",
                      "is_groupable": true,
                      "is_hidden": true,
                      "is_required": true,
                      "order": 0,
                      "placeholder": "string",
                      "search_query": "string",
                      "tooltip": "string",
                      "use_shorthand_notation": true,
                      "view_name": "string"
                    }
                  ]
                }
              ],
              "create_view": {
                "is_hidden": true
              },
              "decimal_places": 0,
              "detail_view": {
                "is_hidden": true
              },
              "display_name": "string",
              "filter_view": {
                "is_hidden": true
              },
              "group_name": "string",
              "is_active_in_detail_view": true,
              "is_bulk_action_enabled": true,
              "is_currency_field": true,
              "is_groupable": true,
              "is_hidden": true,
              "is_hidden_during_create": true,
              "is_read_only": true,
              "is_required": true,
              "is_shown_in_summary": true,
              "is_sortable": true,
              "list_view": {
                "is_hidden": true
              },
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "summary_view": {
                "is_hidden": true
              },
              "tooltip": "string",
              "unit": "string",
              "use_shorthand_notation": true
            },
            "default_value": true
          }
        ],
        "name": "string"
      }
    ],
    "conditions": [
      {
        "effects": [
          {
            "allowed_values": [
              "string"
            ],
            "fields": [
              "string"
            ],
            "immutable": true,
            "invalid": true,
            "require": true,
            "show": true
          }
        ],
        "expression": "string"
      }
    ],
    "deprecated": true,
    "description": "string",
    "fields": [
      {
        "field_type": "array",
        "description": "string",
        "is_derived": true,
        "is_filterable": true,
        "is_immutable": true,
        "is_pii": true,
        "is_required": true,
        "mfz": {},
        "name": "string",
        "oasis": {},
        "origin": "string",
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        },
        "default_value": true
      }
    ],
    "fragment_type": "app",
    "is_custom_leaf_type": true,
    "is_deprecated": true,
    "leaf_type": "string",
    "new_fragment_ref": {
      "type": "app_fragment",
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
    },
    "old_fragment_ref": {
      "type": "app_fragment",
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
    },
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
    "app": "string",
    "app_display_name": "string"
  }
}
```

</details>


<a id="custom-schema-fragments-list"></a>

## `GET /schemas.custom.list`

**List Schemas Custom**

Source: <https://developer.devrev.ai/api-reference/customization/custom-schema-fragments-list>

Lists custom schema fragments.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `app` | no | `array<string>` | The list of app names. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `deprecated` | no | `boolean` | **Deprecated.**<br>Whether only deprecated fragments should be filtered. |
| `include_sync_metadata` | no | `boolean` | Whether to include sync metadata in the response. |
| `is_custom_leaf_type` | no | `boolean` | Whether the leaf type corresponds to a custom object |
| `is_deprecated` | no | `boolean` | Whether the fragment has been deprecated. |
| `leaf_type` | no | `array<string>` | The list of leaf types. |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `prune` | no | `array<custom-schema-fragments-list-request-prune>` | List of fields which are not required in the payload and can be pruned away. |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |
| `space.ids` | no | `array<string>` | Filters for the provided space IDs. |
| `space.include_children` | no | `boolean` | Whether to include child spaces. |
| `space.include_global` | no | `boolean` | Whether to include objects not associated with any space. |
| `space.include_parents` | no | `boolean` | Whether to include parent spaces. |
| `space.op` | no | `string` | The filter operator to be applied on space.<br>*Value in: "any" \| "not_any" \| "not_null" \| "null"* |
| `subtype` | no | `array<string>` | The list of subtypes. |
| `types` | no | `array<custom-schema-fragment-type>` | Filters for custom schema fragment of the provided types. |

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
curl -X GET "https://api.devrev.ai/schemas.custom.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "result": [
    {
      "type": "app_fragment",
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
      "composite_schemas": [
        {
          "description": "string",
          "fields": [
            {
              "field_type": "array",
              "description": "string",
              "is_derived": true,
              "is_filterable": true,
              "is_immutable": true,
              "is_pii": true,
              "is_required": true,
              "mfz": {},
              "name": "string",
              "oasis": {},
              "origin": "string",
              "ui": {
                "card_view": {
                  "is_visible": true
                },
                "client_overrides": [
                  {
                    "client_name": "string",
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_overrides": [
                      {
                        "decimal_places": 0,
                        "display_name": "string",
                        "is_groupable": true,
                        "is_hidden": true,
                        "is_required": true,
                        "order": 0,
                        "placeholder": "string",
                        "search_query": "string",
                        "tooltip": "string",
                        "use_shorthand_notation": true,
                        "view_name": "string"
                      }
                    ]
                  }
                ],
                "create_view": {
                  "is_hidden": true
                },
                "decimal_places": 0,
                "detail_view": {
                  "is_hidden": true
                },
                "display_name": "string",
                "filter_view": {
                  "is_hidden": true
                },
                "group_name": "string",
                "is_active_in_detail_view": true,
                "is_bulk_action_enabled": true,
                "is_currency_field": true,
                "is_groupable": true,
                "is_hidden": true,
                "is_hidden_during_create": true,
                "is_read_only": true,
                "is_required": true,
                "is_shown_in_summary": true,
                "is_sortable": true,
                "list_view": {
                  "is_hidden": true
                },
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "summary_view": {
                  "is_hidden": true
                },
                "tooltip": "string",
                "unit": "string",
                "use_shorthand_notation": true
              },
              "default_value": true
            }
          ],
          "name": "string"
        }
      ],
      "conditions": [
        {
          "effects": [
            {
              "allowed_values": [
                "string"
              ],
              "fields": [
                "string"
              ],
              "immutable": true,
              "invalid": true,
              "require": true,
              "show": true
            }
          ],
          "expression": "string"
        }
      ],
      "deprecated": true,
      "description": "string",
      "fields": [
        {
          "field_type": "array",
          "description": "string",
          "is_derived": true,
          "is_filterable": true,
          "is_immutable": true,
          "is_pii": true,
          "is_required": true,
          "mfz": {},
          "name": "string",
          "oasis": {},
          "origin": "string",
          "ui": {
            "card_view": {
              "is_visible": true
            },
            "client_overrides": [
              {
                "client_name": "string",
                "decimal_places": 0,
                "display_name": "string",
                "is_groupable": true,
                "is_hidden": true,
                "is_required": true,
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "tooltip": "string",
                "use_shorthand_notation": true,
                "view_overrides": [
                  {
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_name": "string"
                  }
                ]
              }
            ],
            "create_view": {
              "is_hidden": true
            },
            "decimal_places": 0,
            "detail_view": {
              "is_hidden": true
            },
            "display_name": "string",
            "filter_view": {
              "is_hidden": true
            },
            "group_name": "string",
            "is_active_in_detail_view": true,
            "is_bulk_action_enabled": true,
            "is_currency_field": true,
            "is_groupable": true,
            "is_hidden": true,
            "is_hidden_during_create": true,
            "is_read_only": true,
            "is_required": true,
            "is_shown_in_summary": true,
            "is_sortable": true,
            "list_view": {
              "is_hidden": true
            },
            "order": 0,
            "placeholder": "string",
            "search_query": "string",
            "summary_view": {
              "is_hidden": true
            },
            "tooltip": "string",
            "unit": "string",
            "use_shorthand_notation": true
          },
          "default_value": true
        }
      ],
      "fragment_type": "app",
      "is_custom_leaf_type": true,
      "is_deprecated": true,
      "leaf_type": "string",
      "new_fragment_ref": {
        "type": "app_fragment",
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
      },
      "old_fragment_ref": {
        "type": "app_fragment",
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
      },
      "sync_metadata": {
        "external_record_id": "string",
        "external_record_type": "string",
        "external_reference": "string",
        "last_sync_in": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
        "last_sync_out": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
      "app": "string",
      "app_display_name": "string"
    }
  ]
}
```

</details>


<a id="custom-schema-fragments-list-post"></a>

## `POST /schemas.custom.list`

**List Schemas Custom (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/custom-schema-fragments-list-post>

Lists custom schema fragments.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `app` | no | `array<string>` | The list of app names. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `deprecated` | no | `boolean` | **Deprecated.**<br>Whether only deprecated fragments should be filtered. |
| `include_sync_metadata` | no | `boolean` | Whether to include sync metadata in the response. |
| `is_custom_leaf_type` | no | `boolean` | Whether the leaf type corresponds to a custom object |
| `is_deprecated` | no | `boolean` | Whether the fragment has been deprecated. |
| `leaf_type` | no | `array<string>` | The list of leaf types. |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `prune` | no | `array<custom-schema-fragments-list-request-prune>` | List of fields which are not required in the payload and can be pruned away. |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |
| `space` | no | `space-filter` |  |
| `subtype` | no | `array<string>` | The list of subtypes. |
| `types` | no | `array<custom-schema-fragment-type>` | Filters for custom schema fragment of the provided types. |

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
curl -X POST "https://api.devrev.ai/schemas.custom.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "result": [
    {
      "type": "app_fragment",
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
      "composite_schemas": [
        {
          "description": "string",
          "fields": [
            {
              "field_type": "array",
              "description": "string",
              "is_derived": true,
              "is_filterable": true,
              "is_immutable": true,
              "is_pii": true,
              "is_required": true,
              "mfz": {},
              "name": "string",
              "oasis": {},
              "origin": "string",
              "ui": {
                "card_view": {
                  "is_visible": true
                },
                "client_overrides": [
                  {
                    "client_name": "string",
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_overrides": [
                      {
                        "decimal_places": 0,
                        "display_name": "string",
                        "is_groupable": true,
                        "is_hidden": true,
                        "is_required": true,
                        "order": 0,
                        "placeholder": "string",
                        "search_query": "string",
                        "tooltip": "string",
                        "use_shorthand_notation": true,
                        "view_name": "string"
                      }
                    ]
                  }
                ],
                "create_view": {
                  "is_hidden": true
                },
                "decimal_places": 0,
                "detail_view": {
                  "is_hidden": true
                },
                "display_name": "string",
                "filter_view": {
                  "is_hidden": true
                },
                "group_name": "string",
                "is_active_in_detail_view": true,
                "is_bulk_action_enabled": true,
                "is_currency_field": true,
                "is_groupable": true,
                "is_hidden": true,
                "is_hidden_during_create": true,
                "is_read_only": true,
                "is_required": true,
                "is_shown_in_summary": true,
                "is_sortable": true,
                "list_view": {
                  "is_hidden": true
                },
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "summary_view": {
                  "is_hidden": true
                },
                "tooltip": "string",
                "unit": "string",
                "use_shorthand_notation": true
              },
              "default_value": true
            }
          ],
          "name": "string"
        }
      ],
      "conditions": [
        {
          "effects": [
            {
              "allowed_values": [
                "string"
              ],
              "fields": [
                "string"
              ],
              "immutable": true,
              "invalid": true,
              "require": true,
              "show": true
            }
          ],
          "expression": "string"
        }
      ],
      "deprecated": true,
      "description": "string",
      "fields": [
        {
          "field_type": "array",
          "description": "string",
          "is_derived": true,
          "is_filterable": true,
          "is_immutable": true,
          "is_pii": true,
          "is_required": true,
          "mfz": {},
          "name": "string",
          "oasis": {},
          "origin": "string",
          "ui": {
            "card_view": {
              "is_visible": true
            },
            "client_overrides": [
              {
                "client_name": "string",
                "decimal_places": 0,
                "display_name": "string",
                "is_groupable": true,
                "is_hidden": true,
                "is_required": true,
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "tooltip": "string",
                "use_shorthand_notation": true,
                "view_overrides": [
                  {
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_name": "string"
                  }
                ]
              }
            ],
            "create_view": {
              "is_hidden": true
            },
            "decimal_places": 0,
            "detail_view": {
              "is_hidden": true
            },
            "display_name": "string",
            "filter_view": {
              "is_hidden": true
            },
            "group_name": "string",
            "is_active_in_detail_view": true,
            "is_bulk_action_enabled": true,
            "is_currency_field": true,
            "is_groupable": true,
            "is_hidden": true,
            "is_hidden_during_create": true,
            "is_read_only": true,
            "is_required": true,
            "is_shown_in_summary": true,
            "is_sortable": true,
            "list_view": {
              "is_hidden": true
            },
            "order": 0,
            "placeholder": "string",
            "search_query": "string",
            "summary_view": {
              "is_hidden": true
            },
            "tooltip": "string",
            "unit": "string",
            "use_shorthand_notation": true
          },
          "default_value": true
        }
      ],
      "fragment_type": "app",
      "is_custom_leaf_type": true,
      "is_deprecated": true,
      "leaf_type": "string",
      "new_fragment_ref": {
        "type": "app_fragment",
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
      },
      "old_fragment_ref": {
        "type": "app_fragment",
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
      },
      "sync_metadata": {
        "external_record_id": "string",
        "external_record_type": "string",
        "external_reference": "string",
        "last_sync_in": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
        "last_sync_out": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
      "app": "string",
      "app_display_name": "string"
    }
  ]
}
```

</details>


<a id="custom-schema-fragments-set"></a>

## `POST /schemas.custom.set`

**Set Schemas Custom**

Source: <https://developer.devrev.ai/api-reference/customization/custom-schema-fragments-set>

Creates or updates a custom schema fragment.

**Required scopes:**

- `custom_type_fragment:write`

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `custom-schema-fragments-set-request-app-fragment`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `string` | *Value in: "app_fragment" \| "custom_type_fragment" \| "tenant_fragment"* |
| `composite_schemas` | no | `array<custom-schema-fragments-set-request-composite-schema>` | List of all composite schemas used in this fragment. |
| `conditions` | no | `array<custom-schema-fragment-condition>` | List of conditions for this fragment. |
| `deleted_fields` | no | `array<string>` | List of field names which are being dropped. |
| `deprecated` | no | `boolean` | **Deprecated.**<br>Whether this fragment has been deprecated. |
| `description` | no | `string` | The description of the custom schema fragment.<br>*Format: text* |
| `fields` | no | `array<schema-field-descriptor>` | List of all fields in this fragment. |
| `is_custom_leaf_type` | no | `boolean` | Whether the leaf type corresponds to a custom object |
| `is_deprecated` | no | `boolean` | Whether this fragment has been deprecated. |
| `leaf_type` | no | `string` | The leaf type this fragment applies to.<br>*Format: text* |
| `app` | yes | `string` | The app this fragment applies to.<br>*Format: text* |
| `app_display_name` | no | `string` | The display name of the app.<br>*Format: text* |

#### Variant `custom-schema-fragments-set-request-custom-type-fragment`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `custom-schema-fragments-set-request-tenant-fragment`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

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
curl -X POST "https://api.devrev.ai/schemas.custom.set" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "app_fragment",
    "description": "string",
    "leaf_type": "string",
    "app": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "id": "string"
}
```

</details>


<a id="stock-schema-fragments-get"></a>

## `GET /schemas.stock.get`

**Get Schemas Stock**

Source: <https://developer.devrev.ai/api-reference/customization/stock-schema-fragments-get>

Gets a stock schema fragment.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | no | `string` | The ID of the stock schema fragment.<br>*Format: id* |
| `leaf_type` | no | `string` | The leaf type this fragment applies to.<br>*Format: text* |

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
curl -X GET "https://api.devrev.ai/schemas.stock.get"
```

<details><summary>Example 200 response</summary>

```json
{
  "fragment": {
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
    "composite_schemas": [
      {
        "description": "string",
        "fields": [
          {
            "field_type": "array",
            "description": "string",
            "is_derived": true,
            "is_filterable": true,
            "is_immutable": true,
            "is_pii": true,
            "is_required": true,
            "mfz": {},
            "name": "string",
            "oasis": {},
            "origin": "string",
            "ui": {
              "card_view": {
                "is_visible": true
              },
              "client_overrides": [
                {
                  "client_name": "string",
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_overrides": [
                    {
                      "decimal_places": 0,
                      "display_name": "string",
                      "is_groupable": true,
                      "is_hidden": true,
                      "is_required": true,
                      "order": 0,
                      "placeholder": "string",
                      "search_query": "string",
                      "tooltip": "string",
                      "use_shorthand_notation": true,
                      "view_name": "string"
                    }
                  ]
                }
              ],
              "create_view": {
                "is_hidden": true
              },
              "decimal_places": 0,
              "detail_view": {
                "is_hidden": true
              },
              "display_name": "string",
              "filter_view": {
                "is_hidden": true
              },
              "group_name": "string",
              "is_active_in_detail_view": true,
              "is_bulk_action_enabled": true,
              "is_currency_field": true,
              "is_groupable": true,
              "is_hidden": true,
              "is_hidden_during_create": true,
              "is_read_only": true,
              "is_required": true,
              "is_shown_in_summary": true,
              "is_sortable": true,
              "list_view": {
                "is_hidden": true
              },
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "summary_view": {
                "is_hidden": true
              },
              "tooltip": "string",
              "unit": "string",
              "use_shorthand_notation": true
            },
            "default_value": true
          }
        ],
        "name": "string"
      }
    ],
    "description": "string",
    "fields": [
      {
        "field_type": "array",
        "description": "string",
        "is_derived": true,
        "is_filterable": true,
        "is_immutable": true,
        "is_pii": true,
        "is_required": true,
        "mfz": {},
        "name": "string",
        "oasis": {},
        "origin": "string",
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        },
        "default_value": true
      }
    ],
    "leaf_type": "string",
    "new_fragment_ref": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "old_fragment_ref": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "title": "string"
  }
}
```

</details>


<a id="stock-schema-fragments-get-post"></a>

## `POST /schemas.stock.get`

**Get Schemas Stock (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/stock-schema-fragments-get-post>

Gets a stock schema fragment.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | no | `string` | The ID of the stock schema fragment.<br>*Format: id* |
| `leaf_type` | no | `string` | The leaf type this fragment applies to.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/schemas.stock.get" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "fragment": {
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
    "composite_schemas": [
      {
        "description": "string",
        "fields": [
          {
            "field_type": "array",
            "description": "string",
            "is_derived": true,
            "is_filterable": true,
            "is_immutable": true,
            "is_pii": true,
            "is_required": true,
            "mfz": {},
            "name": "string",
            "oasis": {},
            "origin": "string",
            "ui": {
              "card_view": {
                "is_visible": true
              },
              "client_overrides": [
                {
                  "client_name": "string",
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_overrides": [
                    {
                      "decimal_places": 0,
                      "display_name": "string",
                      "is_groupable": true,
                      "is_hidden": true,
                      "is_required": true,
                      "order": 0,
                      "placeholder": "string",
                      "search_query": "string",
                      "tooltip": "string",
                      "use_shorthand_notation": true,
                      "view_name": "string"
                    }
                  ]
                }
              ],
              "create_view": {
                "is_hidden": true
              },
              "decimal_places": 0,
              "detail_view": {
                "is_hidden": true
              },
              "display_name": "string",
              "filter_view": {
                "is_hidden": true
              },
              "group_name": "string",
              "is_active_in_detail_view": true,
              "is_bulk_action_enabled": true,
              "is_currency_field": true,
              "is_groupable": true,
              "is_hidden": true,
              "is_hidden_during_create": true,
              "is_read_only": true,
              "is_required": true,
              "is_shown_in_summary": true,
              "is_sortable": true,
              "list_view": {
                "is_hidden": true
              },
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "summary_view": {
                "is_hidden": true
              },
              "tooltip": "string",
              "unit": "string",
              "use_shorthand_notation": true
            },
            "default_value": true
          }
        ],
        "name": "string"
      }
    ],
    "description": "string",
    "fields": [
      {
        "field_type": "array",
        "description": "string",
        "is_derived": true,
        "is_filterable": true,
        "is_immutable": true,
        "is_pii": true,
        "is_required": true,
        "mfz": {},
        "name": "string",
        "oasis": {},
        "origin": "string",
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        },
        "default_value": true
      }
    ],
    "leaf_type": "string",
    "new_fragment_ref": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "old_fragment_ref": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "title": "string"
  }
}
```

</details>


<a id="stock-schema-fragments-list"></a>

## `GET /schemas.stock.list`

**List Schemas Stock**

Source: <https://developer.devrev.ai/api-reference/customization/stock-schema-fragments-list>

Lists stock schema fragments.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `filter_preset` | no | `string` | Filter preset to specify whether to filter only customization enabled leaf types.<br>*Value in: "customizable_types_preset" \| "no_preset"* |
| `leaf_type` | no | `array<string>` | The list of leaf types. |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `prune` | no | `array<stock-schema-fragments-list-request-prune>` | List of fields which are not required in the payload and can be pruned away. |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |

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
curl -X GET "https://api.devrev.ai/schemas.stock.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "result": [
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
      "composite_schemas": [
        {
          "description": "string",
          "fields": [
            {
              "field_type": "array",
              "description": "string",
              "is_derived": true,
              "is_filterable": true,
              "is_immutable": true,
              "is_pii": true,
              "is_required": true,
              "mfz": {},
              "name": "string",
              "oasis": {},
              "origin": "string",
              "ui": {
                "card_view": {
                  "is_visible": true
                },
                "client_overrides": [
                  {
                    "client_name": "string",
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_overrides": [
                      {
                        "decimal_places": 0,
                        "display_name": "string",
                        "is_groupable": true,
                        "is_hidden": true,
                        "is_required": true,
                        "order": 0,
                        "placeholder": "string",
                        "search_query": "string",
                        "tooltip": "string",
                        "use_shorthand_notation": true,
                        "view_name": "string"
                      }
                    ]
                  }
                ],
                "create_view": {
                  "is_hidden": true
                },
                "decimal_places": 0,
                "detail_view": {
                  "is_hidden": true
                },
                "display_name": "string",
                "filter_view": {
                  "is_hidden": true
                },
                "group_name": "string",
                "is_active_in_detail_view": true,
                "is_bulk_action_enabled": true,
                "is_currency_field": true,
                "is_groupable": true,
                "is_hidden": true,
                "is_hidden_during_create": true,
                "is_read_only": true,
                "is_required": true,
                "is_shown_in_summary": true,
                "is_sortable": true,
                "list_view": {
                  "is_hidden": true
                },
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "summary_view": {
                  "is_hidden": true
                },
                "tooltip": "string",
                "unit": "string",
                "use_shorthand_notation": true
              },
              "default_value": true
            }
          ],
          "name": "string"
        }
      ],
      "description": "string",
      "fields": [
        {
          "field_type": "array",
          "description": "string",
          "is_derived": true,
          "is_filterable": true,
          "is_immutable": true,
          "is_pii": true,
          "is_required": true,
          "mfz": {},
          "name": "string",
          "oasis": {},
          "origin": "string",
          "ui": {
            "card_view": {
              "is_visible": true
            },
            "client_overrides": [
              {
                "client_name": "string",
                "decimal_places": 0,
                "display_name": "string",
                "is_groupable": true,
                "is_hidden": true,
                "is_required": true,
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "tooltip": "string",
                "use_shorthand_notation": true,
                "view_overrides": [
                  {
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_name": "string"
                  }
                ]
              }
            ],
            "create_view": {
              "is_hidden": true
            },
            "decimal_places": 0,
            "detail_view": {
              "is_hidden": true
            },
            "display_name": "string",
            "filter_view": {
              "is_hidden": true
            },
            "group_name": "string",
            "is_active_in_detail_view": true,
            "is_bulk_action_enabled": true,
            "is_currency_field": true,
            "is_groupable": true,
            "is_hidden": true,
            "is_hidden_during_create": true,
            "is_read_only": true,
            "is_required": true,
            "is_shown_in_summary": true,
            "is_sortable": true,
            "list_view": {
              "is_hidden": true
            },
            "order": 0,
            "placeholder": "string",
            "search_query": "string",
            "summary_view": {
              "is_hidden": true
            },
            "tooltip": "string",
            "unit": "string",
            "use_shorthand_notation": true
          },
          "default_value": true
        }
      ],
      "leaf_type": "string",
      "new_fragment_ref": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "old_fragment_ref": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "title": "string"
    }
  ]
}
```

</details>


<a id="stock-schema-fragments-list-post"></a>

## `POST /schemas.stock.list`

**List Schemas Stock (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/stock-schema-fragments-list-post>

Lists stock schema fragments.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `filter_preset` | no | `string` | *Value in: "customizable_types_preset" \| "no_preset"* |
| `leaf_type` | no | `array<string>` | The list of leaf types. |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `prune` | no | `array<stock-schema-fragments-list-request-prune>` | List of fields which are not required in the payload and can be pruned away. |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |

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
curl -X POST "https://api.devrev.ai/schemas.stock.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "result": [
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
      "composite_schemas": [
        {
          "description": "string",
          "fields": [
            {
              "field_type": "array",
              "description": "string",
              "is_derived": true,
              "is_filterable": true,
              "is_immutable": true,
              "is_pii": true,
              "is_required": true,
              "mfz": {},
              "name": "string",
              "oasis": {},
              "origin": "string",
              "ui": {
                "card_view": {
                  "is_visible": true
                },
                "client_overrides": [
                  {
                    "client_name": "string",
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_overrides": [
                      {
                        "decimal_places": 0,
                        "display_name": "string",
                        "is_groupable": true,
                        "is_hidden": true,
                        "is_required": true,
                        "order": 0,
                        "placeholder": "string",
                        "search_query": "string",
                        "tooltip": "string",
                        "use_shorthand_notation": true,
                        "view_name": "string"
                      }
                    ]
                  }
                ],
                "create_view": {
                  "is_hidden": true
                },
                "decimal_places": 0,
                "detail_view": {
                  "is_hidden": true
                },
                "display_name": "string",
                "filter_view": {
                  "is_hidden": true
                },
                "group_name": "string",
                "is_active_in_detail_view": true,
                "is_bulk_action_enabled": true,
                "is_currency_field": true,
                "is_groupable": true,
                "is_hidden": true,
                "is_hidden_during_create": true,
                "is_read_only": true,
                "is_required": true,
                "is_shown_in_summary": true,
                "is_sortable": true,
                "list_view": {
                  "is_hidden": true
                },
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "summary_view": {
                  "is_hidden": true
                },
                "tooltip": "string",
                "unit": "string",
                "use_shorthand_notation": true
              },
              "default_value": true
            }
          ],
          "name": "string"
        }
      ],
      "description": "string",
      "fields": [
        {
          "field_type": "array",
          "description": "string",
          "is_derived": true,
          "is_filterable": true,
          "is_immutable": true,
          "is_pii": true,
          "is_required": true,
          "mfz": {},
          "name": "string",
          "oasis": {},
          "origin": "string",
          "ui": {
            "card_view": {
              "is_visible": true
            },
            "client_overrides": [
              {
                "client_name": "string",
                "decimal_places": 0,
                "display_name": "string",
                "is_groupable": true,
                "is_hidden": true,
                "is_required": true,
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "tooltip": "string",
                "use_shorthand_notation": true,
                "view_overrides": [
                  {
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_name": "string"
                  }
                ]
              }
            ],
            "create_view": {
              "is_hidden": true
            },
            "decimal_places": 0,
            "detail_view": {
              "is_hidden": true
            },
            "display_name": "string",
            "filter_view": {
              "is_hidden": true
            },
            "group_name": "string",
            "is_active_in_detail_view": true,
            "is_bulk_action_enabled": true,
            "is_currency_field": true,
            "is_groupable": true,
            "is_hidden": true,
            "is_hidden_during_create": true,
            "is_read_only": true,
            "is_required": true,
            "is_shown_in_summary": true,
            "is_sortable": true,
            "list_view": {
              "is_hidden": true
            },
            "order": 0,
            "placeholder": "string",
            "search_query": "string",
            "summary_view": {
              "is_hidden": true
            },
            "tooltip": "string",
            "unit": "string",
            "use_shorthand_notation": true
          },
          "default_value": true
        }
      ],
      "leaf_type": "string",
      "new_fragment_ref": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "old_fragment_ref": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "title": "string"
    }
  ]
}
```

</details>


<a id="schemas-subtype-prepare-update-get"></a>

## `POST /schemas.subtypes.prepare-update`

**Prepare-Update Schemas Subtypes**

Source: <https://developer.devrev.ai/api-reference/customization/schemas-subtype-prepare-update-get>

Gets the new fragment IDs and fields resulting from changing a subtype.

**Required scopes:**

- `custom_type_fragment:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `is_custom_leaf_type` | no | `boolean` | Whether the leaf type corresponds to a custom object. |
| `leaf_type` | yes | `string` | Leaf type of the object.<br>*Format: text* |
| `new_subtype` | no | `string` | Name of the new subtype for the object.<br>*Format: text* |
| `object` | no | `string` | ID of the object of which subtype is to be changed. Used to fetch the object's custom schema fragments and custom fields<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/schemas.subtypes.prepare-update" \
  -H "Content-Type: application/json" \
  -d '{
    "leaf_type": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "added_fields": [
    {
      "default_value": null,
      "name": "string"
    }
  ],
  "dropped_fields": [
    {
      "conflict_type": "absent_in_new",
      "message": "string",
      "name": "string"
    }
  ],
  "new_custom_schema_fragments": [
    "string"
  ],
  "new_start_stage": "string"
}
```

</details>


<a id="stage-diagrams-create"></a>

## `POST /stage-diagrams.create`

**Create Stage Diagram**

Source: <https://developer.devrev.ai/api-reference/customization/stage-diagrams-create>

Creates a stage diagram.

**Required scopes:**

- `stage_diagram:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `is_custom_leaf_type` | no | `boolean` | Whether the leaf type corresponds to a custom object. |
| `is_default` | no | `boolean` | Whether this is a default stage diagram. |
| `leaf_type` | yes | `string` | The leaf type this stage diagram applies to.<br>*Format: text* |
| `name` | yes | `string` | The name of the stage diagram. Stage diagram is used for defining stage transitions.<br>*Format: text* |
| `stages` | yes | `array<create-stage-node>` | List of stages in the diagram. |

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
curl -X POST "https://api.devrev.ai/stage-diagrams.create" \
  -H "Content-Type: application/json" \
  -d '{
    "leaf_type": "string",
    "name": "string",
    "stages": [
      {
        "stage_id": "string"
      }
    ]
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "stage_diagram": {
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
    "is_custom_leaf_type": true,
    "is_default": true,
    "leaf_type": "string",
    "name": "string",
    "stages": [
      {
        "is_deprecated": true,
        "is_start": true,
        "stage": {
          "display_id": "string",
          "id": "string",
          "name": "string",
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
        "transitions": [
          {
            "target_stage": {
              "display_id": "string",
              "id": "string",
              "name": "string",
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
        ]
      }
    ],
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
```

</details>


<a id="stage-diagrams-get"></a>

## `GET /stage-diagrams.get`

**Get Stage Diagram**

Source: <https://developer.devrev.ai/api-reference/customization/stage-diagrams-get>

Gets a stage diagram.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | no | `string` | The ID of the stage diagram to get.<br>*Format: id* |
| `is_custom_leaf_type` | no | `boolean` | Whether the leaf type corresponds to a custom object. Specify this along with leaf_type to get the default custom object stage diagram. |
| `leaf_type` | no | `string` | The leaf type. Should be specified to retrieve the default stage diagram for the leaf type. If not provided, then id is used.<br>*Format: text* |

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
curl -X GET "https://api.devrev.ai/stage-diagrams.get"
```

<details><summary>Example 200 response</summary>

```json
{
  "stage_diagram": {
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
    "is_custom_leaf_type": true,
    "is_default": true,
    "leaf_type": "string",
    "name": "string",
    "stages": [
      {
        "is_deprecated": true,
        "is_start": true,
        "stage": {
          "display_id": "string",
          "id": "string",
          "name": "string",
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
        "transitions": [
          {
            "target_stage": {
              "display_id": "string",
              "id": "string",
              "name": "string",
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
        ]
      }
    ],
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
```

</details>


<a id="stage-diagrams-get-post"></a>

## `POST /stage-diagrams.get`

**Get Stage Diagram (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/stage-diagrams-get-post>

Gets a stage diagram.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | no | `string` | The ID of the stage diagram to get.<br>*Format: id* |
| `is_custom_leaf_type` | no | `boolean` | Whether the leaf type corresponds to a custom object. Specify this along with leaf_type to get the default custom object stage diagram. |
| `leaf_type` | no | `string` | The leaf type. Should be specified to retrieve the default stage diagram for the leaf type. If not provided, then id is used.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/stage-diagrams.get" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "stage_diagram": {
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
    "is_custom_leaf_type": true,
    "is_default": true,
    "leaf_type": "string",
    "name": "string",
    "stages": [
      {
        "is_deprecated": true,
        "is_start": true,
        "stage": {
          "display_id": "string",
          "id": "string",
          "name": "string",
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
        "transitions": [
          {
            "target_stage": {
              "display_id": "string",
              "id": "string",
              "name": "string",
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
        ]
      }
    ],
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
```

</details>


<a id="stage-diagrams-list"></a>

## `GET /stage-diagrams.list`

**List Stage Diagrams**

Source: <https://developer.devrev.ai/api-reference/customization/stage-diagrams-list>

Lists stage diagrams.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from, otherwise if not provided, then iteration starts from the beginning.<br>*Format: text* |
| `is_custom_leaf_type` | no | `boolean` | Whether only custom object stage diagrams should be filtered. |
| `leaf_type` | no | `array<string>` | The list of leaf types. |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `name` | no | `array<string>` | The list of stage diagram names. |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |

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
curl -X GET "https://api.devrev.ai/stage-diagrams.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "cursor": "string",
  "result": [
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
      "is_custom_leaf_type": true,
      "is_default": true,
      "leaf_type": "string",
      "name": "string",
      "stages": [
        {
          "is_deprecated": true,
          "is_start": true,
          "stage": {
            "display_id": "string",
            "id": "string",
            "name": "string",
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
          "transitions": [
            {
              "target_stage": {
                "display_id": "string",
                "id": "string",
                "name": "string",
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
          ]
        }
      ],
      "sync_metadata": {
        "external_record_id": "string",
        "external_record_type": "string",
        "external_reference": "string",
        "last_sync_in": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
        "last_sync_out": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
  ]
}
```

</details>


<a id="stage-diagrams-list-post"></a>

## `POST /stage-diagrams.list`

**List Stage Diagrams (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/stage-diagrams-list-post>

Lists stage diagrams.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from, otherwise if not provided, then iteration starts from the beginning.<br>*Format: text* |
| `is_custom_leaf_type` | no | `boolean` | Whether only custom object stage diagrams should be filtered. |
| `leaf_type` | no | `array<string>` | The list of leaf types. |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `name` | no | `array<string>` | The list of stage diagram names. |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |

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
curl -X POST "https://api.devrev.ai/stage-diagrams.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "cursor": "string",
  "result": [
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
      "is_custom_leaf_type": true,
      "is_default": true,
      "leaf_type": "string",
      "name": "string",
      "stages": [
        {
          "is_deprecated": true,
          "is_start": true,
          "stage": {
            "display_id": "string",
            "id": "string",
            "name": "string",
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
          "transitions": [
            {
              "target_stage": {
                "display_id": "string",
                "id": "string",
                "name": "string",
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
          ]
        }
      ],
      "sync_metadata": {
        "external_record_id": "string",
        "external_record_type": "string",
        "external_reference": "string",
        "last_sync_in": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
        "last_sync_out": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
  ]
}
```

</details>


<a id="stage-diagrams-update"></a>

## `POST /stage-diagrams.update`

**Update Stage Diagram**

Source: <https://developer.devrev.ai/api-reference/customization/stage-diagrams-update>

Updates a stage diagram.

**Required scopes:**

- `stage_diagram:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the stage diagram to update.<br>*Format: id* |
| `name` | no | `string` | The updated name of the stage diagram.<br>*Format: text* |
| `stages` | no | `array<update-stage-node>` | List of stages in the stage diagram. |

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
curl -X POST "https://api.devrev.ai/stage-diagrams.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "stage_diagram": {
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
    "is_custom_leaf_type": true,
    "is_default": true,
    "leaf_type": "string",
    "name": "string",
    "stages": [
      {
        "is_deprecated": true,
        "is_start": true,
        "stage": {
          "display_id": "string",
          "id": "string",
          "name": "string",
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
        "transitions": [
          {
            "target_stage": {
              "display_id": "string",
              "id": "string",
              "name": "string",
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
        ]
      }
    ],
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
```

</details>


<a id="custom-stages-create"></a>

## `POST /stages.custom.create`

**Create Stages Custom**

Source: <https://developer.devrev.ai/api-reference/customization/custom-stages-create>

Creates a custom stage.

**Required scopes:**

- `custom_stage:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `marketplace_ref` | no | `string` | A reference to the marketplace item from which this stage was imported.<br>*Format: id* |
| `name` | yes | `string` | The name of the custom stage.<br>*Format: text* |
| `ordinal` | yes | `integer` | The ordinal of the custom stage used for ordering.<br>*Format: int32* |
| `state` | yes | `string` | The state ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/stages.custom.create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "string",
    "ordinal": 0,
    "state": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "custom_stage": {
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
    "name": "string",
    "ordinal": 0,
    "state": {
      "display_id": "string",
      "id": "string",
      "is_final": true,
      "name": "string",
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
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
```

</details>


<a id="custom-stages-get"></a>

## `GET /stages.custom.get`

**Get Stages Custom**

Source: <https://developer.devrev.ai/api-reference/customization/custom-stages-get>

Gets a custom stage.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the custom stage to get.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/stages.custom.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "custom_stage": {
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
    "name": "string",
    "ordinal": 0,
    "state": {
      "display_id": "string",
      "id": "string",
      "is_final": true,
      "name": "string",
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
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
```

</details>


<a id="custom-stages-get-post"></a>

## `POST /stages.custom.get`

**Get Stages Custom (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/custom-stages-get-post>

Gets a custom stage.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the custom stage to get.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/stages.custom.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "custom_stage": {
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
    "name": "string",
    "ordinal": 0,
    "state": {
      "display_id": "string",
      "id": "string",
      "is_final": true,
      "name": "string",
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
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
```

</details>


<a id="custom-stages-list"></a>

## `GET /stages.custom.list`

**List Stages Custom**

Source: <https://developer.devrev.ai/api-reference/customization/custom-stages-list>

Lists custom stages.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from, otherwise if not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `name` | no | `array<string>` | The list of stage names. |
| `ordinal` | no | `array<integer>` | The list of stage ordinals. |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |

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
curl -X GET "https://api.devrev.ai/stages.custom.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "cursor": "string",
  "result": [
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
      "name": "string",
      "ordinal": 0,
      "state": {
        "display_id": "string",
        "id": "string",
        "is_final": true,
        "name": "string",
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
      "sync_metadata": {
        "external_record_id": "string",
        "external_record_type": "string",
        "external_reference": "string",
        "last_sync_in": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
        "last_sync_out": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
  ]
}
```

</details>


<a id="custom-stages-list-post"></a>

## `POST /stages.custom.list`

**List Stages Custom (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/custom-stages-list-post>

Lists custom stages.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from, otherwise if not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `name` | no | `array<string>` | The list of stage names. |
| `ordinal` | no | `array<integer>` | The list of stage ordinals. |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |

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
curl -X POST "https://api.devrev.ai/stages.custom.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "cursor": "string",
  "result": [
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
      "name": "string",
      "ordinal": 0,
      "state": {
        "display_id": "string",
        "id": "string",
        "is_final": true,
        "name": "string",
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
      "sync_metadata": {
        "external_record_id": "string",
        "external_record_type": "string",
        "external_reference": "string",
        "last_sync_in": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
        "last_sync_out": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
  ]
}
```

</details>


<a id="custom-stages-update"></a>

## `POST /stages.custom.update`

**Update Stages Custom**

Source: <https://developer.devrev.ai/api-reference/customization/custom-stages-update>

Updates a custom stage.

**Required scopes:**

- `custom_stage:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the custom stage to update.<br>*Format: id* |
| `name` | no | `string` | The updated name of the custom stage.<br>*Format: text* |
| `ordinal` | no | `integer` | The ordinal of the custom stage.<br>*Format: int32* |
| `state_id` | no | `string` | The state ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/stages.custom.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "custom_stage": {
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
    "name": "string",
    "ordinal": 0,
    "state": {
      "display_id": "string",
      "id": "string",
      "is_final": true,
      "name": "string",
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
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
```

</details>


<a id="custom-states-create"></a>

## `POST /states.custom.create`

**Create States Custom**

Source: <https://developer.devrev.ai/api-reference/customization/custom-states-create>

Creates a custom state.

**Required scopes:**

- `custom_state:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `is_final` | no | `boolean` | Whether this is a final state. |
| `name` | yes | `string` | The name of the custom state.<br>*Format: text* |
| `ordinal` | yes | `integer` | Ordinal of the custom state used to identify system states.<br>*Format: int32* |

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
curl -X POST "https://api.devrev.ai/states.custom.create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "string",
    "ordinal": 0
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "custom_state": {
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
    "is_final": true,
    "name": "string",
    "ordinal": 0,
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
```

</details>


<a id="custom-states-get"></a>

## `GET /states.custom.get`

**Get States Custom**

Source: <https://developer.devrev.ai/api-reference/customization/custom-states-get>

Gets a custom state.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the custom state to get.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/states.custom.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "custom_state": {
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
    "is_final": true,
    "name": "string",
    "ordinal": 0,
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
```

</details>


<a id="custom-states-get-post"></a>

## `POST /states.custom.get`

**Get States Custom (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/custom-states-get-post>

Gets a custom state.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the custom state to get.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/states.custom.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "custom_state": {
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
    "is_final": true,
    "name": "string",
    "ordinal": 0,
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
```

</details>


<a id="custom-states-list"></a>

## `GET /states.custom.list`

**List States Custom**

Source: <https://developer.devrev.ai/api-reference/customization/custom-states-list>

Lists custom states.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from, otherwise if not provided, then iteration starts from the beginning.<br>*Format: text* |
| `is_final` | no | `boolean` | Whether only final states should be filtered. |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `name` | no | `array<string>` | The list of state names. |
| `ordinal` | no | `array<integer>` | The list of state ordinals. |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |

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
curl -X GET "https://api.devrev.ai/states.custom.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "cursor": "string",
  "result": [
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
      "is_final": true,
      "name": "string",
      "ordinal": 0,
      "sync_metadata": {
        "external_record_id": "string",
        "external_record_type": "string",
        "external_reference": "string",
        "last_sync_in": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
        "last_sync_out": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
  ]
}
```

</details>


<a id="custom-states-list-post"></a>

## `POST /states.custom.list`

**List States Custom (POST)**

Source: <https://developer.devrev.ai/api-reference/customization/custom-states-list-post>

Lists custom states.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from, otherwise if not provided, then iteration starts from the beginning.<br>*Format: text* |
| `is_final` | no | `boolean` | Whether only final states should be filtered. |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `name` | no | `array<string>` | The list of state names. |
| `ordinal` | no | `array<integer>` | The list of state ordinals. |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |

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
curl -X POST "https://api.devrev.ai/states.custom.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "cursor": "string",
  "result": [
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
      "is_final": true,
      "name": "string",
      "ordinal": 0,
      "sync_metadata": {
        "external_record_id": "string",
        "external_record_type": "string",
        "external_reference": "string",
        "last_sync_in": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
        "last_sync_out": {
          "status": "failed",
          "sync_date": "2023-01-01T12:00:00.000Z",
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
  ]
}
```

</details>


<a id="custom-states-update"></a>

## `POST /states.custom.update`

**Update States Custom**

Source: <https://developer.devrev.ai/api-reference/customization/custom-states-update>

Updates a custom state.

**Required scopes:**

- `custom_state:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the custom state to update.<br>*Format: id* |
| `is_final` | no | `boolean` | Whether this is a final state. |
| `name` | no | `string` | The name of the custom state.<br>*Format: text* |
| `ordinal` | no | `integer` | Ordinal of the custom state used to identify system states.<br>*Format: int32* |

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
curl -X POST "https://api.devrev.ai/states.custom.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "custom_state": {
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
    "is_final": true,
    "name": "string",
    "ordinal": 0,
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
```

</details>
