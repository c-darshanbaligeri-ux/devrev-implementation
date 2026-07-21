# DevRev public API — master catalog

Every public DevRev REST endpoint, grouped by domain, with the HTTP method and
the OAuth scope(s) required. This is the authoritative index for the whole
folder. Source: DevRev auto-generated API-to-scope reference.

Excluded by design (not covered in this folder): AI agents, workflows, and
AirSync connectors — see skills 6, 7, 9 for those.

| Field | Detail |
| --- | --- |
| Base URL | https://api.devrev.ai |
| Auth | `Authorization: Bearer <TOKEN>` on every request |
| Content type | `application/json` |
| Method note | Most endpoints accept both GET (query params) and POST (JSON body). Prefer POST for anything with a non-trivial body. |
| Scope note | "None" means no scope is required, though object-level read/write access still applies. Ranges like `x:read,x:write,x:all` mean any one of those grants access. |
| `/internal/` prefix | **Some endpoints live only under `/internal/`, not the public root.** Verified live 2026-07-18: `POST https://api.devrev.ai/internal/ai-agents.list` works with `Bearer $DEVREV_PAT`, while `POST /ai-agents.list` returns HTTP 404 "route not found". Skill 7 also uses `/internal/workflows.trigger` and other internal paths. If a documented endpoint 404s from the public root, try `/internal/<endpoint>` before assuming the endpoint is gone. **Confirmed live 2026-07-18, same pattern**: `objects.bulk-upgrade` exists ONLY at `/internal/objects.bulk-upgrade` — `{"type":"ticket"}` → HTTP 200 `{"id":"<job_don>"}` (poll via `jobs.get` for `job_category:"bulk_upgrade"`). This closes the long-open "is bulk-upgrade real" question — it is, just internal-only. |
| Required list-filter params | <!-- corrected 2026-07-18: was "webhooks.list needs at least one filter param" --> **`webhooks.list` is the opposite of a normal `.list`: it accepts NO extra fields at all, not even `limit` or `cursor`.** Verified live 2026-07-18: `POST /webhooks.list` with body `{}` (or GET with no query params) returns `200 {"webhooks":[...]}`; adding `{"limit":10}` returns `400 {"type":"invalid_field","field_name":"limit"}`, and likewise for `cursor`, `id`, `name`, `event_types`. The only way to make the earlier-reported 400 happen is to send a body with *any* field in it — the fix is to send fewer params (an empty `{}`), not more. If another `.list` 400s with `type: invalid_field`, try removing the offending field before assuming a filter is missing. |
| Response-wrapper drift | Response bodies use different top-level keys per op. Verified live 2026-07-18, **corrected 2026-07-19 — the original ".list returns {result, cursor}" line below was an overgeneralization**: `.create` typically returns `{"id": "..."}` or `{"<type>": {...}}` (e.g. `custom_state`, `custom_stage`, `fragment`); `.get` returns `{"<type>": {...}}`. For `.list`: **most typed/stock-object endpoints wrap under the plural type name** — `{"accounts":[...]}`, `{"tags":[...]}`, `{"jobs":[...]}`, `{"rev_orgs":[...]}`, `{"rev_users":[...]}`, `{"sla_trackers":[...]}`, `{"dev_users":[...]}`, `{"groups":[...]}`, `{"webhooks":[...]}`, `{"conversations":[...]}`, `{"surveys":[...]}`, `{"meetings":[...]}`, `{"org_schedules":[...]}`, `{"vistas":[...]}` — the generic `{"result": [...]}` wrapper is used only by the "customization" family: `link-types.custom.list`, `custom-objects.list`, `schemas.custom.list`. The pagination cursor field, where present, is named **`next_cursor`**, not `cursor` (seen on `tags.list`, `groups.list`). `link-types.custom.list` additionally returns an undocumented `reverse_result` array alongside `result`. When parsing, check the plural-type-name wrapper first, fall back to `result`, and never assume `{"schema": ...}` etc. |
| `ping` needs a JSON body, not just headers | **New 2026-07-19**: `POST /ping` with `Content-Type: application/json` set but **zero-length body** returns `HTTP 400 {"type":"invalid_content_type"}` — root cause is the header/body-length mismatch, not `/ping` specifically: any endpoint sent `Content-Type: application/json` with no body content is liable to the same rejection. Fix: always pair a JSON `Content-Type` with an actual body (`-d '{}'` at minimum), or omit the header entirely for a bodyless GET/POST. A `GET /ping` with no body works with no such gotcha. |

