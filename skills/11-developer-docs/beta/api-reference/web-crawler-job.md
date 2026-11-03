# Web Crawler Job

Source: <https://developer.devrev.ai/beta/api-reference/web-crawler-job>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/web-crawler-jobs.control` | [web-crawler-jobs-control](#web-crawler-jobs-control) |
| POST | `/web-crawler-jobs.create` | [create-web-crawler-job](#create-web-crawler-job) |
| GET | `/web-crawler-jobs.get` | [get-web-crawler-job](#get-web-crawler-job) |
| POST | `/web-crawler-jobs.get` | [get-web-crawler-job-post](#get-web-crawler-job-post) |
| GET | `/web-crawler-jobs.list` | [list-web-crawler-jobs](#list-web-crawler-jobs) |
| POST | `/web-crawler-jobs.list` | [list-web-crawler-jobs-post](#list-web-crawler-jobs-post) |

<a id="web-crawler-jobs-control"></a>

## `POST /web-crawler-jobs.control`

**Control Web Crawler Jobs**

Source: <https://developer.devrev.ai/beta/api-reference/web-crawler-job/web-crawler-jobs-control>

Change state of a web crawler job to pause or resume it back to running.

**Required scopes:**

- `web_crawler_job:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `action` | yes | `string` | *Value in: "abort" \| "pause" \| "resume"* |
| `id` | yes | `string` | The ID of the job.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/web-crawler-jobs.control" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "abort",
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "web_crawler_job": {
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
    "accept_regexs": [
      "string"
    ],
    "description": "string",
    "domain_names": [
      "string"
    ],
    "frequency": 0,
    "language_code": "string",
    "max_depth": 0,
    "no_parent": true,
    "notify_on_complete": true,
    "num_bytes": 0,
    "num_timeout_urls": 0,
    "num_urls_scraped": 0,
    "reject_regexs": [
      "string"
    ],
    "sitemap_index_urls": [
      "string"
    ],
    "sitemap_urls": [
      "string"
    ],
    "state": "aborted",
    "urls": [
      "string"
    ],
    "user_agent": "string"
  }
}
```

</details>


<a id="create-web-crawler-job"></a>

## `POST /web-crawler-jobs.create`

**Create Web Crawler Job**

Source: <https://developer.devrev.ai/beta/api-reference/web-crawler-job/create-web-crawler-job>

Creates a web crawler job whose objective is to crawl the provided URLs/sitemaps and generate corresponding webpages as artifacts.

**Required scopes:**

- `web_crawler_job:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `accept_regex` | no | `string` | **Deprecated.**<br>The regex a URL must satisfy to be crawled.<br>*Format: text* |
| `accept_regexes` | no | `array<string>` | The list of regexes a URL must satisfy to be crawled.<br>*Items: items <= 100* |
| `applies_to_parts` | yes | `array<string>` | The parts to which created webpage/articles during this crawler job will be linked to.<br>*Items: 1 <= items <= 1* |
| `description` | no | `string` | The description of the job.<br>*Format: text* |
| `domain_names` | no | `array<string>` | The list of allowed domain names to crawl. |
| `frequency` | no | `integer` | Number of days between re-sync job runs. If 0, the job will run only once.<br>*Format: int32* |
| `language_code` | no | `string` | Language code of the articles created by the job.<br>*Format: text*<br>*Length: length <= 10* |
| `max_depth` | no | `integer` | The maximum depth to crawl.<br>*Format: int32* |
| `notify_on_complete` | no | `boolean` | Whether to notify the user when the job is complete. Default is true. |
| `reject_regex` | no | `string` | **Deprecated.**<br>The regex which if satisfied by a URL results in rejection of the URL. If a URL matches both accept and reject regexes, it is rejected.<br>*Format: text* |
| `reject_regexes` | no | `array<string>` | The list of regexes which if satisfied by a URL results in rejection of the URL. If a URL matches both accept and reject regexes, it is rejected.<br>*Items: items <= 100* |
| `sitemap_index_urls` | no | `array<string>` | The list of sitemap index URLs to crawl.<br>*Items: items <= 2* |
| `sitemap_urls` | no | `array<string>` | The list of sitemap URLs to crawl.<br>*Items: items <= 2* |
| `urls` | no | `array<string>` | The list of URLs to crawl.<br>*Items: items <= 50* |
| `user_agent` | no | `string` | User agent to use for crawling websites in this job.<br>*Format: text*<br>*Length: length <= 1024* |

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
curl -X POST "https://api.devrev.ai/web-crawler-jobs.create" \
  -H "Content-Type: application/json" \
  -d '{
    "applies_to_parts": [
      "PROD-12345"
    ]
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "web_crawler_job": {
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
    "accept_regexs": [
      "string"
    ],
    "description": "string",
    "domain_names": [
      "string"
    ],
    "frequency": 0,
    "language_code": "string",
    "max_depth": 0,
    "no_parent": true,
    "notify_on_complete": true,
    "num_bytes": 0,
    "num_timeout_urls": 0,
    "num_urls_scraped": 0,
    "reject_regexs": [
      "string"
    ],
    "sitemap_index_urls": [
      "string"
    ],
    "sitemap_urls": [
      "string"
    ],
    "state": "aborted",
    "urls": [
      "string"
    ],
    "user_agent": "string"
  }
}
```

</details>


<a id="get-web-crawler-job"></a>

## `GET /web-crawler-jobs.get`

**Get Web Crawler Job**

Source: <https://developer.devrev.ai/beta/api-reference/web-crawler-job/get-web-crawler-job>

Gets a web crawler job.

**Required scopes:**

- `web_crawler_job:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the job.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/web-crawler-jobs.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "web_crawler_job": {
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
    "accept_regexs": [
      "string"
    ],
    "description": "string",
    "domain_names": [
      "string"
    ],
    "frequency": 0,
    "language_code": "string",
    "max_depth": 0,
    "no_parent": true,
    "notify_on_complete": true,
    "num_bytes": 0,
    "num_timeout_urls": 0,
    "num_urls_scraped": 0,
    "reject_regexs": [
      "string"
    ],
    "sitemap_index_urls": [
      "string"
    ],
    "sitemap_urls": [
      "string"
    ],
    "state": "aborted",
    "urls": [
      "string"
    ],
    "user_agent": "string"
  }
}
```

</details>


<a id="get-web-crawler-job-post"></a>

## `POST /web-crawler-jobs.get`

**Get Web Crawler Job (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/web-crawler-job/get-web-crawler-job-post>

Gets a web crawler job.

**Required scopes:**

- `web_crawler_job:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the job.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/web-crawler-jobs.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "web_crawler_job": {
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
    "accept_regexs": [
      "string"
    ],
    "description": "string",
    "domain_names": [
      "string"
    ],
    "frequency": 0,
    "language_code": "string",
    "max_depth": 0,
    "no_parent": true,
    "notify_on_complete": true,
    "num_bytes": 0,
    "num_timeout_urls": 0,
    "num_urls_scraped": 0,
    "reject_regexs": [
      "string"
    ],
    "sitemap_index_urls": [
      "string"
    ],
    "sitemap_urls": [
      "string"
    ],
    "state": "aborted",
    "urls": [
      "string"
    ],
    "user_agent": "string"
  }
}
```

</details>


<a id="list-web-crawler-jobs"></a>

## `GET /web-crawler-jobs.list`

**List Web Crawler Jobs**

Source: <https://developer.devrev.ai/beta/api-reference/web-crawler-job/list-web-crawler-jobs>

Lists web crawler jobs.

**Required scopes:**

- `web_crawler_job:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for web crawler jobs created by any of the provided users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of web crawler jobs to return. The default is '50'.<br>*Format: int32* |
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
curl -X GET "https://api.devrev.ai/web-crawler-jobs.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "web_crawler_jobs": [
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
      "accept_regexs": [
        "string"
      ],
      "description": "string",
      "domain_names": [
        "string"
      ],
      "frequency": 0,
      "language_code": "string",
      "max_depth": 0,
      "no_parent": true,
      "notify_on_complete": true,
      "num_bytes": 0,
      "num_timeout_urls": 0,
      "num_urls_scraped": 0,
      "reject_regexs": [
        "string"
      ],
      "sitemap_index_urls": [
        "string"
      ],
      "sitemap_urls": [
        "string"
      ],
      "state": "aborted",
      "urls": [
        "string"
      ],
      "user_agent": "string"
    }
  ]
}
```

</details>


<a id="list-web-crawler-jobs-post"></a>

## `POST /web-crawler-jobs.list`

**List Web Crawler Jobs (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/web-crawler-job/list-web-crawler-jobs-post>

Lists web crawler jobs.

**Required scopes:**

- `web_crawler_job:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for web crawler jobs created by any of the provided users. |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of web crawler jobs to return. The default is '50'.<br>*Format: int32* |
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
curl -X POST "https://api.devrev.ai/web-crawler-jobs.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "web_crawler_jobs": [
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
      "accept_regexs": [
        "string"
      ],
      "description": "string",
      "domain_names": [
        "string"
      ],
      "frequency": 0,
      "language_code": "string",
      "max_depth": 0,
      "no_parent": true,
      "notify_on_complete": true,
      "num_bytes": 0,
      "num_timeout_urls": 0,
      "num_urls_scraped": 0,
      "reject_regexs": [
        "string"
      ],
      "sitemap_index_urls": [
        "string"
      ],
      "sitemap_urls": [
        "string"
      ],
      "state": "aborted",
      "urls": [
        "string"
      ],
      "user_agent": "string"
    }
  ]
}
```

</details>
