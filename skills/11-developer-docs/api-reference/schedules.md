# Schedules

Source: <https://developer.devrev.ai/api-reference/schedules>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/org-schedule-fragments.create` | [org-schedule-fragments-create](#org-schedule-fragments-create) |
| GET | `/org-schedule-fragments.get` | [org-schedule-fragments-get](#org-schedule-fragments-get) |
| POST | `/org-schedule-fragments.get` | [org-schedule-fragments-get-post](#org-schedule-fragments-get-post) |
| POST | `/org-schedule-fragments.transition` | [org-schedule-fragments-transition](#org-schedule-fragments-transition) |
| POST | `/org-schedules.create` | [org-schedules-create](#org-schedules-create) |
| GET | `/org-schedules.evaluate` | [org-schedules-evaluate](#org-schedules-evaluate) |
| POST | `/org-schedules.evaluate` | [org-schedules-evaluate-post](#org-schedules-evaluate-post) |
| GET | `/org-schedules.get` | [org-schedules-get](#org-schedules-get) |
| POST | `/org-schedules.get` | [org-schedules-get-post](#org-schedules-get-post) |
| GET | `/org-schedules.list` | [org-schedules-list](#org-schedules-list) |
| POST | `/org-schedules.list` | [org-schedules-list-post](#org-schedules-list-post) |
| POST | `/org-schedules.set-future` | [org-schedules-set-future](#org-schedules-set-future) |
| POST | `/org-schedules.transition` | [org-schedules-transition](#org-schedules-transition) |
| POST | `/org-schedules.update` | [org-schedules-update](#org-schedules-update) |

<a id="org-schedule-fragments-create"></a>

## `POST /org-schedule-fragments.create`

**Create Org Schedule Fragment**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedule-fragments-create>

Creates an organization schedule fragment.

**Required scopes:**

- `org_schedule_fragment:write` OR `org_schedule_fragment:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `from` | yes | `string` | Date (inclusive) on which the organization schedule fragment begins.<br>*Format: date-time* |
| `intervals` | yes | `array<create-org-schedule-interval>` | The intervals that comprise the schedule fragment. |
| `name` | yes | `string` | Name of the organization schedule fragment.<br>*Format: text* |
| `region_codes` | no | `array<string>` | CLDR region code of the countries/regions it is meant to be valid for. Does not drive logic, serves only for easier filtering and organization. |
| `to` | yes | `string` | Date (exclusive) on which the organization schedule fragment's validity ends.<br>*Format: date-time* |

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
curl -X POST "https://api.devrev.ai/org-schedule-fragments.create" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "2023-01-01T12:00:00.000Z",
    "intervals": [
      {
        "from": "2023-01-01T12:00:00.000Z",
        "name": "string"
      }
    ],
    "name": "string",
    "to": "2023-01-01T12:00:00.000Z"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "org_schedule_fragment": {
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
    "from": "2023-01-01T12:00:00.000Z",
    "intervals": [
      {
        "from": "2023-01-01T12:00:00.000Z",
        "is_excluded": true,
        "name": "string",
        "to": "2023-01-01T12:00:00.000Z"
      }
    ],
    "name": "string",
    "region_codes": [
      "string"
    ],
    "status": "archived",
    "to": "2023-01-01T12:00:00.000Z"
  }
}
```

</details>


<a id="org-schedule-fragments-get"></a>

## `GET /org-schedule-fragments.get`

**Get Org Schedule Fragment**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedule-fragments-get>

Gets an organization schedule fragment.

**Required scopes:**

- `org_schedule_fragment:read` OR `org_schedule_fragment:write` OR `org_schedule_fragment:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | Organization schedule Fragment ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/org-schedule-fragments.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "org_schedule_fragment": {
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
    "from": "2023-01-01T12:00:00.000Z",
    "intervals": [
      {
        "from": "2023-01-01T12:00:00.000Z",
        "is_excluded": true,
        "name": "string",
        "to": "2023-01-01T12:00:00.000Z"
      }
    ],
    "name": "string",
    "region_codes": [
      "string"
    ],
    "status": "archived",
    "to": "2023-01-01T12:00:00.000Z"
  }
}
```

</details>


<a id="org-schedule-fragments-get-post"></a>

## `POST /org-schedule-fragments.get`

**Get Org Schedule Fragment (POST)**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedule-fragments-get-post>

Gets an organization schedule fragment.

**Required scopes:**

- `org_schedule_fragment:read` OR `org_schedule_fragment:write` OR `org_schedule_fragment:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | Organization schedule Fragment ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/org-schedule-fragments.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "org_schedule_fragment": {
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
    "from": "2023-01-01T12:00:00.000Z",
    "intervals": [
      {
        "from": "2023-01-01T12:00:00.000Z",
        "is_excluded": true,
        "name": "string",
        "to": "2023-01-01T12:00:00.000Z"
      }
    ],
    "name": "string",
    "region_codes": [
      "string"
    ],
    "status": "archived",
    "to": "2023-01-01T12:00:00.000Z"
  }
}
```

</details>


<a id="org-schedule-fragments-transition"></a>

## `POST /org-schedule-fragments.transition`

**Transition Org Schedule Fragments**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedule-fragments-transition>

Changes stage of an organization schedule fragment.

**Required scopes:**

- `org_schedule_fragment:write` OR `org_schedule_fragment:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | Organization schedule Fragment ID.<br>*Format: id* |
| `status` | yes | `string` | Status determines how an item can be used. In 'draft' status an item can be edited but can't be used. When 'published' the item can longer be edited but can be used. 'Archived' is read-only.<br>*Value in: "archived" \| "draft" \| "published"* |

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
curl -X POST "https://api.devrev.ai/org-schedule-fragments.transition" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string",
    "status": "archived"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "org_schedule_fragment": {
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
    "from": "2023-01-01T12:00:00.000Z",
    "intervals": [
      {
        "from": "2023-01-01T12:00:00.000Z",
        "is_excluded": true,
        "name": "string",
        "to": "2023-01-01T12:00:00.000Z"
      }
    ],
    "name": "string",
    "region_codes": [
      "string"
    ],
    "status": "archived",
    "to": "2023-01-01T12:00:00.000Z"
  }
}
```

</details>


<a id="org-schedules-create"></a>

## `POST /org-schedules.create`

**Create Org Schedule**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedules-create>

Creates an organization schedule with a default weekly organization schedule and a list of organization schedule fragments.

**Required scopes:**

- `org_schedule:write` OR `org_schedule:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `default_weekly_org_schedule` | no | `set-weekly-org-schedule` |  |
| `min_valid_days` | no | `integer` | Organization schedule must be valid for at least this many days in the future. Meaning organization schedule fragments must cover this period. 0 if omitted.<br>*Format: int64* |
| `name` | yes | `string` | Human-readable name.<br>*Format: text* |
| `org_schedule_fragments` | no | `array<set-org-schedule-fragment-summary>` | List of organization schedule fragments with no overlaps or gaps. |
| `timezone` | yes | `string` | Timezone in which the organization schedule applies. Expected to be a valid IANA time zone name such as America/New_York.<br>*Format: text* |
| `weekly_org_schedules` | no | `array<set-weekly-org-schedule>` | If this day belongs to a named period according to the currently active organization schedule fragment, a weekly organization schedule from this list with the corresponding name will apply. |

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
curl -X POST "https://api.devrev.ai/org-schedules.create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "string",
    "timezone": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "org_schedule": {
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
    "default_weekly_org_schedule": {
      "intervals": [
        {
          "from": 0,
          "to": 0
        }
      ],
      "period_name": "string"
    },
    "min_valid_days": 0,
    "name": "string",
    "org_schedule_fragments": [
      {
        "from": "2023-01-01T12:00:00.000Z",
        "id": "string",
        "to": "2023-01-01T12:00:00.000Z"
      }
    ],
    "status": "archived",
    "timezone": "string",
    "valid_until": "2023-01-01T12:00:00.000Z",
    "version_number": 0,
    "weekly_org_schedules": [
      {
        "intervals": [
          {
            "from": 0,
            "to": 0
          }
        ],
        "period_name": "string"
      }
    ]
  }
}
```

</details>


<a id="org-schedules-evaluate"></a>

## `GET /org-schedules.evaluate`

**Evaluate Org Schedules**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedules-evaluate>

Evaluates an organization's schedule at specified instants.

**Required scopes:**

- `org_schedule:read` OR `org_schedule:write` OR `org_schedule:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | Organization schedule ID.<br>*Format: id* |
| `instants` | yes | `array<string>` | Time instants to evaluate the organization schedule for.<br>*Items: 1 <= items* |

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
curl -X GET "https://api.devrev.ai/org-schedules.evaluate?id=string&instants=2023-01-01T12%3A00%3A00.000Z"
```

<details><summary>Example 200 response</summary>

```json
{
  "instant_evaluations": [
    {
      "at": "2023-01-01T12:00:00.000Z",
      "definedness": "immutable",
      "is_active": true,
      "next_transition": "2023-01-01T12:00:00.000Z"
    }
  ]
}
```

</details>


<a id="org-schedules-evaluate-post"></a>

## `POST /org-schedules.evaluate`

**Evaluate Org Schedules (POST)**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedules-evaluate-post>

Evaluates an organization's schedule at specified instants.

**Required scopes:**

- `org_schedule:read` OR `org_schedule:write` OR `org_schedule:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | Organization schedule ID.<br>*Format: id* |
| `instants` | yes | `array<string>` | Time instants to evaluate the organization schedule for.<br>*Items: 1 <= items* |

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
curl -X POST "https://api.devrev.ai/org-schedules.evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string",
    "instants": [
      "2023-01-01T12:00:00.000Z"
    ]
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "instant_evaluations": [
    {
      "at": "2023-01-01T12:00:00.000Z",
      "definedness": "immutable",
      "is_active": true,
      "next_transition": "2023-01-01T12:00:00.000Z"
    }
  ]
}
```

</details>


<a id="org-schedules-get"></a>

## `GET /org-schedules.get`

**Get Org Schedule**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedules-get>

Gets an organization schedule.

**Required scopes:**

- `org_schedule:read` OR `org_schedule:write` OR `org_schedule:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | Organization schedule ID.<br>*Format: id* |
| `version_number` | no | `integer` | Specific version of the organization schedule to retrieve. If not provided, returns the latest version.<br>*Format: int64* |

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
curl -X GET "https://api.devrev.ai/org-schedules.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "org_schedule": {
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
    "default_weekly_org_schedule": {
      "intervals": [
        {
          "from": 0,
          "to": 0
        }
      ],
      "period_name": "string"
    },
    "min_valid_days": 0,
    "name": "string",
    "org_schedule_fragments": [
      {
        "from": "2023-01-01T12:00:00.000Z",
        "id": "string",
        "to": "2023-01-01T12:00:00.000Z"
      }
    ],
    "status": "archived",
    "timezone": "string",
    "valid_until": "2023-01-01T12:00:00.000Z",
    "version_number": 0,
    "weekly_org_schedules": [
      {
        "intervals": [
          {
            "from": 0,
            "to": 0
          }
        ],
        "period_name": "string"
      }
    ]
  }
}
```

</details>


<a id="org-schedules-get-post"></a>

## `POST /org-schedules.get`

**Get Org Schedule (POST)**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedules-get-post>

Gets an organization schedule.

**Required scopes:**

- `org_schedule:read` OR `org_schedule:write` OR `org_schedule:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | Organization schedule ID.<br>*Format: id* |
| `version_number` | no | `integer` | Specific version of the organization schedule to retrieve. If not provided, returns the latest version.<br>*Format: int64* |

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
curl -X POST "https://api.devrev.ai/org-schedules.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "org_schedule": {
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
    "default_weekly_org_schedule": {
      "intervals": [
        {
          "from": 0,
          "to": 0
        }
      ],
      "period_name": "string"
    },
    "min_valid_days": 0,
    "name": "string",
    "org_schedule_fragments": [
      {
        "from": "2023-01-01T12:00:00.000Z",
        "id": "string",
        "to": "2023-01-01T12:00:00.000Z"
      }
    ],
    "status": "archived",
    "timezone": "string",
    "valid_until": "2023-01-01T12:00:00.000Z",
    "version_number": 0,
    "weekly_org_schedules": [
      {
        "intervals": [
          {
            "from": 0,
            "to": 0
          }
        ],
        "period_name": "string"
      }
    ]
  }
}
```

</details>


<a id="org-schedules-list"></a>

## `GET /org-schedules.list`

**List Org Schedules**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedules-list>

Gets list of organization schedules.

**Required scopes:**

- `org_schedule:read` OR `org_schedule:write` OR `org_schedule:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by_id` | no | `array<string>` | Creator ID the filter matches. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | Max number of organization schedules returned in a page. Default is 50.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `status` | no | `array<org-schedule-status>` | The organization schedule statuses the filter matches. |

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
curl -X GET "https://api.devrev.ai/org-schedules.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "org_schedules": [
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
      "default_weekly_org_schedule": {
        "intervals": [
          {
            "from": 0,
            "to": 0
          }
        ],
        "period_name": "string"
      },
      "min_valid_days": 0,
      "name": "string",
      "org_schedule_fragments": [
        {
          "from": "2023-01-01T12:00:00.000Z",
          "id": "string",
          "to": "2023-01-01T12:00:00.000Z"
        }
      ],
      "status": "archived",
      "timezone": "string",
      "valid_until": "2023-01-01T12:00:00.000Z",
      "version_number": 0,
      "weekly_org_schedules": [
        {
          "intervals": [
            {
              "from": 0,
              "to": 0
            }
          ],
          "period_name": "string"
        }
      ]
    }
  ],
  "prev_cursor": "string"
}
```

</details>


<a id="org-schedules-list-post"></a>

## `POST /org-schedules.list`

**List Org Schedules (POST)**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedules-list-post>

Gets list of organization schedules.

**Required scopes:**

- `org_schedule:read` OR `org_schedule:write` OR `org_schedule:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by_id` | no | `array<string>` | Creator ID the filter matches. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | Max number of organization schedules returned in a page. Default is 50.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `status` | no | `array<org-schedule-status>` | The organization schedule statuses the filter matches. |
| `valid_until` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |

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
curl -X POST "https://api.devrev.ai/org-schedules.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "org_schedules": [
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
      "default_weekly_org_schedule": {
        "intervals": [
          {
            "from": 0,
            "to": 0
          }
        ],
        "period_name": "string"
      },
      "min_valid_days": 0,
      "name": "string",
      "org_schedule_fragments": [
        {
          "from": "2023-01-01T12:00:00.000Z",
          "id": "string",
          "to": "2023-01-01T12:00:00.000Z"
        }
      ],
      "status": "archived",
      "timezone": "string",
      "valid_until": "2023-01-01T12:00:00.000Z",
      "version_number": 0,
      "weekly_org_schedules": [
        {
          "intervals": [
            {
              "from": 0,
              "to": 0
            }
          ],
          "period_name": "string"
        }
      ]
    }
  ],
  "prev_cursor": "string"
}
```

</details>


<a id="org-schedules-set-future"></a>

## `POST /org-schedules.set-future`

**Set-Future Org Schedules**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedules-set-future>

Sets next organization schedule fragment which must begin the day the last existing fragment ends.

**Required scopes:**

- `org_schedule:write` OR `org_schedule:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | Organization schedule ID.<br>*Format: id* |
| `org_schedule_fragment_id` | yes | `string` | Organization schedule Fragment ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/org-schedules.set-future" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string",
    "org_schedule_fragment_id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "org_schedule": {
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
    "default_weekly_org_schedule": {
      "intervals": [
        {
          "from": 0,
          "to": 0
        }
      ],
      "period_name": "string"
    },
    "min_valid_days": 0,
    "name": "string",
    "org_schedule_fragments": [
      {
        "from": "2023-01-01T12:00:00.000Z",
        "id": "string",
        "to": "2023-01-01T12:00:00.000Z"
      }
    ],
    "status": "archived",
    "timezone": "string",
    "valid_until": "2023-01-01T12:00:00.000Z",
    "version_number": 0,
    "weekly_org_schedules": [
      {
        "intervals": [
          {
            "from": 0,
            "to": 0
          }
        ],
        "period_name": "string"
      }
    ]
  }
}
```

</details>


<a id="org-schedules-transition"></a>

## `POST /org-schedules.transition`

**Transition Org Schedules**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedules-transition>

Publishes or archives an organization schedule.

**Required scopes:**

- `org_schedule:write` OR `org_schedule:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | Organization schedule ID.<br>*Format: id* |
| `status` | yes | `string` | Status determines how an item can be used. In 'draft' status an item can be edited but can't be used. When 'published' the item can longer be edited but can be used. 'Archived' is read-only.<br>*Value in: "archived" \| "draft" \| "published"* |

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
curl -X POST "https://api.devrev.ai/org-schedules.transition" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string",
    "status": "archived"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "org_schedule": {
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
    "default_weekly_org_schedule": {
      "intervals": [
        {
          "from": 0,
          "to": 0
        }
      ],
      "period_name": "string"
    },
    "min_valid_days": 0,
    "name": "string",
    "org_schedule_fragments": [
      {
        "from": "2023-01-01T12:00:00.000Z",
        "id": "string",
        "to": "2023-01-01T12:00:00.000Z"
      }
    ],
    "status": "archived",
    "timezone": "string",
    "valid_until": "2023-01-01T12:00:00.000Z",
    "version_number": 0,
    "weekly_org_schedules": [
      {
        "intervals": [
          {
            "from": 0,
            "to": 0
          }
        ],
        "period_name": "string"
      }
    ]
  }
}
```

</details>


<a id="org-schedules-update"></a>

## `POST /org-schedules.update`

**Update Org Schedule**

Source: <https://developer.devrev.ai/api-reference/schedules/org-schedules-update>

Updates an organization schedule.

**Required scopes:**

- `org_schedule:write` OR `org_schedule:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `default_weekly_org_schedule` | no | `set-weekly-org-schedule` |  |
| `id` | yes | `string` | Organization schedule ID.<br>*Format: id* |
| `min_valid_days` | no | `integer` | Organization schedule must be valid for at least this many days in the future. Meaning organization schedule fragments must cover this period. 0 if omitted.<br>*Format: int64* |
| `name` | no | `string` | Human-readable name.<br>*Format: text* |
| `org_schedule_fragments` | no | `array<set-org-schedule-fragment-summary>` | List of organization schedule fragments with no overlaps or gaps. |
| `timezone` | no | `string` | Timezone in which the organization schedule applies. Expected to be a valid IANA time zone name such as America/New_York.<br>*Format: text* |
| `weekly_org_schedules` | no | `array<set-weekly-org-schedule>` | If this day belongs to a named period according to the currently active organization schedule fragment, a weekly organization schedule from this list with the corresponding name will apply. |

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
curl -X POST "https://api.devrev.ai/org-schedules.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "org_schedule": {
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
    "default_weekly_org_schedule": {
      "intervals": [
        {
          "from": 0,
          "to": 0
        }
      ],
      "period_name": "string"
    },
    "min_valid_days": 0,
    "name": "string",
    "org_schedule_fragments": [
      {
        "from": "2023-01-01T12:00:00.000Z",
        "id": "string",
        "to": "2023-01-01T12:00:00.000Z"
      }
    ],
    "status": "archived",
    "timezone": "string",
    "valid_until": "2023-01-01T12:00:00.000Z",
    "version_number": 0,
    "weekly_org_schedules": [
      {
        "intervals": [
          {
            "from": 0,
            "to": 0
          }
        ],
        "period_name": "string"
      }
    ]
  }
}
```

</details>
