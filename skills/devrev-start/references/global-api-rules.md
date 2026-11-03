# Rules that apply to every DevRev API call

Moved here from the repo's `CLAUDE.md`. They are cross-cutting; endpoint-specific facts live in the skills and the finder's briefs.

- **Base URL:** `https://api.devrev.ai`.
- **Headers on every request:** `Authorization: Bearer $DEVREV_PAT`, `Content-Type: application/json`, `Accept: application/json`. Use **double quotes** around the header so the shell expands the variable.
- **Token:** `DEVREV_PAT` is the canonical name (from the environment, else `.env`). `DEVREV_API_KEY` is a synonym, and older scripts may expect `DEVREV_TOKEN`; alias it only if a script needs it: `export DEVREV_TOKEN="$DEVREV_PAT" DEVREV_API_KEY="$DEVREV_PAT"`.
- **Method:** prefer POST with a JSON body for anything non-trivial. GET with query parameters works for most reads.
- **Object references:** always full DON ids (`don:core:dvrv-us-1:devo/<ORG_ID>:ticket/456`), never display ids such as `TKT-456`.
- **Scopes:** `devrev-find --endpoint <name>` shows them. A range such as `x:read,x:write,x:all` means any one grants access; destructive operations (delete, merge) need `x:all`. For work items the scope tracks the type: `works.create` of a ticket needs `ticket:write`, of an issue `issue:write`. Timeline entries have no scope of their own; they inherit the parent object's read/write scope.
- **Custom field prefixes:** `tnt__` (tenant fragment) and `ctype__` (subtype fragment) on records. A wrong prefix **fails silently**: the server accepts the request and ignores the field. Inside a schema *definition* the field names are bare (no prefix).
- **`custom_schema_spec`:** send it with any payload that contains custom fields.
- **Fragment versioning:** schema fragments are versioned. After a schema change (new field, overrides, subtype change), re-save affected records via their `*.update`, or use `objects.bulk-upgrade` to upgrade every record of a type. `objects.bulk-upgrade` exists only at `/internal/objects.bulk-upgrade` (the public path 404s); `{"type":"<obj_type>"}` returns HTTP 200 `{"id":"<job_don>"}`, and you poll `jobs.get` for `job_category:"bulk_upgrade"` / `state:"completed"`. It is confirmed live (2026-07-18) but internal-only, like the `ai-agents.*` endpoints.
- **Custom objects** start with zero access. Grant roles explicitly after creating one.
- **Custom link types** can only be deprecated, never deleted: `link-types.custom.update` with `deprecated: true` (write scope `custom_link_type:write`).
- **`links.replace`** is atomic only for part-to-part default (non-custom) link types. For custom types or other objects it is a non-atomic delete + create, and the type must stay the same across the replacement.
- **Pagination:** follow whichever of `next_cursor` / `cursor` the response returns; stop only when neither is present (`skills/10-api-conventions`).

## Execution checklist

1. Find the endpoint: `devrev-find "<goal>"`, then `devrev-find --endpoint <name>`.
2. Read the domain skill or reference it points at for the exact payload.
3. Substitute real DON ids from earlier calls or from the user.
4. Run the call with the headers above.
5. Verify with the matching `.get` / `.list` immediately.
6. Keep a scratchpad of returned ids (schema id for records, part id for work items, artifact id for attachments).
7. `POST /ping` confirms a token works (no scope needed).
