---
name: devrev-rest-api
description: Read and modify DevRev data through the public REST API — work items (tickets/issues/tasks/incidents/opportunities), timelines, tags, links, accounts and users, conversations, articles, surveys, meetings, SLAs, artifacts, webhooks, schedules, vistas, custom objects, schema/stage customization, and full org builds. Use whenever the user wants to call a DevRev API endpoint or automate a DevRev operation. Does NOT cover AI agents, workflows, or AirSync connectors.
---

# DevRev REST API — executable playbook

Use this to perform any DevRev operation via the REST API. It routes a request
to the right endpoint and doc, and gives the order and safety checks. Read
`CLAUDE.md` first for the global rules; use `references/00_API_Catalog.md` to look up any
endpoint + scope.

## When to use

Trigger when the user wants to create, read, update, delete, link, tag, comment
on, or otherwise operate on DevRev objects programmatically — or build/customize
an org.

## When not to use

- Workflows & agent-callable skills → `skills/6-workflows`
- AI agent configs → `skills/7-agent-building`
- Dashboards → `skills/4-dashboards-and-widgets`
- Datasets → `skills/5-datasets`

## Preconditions

1. A bearer token is available from repo-root `.env` (`DEVREV_PAT`). Alias for scripts: `export DEVREV_TOKEN="$DEVREV_PAT"`. If missing, ask.
2. The token holds the scope for the target endpoint (see `references/00_API_Catalog.md`).
3. For creates that reference parents (rev_user → rev_org → account, work →
   part), the parent objects exist and you have their DON ids.

## Standard headers

```bash
-H "Authorization: Bearer $DEVREV_TOKEN" \
-H "Content-Type: application/json" \
-H "Accept: application/json"
```

## How to handle any request

1. Identify the object/domain from the request.
2. Look up the endpoint and required scope in `references/00_API_Catalog.md`.
3. Open the domain doc (routing table below) for the payload and a worked example.
4. Substitute real DON ids; run the call; save returned ids.
5. Verify with the matching `*.get`/`*.list`. For destructive ops, confirm first.

## Routing table — domain → doc → key endpoints

| Domain | Doc | Key endpoints |
| --- | --- | --- |
| Work items | `references/Work_Items_Timeline_Tags_Links_API.md` | works.create/update/list/get/count/export/delete |
| Timeline / comments | `references/Work_Items_Timeline_Tags_Links_API.md` | timeline-entries.*, reactions.* |
| Tags | `references/Work_Items_Timeline_Tags_Links_API.md` | tags.* |
| Links | `references/Work_Items_Timeline_Tags_Links_API.md` + `references/Custom_Objects_and_Links_API.md` | links.*, link-types.custom.* |
| Parts (product/capability/feature) | `references/DevRev_Building_Org_Using_API_v1.md` Phase 2 | parts.create/list (scope tracks part type) |
| Accounts / orgs / users | `references/Customers_Users_and_Orgs_API.md` | accounts.*, rev-orgs.*, rev-users.*, dev-users.*, groups.* |
| Conversations / chats | `references/Support_Knowledge_and_SLAs_API.md` | conversations.*, chats.* |
| Articles (KB) | `references/Support_Knowledge_and_SLAs_API.md` §3, §3a | articles.* |
| Collections (Help Center) | `references/Support_Knowledge_and_SLAs_API.md` §3b, `references/Directories_Collections_API.md` | directories.* (directory = collection; not related to groups/users) |
| Surveys | `references/Support_Knowledge_and_SLAs_API.md` | surveys.*, surveys.responses.* |
| Meetings | `references/Support_Knowledge_and_SLAs_API.md` | meetings.* |
| SLAs / metrics | `references/Support_Knowledge_and_SLAs_API.md` | slas.*, metric-definitions.*, *-trackers.* |
| Artifacts / files | `references/Platform_and_Admin_API.md` | artifacts.prepare/download/get/list |
| Webhooks | `references/Platform_and_Admin_API.md` | webhooks.* |
| Jobs / keyrings | `references/Platform_and_Admin_API.md` | jobs.*, keyrings.authorize |
| Schedules | `references/Platform_and_Admin_API.md` | org-schedules.*, org-schedule-fragments.* |
| Vistas / views | `references/Platform_and_Admin_API.md` | vistas.*, vistas.groups.* |
| Observability | `references/Platform_and_Admin_API.md` | observability.sessions.* |
| Web crawler | `references/Platform_and_Admin_API.md` | web-crawler-jobs.* |
| Snap widgets / commands / code changes / tokens | `references/Platform_and_Admin_API.md` | snap-widgets.create, commands.*, code-changes.*, auth-tokens.* |
| Custom objects / links | `references/Custom_Objects_and_Links_API.md` | custom-objects.*, link-types.custom.* |
| Stock objects / schemas | `references/Stock_Object_Modification_and_Schemas_API.md` | schemas.custom.set, schemas.stock.*, schemas.aggregated.get (bulk-upgrade unverified — see doc) |
| Stages / states / lifecycle | `references/Stages_States_and_StageDiagrams_API.md` | states.custom.*, stages.custom.*, stage-diagrams.* |
| Full org build | `references/DevRev_Building_Org_Using_API_v1.md` | ordered end-to-end |
| **Trail × Articles × Directories (cross-cutting)** | `references/Trail_Articles_Directories_Model.md` | how `is_part_of`, `applies_to_parts`, and `article.parent` wire together; retrieval ladder; grounding recipes |

