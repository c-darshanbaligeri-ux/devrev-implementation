# Vistas

Source: <https://developer.devrev.ai/api-reference/vistas>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/vistas.delete` | [delete](#delete) |
| GET | `/vistas.get` | [get](#get) |
| POST | `/vistas.get` | [get-post](#get-post) |
| POST | `/vistas.groups.delete` | [groups-delete](#groups-delete) |
| GET | `/vistas.groups.get` | [groups-get](#groups-get) |
| POST | `/vistas.groups.get` | [groups-get-post](#groups-get-post) |
| GET | `/vistas.groups.list` | [groups-list](#groups-list) |
| POST | `/vistas.groups.list` | [groups-list-post](#groups-list-post) |
| GET | `/vistas.list` | [list](#list) |
| POST | `/vistas.list` | [list-post](#list-post) |

<a id="delete"></a>

## `POST /vistas.delete`

**Delete Vista**

Source: <https://developer.devrev.ai/api-reference/vistas/delete>

Deletes the requested vista.

**Required scopes:**

- `vista:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the vista to delete.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/vistas.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "VISTA-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="get"></a>

## `GET /vistas.get`

**Get Vista**

Source: <https://developer.devrev.ai/api-reference/vistas/get>

Gets the requested vistas's information.

**Required scopes:**

- `vista:read` OR `vista:write` OR `vista:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The vista's ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/vistas.get?id=VISTA-12345"
```

<details><summary>Example 200 response</summary>

```json
{
  "vista": {
    "type": "curated",
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
    "is_default": true,
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
    "items": [
      {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    ]
  }
}
```

</details>


<a id="get-post"></a>

## `POST /vistas.get`

**Get Vista (POST)**

Source: <https://developer.devrev.ai/api-reference/vistas/get-post>

Gets the requested vistas's information.

**Required scopes:**

- `vista:read` OR `vista:write` OR `vista:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The vista's ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/vistas.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "VISTA-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "vista": {
    "type": "curated",
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
    "is_default": true,
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
    "items": [
      {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    ]
  }
}
```

</details>


<a id="groups-delete"></a>

## `POST /vistas.groups.delete`

**Delete Vistas Group**

Source: <https://developer.devrev.ai/api-reference/vistas/groups-delete>

Deletes the requested vista group item

**Required scopes:**

- `vista:all`

No scopes required for default vistas.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | ID of the vista group item to be deleted.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/vistas.groups.delete" \
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


<a id="groups-get"></a>

## `GET /vistas.groups.get`

**Get Vistas Group**

Source: <https://developer.devrev.ai/api-reference/vistas/groups-get>

Gets the requested vista group item's information.

**Required scopes:**

- `vista:read` OR `vista:write` OR `vista:all`

No scopes required for default vistas.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The vista group item's ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/vistas.groups.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "vista_group": {
    "object_type": "conversations",
    "end_date": "2023-01-01T12:00:00.000Z",
    "goals": "string",
    "goals_document": "ARTIFACT-12345",
    "id": "string",
    "name": "string",
    "parent": {
      "type": "string",
      "display_id": "string",
      "flavor": "nnl",
      "id": "VISTA-12345",
      "name": "string"
    },
    "start_date": "2023-01-01T12:00:00.000Z",
    "state": "active",
    "type": "curated"
  }
}
```

</details>


<a id="groups-get-post"></a>

## `POST /vistas.groups.get`

**Get Vistas Group (POST)**

Source: <https://developer.devrev.ai/api-reference/vistas/groups-get-post>

Gets the requested vista group item's information.

**Required scopes:**

- `vista:read` OR `vista:write` OR `vista:all`

No scopes required for default vistas.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The vista group item's ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/vistas.groups.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "vista_group": {
    "object_type": "conversations",
    "end_date": "2023-01-01T12:00:00.000Z",
    "goals": "string",
    "goals_document": "ARTIFACT-12345",
    "id": "string",
    "name": "string",
    "parent": {
      "type": "string",
      "display_id": "string",
      "flavor": "nnl",
      "id": "VISTA-12345",
      "name": "string"
    },
    "start_date": "2023-01-01T12:00:00.000Z",
    "state": "active",
    "type": "curated"
  }
}
```

</details>


<a id="groups-list"></a>

## `GET /vistas.groups.list`

**List Vistas Groups**

Source: <https://developer.devrev.ai/api-reference/vistas/groups-list>

Lists the available vista group items.

**Required scopes:**

- `vista:read` OR `vista:write` OR `vista:all`

No scopes required for default vistas.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `ancestor_part` | no | `array<string>` | Filters for vista group items which have one of the parts linked as its ancestor part or primary part. |
| `applies_to_part.include_child_parts` | no | `boolean` | Whether to include items belonging to children of any of the provided parts. |
| `applies_to_part.parts` | no | `array<string>` | Part IDs to filter on. Required if any applies_to_part.* fields are provided. |
| `created_by` | no | `array<string>` | Filter for vistas group item created by any of these users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `group_object_type` | no | `array<vista-group-item-group-object-type>` | Filters for vista group items of the specific group object type. |
| `limit` | no | `integer` | The request to get information about a list of vista groups.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `parent_id` | no | `array<string>` | Parent ID of the vista group item. |
| `sort_by` | no | `array<string>` | Comma-separated fields to sort the objects by. |
| `state` | no | `array<vista-group-item-state>` | Denotes the state of the vista group item. |
| `type` | no | `array<group-item-type>` | Filters for vista group items of the specific type. |

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
curl -X GET "https://api.devrev.ai/vistas.groups.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "vista_group": [
    {
      "object_type": "conversations",
      "end_date": "2023-01-01T12:00:00.000Z",
      "goals": "string",
      "goals_document": "ARTIFACT-12345",
      "id": "string",
      "name": "string",
      "parent": {
        "type": "string",
        "display_id": "string",
        "flavor": "nnl",
        "id": "VISTA-12345",
        "name": "string"
      },
      "start_date": "2023-01-01T12:00:00.000Z",
      "state": "active",
      "type": "curated"
    }
  ]
}
```

</details>


<a id="groups-list-post"></a>

## `POST /vistas.groups.list`

**List Vistas Groups (POST)**

Source: <https://developer.devrev.ai/api-reference/vistas/groups-list-post>

Lists the available vista group items.

**Required scopes:**

- `vista:read` OR `vista:write` OR `vista:all`

No scopes required for default vistas.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `array<group-item-type>` | Filters for vista group items of the specific type. |
| `ancestor_part` | no | `array<string>` | Filters for vista group items which have one of the parts linked as its ancestor part or primary part. |
| `applies_to_part` | no | `applies-to-part-filter` | The filter for applies to part. |
| `created_by` | no | `array<string>` | Filter for vistas group item created by any of these users. |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `end_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `group_object_type` | no | `array<vista-group-item-group-object-type>` | Filters for vista group items of the specific group object type. |
| `limit` | no | `integer` | The request to get information about a list of vista groups.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `parent_id` | no | `array<string>` | Parent ID of the vista group item. |
| `sort_by` | no | `array<string>` | Comma-separated fields to sort the objects by. |
| `start_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `state` | no | `array<vista-group-item-state>` | Denotes the state of the vista group item. |

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
curl -X POST "https://api.devrev.ai/vistas.groups.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "vista_group": [
    {
      "object_type": "conversations",
      "end_date": "2023-01-01T12:00:00.000Z",
      "goals": "string",
      "goals_document": "ARTIFACT-12345",
      "id": "string",
      "name": "string",
      "parent": {
        "type": "string",
        "display_id": "string",
        "flavor": "nnl",
        "id": "VISTA-12345",
        "name": "string"
      },
      "start_date": "2023-01-01T12:00:00.000Z",
      "state": "active",
      "type": "curated"
    }
  ]
}
```

</details>


<a id="list"></a>

## `GET /vistas.list`

**List Vistas**

Source: <https://developer.devrev.ai/api-reference/vistas/list>

Lists the available vistas.

**Required scopes:**

- `vista:read` OR `vista:write` OR `vista:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for vistas created by any of these users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `flavor` | no | `array<grouped-vista-flavor>` | Filters for vistas of specific flavor. |
| `is_default` | no | `boolean` | Whether the default vistas should be fetched or not. |
| `limit` | no | `integer` | The maximum number of vistas to return. The default is '50', the maximum is '100'.<br>*Format: int32* |
| `members` | no | `array<string>` | Filters for vistas accessible to the input members. |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `object_type` | no | `array<dynamic-vista-filter-type>` | Filters for vistas of specific object types like works, parts etc. |
| `shared_with.member` | no | `string` | ID of the group/member with whom the item is shared.<br>*Format: id* |
| `shared_with.role` | no | `string` | Role ID of the group/member with whom the item is shared.<br>*Format: id* |
| `skip_items` | no | `boolean` | Denotes whether to skip items of vista_group_item in response. |
| `sort_by` | no | `array<string>` | Fields to sort the vistas by and the direction to sort them. |
| `state` | no | `array<vista-group-item-state>` | Denotes the state of the vista group item. |
| `type` | no | `array<vista-type>` | Filters for vistas of the specific type. |

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
curl -X GET "https://api.devrev.ai/vistas.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "vistas": [
    {
      "type": "curated",
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
      "is_default": true,
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
      "items": [
        {
          "type": "account",
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      ]
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /vistas.list`

**List Vistas (POST)**

Source: <https://developer.devrev.ai/api-reference/vistas/list-post>

Lists the available vistas.

**Required scopes:**

- `vista:read` OR `vista:write` OR `vista:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `array<vista-type>` | Filters for vistas of the specific type. |
| `created_by` | no | `array<string>` | Filters for vistas created by any of these users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `flavor` | no | `array<grouped-vista-flavor>` | Filters for vistas of specific flavor. |
| `is_default` | no | `boolean` | Whether the default vistas should be fetched or not. |
| `limit` | no | `integer` | The maximum number of vistas to return. The default is '50', the maximum is '100'.<br>*Format: int32* |
| `members` | no | `array<string>` | Filters for vistas accessible to the input members. |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `object_type` | no | `array<dynamic-vista-filter-type>` | Filters for vistas of specific object types like works, parts etc. |
| `shared_with` | no | `array<shared-with-membership-filter>` | Filter for vistas accessible to the input members. |
| `skip_items` | no | `boolean` | Denotes whether to skip items of vista_group_item in response. |
| `sort_by` | no | `array<string>` | Fields to sort the vistas by and the direction to sort them. |
| `state` | no | `array<vista-group-item-state>` | Denotes the state of the vista group item. |

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
curl -X POST "https://api.devrev.ai/vistas.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "vistas": [
    {
      "type": "curated",
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
      "is_default": true,
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
      "items": [
        {
          "type": "account",
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      ]
    }
  ]
}
```

</details>
