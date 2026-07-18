# Work items, timeline, tags & links — DevRev API

Create and manage the core work objects (issue, ticket, task, incident,
opportunity), post to their timelines, react, tag, and link them.

| Field | Detail |
| --- | --- |
| Base URL | https://api.devrev.ai |
| Auth | `Authorization: Bearer <TOKEN>` |

---

## 1. Works (issue / ticket / task / incident / opportunity)

`works.*` is a unified surface for all five work types. The `type` field selects
the subtype, and the required scope tracks it (e.g. `issue:write`, `ticket:write`,
`opportunity:write`).

### Create — `works.create`

```bash
curl -X POST 'https://api.devrev.ai/works.create' \
-H 'Authorization: Bearer <TOKEN>' \
-H 'Content-Type: application/json' \
-d '{
  "type": "ticket",
  "title": "Login fails for Acme",
  "body": "Users cannot log in after the 2.3 release.",
  "applies_to_part": "<PART_ID>",
  "owned_by": [ "<DEVU_OWNER_ID>" ],
  "severity": "high"
}'
```

Common fields: `type`, `title`, `body`, `applies_to_part`, `owned_by`,
`reported_by`, `priority`/`severity`, `stage`, `tags`, `artifacts`,
`external_ref`, and `custom_fields` (with the matching `custom_schema_spec`
when using subtypes).

Issue-specific: `sprint`, `target_close_date`. Opportunity-specific:
`account`, `amount`, `annual_recurring_revenue`.

**Artifacts at create time — confirmed working live 2026-07-18**: pass
`"artifacts": ["<ARTIFACT_DON>"]` directly on `works.create` to attach a file
uploaded via `artifacts.prepare` — the response's `work.artifacts[]` contains
the full artifact object (`display_id`, `file.name`, `file.size`, `file.type`).
**An artifact can be attached to exactly one parent, ever** — re-attaching an
already-attached artifact id (to a different work item, or to a timeline
comment) returns `400 {"type":"artifact_already_attached_to_a_parent","existing_parent":"<don>"}`.
Upload a fresh artifact per attachment target if you need the same file on
two objects.

**`external_ref` is a real idempotency key — confirmed working live 2026-07-18**:
re-running `works.create` with an `external_ref` that already exists for that
work type returns `409 {"message":"Conflict","type":"conflict"}` — it does not
create a duplicate and does not silently no-op. Catch the 409 and look the
record up via `works.list` with `{"external_ref": ["<value>"]}` — note the
filter field is singular `external_ref` even though its value is an array;
`external_refs` (plural) returns `400 {"type":"invalid_field","field_name":"external_refs"}`.

### Read / list / count / export

```bash
# List open tickets on a part
curl -X POST 'https://api.devrev.ai/works.list' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "type": ["ticket"], "applies_to_part": ["<PART_ID>"], "limit": 50 }'
```

- `works.get` — one item by id.
- `works.list` — filter by type, owner, stage, part, tags, dates; paginate with `cursor`.
- `works.count` — count matching a filter.
- `works.export` — bulk export.

### Update / delete

```bash
curl -X POST 'https://api.devrev.ai/works.update' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "id": "<WORK_ID>", "type": "ticket", "stage": { "name": "resolved" },
      "owned_by": { "set": [ "<DEVU_ID>" ] } }'
```

<!-- corrected 2026-07-18: example previously omitted "type" -->
**`type` is required on `works.update`, not optional** (verified live 2026-07-18): omitting it while
setting a type-specific field like `severity` returns `400 {"type":"invalid_field","field_name":"severity"}`
— the server can't resolve the field without knowing the work type. Always include `"type": "<the
work's actual type>"` on every `works.update` call.

`works.delete` needs the `<type>:all` scope.

---

## 2. Timeline entries & reactions

Timeline entries are the comments/events on a work item (or other object).
No dedicated scope — you need read/write on the parent object's type (e.g.
`ticket:write` to comment on a ticket).

### Add a comment — `timeline-entries.create`

```bash
curl -X POST 'https://api.devrev.ai/timeline-entries.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "object": "<WORK_ID>",
  "type": "timeline_comment",
  "body": "Fix deployed to prod, please verify.",
  "visibility": "internal"
}'
```

