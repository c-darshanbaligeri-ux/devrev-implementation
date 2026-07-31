# Trail, Articles, and Directories — the DevRev knowledge model

A single reference tying together the three DevRev objects that carry product
context and grounding knowledge: **Parts (the Trail hierarchy)**, **Articles
(the Knowledge Base)**, and **Directories (editorial "collections")**. This
file exists because these three are typically documented separately (Parts
under `parts.*`, Articles under `articles.*`, Directories in
`Directories_Collections_API.md`) but a real grounding task uses them
together — e.g. resolve a module name to a Trail Part, walk its
`is_part_of` chain, and pull the Articles attached to that Part chain.

**Provenance**: cross-cutting summary sourced from live probes against a
production org (2026-07-30 pull; 2 products / 6 capabilities / 115
features / 8 directories / 82 articles), reconciled against
`developer.devrev.ai/beta/api-reference` pages fetched 2026-07-31. Every
filter and shape below is doc-cited or live-verified — no memory-only claims.

---

## 1. The three objects at a glance

| Concept | DevRev object | Endpoint | Role |
| --- | --- | --- | --- |
| **Trail** | `part` | `parts.list` / `parts.get` | Product → Capability → Feature hierarchy. Scope owner for tests and KB content. |
| **Article** | `article` | `articles.list` / `articles.get` | Knowledge document. Body text lives in an artifact, not inline. |
| **Collection** | `directory` | `directories.list` / `directories.get` | Editorial grouping — "shelves" for articles. Not the retrieval axis. |

There is **no `collections.*` route** — the DevRev object called a "collection"
in Help Center UIs is `directory` at the API layer. Probing `collections.list`
returns `HTTP 404 route not found`.

---

## 2. Trail (Parts) — hierarchy and gotchas

### Structure

The Trail is `product` → `capability` → `feature`, with `feature` nesting up to
several levels deep. Part types accepted: `product`, `capability`, `feature`,
`enhancement`. This org has 0 `enhancement`s and no `runnable`/`microservice`
parts.

### Where the hierarchy actually lives

- The `parent_part` field on a Part record is **always `null`** in this org.
  Do NOT rely on it. See `skills/3-data-upload-and-org-build/SKILL.md`
  Field notes (2026-07-20) for the live confirmation.
- The real edge is an `is_part_of` link, retrieved via `links.list`:

  ```bash
  curl "https://api.devrev.ai/links.list?object=<PART_DON>" -H "Authorization: Bearer <TOKEN>"
  ```

  A non-root part returns one `is_part_of` edge whose `target` is the
  immediate parent.

### `parts.list` `parent_part` filter — depth semantics

Per `developer.devrev.ai/beta/api-reference/parts/list` (2026-07-31):

```json
{
  "type": ["feature"],
  "parent_part": {
    "parts": ["<CAP_DON>"],
    "level": 1
  }
}
```

- `parts` (array of DONs) — required if any `parent_part.*` field is set.
- `level` (int32, ≥1) — "Number of levels to fetch the part hierarchy up to."
- **Omit `level` → walk descendants at ANY depth.** This is the source of the
  2026-07-20 gotcha in this repo (features two levels down showed up in a
  supposed direct-children listing).
- **`level: 1` = direct children only.** Prefer this whenever the intent is
  "give me the immediate children."
- For a per-node authoritative parent check, use `links.list` — `level` filters
  what `parts.list` *returns*, not what a per-node check needs.

### Fields on a Part record

```
id, display_id, name, type, description,
parent_part: null,   # do not rely on
owned_by,            # dev-user DONs
stock_schema_fragment, custom_schema_fragments, custom_fields,
artifacts, tags, sync_metadata, subtype,
created_*, modified_*, object_version
```

---

## 3. Articles — Knowledge Base

### Structure

Every `article` returned by `articles.list` includes:

```
id, display_id, title, article_type, status, scope, language, rank,
parent: { id, display_id, title, ... }          # a DIRECTORY reference
applies_to_parts: [ { id, display_id, type, name, ... }, ... ]  # PART references
extracted_content: [ { id, display_id, file: { type, name, size } } ]  # body artifact
resource: { artifacts: [...], url }             # original upload
tags, brands, num_upvotes, num_downvotes,
authored_by, owned_by, shared_with,
sync_metadata,
created_*, modified_*, object_version, translation_group
```