Detailed payloads and examples live in the domain docs — see `CLAUDE.md` for the
routing table. This file is the lookup index; go to the domain doc to build a call.

---

## Works (issue, ticket, task, incident, opportunity)
Scope varies by work type (e.g. `issue:*`, `ticket:*`, `opportunity:*`, `task:*`, `incident:*`).

| Endpoint | Method | Scope (write example) |
| --- | --- | --- |
| `works.create` | POST | `<type>:write` / `<type>:all` |
| `works.update` | POST | `<type>:write` / `<type>:all` |
| `works.delete` | POST | `<type>:all` |
| `works.get` | GET/POST | `<type>:read` … |
| `works.list` | GET/POST | `<type>:read` … |
| `works.count` | GET/POST | `<type>:read` … |
| `works.export` | GET/POST | `<type>:read` … |

**Idempotency (confirmed live 2026-07-18)**: `works.create` accepts an `external_ref` (string, unique per work type). Re-creating with the same `external_ref` returns **HTTP 409** `{"type":"conflict"}`, not a duplicate and not a silent no-op — catch the 409 and look the record up. The matching `works.list` filter field is `external_ref` (singular, takes an array) — `external_refs` (plural) returns HTTP 400 `invalid_field`. See `skills/3-data-upload-and-org-build/SKILL.md` Field notes for the full pattern.

**`applies_to_part` is required on `works.create` (confirmed live 2026-07-19)**, not merely a "common field" as prior examples implied — omitting it returns `HTTP 400` (a diagnostic `missing_required_field field_name:"applies_to_part"` for `issue`; an opaque `bad_request` with no field name for `ticket`).

**`works.delete` confirmed live and genuinely working (2026-07-19)** — `HTTP 200 {}`, and a follow-up `.get` returns `HTTP 404`. Not previously verified live; this repo's CLAUDE.md Safety list correctly flags all `.delete` calls as destructive/confirm-first, but didn't previously state whether this one actually succeeds. It does — treat it as a real, working destructive operation, same tier as `tags.delete`/`links.delete`/`workflows.delete`.

**Artifacts on works (confirmed live 2026-07-18)**: `works.create` accepts an `artifacts: ["<ARTIFACT_DON>"]` array at create time — the artifact renders fully in the response. An artifact can be attached to exactly ONE parent ever (work item, timeline comment, etc.) — reusing an artifact id on a second object returns HTTP 400 `{"type":"artifact_already_attached_to_a_parent","existing_parent":"<don>"}`.

## Timeline entries & reactions
Scope = read/write of the parent object's type (e.g. `issue:write` to post on an issue).

| Endpoint | Method |
| --- | --- |
| `timeline-entries.create` | POST |
| `timeline-entries.update` | POST |
| `timeline-entries.delete` | POST |
| `timeline-entries.get` | GET/POST |
| `timeline-entries.list` | GET/POST |
| `reactions.list` | GET/POST |
| `reactions.update` | POST |

## Tags
| Endpoint | Method | Scope |
| --- | --- | --- |
| `tags.create` | POST | `tag:write` / `tag:all` |
| `tags.update` | POST | `tag:write` / `tag:all` |
| `tags.delete` | POST | `tag:all` |
| `tags.get` / `tags.list` | GET/POST | `tag:read` … |

## Links
| Endpoint | Method | Scope |
| --- | --- | --- |
| `links.create` | POST | `link:write` / `link:all` (+ read on both objects) |
| `links.replace` | POST | `link:write` / `link:all` (+ read on both). Atomic only for part-to-part default link types |
| `links.delete` | POST | `link:all` (+ read on both) |
| `links.get` / `links.list` | GET/POST | `link:read` … |

## Custom link types
| Endpoint | Method | Scope |
| --- | --- | --- |
| `link-types.custom.create` | POST | `custom_link_type:write` |
| `link-types.custom.update` | POST | `custom_link_type:write` (also used to deprecate) |
| `link-types.custom.get` / `.list` | GET/POST | none |

Note: custom link types cannot be deleted, only deprecated (`deprecated: true`
via `.update`). There is no `link-types.custom.delete`.

## Atoms (generic object fetch)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `atoms.get` | GET/POST | `<object_type>:read` (derived from the id) |

---

