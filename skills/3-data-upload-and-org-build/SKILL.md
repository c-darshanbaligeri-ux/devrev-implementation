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

**Important**: To move a part within the Trail later, use `links.replace` rather than delete-then-create, so you never leave a part orphaned without a parent. The replacement is **atomic only for part-to-part default (non-custom) link types**; for custom link types or non-part endpoints it runs as a non-atomic delete-then-create and the new link must keep the same type and share an endpoint (§3 note).

**Verify**: `parts.list` to confirm the hierarchy; `links.list` on a part to see its connections.

#### Phase 4 — Define custom links & connect objects

**Reference**: `references/DevRev_Building_Org_Using_API_v1.md` Phase 4.

When you need a relationship that the built-in link types don't cover (e.g. tying a custom object to a ticket), define a custom link type once, then create link instances from it. Custom link types can be created between work objects, identity objects (account, rev/dev user, rev org), part objects, and any custom object leaf type.

**ROUTE to `skills/1-object-schema-customization` Playbook 4** for the full custom link type creation flow.

#### Phase 5 — Add work & verify

Attach work items to the right part so they surface on the Trail. Set `applies_to_part` on any ticket or issue you create:

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
   - **Customer data ordering** (§Phase 5 note): `accounts.create` → `rev-orgs.create` → `rev-users.create`, top-down, saving each DON id.
   - **Parts ordering** (Phase 2): product → capability → feature, saving each DON id and passing `parent_part` to children.
   - **Work items** (Phase 5): after parts exist, create work items with `applies_to_part`.

3. **Idempotency**:
   - For **custom objects**: pass a stable `unique_key` on `custom-objects.create` (§1.2, Phase 1). Repeating the call with the same key won't create a duplicate.
   - For **stock objects**: no native `unique_key`. Check-before-create pattern: `*.list` filtered by a unique attribute (e.g. account name or user email), create only if not found. Keep a DON scratchpad or persist to a run file.

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

**Reference**: `references/DevRev_Building_Org_Using_API_v1.md` Phase 5 note (customer data ordering).

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
- Any `*.delete` on accounts, parts, work items, or custom objects
- Any `*.merge` (merges are irreversible)
- Deprecations (e.g. custom link types, stage diagrams)
- `objects.bulk-upgrade` (if confirmed available — see `skills/1-object-schema-customization` Safety note; prefer re-saving via `*.update`)
- `web-crawler-jobs.control` with stop/pause (§8, Platform_and_Admin_API.md)

After bulk data loads:
- Keep a per-run log of created DON ids (persist to a file timestamped with the run).
- Verify counts: run `*.list` for each object type and compare to the source data row count.
- Spot-check a few records: `*.get` on random DON ids to confirm fields are correct.
- If the script fails mid-run, re-run it — idempotency (via `unique_key` or check-before-create) ensures no duplicates.

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
