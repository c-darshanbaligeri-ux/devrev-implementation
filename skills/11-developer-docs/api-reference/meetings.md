# Meetings

Source: <https://developer.devrev.ai/api-reference/meetings>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/meetings.count` | [count](#count) |
| POST | `/meetings.count` | [count-post](#count-post) |
| POST | `/meetings.create` | [create](#create) |
| POST | `/meetings.delete` | [delete](#delete) |
| GET | `/meetings.get` | [get](#get) |
| POST | `/meetings.get` | [get-post](#get-post) |
| GET | `/meetings.list` | [list](#list) |
| POST | `/meetings.list` | [list-post](#list-post) |
| POST | `/meetings.update` | [update](#update) |

<a id="count"></a>

## `GET /meetings.count`

**Count Meetings**

Source: <https://developer.devrev.ai/api-reference/meetings/count>

Counts the meeting records.

**Required scopes:**

- `meeting:read` OR `meeting:write` OR `meeting:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `channel` | no | `array<meeting-channel>` | Filters for meeting on specified channels. |
| `created_by` | no | `array<string>` | Filters for meetings created by the specified user(s). |
| `custom_fields` | no | `object` | Filters for meeting on custom fields. |
| `direction` | no | `array<meeting-direction>` | Direction of the meetings to be fetched. |
| `external_ref` | no | `array<string>` | Filters for meetings with the provided external_ref(s). |
| `links.link_type` | no | `string` | Filters for link type in links associated with the meeting.<br>*Format: text* |
| `links.target` | no | `string` | Filters for target id in links associated with the meeting.<br>*Format: id* |
| `links.target_object_type` | no | `string` | Filters for target object type in links associated with the meeting.<br>*Format: text* |
| `members` | no | `array<string>` | Filter for meeting on specified Member Ids. |
| `organizer` | no | `array<string>` | Filter for meeting on specified organizers. |
| `parent` | no | `array<string>` | **Deprecated.**<br>Filters for meetings with the provided parent. |
| `state` | no | `array<meeting-state>` | Filters for meeting on specified state or outcomes. |
| `subtype` | no | `array<string>` | Subtypes of meeting to be filtered. |
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
| `tags` | no | `array<string>` | Filters for meeting by tags. |

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
curl -X GET "https://api.devrev.ai/meetings.count"
```

<details><summary>Example 200 response</summary>

```json
{
  "count": 0
}
```

</details>


<a id="count-post"></a>

## `POST /meetings.count`

**Count Meetings (POST)**

Source: <https://developer.devrev.ai/api-reference/meetings/count-post>

Counts the meeting records.

**Required scopes:**

- `meeting:read` OR `meeting:write` OR `meeting:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `channel` | no | `array<meeting-channel>` | Filters for meeting on specified channels. |
| `created_by` | no | `array<string>` | Filters for meetings created by the specified user(s). |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `custom_fields` | no | `object` | Filters for meeting on custom fields. |
| `direction` | no | `array<meeting-direction>` | Direction of the meetings to be fetched. |
| `ended_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `external_ref` | no | `array<string>` | Filters for meetings with the provided external_ref(s). |
| `links` | no | `array<meetings-filter-link-summary-filter>` | Filters for links associated with the meeting. |
| `members` | no | `array<string>` | Filter for meeting on specified Member Ids. |
| `modified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `organizer` | no | `array<string>` | Filter for meeting on specified organizers. |
| `parent` | no | `array<string>` | **Deprecated.**<br>Filters for meetings with the provided parent. |
| `scheduled_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `state` | no | `array<meeting-state>` | Filters for meeting on specified state or outcomes. |
| `subtype` | no | `array<string>` | Subtypes of meeting to be filtered. |
| `sync_metadata` | no | `sync-metadata-filter` |  |
| `tags` | no | `array<string>` | Filters for meeting by tags. |

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
curl -X POST "https://api.devrev.ai/meetings.count" \
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

## `POST /meetings.create`

**Create Meeting**

Source: <https://developer.devrev.ai/api-reference/meetings/create>

Creates a new meeting record.

**Required scopes:**

- `meeting:write` OR `meeting:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `artifacts` | no | `array<string>` | The IDs of the artifacts to associate with the meeting. |
| `channel` | yes | `string` | The channel of meeting.<br>*Value in: "amazon_connect" \| "google_meet" \| "offline" \| "other" \| "teams" \| "zoom"* |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | The description of the meeting.<br>*Format: text* |
| `ended_date` | no | `string` | Time at which meeting ended.<br>*Format: date-time* |
| `external_ref` | no | `string` | External reference for the meeting.<br>*Format: text* |
| `external_url` | no | `string` | External URL for the meeting.<br>*Format: text* |
| `members` | no | `array<string>` | IDs of the users or groups that were part of the meeting.<br>*Items: 1 <= items <= 2000* |
| `organizer` | no | `string` | The ID of the user who organized the meeting. If not provided, the creator is set as the organizer.<br>*Format: id* |
| `parent` | no | `string` | **Deprecated.**<br>The parent object ID in which the meeting was created.<br>*Format: id* |
| `recording` | no | `string` | The ID of the meeting's recording artifact.<br>*Format: id* |
| `recording_url` | no | `string` | The recording URL of the meeting.<br>*Format: text* |
| `scheduled_date` | no | `string` | The date and time when the meeting was scheduled.<br>*Format: date-time* |
| `state` | yes | `string` | The state of meeting.<br>*Value in: "canceled" \| "completed" \| "no_show" \| "ongoing" \| "rejected" \| "rescheduled" \| "scheduled" \| "waiting"* |
| `tags` | no | `array<set-tag-with-value>` | Tags associated with the meeting. |
| `title` | yes | `string` | The title of the meeting.<br>*Format: text* |
| `transcript` | no | `string` | The ID of the artifact for the transcript of the meeting.<br>*Format: id* |
| `transcript_article` | no | `string` | The article for the transcript of the meeting.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/meetings.create" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "amazon_connect",
    "state": "canceled",
    "title": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "meeting": {
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
    "channel": "amazon_connect",
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "direction": "incoming",
    "ended_date": "2023-01-01T12:00:00.000Z",
    "external_ref": "string",
    "external_refs": [
      "string"
    ],
    "external_url": "string",
    "is_archived": true,
    "members": [
      {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    ],
    "organizer": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "parent": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "primary_meeting": {
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
      },
      "title": "string"
    },
    "recording": {
      "display_id": "string",
      "id": "string",
      "file": {
        "type": "string",
        "name": "string",
        "size": 0
      }
    },
    "recording_url": "string",
    "scheduled_date": "2023-01-01T12:00:00.000Z",
    "source_date": "2023-01-01T12:00:00.000Z",
    "state": "canceled",
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
    ],
    "title": "string",
    "transcript": {
      "display_id": "string",
      "id": "string",
      "file": {
        "type": "string",
        "name": "string",
        "size": 0
      }
    },
    "transcript_article": {
      "display_id": "string",
      "id": "string",
      "article_type": "article",
      "resource": {
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
        "url": "string"
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
      },
      "title": "string"
    },
    "visibility": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    }
  }
}
```

</details>


<a id="delete"></a>

## `POST /meetings.delete`

**Delete Meeting**

Source: <https://developer.devrev.ai/api-reference/meetings/delete>

Deletes the meeting record.

**Required scopes:**

- `meeting:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The meeting's ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/meetings.delete" \
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

## `GET /meetings.get`

**Get Meeting**

Source: <https://developer.devrev.ai/api-reference/meetings/get>

Gets the meeting record.

**Required scopes:**

- `meeting:read` OR `meeting:write` OR `meeting:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The meeting's ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/meetings.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "meeting": {
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
    "channel": "amazon_connect",
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "direction": "incoming",
    "ended_date": "2023-01-01T12:00:00.000Z",
    "external_ref": "string",
    "external_refs": [
      "string"
    ],
    "external_url": "string",
    "is_archived": true,
    "members": [
      {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    ],
    "organizer": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "parent": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "primary_meeting": {
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
      },
      "title": "string"
    },
    "recording": {
      "display_id": "string",
      "id": "string",
      "file": {
        "type": "string",
        "name": "string",
        "size": 0
      }
    },
    "recording_url": "string",
    "scheduled_date": "2023-01-01T12:00:00.000Z",
    "source_date": "2023-01-01T12:00:00.000Z",
    "state": "canceled",
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
    ],
    "title": "string",
    "transcript": {
      "display_id": "string",
      "id": "string",
      "file": {
        "type": "string",
        "name": "string",
        "size": 0
      }
    },
    "transcript_article": {
      "display_id": "string",
      "id": "string",
      "article_type": "article",
      "resource": {
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
        "url": "string"
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
      },
      "title": "string"
    },
    "visibility": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    }
  }
}
```

</details>


<a id="get-post"></a>

## `POST /meetings.get`

**Get Meeting (POST)**

Source: <https://developer.devrev.ai/api-reference/meetings/get-post>

Gets the meeting record.

**Required scopes:**

- `meeting:read` OR `meeting:write` OR `meeting:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The meeting's ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/meetings.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "meeting": {
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
    "channel": "amazon_connect",
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "direction": "incoming",
    "ended_date": "2023-01-01T12:00:00.000Z",
    "external_ref": "string",
    "external_refs": [
      "string"
    ],
    "external_url": "string",
    "is_archived": true,
    "members": [
      {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    ],
    "organizer": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "parent": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "primary_meeting": {
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
      },
      "title": "string"
    },
    "recording": {
      "display_id": "string",
      "id": "string",
      "file": {
        "type": "string",
        "name": "string",
        "size": 0
      }
    },
    "recording_url": "string",
    "scheduled_date": "2023-01-01T12:00:00.000Z",
    "source_date": "2023-01-01T12:00:00.000Z",
    "state": "canceled",
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
    ],
    "title": "string",
    "transcript": {
      "display_id": "string",
      "id": "string",
      "file": {
        "type": "string",
        "name": "string",
        "size": 0
      }
    },
    "transcript_article": {
      "display_id": "string",
      "id": "string",
      "article_type": "article",
      "resource": {
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
        "url": "string"
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
      },
      "title": "string"
    },
    "visibility": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    }
  }
}
```

</details>


<a id="list"></a>

## `GET /meetings.list`

**List Meetings**

Source: <https://developer.devrev.ai/api-reference/meetings/list>

Lists the meeting records.

**Required scopes:**

- `meeting:read` OR `meeting:write` OR `meeting:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `channel` | no | `array<meeting-channel>` | Filters for meeting on specified channels. |
| `created_by` | no | `array<string>` | Filters for meetings created by the specified user(s). |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for meeting on custom fields. |
| `direction` | no | `array<meeting-direction>` | Direction of the meetings to be fetched. |
| `external_ref` | no | `array<string>` | Filters for meetings with the provided external_ref(s). |
| `limit` | no | `integer` | The maximum number of meetings to return.<br>*Format: int32* |
| `links.link_type` | no | `string` | Filters for link type in links associated with the meeting.<br>*Format: text* |
| `links.target` | no | `string` | Filters for target id in links associated with the meeting.<br>*Format: id* |
| `links.target_object_type` | no | `string` | Filters for target object type in links associated with the meeting.<br>*Format: text* |
| `members` | no | `array<string>` | Filter for meeting on specified Member Ids. |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `organizer` | no | `array<string>` | Filter for meeting on specified organizers. |
| `parent` | no | `array<string>` | **Deprecated.**<br>Filters for meetings with the provided parent. |
| `sort_by` | no | `array<string>` | Fields to sort the meetings by and the direction to sort them. |
| `state` | no | `array<meeting-state>` | Filters for meeting on specified state or outcomes. |
| `subtype` | no | `array<string>` | Subtypes of meeting to be filtered. |
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
| `tags` | no | `array<string>` | Filters for meeting by tags. |

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
curl -X GET "https://api.devrev.ai/meetings.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "meetings": [
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
      "channel": "amazon_connect",
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "description": "string",
      "direction": "incoming",
      "ended_date": "2023-01-01T12:00:00.000Z",
      "external_ref": "string",
      "external_refs": [
        "string"
      ],
      "external_url": "string",
      "is_archived": true,
      "members": [
        {
          "type": "account",
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      ],
      "organizer": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "parent": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "primary_meeting": {
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
        },
        "title": "string"
      },
      "recording": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "recording_url": "string",
      "scheduled_date": "2023-01-01T12:00:00.000Z",
      "source_date": "2023-01-01T12:00:00.000Z",
      "state": "canceled",
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
      ],
      "title": "string",
      "transcript": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "transcript_article": {
        "display_id": "string",
        "id": "string",
        "article_type": "article",
        "resource": {
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
          "url": "string"
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
        },
        "title": "string"
      },
      "visibility": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      }
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="list-post"></a>