## Parts (product / capability / feature)
The scope tracks the part type (like works). Source: `DevRev_Building_Org_Using_API_v1.md` Phase 2.
| Endpoint | Method | Scope |
| --- | --- | --- |
| `parts.create` | POST | `product:write,product:all` (product) / `capability:write,capability:all` (capability) / `feature:write,feature:all` (feature) |
| `parts.list` | GET/POST | corresponding `<part_type>:read,...` |
| `parts.delete` | POST | corresponding `<part_type>:all` (confirmed live 2026-07-20: works, `HTTP 200 {}`, `.get` 404s after; but a part with an existing `is_part_of` child link pointing to it 400s — delete children first) |
| `parts.update` | POST | corresponding `<part_type>:write,...` (confirmed live 2026-07-21: requires `type` in the payload alongside `id` and the changed fields — `{"id":...,"description":...}` alone 400s `bad_request` with no field name; `{"id":...,"type":"product","description":...}` → HTTP 200 with the full updated `part`. Used to set the stock `description` field, present on all part leaf types.) |

Hierarchy: product (root) → capability (`parent_part` = product) → feature (`parent_part` = capability or feature).
A Trail is **not** a separate object — there is no `trails.create`; it's the rendered part hierarchy plus links.
`parts.list`'s `parent_part:{"parts":[<don>]}` filter matches descendants at ANY depth, not just direct children (confirmed live 2026-07-20) — `parts.get`/`.list` never expose a part's own parent, so for an exact immediate-parent check use `links.list` (part as `object`, `link_type:"is_part_of"`, part as `source`, parent as `target`).
(Other `parts.*` verbs are not documented in this folder's references — verify against the official API reference before use.)

---

## Accounts
| Endpoint | Method | Scope |
| --- | --- | --- |
| `accounts.create` | POST | `account:write` / `account:all` |
| `accounts.update` | POST | `account:write` / `account:all` |
| `accounts.delete` | POST | `account:all` |
| `accounts.merge` | POST | `account:all` |
| `accounts.get` / `.list` / `.export` | GET/POST | `account:read` … |

## Rev orgs (workspaces / customer orgs)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `rev-orgs.create` | POST | `rev_org:write` / `rev_org:all` |
| `rev-orgs.update` | POST | `rev_org:write` / `rev_org:all` |
| `rev-orgs.delete` | POST | `rev_org:all` |
| `rev-orgs.get` / `.list` | GET/POST | `rev_org:read` … |

## Rev users (customers / contacts)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `rev-users.create` | POST | `rev_user:write` / `rev_user:all` |
| `rev-users.update` | POST | `rev_user:write` / `rev_user:all` |
| `rev-users.delete` | POST | `rev_user:all` |
| `rev-users.merge` | POST | `rev_user:all` |
| `rev-users.get` / `.list` / `.scan` | GET/POST | `rev_user:read` … |

## Dev users (internal users)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `dev-users.create` | POST | `dev_user:write` / `dev_user:all` |
| `dev-users.update` | POST | `dev_user:write` / `dev_user:all` |
| `dev-users.activate` | POST | `dev_user:write` / `dev_user:all` |
| `dev-users.deactivate` | POST | `dev_user:all` |
| `dev-users.merge` | POST | `dev_user:all` |
| `dev-users.identities.link` / `.unlink` | POST | `dev_user:write` / `dev_user:all` |
| `dev-users.get` / `.list` | GET/POST | `dev_user:read` … |
| `dev-users.self` / `.self.update` | GET/POST | None |

## Dev orgs
| Endpoint | Method | Scope |
| --- | --- | --- |
| `dev-orgs.get` | GET/POST | `dev_org:read` / `dev_org:write` |

## Groups & directory
| Endpoint | Method | Scope |
| --- | --- | --- |
| `groups.create` / `.update` | POST | `group:write` / `group:all` |
| `groups.get` / `.list` | GET/POST | `group:read` … |
| `groups.members.add` / `.remove` | POST | `group_membership:all` |
| `groups.members.list` | GET/POST | `group_membership:read` / `:all` |
| `directories.create` / `.update` | POST | `directory:write` / `directory:all` |
| `directories.delete` | POST | `directory:all` |
| `directories.get` / `.list` / `.count` | GET/POST | `directory:read` … |

## Service accounts & system users
| Endpoint | Method | Scope |
| --- | --- | --- |
| `service-accounts.create` | POST | None (user auth only) |
| `service-accounts.get` | GET/POST | `svcacc:read` |
| `sys-users.list` / `.update` | GET/POST | None |

---

## Conversations
| Endpoint | Method | Scope |
| --- | --- | --- |
| `conversations.create` / `.update` | POST | `conversation:write` / `conversation:all` |
| `conversations.delete` | POST | `conversation:all` |
| `conversations.get` / `.list` | GET/POST | `conversation:read` … |

## Chats
| Endpoint | Method | Scope |
| --- | --- | --- |
| `chats.create` / `.get` / `.update` | POST/GET | None (chat membership governs access) |

## Articles (knowledge base)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `articles.create` / `.update` | POST | `article:write` / `article:all` |
| `articles.delete` | POST | `article:all` (confirmed live 2026-07-21: genuinely works, `HTTP 200 {}`, `.get` 404s after) |
| `articles.get` / `.list` | GET/POST | `article:read` … |

**`articles.create` minimal payload (corrected 2026-07-19)** — see `Support_Knowledge_and_SLAs_API.md` §3 for the full corrected example. `owned_by` is required (not just good practice); `content_format:"rt"` paired with `owned_by` alone returns an opaque `HTTP 400 bad_request` with no diagnostic field name — the working minimal payload is `{title, owned_by, resource}` (an empty `resource: {}` object, not `content_format`).

**Article body content (confirmed live 2026-07-21, see `Support_Knowledge_and_SLAs_API.md` §3a)** — the only working content mechanism is `resource.artifacts: [<artifact_don>]` (upload via `artifacts.prepare` first, same pattern as work-item attachments). `resource.rich_text`/`.content`/`.markdown`/`.html`/`.artifact_id`/`.artifact` and a top-level `artifacts` array are all rejected (`invalid_field`). Never send `resource.type` even though it's a real enum field in the schema — the API rejects it outright alongside `resource.artifacts`. `scope` takes a number (`1`=internal, `2`=external, default), not a string — `{"scope":"internal"}` 400s `unexpected_json_type`. The part-link field is `applies_to_parts` (array, max 10), **not** `applies_to_part_ids` (400s `invalid_field`).

## Directories (Help Center collections) — confirmed live 2026-07-21
A "collection" in the Help Center UI is the `directory` object at the API layer — there is no `collections.*` or `article-collections.*` endpoint (both 404 route-not-found).
| Endpoint | Method | Scope |
| --- | --- | --- |
| `directories.create` / `.update` | POST | `directory:write` / `directory:all` |
| `directories.delete` | POST | `directory:all` |
| `directories.get` / `.list` / `.count` | GET/POST | `directory:read`, `:write`, or `:all` |

Fields: `title` (required), `description`, `parent` (directory id — omit for top-level; nests infinitely), `published` (bool), `tags` (max 20). Articles join a collection from the **article** side — set the article's `parent` field to the directory's DON on `articles.create`/`.update`; an article belongs to only one collection at a time. Full detail: `Support_Knowledge_and_SLAs_API.md` §3b.

## Surveys
| Endpoint | Method | Scope |
| --- | --- | --- |
| `surveys.create` / `.update` / `.send` | POST | `survey:write` / `survey:all` |
| `surveys.delete` | POST | `survey:all` |
| `surveys.get` / `.list` | GET/POST | `survey:read` … |
| `surveys.submit` | POST | `survey_response:write` / `:all` |
| `surveys.responses.list` | GET/POST | `survey_response:read` … |
| `surveys.responses.update` | POST | `survey_response:write` / `:all` |

## Meetings
| Endpoint | Method | Scope |
| --- | --- | --- |
| `meetings.create` / `.update` | POST | `meeting:write` / `meeting:all` |
| `meetings.delete` | POST | `meeting:all` |
| `meetings.get` / `.list` / `.count` | GET/POST | `meeting:read` … |

## SLAs, metrics & trackers
| Endpoint | Method | Scope |
| --- | --- | --- |
| `slas.create` / `.update` / `.assign` / `.transition` | POST | `sla:write` |
| `slas.get` / `.list` | GET/POST | `sla:read` / `sla:write` |
| `metric-definitions.create` / `.update` | POST | `metric_definition:write` / `:all` |
| `metric-definitions.delete` | POST | `metric_definition:all` |
| `metric-definitions.get` / `.list` | GET/POST | `metric_definition:read` … |
| `metric-action.execute` | POST | None |
| `metric-trackers.get` | GET/POST | None |
| `sla-trackers.get` / `.list` | GET/POST | None |

---

## Artifacts (files)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `artifacts.prepare` | POST | `artifact:create` |
| `artifacts.versions.prepare` / `.delete` | POST | `artifact:create` |
| `artifacts.download` | GET/POST | `artifact:read` |
| `artifacts.get` / `.list` / `.locate` | GET/POST | `artifact:read` (+ parent read) |

## Webhooks
| Endpoint | Method | Scope |
| --- | --- | --- |
| `webhooks.create` / `.update` / `.delete` / `.event` | POST | None (default scopes N/A) |
| `webhooks.get` / `.list` | GET/POST | None |

**`webhooks.create` confirmed live 2026-07-19**: the response includes a `secret` field not shown in prior examples (needed for signature verification — capture it at create time, it may not be re-exposed later), and the server silently appends a `"verify"` entry to `event_types` alongside whatever was requested.

## Jobs
| Endpoint | Method | Scope |
| --- | --- | --- |
| `jobs.get` / `.list` | GET/POST | `job:read` |

## Keyrings
| Endpoint | Method | Scope |
| --- | --- | --- |
| `keyrings.authorize` | GET/POST | `keyring:read` |

## Schedules (org schedules & fragments)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `org-schedules.create` / `.update` / `.transition` / `.set-future` | POST | `org_schedule:write` / `:all` |
| `org-schedules.get` / `.list` / `.evaluate` | GET/POST | `org_schedule:read` … |
| `org-schedule-fragments.create` / `.transition` | POST | `org_schedule_fragment:write` / `:all` |
| `org-schedule-fragments.get` | GET/POST | `org_schedule_fragment:read` … |

## Vistas (views)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `vistas.get` / `.list` | GET/POST | `vista:read` … |
| `vistas.delete` | POST | `vista:all` |
| `vistas.groups.get` / `.list` | GET/POST | `vista:read` … (none for default vistas) |
| `vistas.groups.delete` | POST | `vista:all` |

## Observability (sessions)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `observability.sessions.get` / `.list` / `.aggregate` | GET/POST | None |
| `observability.sessions.data.get` | GET/POST | None |
| `observability.sessions.developer-info.get` | GET/POST | None |

## Web crawler jobs
| Endpoint | Method | Scope |
| --- | --- | --- |
| `web-crawler-jobs.create` / `.control` | POST | `web_crawler_job:all` |
| `web-crawler-jobs.get` / `.list` | GET/POST | `web_crawler_job:all` |

## Snap widgets & snap-kit
| Endpoint | Method | Scope |
| --- | --- | --- |
| `snap-widgets.create` | POST | `snap_widget:write` / `:all` |
| `snap-kit-action.execute.deferred` | POST | `snap_widget:write` / `:all` |

## Commands
| Endpoint | Method | Scope |
| --- | --- | --- |
| `commands.create` / `.update` | POST | `command:write` / `command:all` |
| `commands.get` / `.list` | GET/POST | `command:read` … |

## Code changes
| Endpoint | Method | Scope |
| --- | --- | --- |
| `code-changes.create` / `.update` | POST | `code_change:write` / `:all` |
| `code-changes.delete` | POST | `code_change:all` |
| `code-changes.get` / `.list` | GET/POST | `code_change:read` … |

## Auth tokens & connections
| Endpoint | Method | Scope |
| --- | --- | --- |
| `auth-tokens.create` / `.update` / `.delete` / `.self.delete` | POST | None |
| `auth-tokens.get` / `.list` / `.info` | GET/POST | None |
| `dev-orgs.auth-connections.*` | POST/GET | None (user auth only; not via service account) |

## Customization (schemas, custom objects, stages, states, diagrams)
See `Stock_Object_Modification_and_Schemas_API.md`, `Custom_Objects_and_Links_API.md`,
and `Stages_States_and_StageDiagrams_API.md` for full detail. Endpoints:
`schemas.custom.set/get/list`, `schemas.stock.get/list`, `schemas.aggregated.get`,
`schemas.subtypes.list`, `schemas.subtypes.prepare-update`,
`custom-objects.create/update/delete/get/list/count`,
`stages.custom.*`, `states.custom.*`, `stage-diagrams.*`.

**`custom-objects.list`/`.count` require `leaf_type` (confirmed live 2026-07-19)** — omitting it
returns `HTTP 400 missing_required_field field_name:"leaf_type"`. **`custom-objects.delete`
confirmed live and genuinely working** (`HTTP 200 {}`, then `.get` 404s). **`schemas.subtypes.list`
requires a `leaf_type` filter to return anything** — called bare (`{}`) it always returns
`{"subtypes":[]}` regardless of what exists; with `leaf_type` supplied it reflects newly created
subtypes immediately, no indexing delay (this corrects an earlier over-general "subtypes.list has
an indexing delay" finding — see `skills/1-object-schema-customization/SKILL.md` Field notes).

## Health
| Endpoint | Method | Scope |
| --- | --- | --- |
| `ping` | GET/POST | None |