### Body content — the artifact chain

Article bodies are **not inline**. They live in an artifact reachable via:

```
articles.get / articles.list
   └── article.extracted_content[0].id       (the body artifact DON)
       └── artifacts.locate {"id": <don>}    → { "url": "<presigned>", "expires_at": "<ISO-8601>" }
           └── HTTP GET <url>                → the plain-text body
```

- `extracted_content[0]` is DevRev's post-upload text extraction of the body
  (normalized to `text/plain`), signaled ready by a `content_extracted` tag.
  Prefer it over `resource.artifacts[0]` (the raw upload — may be `.md`,
  `.pdf`, etc.).
- `artifacts.locate` returns `{ url, expires_at }`. `expires_at` is the TTL —
  don't cache the URL past it. Presigned S3 URL is a plain GET, no DevRev
  auth header.
- Scope: `artifact:read` **plus parent-read** on the article (403 otherwise).

### `articles.list` server-side filters (doc-cited 2026-07-31)

Do the filtering here, not client-side:

| Filter | Effect |
| --- | --- |
| `applies_to_parts` | Articles attached to any of the given Parts. **This is the retrieval axis** for grounding. |
| `parent` | Articles under the given directory (collection) ids. Editorial axis. |
| `status` | `draft` / `published` / etc. |
| `article_type` | Omitting excludes content blocks. |
| `tags`, `brands`, `scope`, `authored_by`, `owned_by`, `created_by`, `modified_by` | Standard editorial filters. |
| `shared_with.member` / `shared_with.role` | Sharing scope. |
| `sync_metadata.*` | Sync/adaas filters. |
| `cursor`, `limit`, `mode` (`after`/`before`) | Pagination. Default `limit: 50`. |

---

## 4. Directories (the "collections")

### Structure

Per `developer.devrev.ai/beta/api-reference/directory/directories-list` (2026-07-31):

```
id, display_id, title, description, icon,
published: bool,
rank,                                          # ordering key
parent: { id, display_id, title, ... }         # nested directory (multi-level)
body, thumbnail: { id, display_id, file: {...} }   # artifact refs
tags: [{ tag: {...}, value }],
created_by, modified_by, sync_metadata,
created_date, modified_date, object_version
```

### `directories.list` filters (doc-cited 2026-07-31)

| Filter | Notes |
| --- | --- |
| `created_by` / `modified_by` | Array of user DONs. |
| `cursor` / `limit` / `mode` | Pagination (default 50; `after` default). |

**Notable absences**: no server-side `parent` filter, no `applies_to_articles`
membership filter — walking the directory hierarchy is a client-side loop.

### Why directories aren't the retrieval axis

`article.parent` groups articles editorially (shelves like "Release Notes",
"Compliance Documentation", "PEx Module"). Article-to-Trail attachment lives on
`article.applies_to_parts`, which is what an agent or test-case generator
filters on when it wants "articles relevant to Wire Entry / Verification".

Live-org sanity check (2026-07-30 pull): 66 of 82 articles have non-empty
`applies_to_parts`. The 16 without are release notes / BRDs / meta-docs — real
content but not typically grounding material.

---

## 5. How the three connect

```
    directory  ◄────── article.parent                article.applies_to_parts ──►  part
        (collection)      one-to-one                     many-to-many                (Trail node)
                                                                                       │
                                                                                       │  is_part_of link
                                                                                       ▼
                                                                                     part  (parent)
```

Two independent axes on every article:

1. **Editorial (`parent` → directory)** — where it lives on the shelf; fixed at author time.
2. **Applicable (`applies_to_parts` → Parts)** — what product surface it's about; drives retrieval.

Because a Trail Part is the hinge, walking `is_part_of` **upward** from a
feature to its capability to its product lets a caller collect *every*
applicable article — feature-level behavior + capability-level LOVs +
product-level domain overview — with a single upward walk.

---

## 6. Retrieval priority ladder (per ART-30502)

Same order in the two grounding contexts (native agent operations vs. REST fallback):

