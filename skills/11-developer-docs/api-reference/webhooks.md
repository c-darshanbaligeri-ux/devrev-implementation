# Webhooks

Source: <https://developer.devrev.ai/api-reference/webhooks>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/webhooks.create` | [create](#create) |
| POST | `/webhooks.delete` | [delete](#delete) |
| POST | `/webhooks.event` | [event](#event) |
| GET | `/webhooks.get` | [get](#get) |
| POST | `/webhooks.get` | [get-post](#get-post) |
| GET | `/webhooks.list` | [list](#list) |
| POST | `/webhooks.list` | [list-post](#list-post) |
| POST | `/webhooks.update` | [update](#update) |

<a id="create"></a>

## `POST /webhooks.create`

**Create Webhook**

Source: <https://developer.devrev.ai/api-reference/webhooks/create>

Creates a new webhook target.

**Required scopes:** Default Scopes unavailable for this API.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `event_types` | no | `array<webhook-event-type>` | The event types that the webhook endpoint will receive. |
| `headers` | no | `array<webhook-header>` | The headers to include in every webhook invocation.<br>*Items: items <= 8* |
| `secret` | no | `string` | The secret to use when verifying webhook events. If provided, the secret must be between 8 and 32 bytes (inclusive). If not set, a secret will be automatically generated and provided in the response. |
| `url` | yes | `string` | The URL of the webhook endpoint.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/webhooks.create" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "webhook": {
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
    "event_types": [
      "account_created"
    ],
    "headers": [
      {
        "name": "string",
        "value": "string"
      }
    ],
    "secret": "string",
    "status": "active",
    "url": "string"
  }
}
```

</details>


<a id="delete"></a>

## `POST /webhooks.delete`

**Delete Webhook**

Source: <https://developer.devrev.ai/api-reference/webhooks/delete>

Deletes the requested webhook.

**Required scopes:** Default Scopes unavailable for this API.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | ID for the webhook.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/webhooks.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "don:integration:dvrv-us-1:devo/example:webhook/webhook-id"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="event"></a>

## `POST /webhooks.event`

**Event Webhooks**

Source: <https://developer.devrev.ai/api-reference/webhooks/event>

Describes a webhook invocation for an event from DevRev to a webhook's target URL, where the receiving handler must implement the specified protocol. Note the documented endpoint is for exposition and not provided by DevRev.

**Required scopes:** Default Scopes unavailable for this API.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `string` | The event types that the webhook will receive.<br>*Value in: "account_created" \| "account_deleted" \| "account_updated" \| "ai_agent_response" \| "article_created" \| "article_deleted" \| "article_updated" \| "artifact_created" \| "artifact_deleted" \| "artifact_updated" \| "conversation_created" \| "conversation_deleted" \| "conversation_updated" \| "dashboard_created" \| "dashboard_deleted" \| "dashboard_updated" \| "dev_user_created" \| "dev_user_deleted" \| "dev_user_updated" \| "group_created" \| "group_deleted" \| "group_member_added" \| "group_member_removed" \| "group_updated" \| "incident_created" \| "incident_deleted" \| "incident_updated" \| "job_created" \| "job_deleted" \| "job_updated" \| "link_created" \| "link_deleted" \| "link_updated" \| "part_created" \| "part_deleted" \| "part_updated" \| "question_answer_created" \| "question_answer_deleted" \| "question_answer_updated" \| "rev_org_created" \| "rev_org_deleted" \| "rev_org_updated" \| "rev_user_created" \| "rev_user_deleted" \| "rev_user_updated" \| "sla_tracker_created" \| "sla_tracker_deleted" \| "sla_tracker_fetched" \| "sla_tracker_updated" \| "survey_created" \| "survey_deleted" \| "survey_response_created" \| "survey_response_deleted" \| "survey_response_updated" \| "survey_updated" \| "sync_history_created" \| "sync_history_deleted" \| "sync_history_updated" \| "sync_unit_updated" \| "tag_created" \| "tag_deleted" \| "tag_updated" \| "timeline_entry_created" \| "timeline_entry_deleted" \| "timeline_entry_updated" \| "verify" \| "webhook_created" \| "webhook_deleted" \| "webhook_updated" \| "widget_created" \| "widget_deleted" \| "widget_updated" \| "work_created" \| "work_deleted" \| "work_fetched" \| "work_updated"* |
| `account_created` | no | `event-account-created` |  |
| `account_deleted` | no | `event-account-deleted` |  |
| `account_updated` | no | `event-account-updated` |  |
| `ai_agent_created` | no | `event-ai-agent-created` |  |
| `ai_agent_deleted` | no | `event-ai-agent-deleted` |  |
| `ai_agent_response` | no | `event-ai-agent-response` |  |
| `ai_agent_updated` | no | `event-ai-agent-updated` |  |
| `article_created` | no | `event-article-created` |  |
| `article_deleted` | no | `event-article-deleted` |  |
| `article_updated` | no | `event-article-updated` |  |
| `conversation_created` | no | `event-conversation-created` |  |
| `conversation_deleted` | no | `event-conversation-deleted` |  |
| `conversation_updated` | no | `event-conversation-updated` |  |
| `dashboard_created` | no | `event-dashboard-created` |  |
| `dashboard_deleted` | no | `event-dashboard-deleted` |  |
| `dashboard_updated` | no | `event-dashboard-updated` |  |
| `dev_user_created` | no | `event-dev-user-created` |  |
| `dev_user_deleted` | no | `event-dev-user-deleted` |  |
| `dev_user_updated` | no | `event-dev-user-updated` |  |
| `group_created` | no | `event-group-created` |  |
| `group_deleted` | no | `event-group-deleted` |  |
| `group_member_added` | no | `event-group-member-added` |  |
| `group_member_removed` | no | `event-group-member-removed` |  |
| `group_updated` | no | `event-group-updated` |  |
| `id` | yes | `string` | The event's ID.<br>*Format: id* |
| `incident_created` | no | `event-incident-created` |  |
| `incident_deleted` | no | `event-incident-deleted` |  |
| `incident_updated` | no | `event-incident-updated` |  |
| `link_created` | no | `event-link-created` |  |
| `link_deleted` | no | `event-link-deleted` |  |
| `link_updated` | no | `event-link-updated` |  |
| `part_created` | no | `event-part-created` |  |
| `part_deleted` | no | `event-part-deleted` |  |
| `part_updated` | no | `event-part-updated` |  |
| `question_answer_created` | no | `event-question-answer-created` |  |
| `question_answer_deleted` | no | `event-question-answer-deleted` |  |
| `question_answer_updated` | no | `event-question-answer-updated` |  |
| `rev_org_created` | no | `event-rev-org-created` |  |
| `rev_org_deleted` | no | `event-rev-org-deleted` |  |
| `rev_org_updated` | no | `event-rev-org-updated` |  |
| `rev_user_created` | no | `event-rev-user-created` |  |
| `rev_user_deleted` | no | `event-rev-user-deleted` |  |
| `rev_user_updated` | no | `event-rev-user-updated` |  |
| `service_plan_created` | no | `event-service-plan-created` |  |
| `service_plan_updated` | no | `event-service-plan-updated` |  |
| `sla_tracker_created` | no | `event-sla-tracker-created` |  |
| `sla_tracker_deleted` | no | `event-sla-tracker-deleted` |  |
| `sla_tracker_fetched` | no | `empty\|event-sla-tracker-fetched-ok` |  |
| `sla_tracker_updated` | no | `event-sla-tracker-updated` |  |
| `survey_created` | no | `event-survey-created` |  |
| `survey_deleted` | no | `event-survey-deleted` |  |
| `survey_response_created` | no | `event-survey-response-created` |  |
| `survey_response_deleted` | no | `event-survey-response-deleted` |  |
| `survey_response_updated` | no | `event-survey-response-updated` |  |
| `survey_updated` | no | `event-survey-updated` |  |
| `sync_history_created` | no | `event-sync-history-created` |  |
| `sync_history_deleted` | no | `event-sync-history-deleted` |  |
| `sync_history_updated` | no | `event-sync-history-updated` |  |
| `tag_created` | no | `event-tag-created` |  |
| `tag_deleted` | no | `event-tag-deleted` |  |
| `tag_updated` | no | `event-tag-updated` |  |
| `timeline_entry_created` | no | `event-timeline-entry-created` |  |
| `timeline_entry_deleted` | no | `event-timeline-entry-deleted` |  |
| `timeline_entry_updated` | no | `event-timeline-entry-updated` |  |
| `timestamp` | no | `string` | Timestamp of the webhook's invocation for the event. Note this should be used to protect against replay attacks, where the event should only be processed if the timestamp isn't stale by several seconds.<br>*Format: date-time* |
| `verify` | no | `webhook-event-verify` |  |
| `webhook_created` | no | `event-webhook-created` |  |
| `webhook_deleted` | no | `event-webhook-deleted` |  |
| `webhook_id` | yes | `string` | ID of the webhook for the event.<br>*Format: id* |
| `webhook_updated` | no | `event-webhook-updated` |  |
| `widget_created` | no | `event-widget-created` |  |
| `widget_deleted` | no | `event-widget-deleted` |  |
| `widget_updated` | no | `event-widget-updated` |  |
| `work_created` | no | `event-work-created` |  |
| `work_deleted` | no | `event-work-deleted` |  |
| `work_fetched` | no | `empty\|event-work-fetched-ok` |  |
| `work_updated` | no | `event-work-updated` |  |
| `workflow_created` | no | `event-workflow-created` |  |
| `workflow_deleted` | no | `event-workflow-deleted` |  |
| `workflow_step_created` | no | `event-workflow-step-created` |  |
| `workflow_step_deleted` | no | `event-workflow-step-deleted` |  |
| `workflow_step_updated` | no | `event-workflow-step-updated` |  |
| `workflow_updated` | no | `event-workflow-updated` |  |
| `workflow_version_created` | no | `event-workflow-version-created` |  |
| `workflow_version_deleted` | no | `event-workflow-version-deleted` |  |
| `workflow_version_updated` | no | `event-workflow-version-updated` |  |

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
curl -X POST "https://api.devrev.ai/webhooks.event" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string",
    "webhook_id": "don:integration:dvrv-us-1:devo/example:webhook/webhook-id"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "challenge": "string"
}
```

</details>


<a id="get"></a>

## `GET /webhooks.get`

**Get Webhook**

Source: <https://developer.devrev.ai/api-reference/webhooks/get>

Gets the requested webhook's information.

**Required scopes:** Default Scopes unavailable for this API.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | ID for the webhook.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/webhooks.get?id=don%3Aintegration%3Advrv-us-1%3Adevo%2Fexample%3Awebhook%2Fwebhook-id"
```

<details><summary>Example 200 response</summary>

```json
{
  "webhook": {
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
    "event_types": [
      "account_created"
    ],
    "headers": [
      {
        "name": "string",
        "value": "string"
      }
    ],
    "secret": "string",
    "status": "active",
    "url": "string"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /webhooks.get`

**Get Webhook (POST)**

Source: <https://developer.devrev.ai/api-reference/webhooks/get-post>

Gets the requested webhook's information.

**Required scopes:** Default Scopes unavailable for this API.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | ID for the webhook.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/webhooks.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "don:integration:dvrv-us-1:devo/example:webhook/webhook-id"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "webhook": {
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
    "event_types": [
      "account_created"
    ],
    "headers": [
      {
        "name": "string",
        "value": "string"
      }
    ],
    "secret": "string",
    "status": "active",
    "url": "string"
  }
}
```

</details>


<a id="list"></a>

## `GET /webhooks.list`

**List Webhooks**

Source: <https://developer.devrev.ai/api-reference/webhooks/list>

Lists the webhooks.

**Required scopes:** Default Scopes unavailable for this API.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `status` | no | `array<webhook-status>` | Filters for webhooks with the provided statuses. |

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
curl -X GET "https://api.devrev.ai/webhooks.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "webhooks": [
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
      "event_types": [
        "account_created"
      ],
      "headers": [
        {
          "name": "string",
          "value": "string"
        }
      ],
      "secret": "string",
      "status": "active",
      "url": "string"
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /webhooks.list`

**List Webhooks (POST)**

Source: <https://developer.devrev.ai/api-reference/webhooks/list-post>

Lists the webhooks.

**Required scopes:** Default Scopes unavailable for this API.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `status` | no | `array<webhook-status>` | Filters for webhooks with the provided statuses. |

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
curl -X POST "https://api.devrev.ai/webhooks.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "webhooks": [
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
      "event_types": [
        "account_created"
      ],
      "headers": [
        {
          "name": "string",
          "value": "string"
        }
      ],
      "secret": "string",
      "status": "active",
      "url": "string"
    }
  ]
}
```

</details>


<a id="update"></a>

## `POST /webhooks.update`

**Update Webhook**

Source: <https://developer.devrev.ai/api-reference/webhooks/update>

Updates the requested webhook.

**Required scopes:** Default Scopes unavailable for this API.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `action` | no | `string` | The action to update the webhook's status.<br>*Value in: "activate" \| "deactivate"* |
| `event_types` | no | `webhooks-update-request-event-types` |  |
| `headers` | no | `webhooks-update-request-headers` |  |
| `id` | yes | `string` | ID for the webhook.<br>*Format: id* |
| `secret` | no | `string` | If provided, updates the secret that's used when verifying webhook events, which must be between 8 and 32 bytes (inclusive). Otherwise if empty, then a new secret is generated. If the webhook is active, then its status will transition to the 'unverified' state and it won't receive any object events until successfully verified. |
| `url` | no | `string` | The webhook's updated URL. If the webhook is active, then the webhook's status will transition to the 'unverified' state and it won't receive any object events until successfully verified.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/webhooks.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "don:integration:dvrv-us-1:devo/example:webhook/webhook-id"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "webhook": {
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
    "event_types": [
      "account_created"
    ],
    "headers": [
      {
        "name": "string",
        "value": "string"
      }
    ],
    "secret": "string",
    "status": "active",
    "url": "string"
  }
}
```

</details>
