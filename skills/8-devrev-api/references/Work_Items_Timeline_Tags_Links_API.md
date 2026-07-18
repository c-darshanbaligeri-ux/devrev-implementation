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
`reported_by`, `priority`/`severity`, `stage`, `tags`, and `custom_fields`
(with the matching `custom_schema_spec` when using subtypes).

Issue-specific: `sprint`, `target_close_date`. Opportunity-specific:
`account`, `amount`, `annual_recurring_revenue`.

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
-d '{ "id": "<WORK_ID>", "stage": { "name": "resolved" },
      "owned_by": { "set": [ "<DEVU_ID>" ] } }'
```

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
- `tags.delete` — `tag:all`.
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
- `links.delete` — remove a link (`link:all`).
- Requires `link:write`/`link:all` plus read access to both objects. Always use
  DON ids, never display IDs.

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
