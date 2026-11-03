# Incidents

Source: <https://developer.devrev.ai/beta/api-reference/incidents>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/incidents.create` | [create](#create) |
| POST | `/incidents.delete` | [delete](#delete) |
| GET | `/incidents.get` | [get](#get) |
| POST | `/incidents.get` | [get-post](#get-post) |
| GET | `/incidents.group` | [group](#group) |
| POST | `/incidents.group` | [group-post](#group-post) |
| GET | `/incidents.list` | [list](#list) |
| POST | `/incidents.list` | [list-post](#list-post) |
| POST | `/incidents.update` | [update](#update) |

<a id="create"></a>

## `POST /incidents.create`

**Create Incident**

Source: <https://developer.devrev.ai/beta/api-reference/incidents/create>

Creates an incident.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `acknowledged_date` | no | `string` | Timestamp when the incident was acknowledged.<br>*Format: date-time* |
| `applies_to_parts` | no | `array<string>` | Parts to which the incident is applicable to. |
| `artifacts` | no | `array<string>` | Artifacts attached to the incident. |
| `body` | no | `string` | Body of the incident.<br>*Format: text* |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `external_source_data` | no | `create-external-source-data-comp` | Create object for external_source_data_comp. |
| `identified_date` | no | `string` | Time when the incident was identified/reported.<br>*Format: date-time* |
| `impact` | no | `create-impacted-customer-details` |  |
| `mitigated_date` | no | `string` | Timestamp when the incident was mitigated.<br>*Format: date-time* |
| `owned_by` | no | `array<string>` | User IDs of the users that own the incident. |
| `pia` | no | `array<string>` | The article ids of the Post-Incident Analysis(PIA) of the incident. |
| `playbooks` | no | `array<string>` | The article ids of the playbook(s) associated with the incident. |
| `related_docs` | no | `array<string>` | The article ids of other documents associated with the incident. |
| `reported_by` | no | `integer` | The entity that first reported the incident.<br>*Format: int64* |
| `severity` | no | `integer` | Severity of the incident.<br>*Format: int64* |
| `source` | no | `integer` | **Deprecated.**<br>Source of where the incident was created. Only sys users and service accounts are supposed to set this field.<br>*Format: int64* |
| `stage` | no | `create-stage` | Create object for stage. |
| `stage_validation_options` | no | `array<stage-validation-option-for-create>` | The type of stage validations options when creating an incident. |
| `staged_info` | no | `create-staged-info` | Create object for staged_info. |
| `sync_metadata` | no | `create-sync-metadata` |  |
| `tags` | no | `array<create-tag-with-value>` | Tags associated with the object. |
| `target_close_date` | no | `string` | Timestamp when the incident is expected to be resolved.<br>*Format: date-time* |
| `title` | yes | `string` | Title of the incident.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/incidents.create" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "incident": {
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
    "acknowledged_date": "2023-01-01T12:00:00.000Z",
    "actual_close_date": "2023-01-01T12:00:00.000Z",
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
    "identified_date": "2023-01-01T12:00:00.000Z",
    "impact": {
      "count": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "customer_ids": [
        {
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      ]
    },
    "mitigated_date": "2023-01-01T12:00:00.000Z",
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
    "pia": [
      {
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
      }
    ],
    "playbooks": [
      {
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
      }
    ],
    "reported_by": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
    "severity": {
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
    "source": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
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
    "title": "string"
  }
}
```

</details>


<a id="delete"></a>

## `POST /incidents.delete`

**Delete Incident**

Source: <https://developer.devrev.ai/beta/api-reference/incidents/delete>

Deletes an incident.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | ID for the incident.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/incidents.delete" \
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

## `GET /incidents.get`

**Get Incident**

Source: <https://developer.devrev.ai/beta/api-reference/incidents/get>

Gets an incident.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the incident to get.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/incidents.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "incident": {
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
    "acknowledged_date": "2023-01-01T12:00:00.000Z",
    "actual_close_date": "2023-01-01T12:00:00.000Z",
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
    "identified_date": "2023-01-01T12:00:00.000Z",
    "impact": {
      "count": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "customer_ids": [
        {
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      ]
    },
    "mitigated_date": "2023-01-01T12:00:00.000Z",
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
    "pia": [
      {
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
      }
    ],
    "playbooks": [
      {
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
      }
    ],
    "reported_by": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
    "severity": {
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
    "source": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
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
    "title": "string"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /incidents.get`

**Get Incident (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/incidents/get-post>

Gets an incident.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the incident to get.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/incidents.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "incident": {
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
    "acknowledged_date": "2023-01-01T12:00:00.000Z",
    "actual_close_date": "2023-01-01T12:00:00.000Z",
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
    "identified_date": "2023-01-01T12:00:00.000Z",
    "impact": {
      "count": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "customer_ids": [
        {
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      ]
    },
    "mitigated_date": "2023-01-01T12:00:00.000Z",
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
    "pia": [
      {
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
      }
    ],
    "playbooks": [
      {
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
      }
    ],
    "reported_by": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
    "severity": {
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
    "source": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
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
    "title": "string"
  }
}
```

</details>


<a id="group"></a>

## `GET /incidents.group`

**Group Incidents**

Source: <https://developer.devrev.ai/beta/api-reference/incidents/group>

Lists collections of incidents by groups.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `group_by` | yes | `string` | The field to group the incidents by.<br>*Format: text* |
| `applies_to_parts` | no | `array<string>` | Filters for incidents that apply to any of the provided parts. |
| `created_by` | no | `array<string>` | Filters for incidents created by any of the provided users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `impacted_customers` | no | `array<string>` | Filters for incidents with any of the provided impacted customers. |
| `include_child_parts` | no | `boolean` | Whether to include items belonging to children of any of the provided parts. |
| `limit` | no | `integer` | The maximum number of groups to return. If not set, then the default is '10'.<br>*Format: int32* |
| `limit_per_group` | no | `integer` | The maximum number of incidents to return for an individual group. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `owned_by` | no | `array<string>` | Filters for incidents owned by any of the provided users. |
| `pia` | no | `array<string>` | Filters for incidents with any of the provided PIAs. |
| `playbooks` | no | `array<string>` | Filters for incidents with any of the provided playbooks. |
| `related_docs` | no | `array<string>` | Filters for incidents with any of the provided related docs. |
| `reported_by` | no | `array<integer>` | Filters for incidents with any of the provided reporters. |
| `severity` | no | `array<integer>` | Filters for incidents containing any of the provided severities. |
| `sort_by` | no | `array<string>` | Comma-separated fields to sort the incidents by. |
| `source` | no | `array<integer>` | **Deprecated.**<br>Filters for incidents with any of the provided sources. |
| `stage` | no | `array<string>` | Filters for incidents in any of the provided stages. |
| `staged_info.is_staged` | no | `boolean` | Filters for issues that are staged. |
| `subtype` | no | `array<string>` | Filters for incidents with any of the provided subtypes. |
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
| `title` | no | `array<string>` | Filters for incidents by the provided titles. |

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
curl -X GET "https://api.devrev.ai/incidents.group?group_by=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "groups": [
    {
      "incidents": [
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
          "acknowledged_date": "2023-01-01T12:00:00.000Z",
          "actual_close_date": "2023-01-01T12:00:00.000Z",
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
          "identified_date": "2023-01-01T12:00:00.000Z",
          "impact": {
            "count": {
              "color": "string",
              "id": 0,
              "label": "string",
              "ordinal": 0,
              "value": null
            },
            "customer_ids": [
              {
                "display_id": "string",
                "id": "string",
                "display_name": "string"
              }
            ]
          },
          "mitigated_date": "2023-01-01T12:00:00.000Z",
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
          "pia": [
            {
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
            }
          ],
          "playbooks": [
            {
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
            }
          ],
          "reported_by": {
            "color": "string",
            "id": 0,
            "label": "string",
            "ordinal": 0,
            "value": null
          },
          "severity": {
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
          "source": {
            "color": "string",
            "id": 0,
            "label": "string",
            "ordinal": 0,
            "value": null
          },
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
          "title": "string"
        }
      ],
      "key": {
        "type": "bool",
        "display_value": "string",
        "value": true
      },
      "next_cursor": "string",
      "prev_cursor": "string",
      "total": 0
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="group-post"></a>

## `POST /incidents.group`

**Group Incidents (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/incidents/group-post>

Lists collections of incidents by groups.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `acknowledged_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `actual_close_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `applies_to_parts` | no | `array<string>` | Filters for incidents that apply to any of the provided parts. |
| `created_by` | no | `array<string>` | Filters for incidents created by any of the provided users. |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `group_by` | yes | `string` | The field to group the incidents by.<br>*Format: text* |
| `identified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `impacted_customers` | no | `array<string>` | Filters for incidents with any of the provided impacted customers. |
| `include_child_parts` | no | `boolean` | Whether to include items belonging to children of any of the provided parts. |
| `limit` | no | `integer` | The maximum number of groups to return. If not set, then the default is '10'.<br>*Format: int32* |
| `limit_per_group` | no | `integer` | The maximum number of incidents to return for an individual group. The default is '50'.<br>*Format: int32* |
| `mitigated_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `owned_by` | no | `array<string>` | Filters for incidents owned by any of the provided users. |
| `pia` | no | `array<string>` | Filters for incidents with any of the provided PIAs. |
| `playbooks` | no | `array<string>` | Filters for incidents with any of the provided playbooks. |
| `related_docs` | no | `array<string>` | Filters for incidents with any of the provided related docs. |
| `reported_by` | no | `array<integer>` | Filters for incidents with any of the provided reporters. |
| `severity` | no | `array<integer>` | Filters for incidents containing any of the provided severities. |
| `sort_by` | no | `array<string>` | Comma-separated fields to sort the incidents by. |
| `source` | no | `array<integer>` | **Deprecated.**<br>Filters for incidents with any of the provided sources. |
| `stage` | no | `array<string>` | Filters for incidents in any of the provided stages. |
| `staged_info` | no | `staged-info-filter` |  |
| `subtype` | no | `array<string>` | Filters for incidents with any of the provided subtypes. |
| `sync_metadata` | no | `sync-metadata-filter` |  |
| `target_close_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `title` | no | `array<string>` | Filters for incidents by the provided titles. |

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
curl -X POST "https://api.devrev.ai/incidents.group" \
  -H "Content-Type: application/json" \
  -d '{
    "group_by": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "groups": [
    {
      "incidents": [
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
          "acknowledged_date": "2023-01-01T12:00:00.000Z",
          "actual_close_date": "2023-01-01T12:00:00.000Z",
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
          "identified_date": "2023-01-01T12:00:00.000Z",
          "impact": {
            "count": {
              "color": "string",
              "id": 0,
              "label": "string",
              "ordinal": 0,
              "value": null
            },
            "customer_ids": [
              {
                "display_id": "string",
                "id": "string",
                "display_name": "string"
              }
            ]
          },
          "mitigated_date": "2023-01-01T12:00:00.000Z",
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
          "pia": [
            {
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
            }
          ],
          "playbooks": [
            {
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
            }
          ],
          "reported_by": {
            "color": "string",
            "id": 0,
            "label": "string",
            "ordinal": 0,
            "value": null
          },
          "severity": {
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
          "source": {
            "color": "string",
            "id": 0,
            "label": "string",
            "ordinal": 0,
            "value": null
          },
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
          "title": "string"
        }
      ],
      "key": {
        "type": "bool",
        "display_value": "string",
        "value": true
      },
      "next_cursor": "string",
      "prev_cursor": "string",
      "total": 0
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="list"></a>

## `GET /incidents.list`

**List Incidents**

Source: <https://developer.devrev.ai/beta/api-reference/incidents/list>

Lists incidents.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `applies_to_parts` | no | `array<string>` | Filters for incidents that apply to any of the provided parts. |
| `created_by` | no | `array<string>` | Filters for incidents created by any of the provided users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `impacted_customers` | no | `array<string>` | Filters for incidents with any of the provided impacted customers. |
| `include_child_parts` | no | `boolean` | Whether to include items belonging to children of any of the provided parts. |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `owned_by` | no | `array<string>` | Filters for incidents owned by any of the provided users. |
| `pia` | no | `array<string>` | Filters for incidents with any of the provided PIAs. |
| `playbooks` | no | `array<string>` | Filters for incidents with any of the provided playbooks. |
| `related_docs` | no | `array<string>` | Filters for incidents with any of the provided related docs. |
| `reported_by` | no | `array<integer>` | Filters for incidents with any of the provided reporters. |
| `severity` | no | `array<integer>` | Filters for incidents containing any of the provided severities. |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |
| `source` | no | `array<integer>` | **Deprecated.**<br>Filters for incidents with any of the provided sources. |
| `stage` | no | `array<string>` | Filters for incidents in any of the provided stages. |
| `staged_info.is_staged` | no | `boolean` | Filters for issues that are staged. |
| `subtype` | no | `array<string>` | Filters for incidents with any of the provided subtypes. |
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
| `title` | no | `array<string>` | Filters for incidents by the provided titles. |

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
curl -X GET "https://api.devrev.ai/incidents.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "incidents": [
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
      "acknowledged_date": "2023-01-01T12:00:00.000Z",
      "actual_close_date": "2023-01-01T12:00:00.000Z",
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
      "identified_date": "2023-01-01T12:00:00.000Z",
      "impact": {
        "count": {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        },
        "customer_ids": [
          {
            "display_id": "string",
            "id": "string",
            "display_name": "string"
          }
        ]
      },
      "mitigated_date": "2023-01-01T12:00:00.000Z",
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
      "pia": [
        {
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
        }
      ],
      "playbooks": [
        {
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
        }
      ],
      "reported_by": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "severity": {
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
      "source": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
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
      "title": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="list-post"></a>

## `POST /incidents.list`

**List Incidents (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/incidents/list-post>

Lists incidents.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `acknowledged_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `actual_close_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `applies_to_parts` | no | `array<string>` | Filters for incidents that apply to any of the provided parts. |
| `created_by` | no | `array<string>` | Filters for incidents created by any of the provided users. |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `identified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `impacted_customers` | no | `array<string>` | Filters for incidents with any of the provided impacted customers. |
| `include_child_parts` | no | `boolean` | Whether to include items belonging to children of any of the provided parts. |
| `limit` | no | `integer` | The maximum number of items.<br>*Format: int32* |
| `mitigated_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `owned_by` | no | `array<string>` | Filters for incidents owned by any of the provided users. |
| `pia` | no | `array<string>` | Filters for incidents with any of the provided PIAs. |
| `playbooks` | no | `array<string>` | Filters for incidents with any of the provided playbooks. |
| `related_docs` | no | `array<string>` | Filters for incidents with any of the provided related docs. |
| `reported_by` | no | `array<integer>` | Filters for incidents with any of the provided reporters. |
| `severity` | no | `array<integer>` | Filters for incidents containing any of the provided severities. |
| `sort_by` | no | `array<string>` | The list of fields to sort the items by and how to sort them. |
| `source` | no | `array<integer>` | **Deprecated.**<br>Filters for incidents with any of the provided sources. |
| `stage` | no | `array<string>` | Filters for incidents in any of the provided stages. |
| `staged_info` | no | `staged-info-filter` |  |
| `subtype` | no | `array<string>` | Filters for incidents with any of the provided subtypes. |
| `sync_metadata` | no | `sync-metadata-filter` |  |
| `target_close_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `title` | no | `array<string>` | Filters for incidents by the provided titles. |

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
curl -X POST "https://api.devrev.ai/incidents.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "incidents": [
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
      "acknowledged_date": "2023-01-01T12:00:00.000Z",
      "actual_close_date": "2023-01-01T12:00:00.000Z",
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
      "identified_date": "2023-01-01T12:00:00.000Z",
      "impact": {
        "count": {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        },
        "customer_ids": [
          {
            "display_id": "string",
            "id": "string",
            "display_name": "string"
          }
        ]
      },
      "mitigated_date": "2023-01-01T12:00:00.000Z",
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
      "pia": [
        {
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
        }
      ],
      "playbooks": [
        {
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
        }
      ],
      "reported_by": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "severity": {
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
      "source": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
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
      "title": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="update"></a>

## `POST /incidents.update`

**Update Incident**

Source: <https://developer.devrev.ai/beta/api-reference/incidents/update>

Updates an incident.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `acknowledged_date` | no | `string` | Timestamp when the incident was acknowledged.<br>*Format: date-time* |
| `applies_to_parts` | no | `update-incident-applies-to-parts` |  |
| `artifacts` | no | `update-incident-artifacts` |  |
| `body` | no | `string` | Body of the incident.<br>*Format: text* |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `external_source_data` | no | `update-external-source-data-comp` | Update object for ExternalSourceDataComp. |
| `id` | yes | `string` | The ID of the incident to be updated.<br>*Format: id* |
| `identified_date` | no | `string` | Time when the incident was identified/reported.<br>*Format: date-time* |
| `impact` | no | `update-impacted-customer-details` |  |
| `mitigated_date` | no | `string` | Timestamp when the incident was mitigated.<br>*Format: date-time* |
| `owned_by` | no | `update-incident-owned-by` |  |
| `pia` | no | `update-incident-pia` |  |
| `playbooks` | no | `update-incident-playbooks` |  |
| `related_docs` | no | `update-incident-related-docs` |  |
| `reported_by` | no | `integer` | The entity that first reported the incident.<br>*Format: int64* |
| `severity` | no | `integer` | Severity of the incident.<br>*Format: int64* |
| `source` | no | `integer` | **Deprecated.**<br>Source of where the incident was created. Only sys users and service accounts are supposed to set this field.<br>*Format: int64* |
| `stage` | no | `update-stage` | Update object for Stage. |
| `stage_validation_options` | no | `array<stage-validation-option-for-update>` | The type of stage validations options when updating the stage or the stage diagram of an incident. |
| `staged_info` | no | `update-staged-info` | Update object for StagedInfo. |
| `sync_metadata` | no | `update-sync-metadata` |  |
| `tags` | no | `update-incident-tags` |  |
| `target_close_date` | no | `string\|null` | Updates the timestamp when the incident is expected to be resolved.<br>*Format: date-time* |
| `title` | no | `string` | Title of the incident.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/incidents.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "incident": {
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
    "acknowledged_date": "2023-01-01T12:00:00.000Z",
    "actual_close_date": "2023-01-01T12:00:00.000Z",
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
    "identified_date": "2023-01-01T12:00:00.000Z",
    "impact": {
      "count": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "customer_ids": [
        {
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      ]
    },
    "mitigated_date": "2023-01-01T12:00:00.000Z",
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
    "pia": [
      {
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
      }
    ],
    "playbooks": [
      {
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
      }
    ],
    "reported_by": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
    "severity": {
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
    "source": {
      "color": "string",
      "id": 0,
      "label": "string",
      "ordinal": 0,
      "value": null
    },
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
    "title": "string"
  }
}
```

</details>
