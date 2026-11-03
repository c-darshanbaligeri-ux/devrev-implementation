# Code Changes

Source: <https://developer.devrev.ai/api-reference/code-changes>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/code-changes.create` | [create](#create) |
| POST | `/code-changes.delete` | [delete](#delete) |
| GET | `/code-changes.get` | [get](#get) |
| POST | `/code-changes.get` | [get-post](#get-post) |
| GET | `/code-changes.list` | [list](#list) |
| POST | `/code-changes.list` | [list-post](#list-post) |
| POST | `/code-changes.update` | [update](#update) |

<a id="create"></a>

## `POST /code-changes.create`

**Create Code Change**

Source: <https://developer.devrev.ai/api-reference/code-changes/create>

Creates a code change object.

**Required scopes:**

- `code_change:write` OR `code_change:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |

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
curl -X POST "https://api.devrev.ai/code-changes.create" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "code_change": {
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
    "branch": "string",
    "closed_date": "2023-01-01T12:00:00.000Z",
    "commit_id": "string",
    "description": "string",
    "external_identifier": "string",
    "filtered_loc": {
      "file_count": 0,
      "lines_added": 0,
      "lines_deleted": 0,
      "lines_modified": 0
    },
    "repo_url": "string",
    "source": "azure_devops",
    "target_branch": "string",
    "title": "string",
    "total_loc": {
      "file_count": 0,
      "lines_added": 0,
      "lines_deleted": 0,
      "lines_modified": 0
    }
  }
}
```

</details>


<a id="delete"></a>

## `POST /code-changes.delete`

**Delete Code Change**

Source: <https://developer.devrev.ai/api-reference/code-changes/delete>

Deletes a code change object.

**Required scopes:**

- `code_change:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | ID of the code change object which is to be deleted.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/code-changes.delete" \
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

## `GET /code-changes.get`

**Get Code Change**

Source: <https://developer.devrev.ai/api-reference/code-changes/get>

Gets a code change object.

**Required scopes:**

- `code_change:read` OR `code_change:write` OR `code_change:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The code change object ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/code-changes.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "code_change": {
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
    "branch": "string",
    "closed_date": "2023-01-01T12:00:00.000Z",
    "commit_id": "string",
    "description": "string",
    "external_identifier": "string",
    "filtered_loc": {
      "file_count": 0,
      "lines_added": 0,
      "lines_deleted": 0,
      "lines_modified": 0
    },
    "repo_url": "string",
    "source": "azure_devops",
    "target_branch": "string",
    "title": "string",
    "total_loc": {
      "file_count": 0,
      "lines_added": 0,
      "lines_deleted": 0,
      "lines_modified": 0
    }
  }
}
```

</details>


<a id="get-post"></a>

## `POST /code-changes.get`

**Get Code Change (POST)**

Source: <https://developer.devrev.ai/api-reference/code-changes/get-post>

Gets a code change object.

**Required scopes:**

- `code_change:read` OR `code_change:write` OR `code_change:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The code change object ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/code-changes.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "code_change": {
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
    "branch": "string",
    "closed_date": "2023-01-01T12:00:00.000Z",
    "commit_id": "string",
    "description": "string",
    "external_identifier": "string",
    "filtered_loc": {
      "file_count": 0,
      "lines_added": 0,
      "lines_deleted": 0,
      "lines_modified": 0
    },
    "repo_url": "string",
    "source": "azure_devops",
    "target_branch": "string",
    "title": "string",
    "total_loc": {
      "file_count": 0,
      "lines_added": 0,
      "lines_deleted": 0,
      "lines_modified": 0
    }
  }
}
```

</details>


<a id="list"></a>

## `GET /code-changes.list`

**List Code Changes**

Source: <https://developer.devrev.ai/api-reference/code-changes/list>

Lists code change objects.

**Required scopes:**

- `code_change:read` OR `code_change:write` OR `code_change:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of code change objects to return. The default is '50'.<br>*Format: int32* |
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
curl -X GET "https://api.devrev.ai/code-changes.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "code_changes": [
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
      "branch": "string",
      "closed_date": "2023-01-01T12:00:00.000Z",
      "commit_id": "string",
      "description": "string",
      "external_identifier": "string",
      "filtered_loc": {
        "file_count": 0,
        "lines_added": 0,
        "lines_deleted": 0,
        "lines_modified": 0
      },
      "repo_url": "string",
      "source": "azure_devops",
      "target_branch": "string",
      "title": "string",
      "total_loc": {
        "file_count": 0,
        "lines_added": 0,
        "lines_deleted": 0,
        "lines_modified": 0
      }
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="list-post"></a>

## `POST /code-changes.list`

**List Code Changes (POST)**

Source: <https://developer.devrev.ai/api-reference/code-changes/list-post>

Lists code change objects.

**Required scopes:**

- `code_change:read` OR `code_change:write` OR `code_change:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of code change objects to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |

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
curl -X POST "https://api.devrev.ai/code-changes.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "code_changes": [
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
      "branch": "string",
      "closed_date": "2023-01-01T12:00:00.000Z",
      "commit_id": "string",
      "description": "string",
      "external_identifier": "string",
      "filtered_loc": {
        "file_count": 0,
        "lines_added": 0,
        "lines_deleted": 0,
        "lines_modified": 0
      },
      "repo_url": "string",
      "source": "azure_devops",
      "target_branch": "string",
      "title": "string",
      "total_loc": {
        "file_count": 0,
        "lines_added": 0,
        "lines_deleted": 0,
        "lines_modified": 0
      }
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="update"></a>

## `POST /code-changes.update`

**Update Code Change**

Source: <https://developer.devrev.ai/api-reference/code-changes/update>

Updates a code change object.

**Required scopes:**

- `code_change:write` OR `code_change:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `id` | yes | `string` | The ID of the code change object to be updated.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/code-changes.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "code_change": {
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
    "branch": "string",
    "closed_date": "2023-01-01T12:00:00.000Z",
    "commit_id": "string",
    "description": "string",
    "external_identifier": "string",
    "filtered_loc": {
      "file_count": 0,
      "lines_added": 0,
      "lines_deleted": 0,
      "lines_modified": 0
    },
    "repo_url": "string",
    "source": "azure_devops",
    "target_branch": "string",
    "title": "string",
    "total_loc": {
      "file_count": 0,
      "lines_added": 0,
      "lines_deleted": 0,
      "lines_modified": 0
    }
  }
}
```

</details>
