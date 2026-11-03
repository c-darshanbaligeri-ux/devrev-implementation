# Groups

Source: <https://developer.devrev.ai/beta/api-reference/groups>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/groups.create` | [create](#create) |
| GET | `/groups.get` | [get](#get) |
| POST | `/groups.get` | [get-post](#get-post) |
| GET | `/groups.list` | [list](#list) |
| POST | `/groups.list` | [list-post](#list-post) |
| POST | `/groups.members.add` | [group-members-add](#group-members-add) |
| GET | `/groups.members.count` | [group-members-count](#group-members-count) |
| POST | `/groups.members.count` | [group-members-count-post](#group-members-count-post) |
| GET | `/groups.members.list` | [group-members-list](#group-members-list) |
| POST | `/groups.members.list` | [group-members-list-post](#group-members-list-post) |
| POST | `/groups.members.remove` | [group-members-remove](#group-members-remove) |
| POST | `/groups.update` | [update](#update) |

<a id="create"></a>

## `POST /groups.create`

**Create Group**

Source: <https://developer.devrev.ai/beta/api-reference/groups/create>

Creates a new group. A group is a collection of users.

**Required scopes:**

- `group:write` OR `group:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `string` | Type of the group.<br>*Value in: "dynamic" \| "static"* |
| `description` | yes | `string` | Description of the group.<br>*Format: text* |
| `dynamic_group_info` | no | `dynamic-group-info` | Information to define dynamic groups. |
| `member_type` | no | `string` | Type of the members in the group.<br>*Value in: "dev_user" \| "rev_user"* |
| `name` | yes | `string` | Unique name of the group.<br>*Format: text* |
| `owner` | no | `string` | Owner of the group.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/groups.create" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "string",
    "name": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "group": {
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
    "description": "string",
    "is_default": true,
    "member_type": "dev_user",
    "name": "string",
    "owner": {
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
    "parents": [
      "string"
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


<a id="get"></a>

## `GET /groups.get`

**Get Group**

Source: <https://developer.devrev.ai/beta/api-reference/groups/get>

Gets the requested group.

**Required scopes:**

- `group:read` OR `group:write` OR `group:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the group to get.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/groups.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "group": {
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
    "description": "string",
    "is_default": true,
    "member_type": "dev_user",
    "name": "string",
    "owner": {
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
    "parents": [
      "string"
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


<a id="get-post"></a>

## `POST /groups.get`

**Get Group (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/groups/get-post>

Gets the requested group.

**Required scopes:**

- `group:read` OR `group:write` OR `group:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the group to get.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/groups.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "group": {
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
    "description": "string",
    "is_default": true,
    "member_type": "dev_user",
    "name": "string",
    "owner": {
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
    "parents": [
      "string"
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


<a id="list"></a>

## `GET /groups.list`

**List Groups**

Source: <https://developer.devrev.ai/beta/api-reference/groups/list>

Lists the available groups.

**Required scopes:**

- `group:read` OR `group:write` OR `group:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters the groups on the basis of creator. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `group_type` | no | `array<group-type>` | Filters the groups based on the group type. |
| `ingestion_source` | no | `array<group-ingestion-source>` | Filter groups by ingestion source(s). |
| `is_archived` | no | `boolean` | Filters the groups on the basis of archival status. |
| `is_default` | no | `boolean` | Whether to fetch default or custom groups. |
| `limit` | no | `integer` | The maximum number of groups to return. The default is '50'.<br>*Format: int32* |
| `member_type` | no | `array<group-member-type>` | Filters the groups on basis of member type. |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `name` | no | `array<string>` | Filters the groups on the basis of group name. |
| `sort_by` | no | `array<string>` | Comma-separated fields to sort the groups by. |
| `space.ids` | no | `array<string>` | Filters for the provided space IDs. |
| `space.include_children` | no | `boolean` | Whether to include child spaces. |
| `space.include_global` | no | `boolean` | Whether to include objects not associated with any space. |
| `space.include_parents` | no | `boolean` | Whether to include parent spaces. |
| `space.op` | no | `string` | The filter operator to be applied on space.<br>*Value in: "any" \| "not_any" \| "not_null" \| "null"* |
| `sync_metadata.external_record` | no | `array<string>` | Filters for issues with this specific external record. |
| `sync_metadata.external_record_type` | no | `array<string>` | Filters for issues with this specific external record type. |
| `sync_metadata.external_reference` | no | `array<string>` | Filters for issues with this specific external reference. |
| `sync_metadata.last_sync_in.status` | no | `array<sync-metadata-filter-sync-in-filter-status>` | Filters for works with selected sync statuses. |
| `sync_metadata.last_sync_in.sync_history` | no | `array<string>` | Filters for works modified with selected sync history. |
| `sync_metadata.last_sync_in.sync_unit` | no | `array<string>` | Filters for works modified with selected sync units. |
| `sync_metadata.last_sync_out.status` | no | `array<sync-metadata-filter-sync-out-filter-status>` | Filters for works with selected sync statuses. |
| `sync_metadata.last_sync_out.sync_history` | no | `array<string>` | Filters for works modified with selected sync history. |
| `sync_metadata.last_sync_out.sync_unit` | no | `array<string>` | Filters for works modified with selected sync units. |
| `sync_metadata.origin_system` | no | `array<string>` | Filters for issues synced from this specific origin system. |

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
curl -X GET "https://api.devrev.ai/groups.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "groups": [
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
      "description": "string",
      "is_default": true,
      "member_type": "dev_user",
      "name": "string",
      "owner": {
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
      "parents": [
        "string"
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
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="list-post"></a>

## `POST /groups.list`

**List Groups (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/groups/list-post>

Lists the available groups.

**Required scopes:**

- `group:read` OR `group:write` OR `group:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters the groups on the basis of creator. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `group_type` | no | `array<group-type>` | Filters the groups based on the group type. |
| `ingestion_source` | no | `array<group-ingestion-source>` | Filter groups by ingestion source(s). |
| `is_archived` | no | `boolean` | Filters the groups on the basis of archival status. |
| `is_default` | no | `boolean` | Whether to fetch default or custom groups. |
| `limit` | no | `integer` | The maximum number of groups to return. The default is '50'.<br>*Format: int32* |
| `member_type` | no | `array<group-member-type>` | Filters the groups on basis of member type. |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `name` | no | `array<string>` | Filters the groups on the basis of group name. |
| `sort_by` | no | `array<string>` | Comma-separated fields to sort the groups by. |
| `space` | no | `space-filter` |  |
| `sync_metadata` | no | `sync-metadata-filter` |  |

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
curl -X POST "https://api.devrev.ai/groups.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "groups": [
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
      "description": "string",
      "is_default": true,
      "member_type": "dev_user",
      "name": "string",
      "owner": {
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
      "parents": [
        "string"
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
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="group-members-add"></a>

## `POST /groups.members.add`

**Add Groups Members**

Source: <https://developer.devrev.ai/beta/api-reference/groups/group-members-add>

Adds a member to a group.

**Required scopes:**

- `group_membership:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `group` | yes | `string` | ID of the group where the member is being added.<br>*Format: id* |
| `member` | yes | `string` | ID of the member to be added. Can be a user or a group.<br>*Format: id* |
| `member_rev_org` | no | `string` | Rev org of the rev user to be added. This should be specified only if the member is a rev user<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/groups.members.add" \
  -H "Content-Type: application/json" \
  -d '{
    "group": "string",
    "member": "DEVU-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="group-members-count"></a>

## `GET /groups.members.count`

**Count Groups Members**

Source: <https://developer.devrev.ai/beta/api-reference/groups/group-members-count>

Counts the members in a group.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `group` | yes | `string` | ID of the group for which to count members.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/groups.members.count?group=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "count": 0,
  "has_more": true
}
```

</details>


<a id="group-members-count-post"></a>

## `POST /groups.members.count`

**Count Groups Members (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/groups/group-members-count-post>

Counts the members in a group.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `group` | yes | `string` | ID of the group for which to count members.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/groups.members.count" \
  -H "Content-Type: application/json" \
  -d '{
    "group": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "count": 0,
  "has_more": true
}
```

</details>


<a id="group-members-list"></a>

## `GET /groups.members.list`

**List Groups Members**

Source: <https://developer.devrev.ai/beta/api-reference/groups/group-members-list>

Lists the members in a group.

**Required scopes:**

- `group_membership:read` OR `group_membership:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `group` | yes | `string` | ID of the group for which to list members.<br>*Format: id* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of members to return. If not set, then the default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `sort_by` | no | `array<string>` | Fields to sort the group members by and the direction to sort them. |

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
curl -X GET "https://api.devrev.ai/groups.members.list?group=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "members": [
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
      "member_rev_org": {
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="group-members-list-post"></a>

## `POST /groups.members.list`

**List Groups Members (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/groups/group-members-list-post>

Lists the members in a group.

**Required scopes:**

- `group_membership:read` OR `group_membership:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `group` | yes | `string` | ID of the group for which to list members.<br>*Format: id* |
| `limit` | no | `integer` | The maximum number of members to return. If not set, then the default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `sort_by` | no | `array<string>` | Fields to sort the group members by and the direction to sort them. |

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
curl -X POST "https://api.devrev.ai/groups.members.list" \
  -H "Content-Type: application/json" \
  -d '{
    "group": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "members": [
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
      "member_rev_org": {
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="group-members-remove"></a>

## `POST /groups.members.remove`

**Remove Groups Members**

Source: <https://developer.devrev.ai/beta/api-reference/groups/group-members-remove>

Removes a member from a group.

**Required scopes:**

- `group_membership:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `group` | yes | `string` | ID of the group where the member is being removed.<br>*Format: id* |
| `member` | yes | `string` | ID of the member to be removed. Can be a user or a group.<br>*Format: id* |
| `member_rev_org` | no | `string` | Rev org of the rev user to be removed. This should be specified only if the member is a rev user<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/groups.members.remove" \
  -H "Content-Type: application/json" \
  -d '{
    "group": "string",
    "member": "DEVU-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="update"></a>

## `POST /groups.update`

**Update Group**

Source: <https://developer.devrev.ai/beta/api-reference/groups/update>

Updates the requested group.

**Required scopes:**

- `group:write` OR `group:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `description` | no | `string` | The updated group's description.<br>*Format: text* |
| `dynamic_group_info` | no | `groups-update-request-dynamic-group-info` |  |
| `id` | yes | `string` | The ID of the group to update.<br>*Format: id* |
| `name` | no | `string` | The updated group's name.<br>*Format: text* |
| `owner` | no | `string\|null` | The updated group's owner.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/groups.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "group": {
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
    "description": "string",
    "is_default": true,
    "member_type": "dev_user",
    "name": "string",
    "owner": {
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
    "parents": [
      "string"
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
