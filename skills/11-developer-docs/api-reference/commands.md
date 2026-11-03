# Commands

Source: <https://developer.devrev.ai/api-reference/commands>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/commands.create` | [create](#create) |
| GET | `/commands.get` | [get](#get) |
| POST | `/commands.get` | [get-post](#get-post) |
| GET | `/commands.list` | [list](#list) |
| POST | `/commands.list` | [list-post](#list-post) |
| POST | `/commands.update` | [update](#update) |

<a id="create"></a>

## `POST /commands.create`

**Create Command**

Source: <https://developer.devrev.ai/api-reference/commands/create>

Creates a command.

**Required scopes:**

- `command:write` OR `command:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `action` | no | `create-command-action` |  |
| `description` | no | `string` | Description of the command.<br>*Format: text* |
| `display_name` | no | `string` | Display name of the command.<br>*Format: text* |
| `name` | yes | `string` | Name of the command.<br>*Format: text* |
| `namespace` | yes | `string` | Namespace of the command.<br>*Format: text* |
| `shared_with` | no | `array<set-shared-with-membership>` | The list of users, groups and audiences with whom the command is shared. |
| `source` | no | `string` | ID of the source which created this command.<br>*Format: id* |
| `status` | no | `string` | Status of the command.<br>*Value in: "disabled" \| "draft" \| "enabled"* |
| `surfaces` | no | `array<create-command-surface>` | Surfaces where this command can be invoked. |
| `usage_hint` | no | `string` | A user friendly description of the parameters which can be passed to the command.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/commands.create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "string",
    "namespace": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "command": {
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
    "action": {
      "code": "string",
      "executor_type": "rego",
      "message": "string"
    },
    "description": "string",
    "display_name": "string",
    "name": "string",
    "namespace": "string",
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
    "source": {
      "display_id": "string",
      "id": "string"
    },
    "status": "disabled",
    "surfaces": [
      {
        "object_types": [
          "account"
        ],
        "surface": "customer_chat"
      }
    ],
    "usage_hint": "string"
  }
}
```

</details>


<a id="get"></a>

## `GET /commands.get`

**Get Command**

Source: <https://developer.devrev.ai/api-reference/commands/get>

Gets a command.

**Required scopes:**

- `command:read` OR `command:write` OR `command:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The command's ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/commands.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "command": {
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
    "action": {
      "code": "string",
      "executor_type": "rego",
      "message": "string"
    },
    "description": "string",
    "display_name": "string",
    "name": "string",
    "namespace": "string",
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
    "source": {
      "display_id": "string",
      "id": "string"
    },
    "status": "disabled",
    "surfaces": [
      {
        "object_types": [
          "account"
        ],
        "surface": "customer_chat"
      }
    ],
    "usage_hint": "string"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /commands.get`

**Get Command (POST)**

Source: <https://developer.devrev.ai/api-reference/commands/get-post>

Gets a command.

**Required scopes:**

- `command:read` OR `command:write` OR `command:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The command's ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/commands.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "command": {
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
    "action": {
      "code": "string",
      "executor_type": "rego",
      "message": "string"
    },
    "description": "string",
    "display_name": "string",
    "name": "string",
    "namespace": "string",
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
    "source": {
      "display_id": "string",
      "id": "string"
    },
    "status": "disabled",
    "surfaces": [
      {
        "object_types": [
          "account"
        ],
        "surface": "customer_chat"
      }
    ],
    "usage_hint": "string"
  }
}
```

</details>


<a id="list"></a>

## `GET /commands.list`

**List Commands**

Source: <https://developer.devrev.ai/api-reference/commands/list>

Lists commands for a Dev organization.

**Required scopes:**

- `command:read` OR `command:write` OR `command:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `executor_type` | no | `array<command-action-executor-type>` | Filtering based on executor_type. |
| `limit` | no | `integer` | The maximum number of commands to return per page. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `namespace` | no | `array<string>` | Filter commands based on namespace. |
| `sort_by` | no | `array<string>` | List of fields to sort the commands items by and how to sort them. |
| `source_object_id` | no | `string` | ID of the object where command is invoked (work/part/conversation).<br>*Format: id* |
| `status` | no | `array<command-status>` | Filter commands based on status. |

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
curl -X GET "https://api.devrev.ai/commands.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "commands": [
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
      "action": {
        "code": "string",
        "executor_type": "rego",
        "message": "string"
      },
      "description": "string",
      "display_name": "string",
      "name": "string",
      "namespace": "string",
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
      "source": {
        "display_id": "string",
        "id": "string"
      },
      "status": "disabled",
      "surfaces": [
        {
          "object_types": [
            "account"
          ],
          "surface": "customer_chat"
        }
      ],
      "usage_hint": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="list-post"></a>

## `POST /commands.list`

**List Commands (POST)**

Source: <https://developer.devrev.ai/api-reference/commands/list-post>

Lists commands for a Dev organization.

**Required scopes:**

- `command:read` OR `command:write` OR `command:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `executor_type` | no | `array<command-action-executor-type>` | Filtering based on executor_type. |
| `limit` | no | `integer` | The maximum number of commands to return per page. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `namespace` | no | `array<string>` | Filter commands based on namespace. |
| `sort_by` | no | `array<string>` | List of fields to sort the commands items by and how to sort them. |
| `source_object_id` | no | `string` | ID of the object where command is invoked (work/part/conversation).<br>*Format: id* |
| `status` | no | `array<command-status>` | Filter commands based on status. |

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
curl -X POST "https://api.devrev.ai/commands.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "commands": [
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
      "action": {
        "code": "string",
        "executor_type": "rego",
        "message": "string"
      },
      "description": "string",
      "display_name": "string",
      "name": "string",
      "namespace": "string",
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
      "source": {
        "display_id": "string",
        "id": "string"
      },
      "status": "disabled",
      "surfaces": [
        {
          "object_types": [
            "account"
          ],
          "surface": "customer_chat"
        }
      ],
      "usage_hint": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="update"></a>

## `POST /commands.update`

**Update Command**

Source: <https://developer.devrev.ai/api-reference/commands/update>

Updates a command.

**Required scopes:**

- `command:write` OR `command:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `action` | no | `update-command-action` |  |
| `description` | no | `string` | Description of the command.<br>*Format: text* |
| `display_name` | no | `string` | Display name of the command.<br>*Format: text* |
| `id` | yes | `string` | The ID of the command to update.<br>*Format: id* |
| `name` | no | `string` | Name of the command.<br>*Format: text* |
| `namespace` | no | `string` | Namespace of the command.<br>*Format: text* |
| `shared_with` | no | `array<set-shared-with-membership>` | The list of users, groups and audiences with whom the command is shared. |
| `source` | no | `string` | ID of the source which created this command.<br>*Format: id* |
| `status` | no | `string` | Status of the command.<br>*Value in: "disabled" \| "draft" \| "enabled"* |
| `surfaces` | no | `array<update-command-surface>` | Surfaces where this command can be invoked. |
| `usage_hint` | no | `string` | A user friendly description of the parameters which can be passed to the command.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/commands.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "command": {
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
    "action": {
      "code": "string",
      "executor_type": "rego",
      "message": "string"
    },
    "description": "string",
    "display_name": "string",
    "name": "string",
    "namespace": "string",
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
    "source": {
      "display_id": "string",
      "id": "string"
    },
    "status": "disabled",
    "surfaces": [
      {
        "object_types": [
          "account"
        ],
        "surface": "customer_chat"
      }
    ],
    "usage_hint": "string"
  }
}
```

</details>