1. **`FetchObjectContext` (native op — `don:integration:dvrv-in-1:operation/devrev.fetch_object_context`)** — when you have a DON. Deterministic, full field set.
2. **`HybridSearch` (native op — `don:integration:dvrv-in-1:operation/devrev.hybrid_search`)** — when discovering by meaning. Scope `namespace` narrowly (see the 37-value enum in `skills/7-agent-building/references/api-contracts.md`).
3. **REST `search.core`** — REST-callable alternative for mixed-type hits (parts, articles, works, custom-objects). Uses cursor pagination.
4. **REST `articles.list?applies_to_parts=<part>` / `parts.list` / `directories.list`** — deterministic, portable, literal matching only.
5. **Generic model knowledge** — last resort. Doctrine: never answer from memory; cite the source.

**Native ops are agent operations invoked by DON, NOT REST endpoints.** A `curl` to
`hybrid-search.query` returns `HTTP 404 route not found`. `search.core` is the
REST-callable substitute.

---

## 7. End-to-end grounding recipes

### "Give me the KB for this Trail Part"

```bash
# 1. FetchObjectContext (agent) OR parts.get (REST) on the Part id.
curl -X POST "https://api.devrev.ai/parts.get" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"id": "<PART_DON>"}'

# 2. Walk is_part_of upward (feature → capability → product), collecting Part DONs.
curl "https://api.devrev.ai/links.list?object=<PART_DON>" \
  -H "Authorization: Bearer <TOKEN>"

# 3. Retrieve every article for the collected DONs.
curl "https://api.devrev.ai/articles.list?applies_to_parts=<PART_DON>&applies_to_parts=<PARENT_DON>&applies_to_parts=<GRANDPARENT_DON>" \
  -H "Authorization: Bearer <TOKEN>"

# 4. For each article you want to read, follow the extracted_content → artifacts.locate → GET chain (see §3).
```

### "Given a fuzzy module name, find the Trail Part and its KB"

```bash
# Preferred (agent): HybridSearch with namespace scoped to a part type.
# Fallback (REST): parts.list with an exact name filter across likely types.
curl -X POST "https://api.devrev.ai/parts.list" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"type": ["feature","capability","product"], "name": ["Wire Transfer"]}'
# → if 0 → try HybridSearch; do NOT invent a Part id.
# → if >1 → disambiguate via links.list on each candidate's is_part_of edge.
```

### "Which articles cover this term, across the whole KB?"

```bash
# HybridSearch (namespace: article, plus question_answer for Q&As).
# REST fallback: articles.list (title match is client-side — there is no server-side title search).
```

---

## 8. Common pitfalls

- **Never trust `part.parent_part` as a field.** It's always null. Use `links.list` for `is_part_of`.
- **Never omit `parent_part.level` when you want direct children only.** Omission = walk-to-leaves.
- **Never assume a directory ("collection") is a retrieval filter.** Filter by `applies_to_parts` instead.
- **Never read an article body inline.** Follow the artifact chain via `extracted_content[0]` → `artifacts.locate` → GET.
- **Never send `applies_to_part_ids`.** The correct field is `applies_to_parts` (400s otherwise; see the 2026-07-21 finding in `Support_Knowledge_and_SLAs_API.md`).
- **Never send `resource.type` or inline text/markdown/html.** Article bodies must be uploaded via `artifacts.prepare` and referenced through `resource.artifacts`.
- **Never guess a `namespace` value on `search.hybrid`.** It's required and the 37-value enum is documented — see `skills/7-agent-building/references/api-contracts.md`.

---

## 9. Related files

| File | Role |
| --- | --- |
| `skills/8-devrev-api/references/Support_Knowledge_and_SLAs_API.md` | Full article CRUD + body-artifact retrieval |
| `skills/8-devrev-api/references/Directories_Collections_API.md` | Directory CRUD (create/get/list/count/update/delete) |
| `skills/8-devrev-api/references/Platform_and_Admin_API.md` | Artifacts (prepare / upload / locate / download) |
| `skills/8-devrev-api/references/DevRev_Building_Org_Using_API_v1.md` | Building the Trail (parts.create with `parent_part`) |
| `skills/7-agent-building/references/api-contracts.md` | HybridSearch / FetchObjectContext trigger DONs + `namespace` enum |
| `skills/3-data-upload-and-org-build/SKILL.md` (Field notes) | Live-verified Trail-build behavior (parts.list depth, delete-order, etc.) |
| `docs/LEARNINGS.md` | Dated journal (2026-07-20 depth gotcha, 2026-07-21 article-body chain, 2026-07-31 doc reconciliation) |
