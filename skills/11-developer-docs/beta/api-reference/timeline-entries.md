# Timeline Entries

Source: <https://developer.devrev.ai/beta/api-reference/timeline-entries>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/reactions.list` | [reactions-list](#reactions-list) |
| POST | `/reactions.list` | [reactions-list-post](#reactions-list-post) |
| POST | `/reactions.update` | [reactions-update](#reactions-update) |
| POST | `/timeline-entries.create` | [create](#create) |
| POST | `/timeline-entries.delete` | [delete](#delete) |
| GET | `/timeline-entries.get` | [get](#get) |
| POST | `/timeline-entries.get` | [get-post](#get-post) |
| GET | `/timeline-entries.list` | [list](#list) |
| POST | `/timeline-entries.list` | [list-post](#list-post) |
| POST | `/timeline-entries.update` | [update](#update) |

<a id="reactions-list"></a>

## `GET /reactions.list`

**List Reactions**

Source: <https://developer.devrev.ai/beta/api-reference/timeline-entries/reactions-list>

Lists the reactors for an object.

**Required scopes:** Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline).

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `object` | yes | `string` | The ID of the object to list reactors for.<br>*Format: id* |
| `cursor` | no | `string` | The cursor to resume iteration from, otherwise if not provided, then iteration starts from the beginning.<br>*Format: text* |
| `emoji` | no | `string` | The emoji to list the reactors for. This can be the short name of the emoji (e.g. "joy"), or the code point (e.g. "1f602"). If not provided, all reactions for the object are returned.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of reactors to return.<br>*Format: int32* |

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
curl -X GET "https://api.devrev.ai/reactions.list?object=don%3Acore%3Advrv-us-1%3Adevo%2Fexample%3Aticket%2F123%3Acomment%2Fcomment-id"
```

<details><summary>Example 200 response</summary>

```json
{
  "emojis": [
    "string"
  ],
  "next_cursor": "string",
  "reactors": [
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
  ]
}
```

</details>


<a id="reactions-list-post"></a>

## `POST /reactions.list`

**List Reactions (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/timeline-entries/reactions-list-post>

Lists the reactors for an object.

**Required scopes:** Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline).

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from, otherwise if not provided, then iteration starts from the beginning.<br>*Format: text* |
| `emoji` | no | `string` | The emoji to list the reactors for. This can be the short name of the emoji (e.g. "joy"), or the code point (e.g. "1f602"). If not provided, all reactions for the object are returned.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of reactors to return.<br>*Format: int32* |
| `object` | yes | `string` | The ID of the object to list reactors for.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/reactions.list" \
  -H "Content-Type: application/json" \
  -d '{
    "object": "don:core:dvrv-us-1:devo/example:ticket/123:comment/comment-id"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "emojis": [
    "string"
  ],
  "next_cursor": "string",
  "reactors": [
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
  ]
}
```

</details>


<a id="reactions-update"></a>

## `POST /reactions.update`

**Update Reaction**

Source: <https://developer.devrev.ai/beta/api-reference/timeline-entries/reactions-update>

Updates a reaction for an object.

**Required scopes:** Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline).

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `action` | yes | `string` | *Value in: "add" \| "remove"* |
| `emoji` | yes | `string` | The emoji for the reaction. This can be the short name of the emoji (e.g. "joy"), or the code point (e.g. "1f602").<br>*Format: text* |
| `object` | yes | `string` | The object to update the reaction for.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/reactions.update" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "add",
    "emoji": "string",
    "object": "don:core:dvrv-us-1:devo/example:ticket/123:comment/comment-id"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="create"></a>

## `POST /timeline-entries.create`

**Create Timeline Entry**

Source: <https://developer.devrev.ai/beta/api-reference/timeline-entries/create>

Creates a new entry on an object's timeline.

**Required scopes:** Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline).

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `timeline-entries-create-request-timeline-comment`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | yes | `string` | *Value in: "timeline_comment"* |
| `collections` | no | `array<timeline-entries-collection>` | The collection(s) that the entry belongs to, otherwise if not provided, then the entry's default collection is used. |
| `expires_at` | no | `string` | If set, then the entry is ephemeral and will be deleted after the provided time. The minimum value should be at least a minute more than the current timestamp.<br>*Format: date-time* |
| `labels` | no | `array<string>` | The labels to be associated with the entry.<br>*Length: 1 <= length <= 64*<br>*Items: items <= 16* |
| `object` | yes | `string` | The ID of the object to create the timeline entry for.<br>*Format: id* |
| `private_to` | no | `array<string>` | If the visibility of the entry is private, this specifies the users that the entry is private to. Note the creator is always implicitly included in this list. |
| `visibility` | no | `string` | The visibility of the entry. If 'private', then the entry is only visible to the creator, 'internal' is visible with the Dev organization, 'external' is visible to the Dev organzation and Rev users, and 'public' is visible to all. If not set, then the default visibility is 'external'.<br>*Value in: "external" \| "internal" \| "private" \| "public"* |
| `artifacts` | no | `array<string>` | The IDs of the artifacts attached to the comment.<br>*Items: items <= 50* |
| `body` | no | `string` | The comment's body.<br>*Format: text* |
| `body_type` | no | `string` | The type of the body to use for the comment.<br>*Value in: "data" \| "snap_kit" \| "snap_widget" \| "text"* |
| `external_ref` | no | `string` | The external reference for the comment. This must be unique within the object's timeline.<br>*Format: text*<br>*Length: 1 <= length <= 512* |
| `in_reply_to` | no | `string` | The comment this comment is in reply to.<br>*Format: id* |
| `link_previews` | no | `array<string>` | The IDs of the previews of the links posted in the comment. |
| `snap_kit_body` | no | `timeline-snap-kit-body` | Snap Kit Body of the comment. |
| `snap_widget_body` | no | `array<string>` | The snap widget body of the comment. |

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
curl -X POST "https://api.devrev.ai/timeline-entries.create" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "timeline_comment",
    "object": "PROD-12345"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "timeline_entry": {
    "type": "timeline_change_event",
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
    "external_ref": "string",
    "labels": [
      "string"
    ],
    "object": "string",
    "object_display_id": "string",
    "object_type": "account",
    "panels": [
      "alerts"
    ],
    "reactions": [
      {
        "emoji": "string",
        "reacted": true,
        "total_users": 0
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
    },
    "thread": {
      "total_replies": 0
    },
    "visibility": "external",
    "event": {
      "type": "annotated",
      "created": {
        "object": {
          "type": "account",
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      },
      "deleted": {
        "object_id": "string"
      },
      "linked": {
        "link": {
          "display_id": "string",
          "id": "string",
          "link_type": "custom_link",
          "source": {
            "type": "account",
            "display_id": "string",
            "id": "string",
            "display_name": "string"
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
          "target": {
            "type": "account",
            "display_id": "string",
            "id": "string",
            "display_name": "string"
          }
        }
      },
      "updated": {
        "field_deltas": [
          {
            "field_descriptor": {
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
            },
            "name": "string",
            "new_value": {
              "type": "bool",
              "display_value": "string",
              "value": true
            },
            "old_value": {
              "type": "bool",
              "display_value": "string",
              "value": true
            }
          }
        ],
        "object_type": "string"
      }
    }
  }
}
```

</details>


<a id="delete"></a>

## `POST /timeline-entries.delete`

**Delete Timeline Entry**

Source: <https://developer.devrev.ai/beta/api-reference/timeline-entries/delete>

Deletes an entry from an object's timeline.

**Required scopes:** Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline).

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the timeline entry to delete.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/timeline-entries.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "don:core:dvrv-us-1:devo/example:ticket/123:comment/comment-id"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="get"></a>

## `GET /timeline-entries.get`

**Get Timeline Entry**

Source: <https://developer.devrev.ai/beta/api-reference/timeline-entries/get>

Gets an entry on an object's timeline.

**Required scopes:** Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline).

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the timeline entry to get.<br>*Format: id* |
| `external_ref` | no | `string` | If set, then gets the entry with the given external reference for the provided entry ID's timeline.<br>*Format: text*<br>*Length: 1 <= length <= 512* |

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
curl -X GET "https://api.devrev.ai/timeline-entries.get?id=don%3Acore%3Advrv-us-1%3Adevo%2Fexample%3Aticket%2F123%3Acomment%2Fcomment-id"
```

<details><summary>Example 200 response</summary>

```json
{
  "timeline_entry": {
    "type": "timeline_change_event",
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
    "external_ref": "string",
    "labels": [
      "string"
    ],
    "object": "string",
    "object_display_id": "string",
    "object_type": "account",
    "panels": [
      "alerts"
    ],
    "reactions": [
      {
        "emoji": "string",
        "reacted": true,
        "total_users": 0
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
    },
    "thread": {
      "total_replies": 0
    },
    "visibility": "external",
    "event": {
      "type": "annotated",
      "created": {
        "object": {
          "type": "account",
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      },
      "deleted": {
        "object_id": "string"
      },
      "linked": {
        "link": {
          "display_id": "string",
          "id": "string",
          "link_type": "custom_link",
          "source": {
            "type": "account",
            "display_id": "string",
            "id": "string",
            "display_name": "string"
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
          "target": {
            "type": "account",
            "display_id": "string",
            "id": "string",
            "display_name": "string"
          }
        }
      },
      "updated": {
        "field_deltas": [
          {
            "field_descriptor": {
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
            },
            "name": "string",
            "new_value": {
              "type": "bool",
              "display_value": "string",
              "value": true
            },
            "old_value": {
              "type": "bool",
              "display_value": "string",
              "value": true
            }
          }
        ],
        "object_type": "string"
      }
    }
  }
}
```

</details>


<a id="get-post"></a>

## `POST /timeline-entries.get`

**Get Timeline Entry (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/timeline-entries/get-post>

Gets an entry on an object's timeline.

**Required scopes:** Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline).

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `external_ref` | no | `string` | If set, then gets the entry with the given external reference for the provided entry ID's timeline.<br>*Format: text*<br>*Length: 1 <= length <= 512* |
| `id` | yes | `string` | The ID of the timeline entry to get.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/timeline-entries.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "don:core:dvrv-us-1:devo/example:ticket/123:comment/comment-id"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "timeline_entry": {
    "type": "timeline_change_event",
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
    "external_ref": "string",
    "labels": [
      "string"
    ],
    "object": "string",
    "object_display_id": "string",
    "object_type": "account",
    "panels": [
      "alerts"
    ],
    "reactions": [
      {
        "emoji": "string",
        "reacted": true,
        "total_users": 0
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
    },
    "thread": {
      "total_replies": 0
    },
    "visibility": "external",
    "event": {
      "type": "annotated",
      "created": {
        "object": {
          "type": "account",
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      },
      "deleted": {
        "object_id": "string"
      },
      "linked": {
        "link": {
          "display_id": "string",
          "id": "string",
          "link_type": "custom_link",
          "source": {
            "type": "account",
            "display_id": "string",
            "id": "string",
            "display_name": "string"
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
          "target": {
            "type": "account",
            "display_id": "string",
            "id": "string",
            "display_name": "string"
          }
        }
      },
      "updated": {
        "field_deltas": [
          {
            "field_descriptor": {
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
            },
            "name": "string",
            "new_value": {
              "type": "bool",
              "display_value": "string",
              "value": true
            },
            "old_value": {
              "type": "bool",
              "display_value": "string",
              "value": true
            }
          }
        ],
        "object_type": "string"
      }
    }
  }
}
```

</details>


<a id="list"></a>

## `GET /timeline-entries.list`

**List Timeline Entries**

Source: <https://developer.devrev.ai/beta/api-reference/timeline-entries/list>

Lists the timeline entries for an object.

**Required scopes:** Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline).

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `object` | yes | `string` | The ID of the object to list timeline entries for.<br>*Format: id* |
| `bias` | no | `string` | The bias for request processing. The default is 'speed'.<br>*Value in: "quantity" \| "speed"* |
| `collections` | no | `array<timeline-entries-collection>` | The collection(s) to list entries from, otherwise if not provided, all entries are returned.<br>*Items: items <= 1* |
| `created_by` | no | `array<string>` | Filters for entries created by any of the provided users. |
| `created_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `created_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `labels` | no | `array<string>` | Filters for entries containing at least one of the provided labels, otherwise if no labels are provided, then no label filtering is done.<br>*Length: 1 <= length <= 64* |
| `limit` | no | `integer` | The maximum number of entries to return. Note that fewer (possibly zero) entries may be returned even if there are more entries, where the returned cursor(s) are guaranteed to be updated.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `panels` | no | `array<timeline-entry-panel>` | Filters for entries to be displayed on the provided panel(s). |
| `visibility` | no | `array<timeline-entry-visibility>` | The visibility of the timeline entries to filter for. Note this is a strict filter, such that only entries with the exact visibilities specified will be returned. |

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
curl -X GET "https://api.devrev.ai/timeline-entries.list?object=PROD-12345"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "timeline_entries": [
    {
      "type": "timeline_change_event",
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
      "external_ref": "string",
      "labels": [
        "string"
      ],
      "object": "string",
      "object_display_id": "string",
      "object_type": "account",
      "panels": [
        "alerts"
      ],
      "reactions": [
        {
          "emoji": "string",
          "reacted": true,
          "total_users": 0
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
      },
      "thread": {
        "total_replies": 0
      },
      "visibility": "external",
      "event": {
        "type": "annotated",
        "created": {
          "object": {
            "type": "account",
            "display_id": "string",
            "id": "string",
            "display_name": "string"
          }
        },
        "deleted": {
          "object_id": "string"
        },
        "linked": {
          "link": {
            "display_id": "string",
            "id": "string",
            "link_type": "custom_link",
            "source": {
              "type": "account",
              "display_id": "string",
              "id": "string",
              "display_name": "string"
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
            "target": {
              "type": "account",
              "display_id": "string",
              "id": "string",
              "display_name": "string"
            }
          }
        },
        "updated": {
          "field_deltas": [
            {
              "field_descriptor": {
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
              },
              "name": "string",
              "new_value": {
                "type": "bool",
                "display_value": "string",
                "value": true
              },
              "old_value": {
                "type": "bool",
                "display_value": "string",
                "value": true
              }
            }
          ],
          "object_type": "string"
        }
      }
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /timeline-entries.list`

**List Timeline Entries (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/timeline-entries/list-post>

Lists the timeline entries for an object.

**Required scopes:** Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline).

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `bias` | no | `string` | *Value in: "quantity" \| "speed"* |
| `collections` | no | `array<timeline-entries-collection>` | The collection(s) to list entries from, otherwise if not provided, all entries are returned.<br>*Items: items <= 1* |
| `created_by` | no | `array<string>` | Filters for entries created by any of the provided users. |
| `created_date` | no | `date-time-filter` |  |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `labels` | no | `array<string>` | Filters for entries containing at least one of the provided labels, otherwise if no labels are provided, then no label filtering is done.<br>*Length: 1 <= length <= 64* |
| `limit` | no | `integer` | The maximum number of entries to return. Note that fewer (possibly zero) entries may be returned even if there are more entries, where the returned cursor(s) are guaranteed to be updated.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `object` | yes | `string` | The ID of the object to list timeline entries for.<br>*Format: id* |
| `panels` | no | `array<timeline-entry-panel>` | Filters for entries to be displayed on the provided panel(s). |
| `visibility` | no | `array<timeline-entry-visibility>` | The visibility of the timeline entries to filter for. Note this is a strict filter, such that only entries with the exact visibilities specified will be returned. |

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
curl -X POST "https://api.devrev.ai/timeline-entries.list" \
  -H "Content-Type: application/json" \
  -d '{
    "object": "PROD-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "timeline_entries": [
    {
      "type": "timeline_change_event",
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
      "external_ref": "string",
      "labels": [
        "string"
      ],
      "object": "string",
      "object_display_id": "string",
      "object_type": "account",
      "panels": [
        "alerts"
      ],
      "reactions": [
        {
          "emoji": "string",
          "reacted": true,
          "total_users": 0
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
      },
      "thread": {
        "total_replies": 0
      },
      "visibility": "external",
      "event": {
        "type": "annotated",
        "created": {
          "object": {
            "type": "account",
            "display_id": "string",
            "id": "string",
            "display_name": "string"
          }
        },
        "deleted": {
          "object_id": "string"
        },
        "linked": {
          "link": {
            "display_id": "string",
            "id": "string",
            "link_type": "custom_link",
            "source": {
              "type": "account",
              "display_id": "string",
              "id": "string",
              "display_name": "string"
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
            "target": {
              "type": "account",
              "display_id": "string",
              "id": "string",
              "display_name": "string"
            }
          }
        },
        "updated": {
          "field_deltas": [
            {
              "field_descriptor": {
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
              },
              "name": "string",
              "new_value": {
                "type": "bool",
                "display_value": "string",
                "value": true
              },
              "old_value": {
                "type": "bool",
                "display_value": "string",
                "value": true
              }
            }
          ],
          "object_type": "string"
        }
      }
    }
  ]
}
```

</details>


<a id="update"></a>

## `POST /timeline-entries.update`

**Update Timeline Entry**

Source: <https://developer.devrev.ai/beta/api-reference/timeline-entries/update>

Updates an entry on an object's timeline.

**Required scopes:** Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline).

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `timeline-entries-update-request-timeline-comment`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | yes | `string` | *Value in: "timeline_comment"* |
| `id` | yes | `string` | The ID of the timeline entry to update.<br>*Format: id* |
| `artifacts` | no | `timeline-entries-update-request-timeline-comment-artifacts` |  |
| `body` | no | `string` | The updated comment's body.<br>*Format: text* |
| `body_type` | no | `string` | The type of the body to use for the comment.<br>*Value in: "data" \| "snap_kit" \| "snap_widget" \| "text"* |
| `external_ref` | no | `string\|null` | The updated external reference for the comment. If set, this must be unique within the object's timeline, otherwise if null, then clears the value.<br>*Format: text*<br>*Length: 1 <= length <= 512* |
| `link_previews` | no | `timeline-entries-update-request-timeline-comment-link-previews` |  |
| `snap_kit_body` | no | `timeline-snap-kit-body` | Snap Kit Body of the comment. |

### Response codes

- `200` — `application/json`
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
curl -X POST "https://api.devrev.ai/timeline-entries.update" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "timeline_comment",
    "id": "don:core:dvrv-us-1:devo/example:ticket/123:comment/comment-id"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "timeline_entry": {
    "type": "timeline_change_event",
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
    "external_ref": "string",
    "labels": [
      "string"
    ],
    "object": "string",
    "object_display_id": "string",
    "object_type": "account",
    "panels": [
      "alerts"
    ],
    "reactions": [
      {
        "emoji": "string",
        "reacted": true,
        "total_users": 0
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
    },
    "thread": {
      "total_replies": 0
    },
    "visibility": "external",
    "event": {
      "type": "annotated",
      "created": {
        "object": {
          "type": "account",
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      },
      "deleted": {
        "object_id": "string"
      },
      "linked": {
        "link": {
          "display_id": "string",
          "id": "string",
          "link_type": "custom_link",
          "source": {
            "type": "account",
            "display_id": "string",
            "id": "string",
            "display_name": "string"
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
          "target": {
            "type": "account",
            "display_id": "string",
            "id": "string",
            "display_name": "string"
          }
        }
      },
      "updated": {
        "field_deltas": [
          {
            "field_descriptor": {
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
            },
            "name": "string",
            "new_value": {
              "type": "bool",
              "display_value": "string",
              "value": true
            },
            "old_value": {
              "type": "bool",
              "display_value": "string",
              "value": true
            }
          }
        ],
        "object_type": "string"
      }
    }
  }
}
```

</details>
