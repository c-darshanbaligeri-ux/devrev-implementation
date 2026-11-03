# Notifications

Source: <https://developer.devrev.ai/beta/api-reference/notifications>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/content-template.create` | [content-template-create](#content-template-create) |
| GET | `/content-template.get` | [content-template-get](#content-template-get) |
| POST | `/content-template.get` | [content-template-get-post](#content-template-get-post) |
| GET | `/content-template.list` | [content-template-list](#content-template-list) |
| POST | `/content-template.list` | [content-template-list-post](#content-template-list-post) |
| POST | `/notifications.send` | [send](#send) |

<a id="content-template-create"></a>

## `POST /content-template.create`

**Create Content Template**

Source: <https://developer.devrev.ai/beta/api-reference/notifications/content-template-create>

Create the content template.

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `content-template-create-request-notification-content-template`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `string` | *Value in: "notification_content_template"* |
| `input_fields_schema` | no | `array<schema-field-descriptor>` | Input fields schema. The fields will be used to replace variables present in the content template. |
| `name` | no | `string` | The name of the content template. The name must be unique for each creator of the content template.<br>*Format: text* |
| `defaults` | yes | `array<content-template-create-request-notification-content-template-default-notification-content-template>` | Default notification template per language. Only one is permitted per language. These will be used to replace the notification content on basis of language preferences of the user. Default is EN(US). |

#### Variant `content-template-create-request-notification-content-template-translation`

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
curl -X POST "https://api.devrev.ai/content-template.create" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "notification_content_template",
    "name": "string",
    "defaults": [
      {
        "body": "string",
        "title": "string"
      }
    ]
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "content_template": {
    "type": "notification_content_template",
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
    "object_version": 0
  }
}
```

</details>


<a id="content-template-get"></a>

## `GET /content-template.get`

**Get Content Template**

Source: <https://developer.devrev.ai/beta/api-reference/notifications/content-template-get>

Get the content template.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The content template's ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/content-template.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "content_template": {
    "type": "notification_content_template",
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
    "object_version": 0
  }
}
```

</details>


<a id="content-template-get-post"></a>

## `POST /content-template.get`

**Get Content Template (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/notifications/content-template-get-post>

Get the content template.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The content template's ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/content-template.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "content_template": {
    "type": "notification_content_template",
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
    "object_version": 0
  }
}
```

</details>


<a id="content-template-list"></a>

## `GET /content-template.list`

**List Content Template**

Source: <https://developer.devrev.ai/beta/api-reference/notifications/content-template-list>

Lists the content templates.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for content template created by any of these users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of content template to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `name` | no | `array<string>` | Filters for content template based on name. |
| `sort_by` | no | `array<string>` | Fields to sort the content template by and the direction to sort them. |
| `type` | no | `array<content-template-type>` | Filters for content template of the provided types. |

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
curl -X GET "https://api.devrev.ai/content-template.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "content_template": [
    {
      "type": "notification_content_template",
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
      "object_version": 0
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="content-template-list-post"></a>

## `POST /content-template.list`

**List Content Template (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/notifications/content-template-list-post>

Lists the content templates.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `array<content-template-type>` | Filters for content template of the provided types. |
| `created_by` | no | `array<string>` | Filters for content template created by any of these users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of content template to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `name` | no | `array<string>` | Filters for content template based on name. |
| `sort_by` | no | `array<string>` | Fields to sort the content template by and the direction to sort them. |

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
curl -X POST "https://api.devrev.ai/content-template.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "content_template": [
    {
      "type": "notification_content_template",
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
      "object_version": 0
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="send"></a>

## `POST /notifications.send`

**Send Notifications**

Source: <https://developer.devrev.ai/beta/api-reference/notifications/send>

Generate a notification.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `notifications` | yes | `array<send-notification>` | The list of notifications to send.<br>*Items: 1 <= items <= 10* |

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
curl -X POST "https://api.devrev.ai/notifications.send" \
  -H "Content-Type: application/json" \
  -d '{
    "notifications": [
      {
        "type": "generic_notification",
        "receiver": "string",
        "event_type": "alert",
        "metadata": [
          {
            "content_template": "string"
          }
        ]
      }
    ]
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>
