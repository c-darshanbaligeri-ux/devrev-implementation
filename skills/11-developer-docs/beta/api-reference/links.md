# Links

Source: <https://developer.devrev.ai/beta/api-reference/links>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/links.create` | [create](#create) |
| POST | `/links.delete` | [delete](#delete) |
| GET | `/links.get` | [get](#get) |
| POST | `/links.get` | [get-post](#get-post) |
| GET | `/links.list` | [list](#list) |
| POST | `/links.list` | [list-post](#list-post) |
| POST | `/links.replace` | [replace](#replace) |

<a id="create"></a>

## `POST /links.create`

**Create Link**

Source: <https://developer.devrev.ai/beta/api-reference/links/create>

Creates a link between two objects to indicate a relationship.

**Required scopes:**

- `link:write` OR `link:all`

Also needs linked objects read access.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `custom_link_type` | no | `string` | The ID of the custom link type.<br>*Format: id* |
| `link_type` | no | `string` | Type of link used to define the relationship.<br>*Value in: "custom_link" \| "developed_with" \| "imports" \| "is_analyzed_by" \| "is_converted_to" \| "is_dependent_on" \| "is_duplicate_of" \| "is_follow_up_of" \| "is_merged_into" \| "is_parent_of" \| "is_part_of" \| "is_related_to" \| "serves"* |
| `source` | yes | `string` | The ID of the source object.<br>*Format: id* |
| `target` | yes | `string` | The ID of the target object.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/links.create" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "string",
    "target": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "link": {
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
    "custom_link_type": {
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
    },
    "link_type": "custom_link",
    "source": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
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
    "target": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    }
  }
}
```

</details>


<a id="delete"></a>

## `POST /links.delete`

**Delete Link**

Source: <https://developer.devrev.ai/beta/api-reference/links/delete>

Deletes a link between two objects. Note that for part hierarchy links (e.g. enhancement to capability), deleting a link may leave an orphan object with no parent. If the intent is to re-parent an object rather than unlink it entirely, use `links.replace` instead, which atomically removes the old link and creates a new one in a single transaction.

**Required scopes:**

- `link:all`

Also needs linked objects read access.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the link to delete.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/links.delete" \
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

## `GET /links.get`

**Get Link**

Source: <https://developer.devrev.ai/beta/api-reference/links/get>

Gets the requested link's information.

**Required scopes:**

- `link:read` OR `link:write` OR `link:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The requested link's ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/links.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "link": {
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
    "custom_link_type": {
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
    },
    "link_type": "custom_link",
    "source": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
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
    "target": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    }
  }
}
```

</details>


<a id="get-post"></a>

## `POST /links.get`

**Get Link (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/links/get-post>

Gets the requested link's information.

**Required scopes:**

- `link:read` OR `link:write` OR `link:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The requested link's ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/links.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "link": {
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
    "custom_link_type": {
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
    },
    "link_type": "custom_link",
    "source": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
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
    "target": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    }
  }
}
```

</details>


<a id="list"></a>

## `GET /links.list`

**List Links**

Source: <https://developer.devrev.ai/beta/api-reference/links/list>

Lists the available links.

**Required scopes:**

- `link:read` OR `link:write` OR `link:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `object` | yes | `string` | The ID of the object to list the links for.<br>*Format: id* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_link_type` | no | `array<string>` | The custom link types to filter for, otherwise if not present, all custom link types are included. |
| `direction` | no | `string` | The direction of the links to list, otherwise if not present, then links in both directions (source and target) are included.<br>*Value in: "is_source" \| "is_target"* |
| `limit` | no | `integer` | The maximum number of links to return. If not set, then the default is '50'.<br>*Format: int32* |
| `link_type` | no | `array<link-type>` | The link type(s) to filter for, otherwise if not present, all link types are included. |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `object_types` | no | `array<link-endpoint-type>` | The object types to filter for, otherwise if not present, all object types are included. |
| `types` | no | `array<link-type>` | **Deprecated.**<br>The link types to filter for, otherwise if not present, all link types are included. |

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
curl -X GET "https://api.devrev.ai/links.list?object=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "links": [
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
      "custom_link_type": {
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
      },
      "link_type": "custom_link",
      "source": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
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
      "target": {
        "type": "account",
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


<a id="list-post"></a>

## `POST /links.list`

**List Links (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/links/list-post>

Lists the available links.

**Required scopes:**

- `link:read` OR `link:write` OR `link:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_link_type` | no | `array<string>` | The custom link types to filter for, otherwise if not present, all custom link types are included. |
| `direction` | no | `string` | The direction of link, which can either be outbound such that the object is the source of the link, otherwise inbound where the object is the target of the link.<br>*Value in: "is_source" \| "is_target"* |
| `limit` | no | `integer` | The maximum number of links to return. If not set, then the default is '50'.<br>*Format: int32* |
| `link_type` | no | `array<link-type>` | The link type(s) to filter for, otherwise if not present, all link types are included. |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `object` | yes | `string` | The ID of the object to list the links for.<br>*Format: id* |
| `object_types` | no | `array<link-endpoint-type>` | The object types to filter for, otherwise if not present, all object types are included. |
| `types` | no | `array<link-type>` | **Deprecated.**<br>The link types to filter for, otherwise if not present, all link types are included. |

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
curl -X POST "https://api.devrev.ai/links.list" \
  -H "Content-Type: application/json" \
  -d '{
    "object": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "links": [
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
      "custom_link_type": {
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
      },
      "link_type": "custom_link",
      "source": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
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
      "target": {
        "type": "account",
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


<a id="replace"></a>

## `POST /links.replace`

**Replace Links**

Source: <https://developer.devrev.ai/beta/api-reference/links/replace>

Replaces an existing link with a new one. This is useful when an object must always remain linked to a parent — for example, re-parenting an enhancement under a different capability or product part — because it avoids the intermediate unlinked (orphan) state that would otherwise occur if you deleted the old link and created a new one as two separate steps. The existing link identified by `id` is removed and a new link is created from `source` to `target`. Optionally, a different `link_type` or `custom_link_type` can be specified for the new link. For links between parts using a default (non-custom) link type, the replacement is performed atomically. For all other cases (custom link types or non-part endpoints), the replacement is performed as a non-atomic delete followed by a create; in these cases, the new link must have the same link type (or the same `custom_link_type` DON) as the existing link, and must share at least one of the source or target with the existing link, otherwise the request is rejected.

**Required scopes:**

- `link:write` OR `link:all`

Also needs linked objects read access.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `custom_link_type` | no | `string` | The ID of the custom link type, for the new link to be created.<br>*Format: id* |
| `id` | yes | `string` | The ID of the link to be replaced.<br>*Format: id* |
| `link_type` | no | `string` | Type of link used to define the relationship.<br>*Value in: "custom_link" \| "developed_with" \| "imports" \| "is_analyzed_by" \| "is_converted_to" \| "is_dependent_on" \| "is_duplicate_of" \| "is_follow_up_of" \| "is_merged_into" \| "is_parent_of" \| "is_part_of" \| "is_related_to" \| "serves"* |
| `source` | yes | `string` | The ID of the source object.<br>*Format: id* |
| `target` | yes | `string` | The ID of the target object.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/links.replace" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string",
    "source": "string",
    "target": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "link": {
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
    "custom_link_type": {
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
    },
    "link_type": "custom_link",
    "source": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
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
    "target": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    }
  }
}
```

</details>
