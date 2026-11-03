# Airdrop

Source: <https://developer.devrev.ai/beta/api-reference/airdrop>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/airdrop.capabilities.get` | [capabilities-get](#capabilities-get) |
| POST | `/airdrop.capabilities.get` | [capabilities-get-post](#capabilities-get-post) |
| POST | `/airdrop.external-sync-units.discover` | [external-sync-units-discover](#external-sync-units-discover) |
| GET | `/airdrop.external-sync-units.list` | [external-sync-units-list](#external-sync-units-list) |
| POST | `/airdrop.external-sync-units.list` | [external-sync-units-list-post](#external-sync-units-list-post) |
| POST | `/airdrop.sync-units.action` | [trigger-sync-units-action](#trigger-sync-units-action) |
| POST | `/airdrop.sync-units.create` | [sync-units-create](#sync-units-create) |
| POST | `/airdrop.sync-units.create.bulk` | [sync-units-bulk-create](#sync-units-bulk-create) |
| GET | `/airdrop.sync-units.get` | [sync-units-get](#sync-units-get) |
| POST | `/airdrop.sync-units.get` | [sync-units-get-post](#sync-units-get-post) |
| GET | `/airdrop.sync-units.history` | [sync-units-history](#sync-units-history) |
| POST | `/airdrop.sync-units.history` | [sync-units-history-post](#sync-units-history-post) |
| GET | `/airdrop.sync-units.list` | [sync-units-list](#sync-units-list) |
| POST | `/airdrop.sync-units.list` | [sync-units-list-post](#sync-units-list-post) |
| POST | `/airdrop.sync-units.update` | [sync-units-update](#sync-units-update) |

<a id="capabilities-get"></a>

## `GET /airdrop.capabilities.get`

**Get Airdrop Capability**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/capabilities-get>

Gets the capabilities of airdrop.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `external_system_capabilities` | no | `array<external-system-capability>` | List of external system capabilities of possible imports and their constraints. |

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
curl -X GET "https://api.devrev.ai/airdrop.capabilities.get"
```

<details><summary>Example 200 response</summary>

```json
{
  "external_system_capabilities": [
    {
      "display_name": "string",
      "external_import_slug": "string",
      "external_system_name": "string",
      "external_system_type": "adaas",
      "icon_artifact": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "import_slug": "string",
      "keyring_type_ids": [
        "string"
      ],
      "marketplace_item_slug": "string",
      "min_sync_period": 0,
      "periodic_sync_directions": [
        "from_devrev"
      ],
      "snap_in_id": "string",
      "snap_in_name": "string",
      "snap_in_slug": "string",
      "supported_capabilities": [
        "computer_sync"
      ]
    }
  ],
  "external_system_names": [
    "string"
  ]
}
```

</details>


<a id="capabilities-get-post"></a>

## `POST /airdrop.capabilities.get`

**Get Airdrop Capability (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/capabilities-get-post>

Gets the capabilities of airdrop.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `external_system_capabilities` | no | `array<external-system-capability>` | List of external system capabilities of possible imports and their constraints. |

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
curl -X POST "https://api.devrev.ai/airdrop.capabilities.get" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "external_system_capabilities": [
    {
      "display_name": "string",
      "external_import_slug": "string",
      "external_system_name": "string",
      "external_system_type": "adaas",
      "icon_artifact": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "import_slug": "string",
      "keyring_type_ids": [
        "string"
      ],
      "marketplace_item_slug": "string",
      "min_sync_period": 0,
      "periodic_sync_directions": [
        "from_devrev"
      ],
      "snap_in_id": "string",
      "snap_in_name": "string",
      "snap_in_slug": "string",
      "supported_capabilities": [
        "computer_sync"
      ]
    }
  ],
  "external_system_names": [
    "string"
  ]
}
```

</details>


<a id="external-sync-units-discover"></a>

## `POST /airdrop.external-sync-units.discover`

**Discover Airdrop External Sync Units**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/external-sync-units-discover>

Request to discover external sync units on a given external system of record.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `external_import_slug` | no | `string` | External import slug which will perform external sync unit discovery, only populated for adaas external system type.<br>*Format: text* |
| `external_system_type` | yes | `string` | *Value in: "adaas" \| "confluence" \| "github" \| "hubspot" \| "jira" \| "jira_data_center" \| "linear" \| "rocketlane" \| "s3" \| "salesforce_sales" \| "salesforce_service" \| "servicenow" \| "sim" \| "zendesk"* |
| `import_slug` | no | `string` | Import slug which will perform external sync unit discovery, only populated for adaas external system type.<br>*Format: text* |
| `keyring` | yes | `string` | Keyring that will be used for external sync unit discovery.<br>*Format: id* |
| `snap_in_slug` | no | `string` | Snap in slug which will perform external sync unit discovery, only populated for adaas external system type.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/airdrop.external-sync-units.discover" \
  -H "Content-Type: application/json" \
  -d '{
    "external_system_type": "adaas",
    "keyring": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="external-sync-units-list"></a>

## `GET /airdrop.external-sync-units.list`

**List Airdrop External Sync Units**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/external-sync-units-list>

Lists external sync units.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `keyring` | yes | `string` | Keyring that will be used for external sync unit listing.<br>*Format: id* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `filter.external_sync_unit_name` | no | `string` | External sync unit name.<br>*Format: text* |
| `filter.external_system_type` | no | `string` | External system type.<br>*Value in: "adaas" \| "confluence" \| "github" \| "hubspot" \| "jira" \| "jira_data_center" \| "linear" \| "rocketlane" \| "s3" \| "salesforce_sales" \| "salesforce_service" \| "servicenow" \| "sim" \| "zendesk"* |
| `filter.import_slug` | no | `string` | Import slug of the connector.<br>*Format: text* |
| `filter.snap_in_slug` | no | `string` | Snap in slug of the connector.<br>*Format: text* |
| `filter.used` | no | `boolean` | Filter for external sync units that are used. |
| `limit` | no | `integer` | The maximum number of items to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |

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
curl -X GET "https://api.devrev.ai/airdrop.external-sync-units.list?keyring=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "external_sync_units": [
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
      "object_version": 0
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="external-sync-units-list-post"></a>

## `POST /airdrop.external-sync-units.list`

**List Airdrop External Sync Units (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/external-sync-units-list-post>

Lists external sync units.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `filter` | no | `airdrop-external-sync-units-list-filter` |  |
| `keyring` | yes | `string` | Keyring that will be used for external sync unit listing.<br>*Format: id* |
| `limit` | no | `integer` | The maximum number of items to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |

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
curl -X POST "https://api.devrev.ai/airdrop.external-sync-units.list" \
  -H "Content-Type: application/json" \
  -d '{
    "keyring": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "external_sync_units": [
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
      "object_version": 0
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="trigger-sync-units-action"></a>

## `POST /airdrop.sync-units.action`

**Action Airdrop Sync Units**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/trigger-sync-units-action>

Requests an action on a single sync unit.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `action` | yes | `string` | Available actions for a given SyncUnit.<br>*Value in: "delete" \| "full_sync" \| "start" \| "sync_from_devrev" \| "sync_to_devrev"* |
| `extract_from_date` | no | `string` | Date from which the sync unit should be extracted.<br>*Format: date-time* |
| `id` | yes | `string` | Sync unit on which the action should be triggered.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/airdrop.sync-units.action" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "delete",
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "sync_unit": {
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
    "external_sync_unit_name": "string",
    "external_system_id": "string",
    "external_system_name": "string",
    "external_system_type": "adaas",
    "is_archived": true,
    "name": "string",
    "sync_pack_id": "string",
    "sync_run": {
      "ended_at": "2023-01-01T12:00:00.000Z",
      "item_analytics_artifact": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "mode": "initial",
      "progress": {
        "state": "completed"
      },
      "reserved_rate_limit_percentage": 0,
      "started_at": "2023-01-01T12:00:00.000Z"
    },
    "sync_type": "manual"
  }
}
```

</details>


<a id="sync-units-create"></a>

## `POST /airdrop.sync-units.create`

**Create Airdrop Sync Unit**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/sync-units-create>

Creates sync unit that is used for syncs between DevRev and external system of records.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `sync_unit` | yes | `create-sync-unit` |  |

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
curl -X POST "https://api.devrev.ai/airdrop.sync-units.create" \
  -H "Content-Type: application/json" \
  -d '{
    "sync_unit": {
      "external_sync_unit": "string",
      "keyring": "string"
    }
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "sync_unit": {
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
    "external_sync_unit_name": "string",
    "external_system_id": "string",
    "external_system_name": "string",
    "external_system_type": "adaas",
    "is_archived": true,
    "name": "string",
    "sync_pack_id": "string",
    "sync_run": {
      "ended_at": "2023-01-01T12:00:00.000Z",
      "item_analytics_artifact": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "mode": "initial",
      "progress": {
        "state": "completed"
      },
      "reserved_rate_limit_percentage": 0,
      "started_at": "2023-01-01T12:00:00.000Z"
    },
    "sync_type": "manual"
  }
}
```

</details>


<a id="sync-units-bulk-create"></a>

## `POST /airdrop.sync-units.create.bulk`

**Bulk Airdrop Sync Units Create**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/sync-units-bulk-create>

Creates sync units that are used for syncs between DevRev and external systems of record.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `sync_units` | yes | `array<create-sync-unit>` | Sync unit create candidates. |

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
curl -X POST "https://api.devrev.ai/airdrop.sync-units.create.bulk" \
  -H "Content-Type: application/json" \
  -d '{
    "sync_units": [
      {
        "external_sync_unit": "string",
        "keyring": "string"
      }
    ]
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "sync_units": [
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
      "external_sync_unit_name": "string",
      "external_system_id": "string",
      "external_system_name": "string",
      "external_system_type": "adaas",
      "is_archived": true,
      "name": "string",
      "sync_pack_id": "string",
      "sync_run": {
        "ended_at": "2023-01-01T12:00:00.000Z",
        "item_analytics_artifact": {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        },
        "mode": "initial",
        "progress": {
          "state": "completed"
        },
        "reserved_rate_limit_percentage": 0,
        "started_at": "2023-01-01T12:00:00.000Z"
      },
      "sync_type": "manual"
    }
  ]
}
```

</details>


<a id="sync-units-get"></a>

## `GET /airdrop.sync-units.get`

**Get Airdrop Sync Unit**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/sync-units-get>

Gets a single sync unit's information.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | Requested sync unit ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/airdrop.sync-units.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "sync_unit": {
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
    "external_sync_unit_name": "string",
    "external_system_id": "string",
    "external_system_name": "string",
    "external_system_type": "adaas",
    "is_archived": true,
    "name": "string",
    "sync_pack_id": "string",
    "sync_run": {
      "ended_at": "2023-01-01T12:00:00.000Z",
      "item_analytics_artifact": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "mode": "initial",
      "progress": {
        "state": "completed"
      },
      "reserved_rate_limit_percentage": 0,
      "started_at": "2023-01-01T12:00:00.000Z"
    },
    "sync_type": "manual"
  }
}
```

</details>


<a id="sync-units-get-post"></a>

## `POST /airdrop.sync-units.get`

**Get Airdrop Sync Unit (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/sync-units-get-post>

Gets a single sync unit's information.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | Requested sync unit ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/airdrop.sync-units.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "sync_unit": {
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
    "external_sync_unit_name": "string",
    "external_system_id": "string",
    "external_system_name": "string",
    "external_system_type": "adaas",
    "is_archived": true,
    "name": "string",
    "sync_pack_id": "string",
    "sync_run": {
      "ended_at": "2023-01-01T12:00:00.000Z",
      "item_analytics_artifact": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "mode": "initial",
      "progress": {
        "state": "completed"
      },
      "reserved_rate_limit_percentage": 0,
      "started_at": "2023-01-01T12:00:00.000Z"
    },
    "sync_type": "manual"
  }
}
```

</details>


<a id="sync-units-history"></a>

## `GET /airdrop.sync-units.history`

**History Airdrop Sync Units**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/sync-units-history>

Gets a list of sync unit historical records.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | Sync unit that will be used for sync history listing.<br>*Format: id* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `filter.has_errors_or_warnings` | no | `boolean` | Filter for sync runs that have errors. |
| `filter.mode` | no | `array<sync-run-mode>` | Mode of the sync run. |
| `filter.started_by` | no | `array<sync-run-started-by>` | User who started the sync run. |
| `filter.state` | no | `array<sync-run-progress-state>` | State of the sync run. |
| `limit` | no | `integer` | The maximum number of items to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |

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
curl -X GET "https://api.devrev.ai/airdrop.sync-units.history?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "sync_history": [
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
      "sync_run": {
        "ended_at": "2023-01-01T12:00:00.000Z",
        "item_analytics_artifact": {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        },
        "mode": "initial",
        "progress": {
          "state": "completed"
        },
        "reserved_rate_limit_percentage": 0,
        "started_at": "2023-01-01T12:00:00.000Z"
      },
      "sync_unit": "string"
    }
  ]
}
```

</details>


<a id="sync-units-history-post"></a>

## `POST /airdrop.sync-units.history`

**History Airdrop Sync Units (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/sync-units-history-post>

Gets a list of sync unit historical records.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `filter` | no | `airdrop-sync-units-history-filter` |  |
| `id` | yes | `string` | Sync unit that will be used for sync history listing.<br>*Format: id* |
| `limit` | no | `integer` | The maximum number of items to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |

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
curl -X POST "https://api.devrev.ai/airdrop.sync-units.history" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "sync_history": [
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
      "sync_run": {
        "ended_at": "2023-01-01T12:00:00.000Z",
        "item_analytics_artifact": {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        },
        "mode": "initial",
        "progress": {
          "state": "completed"
        },
        "reserved_rate_limit_percentage": 0,
        "started_at": "2023-01-01T12:00:00.000Z"
      },
      "sync_unit": "string"
    }
  ]
}
```

</details>


<a id="sync-units-list"></a>

## `GET /airdrop.sync-units.list`

**List Airdrop Sync Units**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/sync-units-list>

Gets a list of sync units.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `filter.action_required` | no | `boolean` | Filter for sync units that have an action required. |
| `filter.external_system_name` | no | `array<string>` | Filters for sync units with the provided external system names. |
| `filter.external_system_type` | no | `array<external-system-type>` | External system type. |
| `filter.imported_by_id` | no | `array<string>` | ID of the user who imported the sync unit. |
| `filter.keyring_id` | no | `string` | Keyring ID associated with the import<br>*Format: id* |
| `filter.recipe_version` | no | `string` | Recipe version of the sync unit.<br>*Value in: "v2" \| "v3"* |
| `filter.state` | no | `array<sync-progress-state>` | State of the sync unit. |
| `filter.sync_pack_id` | no | `string` | Sync pack ID associated with the sync unit.<br>*Format: id* |
| `filter.sync_unit_name` | no | `string` | Sync unit name.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of sync units to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `sort_by` | no | `array<string>` | Comma-separated fields to sort the sync units by. |

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
curl -X GET "https://api.devrev.ai/airdrop.sync-units.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "sync_units": [
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
      "external_sync_unit_name": "string",
      "external_system_id": "string",
      "external_system_name": "string",
      "external_system_type": "adaas",
      "is_archived": true,
      "name": "string",
      "sync_pack_id": "string",
      "sync_run": {
        "ended_at": "2023-01-01T12:00:00.000Z",
        "item_analytics_artifact": {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        },
        "mode": "initial",
        "progress": {
          "state": "completed"
        },
        "reserved_rate_limit_percentage": 0,
        "started_at": "2023-01-01T12:00:00.000Z"
      },
      "sync_type": "manual"
    }
  ]
}
```

</details>


<a id="sync-units-list-post"></a>

## `POST /airdrop.sync-units.list`

**List Airdrop Sync Units (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/sync-units-list-post>

Gets a list of sync units.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `filter` | no | `airdrop-sync-units-list-filter` |  |
| `limit` | no | `integer` | The maximum number of sync units to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `sort_by` | no | `array<string>` | Comma-separated fields to sort the sync units by. |

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
curl -X POST "https://api.devrev.ai/airdrop.sync-units.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "sync_units": [
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
      "external_sync_unit_name": "string",
      "external_system_id": "string",
      "external_system_name": "string",
      "external_system_type": "adaas",
      "is_archived": true,
      "name": "string",
      "sync_pack_id": "string",
      "sync_run": {
        "ended_at": "2023-01-01T12:00:00.000Z",
        "item_analytics_artifact": {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        },
        "mode": "initial",
        "progress": {
          "state": "completed"
        },
        "reserved_rate_limit_percentage": 0,
        "started_at": "2023-01-01T12:00:00.000Z"
      },
      "sync_type": "manual"
    }
  ]
}
```

</details>


<a id="sync-units-update"></a>

## `POST /airdrop.sync-units.update`

**Update Airdrop Sync Unit**

Source: <https://developer.devrev.ai/beta/api-reference/airdrop/sync-units-update>

Updates a single sync unit.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `archive` | no | `boolean` | Flag to indicate the archive status of the sync unit. If set to true, the sync unit will be archived. |
| `extraction_window` | no | `string` | Extraction window for the sync unit.<br>*Format: text* |
| `first_sync_direction` | no | `string` | *Value in: "from_devrev" \| "to_devrev"* |
| `id` | yes | `string` | Sync unit on which the update should be performed.<br>*Format: id* |
| `keyring` | no | `string` | New keyring with which the sync unit will be updated.<br>*Format: id* |
| `periodic_sync` | no | `airdrop-periodic-sync-update` | Periodic sync configuration update. |
| `subscriber_ids` | no | `airdrop-sync-unit-subscriber-update-list` |  |
| `sync_tier` | no | `string` | The Tier in which a sync should be run.<br>*Value in: "tier_1" \| "tier_2" \| "tier_3"* |

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
curl -X POST "https://api.devrev.ai/airdrop.sync-units.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "sync_unit": {
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
    "external_sync_unit_name": "string",
    "external_system_id": "string",
    "external_system_name": "string",
    "external_system_type": "adaas",
    "is_archived": true,
    "name": "string",
    "sync_pack_id": "string",
    "sync_run": {
      "ended_at": "2023-01-01T12:00:00.000Z",
      "item_analytics_artifact": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "mode": "initial",
      "progress": {
        "state": "completed"
      },
      "reserved_rate_limit_percentage": 0,
      "started_at": "2023-01-01T12:00:00.000Z"
    },
    "sync_type": "manual"
  }
}
```

</details>
