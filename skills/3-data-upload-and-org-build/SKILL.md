---
name: data-upload-and-org-build
description: Upload files and artifacts to DevRev, attach files to objects, migrate data via bulk record creation, and build a complete DevRev org from scratch (end-to-end org setup with customization → parts → Trails → links → work). Use when you need to upload files, attach artifacts, load CSV data, create many records, or stand up a full customer org programmatically. Covers artifacts.prepare/upload, ordered org build phases, bulk data loading patterns, and idempotent record creation.
---

# Data upload & org build — executable playbook

Upload files and artifacts to DevRev, migrate data programmatically, and build a complete customer organization from scratch through the API. Read the repo root `CLAUDE.md` first for global API rules; use this skill for file uploads, bulk data loads, or end-to-end org setup requests.

## When to use

Trigger when the user wants to:
- Upload a file or attach an artifact to a work item, timeline entry, or other object
- Migrate data from another system (load records programmatically)
- Build a fresh DevRev org from scratch (end-to-end setup)
- Bulk create records (tickets, accounts, custom objects, parts)
- Import data from CSV or another source
- Stand up a demo or proof-of-concept environment

## When not to use

- Object schema customization (fields, subtypes, custom objects) → `skills/1-object-schema-customization`
- Stage/state/lifecycle customization → `skills/2-stage-lifecycle-customization`
- Raw API calls with no data loading → `skills/8-devrev-api`

## Preconditions