## Common recipes

- File a ticket from a report: `works.create` (type ticket) → optionally
  `timeline-entries.create` for context → `links.create` to relate to an issue.
- Onboard a customer: `accounts.create` → `rev-orgs.create` → `rev-users.create`.
- Publish KB content: `articles.create` (status draft) → review →
  `articles.update` (status published).
- Stand up support metrics: `metric-definitions.create` → `slas.create` →
  `slas.assign` → check `sla-trackers.get`.
- Attach a file: `artifacts.prepare` → upload bytes to returned URL → reference
  the artifact id on the parent object.

## Scratchpad (track DON ids)

```
ACCOUNT_ID=      REV_ORG_ID=      REV_USER_ID=     DEVU_ID=
PRODUCT_ID=      CAP_ID=          FEAT_ID=         PART_ID=
WORK_ID=         ARTIFACT_ID=     SLA_ID=          SURVEY_ID=
CUSTOM_OBJECT_ID= CUSTOM_LINK_TYPE_ID= STAGE_DIAGRAM_ID=
```

## Safety checklist

- Confirm before any `*.delete`, `*.merge`, deprecation, `objects.bulk-upgrade`,
  or `web-crawler-jobs.control` — these are destructive/irreversible.
- Never commit the token; read it from the environment.
- Always use DON ids, never display IDs.
- If a call returns 403, report the missing scope from `references/00_API_Catalog.md` rather
  than retrying blindly.

## Accuracy notes (verified against the DevRev API-to-scope reference)

- Custom link types: create/update/get/list only. **No `link-types.custom.delete`**
  — deprecate with `deprecated: true` via `.update`. Write scope
  `custom_link_type:write`.
- `links.replace` is atomic only for part-to-part default link types; otherwise a
  non-atomic delete+create that must keep the same link type and share an endpoint.
- `objects.bulk-upgrade` — **confirmed live 2026-07-18**: exists ONLY at
  `/internal/objects.bulk-upgrade` (public-root `objects.bulk-upgrade` 404s).
  `{"type":"<obj_type>"}` → HTTP 200 `{"id":"<job_don>"}`; poll `jobs.get` for
  `job_category:"bulk_upgrade"` / `state:"completed"`. Affects ALL records of
  that type org-wide — confirm before running; prefer re-saving a single
  record via its `*.update` with the current `custom_schema_spec` instead.
- Tags on custom objects are modeled as a custom field (an `id`-typed field with
  `id_type: ["tag"]`, or an enum/tokens field), not the native `tags` property
  that stock objects (works, parts, accounts) expose.
