# Snap Widgets

Source: <https://developer.devrev.ai/api-reference/snap-widgets>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/snap-widgets.create` | [create](#create) |

<a id="create"></a>

## `POST /snap-widgets.create`

**Create Snap Widget**

Source: <https://developer.devrev.ai/api-reference/snap-widgets/create>

Create a snap widget object.

**Required scopes:**

- `snap_widget:write` OR `snap_widget:all`

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `create-email-preview-widget`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | yes | `string` | *Value in: "email_preview" \| "starter_message_nudge"* |
| `interactions` | no | `array<snap-widget-interaction>` | The list of interactions supported by the widget. |
| `name` | yes | `string` | A human readable name for the snap widget.<br>*Format: text* |
| `namespace` | no | `string` | Logical grouping of snap widgets. Useful for filtering.<br>*Value in: "ai_assistant_message" \| "comment_suggestion_replies" \| "email_preview" \| "link_preview" \| "meeting_preview" \| "plug_nudge" \| "side_thread"* |
| `shared_with` | no | `array<set-shared-with-membership>` | Sets the members that the snap widget is shared with.<br>*Items: items <= 8* |
| `status` | no | `string` | The status of the snap widget.<br>*Value in: "draft" \| "published"* |
| `bcc` | no | `array<create-email-info>` | The list of bcc addresses. |
| `cc` | no | `array<create-email-info>` | The list of cc addresses. |
| `from` | no | `array<create-email-info>` | The list of from addresses. |
| `html_body` | no | `string` | The html body of the email.<br>*Format: text* |
| `in_reply_to` | no | `string` | The in reply to of the email.<br>*Format: text* |
| `inlines` | no | `array<create-email-inline-attachment>` | The list of inline attachments. |
| `is_spam` | no | `boolean` | Whether the email is spam. |
| `message_id` | no | `string` | The message id of the email.<br>*Format: text* |
| `raw_email_artifact` | no | `string` | The raw email artifact.<br>*Format: id* |
| `references` | no | `array<string>` | The list of references in the email. |
| `reply_to` | no | `array<create-email-info>` | The list of reply to addresses. |
| `sent_timestamp` | no | `string` | The time the email was sent.<br>*Format: date-time* |
| `subject` | no | `string` | The subject of the email.<br>*Format: text* |
| `text_body` | no | `string` | The text body of the email.<br>*Format: text* |
| `to` | no | `array<create-email-info>` | The list of to addresses. |

#### Variant `create-starter-message-nudge-widget`

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
curl -X POST "https://api.devrev.ai/snap-widgets.create" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "email_preview",
    "name": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "snap_widget": {
    "type": "email_preview",
    "parent_id": "string",
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
    "interactions": [
      {
        "type": "click",
        "click_action": "open_plug_widget"
      }
    ],
    "name": "string",
    "namespace": "ai_assistant_message",
    "status": "draft",
    "bcc": [
      {
        "address": "string",
        "name": "string",
        "user": {
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
    "cc": [
      {
        "address": "string",
        "name": "string",
        "user": {
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
    "from": [
      {
        "address": "string",
        "name": "string",
        "user": {
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
    "html_body": "string",
    "in_reply_to": "string",
    "inlines": [
      {
        "artifact": {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        },
        "content_id": "string"
      }
    ],
    "is_spam": true,
    "message_id": "string",
    "raw_email_artifact": {
      "display_id": "string",
      "id": "string",
      "file": {
        "type": "string",
        "name": "string",
        "size": 0
      }
    },
    "references": [
      "string"
    ],
    "reply_to": [
      {
        "address": "string",
        "name": "string",
        "user": {
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
    "sent_timestamp": "2023-01-01T12:00:00.000Z",
    "subject": "string",
    "text_body": "string",
    "to": [
      {
        "address": "string",
        "name": "string",
        "user": {
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
    ]
  }
}
```

</details>
