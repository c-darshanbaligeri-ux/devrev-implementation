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

**Corrected 2026-07-19** — the payload below is the live-verified minimal working shape.
`owned_by` is genuinely required, not just good practice: omitting it returns
`HTTP 400 missing_required_field field_name:"owned_by"`. The combination of `owned_by` +
`content_format: "rt"` (this section's previous example, minus `applies_to_parts`) returns an
opaque `HTTP 400 bad_request` with **no diagnostic field name** — swap `content_format` for an
empty `resource: {}` object and it succeeds:

```bash
curl -X POST 'https://api.devrev.ai/articles.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "title": "How to reset your password",
  "owned_by": [ "<DEVU_ID>" ],
  "resource": {}
}'
```

`applies_to_parts` is optional (contrary to the prior example's implication it was needed for a
minimal create). The response omits `content_format` and reflects `resource:{}` and a default
`scope: "external"`.

| Endpoint | Scope |
| --- | --- |
| `articles.create` / `.update` | `article:write` / `:all` |
| `articles.delete` | `article:all` |
| `articles.get` / `.list` | `article:read` … |

`articles.list` response — confirmed live 2026-07-18: wrapper is `{"articles": [...], "total": <int>}`.
The extra top-level `total` count is not on most other `.list` endpoints tested in this folder (they
return only the array + `cursor`); useful for pagination UI without a separate `.count` call.

Articles support `status` (draft/published), `scope` (internal/external),
`tags`, and sharing via `shared_with`.

**`articles.list` server-side filters (doc-cited 2026-07-31 from
`developer.devrev.ai/beta/api-reference/articles/list-articles`) — do the filtering here, not
client-side.** The endpoint accepts:

| Filter | Type | Effect |
| --- | --- | --- |
| `applies_to_parts` | `array<string>` | Articles attached to any of the provided Parts (grounding-by-part is the fast path here). |
| `parent` | `array<string>` | Articles under the provided **directory** ids ("collection" grouping). |
| `status` | `array<article-status>` | e.g. `"archived"`. |
| `article_type` | `array<article-type>` | Omitting it excludes content blocks. |
| `authored_by` / `owned_by` / `created_by` / `modified_by` | `array<string>` | User-id filters. |
| `brands` / `tags` / `scope` | `array` | Editorial filters. |
| `shared_with.member` / `shared_with.role` | `string` | Sharing scope. |
| `sync_metadata.*` | `array<string>` / status enum | Adaas / sync-history filters. |
| `cursor` / `limit` / `mode` (`"after"`/`"before"`) | pagination | Default `limit: 50`. |

**Doctrine reminder for KB grounding**: `applies_to_parts` is the retrieval axis (a KB article's
attachment to a Trail Part). `parent` (the directory) is the *editorial* axis and rarely the
right retrieval filter — use it only when you deliberately want "everything on this shelf" (release
notes, compliance docs) rather than "everything relevant to this feature". Prefer
`applies_to_parts` for test-case / agent-grounding work, `parent` for browsing.

**Cross-reference**: HybridSearch (`namespace: article` — see
`skills/7-agent-building/references/api-contracts.md`) is the semantic-discovery alternative when
you don't have a Part id yet; take the returned id and call `articles.get` or read via
`articles.list?applies_to_parts=<part>` for authoritative detail.

### 3a. Article body content — confirmed live 2026-07-21 (closes the prior open gap)

The empty `resource: {}` payload above creates an article with **no body content** — it was
only ever a minimal-create smoke test. The real content mechanism is `resource.artifacts`, an
array of artifact DONs (same `artifacts.prepare` → upload → reference pattern used for
`works.create`, see `Platform_and_Admin_API.md` §1):

```bash
# 1. Prepare + upload the file (e.g. a .md file) exactly as for work-item attachments
curl -X POST 'https://api.devrev.ai/artifacts.prepare' -H 'Authorization: Bearer <TOKEN>' \
  -d '{"file_name":"my-article.md","file_type":"text/markdown"}'
# -> upload the returned form_data + file to the returned url (HTTP 204 on success)

# 2. Reference the artifact on the article
curl -X POST 'https://api.devrev.ai/articles.create' -H 'Authorization: Bearer <TOKEN>' \
-d '{
  "title": "Wire Status Reference",
  "owned_by": [ "<DEVU_ID>" ],
  "resource": { "artifacts": [ "<ARTIFACT_DON>" ] },
  "scope": 1,
  "applies_to_parts": [ "<PART_DON>" ],
  "parent": "<DIRECTORY_DON>"
}'
```

Confirmed facts from this live test:
- `resource.artifacts` is the field (an array of artifact DONs, `max_items: 200`, per
  `schemas.stock.get {"leaf_type":"article"}`'s `resource` composite schema). **Do not send
  `resource.type`** — it exists in the schema as an enum (`artifact`/`url`) but the API rejects it
  outright: `{"type":"invalid_field","field_name":"type"}`, even when the rest of the payload is
  otherwise valid. Only send `resource.artifacts` (or `resource.url` for the URL-reference variant
  below) — never `resource.type` alongside them.
- `resource.url` (a bare string) also works, for linking to an already-hosted external page rather
  than uploading content — confirmed live, returns `resource: {"url": "..."}`.
- After creating an article with `resource.artifacts` set, DevRev **asynchronously extracts the
  file's content** — within ~2 seconds in testing, `articles.get` showed a new `extracted_content`
  array (a second, DevRev-generated artifact, `text/plain`, distinct from the originally uploaded
  file) and a `tags: [{"tag": {"name": "content_extracted"}, "value": "<timestamp>"}]` entry
  marking completion. Poll `articles.get` for the `content_extracted` tag before assuming the
  article's searchable/rendered content is ready.
- **`resource.rich_text`, `resource.content`, `resource.markdown`, `resource.html`,
  `resource.artifact_id`, `resource.artifact`, and a top-level `artifacts` array (the `works.create`
  pattern) were all tried and all rejected** with `{"type":"invalid_field","field_name":"<name>"}` —
  none of these are real fields on the article `resource` composite. `resource.artifacts` (plural,
  array) is the only content-bearing field confirmed to work.
- **Markdown with tables renders/extracts correctly**; plain rich-text/HTML strings inline in the
  payload are NOT supported at all — content must go through the artifact-upload path.
- **`scope` takes a number, not the string label** — `{"scope":"internal"}` 400s
  (`unexpected_json_type`, expected number); the correct values are `1` = internal, `2` = external
  (default if omitted), per `schemas.stock.get`'s `scope` `uenum` definition. `scope` is also
  `is_immutable`/`is_read_only` in that same schema — set it at create time; don't expect
  `articles.update` to change it later (not independently re-tested, but the schema flags block it).
- **The part-linking field is `applies_to_parts`, NOT `applies_to_part_ids`** — the latter 400s
  with `{"type":"invalid_field","field_name":"applies_to_part_ids"}`. `applies_to_parts` takes an
  array of part DONs, `max_items: 10`, and the response echoes back full part objects (not just
  ids).
- `parent` — see §3b below; works identically on `articles.create` and `.update`.
- `articles.delete` **confirmed live and genuinely works** (`HTTP 200 {}`, follow-up `.get` 404s),
  same tier as `works.delete`/`custom-objects.delete`/`workflows.delete` — safe to clean up
  throwaway/test articles, but treat as destructive/confirm-first like any other working `.delete`.

### 3b. Collections (directories) — confirmed live 2026-07-21

**A "collection" in the DevRev Help Center UI is the `directory` object at the API layer.** This
was previously undocumented anywhere in this repo — no `collections.*`/`article-collections.*`
endpoint exists (both 404 route-not-found); the real family is `directories.*`.

| Endpoint | Method | Scope |
| --- | --- | --- |
| `directories.create` | POST | `directory:write` / `:all` |
| `directories.get` | GET/POST | `directory:read`, `:write`, or `:all` |
| `directories.list` | GET/POST | `directory:read`, `:write`, or `:all` |
| `directories.count` | GET/POST | `directory:read`, `:write`, or `:all` |
| `directories.update` | POST | `directory:write` / `:all` |
| `directories.delete` | POST | `directory:all` |

```bash
curl -X POST 'https://api.devrev.ai/directories.create' -H 'Authorization: Bearer <TOKEN>' \
-d '{ "title": "PEx Module", "description": "Payments Exchange domain knowledge base",
      "published": false }'
```
**Confirmed live** — `HTTP 201`, returns the full `directory` object (`id`, `display_id`, etc.).
Fields: `title` (required), `description`, `parent` (id — omit for top-level, set to nest inside
another directory; collections nest infinitely), `published` (bool), `language`, `thumbnail`
(artifact id), `tags` (array, max 20).

**Articles join a collection from the article side, not the directory side** — set the article's
`parent` field to the directory's DON on `articles.create` or `.update`:
```bash
curl -X POST 'https://api.devrev.ai/articles.update' -H 'Authorization: Bearer <TOKEN>' \
-d '{ "id": "<ARTICLE_DON>", "parent": "<DIRECTORY_DON>" }'
```
Confirmed live both at create time (inline `"parent": "<DIRECTORY_DON>"`) and via a separate
`.update` call — `articles.get` afterward shows `parent: {"id": "...", "display_id": "..."}`.
**An article can belong to only one collection at a time** (undocumented constraint, stated in the
source doc for this section — not independently stress-tested by trying to move an article between
two collections, but the single-`parent`-field shape makes this the expected behavior).

`directories.delete` is blocked if the directory still contains nested items (sub-collections or
articles) — empty it first (not independently verified live this session; documented behavior).

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
