# Conversations

Source: <https://developer.devrev.ai/api-reference/conversations>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/conversations.create` | [create](#create) |
| POST | `/conversations.delete` | [delete](#delete) |
| GET | `/conversations.get` | [get](#get) |
| POST | `/conversations.get` | [get-post](#get-post) |
| GET | `/conversations.list` | [list](#list) |
| POST | `/conversations.list` | [list-post](#list-post) |
| POST | `/conversations.update` | [update](#update) |

<a id="create"></a>

## `POST /conversations.create`

**Create Conversation**

Source: <https://developer.devrev.ai/api-reference/conversations/create>

Creates a conversation.

**Required scopes:**

- `conversation:write` OR `conversation:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | yes | `string` | *Value in: "support"* |
| `account` | no | `string` | The account associated with the conversation.<br>*Format: id* |
| `ai_resolution_status` | no | `integer` | The AI resolution status enum ID for the conversation. Stock allowed values:<br>```<br>  {<br>    "id": 1,<br>    "label": "deflected",<br>    "ordinal": 1,<br>    "overridable": false<br>  },<br>  {<br>    "id": 2,<br>    "label": "escalated",<br>    "ordinal": 2,<br>    "overridable": false<br>  }<br>```<br>*Format: int64* |
| `brand` | no | `string` | The brand associated with the conversation.<br>*Format: id* |
| `channels` | no | `array<string>` | Channel IDs of the conversation. |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | Description for the conversation.<br>*Format: text* |
| `group` | no | `string` | The group that the conversation is associated with.<br>*Format: id* |
| `is_spam` | no | `boolean` | Whether the conversation is spam. |
| `members` | no | `array<string>` | The users in the conversation. |
| `messages` | no | `array<conversations-create-request-message>` | Initial messages on the conversation. |
| `metadata` | no | `conversations-create-request-metadata` |  |
| `owned_by` | no | `array<string>` | The users that own the conversation. |
| `owned_by_agent` | no | `string` | The ID of the AI agent that owns the conversation.<br>*Format: id* |
| `source_channel` | no | `string` | Whether the conversation is from a source channel.<br>*Format: text* |
| `source_channel_v2` | no | `string` | Source channel ID of the conversation.<br>*Format: id* |
| `stage` | no | `stage-init` | Sets an object's initial stage. |
| `tags` | no | `array<set-tag-with-value>` | Tags associated with the conversation. |
| `title` | no | `string` | The title for the conversation.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/conversations.create" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "support"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "conversation": {
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
    "account": {
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "actual_close_date": "2023-01-01T12:00:00.000Z",
    "ai_resolution_status": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
    "applies_to_parts": [
      {
        "type": "capability",
        "display_id": "string",
        "id": "string",
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
    ],
    "channels": [
      {
        "display_id": "string",
        "id": "string"
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "group": {
      "display_id": "string",
      "id": "string",
      "member_type": "dev_user",
      "name": "string",
      "parents": [
        "string"
      ],
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
    "is_frozen": true,
    "last_external_message_date": "2023-01-01T12:00:00.000Z",
    "members": [
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
    "messages": [
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
    ],
    "metadata": {
      "url_context": "string"
    },
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
    "sentiment": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
    "sentiment_modified_date": "2023-01-01T12:00:00.000Z",
    "sentiment_summary": "string",
    "sla_summary": {
      "closest_to_breach_metric": "string",
      "org_schedule": {
        "display_id": "string",
        "id": "string",
        "name": "string",
        "status": "archived",
        "timezone": "string",
        "valid_until": "2023-01-01T12:00:00.000Z",
        "version_number": 0
      },
      "remaining_time": 0,
      "sla_tracker": {
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
        "applies_to_id": "string",
        "applies_to_type": "conversation",
        "metric_target_summaries": [
          {
            "breached_at": "2023-01-01T12:00:00.000Z",
            "completed_at": "2023-01-01T12:00:00.000Z",
            "completed_in": 0,
            "completed_in_seconds": 0,
            "in_policy": true,
            "is_out_of_schedule": true,
            "metric_definition": {
              "display_id": "string",
              "id": "string",
              "name": "string"
            },
            "next_schedule_transition": "2023-01-01T12:00:00.000Z",
            "org_schedule": {
              "display_id": "string",
              "id": "string",
              "name": "string",
              "status": "archived",
              "timezone": "string",
              "valid_until": "2023-01-01T12:00:00.000Z",
              "version_number": 0
            },
            "org_schedule_version": 0,
            "remaining_time": 0,
            "stage": "string",
            "status": "string",
            "target_time": "2023-01-01T12:00:00.000Z",
            "warning_target_time": "2023-01-01T12:00:00.000Z"
          }
        ],
        "removed_sla_metric_history": [
          {
            "metric_definition": {
              "display_id": "string",
              "id": "string",
              "name": "string"
            },
            "removed_at": "2023-01-01T12:00:00.000Z",
            "removed_by": {
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
          }
        ],
        "sla": {
          "display_id": "string",
          "id": "string",
          "name": "string",
          "sla_type": "external",
          "status": "archived"
        },
        "sla_policy_id": "string",
        "stage": "string",
        "status": "string"
      },
      "stage": "breached",
      "target_time": "2023-01-01T12:00:00.000Z"
    },
    "sla_tracker": {
      "display_id": "string",
      "id": "string",
      "applies_to_type": "conversation"
    },
    "source_channel": "string",
    "source_channel_v2": {
      "display_id": "string",
      "id": "string"
    },
    "stage": {
      "name": "string",
      "notes": "string",
      "ordinal": 0,
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
    "title": "string"
  }
}
```

</details>


<a id="delete"></a>

## `POST /conversations.delete`

**Delete Conversation**

Source: <https://developer.devrev.ai/api-reference/conversations/delete>

Deletes the requested conversation.

**Required scopes:**

- `conversation:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the conversation to delete.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/conversations.delete" \
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

## `GET /conversations.get`

**Get Conversation**

Source: <https://developer.devrev.ai/api-reference/conversations/get>

Gets the requested conversation's information.

**Required scopes:**

- `conversation:read` OR `conversation:write` OR `conversation:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The requested conversation's ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/conversations.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "conversation": {
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
    "account": {
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "actual_close_date": "2023-01-01T12:00:00.000Z",
    "ai_resolution_status": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
    "applies_to_parts": [
      {
        "type": "capability",
        "display_id": "string",
        "id": "string",
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
    ],
    "channels": [
      {
        "display_id": "string",
        "id": "string"
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "group": {
      "display_id": "string",
      "id": "string",
      "member_type": "dev_user",
      "name": "string",
      "parents": [
        "string"
      ],
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
    "is_frozen": true,
    "last_external_message_date": "2023-01-01T12:00:00.000Z",
    "members": [
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
    "messages": [
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
    ],
    "metadata": {
      "url_context": "string"
    },
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
    "sentiment": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
    "sentiment_modified_date": "2023-01-01T12:00:00.000Z",
    "sentiment_summary": "string",
    "sla_summary": {
      "closest_to_breach_metric": "string",
      "org_schedule": {
        "display_id": "string",
        "id": "string",
        "name": "string",
        "status": "archived",
        "timezone": "string",
        "valid_until": "2023-01-01T12:00:00.000Z",
        "version_number": 0
      },
      "remaining_time": 0,
      "sla_tracker": {
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
        "applies_to_id": "string",
        "applies_to_type": "conversation",
        "metric_target_summaries": [
          {
            "breached_at": "2023-01-01T12:00:00.000Z",
            "completed_at": "2023-01-01T12:00:00.000Z",
            "completed_in": 0,
            "completed_in_seconds": 0,
            "in_policy": true,
            "is_out_of_schedule": true,
            "metric_definition": {
              "display_id": "string",
              "id": "string",
              "name": "string"
            },
            "next_schedule_transition": "2023-01-01T12:00:00.000Z",
            "org_schedule": {
              "display_id": "string",
              "id": "string",
              "name": "string",
              "status": "archived",
              "timezone": "string",
              "valid_until": "2023-01-01T12:00:00.000Z",
              "version_number": 0
            },
            "org_schedule_version": 0,
            "remaining_time": 0,
            "stage": "string",
            "status": "string",
            "target_time": "2023-01-01T12:00:00.000Z",
            "warning_target_time": "2023-01-01T12:00:00.000Z"
          }
        ],
        "removed_sla_metric_history": [
          {
            "metric_definition": {
              "display_id": "string",
              "id": "string",
              "name": "string"
            },
            "removed_at": "2023-01-01T12:00:00.000Z",
            "removed_by": {
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
          }
        ],
        "sla": {
          "display_id": "string",
          "id": "string",
          "name": "string",
          "sla_type": "external",
          "status": "archived"
        },
        "sla_policy_id": "string",
        "stage": "string",
        "status": "string"
      },
      "stage": "breached",
      "target_time": "2023-01-01T12:00:00.000Z"
    },
    "sla_tracker": {
      "display_id": "string",
      "id": "string",
      "applies_to_type": "conversation"
    },
    "source_channel": "string",
    "source_channel_v2": {
      "display_id": "string",
      "id": "string"
    },
    "stage": {
      "name": "string",
      "notes": "string",
      "ordinal": 0,
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
    "title": "string"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /conversations.get`

**Get Conversation (POST)**

Source: <https://developer.devrev.ai/api-reference/conversations/get-post>

Gets the requested conversation's information.

**Required scopes:**

- `conversation:read` OR `conversation:write` OR `conversation:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The requested conversation's ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/conversations.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "conversation": {
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
    "account": {
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "actual_close_date": "2023-01-01T12:00:00.000Z",
    "ai_resolution_status": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
    "applies_to_parts": [
      {
        "type": "capability",
        "display_id": "string",
        "id": "string",
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
    ],
    "channels": [
      {
        "display_id": "string",
        "id": "string"
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "group": {
      "display_id": "string",
      "id": "string",
      "member_type": "dev_user",
      "name": "string",
      "parents": [
        "string"
      ],
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
    "is_frozen": true,
    "last_external_message_date": "2023-01-01T12:00:00.000Z",
    "members": [
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
    "messages": [
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
    ],
    "metadata": {
      "url_context": "string"
    },
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
    "sentiment": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
    "sentiment_modified_date": "2023-01-01T12:00:00.000Z",
    "sentiment_summary": "string",
    "sla_summary": {
      "closest_to_breach_metric": "string",
      "org_schedule": {
        "display_id": "string",
        "id": "string",
        "name": "string",
        "status": "archived",
        "timezone": "string",
        "valid_until": "2023-01-01T12:00:00.000Z",
        "version_number": 0
      },
      "remaining_time": 0,
      "sla_tracker": {
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
        "applies_to_id": "string",
        "applies_to_type": "conversation",
        "metric_target_summaries": [
          {
            "breached_at": "2023-01-01T12:00:00.000Z",
            "completed_at": "2023-01-01T12:00:00.000Z",
            "completed_in": 0,
            "completed_in_seconds": 0,
            "in_policy": true,
            "is_out_of_schedule": true,
            "metric_definition": {
              "display_id": "string",
              "id": "string",
              "name": "string"
            },
            "next_schedule_transition": "2023-01-01T12:00:00.000Z",
            "org_schedule": {
              "display_id": "string",
              "id": "string",
              "name": "string",
              "status": "archived",
              "timezone": "string",
              "valid_until": "2023-01-01T12:00:00.000Z",
              "version_number": 0
            },
            "org_schedule_version": 0,
            "remaining_time": 0,
            "stage": "string",
            "status": "string",
            "target_time": "2023-01-01T12:00:00.000Z",
            "warning_target_time": "2023-01-01T12:00:00.000Z"
          }
        ],
        "removed_sla_metric_history": [
          {
            "metric_definition": {
              "display_id": "string",
              "id": "string",
              "name": "string"
            },
            "removed_at": "2023-01-01T12:00:00.000Z",
            "removed_by": {
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
          }
        ],
        "sla": {
          "display_id": "string",
          "id": "string",
          "name": "string",
          "sla_type": "external",
          "status": "archived"
        },
        "sla_policy_id": "string",
        "stage": "string",
        "status": "string"
      },
      "stage": "breached",
      "target_time": "2023-01-01T12:00:00.000Z"
    },
    "sla_tracker": {
      "display_id": "string",
      "id": "string",
      "applies_to_type": "conversation"
    },
    "source_channel": "string",
    "source_channel_v2": {
      "display_id": "string",
      "id": "string"
    },
    "stage": {
      "name": "string",
      "notes": "string",
      "ordinal": 0,
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
    "title": "string"
  }
}
```

</details>


<a id="list"></a>

## `GET /conversations.list`

**List Conversations**

Source: <https://developer.devrev.ai/api-reference/conversations/list>

Lists the available conversations.

**Required scopes:**

- `conversation:read` OR `conversation:write` OR `conversation:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `account` | no | `array<string>` | Filters for conversations that are associated with any of the accounts. |
| `ai_resolution_status` | no | `array<integer>` | Filters for conversations with any of the provided AI resolution statuses. |
| `applies_to_parts` | no | `array<string>` | Filters for conversations belonging to any of the provided parts. |
| `brand` | no | `array<string>` | Filters for tickets that are associated with any of the brands. |
| `channels` | no | `array<string>` | Filters for conversations that are associated with any of the channels. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `group` | no | `array<string>` | Filters for conversation that belong to the given groups. |
| `is_creator_verified` | no | `boolean` | Filters for conversations that are created by verified users. |
| `is_frozen` | no | `boolean` | Filters for conversations that are frozen. |
| `is_spam` | no | `boolean` | Filters for conversations that are spam. |
| `limit` | no | `integer` | The maximum number of conversations to return. The default is '50'.<br>*Format: int32* |
| `members` | no | `array<string>` | Filters for conversations where these users are participants. |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `modified_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `modified_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `owned_by` | no | `array<string>` | Filters for conversations owned by any of these users. |
| `owned_by_agent` | no | `array<string>` | Filters for conversations owned by any of the AI agents. |
| `rev_org` | no | `array<string>` | **Deprecated.**<br>Filters for conversations that are associated with any of the provided Rev organizations. |
| `rev_orgs` | no | `array<string>` | Filters for conversations that are associated with any of the provided Rev organizations. |
| `sla_summary.stage` | no | `array<sla-summary-stage>` | Filters for records with any of the provided SLA stages. |
| `sort_by` | no | `array<string>` | Fields to sort the conversations by and the direction to sort them. |
| `source_channel` | no | `array<string>` | Filters for conversations with any of the provided source channels. |
| `source_channel_v2` | no | `array<string>` | Filters for conversations that are associated with the source channel. |
| `source_channels` | no | `array<string>` | **Deprecated.**<br>Filters for conversations with any of the provided source channels. |
| `stage.name` | no | `array<string>` | Filters for records in the provided stage(s) by name. |
| `stage.stages` | no | `array<string>` | List of IDs of the custom stages which will be used for filtering. |
| `state` | no | `array<string>` | Filters for conversations with any of the provided states. |
| `subtype` | no | `array<string>` | Filters for conversation with any of the provided subtypes. |
| `tags` | no | `array<string>` | **Deprecated.**<br>Filters for conversations with any of the provided tags. |
| `tags_v2.id` | no | `string` | The ID of the tag.<br>*Format: id* |
| `tags_v2.value` | no | `string` | The value for the object's association with the tag. If specified, the value must be one that's specified in the tag's allowed values.<br>*Format: text* |

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
curl -X GET "https://api.devrev.ai/conversations.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "conversations": [
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
      "account": {
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "actual_close_date": "2023-01-01T12:00:00.000Z",
      "ai_resolution_status": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "applies_to_parts": [
        {
          "type": "capability",
          "display_id": "string",
          "id": "string",
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
      ],
      "channels": [
        {
          "display_id": "string",
          "id": "string"
        }
      ],
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "description": "string",
      "group": {
        "display_id": "string",
        "id": "string",
        "member_type": "dev_user",
        "name": "string",
        "parents": [
          "string"
        ],
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
      "is_frozen": true,
      "last_external_message_date": "2023-01-01T12:00:00.000Z",
      "members": [
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
      "messages": [
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
                            {}
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
      ],
      "metadata": {
        "url_context": "string"
      },
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
      "sentiment": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "sentiment_modified_date": "2023-01-01T12:00:00.000Z",
      "sentiment_summary": "string",
      "sla_summary": {
        "closest_to_breach_metric": "string",
        "org_schedule": {
          "display_id": "string",
          "id": "string",
          "name": "string",
          "status": "archived",
          "timezone": "string",
          "valid_until": "2023-01-01T12:00:00.000Z",
          "version_number": 0
        },
        "remaining_time": 0,
        "sla_tracker": {
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
          "applies_to_id": "string",
          "applies_to_type": "conversation",
          "metric_target_summaries": [
            {
              "breached_at": "2023-01-01T12:00:00.000Z",
              "completed_at": "2023-01-01T12:00:00.000Z",
              "completed_in": 0,
              "completed_in_seconds": 0,
              "in_policy": true,
              "is_out_of_schedule": true,
              "metric_definition": {
                "display_id": "string",
                "id": "string",
                "name": "string"
              },
              "next_schedule_transition": "2023-01-01T12:00:00.000Z",
              "org_schedule": {
                "display_id": "string",
                "id": "string",
                "name": "string",
                "status": "archived",
                "timezone": "string",
                "valid_until": "2023-01-01T12:00:00.000Z",
                "version_number": 0
              },
              "org_schedule_version": 0,
              "remaining_time": 0,
              "stage": "string",
              "status": "string",
              "target_time": "2023-01-01T12:00:00.000Z",
              "warning_target_time": "2023-01-01T12:00:00.000Z"
            }
          ],
          "removed_sla_metric_history": [
            {
              "metric_definition": {
                "display_id": "string",
                "id": "string",
                "name": "string"
              },
              "removed_at": "2023-01-01T12:00:00.000Z",
              "removed_by": {
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
            }
          ],
          "sla": {
            "display_id": "string",
            "id": "string",
            "name": "string",
            "sla_type": "external",
            "status": "archived"
          },
          "sla_policy_id": "string",
          "stage": "string",
          "status": "string"
        },
        "stage": "breached",
        "target_time": "2023-01-01T12:00:00.000Z"
      },
      "sla_tracker": {
        "display_id": "string",
        "id": "string",
        "applies_to_type": "conversation"
      },
      "source_channel": "string",
      "source_channel_v2": {
        "display_id": "string",
        "id": "string"
      },
      "stage": {
        "name": "string",
        "notes": "string",
        "ordinal": 0,
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
      "title": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="list-post"></a>

## `POST /conversations.list`

**List Conversations (POST)**

Source: <https://developer.devrev.ai/api-reference/conversations/list-post>

Lists the available conversations.

**Required scopes:**

- `conversation:read` OR `conversation:write` OR `conversation:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `account` | no | `array<string>` | Filters for conversations that are associated with any of the accounts. |
| `actual_close_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `ai_resolution_status` | no | `array<integer>` | Filters for conversations with any of the provided AI resolution statuses. |
| `applies_to_parts` | no | `array<string>` | Filters for conversations belonging to any of the provided parts. |
| `brand` | no | `array<string>` | Filters for tickets that are associated with any of the brands. |
| `channels` | no | `array<string>` | Filters for conversations that are associated with any of the channels. |
| `created_date_new` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `group` | no | `array<string>` | Filters for conversation that belong to the given groups. |
| `is_creator_verified` | no | `boolean` | Filters for conversations that are created by verified users. |
| `is_frozen` | no | `boolean` | Filters for conversations that are frozen. |
| `is_spam` | no | `boolean` | Filters for conversations that are spam. |
| `limit` | no | `integer` | The maximum number of conversations to return. The default is '50'.<br>*Format: int32* |
| `members` | no | `array<string>` | Filters for conversations where these users are participants. |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter` |  |
| `owned_by` | no | `array<string>` | Filters for conversations owned by any of these users. |
| `owned_by_agent` | no | `array<string>` | Filters for conversations owned by any of the AI agents. |
| `rev_org` | no | `array<string>` | **Deprecated.**<br>Filters for conversations that are associated with any of the provided Rev organizations. |
| `rev_orgs` | no | `array<string>` | Filters for conversations that are associated with any of the provided Rev organizations. |
| `sla_summary` | no | `sla-summary-filter` | The filter for SLA summary. |
| `sort_by` | no | `array<string>` | Fields to sort the conversations by and the direction to sort them. |
| `source_channel` | no | `array<string>` | Filters for conversations with any of the provided source channels. |
| `source_channel_v2` | no | `array<string>` | Filters for conversations that are associated with the source channel. |
| `source_channels` | no | `array<string>` | **Deprecated.**<br>Filters for conversations with any of the provided source channels. |
| `stage` | no | `stage-filter` | The filter for stages. |
| `state` | no | `array<string>` | Filters for conversations with any of the provided states. |
| `subtype` | no | `array<string>` | Filters for conversation with any of the provided subtypes. |
| `tags` | no | `array<string>` | **Deprecated.**<br>Filters for conversations with any of the provided tags. |
| `tags_v2` | no | `array<tag-with-value-filter>` | Filters for conversations with any of the provided tags with value. |

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
curl -X POST "https://api.devrev.ai/conversations.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "conversations": [
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
      "account": {
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "actual_close_date": "2023-01-01T12:00:00.000Z",
      "ai_resolution_status": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "applies_to_parts": [
        {
          "type": "capability",
          "display_id": "string",
          "id": "string",
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
      ],
      "channels": [
        {
          "display_id": "string",
          "id": "string"
        }
      ],
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "description": "string",
      "group": {
        "display_id": "string",
        "id": "string",
        "member_type": "dev_user",
        "name": "string",
        "parents": [
          "string"
        ],
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
      "is_frozen": true,
      "last_external_message_date": "2023-01-01T12:00:00.000Z",
      "members": [
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
      "messages": [
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
                            {}
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
      ],
      "metadata": {
        "url_context": "string"
      },
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
      "sentiment": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "sentiment_modified_date": "2023-01-01T12:00:00.000Z",
      "sentiment_summary": "string",
      "sla_summary": {
        "closest_to_breach_metric": "string",
        "org_schedule": {
          "display_id": "string",
          "id": "string",
          "name": "string",
          "status": "archived",
          "timezone": "string",
          "valid_until": "2023-01-01T12:00:00.000Z",
          "version_number": 0
        },
        "remaining_time": 0,
        "sla_tracker": {
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
          "applies_to_id": "string",
          "applies_to_type": "conversation",
          "metric_target_summaries": [
            {
              "breached_at": "2023-01-01T12:00:00.000Z",
              "completed_at": "2023-01-01T12:00:00.000Z",
              "completed_in": 0,
              "completed_in_seconds": 0,
              "in_policy": true,
              "is_out_of_schedule": true,
              "metric_definition": {
                "display_id": "string",
                "id": "string",
                "name": "string"
              },
              "next_schedule_transition": "2023-01-01T12:00:00.000Z",
              "org_schedule": {
                "display_id": "string",
                "id": "string",
                "name": "string",
                "status": "archived",
                "timezone": "string",
                "valid_until": "2023-01-01T12:00:00.000Z",
                "version_number": 0
              },
              "org_schedule_version": 0,
              "remaining_time": 0,
              "stage": "string",
              "status": "string",
              "target_time": "2023-01-01T12:00:00.000Z",
              "warning_target_time": "2023-01-01T12:00:00.000Z"
            }
          ],
          "removed_sla_metric_history": [
            {
              "metric_definition": {
                "display_id": "string",
                "id": "string",
                "name": "string"
              },
              "removed_at": "2023-01-01T12:00:00.000Z",
              "removed_by": {
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
            }
          ],
          "sla": {
            "display_id": "string",
            "id": "string",
            "name": "string",
            "sla_type": "external",
            "status": "archived"
          },
          "sla_policy_id": "string",
          "stage": "string",
          "status": "string"
        },
        "stage": "breached",
        "target_time": "2023-01-01T12:00:00.000Z"
      },
      "sla_tracker": {
        "display_id": "string",
        "id": "string",
        "applies_to_type": "conversation"
      },
      "source_channel": "string",
      "source_channel_v2": {
        "display_id": "string",
        "id": "string"
      },
      "stage": {
        "name": "string",
        "notes": "string",
        "ordinal": 0,
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
      "title": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="update"></a>

## `POST /conversations.update`

**Update Conversation**

Source: <https://developer.devrev.ai/api-reference/conversations/update>

Updates the requested conversation.

**Required scopes:**

- `conversation:write` OR `conversation:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `account` | no | `string\|null` | The account associated with the conversation.<br>*Format: id* |
| `ai_resolution_status` | no | `integer` | The AI resolution status enum ID for the conversation. Stock allowed values:<br>```<br>  {<br>    "id": 1,<br>    "label": "deflected",<br>    "ordinal": 1,<br>    "overridable": false<br>  },<br>  {<br>    "id": 2,<br>    "label": "escalated",<br>    "ordinal": 2,<br>    "overridable": false<br>  }<br>```<br>*Format: int64* |
| `applies_to_parts` | no | `conversations-update-request-applies-to-parts` |  |
| `brand` | no | `string` | The brand associated with the conversation.<br>*Format: id* |
| `channels` | no | `conversations-update-request-channels` |  |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | The updated description for the conversation.<br>*Format: text* |
| `group` | no | `string` | The group that the conversation is associated with.<br>*Format: id* |
| `id` | yes | `string` | The ID of the conversation to update.<br>*Format: id* |
| `is_frozen` | no | `boolean` | Whether the conversation is frozen. |
| `is_spam` | no | `boolean` | Whether the conversation is spam. |
| `members` | no | `conversations-update-request-members` |  |
| `metadata` | no | `conversations-update-request-metadata` |  |
| `owned_by` | no | `conversations-update-request-owned-by` |  |
| `owned_by_agent` | no | `string\|null` | The ID of the AI agent that owns the conversation.<br>*Format: id* |
| `sentiment` | no | `integer` | The enum ID for the sentiment of the conversation. The allowed ids can be extended by the user. Stock allowed values:<br>```<br>  {<br>    "id": 1,<br>    "label": "Delighted",<br>    "ordinal": 1,<br>    "overridable": true<br>  },<br>  {<br>    "id": 2,<br>    "label": "Happy",<br>    "ordinal": 2,<br>    "overridable": true<br>  },<br>  {<br>    "id": 3,<br>    "label": "Neutral",<br>    "ordinal": 3,<br>    "overridable": true<br>  },<br>  {<br>    "id": 4,<br>    "label": "Unhappy",<br>    "ordinal": 4,<br>    "overridable": true<br>  },<br>  {<br>    "id": 5,<br>    "label": "Frustrated",<br>    "ordinal": 5,<br>    "overridable": true<br>  }<br>```<br>*Format: int64* |
| `sentiment_modified_date` | no | `string` | Timestamp at which sentiment was last modified.<br>*Format: date-time* |
| `sentiment_summary` | no | `string` | Summary justifying the current sentiment.<br>*Format: text* |
| `source_channel_v2` | no | `string` | Source channel ID of the conversation.<br>*Format: id* |
| `stage` | no | `stage-update` | Updates an object's stage. |
| `status` | no | `string` | The updated status of the conversation.<br>*Format: text* |
| `tags` | no | `conversations-update-request-tags` |  |
| `title` | no | `string` | The updated title of the conversation.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/conversations.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "conversation": {
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
    "account": {
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "actual_close_date": "2023-01-01T12:00:00.000Z",
    "ai_resolution_status": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
    "applies_to_parts": [
      {
        "type": "capability",
        "display_id": "string",
        "id": "string",
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
    ],
    "channels": [
      {
        "display_id": "string",
        "id": "string"
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "group": {
      "display_id": "string",
      "id": "string",
      "member_type": "dev_user",
      "name": "string",
      "parents": [
        "string"
      ],
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
    "is_frozen": true,
    "last_external_message_date": "2023-01-01T12:00:00.000Z",
    "members": [
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
    "messages": [
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
    ],
    "metadata": {
      "url_context": "string"
    },
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
    "sentiment": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
    "sentiment_modified_date": "2023-01-01T12:00:00.000Z",
    "sentiment_summary": "string",
    "sla_summary": {
      "closest_to_breach_metric": "string",
      "org_schedule": {
        "display_id": "string",
        "id": "string",
        "name": "string",
        "status": "archived",
        "timezone": "string",
        "valid_until": "2023-01-01T12:00:00.000Z",
        "version_number": 0
      },
      "remaining_time": 0,
      "sla_tracker": {
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
        "applies_to_id": "string",
        "applies_to_type": "conversation",
        "metric_target_summaries": [
          {
            "breached_at": "2023-01-01T12:00:00.000Z",
            "completed_at": "2023-01-01T12:00:00.000Z",
            "completed_in": 0,
            "completed_in_seconds": 0,
            "in_policy": true,
            "is_out_of_schedule": true,
            "metric_definition": {
              "display_id": "string",
              "id": "string",
              "name": "string"
            },
            "next_schedule_transition": "2023-01-01T12:00:00.000Z",
            "org_schedule": {
              "display_id": "string",
              "id": "string",
              "name": "string",
              "status": "archived",
              "timezone": "string",
              "valid_until": "2023-01-01T12:00:00.000Z",
              "version_number": 0
            },
            "org_schedule_version": 0,
            "remaining_time": 0,
            "stage": "string",
            "status": "string",
            "target_time": "2023-01-01T12:00:00.000Z",
            "warning_target_time": "2023-01-01T12:00:00.000Z"
          }
        ],
        "removed_sla_metric_history": [
          {
            "metric_definition": {
              "display_id": "string",
              "id": "string",
              "name": "string"
            },
            "removed_at": "2023-01-01T12:00:00.000Z",
            "removed_by": {
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
          }
        ],
        "sla": {
          "display_id": "string",
          "id": "string",
          "name": "string",
          "sla_type": "external",
          "status": "archived"
        },
        "sla_policy_id": "string",
        "stage": "string",
        "status": "string"
      },
      "stage": "breached",
      "target_time": "2023-01-01T12:00:00.000Z"
    },
    "sla_tracker": {
      "display_id": "string",
      "id": "string",
      "applies_to_type": "conversation"
    },
    "source_channel": "string",
    "source_channel_v2": {
      "display_id": "string",
      "id": "string"
    },
    "stage": {
      "name": "string",
      "notes": "string",
      "ordinal": 0,
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
    "title": "string"
  }
}
```

</details>
