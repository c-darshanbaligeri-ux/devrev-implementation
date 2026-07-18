# Support, knowledge & SLAs — DevRev API

Customer-facing and support-ops objects: conversations, chats, knowledge-base
articles, surveys, meetings, and SLAs / metric definitions / trackers.

| Field | Detail |
| --- | --- |
| Base URL | https://api.devrev.ai |
| Auth | `Authorization: Bearer <TOKEN>` |

---

## 1. Conversations

A support/sales conversation thread (e.g. PLuG chat, imported channel).

```bash
curl -X POST 'https://api.devrev.ai/conversations.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "title": "Billing question from Acme",
      "members": [ "<REV_USER_ID>", "<DEVU_ID>" ] }'
```

| Endpoint | Scope |
| --- | --- |
| `conversations.create` / `.update` | `conversation:write` / `:all` |
| `conversations.delete` | `conversation:all` |
| `conversations.get` / `.list` | `conversation:read` … |

Post messages to a conversation via `timeline-entries.create` with the
conversation as the `object` (see the work-items/timeline doc).

---

## 2. Chats

Lightweight chat objects; access is governed by chat membership, so no explicit
scope is required.

- `chats.create` — start a chat.
- `chats.get` — fetch.
- `chats.update` — modify.

---

## 3. Articles (knowledge base)

```bash
curl -X POST 'https://api.devrev.ai/articles.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "title": "How to reset your password",
  "applies_to_parts": [ "<PART_ID>" ],
  "owned_by": [ "<DEVU_ID>" ],
  "content_format": "rt"
}'
```

| Endpoint | Scope |
| --- | --- |
| `articles.create` / `.update` | `article:write` / `:all` |
| `articles.delete` | `article:all` |
| `articles.get` / `.list` | `article:read` … |

Articles support `status` (draft/published), `scope` (internal/external),
`tags`, and sharing via `shared_with`.

---

## 4. Surveys

```bash
# Send a survey
curl -X POST 'https://api.devrev.ai/surveys.send' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "survey": "<SURVEY_ID>", "object": "<CONVERSATION_OR_TICKET_ID>" }'
```

| Endpoint | Scope | Purpose |
| --- | --- | --- |
| `surveys.create` / `.update` | `survey:write` / `:all` | Define a survey |
| `surveys.send` | `survey:write` / `:all` | Send to a target |
| `surveys.delete` | `survey:all` | Delete |
| `surveys.get` / `.list` | `survey:read` … | Read |
| `surveys.submit` | `survey_response:write` / `:all` | Submit a response |
| `surveys.responses.list` | `survey_response:read` … | Read responses |
| `surveys.responses.update` | `survey_response:write` / `:all` | Edit a response |

CSAT/NPS reporting is built on survey responses.

---

## 5. Meetings

```bash
curl -X POST 'https://api.devrev.ai/meetings.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "title": "Acme QBR",
      "members": [ "<DEVU_ID>", "<REV_USER_ID>" ],
      "scheduled_date": "2026-08-01T15:00:00Z" }'
```

`meetings.get/list/count/update/delete` — scopes `meeting:read/write/all`.
Link a meeting to an opportunity or ticket via `links.create`.

---

## 6. SLAs, metric definitions & trackers

SLAs define response/resolution targets; metric definitions parameterize them;
trackers report live status.

```bash
# Create an SLA and assign it
curl -X POST 'https://api.devrev.ai/slas.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "name": "Standard support SLA", ... }'

curl -X POST 'https://api.devrev.ai/slas.assign' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "sla": "<SLA_ID>", "object": "<TICKET_OR_ACCOUNT_ID>" }'
```

| Endpoint | Scope |
| --- | --- |
| `slas.create` / `.update` / `.assign` / `.transition` | `sla:write` |
| `slas.get` / `.list` | `sla:read` / `sla:write` |
| `metric-definitions.create` / `.update` | `metric_definition:write` / `:all` |
| `metric-definitions.delete` | `metric_definition:all` |
| `metric-definitions.get` / `.list` | `metric_definition:read` … |
| `metric-action.execute` | None |
| `metric-trackers.get` | None |
| `sla-trackers.get` / `.list` | None |

---

## 7. Pitfalls

- Posting a message: there is no `messages.create` — use `timeline-entries.create`
  against the conversation/ticket object.
- Article visibility — set `scope` (internal vs external) and `status` (draft vs
  published); an unpublished article won't surface to customers.
- SLA not taking effect — creating an SLA isn't enough; `slas.assign` it to the
  object (or account), then check `sla-trackers.get`.