1. Token in `.env` (`DEVREV_PAT`). If missing, tell the user exactly what to put in it and stop — never fabricate a token.
2. Verify token works: `POST https://api.devrev.ai/ping` before starting.
3. Required scopes (from `references/Platform_and_Admin_API.md` §1 and `references/DevRev_Building_Org_Using_API_v1.md`):
   - `artifact:create` for `artifacts.prepare`
   - `artifact:read` for `artifacts.download` / `.get` / `.list` (plus parent object's read scope)
   - Object-specific write scopes for bulk record creation (e.g. `ticket:write`, `account:write`, `custom_type_fragment:write` for custom objects)
4. For operations referencing parent objects (e.g. attaching a file to a ticket, creating work items that reference parts), the parent DON ids must exist. Keep a DON scratchpad (see below).

## Playbooks

Every playbook step cites the exact reference file and section. Follow the order, substitute real DON ids, and verify after each change.

### Playbook 1 — Upload a file (artifact)

**Reference**: `references/Platform_and_Admin_API.md` §1 (Artifacts).

**You cannot POST bytes to `artifacts.create`** — always use the prepare-then-upload flow (§14 pitfall).

**Steps**:

1. **Prepare an upload** — `artifacts.prepare` (scope: `artifact:create`) returns a URL + form fields.

   ```bash
   curl -X POST 'https://api.devrev.ai/artifacts.prepare' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{ "file_name": "screenshot.png", "file_type": "image/png" }'
   ```

   The response contains an `upload_url` and optional `form_data` fields. Save the returned artifact id (`ARTIFACT_ID`) from the response.

2. **Upload the file bytes** — POST the file to the returned `upload_url` as multipart form data. Use the `form_data` fields if provided, and include the file contents.

   ```bash
   curl -X POST '<UPLOAD_URL>' \
   -F 'file=@/path/to/screenshot.png'
   ```

3. **Reference the artifact** — once uploaded, reference the artifact id on the parent object (e.g. a work item, timeline entry, or custom object). The exact field depends on the parent: typically `artifacts: [<ARTIFACT_ID>]` or similar.

4. **Verify** — `artifacts.get` or `artifacts.list` (scope: `artifact:read` + parent object's read scope) to confirm the artifact exists; `artifacts.download` to retrieve the file.

**Download a file**: `artifacts.download` with the artifact id returns a download URL.

```bash
curl -X POST 'https://api.devrev.ai/artifacts.download' \
-H 'Authorization: Bearer $DEVREV_TOKEN' \
-d '{ "id": "<ARTIFACT_ID>" }'
```

### Playbook 2 — Build a complete org from scratch (end-to-end)

**Reference**: `references/DevRev_Building_Org_Using_API_v1.md` (entire file).

This is the standard, repeatable procedure to build out a customer organization in DevRev through the API. It consolidates four core building blocks — object customization, parts creation, Trails, and custom links — into one ordered workflow.

**Scope**: this guide focuses on modeling the org (objects, product structure, relationships). It assumes the customer account and users already exist. It does not provision a brand-new Dev org tenant (a one-time step done from the DevRev app or during subscription).

**Ordering matters** (§4): shape the data model first, then the product structure, then the connections, then the work that hangs off them.

| Phase | Key endpoints | Produces |
| --- | --- | --- |
| 0 | Auth & prerequisites | A valid bearer token |
| 1 | Object customization | Subtypes, custom fields, custom objects |
| 2 | Parts | product / capability / feature / runnable IDs |
| 3 | Trail | A connected part hierarchy (the Trail) |
| 4 | Custom links | Custom relationships between objects |
| 5 | Work & verify | Tickets/issues on parts; verification |

#### Phase 0 — Prerequisites & authentication

Every request needs standard headers (`Authorization: Bearer $DEVREV_TOKEN`, `Content-Type: application/json`, `Accept: application/json`). Objects are referenced by their DON id (e.g. `don:core:dvrv-us-1:devo/0:product/1`). Save every id a call returns — later phases depend on them. Keep a scratchpad of IDs: `PRODUCT_ID`, `CAP_ID`, `FEAT_ID`, `RUN_ID`, and any custom link type IDs.

#### Phase 1 — Customize objects

**Reference**: `references/DevRev_Building_Org_Using_API_v1.md` Phase 1.

Object customization tailors DevRev's built-in objects (issue, ticket, opportunity, account, contact, part) or defines entirely new object types. The model is additive — you layer definitions on top of stock fields; built-in fields are never modified.

**ROUTE to `skills/1-object-schema-customization`** for:
- Adding a subtype with custom fields (§1.2)
- Tenant custom fields (§1.3)
- Custom stages & dependent fields (§1.4)
- Custom objects (§1.5)

**ROUTE to `skills/2-stage-lifecycle-customization`** for:
- Creating states, stages, and stage diagrams (§1.4)

After Phase 1, you have: subtypes, custom fields, custom objects, and optionally custom stages/diagrams defined. Save all DON ids.

#### Phase 2 — Create parts (the product hierarchy)

**Reference**: `references/DevRev_Building_Org_Using_API_v1.md` Phase 2.

Parts are the backbone of the customer's product model. Customer parts (product → capability → feature) form the hierarchy; builder parts (runnable, linkable) are internal components that power them.

1. **Create the product** (root; no parent):

   ```bash
   curl -X POST 'https://api.devrev.ai/parts.create' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{ "type": "product", "name": "Acme Platform",
     "owned_by": [ "<DEVU_OWNER_ID>" ] }'
   ```

   Save as `PRODUCT_ID`.

2. **Add a capability** under it, passing the product DON as `parent_part`:

   ```bash
   curl -X POST 'https://api.devrev.ai/parts.create' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{ "type": "capability", "name": "Authentication",
     "parent_part": [ "<PRODUCT_ID>" ], "owned_by": [ "<DEVU_OWNER_ID>" ] }'
   ```

   Save as `CAP_ID`.

3. **Add features** under the capability (`parent_part` = `CAP_ID`).

4. **Add builder parts** (type `runnable` / `linkable`) which have no `parent_part` — they join the model via links in Phase 3.

**Verify**: `parts.list` to confirm the hierarchy exists.

| Part type | Parent | Write scope |
| --- | --- | --- |
| product | none (root) | `product:write` OR `product:all` |
| capability | product | `capability:write` OR `capability:all` |
| feature | capability (or feature) | `feature:write` OR `feature:all` |
| runnable / linkable | none; linked in Phase 3 | (builder part scope) |

#### Phase 3 — Build the Trail

**Reference**: `references/DevRev_Building_Org_Using_API_v1.md` Phase 3.

**There is no `trails.create` endpoint** (§3). A Trail is the rendered view of the part hierarchy you just built plus the links between parts. Building the Trail means: (1) the `parent_part` relationships from Phase 2, and (2) connecting builder parts to the customer parts they power.

Link a runnable to the feature it serves with `links.create` using the built-in link type `serves`:

```bash
curl -X POST 'https://api.devrev.ai/links.create' \
-H 'Authorization: Bearer $DEVREV_TOKEN' \
-d '{ "link_type": "serves",
  "source": "<RUNNABLE_ID>",
  "target": "<FEATURE_ID>" }'
```

Common built-in link types: `serves`, `is_part_of`, `is_dependent_on`, `is_related_to`. Once parts are created and linked, open Product > Trails in the app to see the connected graph rendered visually.

**Important**: To move a part within the Trail later, use `links.replace` rather than delete-then-create, so you never leave a part orphaned without a parent. The replacement is **atomic only for part-to-part default (non-custom) link types**; for custom link types or non-part endpoints it runs as a non-atomic delete-then-create and the new link must keep the same type and share an endpoint (Phase 3 note).

**Verify**: `parts.list` to confirm the hierarchy; `links.list` on a part to see its connections.

#### Phase 4 — Define custom links & connect objects

**Reference**: `references/DevRev_Building_Org_Using_API_v1.md` Phase 4.

When you need a relationship that the built-in link types don't cover (e.g. tying a custom object to a ticket), define a custom link type once, then create link instances from it. Custom link types can be created between work objects, identity objects (account, rev/dev user, rev org), part objects, and any custom object leaf type.

**ROUTE to `skills/1-object-schema-customization` Playbook 4** for the full custom link type creation flow.

#### Phase 5 — Add work & verify

Attach work items to the right part so they surface on the Trail. Set `applies_to_part` on any ticket or issue you create — **confirmed live 2026-07-19: this field is actually required on `works.create`**, not just good practice. Omitting it returns `HTTP 400` (a diagnostic `missing_required_field field_name:"applies_to_part"` for `issue`; an opaque `bad_request` with no field name for `ticket`):

```bash
curl -X POST 'https://api.devrev.ai/works.create' \
-H 'Authorization: Bearer $DEVREV_TOKEN' \
-d '{ "type": "ticket", "title": "Login fails for Acme",
  "applies_to_part": "<FEATURE_ID>",
  "owned_by": [ "<DEVU_OWNER_ID>" ] }'
```

**Verify** the setup:
- `parts.list` — confirm the product hierarchy exists.
- `links.list` on a part — confirm builder parts, custom links, and work are attached.
- `schemas.custom.list` / `custom-objects.list` — confirm your fragments and custom objects.

**End-to-end worked example** (§end-to-end): see `references/DevRev_Building_Org_Using_API_v1.md` §"End-to-end worked example" for a numbered step-by-step walkthrough.

### Playbook 3 — Bulk record creation (data migration)

**Reference**: `references/DevRev_Building_Org_Using_API_v1.md` (concept); no public bulk-create endpoint exists.

**Be HONEST**: there is no public bulk-create endpoint in the API catalog. Bulk loads = deterministic scripted loops over `*.create`, made idempotent via `unique_key` (custom objects) or check-before-create (`*.list` filter). Safe to re-run; fail loudly on non-2xx.

**Pattern**:

1. **Prepare the data** — parse the CSV or source data into a list of records to create.

2. **Create records in order** (respect dependencies):
   - **Customer data ordering** (`references/Customers_Users_and_Orgs_API.md` §8, build order): `accounts.create` → `rev-orgs.create` → `rev-users.create`, top-down, saving each DON id.
   - **Parts ordering** (Phase 2): product → capability → feature, saving each DON id and passing `parent_part` to children.
   - **Work items** (Phase 5): after parts exist, create work items with `applies_to_part`.

3. **Idempotency**:
   - For **custom objects**: pass a stable `unique_key` on `custom-objects.create` (`references/DevRev_Building_Org_Using_API_v1.md` §1.5, Custom objects). Repeating the call with the same key won't create a duplicate.
   - For **work items (tickets/issues/etc.) specifically**: `works.create` has a real idempotency key — `external_ref` (must be unique within the work type). **Confirmed live 2026-07-18**: re-running `works.create` with the same `external_ref` returns **HTTP 409** `{"type":"conflict"}` rather than creating a duplicate or silently no-op-ing. Catch the 409 and look the record up via `works.list` with `{"external_ref": ["<value>"]}` (field name is singular `external_ref`, even though it takes an array — `external_refs` returns HTTP 400 `invalid_field`). Prefer this over generic check-before-create for work items.
   - For **other stock objects** (accounts, etc.) with no `external_ref`-equivalent: no native `unique_key`. Check-before-create pattern: `*.list` filtered by a unique attribute (e.g. account name or user email), create only if not found. Keep a DON scratchpad or persist to a run file.

4. **Error handling**: fail loudly on non-2xx. Log each created DON id to a per-run file. If the script crashes, re-run it — idempotency ensures no duplicates.

5. **Verify**: after the load, run `*.list` for each object type to confirm counts and spot-check records.

**Example script structure** (pseudocode):

```bash
#!/usr/bin/env bash
set -a; source .env; set +a
export DEVREV_TOKEN="$DEVREV_PAT"
RUN_LOG="run-$(date +%s).log"

while IFS=, read -r name email; do
  # Check if account exists
  ACCT_ID=$(curl -s -X POST 'https://api.devrev.ai/accounts.list' \
    -H "Authorization: Bearer $DEVREV_TOKEN" \
    -d "{\"filters\": {\"name\": [\"$name\"]}}" | jq -r '.accounts[0].id // empty')
  
  if [ -z "$ACCT_ID" ]; then
    ACCT_ID=$(curl -s -X POST 'https://api.devrev.ai/accounts.create' \
      -H "Authorization: Bearer $DEVREV_TOKEN" \
      -d "{\"name\": \"$name\", \"owned_by\": [\"<OWNER_ID>\"]}" | jq -r '.account.id')
    echo "CREATED account $name -> $ACCT_ID" >> "$RUN_LOG"
  else
    echo "SKIPPED account $name (exists: $ACCT_ID)" >> "$RUN_LOG"
  fi
done < accounts.csv
```

**Keep a per-run log of created DON ids**. Re-runs must converge (no duplicates).

### Ordered customer data creation

**Reference**: `references/Customers_Users_and_Orgs_API.md` §8 "Object relationships (build order)".

When creating customer identity objects, follow this top-down order (each tier saves DON ids for the next):

1. `accounts.create` — save `ACCOUNT_ID`
2. `rev-orgs.create` with `account: <ACCOUNT_ID>` — save `REV_ORG_ID`
3. `rev-users.create` with `rev_org: <REV_ORG_ID>` — save `REV_USER_ID`

**Verify**: `accounts.list`, `rev-orgs.list`, `rev-users.list` to confirm the hierarchy.

## Reference index

| File | When to read it |
| --- | --- |
| `references/Platform_and_Admin_API.md` | Artifact upload/download (§1); webhooks, jobs, schedules, vistas, observability, web-crawler, snap-widgets, commands, code-changes, auth-tokens (§2–12); common pitfalls (§14) |
| `references/DevRev_Building_Org_Using_API_v1.md` | Entire file — end-to-end org build playbook (§4 setup at a glance, Phase 0–5), key concepts (§3), worked example (§end-to-end), troubleshooting (§troubleshooting), best practices (§best practices) |
| `references/Customers_Users_and_Orgs_API.md` | Accounts, rev-orgs, rev-users, dev-users, groups — payloads and the §8 build order (account → rev_org → rev_user) used by customer data loads |

## DON id scratchpad

Keep track of returned DON ids for dependent calls:

```
PRODUCT_ID=       CAP_ID=           FEAT_ID=          RUN_ID=
ACCOUNT_ID=       REV_ORG_ID=       REV_USER_ID=      DEVU_OWNER_ID=
WORK_ID=          ARTIFACT_ID=      CUSTOM_OBJECT_ID= CUSTOM_LINK_TYPE_ID=
PART_ID=          TICKET_ID=        STAGE_DIAGRAM_ID=
```

## Safety

Confirm before these destructive/irreversible operations:
- Any `*.delete` on accounts, parts, work items, or custom objects. **`works.delete` confirmed live 2026-07-19**: it genuinely works (`HTTP 200 {}`, follow-up `.get` returns `HTTP 404`) — it is not a no-op or a stub. Treat it as a real destructive operation requiring confirmation, same as any other working `.delete`.
- Any `*.merge` (merges are irreversible)
- Deprecations (e.g. custom link types, stage diagrams)
- `objects.bulk-upgrade` — **confirmed live 2026-07-18**: exists at `/internal/objects.bulk-upgrade` (not public-root), affects ALL records of the given `type` org-wide via an async job. Confirm before running; prefer re-saving via `*.update` for targeted upgrades.
- `web-crawler-jobs.control` with stop/pause (§8, Platform_and_Admin_API.md)

After bulk data loads:
- Keep a per-run log of created DON ids (persist to a file timestamped with the run).
- Verify counts: run `*.list` for each object type and compare to the source data row count.
- Spot-check a few records: `*.get` on random DON ids to confirm fields are correct.
- If the script fails mid-run, re-run it — idempotency (via `unique_key` for custom objects, or `external_ref` + catching HTTP 409 for stock work items — **confirmed live 2026-07-18**, see Field notes) ensures no duplicates.

## Common pitfalls

From the references:

- **Artifact upload**: you can't POST bytes to `artifacts.create` — always `artifacts.prepare` first, upload to the returned URL, then reference the artifact id on the parent object (`references/Platform_and_Admin_API.md` §14).
- **Wrong order**: customization must precede data because records need schemas/stages. Data precedes analytics because dashboards need records. Follow Phase 0 → 1 → 2 → 3 → 4 → 5 (`references/DevRev_Building_Org_Using_API_v1.md` §4, §best practices).
- **Display IDs in links**: always pass the full DON id (`don:core:...:ticket/456`), never a display ID like `TKT-456`, in `parent_part`, `applies_to_part`, and link calls (`references/DevRev_Building_Org_Using_API_v1.md` §troubleshooting, §best practices).
- **Orphaned parts mid-move**: use `links.replace` to re-parent a part atomically (only for part-to-part default link types), not delete-then-create (`references/DevRev_Building_Org_Using_API_v1.md` Phase 3 note, §troubleshooting, §best practices).
- **Wrong namespace prefix**: `tnt__` for tenant fields, `ctype__` for subtype fields — a mismatched prefix silently fails to match with no error (`references/DevRev_Building_Org_Using_API_v1.md` §troubleshooting, §best practices).
- **Custom objects inaccessible**: they start with zero access by default (even for admins) — grant object- and field-level roles in Settings (`references/DevRev_Building_Org_Using_API_v1.md` Phase 1 §1.5, §troubleshooting, §best practices).
- **Duplicate records**: pass a stable `unique_key` on `custom-objects.create` for idempotency; for stock objects, check-before-create with `*.list` filter.
- **No bulk-create endpoint**: there is no public bulk-create endpoint — bulk loads = deterministic scripted loops over `*.create`, idempotent via `unique_key` or check-before-create, safe to re-run, fail loudly on non-2xx (documented honestly here).

## Field notes (live-learned; see docs/LEARNINGS.md)

Dated facts discovered while operating this domain — errors hit, restrictions found, behaviors that
differ from the references. Add entries via the `capture-learnings` protocol
(`.claude/skills/capture-learnings/SKILL.md`): one dated bullet per fact, with evidence. If a fact
*corrects* a reference doc, fix the doc in place too — this section is for knowledge that has no
better home or needs domain-level visibility.

- **2026-07-18 · Artifact upload path works end-to-end.** `POST /artifacts.prepare` (body: `{"file_name","file_type"}`) returns `{id, url, form_data[]}` with a pre-signed S3 URL. Then `POST` (multipart form) all the `form_data[]` fields plus `file=@<path>` to `url`. Success is **HTTP 204** (empty body). Verify immediately with `GET /artifacts.get?id=<don>` — the file name + size land within seconds.
- **2026-07-18 · No public artifact delete endpoint.** Verified live: `artifacts.delete`, `artifact-versions.delete`, `artifact-versions.delete-one` all return HTTP 404 route-not-found. Artifacts persist by design (content-hash addressable). Any test upload lives forever unless purged via infra — plan accordingly.
- **2026-07-18 · Attaching an artifact to a work item at create time works via the `artifacts` array on `works.create`.** `{"type":"ticket", ..., "artifacts":["<ARTIFACT_DON>"]}` → HTTP 201, and the response's `work.artifacts[]` contains the full artifact object (`display_id`, `file.name`, `file.size`, `file.type`). Verified with `works.get` afterwards — the artifact is retained.
- **2026-07-18 · An artifact can be attached to exactly ONE parent, ever.** Re-attaching the same artifact id to a second object (tried: a `timeline_comment` after it was already on a `ticket`) returns **HTTP 400** `{"type":"artifact_already_attached_to_a_parent","existing_parent":"<don>","is_same":false}`. This is undocumented in `references/Platform_and_Admin_API.md` §1 — that section implies an artifact id can just be "referenced on the parent object" with no exclusivity caveat. If you need the same file on two objects, `artifacts.prepare` + upload it twice (two artifact ids).
- **2026-07-18 · `timeline-entries.create` (comment) also accepts an `artifacts` array and works end-to-end.** `POST /timeline-entries.create` with `{"type":"timeline_comment","object":"<WORK_DON>","body":"...","artifacts":["<ARTIFACT_DON>"]}` → HTTP 201, returns `{"timeline_entry": {...}}` (note the wrapper key is `timeline_entry`, singular). This satisfies the "attach to a timeline entry" path distinct from attaching directly on `works.create`. Not previously exercised in Phase 2/2b.
- **2026-07-18 · `works.create` has a real idempotency key: `external_ref`.** Re-running `works.create` with an identical `external_ref` on the same work type returns **HTTP 409** `{"message":"Conflict","type":"conflict"}` — it does NOT silently create a duplicate, and does NOT silently no-op; the caller must catch the 409 and treat it as "already exists." This is a materially better idempotency mechanism than the SKILL.md's documented "check-before-create via `*.list` filter" fallback for stock objects — `external_ref` gives you a real uniqueness constraint, closer to `custom-objects.create`'s `unique_key`. Recommended pattern: set a stable `external_ref` on every `works.create`, treat HTTP 409 as "already exists, look it up," and always look it up via `works.list` (see next note for the correct filter field name).
- **2026-07-18 · `works.list` filter field is `external_ref` (singular key, array value), NOT `external_refs`.** `{"external_refs":[...]}` → HTTP 400 `{"type":"invalid_field","field_name":"external_refs"}`. Correct payload: `{"external_ref":["e2e-orgbuild-test-1"]}` → HTTP 200 with the matching work in `works[]`. This is the check-before-create lookup call the SKILL.md's bulk pattern relies on — get the field name right or the whole idempotent-reprocessing pattern breaks silently (400, not a graceful empty list).
- **2026-07-18 · `parts.list`'s `parent_part` filter is an object, not a bare array.** `{"parent_part":["<CAP_DON>"]}` → HTTP 400 `{"type":"unexpected_json_type","actual":"array","expected":"object","field_name":"parent_part"}`. Correct shape: `{"parent_part":{"parts":["<CAP_DON>"], "level": <optional int>}}` → HTTP 200. `parts.create` itself is confirmed working exactly as documented (`type`, `name`, `parent_part` as an array of DONs, `owned_by`) — HTTP 201, and `parts.get` on the new part plus `links.list?object=<new_part_don>` both confirm an `is_part_of` link was auto-created from child to parent (link type `is_part_of`, not something you create yourself in Phase 2 — Phase 2's `parent_part` field does it for you).
- **2026-07-18 · No `trails.*` endpoint exists at all** (root and no `/internal/` variant tried return route-not-found for `trails.create`/`trails.list`). Confirms the SKILL.md's "there is no `trails.create` endpoint" claim — Trail is purely the rendered view of `parent_part` + links, exactly as documented.
- **2026-07-19 · `applies_to_part` is required on `works.create`, not just a common/best-practice field.** Omitting it returns `HTTP 400` — a diagnostic `missing_required_field field_name:"applies_to_part"` for `issue`, an opaque `bad_request` with no field name for `ticket`. Prior examples showed it in payloads but never flagged it as mandatory.
- **2026-07-19 · `works.delete` confirmed live and genuinely working — corrects an implicit assumption that work items are undeletable.** `POST works.delete {"id":"<don>"}` → `HTTP 200 {}`; follow-up `works.get` → `HTTP 404`. This is a real, working destructive operation (used to clean up 2 throwaway test tickets this session) — unlike artifacts (no delete endpoint at all, see above) or custom stages/states (permanent, per skill 2's findings). Treat it as destructive/confirm-first like any other working `.delete`, not as something to assume is blocked.
- **2026-07-18 · `objects.bulk-upgrade` EXISTS and works — CLOSES the open question from Phase 2.** It is an `/internal/` endpoint, not a public-root one: `POST /internal/objects.bulk-upgrade` with `{"type":"ticket"}` → HTTP 200 `{"id":"<job_don>", "id_v1":"<job_don_v1>"}`. The call at `POST /objects.bulk-upgrade` (no `/internal/` prefix) returns HTTP 404 route-not-found — that's almost certainly why every prior check (which likely hit the public root) reported it as "not in the public API catalog." It queues an async job: `GET /jobs.get?id=<job_don>` → `job_category: "bulk_upgrade"`, `state: "completed"`, `progress: 100`, `title: "Bulk Upgrade"`, with a `metadata_list` entry `{"key":"Count","value":"<N>"}` giving the number of records upgraded. Scope/permission requirements weren't isolated (the PAT used has broad admin scope), and only `type` was tested as a filter (`subtype` also accepts per the schema but wasn't exercised). Safety note: it affects ALL records of the given `type` org-wide — treat as we already do (confirm before running), but it is no longer "possibly-fictional," it is confirmed real and internal-only.
- **2026-07-20 · CORRECTED: `parts.list`'s `parent_part: {"parts": [<DON>]}` filter matches DESCENDANTS AT ANY DEPTH, not just direct children — the 2026-07-18 bullet above only documented the filter's shape (object vs. bare array), not this depth behavior.** Verified live building a 4-level Trail (product → capability → feature → feature): filtering `type:["feature"], parent_part:{"parts":[<grandparent_capability_don>]}` returned features nested two levels down, not just the direct-child features. `parts.get`/`parts.list` also never return a `parent_part` field on the part record itself (confirmed: the field is simply absent from the response) — the only authoritative way to read a part's true immediate parent is `links.list` with the part as `object`, filtering to `link_type:"is_part_of"` edges where the part is the `source` (the `target` is the immediate parent). **Practical impact**: a check-before-create idempotency script that does `parts.list` by `name` + `parent_part` filter can silently match the wrong node when a descendant subtree reuses a name (e.g. a submodule and one of its own child features sharing an identical name) — this produced real cascading duplicate parts across repeated runs before being caught by an independent `links.list`-based tree walk. Idempotency for parts must verify the exact parent via `links.list`, not the `parent_part` list filter.
- **2026-07-20 · `parts.delete` requires children to be deleted first — deleting a parent while an `is_part_of` child link still points to it returns HTTP 400 `bad_request` with no diagnostic field name.** Delete leaf parts before their parent when cleaning up a mis-built subtree; retrying the parent delete after its children are gone succeeds (`HTTP 200 {}`, confirmed via a follow-up `parts.get` → `HTTP 404`).
