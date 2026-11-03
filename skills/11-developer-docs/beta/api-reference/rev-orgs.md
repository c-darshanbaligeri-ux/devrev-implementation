# Rev Orgs

Source: <https://developer.devrev.ai/beta/api-reference/rev-orgs>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/rev-orgs.create` | [create](#create) |
| POST | `/rev-orgs.delete` | [delete](#delete) |
| GET | `/rev-orgs.get` | [get](#get) |
| POST | `/rev-orgs.get` | [get-post](#get-post) |
| GET | `/rev-orgs.list` | [list](#list) |
| POST | `/rev-orgs.list` | [list-post](#list-post) |
| POST | `/rev-orgs.update` | [update](#update) |

<a id="create"></a>

## `POST /rev-orgs.create`

**Create Rev Org**

Source: <https://developer.devrev.ai/beta/api-reference/rev-orgs/create>

Creates a Rev organization in the authenticated user's Dev organization.

**Required scopes:**

- `rev_org:write` OR `rev_org:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `account` | yes | `string` | Account Id to associate with this Rev organization.<br>*Format: id* |
| `artifacts` | no | `array<string>` | The IDs of the artifacts to associate with the Rev organization. |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_fragments` | no | `array<string>` | Schema fragment IDs associated with this Rev organization. |
| `description` | no | `string` | Description of the Rev organization.<br>*Format: text* |
| `display_name` | yes | `string` | Name of the Rev organization.<br>*Format: text* |
| `domain` | no | `string` | **Deprecated.**<br>Company's domain name. Example - 'devrev.ai'.<br>*Format: text* |
| `environment` | no | `string` | The environment of the Org. Defaults to 'production' if not specified.<br>*Value in: "production" \| "staging" \| "test"* |
| `external_ref` | no | `string` | External ref is a custom unique identifier which is a reference to an unique id for this organization's data in some system of records.<br>*Format: text* |
| `shared_with` | no | `array<set-shared-with-membership>` | Members this Rev organization is shared with. |
| `tags` | no | `array<set-tag-with-value>` | Tags associated with the Rev organization. |
| `tier` | no | `string` | The tier of the RevOrg.<br>*Format: text* |

### Response codes

- `201` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `409` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/rev-orgs.create" \
  -H "Content-Type: application/json" \
  -d '{
    "account": "ACC-12345",
    "display_name": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "rev_org": {
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
    "account": {
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
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
    "domain": "string",
    "external_ref": "string",
    "primary_rev_org": {
      "type": "account",
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
    ]
  }
}
```

</details>


<a id="delete"></a>

## `POST /rev-orgs.delete`

**Delete Rev Org**

Source: <https://developer.devrev.ai/beta/api-reference/rev-orgs/delete>

Deletes the Rev organization.

**Required scopes:**

- `rev_org:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of Rev organization to delete.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/rev-orgs.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "REV-AbCdEfGh"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="get"></a>

## `GET /rev-orgs.get`

**Get Rev Org**

Source: <https://developer.devrev.ai/beta/api-reference/rev-orgs/get>

Retrieves the Rev organization's information.

**Required scopes:**

- `rev_org:read` OR `rev_org:write` OR `rev_org:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `account` | no | `string` | The ID of account for which default Rev organization is to be fetched.<br>*Format: id* |
| `id` | no | `string` | The ID of the required Rev organization.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/rev-orgs.get"
```

<details><summary>Example 200 response</summary>

```json
{
  "rev_org": {
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
    "account": {
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
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
    "domain": "string",
    "external_ref": "string",
    "primary_rev_org": {
      "type": "account",
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
    ]
  }
}
```

</details>


<a id="get-post"></a>

## `POST /rev-orgs.get`

**Get Rev Org (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/rev-orgs/get-post>

Retrieves the Rev organization's information.

**Required scopes:**

- `rev_org:read` OR `rev_org:write` OR `rev_org:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `account` | no | `string` | The ID of account for which default Rev organization is to be fetched.<br>*Format: id* |
| `id` | no | `string` | The ID of the required Rev organization.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/rev-orgs.get" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "rev_org": {
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
    "account": {
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
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
    "domain": "string",
    "external_ref": "string",
    "primary_rev_org": {
      "type": "account",
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
    ]
  }
}
```

</details>


<a id="list"></a>

## `GET /rev-orgs.list`

**List Rev Orgs**

Source: <https://developer.devrev.ai/beta/api-reference/rev-orgs/list>

Gets the list of Rev organizations' information belonging to the authenticated user's Dev Organization which the user is also authorized to access.

**Required scopes:**

- `rev_org:read` OR `rev_org:write` OR `rev_org:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `account` | no | `array<string>` | Filters by account. |
| `created_by` | no | `array<string>` | Filters by creator. |
| `created_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `created_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_field_filter` | no | `array<string>` | Filters on custom fields. Input will be of the format (custom_field_filter=field_name1:val1,val2,val3&custom_field_filter=field_name2:val1,val2). |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `display_name` | no | `array<string>` | Array of display names of Rev orgs to be filtered. |
| `external_ref` | no | `array<string>` | List of external refs to filter Rev organizations for. |
| `limit` | no | `integer` | The maximum number of Rev organizations to be retrieved per page.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `modified_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `modified_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `sort_by` | no | `array<string>` | Fields to sort the Rev organizations by and the direction to sort them. |
| `tags` | no | `array<string>` | List of tags to be filtered. |

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
curl -X GET "https://api.devrev.ai/rev-orgs.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "rev_orgs": [
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
      "display_name": "string",
      "account": {
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
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
      "domain": "string",
      "external_ref": "string",
      "primary_rev_org": {
        "type": "account",
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
      ]
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /rev-orgs.list`

**List Rev Orgs (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/rev-orgs/list-post>

Gets the list of Rev organizations' information belonging to the authenticated user's Dev Organization which the user is also authorized to access.

**Required scopes:**

- `rev_org:read` OR `rev_org:write` OR `rev_org:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `account` | no | `array<string>` | Filters by account. |
| `created_by` | no | `array<string>` | Filters by creator. |
| `created_date` | no | `date-time-filter` |  |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_field_filter` | no | `array<string>` | Filters on custom fields. Input will be of the format (custom_field_filter=field_name1:val1,val2,val3&custom_field_filter=field_name2:val1,val2). |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `display_name` | no | `array<string>` | Array of display names of Rev orgs to be filtered. |
| `external_ref` | no | `array<string>` | List of external refs to filter Rev organizations for. |
| `limit` | no | `integer` | The maximum number of Rev organizations to be retrieved per page.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter` |  |
| `sort_by` | no | `array<string>` | Fields to sort the Rev organizations by and the direction to sort them. |
| `tags` | no | `array<string>` | List of tags to be filtered. |

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
curl -X POST "https://api.devrev.ai/rev-orgs.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "rev_orgs": [
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
      "display_name": "string",
      "account": {
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
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
      "domain": "string",
      "external_ref": "string",
      "primary_rev_org": {
        "type": "account",
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
      ]
    }
  ]
}
```

</details>


<a id="update"></a>

## `POST /rev-orgs.update`

**Update Rev Org**

Source: <https://developer.devrev.ai/beta/api-reference/rev-orgs/update>

Updates the Rev organization's information.

**Required scopes:**

- `rev_org:write` OR `rev_org:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `account` | no | `string` | **Deprecated.**<br>New account ID to associate with this Rev organization.<br>*Format: id* |
| `artifacts` | no | `rev-orgs-update-request-artifacts` |  |
| `custom_schema_fragments` | no | `array<string>` | Schema fragment IDs associated with this Rev organization. |
| `description` | no | `string` | Description of the Rev organization.<br>*Format: text* |
| `display_name` | no | `string` | Customer chosen name for the Rev organization.<br>*Format: text* |
| `domain` | no | `string` | **Deprecated.**<br>Company's domain name. Example - 'devrev.ai'.<br>*Format: text* |
| `environment` | no | `string` | The environment of the Org. Defaults to 'production' if not specified.<br>*Value in: "production" \| "staging" \| "test"* |
| `external_ref` | no | `string` | External ref is a custom unique identifier which is a reference to an unique id for this organization's data in some system of records.<br>*Format: text* |
| `id` | yes | `string` | The ID of Rev organization to update.<br>*Format: id* |
| `shared_with` | no | `rev-orgs-update-request-shared-with` |  |
| `tags` | no | `array<set-tag-with-value>` | Tags associated with the Rev organization. |
| `tier` | no | `string` | The tier of the RevOrg.<br>*Format: text* |

### Response codes

- `200` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `404` — `application/json`
- `409` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/rev-orgs.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "REV-AbCdEfGh"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "rev_org": {
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
    "account": {
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
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
    "domain": "string",
    "external_ref": "string",
    "primary_rev_org": {
      "type": "account",
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
    ]
  }
}
```

</details>
