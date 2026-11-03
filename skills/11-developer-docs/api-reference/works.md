# Works

Source: <https://developer.devrev.ai/api-reference/works>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/works.count` | [count](#count) |
| POST | `/works.count` | [count-post](#count-post) |
| POST | `/works.create` | [create](#create) |
| POST | `/works.delete` | [delete](#delete) |
| GET | `/works.export` | [export](#export) |
| POST | `/works.export` | [export-post](#export-post) |
| GET | `/works.get` | [get](#get) |
| POST | `/works.get` | [get-post](#get-post) |
| GET | `/works.list` | [list](#list) |
| POST | `/works.list` | [list-post](#list-post) |
| POST | `/works.update` | [update](#update) |

<a id="count"></a>

## `GET /works.count`

**Count Works**

Source: <https://developer.devrev.ai/api-reference/works/count>

Get count of work matching given filter.

**Required scopes:** Depends on the object type in the `type` field:

| type | required scope |
| --- | --- |
| incident | `incident:read` OR `incident:write` OR `incident:all` |
| issue | `issue:read` OR `issue:write` OR `issue:all` |
| opportunity | `opportunity:read` OR `opportunity:write` OR `opportunity:all` |
| task | `task:read` OR `task:write` OR `task:all` |
| ticket | `ticket:read` OR `ticket:write` OR `ticket:all` |

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `applies_to_part` | no | `array<string>` | Filters for work belonging to any of the provided parts. |
| `created_by` | no | `array<string>` | Filters for work created by any of these users. |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `external_ref` | no | `array<string>` | Filters for work with any of the provided external references. |
| `issue.accounts` | no | `array<string>` | Filters for issues with any of the provided accounts. |
| `issue.priority` | no | `array<issue-priority>` | Filters for issues with any of the provided priorities. |
| `issue.priority_v2` | no | `array<integer>` | Filters for issues with any of the provided priority enum ids. |
| `issue.rev_orgs` | no | `array<string>` | Filters for issues with any of the provided Rev organizations. |
| `issue.sla_summary.stage` | no | `array<sla-summary-stage>` | Filters for records with any of the provided SLA stages. |
| `issue.space.ids` | no | `array<string>` | Filters for the provided space IDs. |
| `issue.space.include_children` | no | `boolean` | Whether to include child spaces. |
| `issue.space.include_global` | no | `boolean` | Whether to include objects not associated with any space. |
| `issue.space.include_parents` | no | `boolean` | Whether to include parent spaces. |
| `issue.space.op` | no | `string` | The filter operator to be applied on space.<br>*Value in: "any" \| "not_any" \| "not_null" \| "null"* |
| `issue.sprint` | no | `array<string>` | Filters for issues with any of the sprint. |
| `issue.sprint_state` | no | `array<works-filter-issue-sprint-state-value>` | Filters for issues with any of the provided sprint states. |
| `issue.subtype` | no | `array<string>` | Filters for issues with any of the provided subtypes. |
| `modified_by` | no | `array<string>` | Filters for work modified by any of these users. |
| `opportunity.account` | no | `array<string>` | Filters for opportunities belonging to any of the provided accounts. |
| `opportunity.contacts` | no | `array<string>` | Filters for opportunities with any of the provided contacts. |
| `opportunity.forecast_category_v2` | no | `array<integer>` | Filters for opportunities with any of the provided forecast category enum IDs. |
| `opportunity.subtype` | no | `array<string>` | Filters for opportunity with any of the provided subtypes. |
| `owned_by` | no | `array<string>` | Filters for work owned by any of these users. |
| `reported_by` | no | `array<string>` | Filters for work reported by any of these users. |
| `stage.name` | no | `array<string>` | Filters for records in the provided stage(s) by name. |
| `stage.stages` | no | `array<string>` | List of IDs of the custom stages which will be used for filtering. |
| `staged_info.is_staged` | no | `boolean` | Filters for issues that are staged. |
| `state` | no | `array<string>` | Filters for work with any of the provided states. |
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
| `tags` | no | `array<string>` | Filters for work with any of the provided tags. |
| `ticket.account` | no | `array<string>` | Filters for tickets with any of the provided accounts. |
| `ticket.brand` | no | `array<string>` | Filters for tickets that are associated with any of the brands. |
| `ticket.channels` | no | `array<ticket-channels>` | Filters for tickets with any of the provided channels. |
| `ticket.channels_v2` | no | `array<string>` | Filters for tickets that are associated with any of the channels. |
| `ticket.group` | no | `array<string>` | Filters for tickets belonging to specific groups. |
| `ticket.group_op` | no | `string` | The filter operator to be applied on group filter for tickets.<br>*Value in: "all" \| "any" \| "empty" \| "not_any" \| "not_empty"* |
| `ticket.is_frozen` | no | `boolean` | Filters for frozen tickets. |
| `ticket.is_spam` | no | `boolean` | Filters for tickets that are spam. |
| `ticket.needs_response` | no | `boolean` | Filters for tickets that need response. |
| `ticket.rev_org` | no | `array<string>` | Filters for tickets that are associated with any of the provided Rev organizations. |
| `ticket.severity` | no | `array<ticket-severity>` | Filters for tickets with any of the provided severities. |
| `ticket.sla_summary.stage` | no | `array<sla-summary-stage>` | Filters for records with any of the provided SLA stages. |
| `ticket.source_channel` | no | `array<string>` | Filters for tickets with any of the provided source channels. |
| `ticket.source_channel_v2` | no | `array<string>` | Filters for tickets that are associated with any of the source channels. |
| `ticket.subtype` | no | `array<string>` | Filters for tickets with any of the provided subtypes. |
| `ticket.visibility` | no | `array<integer>` | Visibility enum ID of the ticket. |
| `type` | no | `array<work-type>` | Filters for work of the provided types. |
| `vista` | no | `string` | Filters for work belonging to the given vista.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/works.count"
```

<details><summary>Example 200 response</summary>

```json
{
  "count": 0,
  "has_more": true
}
```

</details>


<a id="count-post"></a>

## `POST /works.count`

**Count Works (POST)**

Source: <https://developer.devrev.ai/api-reference/works/count-post>

Get count of work matching given filter.

**Required scopes:** Depends on the object type in the `type` field:

| type | required scope |
| --- | --- |
| incident | `incident:read` OR `incident:write` OR `incident:all` |
| issue | `issue:read` OR `issue:write` OR `issue:all` |
| opportunity | `opportunity:read` OR `opportunity:write` OR `opportunity:all` |
| task | `task:read` OR `task:write` OR `task:all` |
| ticket | `ticket:read` OR `ticket:write` OR `ticket:all` |

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `array<work-type>` | Filters for work of the provided types. |
| `actual_close_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `applies_to_part` | no | `array<string>` | Filters for work belonging to any of the provided parts. |
| `created_by` | no | `array<string>` | Filters for work created by any of these users. |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `external_ref` | no | `array<string>` | Filters for work with any of the provided external references. |
| `issue` | no | `works-filter-issue` |  |
| `modified_by` | no | `array<string>` | Filters for work modified by any of these users. |
| `modified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `opportunity` | no | `works-filter-opportunity` |  |
| `owned_by` | no | `array<string>` | Filters for work owned by any of these users. |
| `reported_by` | no | `array<string>` | Filters for work reported by any of these users. |
| `stage` | no | `stage-filter` | The filter for stages. |
| `staged_info` | no | `staged-info-filter` |  |
| `state` | no | `array<string>` | Filters for work with any of the provided states. |
| `sync_metadata` | no | `sync-metadata-filter` |  |
| `tags` | no | `array<string>` | Filters for work with any of the provided tags. |
| `target_close_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `ticket` | no | `works-filter-ticket` |  |
| `vista` | no | `string` | Filters for work belonging to the given vista.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/works.count" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "count": 0,
  "has_more": true
}
```

</details>


<a id="create"></a>

## `POST /works.create`

**Create Work**

Source: <https://developer.devrev.ai/api-reference/works/create>

Creates new work ([issue](https://devrev.ai/docs/product/build), [ticket](https://devrev.ai/docs/product/support)) item. [task](https://devrev.ai/docs/product/tasks) and opportunity work types are supported in the beta version.

**Required scopes:** Depends on the object type in the `type` field:

| type | required scope |
| --- | --- |
| incident | `incident:write` OR `incident:all` |
| issue | `issue:write` OR `issue:all` |
| opportunity | `opportunity:write` OR `opportunity:all` |
| task | `task:write` OR `task:all` |
| ticket | `ticket:write` OR `ticket:all` |

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `works-create-request-issue`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | yes | `string` | *Value in: "issue" \| "opportunity" \| "task" \| "ticket"* |
| `applies_to_part` | yes | `string` | The [part](https://devrev.ai/docs/product/parts) that the work applies to. Specifying a part is required when creating tickets and issues.<br>*Format: id* |
| `artifacts` | no | `array<string>` | The IDs of the artifacts to associate with the work item. |
| `body` | no | `string` | Body of the work object.<br>*Format: text*<br>*Length: length <= 65536* |
| `custom_fields` | no | `object` | Custom fields. |
| `custom_schema_fragments` | no | `array<string>` | The custom schema fragments to use. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `external_ref` | no | `string` | The external reference for the work item. This must be unique within the type of work item.<br>*Format: text*<br>*Length: 1 <= length <= 512* |
| `owned_by` | yes | `array<string>` | The users that own the work. |
| `reported_by` | no | `array<string>` | The users that reported the work. |
| `stage` | no | `stage-init` | Sets an object's initial stage. |
| `stage_validation_options` | no | `array<stage-validation-option-for-create>` | The type of stage validations options when creating a work item. |
| `tags` | no | `array<set-tag-with-value>` | Tags associated with the work item. |
| `target_close_date` | no | `string` | Timestamp for when the work is expected to be complete.<br>*Format: date-time* |
| `title` | yes | `string` | Title of the work object.<br>*Format: text*<br>*Length: 1 <= length <= 256* |
| `developed_with` | no | `array<string>` | The IDs of the parts associated with issue.<br>*Items: items <= 8* |
| `priority` | no | `string` | Priority of the work based upon impact and criticality.<br>*Value in: "p0" \| "p1" \| "p2" \| "p3"* |
| `priority_v2` | no | `integer` | Priority enum id of the work based upon impact and criticality. The allowed ids can be extended by the user. Stock allowed values:<br>```<br>  {<br>    "id": 1,<br>    "label": "P0",<br>    "ordinal": 1,<br>    "overridable": true<br>  },<br>  {<br>    "id": 2,<br>    "label": "P1",<br>    "ordinal": 2,<br>    "overridable": true<br>  },<br>  {<br>    "id": 3,<br>    "label": "P2",<br>    "ordinal": 3,<br>    "overridable": true<br>  },<br>  {<br>    "id": 4,<br>    "label": "P3",<br>    "ordinal": 4,<br>    "overridable": true<br>  }<br>```<br>*Format: int64* |
| `space` | no | `string` | The space that the issue belongs to.<br>*Format: id* |
| `sprint` | no | `string` | The sprint that the issue belongs to.<br>*Format: id* |
| `target_start_date` | no | `string` | Timestamp for when the work is expected to start.<br>*Format: date-time* |

#### Variant `works-create-request-opportunity`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `works-create-request-task`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `works-create-request-ticket`

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
curl -X POST "https://api.devrev.ai/works.create" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "issue",
    "applies_to_part": "PROD-12345",
    "owned_by": [
      "DEVU-12345"
    ],
    "title": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "work": {
    "type": "issue",
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
    "actual_close_date": "2023-01-01T12:00:00.000Z",
    "applies_to_part": {
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
    "body": "string",
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "external_ref": "string",
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
    "reported_by": [
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
    "state_display_name": "string",
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
    "target_close_date": "2023-01-01T12:00:00.000Z",
    "title": "string",
    "actual_start_date": "2023-01-01T12:00:00.000Z",
    "developed_with": [
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
    "display_id_alias": "string",
    "estimated_effort": 0.1,
    "last_code_activity": "2023-01-01T12:00:00.000Z",
    "priority": "p0",
    "priority_v2": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
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
    "space": "string",
    "sprint": {
      "type": "curated",
      "end_date": "2023-01-01T12:00:00.000Z",
      "id": "string",
      "name": "string",
      "start_date": "2023-01-01T12:00:00.000Z",
      "state": "active"
    },
    "target_start_date": "2023-01-01T12:00:00.000Z"
  }
}
```

</details>


<a id="delete"></a>

## `POST /works.delete`

**Delete Work**

Source: <https://developer.devrev.ai/api-reference/works/delete>

Deletes a work item.

**Required scopes:** Depends on the object type in the `id` field:

| type | required scope |
| --- | --- |
| incident | `incident:all` |
| issue | `issue:all` |
| opportunity | `opportunity:all` |
| task | `task:all` |
| ticket | `ticket:all` |

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The work's ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/works.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ISS-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="export"></a>

## `GET /works.export`

**Export Works**

Source: <https://developer.devrev.ai/api-reference/works/export>

Exports a collection of work items.

**Required scopes:** Depends on the object type in the `type` field:

| type | required scope |
| --- | --- |
| incident | `incident:read` OR `incident:write` OR `incident:all` |
| issue | `issue:read` OR `issue:write` OR `issue:all` |
| opportunity | `opportunity:read` OR `opportunity:write` OR `opportunity:all` |
| task | `task:read` OR `task:write` OR `task:all` |
| ticket | `ticket:read` OR `ticket:write` OR `ticket:all` |

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `applies_to_part` | no | `array<string>` | Filters for work belonging to any of the provided parts. |
| `created_by` | no | `array<string>` | Filters for work created by any of these users. |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `external_ref` | no | `array<string>` | Filters for work with any of the provided external references. |
| `first` | no | `integer` | The number of work items to return. The default is '50', the maximum is '5000'.<br>*Format: int32* |
| `issue.accounts` | no | `array<string>` | Filters for issues with any of the provided accounts. |
| `issue.priority` | no | `array<issue-priority>` | Filters for issues with any of the provided priorities. |
| `issue.priority_v2` | no | `array<integer>` | Filters for issues with any of the provided priority enum ids. |
| `issue.rev_orgs` | no | `array<string>` | Filters for issues with any of the provided Rev organizations. |
| `issue.sla_summary.stage` | no | `array<sla-summary-stage>` | Filters for records with any of the provided SLA stages. |
| `issue.space.ids` | no | `array<string>` | Filters for the provided space IDs. |
| `issue.space.include_children` | no | `boolean` | Whether to include child spaces. |
| `issue.space.include_global` | no | `boolean` | Whether to include objects not associated with any space. |
| `issue.space.include_parents` | no | `boolean` | Whether to include parent spaces. |
| `issue.space.op` | no | `string` | The filter operator to be applied on space.<br>*Value in: "any" \| "not_any" \| "not_null" \| "null"* |
| `issue.sprint` | no | `array<string>` | Filters for issues with any of the sprint. |
| `issue.sprint_state` | no | `array<works-filter-issue-sprint-state-value>` | Filters for issues with any of the provided sprint states. |
| `issue.subtype` | no | `array<string>` | Filters for issues with any of the provided subtypes. |
| `modified_by` | no | `array<string>` | Filters for work modified by any of these users. |
| `opportunity.account` | no | `array<string>` | Filters for opportunities belonging to any of the provided accounts. |
| `opportunity.contacts` | no | `array<string>` | Filters for opportunities with any of the provided contacts. |
| `opportunity.forecast_category_v2` | no | `array<integer>` | Filters for opportunities with any of the provided forecast category enum IDs. |
| `opportunity.subtype` | no | `array<string>` | Filters for opportunity with any of the provided subtypes. |
| `owned_by` | no | `array<string>` | Filters for work owned by any of these users. |
| `reported_by` | no | `array<string>` | Filters for work reported by any of these users. |
| `sort_by` | no | `array<string>` | Fields to sort the work items by and the direction to sort them. |
| `stage.name` | no | `array<string>` | Filters for records in the provided stage(s) by name. |
| `stage.stages` | no | `array<string>` | List of IDs of the custom stages which will be used for filtering. |
| `staged_info.is_staged` | no | `boolean` | Filters for issues that are staged. |
| `state` | no | `array<string>` | Filters for work with any of the provided states. |
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
| `tags` | no | `array<string>` | Filters for work with any of the provided tags. |
| `ticket.account` | no | `array<string>` | Filters for tickets with any of the provided accounts. |
| `ticket.brand` | no | `array<string>` | Filters for tickets that are associated with any of the brands. |
| `ticket.channels` | no | `array<ticket-channels>` | Filters for tickets with any of the provided channels. |
| `ticket.channels_v2` | no | `array<string>` | Filters for tickets that are associated with any of the channels. |
| `ticket.group` | no | `array<string>` | Filters for tickets belonging to specific groups. |
| `ticket.group_op` | no | `string` | The filter operator to be applied on group filter for tickets.<br>*Value in: "all" \| "any" \| "empty" \| "not_any" \| "not_empty"* |
| `ticket.is_frozen` | no | `boolean` | Filters for frozen tickets. |
| `ticket.is_spam` | no | `boolean` | Filters for tickets that are spam. |
| `ticket.needs_response` | no | `boolean` | Filters for tickets that need response. |
| `ticket.rev_org` | no | `array<string>` | Filters for tickets that are associated with any of the provided Rev organizations. |
| `ticket.severity` | no | `array<ticket-severity>` | Filters for tickets with any of the provided severities. |
| `ticket.sla_summary.stage` | no | `array<sla-summary-stage>` | Filters for records with any of the provided SLA stages. |
| `ticket.source_channel` | no | `array<string>` | Filters for tickets with any of the provided source channels. |
| `ticket.source_channel_v2` | no | `array<string>` | Filters for tickets that are associated with any of the source channels. |
| `ticket.subtype` | no | `array<string>` | Filters for tickets with any of the provided subtypes. |
| `ticket.visibility` | no | `array<integer>` | Visibility enum ID of the ticket. |
| `type` | no | `array<work-type>` | Filters for work of the provided types. |
| `vista` | no | `string` | Filters for work belonging to the given vista.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/works.export"
```

<details><summary>Example 200 response</summary>

```json
{
  "works": [
    {
      "type": "issue",
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
      "actual_close_date": "2023-01-01T12:00:00.000Z",
      "applies_to_part": {
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
      "body": "string",
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "external_ref": "string",
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
      "reported_by": [
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
      "state_display_name": "string",
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
      "target_close_date": "2023-01-01T12:00:00.000Z",
      "title": "string",
      "actual_start_date": "2023-01-01T12:00:00.000Z",
      "developed_with": [
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
      "display_id_alias": "string",
      "estimated_effort": 0.1,
      "last_code_activity": "2023-01-01T12:00:00.000Z",
      "priority": "p0",
      "priority_v2": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
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
      "space": "string",
      "sprint": {
        "type": "curated",
        "end_date": "2023-01-01T12:00:00.000Z",
        "id": "string",
        "name": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "state": "active"
      },
      "target_start_date": "2023-01-01T12:00:00.000Z"
    }
  ]
}
```

</details>


<a id="export-post"></a>

## `POST /works.export`

**Export Works (POST)**

Source: <https://developer.devrev.ai/api-reference/works/export-post>

Exports a collection of work items.

**Required scopes:** Depends on the object type in the `type` field:

| type | required scope |
| --- | --- |
| incident | `incident:read` OR `incident:write` OR `incident:all` |
| issue | `issue:read` OR `issue:write` OR `issue:all` |
| opportunity | `opportunity:read` OR `opportunity:write` OR `opportunity:all` |
| task | `task:read` OR `task:write` OR `task:all` |
| ticket | `ticket:read` OR `ticket:write` OR `ticket:all` |

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `array<work-type>` | Filters for work of the provided types. |
| `actual_close_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `applies_to_part` | no | `array<string>` | Filters for work belonging to any of the provided parts. |
| `created_by` | no | `array<string>` | Filters for work created by any of these users. |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `external_ref` | no | `array<string>` | Filters for work with any of the provided external references. |
| `first` | no | `integer` | The number of work items to return. The default is '50', the maximum is '5000'.<br>*Format: int32* |
| `issue` | no | `works-filter-issue` |  |
| `modified_by` | no | `array<string>` | Filters for work modified by any of these users. |
| `modified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `opportunity` | no | `works-filter-opportunity` |  |
| `owned_by` | no | `array<string>` | Filters for work owned by any of these users. |
| `reported_by` | no | `array<string>` | Filters for work reported by any of these users. |
| `sort_by` | no | `array<string>` | Fields to sort the work items by and the direction to sort them. |
| `stage` | no | `stage-filter` | The filter for stages. |
| `staged_info` | no | `staged-info-filter` |  |
| `state` | no | `array<string>` | Filters for work with any of the provided states. |
| `sync_metadata` | no | `sync-metadata-filter` |  |
| `tags` | no | `array<string>` | Filters for work with any of the provided tags. |
| `target_close_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `ticket` | no | `works-filter-ticket` |  |
| `vista` | no | `string` | Filters for work belonging to the given vista.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/works.export" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "works": [
    {
      "type": "issue",
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
      "actual_close_date": "2023-01-01T12:00:00.000Z",
      "applies_to_part": {
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
      "body": "string",
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "external_ref": "string",
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
      "reported_by": [
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
      "state_display_name": "string",
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
      "target_close_date": "2023-01-01T12:00:00.000Z",
      "title": "string",
      "actual_start_date": "2023-01-01T12:00:00.000Z",
      "developed_with": [
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
      "display_id_alias": "string",
      "estimated_effort": 0.1,
      "last_code_activity": "2023-01-01T12:00:00.000Z",
      "priority": "p0",
      "priority_v2": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
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
      "space": "string",
      "sprint": {
        "type": "curated",
        "end_date": "2023-01-01T12:00:00.000Z",
        "id": "string",
        "name": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "state": "active"
      },
      "target_start_date": "2023-01-01T12:00:00.000Z"
    }
  ]
}
```

</details>


<a id="get"></a>

## `GET /works.get`

**Get Work**

Source: <https://developer.devrev.ai/api-reference/works/get>

Gets a work item's information.

**Required scopes:** Depends on the object type in the `id` field:

| type | required scope |
| --- | --- |
| incident | `incident:read` OR `incident:write` OR `incident:all` |
| issue | `issue:read` OR `issue:write` OR `issue:all` |
| opportunity | `opportunity:read` OR `opportunity:write` OR `opportunity:all` |
| task | `task:read` OR `task:write` OR `task:all` |
| ticket | `ticket:read` OR `ticket:write` OR `ticket:all` |

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The work's ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/works.get?id=ISS-12345"
```

<details><summary>Example 200 response</summary>

```json
{
  "work": {
    "type": "issue",
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
    "actual_close_date": "2023-01-01T12:00:00.000Z",
    "applies_to_part": {
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
    "body": "string",
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "external_ref": "string",
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
    "reported_by": [
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
    "state_display_name": "string",
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
    "target_close_date": "2023-01-01T12:00:00.000Z",
    "title": "string",
    "actual_start_date": "2023-01-01T12:00:00.000Z",
    "developed_with": [
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
    "display_id_alias": "string",
    "estimated_effort": 0.1,
    "last_code_activity": "2023-01-01T12:00:00.000Z",
    "priority": "p0",
    "priority_v2": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
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
    "space": "string",
    "sprint": {
      "type": "curated",
      "end_date": "2023-01-01T12:00:00.000Z",
      "id": "string",
      "name": "string",
      "start_date": "2023-01-01T12:00:00.000Z",
      "state": "active"
    },
    "target_start_date": "2023-01-01T12:00:00.000Z"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /works.get`

**Get Work (POST)**

Source: <https://developer.devrev.ai/api-reference/works/get-post>

Gets a work item's information.

**Required scopes:** Depends on the object type in the `id` field:

| type | required scope |
| --- | --- |
| incident | `incident:read` OR `incident:write` OR `incident:all` |
| issue | `issue:read` OR `issue:write` OR `issue:all` |
| opportunity | `opportunity:read` OR `opportunity:write` OR `opportunity:all` |
| task | `task:read` OR `task:write` OR `task:all` |
| ticket | `ticket:read` OR `ticket:write` OR `ticket:all` |

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The work's ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/works.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ISS-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "work": {
    "type": "issue",
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
    "actual_close_date": "2023-01-01T12:00:00.000Z",
    "applies_to_part": {
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
    "body": "string",
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "external_ref": "string",
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
    "reported_by": [
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
    "state_display_name": "string",
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
    "target_close_date": "2023-01-01T12:00:00.000Z",
    "title": "string",
    "actual_start_date": "2023-01-01T12:00:00.000Z",
    "developed_with": [
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
    "display_id_alias": "string",
    "estimated_effort": 0.1,
    "last_code_activity": "2023-01-01T12:00:00.000Z",
    "priority": "p0",
    "priority_v2": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
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
    "space": "string",
    "sprint": {
      "type": "curated",
      "end_date": "2023-01-01T12:00:00.000Z",
      "id": "string",
      "name": "string",
      "start_date": "2023-01-01T12:00:00.000Z",
      "state": "active"
    },
    "target_start_date": "2023-01-01T12:00:00.000Z"
  }
}
```

</details>


<a id="list"></a>

## `GET /works.list`

**List Works**

Source: <https://developer.devrev.ai/api-reference/works/list>

Lists a collection of work items.

**Required scopes:** Depends on the object type in the `type` field:

| type | required scope |
| --- | --- |
| incident | `incident:read` OR `incident:write` OR `incident:all` |
| issue | `issue:read` OR `issue:write` OR `issue:all` |
| opportunity | `opportunity:read` OR `opportunity:write` OR `opportunity:all` |
| task | `task:read` OR `task:write` OR `task:all` |
| ticket | `ticket:read` OR `ticket:write` OR `ticket:all` |

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `applies_to_part` | no | `array<string>` | Filters for work belonging to any of the provided parts. |
| `created_by` | no | `array<string>` | Filters for work created by any of these users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `external_ref` | no | `array<string>` | Filters for work with any of the provided external references. |
| `issue.accounts` | no | `array<string>` | Filters for issues with any of the provided accounts. |
| `issue.priority` | no | `array<issue-priority>` | Filters for issues with any of the provided priorities. |
| `issue.priority_v2` | no | `array<integer>` | Filters for issues with any of the provided priority enum ids. |
| `issue.rev_orgs` | no | `array<string>` | Filters for issues with any of the provided Rev organizations. |
| `issue.sla_summary.stage` | no | `array<sla-summary-stage>` | Filters for records with any of the provided SLA stages. |
| `issue.space.ids` | no | `array<string>` | Filters for the provided space IDs. |
| `issue.space.include_children` | no | `boolean` | Whether to include child spaces. |
| `issue.space.include_global` | no | `boolean` | Whether to include objects not associated with any space. |
| `issue.space.include_parents` | no | `boolean` | Whether to include parent spaces. |
| `issue.space.op` | no | `string` | The filter operator to be applied on space.<br>*Value in: "any" \| "not_any" \| "not_null" \| "null"* |
| `issue.sprint` | no | `array<string>` | Filters for issues with any of the sprint. |
| `issue.sprint_state` | no | `array<works-filter-issue-sprint-state-value>` | Filters for issues with any of the provided sprint states. |
| `issue.subtype` | no | `array<string>` | Filters for issues with any of the provided subtypes. |
| `limit` | no | `integer` | The maximum number of works to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `modified_by` | no | `array<string>` | Filters for work modified by any of these users. |
| `opportunity.account` | no | `array<string>` | Filters for opportunities belonging to any of the provided accounts. |
| `opportunity.contacts` | no | `array<string>` | Filters for opportunities with any of the provided contacts. |
| `opportunity.forecast_category_v2` | no | `array<integer>` | Filters for opportunities with any of the provided forecast category enum IDs. |
| `opportunity.subtype` | no | `array<string>` | Filters for opportunity with any of the provided subtypes. |
| `owned_by` | no | `array<string>` | Filters for work owned by any of these users. |
| `reported_by` | no | `array<string>` | Filters for work reported by any of these users. |
| `sort_by` | no | `array<string>` | Fields to sort the works by and the direction to sort them. |
| `stage.name` | no | `array<string>` | Filters for records in the provided stage(s) by name. |
| `stage.stages` | no | `array<string>` | List of IDs of the custom stages which will be used for filtering. |
| `staged_info.is_staged` | no | `boolean` | Filters for issues that are staged. |
| `state` | no | `array<string>` | Filters for work with any of the provided states. |
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
| `tags` | no | `array<string>` | Filters for work with any of the provided tags. |
| `ticket.account` | no | `array<string>` | Filters for tickets with any of the provided accounts. |
| `ticket.brand` | no | `array<string>` | Filters for tickets that are associated with any of the brands. |
| `ticket.channels` | no | `array<ticket-channels>` | Filters for tickets with any of the provided channels. |
| `ticket.channels_v2` | no | `array<string>` | Filters for tickets that are associated with any of the channels. |
| `ticket.group` | no | `array<string>` | Filters for tickets belonging to specific groups. |
| `ticket.group_op` | no | `string` | The filter operator to be applied on group filter for tickets.<br>*Value in: "all" \| "any" \| "empty" \| "not_any" \| "not_empty"* |
| `ticket.is_frozen` | no | `boolean` | Filters for frozen tickets. |
| `ticket.is_spam` | no | `boolean` | Filters for tickets that are spam. |
| `ticket.needs_response` | no | `boolean` | Filters for tickets that need response. |
| `ticket.rev_org` | no | `array<string>` | Filters for tickets that are associated with any of the provided Rev organizations. |
| `ticket.severity` | no | `array<ticket-severity>` | Filters for tickets with any of the provided severities. |
| `ticket.sla_summary.stage` | no | `array<sla-summary-stage>` | Filters for records with any of the provided SLA stages. |
| `ticket.source_channel` | no | `array<string>` | Filters for tickets with any of the provided source channels. |
| `ticket.source_channel_v2` | no | `array<string>` | Filters for tickets that are associated with any of the source channels. |
| `ticket.subtype` | no | `array<string>` | Filters for tickets with any of the provided subtypes. |
| `ticket.visibility` | no | `array<integer>` | Visibility enum ID of the ticket. |
| `type` | no | `array<work-type>` | Filters for work of the provided types. |
| `vista` | no | `string` | Filters for work belonging to the given vista.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/works.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "works": [
    {
      "type": "issue",
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
      "actual_close_date": "2023-01-01T12:00:00.000Z",
      "applies_to_part": {
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
      "body": "string",
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "external_ref": "string",
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
      "reported_by": [
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
      "state_display_name": "string",
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
      "target_close_date": "2023-01-01T12:00:00.000Z",
      "title": "string",
      "actual_start_date": "2023-01-01T12:00:00.000Z",
      "developed_with": [
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
      "display_id_alias": "string",
      "estimated_effort": 0.1,
      "last_code_activity": "2023-01-01T12:00:00.000Z",
      "priority": "p0",
      "priority_v2": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
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
      "space": "string",
      "sprint": {
        "type": "curated",
        "end_date": "2023-01-01T12:00:00.000Z",
        "id": "string",
        "name": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "state": "active"
      },
      "target_start_date": "2023-01-01T12:00:00.000Z"
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /works.list`

**List Works (POST)**

Source: <https://developer.devrev.ai/api-reference/works/list-post>

Lists a collection of work items.

**Required scopes:** Depends on the object type in the `type` field:

| type | required scope |
| --- | --- |
| incident | `incident:read` OR `incident:write` OR `incident:all` |
| issue | `issue:read` OR `issue:write` OR `issue:all` |
| opportunity | `opportunity:read` OR `opportunity:write` OR `opportunity:all` |
| task | `task:read` OR `task:write` OR `task:all` |
| ticket | `ticket:read` OR `ticket:write` OR `ticket:all` |

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `array<work-type>` | Filters for work of the provided types. |
| `actual_close_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `applies_to_part` | no | `array<string>` | Filters for work belonging to any of the provided parts. |
| `created_by` | no | `array<string>` | Filters for work created by any of these users. |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `external_ref` | no | `array<string>` | Filters for work with any of the provided external references. |
| `issue` | no | `works-filter-issue` |  |
| `limit` | no | `integer` | The maximum number of works to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_by` | no | `array<string>` | Filters for work modified by any of these users. |
| `modified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `opportunity` | no | `works-filter-opportunity` |  |
| `owned_by` | no | `array<string>` | Filters for work owned by any of these users. |
| `reported_by` | no | `array<string>` | Filters for work reported by any of these users. |
| `sort_by` | no | `array<string>` | Fields to sort the works by and the direction to sort them. |
| `stage` | no | `stage-filter` | The filter for stages. |
| `staged_info` | no | `staged-info-filter` |  |
| `state` | no | `array<string>` | Filters for work with any of the provided states. |
| `sync_metadata` | no | `sync-metadata-filter` |  |
| `tags` | no | `array<string>` | Filters for work with any of the provided tags. |
| `target_close_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `ticket` | no | `works-filter-ticket` |  |
| `vista` | no | `string` | Filters for work belonging to the given vista.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/works.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "works": [
    {
      "type": "issue",
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
      "actual_close_date": "2023-01-01T12:00:00.000Z",
      "applies_to_part": {
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
      "body": "string",
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "external_ref": "string",
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
      "reported_by": [
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
      "state_display_name": "string",
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
      "target_close_date": "2023-01-01T12:00:00.000Z",
      "title": "string",
      "actual_start_date": "2023-01-01T12:00:00.000Z",
      "developed_with": [
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
      "display_id_alias": "string",
      "estimated_effort": 0.1,
      "last_code_activity": "2023-01-01T12:00:00.000Z",
      "priority": "p0",
      "priority_v2": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
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
      "space": "string",
      "sprint": {
        "type": "curated",
        "end_date": "2023-01-01T12:00:00.000Z",
        "id": "string",
        "name": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "state": "active"
      },
      "target_start_date": "2023-01-01T12:00:00.000Z"
    }
  ]
}
```

</details>


<a id="update"></a>

## `POST /works.update`

**Update Work**

Source: <https://developer.devrev.ai/api-reference/works/update>

Updates a work item's information.

**Required scopes:** Depends on the object type in the `id` field:

| type | required scope |
| --- | --- |
| incident | `incident:write` OR `incident:all` |
| issue | `issue:write` OR `issue:all` |
| opportunity | `opportunity:write` OR `opportunity:all` |
| task | `task:write` OR `task:all` |
| ticket | `ticket:write` OR `ticket:all` |

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `empty`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `string` | *Value in: "issue" \| "opportunity" \| "task" \| "ticket"* |
| `applies_to_part` | no | `string` | Updates the part that the work item applies to.<br>*Format: id* |
| `artifacts` | no | `works-update-request-artifacts` |  |
| `body` | no | `string` | Updated body of the work object, or unchanged if not provided.<br>*Format: text*<br>*Length: length <= 65536* |
| `custom_fields` | no | `object` | Custom fields. |
| `custom_schema_fragments` | no | `array<string>` | The custom schema fragments to use. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `id` | yes | `string` | The work's ID.<br>*Format: id* |
| `object_version` | no | `integer` | The object version of the work to be updated. If provided, the update will be rejected if the object version does not match the latest version.<br>*Format: int64* |
| `owned_by` | no | `works-update-request-owned-by` |  |
| `reported_by` | no | `works-update-request-reported-by` |  |
| `stage` | no | `stage-update` | Updates an object's stage. |
| `stage_validation_options` | no | `array<stage-validation-option-for-update>` | The type of stage validations options when updating the stage or the stage diagram of an object. |
| `staged_info` | no | `works-update-request-staged-info-update` |  |
| `tags` | no | `works-update-request-tags` |  |
| `target_close_date` | no | `string\|null` | Updates the timestamp for when the work is expected to be complete.<br>*Format: date-time* |
| `title` | no | `string` | Updated title of the work object, or unchanged if not provided.<br>*Format: text*<br>*Length: 1 <= length <= 256* |
| `[key: string]` | no | `never` |  |

#### Variant `works-update-request-issue`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `works-update-request-opportunity`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `works-update-request-task`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `works-update-request-ticket`

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
curl -X POST "https://api.devrev.ai/works.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ISS-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "work": {
    "type": "issue",
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
    "actual_close_date": "2023-01-01T12:00:00.000Z",
    "applies_to_part": {
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
    "body": "string",
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "external_ref": "string",
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
    "reported_by": [
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
    "state_display_name": "string",
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
    "target_close_date": "2023-01-01T12:00:00.000Z",
    "title": "string",
    "actual_start_date": "2023-01-01T12:00:00.000Z",
    "developed_with": [
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
    "display_id_alias": "string",
    "estimated_effort": 0.1,
    "last_code_activity": "2023-01-01T12:00:00.000Z",
    "priority": "p0",
    "priority_v2": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
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
    "space": "string",
    "sprint": {
      "type": "curated",
      "end_date": "2023-01-01T12:00:00.000Z",
      "id": "string",
      "name": "string",
      "start_date": "2023-01-01T12:00:00.000Z",
      "state": "active"
    },
    "target_start_date": "2023-01-01T12:00:00.000Z"
  }
}
```

</details>
