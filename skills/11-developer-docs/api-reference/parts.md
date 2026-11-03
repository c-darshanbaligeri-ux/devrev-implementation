# Parts

Source: <https://developer.devrev.ai/api-reference/parts>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/parts.create` | [create](#create) |
| POST | `/parts.delete` | [delete](#delete) |
| GET | `/parts.get` | [get](#get) |
| POST | `/parts.get` | [get-post](#get-post) |
| GET | `/parts.list` | [list](#list) |
| POST | `/parts.list` | [list-post](#list-post) |
| POST | `/parts.update` | [update](#update) |

<a id="create"></a>

## `POST /parts.create`

**Create Part**

Source: <https://developer.devrev.ai/api-reference/parts/create>

Creates new [part](https://devrev.ai/docs/product/parts).

**Required scopes:** Depends on the object type in the `type` field:

| type | required scope |
| --- | --- |
| capability | `capability:write` OR `capability:all` |
| enhancement | `enhancement:write` OR `enhancement:all` |
| feature | `feature:write` OR `feature:all` |
| product | `product:write` OR `product:all` |

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `parts-create-request-capability`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `string` | *Value in: "capability" \| "enhancement" \| "feature" \| "linkable" \| "product" \| "runnable"* |
| `artifacts` | no | `array<string>` | The IDs of the artifacts. |
| `custom_fields` | no | `object` | Custom fields. |
| `custom_schema_fragments` | no | `array<string>` | The custom schema fragments to use. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | Description of the part.<br>*Format: text* |
| `links` | no | `array<embed-links-create-request>` | Links associated with the part. |
| `name` | no | `string` | Name of the part.<br>*Format: text* |
| `owned_by` | no | `array<string>` | The users that own the part. |
| `stage_validation_options` | no | `array<stage-validation-option-for-create>` | The type of stage validations options when creating a part. |
| `tags` | no | `array<set-tag-with-value>` | Tags associated with the part. |
| `parent_part` | yes | `array<string>` | ID of the parent product for the capability.<br>*Items: items <= 1* |

#### Variant `parts-create-request-enhancement`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `parts-create-request-feature`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `parts-create-request-linkable`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `parts-create-request-product`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `parts-create-request-runnable`

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
curl -X POST "https://api.devrev.ai/parts.create" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "capability",
    "name": "string",
    "owned_by": [
      "DEVU-12345"
    ],
    "parent_part": [
      "PROD-12345"
    ]
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "part": {
    "type": "capability",
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
    "name": "string",
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
    ]
  }
}
```

</details>


<a id="delete"></a>

## `POST /parts.delete`

**Delete Part**

Source: <https://developer.devrev.ai/api-reference/parts/delete>

Deletes a [part](https://devrev.ai/docs/product/parts).

**Required scopes:** Depends on the object type in the `id` field:

| type | required scope |
| --- | --- |
| capability | `capability:all` |
| enhancement | `enhancement:all` |
| feature | `feature:all` |
| product | `product:all` |

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the part to delete.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/parts.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "PROD-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="get"></a>

## `GET /parts.get`

**Get Part**

Source: <https://developer.devrev.ai/api-reference/parts/get>

Gets a [part's](https://devrev.ai/docs/product/parts) information.

**Required scopes:** Depends on the object type in the `id` field:

| type | required scope |
| --- | --- |
| capability | `capability:read` OR `capability:write` OR `capability:all` |
| enhancement | `enhancement:read` OR `enhancement:write` OR `enhancement:all` |
| feature | `feature:read` OR `feature:write` OR `feature:all` |
| product | `product:read` OR `product:write` OR `product:all` |

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the part to retrieve.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/parts.get?id=PROD-12345"
```

<details><summary>Example 200 response</summary>

```json
{
  "part": {
    "type": "capability",
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
    "name": "string",
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
    ]
  }
}
```

</details>


<a id="get-post"></a>

## `POST /parts.get`

**Get Part (POST)**

Source: <https://developer.devrev.ai/api-reference/parts/get-post>

Gets a [part's](https://devrev.ai/docs/product/parts) information.

**Required scopes:** Depends on the object type in the `id` field:

| type | required scope |
| --- | --- |
| capability | `capability:read` OR `capability:write` OR `capability:all` |
| enhancement | `enhancement:read` OR `enhancement:write` OR `enhancement:all` |
| feature | `feature:read` OR `feature:write` OR `feature:all` |
| product | `product:read` OR `product:write` OR `product:all` |

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the part to retrieve.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/parts.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "PROD-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "part": {
    "type": "capability",
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
    "name": "string",
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
    ]
  }
}
```

</details>


<a id="list"></a>

## `GET /parts.list`

**List Parts**

Source: <https://developer.devrev.ai/api-reference/parts/list>

Lists a collection of [parts](https://devrev.ai/docs/product/parts).

**Required scopes:** Depends on the object type in the `id` field:

| type | required scope |
| --- | --- |
| capability | `capability:read` OR `capability:write` OR `capability:all` |
| enhancement | `enhancement:read` OR `enhancement:write` OR `enhancement:all` |
| feature | `feature:read` OR `feature:write` OR `feature:all` |
| product | `product:read` OR `product:write` OR `product:all` |

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for parts created by any of these users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `enhancement.accounts` | no | `array<string>` | Filters for enhancement by its accounts. |
| `enhancement.actual_close_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `enhancement.actual_close_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `enhancement.actual_start_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `enhancement.actual_start_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `enhancement.health` | no | `array<integer>` | Filters for enhancement by its health status. The allowed ids can be extended by the user. Stock allowed values:<br>```<br>  {<br>    "id": 1,<br>    "label": "On Track",<br>    "ordinal": 1,<br>    "overridable": true<br>  },<br>  {<br>    "id": 2,<br>    "label": "At Risk",<br>    "ordinal": 2,<br>    "overridable": true<br>  },<br>  {<br>    "id": 3,<br>    "label": "Off Track",<br>    "ordinal": 3,<br>    "overridable": true<br>  },<br>  {<br>    "id": 4,<br>    "label": "Not Applicable",<br>    "ordinal": 4,<br>    "overridable": true<br>  }<br>``` |
| `enhancement.opportunities` | no | `array<string>` | Filters for enhancement by its opportunities. |
| `enhancement.rev_score_tier` | no | `array<enhancement-rev-score-tier>` | Filters for enhancement by its rev score tier. |
| `enhancement.space.ids` | no | `array<string>` | Filters for the provided space IDs. |
| `enhancement.space.include_children` | no | `boolean` | Whether to include child spaces. |
| `enhancement.space.include_global` | no | `boolean` | Whether to include objects not associated with any space. |
| `enhancement.space.include_parents` | no | `boolean` | Whether to include parent spaces. |
| `enhancement.space.op` | no | `string` | The filter operator to be applied on space.<br>*Value in: "any" \| "not_any" \| "not_null" \| "null"* |
| `enhancement.stage_v2` | no | `array<string>` | List of IDs of the custom stages which will be used for filtering. |
| `enhancement.state_v2` | no | `array<string>` | Filters for part with any of the provided custom states. |
| `enhancement.target_close_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `enhancement.target_close_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `enhancement.target_start_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `enhancement.target_start_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `enhancement.tickets` | no | `array<string>` | Filters for enhancement by its tickets. |
| `limit` | no | `integer` | The maximum number of parts to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `modified_by` | no | `array<string>` | Filters for parts modified by any of these users. |
| `name` | no | `array<string>` | Filters for parts of the provided name(s). |
| `owned_by` | no | `array<string>` | Filters for parts owned by any of these users. |
| `parent_part.level` | no | `integer` | Number of levels to fetch the part hierarchy up to.<br>*Format: int32*<br>*Range: 1 <= value* |
| `parent_part.parts` | no | `array<string>` | Part IDs to fetch the hierarchy for. Required if any parent_part.* fields are provided.<br>*Items: 1 <= items* |
| `sort_by` | no | `array<string>` | Fields to sort the parts by and the direction to sort them. |
| `subtype` | no | `array<string>` | Filters for subtypes. |
| `tags` | no | `array<string>` | Filters for part with any of the provided tags. |
| `type` | no | `array<part-type>` | Filters for parts of the provided type(s). |

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
curl -X GET "https://api.devrev.ai/parts.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "parts": [
    {
      "type": "capability",
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
      "name": "string",
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
      ]
    }
  ],
  "prev_cursor": "string"
}
```

</details>


<a id="list-post"></a>

## `POST /parts.list`

**List Parts (POST)**

Source: <https://developer.devrev.ai/api-reference/parts/list-post>

Lists a collection of [parts](https://devrev.ai/docs/product/parts).

**Required scopes:** Depends on the object type in the `id` field:

| type | required scope |
| --- | --- |
| capability | `capability:read` OR `capability:write` OR `capability:all` |
| enhancement | `enhancement:read` OR `enhancement:write` OR `enhancement:all` |
| feature | `feature:read` OR `feature:write` OR `feature:all` |
| product | `product:read` OR `product:write` OR `product:all` |

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `array<part-type>` | Filters for parts of the provided type(s). |
| `created_by` | no | `array<string>` | Filters for parts created by any of these users. |
| `created_date_v2` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `enhancement` | no | `parts-filter-enhancement` |  |
| `limit` | no | `integer` | The maximum number of parts to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_by` | no | `array<string>` | Filters for parts modified by any of these users. |
| `modified_date_v2` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `name` | no | `array<string>` | Filters for parts of the provided name(s). |
| `owned_by` | no | `array<string>` | Filters for parts owned by any of these users. |
| `parent_part` | no | `parent-part-filter` | The filter for specifying parent part. |
| `sort_by` | no | `array<string>` | Fields to sort the parts by and the direction to sort them. |
| `subtype` | no | `array<string>` | Filters for subtypes. |
| `tags` | no | `array<string>` | Filters for part with any of the provided tags. |

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
curl -X POST "https://api.devrev.ai/parts.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "parts": [
    {
      "type": "capability",
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
      "name": "string",
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
      ]
    }
  ],
  "prev_cursor": "string"
}
```

</details>


<a id="update"></a>

## `POST /parts.update`

**Update Part**

Source: <https://developer.devrev.ai/api-reference/parts/update>

Updates a [part's](https://devrev.ai/docs/product/parts) information.

**Required scopes:** Depends on the object type in the `type` field:

| type | required scope |
| --- | --- |
| capability | `capability:write` OR `capability:all` |
| enhancement | `enhancement:write` OR `enhancement:all` |
| feature | `feature:write` OR `feature:all` |
| product | `product:write` OR `product:all` |

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `empty`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `string` | *Value in: "capability" \| "enhancement" \| "feature" \| "linkable" \| "product" \| "runnable"* |
| `artifacts` | no | `parts-update-request-artifacts` |  |
| `custom_fields` | no | `object` | Custom fields. |
| `custom_schema_fragments` | no | `array<string>` | The custom schema fragments to use. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | The updated description of the part.<br>*Format: text* |
| `id` | yes | `string` | The ID of the part to update.<br>*Format: id* |
| `name` | no | `string` | The updated name of the part.<br>*Format: text* |
| `owned_by` | no | `parts-update-request-owned-by` |  |
| `stage_validation_options` | no | `array<stage-validation-option-for-update>` | The type of stage validations options when updating the stage or the stage diagram of an object. |
| `tags` | no | `parts-update-request-tags` |  |
| `[key: string]` | no | `never` |  |

#### Variant `parts-update-request-capability`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `parts-update-request-enhancement`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `parts-update-request-feature`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `parts-update-request-linkable`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `parts-update-request-product`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `parts-update-request-runnable`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

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
curl -X POST "https://api.devrev.ai/parts.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "PROD-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "part": {
    "type": "capability",
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
    "name": "string",
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
    ]
  }
}
```

</details>