## `POST /meetings.list`

**List Meetings (POST)**

Source: <https://developer.devrev.ai/api-reference/meetings/list-post>

Lists the meeting records.

**Required scopes:**

- `meeting:read` OR `meeting:write` OR `meeting:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `channel` | no | `array<meeting-channel>` | Filters for meeting on specified channels. |
| `created_by` | no | `array<string>` | Filters for meetings created by the specified user(s). |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for meeting on custom fields. |
| `direction` | no | `array<meeting-direction>` | Direction of the meetings to be fetched. |
| `ended_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `external_ref` | no | `array<string>` | Filters for meetings with the provided external_ref(s). |
| `limit` | no | `integer` | The maximum number of meetings to return.<br>*Format: int32* |
| `links` | no | `array<meetings-filter-link-summary-filter>` | Filters for links associated with the meeting. |
| `members` | no | `array<string>` | Filter for meeting on specified Member Ids. |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `organizer` | no | `array<string>` | Filter for meeting on specified organizers. |
| `parent` | no | `array<string>` | **Deprecated.**<br>Filters for meetings with the provided parent. |
| `scheduled_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `sort_by` | no | `array<string>` | Fields to sort the meetings by and the direction to sort them. |
| `state` | no | `array<meeting-state>` | Filters for meeting on specified state or outcomes. |
| `subtype` | no | `array<string>` | Subtypes of meeting to be filtered. |
| `sync_metadata` | no | `sync-metadata-filter` |  |
| `tags` | no | `array<string>` | Filters for meeting by tags. |

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
curl -X POST "https://api.devrev.ai/meetings.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "meetings": [
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
      "channel": "amazon_connect",
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "description": "string",
      "direction": "incoming",
      "ended_date": "2023-01-01T12:00:00.000Z",
      "external_ref": "string",
      "external_refs": [
        "string"
      ],
      "external_url": "string",
      "is_archived": true,
      "members": [
        {
          "type": "account",
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      ],
      "organizer": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "parent": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "primary_meeting": {
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
        },
        "title": "string"
      },
      "recording": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "recording_url": "string",
      "scheduled_date": "2023-01-01T12:00:00.000Z",
      "source_date": "2023-01-01T12:00:00.000Z",
      "state": "canceled",
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
      ],
      "title": "string",
      "transcript": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "transcript_article": {
        "display_id": "string",
        "id": "string",
        "article_type": "article",
        "resource": {
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
          "url": "string"
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
        },
        "title": "string"
      },
      "visibility": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      }
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="update"></a>

## `POST /meetings.update`

**Update Meeting**

Source: <https://developer.devrev.ai/api-reference/meetings/update>

Updates the meeting record.

**Required scopes:**

- `meeting:write` OR `meeting:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `artifacts` | no | `meetings-update-request-artifact-ids` |  |
| `channel` | no | `string` | The channel of meeting.<br>*Value in: "amazon_connect" \| "google_meet" \| "offline" \| "other" \| "teams" \| "zoom"* |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | The description of the meeting.<br>*Format: text* |
| `ended_date` | no | `string\|null` | Updates the date and time when the meeting ended.<br>*Format: date-time* |
| `external_ref` | no | `string` | External Reference for the meeting.<br>*Format: text* |
| `external_url` | no | `string` | External URL for the meeting.<br>*Format: text* |
| `id` | yes | `string` | The meetings ID.<br>*Format: id* |
| `members` | no | `meetings-update-request-members` |  |
| `organizer` | no | `string` | The ID of the user who organized the meeting.<br>*Format: id* |
| `recording` | no | `string\|null` | The ID of the meeting's recording artifact.<br>*Format: id* |
| `recording_url` | no | `string` | The recording URL of the meeting.<br>*Format: text* |
| `scheduled_date` | no | `string\|null` | Updates the date and time when the meeting was scheduled.<br>*Format: date-time* |
| `state` | no | `string` | The state of meeting.<br>*Value in: "canceled" \| "completed" \| "no_show" \| "ongoing" \| "rejected" \| "rescheduled" \| "scheduled" \| "waiting"* |
| `tags` | no | `meetings-update-request-tags` |  |
| `title` | no | `string` | The title of the meeting.<br>*Format: text* |
| `transcript` | no | `string` | The ID of the artifact for the transcript of the meeting.<br>*Format: id* |
| `transcript_article` | no | `string` | The article for the transcript of the meeting.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/meetings.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "meeting": {
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
    "channel": "amazon_connect",
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "direction": "incoming",
    "ended_date": "2023-01-01T12:00:00.000Z",
    "external_ref": "string",
    "external_refs": [
      "string"
    ],
    "external_url": "string",
    "is_archived": true,
    "members": [
      {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    ],
    "organizer": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "parent": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "primary_meeting": {
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
      },
      "title": "string"
    },
    "recording": {
      "display_id": "string",
      "id": "string",
      "file": {
        "type": "string",
        "name": "string",
        "size": 0
      }
    },
    "recording_url": "string",
    "scheduled_date": "2023-01-01T12:00:00.000Z",
    "source_date": "2023-01-01T12:00:00.000Z",
    "state": "canceled",
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
    ],
    "title": "string",
    "transcript": {
      "display_id": "string",
      "id": "string",
      "file": {
        "type": "string",
        "name": "string",
        "size": 0
      }
    },
    "transcript_article": {
      "display_id": "string",
      "id": "string",
      "article_type": "article",
      "resource": {
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
        "url": "string"
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
      },
      "title": "string"
    },
    "visibility": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    }
  }
}
```

</details>
