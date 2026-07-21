# Collections for Articles — DevRev API

> **Provenance**: sourced from user-supplied documentation (2026-07-21), not derived from this
> repo's own live testing pass. **Verified live 2026-07-21** by this repo: `directories.create`
> (create/list/get all confirmed working), setting an article's `parent` to a directory DON both
> at `articles.create` time and via `.update` (confirmed working). `directories.update`/`.delete`/
> `.count` and the nested-item delete-block behavior were **not** independently re-verified live —
> treat those specific claims as documented-but-unconfirmed until exercised. Cross-reference:
> `Support_Knowledge_and_SLAs_API.md` §3b (the live-verified summary) and
> `docs/LEARNINGS.md` (dated entry).

## Key concept

In DevRev, a **collection** (the parent container that organizes articles in your Help Center) is represented at the API layer by the **directory** object. All collection operations use the `directories.*` endpoints, and articles are linked to a collection via the article's `parent` field.

- **Base URL:** `https://api.devrev.ai`
- **Auth:** every request needs a header `Authorization: Bearer <TOKEN>` (a Personal Access Token).
- **Nesting:** collections can be nested infinitely — a directory's `parent` field points to another directory, giving a multi-level hierarchy.

---

## Full list of collection (directory) endpoints

| Operation | Method | Endpoint | Required scope |
| --- | --- | --- | --- |
| Create | POST | `/directories.create` | `directory:write` or `directory:all` |
| Get | GET/POST | `/directories.get` | `directory:read`, `directory:write`, or `directory:all` |
| List | GET/POST | `/directories.list` | `directory:read`, `directory:write`, or `directory:all` |
| Count | GET/POST | `/directories.count` | `directory:read`, `directory:write`, or `directory:all` |
| Update | POST | `/directories.update` | `directory:write` or `directory:all` |
| Delete | POST | `/directories.delete` | `directory:all` |

---

## 1. Create a collection

**`POST /directories.create`** — creates a directory (collection).

### Request body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `title` | string | Yes | Title of the collection. |
| `description` | string | No | Description of the collection. |
| `parent` | id | No | Parent directory ID. Omit for a top-level collection; set it to nest inside another collection. |
| `published` | boolean | No | Whether the collection is published. |
| `language` | string | No | Language of the collection. |
| `thumbnail` | id | No | ID of the thumbnail artifact. |
| `tags` | array | No | Tags to associate (max 20). |

### Example

```bash
curl -X POST "https://api.devrev.ai/directories.create" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started",
    "description": "Onboarding guides for new users",
    "published": true
  }'
```

To nest it inside another collection, add `"parent": "<parent_directory_id>"`.

The `201` response returns the full `directory` object, including its `id` (use this to attach articles or nest sub-collections).

---

## 2. Get a collection

**`GET` or `POST /directories.get`** — fetches a single directory by its ID.

```bash
curl -X POST "https://api.devrev.ai/directories.get" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{ "id": "<directory_id>" }'
```

---

## 3. List collections

**`GET` or `POST /directories.list`** — lists directories matching the request; supports pagination.

```bash
curl -X POST "https://api.devrev.ai/directories.list" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## 4. Count collections

**`GET` or `POST /directories.count`** — returns the count of directories matching a filter.

```bash
curl -X POST "https://api.devrev.ai/directories.count" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## 5. Update a collection

**`POST /directories.update`** — updates the specified directory.

### Request body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | id | Yes | ID of the directory to update. |
| `title` | string | No | Updated title. |
| `description` | string | No | Updated description. |
| `parent` | id or null | No | Updated parent (re-parent / nest the collection). |
| `published` | boolean | No | Whether the collection is published. |
| `icon` | string | No | Updated icon. |
| `thumbnail` | id or null | No | Updated thumbnail artifact. |
| `reorder` | object | No | Reorder the collection within the hierarchy. |
| `tags` | object | No | Updated tags. |

### Example

```bash
curl -X POST "https://api.devrev.ai/directories.update" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "<directory_id>",
    "title": "New Title",
    "parent": "<new_parent_id>"
  }'
```

---

## 6. Delete a collection

**`POST /directories.delete`** — deletes the specified directory. Requires the `directory:all` scope. The only body field is `id` (required).

```bash
curl -X POST "https://api.devrev.ai/directories.delete" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{ "id": "<directory_id>" }'
```

> **Note:** deletion is blocked if there are nested items (sub-collections or articles) inside the collection — empty it first.

---

## Assigning articles to a collection

A collection groups articles, but you assign an article to it from the **article** side, not the directory side. Set the article's `parent` field to the target directory (collection) ID when calling `/articles.create` or `/articles.update`.

> **Constraint:** an article can belong to only **one** collection at a time.

---

## Notes

- These endpoints are documented under both the **Public** and **Beta** API references; both expose the same `directories.*` contract.
- All DevRev APIs are REST-based, accept JSON request bodies, and return JSON responses with standard HTTP status codes.