- **Rate limits — the repo-root `rate limits.md` document's numbers are wrong,
  confirmed live 2026-07-24.** That doc states a 600 req/min "Standard tier"
  ceiling. A real org on this token (`devo/24TiM4xJFF`) showed
  `x-ratelimit-limit: 8000` and a clean 60-second rolling window (`x-ratelimit-reset`
  landed on an exact 60s boundary from request time) on ordinary `works.list`
  calls — over 13x the documented number. Don't hardcode either number as a
  planning assumption for a new org/token; read `x-ratelimit-limit` and
  `x-ratelimit-remaining` from the live response headers every time and pace
  off those, not off any static table (this repo's or otherwise). The general
  shape of `rate limits.md`'s advice (adaptive delay tiers by quota %, 429
  exponential backoff respecting `Retry-After`, circuit breaker after N
  consecutive 429s) is sound and reusable — only the specific tier numbers are
  unverified/wrong.
- **`works.list` filter shape for subtype — undocumented anywhere in this repo
  until confirmed live 2026-07-24**: `{"type":["issue"], "issue":{"subtype":["<value>"]}}`
  (nested under the type name as its own object key), NOT a top-level `"subtype"`
  array (`400 invalid_field field_name:"subtype"`) and NOT `custom_schema_spec`
  (`400 invalid_field field_name:"custom_schema_spec"`, that field is
  create/update-only). Verified both that a real subtype value returns matching
  records with `"subtype":"<value>"` echoed on each, and that a bogus subtype
  value returns `{"works":[]}` — confirms the filter is genuinely applied, not
  silently ignored.

## Verify

```bash
curl -X POST 'https://api.devrev.ai/ping' -H "Authorization: Bearer $DEVREV_TOKEN" -d '{}'
curl -X POST 'https://api.devrev.ai/works.list' -H "Authorization: Bearer $DEVREV_TOKEN" -d '{ "type": ["ticket"], "limit": 5 }'
```

## Field notes (live-learned; see docs/LEARNINGS.md)

Dated facts discovered while operating this domain — errors hit, restrictions found, behaviors that
differ from the references. Add entries via the `capture-learnings` protocol
(`.claude/skills/capture-learnings/SKILL.md`): one dated bullet per fact, with evidence. If a fact
*corrects* a reference doc, fix the doc in place too — this section is for knowledge that has no
better home or needs domain-level visibility.

- (2026-07-18) `webhooks.list` accepts **zero** fields — even `limit`/`cursor` return
  `400 {"type":"invalid_field","field_name":"<field>"}`. Call it with a bare `{}`. (Corrects a prior
  session's note that it "needs a filter param" — see `00_API_Catalog.md`.)
- (2026-07-18) `works.update` requires `"type"` in the payload whenever you set a type-specific
  field (e.g. `severity`) — omitting it returns `400 {"type":"invalid_field","field_name":"<field>"}`,
  not a silent ignore.
- (2026-07-18) `links.create` with a built-in `link_type` can 400 with an opaque
  `{"type":"bad_request"}` (no `field_name`) when the type isn't valid for that
  (source-type, target-type) pair — e.g. `is_related_to`/`is_part_of` ticket→issue both failed while
  `is_dependent_on` ticket→issue and `is_related_to` issue→issue succeeded. Try a different built-in
  type before assuming the request is malformed.
- (2026-07-18) `links.delete` and `tags.delete` both genuinely delete (verified via a subsequent
  404 on `.get`) — unlike custom link types, stages/states, and custom-object schema fragments,
  which have no delete and are deprecate-only or permanent.
- (2026-07-21) **A Help Center "collection" is the `directory` object, not a `collections.*`
  endpoint** (that name space 404s entirely). `directories.create` confirmed live; articles join a
  collection via the article's own `parent` field (max one collection per article), not from the
  directory side. `directory` was previously miscategorized in
  `Customers_Users_and_Orgs_API.md` §6 as a groups/users container — corrected in place; the real
  home is `Support_Knowledge_and_SLAs_API.md` §3b and `Directories_Collections_API.md`.
- (2026-07-21) **Article body content only works via `resource.artifacts` (artifact upload), not
  any inline text field.** `resource.rich_text`/`.content`/`.markdown`/`.html` and a top-level
  `artifacts` array are all rejected `invalid_field`; `resource.type` is a real schema field but the
  API rejects it outright even when valid otherwise — never send it. `scope` takes a number
  (`1`=internal, `2`=external), not a string. The part-link field is `applies_to_parts`, not
  `applies_to_part_ids`. Full detail: `Support_Knowledge_and_SLAs_API.md` §3a.
