# Event Sources

Source: <https://developer.devrev.ai/beta/api-reference/event-sources>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/event-sources.get` | [get](#get) |
| POST | `/event-sources.get` | [get-post](#get-post) |
| POST | `/event-sources.schedule` | [schedule-event](#schedule-event) |
| POST | `/event-sources.unschedule` | [delete-scheduled-event](#delete-scheduled-event) |
| POST | `/track-events.publish` | [track-events-publish](#track-events-publish) |

<a id="get"></a>

## `GET /event-sources.get`

**Get Event Source**

Source: <https://developer.devrev.ai/beta/api-reference/event-sources/get>

Gets an event source.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The event source's ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/event-sources.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "event_source": {
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
    "config": {},
    "name": "string",
    "setup_instructions": {
      "content": "string"
    },
    "status": "active",
    "trigger_url": "string"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /event-sources.get`

**Get Event Source (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/event-sources/get-post>

Gets an event source.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The event source's ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/event-sources.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "event_source": {
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
    "config": {},
    "name": "string",
    "setup_instructions": {
      "content": "string"
    },
    "status": "active",
    "trigger_url": "string"
  }
}
```

</details>


<a id="schedule-event"></a>

## `POST /event-sources.schedule`

**Schedule Event Sources**

Source: <https://developer.devrev.ai/beta/api-reference/event-sources/schedule-event>

Schedules an event to be published to the specified event source.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `event_key` | no | `string` | A unique key for this event (scoped to an event source) used for updating/getting/deleting scheduled events.<br>*Format: text* |
| `event_type` | yes | `string` | The type of the event.<br>*Format: text* |
| `id` | yes | `string` | The event source's ID.<br>*Format: id* |
| `payload` | yes | `string` | The raw payload of the event. |
| `publish_at` | no | `string` | The timestamp at which the event should be published. The event is guaranteed to be published after this. If omitted, the event is published immediately.<br>*Format: date-time* |
| `update_if_exists` | no | `boolean` | Whether or not to update an existing scheduled event with the same event key. If this is false, and an event is already scheduled with the same event key, then HTTP 409 Conflict is returned. |

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
curl -X POST "https://api.devrev.ai/event-sources.schedule" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "string",
    "id": "string",
    "payload": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "event_key": "string"
}
```

</details>


<a id="delete-scheduled-event"></a>

## `POST /event-sources.unschedule`

**Unschedule Event Sources**

Source: <https://developer.devrev.ai/beta/api-reference/event-sources/delete-scheduled-event>

Deletes an event scheduled for the specified event source.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `event_key` | yes | `string` | The event key for the event which we want to delete.<br>*Format: text* |
| `id` | yes | `string` | The event source's ID.<br>*Format: id* |

### Response codes

- `200` — empty body
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
curl -X POST "https://api.devrev.ai/event-sources.unschedule" \
  -H "Content-Type: application/json" \
  -d '{
    "event_key": "string",
    "id": "string"
  }'
```


<a id="track-events-publish"></a>

## `POST /track-events.publish`

**Publish Track Events**

Source: <https://developer.devrev.ai/beta/api-reference/event-sources/track-events-publish>

Allows publishing of events (example from plug widget).

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `events_list` | yes | `array<track-event>` |  |

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
curl -X POST "https://api.devrev.ai/track-events.publish" \
  -H "Content-Type: application/json" \
  -d '{
    "events_list": [
      {
        "name": "string",
        "payload": {}
      }
    ]
  }'
```

<details><summary>Example 201 response</summary>

```json
{}
```

</details>