- `visibility` controls who sees it (e.g. `internal`, `external`, `private`).
  See the "Restricted messages on a timeline" guide for the full model.
- `timeline-entries.get` / `.list` — read the timeline; `list` filters by object.
- `timeline-entries.update` / `.delete` — edit or remove an entry.
- **`timeline-entries.list` response shape and content — confirmed live 2026-07-18**: wrapper key is
  `{"timeline_entries": [...]}` (not the generic `{"result": [...], "cursor": ...}` pattern the
  catalog describes for most `.list` endpoints). The list also auto-includes `timeline_change_event`
  entries (object creation, field updates like `severity` changing) interleaved with
  `timeline_comment` entries, ordered by `created_date` — not just comments you posted. Don't assume
  `.list` only returns what you created via `.create`.

### Reactions — `reactions.list` / `reactions.update`
React to a timeline entry (emoji-style). `reactions.update` adds/removes; scope
follows the parent object type.

---

## 3. Tags

```bash
# Create a tag
curl -X POST 'https://api.devrev.ai/tags.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "name": "billing", "description": "Billing-related work" }'
```

- `tags.get` / `.list` — read tags.
- `tags.update` — rename / re-describe (`tag:write`).
- `tags.delete` — `tag:all`. **Confirmed working live 2026-07-18** (unlike most other `.delete`
  endpoints in this API, which are missing or deprecate-only): `POST tags.delete {"id": "<TAG_ID>"}`
  returns `200 {}`, and a follow-up `tags.get` on the same id returns `404 {"type":"not_found"}`.
  Passing a malformed/nonexistent id returns `400 {"type":"invalid_id","field_name":"id"}`.
- Apply a tag by including it in a work item's `tags` on `works.create/update`.

---

## 4. Links

Connect two objects. Built-in link types: `serves`, `is_part_of`,
`is_dependent_on`, `is_related_to`. For custom relationships and full detail,
see `Custom_Objects_and_Links_API.md`.

```bash
# Link a ticket to an issue
curl -X POST 'https://api.devrev.ai/links.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "link_type": "is_related_to",
      "source": "<TICKET_ID>", "target": "<ISSUE_ID>" }'
```

- `links.list` — list an object's links.
- `links.replace` — swap a link (atomic only for part-to-part default link types;
  otherwise a non-atomic delete+create keeping the same type). Re-parents a part
  without an orphan gap.
- `links.delete` — remove a link (`link:all`). **Confirmed working live 2026-07-18**:
  `POST links.delete {"id": "<LINK_ID>"}` returns `200 {}`; a follow-up `links.get`
  on the same id returns `404`. Unlike custom link types (deprecate-only) and most
  other `.delete` endpoints, built-in link instances genuinely delete.
- Requires `link:write`/`link:all` plus read access to both objects. Always use
  DON ids, never display IDs.
- **Built-in `link_type` values are restricted by the (source type, target type)
  pair — not every type works between every pair of objects.** Verified live
  2026-07-18 in one org: `is_related_to` and `is_part_of` both returned
  `400 {"type":"bad_request"}` (no field_name — opaque error) between a ticket and
  an issue, and `is_related_to source→target` reversed (issue→ticket) also 400'd;
  but `is_dependent_on` succeeded ticket→issue, and `is_related_to` succeeded
  issue→issue (same type on both ends). Treat a bare `bad_request` from
  `links.create` as "this link_type/object-type combination isn't allowed," not
  as a malformed request — try a different built-in type or check the object
  types before assuming the call is broken.

---

## 5. Atoms — generic fetch

`atoms.get` fetches any object by id when you don't want a type-specific call.
The required scope is derived from the id (e.g. an issue id needs `issue:read`).

```bash
curl -X POST 'https://api.devrev.ai/atoms.get' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "id": "<OBJECT_ID>" }'
```

---

## 6. Pitfalls

- Wrong scope for the work type — `works.create` of a ticket needs `ticket:write`,
  not a generic scope.
- Commenting without parent access — timeline calls need the parent object's
  read/write scope, not a "timeline" scope (there isn't one).
- Using a display ID (TKT-123) in links or `applies_to_part` — always use the DON.
- Forgetting `custom_schema_spec` when a work item uses a subtype with custom fields.
