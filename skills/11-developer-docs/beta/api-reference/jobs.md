# Jobs

Source: <https://developer.devrev.ai/beta/api-reference/jobs>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/jobs.get` | [get-job](#get-job) |
| POST | `/jobs.get` | [get-job-post](#get-job-post) |
| GET | `/jobs.list` | [list-jobs](#list-jobs) |
| POST | `/jobs.list` | [list-jobs-post](#list-jobs-post) |

<a id="get-job"></a>

## `GET /jobs.get`

**Get Job**

Source: <https://developer.devrev.ai/beta/api-reference/jobs/get-job>

Retrieves a job's information.

**Required scopes:**

- `job:read`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the job to be retrieved.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/jobs.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "job": {
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
    "job_category": "bulk_upgrade",
    "job_id": "string",
    "metadata_list": [
      {
        "type": "bool",
        "key": "string",
        "value": "string"
      }
    ],
    "output_artifacts": [
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
    "progress": 0,
    "retry_count": 0,
    "state": "completed",
    "title": "string"
  }
}
```

</details>


<a id="get-job-post"></a>

## `POST /jobs.get`

**Get Job (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/jobs/get-job-post>

Retrieves a job's information.

**Required scopes:**

- `job:read`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the job to be retrieved.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/jobs.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "job": {
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
    "job_category": "bulk_upgrade",
    "job_id": "string",
    "metadata_list": [
      {
        "type": "bool",
        "key": "string",
        "value": "string"
      }
    ],
    "output_artifacts": [
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
    "progress": 0,
    "retry_count": 0,
    "state": "completed",
    "title": "string"
  }
}
```

</details>


<a id="list-jobs"></a>

## `GET /jobs.list`

**List Jobs**

Source: <https://developer.devrev.ai/beta/api-reference/jobs/list-jobs>

Gets a list of jobs.

**Required scopes:**

- `job:read`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `category` | no | `array<job-category>` | Filters on job category. |
| `created_by` | no | `array<string>` | Filters for jobs created by the specified user(s). |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of jobs to return per page. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `owned_by_id` | no | `array<string>` | Filters on the user who owns the job. |
| `parent_ids` | no | `array<string>` | Filters on parent ids for jobs. |
| `sort_by` | no | `array<string>` | Fields to sort the jobs by and the direction to sort them in. |
| `state` | no | `array<job-state>` | Filters on job state. |

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
curl -X GET "https://api.devrev.ai/jobs.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "jobs": [
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
      "job_category": "bulk_upgrade",
      "job_id": "string",
      "metadata_list": [
        {
          "type": "bool",
          "key": "string",
          "value": "string"
        }
      ],
      "output_artifacts": [
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
      "progress": 0,
      "retry_count": 0,
      "state": "completed",
      "title": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="list-jobs-post"></a>

## `POST /jobs.list`

**List Jobs (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/jobs/list-jobs-post>

Gets a list of jobs.

**Required scopes:**

- `job:read`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `category` | no | `array<job-category>` | Filters on job category. |
| `created_by` | no | `array<string>` | Filters for jobs created by the specified user(s). |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of jobs to return per page. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `owned_by_id` | no | `array<string>` | Filters on the user who owns the job. |
| `parent_ids` | no | `array<string>` | Filters on parent ids for jobs. |
| `sort_by` | no | `array<string>` | Fields to sort the jobs by and the direction to sort them in. |
| `state` | no | `array<job-state>` | Filters on job state. |

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
curl -X POST "https://api.devrev.ai/jobs.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "jobs": [
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
      "job_category": "bulk_upgrade",
      "job_id": "string",
      "metadata_list": [
        {
          "type": "bool",
          "key": "string",
          "value": "string"
        }
      ],
      "output_artifacts": [
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
      "progress": 0,
      "retry_count": 0,
      "state": "completed",
      "title": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>
