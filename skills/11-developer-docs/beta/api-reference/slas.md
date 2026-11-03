# Slas

Source: <https://developer.devrev.ai/beta/api-reference/slas>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/metric-action.execute` | [metric-action-execute](#metric-action-execute) |
| POST | `/metric-definitions.create` | [metric-definitions-create](#metric-definitions-create) |
| POST | `/metric-definitions.delete` | [metric-definitions-delete](#metric-definitions-delete) |
| GET | `/metric-definitions.get` | [metric-definitions-get](#metric-definitions-get) |
| POST | `/metric-definitions.get` | [metric-definitions-get-post](#metric-definitions-get-post) |
| GET | `/metric-definitions.list` | [metric-definitions-list](#metric-definitions-list) |
| POST | `/metric-definitions.list` | [metric-definitions-list-post](#metric-definitions-list-post) |
| POST | `/metric-definitions.update` | [metric-definitions-update](#metric-definitions-update) |
| GET | `/metric-trackers.get` | [metric-trackers-get](#metric-trackers-get) |
| POST | `/metric-trackers.get` | [metric-trackers-get-post](#metric-trackers-get-post) |
| GET | `/sla-trackers.get` | [sla-trackers-get](#sla-trackers-get) |
| POST | `/sla-trackers.get` | [sla-trackers-get-post](#sla-trackers-get-post) |
| GET | `/sla-trackers.list` | [sla-trackers-list](#sla-trackers-list) |
| POST | `/sla-trackers.list` | [sla-trackers-list-post](#sla-trackers-list-post) |
| POST | `/sla-trackers.remove-metric` | [sla-trackers-remove-metric](#sla-trackers-remove-metric) |
| POST | `/slas.assign` | [assign](#assign) |
| POST | `/slas.create` | [create](#create) |
| GET | `/slas.get` | [get](#get) |
| POST | `/slas.get` | [get-post](#get-post) |
| GET | `/slas.list` | [list](#list) |
| POST | `/slas.list` | [list-post](#list-post) |
| POST | `/slas.transition` | [transition](#transition) |
| POST | `/slas.update` | [update](#update) |

<a id="metric-action-execute"></a>

## `POST /metric-action.execute`

**Execute Metric Action**

Source: <https://developer.devrev.ai/beta/api-reference/slas/metric-action-execute>

Executes the metric action on the given object.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `action` | yes | `string` | *Value in: "complete" \| "pause" \| "restart" \| "resume" \| "start"* |
| `event_date` | yes | `string` | Timestamp of the event.<br>*Format: date-time* |
| `metric` | yes | `string` | The metric's ID for which the metric action is to be executed.<br>*Format: id* |
| `object` | yes | `string` | The underlying object's ID on which the metric action is to be executed.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/metric-action.execute" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "complete",
    "event_date": "2023-01-01T12:00:00.000Z",
    "metric": "string",
    "object": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="metric-definitions-create"></a>

## `POST /metric-definitions.create`

**Create Metric Definition**

Source: <https://developer.devrev.ai/beta/api-reference/slas/metric-definitions-create>

Creates a custom metric definition

**Required scopes:**

- `metric_definition:write` OR `metric_definition:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `applies_to` | yes | `array<metric-definition-applies-to>` | The list of object types on which the metric can be applied. |
| `description` | no | `string` | Description of the purpose and operation of the metric.<br>*Format: text*<br>*Length: length <= 1024* |
| `name` | yes | `string` | A unique human readable name of the metric.<br>*Format: text*<br>*Length: 1 <= length <= 64* |

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
curl -X POST "https://api.devrev.ai/metric-definitions.create" \
  -H "Content-Type: application/json" \
  -d '{
    "applies_to": [
      "conversation"
    ],
    "name": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "metric_definition": {
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
    "name": "string"
  }
}
```

</details>


<a id="metric-definitions-delete"></a>

## `POST /metric-definitions.delete`

**Delete Metric Definition**

Source: <https://developer.devrev.ai/beta/api-reference/slas/metric-definitions-delete>

Deletes a custom metric definition

**Required scopes:**

- `metric_definition:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the metric definition to be deleted.<br>*Format: id* |

### Response codes

- `204` — `application/json`
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
curl -X POST "https://api.devrev.ai/metric-definitions.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 204 response</summary>

```json
{}
```

</details>


<a id="metric-definitions-get"></a>

## `GET /metric-definitions.get`

**Get Metric Definition**

Source: <https://developer.devrev.ai/beta/api-reference/slas/metric-definitions-get>

Gets a custom metric definition

**Required scopes:**

- `metric_definition:read` OR `metric_definition:write` OR `metric_definition:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | no | `string` | The ID of the metric definition to get.<br>*Format: id* |
| `name` | no | `string` | The unique human readable name of the metric.<br>*Format: text*<br>*Length: 1 <= length <= 64* |

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
curl -X GET "https://api.devrev.ai/metric-definitions.get"
```

<details><summary>Example 200 response</summary>

```json
{
  "metric_definition": {
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
    "name": "string"
  }
}
```

</details>


<a id="metric-definitions-get-post"></a>

## `POST /metric-definitions.get`

**Get Metric Definition (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/slas/metric-definitions-get-post>

Gets a custom metric definition

**Required scopes:**

- `metric_definition:read` OR `metric_definition:write` OR `metric_definition:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | no | `string` | The ID of the metric definition to get.<br>*Format: id* |
| `name` | no | `string` | The unique human readable name of the metric.<br>*Format: text*<br>*Length: 1 <= length <= 64* |

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
curl -X POST "https://api.devrev.ai/metric-definitions.get" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "metric_definition": {
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
    "name": "string"
  }
}
```

</details>


<a id="metric-definitions-list"></a>

## `GET /metric-definitions.list`

**List Metric Definitions**

Source: <https://developer.devrev.ai/beta/api-reference/slas/metric-definitions-list>

Lists metric definitions matching a filter.

**Required scopes:**

- `metric_definition:read` OR `metric_definition:write` OR `metric_definition:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `applies_to_type` | no | `array<metric-definition-applies-to>` | The type of objects the metric definition applies to. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `include_custom_metrics` | no | `boolean` | Whether to include custom metrics in the response. If not set, then custom metrics are excluded. |
| `limit` | no | `integer` | The maximum number of records to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `sort_by` | no | `array<string>` | Fields to sort the records by and the direction to sort them. |
| `status` | no | `array<metric-definition-status>` | The status of the metric definition. |
| `type` | no | `array<metric-definition-metric-type>` | The type of metric definitions sought. |

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
curl -X GET "https://api.devrev.ai/metric-definitions.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "metric_definitions": [
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
      "name": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="metric-definitions-list-post"></a>

## `POST /metric-definitions.list`

**List Metric Definitions (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/slas/metric-definitions-list-post>

Lists metric definitions matching a filter.

**Required scopes:**

- `metric_definition:read` OR `metric_definition:write` OR `metric_definition:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `array<metric-definition-metric-type>` | The type of metric definitions sought. |
| `applies_to_type` | no | `array<metric-definition-applies-to>` | The type of objects the metric definition applies to. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `include_custom_metrics` | no | `boolean` | Whether to include custom metrics in the response. If not set, then custom metrics are excluded. |
| `limit` | no | `integer` | The maximum number of records to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `sort_by` | no | `array<string>` | Fields to sort the records by and the direction to sort them. |
| `status` | no | `array<metric-definition-status>` | The status of the metric definition. |

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
curl -X POST "https://api.devrev.ai/metric-definitions.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "metric_definitions": [
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
      "name": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="metric-definitions-update"></a>

## `POST /metric-definitions.update`

**Update Metric Definition**

Source: <https://developer.devrev.ai/beta/api-reference/slas/metric-definitions-update>

Updates a custom metric definition

**Required scopes:**

- `metric_definition:write` OR `metric_definition:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `description` | no | `string` | The updated description of the purpose and operation of the metric.<br>*Format: text*<br>*Length: length <= 1024* |
| `id` | yes | `string` | The ID of the metric definition to update.<br>*Format: id* |
| `name` | no | `string` | The updated unique human readable name of the metric.<br>*Format: text*<br>*Length: 1 <= length <= 64* |
| `status` | no | `string` | The status of the metric. 'active' metrics can be used to create new SLAs, while 'inactive' metrics can not be used in new SLAs. Metrics can be updated between 'active' and 'inactive' states.<br>*Value in: "active" \| "inactive"* |

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
curl -X POST "https://api.devrev.ai/metric-definitions.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "metric_definition": {
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
    "name": "string"
  }
}
```

</details>


<a id="metric-trackers-get"></a>

## `GET /metric-trackers.get`

**Get Metric Tracker**

Source: <https://developer.devrev.ai/beta/api-reference/slas/metric-trackers-get>

Gets a metric tracker.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `metric` | yes | `string` | The ID of the metric that is being tracked.<br>*Format: id* |
| `object` | yes | `string` | The ID of the underlying object on which the metric is being tracked.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/metric-trackers.get?metric=string&object=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "metric_tracker": {
    "type": "time_metric_tracker",
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
    "active_intervals": [
      {}
    ],
    "last_started_at": "2023-01-01T12:00:00.000Z",
    "org_schedule": {
      "display_id": "string",
      "id": "string",
      "name": "string",
      "status": "archived",
      "timezone": "string",
      "valid_until": "2023-01-01T12:00:00.000Z",
      "version_number": 0
    },
    "status": "completed",
    "time_consumed": 0
  }
}
```

</details>


<a id="metric-trackers-get-post"></a>

## `POST /metric-trackers.get`

**Get Metric Tracker (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/slas/metric-trackers-get-post>

Gets a metric tracker.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `metric` | yes | `string` | The ID of the metric that is being tracked.<br>*Format: id* |
| `object` | yes | `string` | The ID of the underlying object on which the metric is being tracked.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/metric-trackers.get" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "string",
    "object": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "metric_tracker": {
    "type": "time_metric_tracker",
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
    "active_intervals": [
      {}
    ],
    "last_started_at": "2023-01-01T12:00:00.000Z",
    "org_schedule": {
      "display_id": "string",
      "id": "string",
      "name": "string",
      "status": "archived",
      "timezone": "string",
      "valid_until": "2023-01-01T12:00:00.000Z",
      "version_number": 0
    },
    "status": "completed",
    "time_consumed": 0
  }
}
```

</details>


<a id="sla-trackers-get"></a>

## `GET /sla-trackers.get`

**Get SLA Tracker**

Source: <https://developer.devrev.ai/beta/api-reference/slas/sla-trackers-get>

Gets an SLA tracker.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the SLA tracker to get.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/sla-trackers.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
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
  }
}
```

</details>


<a id="sla-trackers-get-post"></a>

## `POST /sla-trackers.get`

**Get SLA Tracker (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/slas/sla-trackers-get-post>

Gets an SLA tracker.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the SLA tracker to get.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/sla-trackers.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
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
  }
}
```

</details>


<a id="sla-trackers-list"></a>

## `GET /sla-trackers.list`

**List SLA Trackers**

Source: <https://developer.devrev.ai/beta/api-reference/slas/sla-trackers-list>

Lists SLA trackers matching a filter.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `created_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of SLA trackers to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `modified_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `modified_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `sort_by` | no | `array<string>` | Fields to sort the SLA Trackers by and the direction to sort them. |
| `stage` | no | `array<string>` | The SLA tracker stages the filter matches. |
| `status` | no | `array<string>` | The SLA tracker statuses the filter matches. |

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
curl -X GET "https://api.devrev.ai/sla-trackers.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "sla_trackers": [
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
    }
  ]
}
```

</details>


<a id="sla-trackers-list-post"></a>

## `POST /sla-trackers.list`

**List SLA Trackers (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/slas/sla-trackers-list-post>

Lists SLA trackers matching a filter.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_date` | no | `date-time-filter` |  |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of SLA trackers to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter` |  |
| `sort_by` | no | `array<string>` | Fields to sort the SLA Trackers by and the direction to sort them. |
| `stage` | no | `array<string>` | The SLA tracker stages the filter matches. |
| `status` | no | `array<string>` | The SLA tracker statuses the filter matches. |

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
curl -X POST "https://api.devrev.ai/sla-trackers.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "sla_trackers": [
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
    }
  ]
}
```

</details>


<a id="sla-trackers-remove-metric"></a>

## `POST /sla-trackers.remove-metric`

**Remove SLA Tracker Metric**

Source: <https://developer.devrev.ai/beta/api-reference/slas/sla-trackers-remove-metric>

Removes a metric from the given object's SLA.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `metric` | yes | `string` | ID of the metric that is to be removed. If the metric has already been removed, there will be no effect.<br>*Format: id* |
| `object` | yes | `string` | ID of the object from which the metric is to be removed.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/sla-trackers.remove-metric" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "string",
    "object": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
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
  }
}
```

</details>


<a id="assign"></a>

## `POST /slas.assign`

**Assign SLAs**

Source: <https://developer.devrev.ai/beta/api-reference/slas/assign>

Assigns the SLA to a set of Rev organizations.

**Required scopes:**

- `sla:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | no | `string` | The SLA which would be assigned to the Rev organizations. If omitted, the SLA of all the rev organizations referenced will be unset.<br>*Format: id* |
| `rev_orgs` | yes | `array<string>` | The Rev organizations to apply the SLA to. |

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
curl -X POST "https://api.devrev.ai/slas.assign" \
  -H "Content-Type: application/json" \
  -d '{
    "rev_orgs": [
      "REV-AbCdEfGh"
    ]
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "results": [
    {
      "error": {
        "type": "string",
        "message": "string",
        "status": 0
      },
      "rev_org": {
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    }
  ]
}
```

</details>


<a id="create"></a>

## `POST /slas.create`

**Create SLA**

Source: <https://developer.devrev.ai/beta/api-reference/slas/create>

Creates an SLA in draft status.

**Required scopes:**

- `sla:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `account_selector` | no | `accounts-filters` |  |
| `applies_to` | no | `array<sla-applies-to>` | The object types this SLA can apply to. |
| `description` | no | `string` | Description of the purpose and capabilities of the SLA.<br>*Format: text* |
| `evaluation_period` | no | `string` | Specifies the frequency of when the contractually-meaningful evaluation of the SLA happens. The organization for their own information might evaluate the various metrics contained in the policy as often as we can make it feasible for them, but only the evaluation at the end of the evaluation period triggers a compensation and needs to be shared with the customer.<br>*Value in: "monthly" \| "quarterly" \| "weekly" \| "yearly"* |
| `name` | yes | `string` | Human-readable name.<br>*Format: text* |
| `policies` | no | `array<set-sla-policy>` | The policies encompassed by this SLA, ordered in decreasing priority. |
| `sla_type` | no | `string` | Type of the SLA.<br>*Value in: "external" \| "internal"* |

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
curl -X POST "https://api.devrev.ai/slas.create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "sla": {
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
    "account_filter": {},
    "compensation": {},
    "description": "string",
    "evaluation_period": "monthly",
    "name": "string",
    "policies": [
      {}
    ],
    "sla_type": "external",
    "status": "archived"
  }
}
```

</details>


<a id="get"></a>

## `GET /slas.get`

**Get SLA**

Source: <https://developer.devrev.ai/beta/api-reference/slas/get>

Gets an SLA.

**Required scopes:**

- `sla:read` OR `sla:write`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the SLA to get.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/slas.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "sla": {
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
    "account_filter": {},
    "compensation": {},
    "description": "string",
    "evaluation_period": "monthly",
    "name": "string",
    "policies": [
      {}
    ],
    "sla_type": "external",
    "status": "archived"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /slas.get`

**Get SLA (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/slas/get-post>

Gets an SLA.

**Required scopes:**

- `sla:read` OR `sla:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the SLA to get.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/slas.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "sla": {
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
    "account_filter": {},
    "compensation": {},
    "description": "string",
    "evaluation_period": "monthly",
    "name": "string",
    "policies": [
      {}
    ],
    "sla_type": "external",
    "status": "archived"
  }
}
```

</details>


<a id="list"></a>

## `GET /slas.list`

**List SLAs**

Source: <https://developer.devrev.ai/beta/api-reference/slas/list>

Lists SLAs matching a filter.

**Required scopes:**

- `sla:read` OR `sla:write`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `applies_to` | no | `array<sla-applies-to>` | The object types the SLA applies to. |
| `applies_to_op` | no | `string` | The Filter operator to be applied on the applies to object types filter.<br>*Value in: "all" \| "any"* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of SLAs to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `sla_type` | no | `array<sla-type>` | The SLA types the filter matches. |
| `sort_by` | no | `array<string>` | Fields to sort the SLAs by and the direction to sort them. |
| `status` | no | `array<sla-status>` | The SLA statuses the filter matches. |

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
curl -X GET "https://api.devrev.ai/slas.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "slas": [
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
      "account_filter": {},
      "compensation": {},
      "description": "string",
      "evaluation_period": "monthly",
      "name": "string",
      "policies": [
        {}
      ],
      "sla_type": "external",
      "status": "archived"
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /slas.list`

**List SLAs (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/slas/list-post>

Lists SLAs matching a filter.

**Required scopes:**

- `sla:read` OR `sla:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `applies_to` | no | `array<sla-applies-to>` | The object types the SLA applies to. |
| `applies_to_op` | no | `string` | *Value in: "all" \| "any"* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of SLAs to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `sla_type` | no | `array<sla-type>` | The SLA types the filter matches. |
| `sort_by` | no | `array<string>` | Fields to sort the SLAs by and the direction to sort them. |
| `status` | no | `array<sla-status>` | The SLA statuses the filter matches. |

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
curl -X POST "https://api.devrev.ai/slas.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "slas": [
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
      "account_filter": {},
      "compensation": {},
      "description": "string",
      "evaluation_period": "monthly",
      "name": "string",
      "policies": [
        {}
      ],
      "sla_type": "external",
      "status": "archived"
    }
  ]
}
```

</details>


<a id="transition"></a>

## `POST /slas.transition`

**Transition SLAs**

Source: <https://developer.devrev.ai/beta/api-reference/slas/transition>

Changes the status of an SLA.

**Required scopes:**

- `sla:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The updated SLA.<br>*Format: id* |
| `status` | yes | `string` | Status determines how an item can be used. In 'draft' status an item can be edited but can't be used. When 'published' the item can longer be edited but can be used. 'Archived' is read-only.<br>*Value in: "archived" \| "draft" \| "published"* |

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
curl -X POST "https://api.devrev.ai/slas.transition" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string",
    "status": "archived"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "sla": {
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
    "account_filter": {},
    "compensation": {},
    "description": "string",
    "evaluation_period": "monthly",
    "name": "string",
    "policies": [
      {}
    ],
    "sla_type": "external",
    "status": "archived"
  }
}
```

</details>


<a id="update"></a>

## `POST /slas.update`

**Update SLA**

Source: <https://developer.devrev.ai/beta/api-reference/slas/update>

Updates a draft SLA.

**Required scopes:**

- `sla:write`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `account_selector` | no | `accounts-filters` |  |
| `description` | no | `string` | Description of the purpose and capabilities of the SLA.<br>*Format: text* |
| `evaluation_period` | no | `string` | Specifies the frequency of when the contractually-meaningful evaluation of the SLA happens. The organization for their own information might evaluate the various metrics contained in the policy as often as we can make it feasible for them, but only the evaluation at the end of the evaluation period triggers a compensation and needs to be shared with the customer.<br>*Value in: "monthly" \| "quarterly" \| "weekly" \| "yearly"* |
| `id` | yes | `string` | The SLA's ID.<br>*Format: id* |
| `name` | no | `string` | Human-readable name.<br>*Format: text* |
| `policies` | no | `array<set-sla-policy>` | The policies encompassed by this SLA, ordered in decreasing priority, the whole array will be overwritten by the contents of this array. |

### Response codes

- `201` — `application/json`
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
curl -X POST "https://api.devrev.ai/slas.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "sla": {
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
    "account_filter": {},
    "compensation": {},
    "description": "string",
    "evaluation_period": "monthly",
    "name": "string",
    "policies": [
      {}
    ],
    "sla_type": "external",
    "status": "archived"
  }
}
```

</details>
