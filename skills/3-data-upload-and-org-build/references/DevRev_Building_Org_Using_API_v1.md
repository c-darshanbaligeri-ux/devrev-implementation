# Building a Customer Org Using the DevRev API
**Implementation Playbook**

*Object customization, parts creation, Trails, and custom links - end to end.*

| Field | Detail |
| --- | --- |
| Document title | Building a Customer Org Using the DevRev API |
| Purpose | Standardize how we build out a customer org via API |
| Audience | Implementation engineers, Solutions Engineers, Onboarding/AAI teams |
| Owner | Implementation / Solutions Engineering |
| Status | For team review |
| Version | 1.0 |
| Last updated | 16 July 2026 |
| Base URL | https://api.devrev.ai |
| Authentication | Bearer <TOKEN> (PAT or Service Account Token) |


---


# 1. Purpose & summary

This playbook is the standard, repeatable procedure our teams follow to build out a customer organization in DevRev through the API. It consolidates the four core building blocks - object customization, parts creation, Trails, and custom links - into one ordered workflow, so any engineer can execute a consistent, high-quality setup without prior context.

It is written to be self-contained: each phase states what it produces, provides copy-and-paste API calls, and flags what to carry forward to the next phase.

> **Note:** Scope: this guide focuses on modeling the org - its objects, product structure, and relationships. It assumes the customer account and users already exist. It does not provision a brand-new Dev org tenant, which is a one-time step done from the DevRev app or during subscription provisioning.

# 2. Who this is for & what you'll achieve

Intended readers:

- Implementation and onboarding engineers standing up a new customer org.
- Solutions Engineers configuring a demo or proof-of-concept environment.
- Anyone automating org setup who needs the correct API sequence and payloads.

By the end of this guide you will have:

- Customized DevRev objects with subtypes, custom fields, stages, and (optionally) custom object types.
- Created the customer's product hierarchy of parts.
- Built a connected Trail that visualizes that hierarchy and its supporting components.
- Defined custom links and connected objects across the org.
- Attached work to the right parts and verified the whole setup.

## Prerequisites

- A DevRev bearer token (Personal Access Token for manual work, or Service Account Token for automation).
- The customer account and users already created in the org.
- Appropriate write scopes for the object types you will create (see each phase).

# 3. Key concepts at a glance

A handful of terms recur throughout every phase below. Skim these once before you start - it will save you from backtracking.

| Term | What it means |
| --- | --- |
| DON id | DevRev's global object identifier, e.g. don:core:dvrv-us-1:devo/0:product/1. Always reference objects by DON, never by display ID like PROD-123, in parent_part and link calls. |
| Leaf type | The concrete object type - issue, ticket, product, capability, etc. - set in the leaf_type field. |
| Schema fragment | A reusable building block of custom fields. tenant_fragment applies org-wide; custom_type_fragment applies to a subtype; app_fragment is for automation-added fields. |
| Subtype | A named flavour of a leaf type (e.g. bug is a subtype of issue) that adds its own fields via the ctype__ prefix. |
| Tenant field | A custom field added to every record of a leaf type, prefixed tnt__. |
| Part | The backbone of the product model. Customer parts (product -> capability -> feature) form the visible hierarchy; builder parts (runnable, linkable) are the internal components that power them. |
| Trail | Not a separate object - it's the rendered graph view of your part hierarchy plus the links between parts. Open Product > Trails in the app to see it. |
| Custom link type | A relationship you define once (e.g. "ticket relates to campaign") and then create many link instances from. |


# 4. Setup at a glance (recommended order)

The order matters: shape the data model first, then the product structure, then the connections, then the work that hangs off them.

| # | Phase | Key endpoints | Produces |
| --- | --- | --- | --- |
| 0 | Auth & prerequisites | - | A valid bearer token |
| 1 | Object customization | schemas.custom.set, custom-objects.create | Subtypes, custom fields, custom objects |
| 2 | Parts | parts.create | product / capability / feature / runnable IDs |
| 3 | Trail | parts.create + parent_part, links.create | A connected part hierarchy (the Trail) |
| 4 | Custom links | link-types.custom.create, links.create | Custom relationships between objects |
| 5 | Work & verify | works.create, parts.list, links.list | Tickets/issues on parts; verification |


# Phase 0 - Prerequisites & authentication

Every request needs a bearer token in the Authorization header:

```bash
Authorization: Bearer <TOKEN>
Content-Type: application/json
Accept: application/json
```
- Use a Personal Access Token (PAT) for manual setup, or a Service Account Token for automation.
- Objects are referenced by their DON id (e.g. don:core:dvrv-us-1:devo/0:product/1). Save every id a call returns - later phases depend on them.
- Work top-down and keep a scratchpad of IDs: PRODUCT_ID, CAP_ID, FEAT_ID, RUN_ID, and any custom_link_type IDs.

# Phase 1 - Customize objects

Object customization tailors DevRev's built-in objects (issue, ticket, opportunity, account, contact, part) to the customer's workflow, or defines entirely new object types. The model is additive - you layer your definitions on top of stock fields; built-in fields are never modified.


## 1.1 Concepts

- Leaf type - the concrete object type, e.g. issue or ticket (the leaf_type field).
- Schema fragment - a building block of custom fields. Types: tenant_fragment (org-wide), custom_type_fragment (subtypes), app_fragment (automation fields).
- Subtype - a flavour of a leaf type (e.g. bug subtype of issue) with extra fields.
- Namespaces - subtype fields are prefixed ctype__; tenant fields are prefixed tnt__.

## 1.2 Add a subtype with custom fields

Define a 'bug' subtype of issue with custom fields:

```bash
curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "type": "custom_type_fragment",
  "leaf_type": "issue",
  "subtype": "bug",
  "subtype_display_name": "Bug",
  "fields": [
    { "name": "impacted_environments", "field_type": "array",
      "base_type": "enum",
      "allowed_values": [ "Dev", "QA", "Prod" ],
      "is_filterable": true,
      "ui": { "display_name": "Impacted Environments" } },
    { "name": "rca", "field_type": "rich_text",
      "ui": { "display_name": "RCA" } }
  ]
}'
```
Create a bug-flavoured issue using the subtype and ctype__ fields:

```bash
curl -X POST 'https://api.devrev.ai/works.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "type": "issue",
  "title": "API failure in Prod",
  "applies_to_part": "<PART_ID>",
  "owned_by": [ "<DEVU_OWNER_ID>" ],
  "custom_schema_spec": { "subtype": "bug" },
  "custom_fields": { "ctype__impacted_environments": [ "Prod" ] }
}'
```

## 1.3 Tenant custom fields & field types

A tenant field applies to every record of a type. Add release notes to all issues:

```bash
curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "type": "tenant_fragment",
  "leaf_type": "issue",
  "fields": [ { "name": "release_notes", "field_type": "rich_text",
    "ui": { "display_name": "Release Notes" } } ]
}'
```
Supported field types: int, double, bool, tokens, text, rich_text, enum, uenum (advanced enum with stable numeric IDs), timestamp, date, and id - plus array/list variants of each. Fragments are immutable and versioned automatically; to remove a field, list it in deleted_fields.


## 1.4 Custom stages & dependent fields

Model the object lifecycle: create a stage with stages.custom.create, wire allowed transitions with stage-diagrams.create, then reference the diagram from the subtype fragment (stage_diagram_id). Enforce rules with dependent-field conditions, e.g. require RCA when a bug reaches the completed stage:

```bash
"conditions": [{
  "expression": "stage == 'don:core:dvrv-us-1:devo/0:stage/5'",
  "effects": [{ "fields": [ "custom_fields.rca" ], "require": true }]
}]
```

## 1.5 Custom objects (new object types)

If the customer needs a net-new object type, define its schema with is_custom_leaf_type: true and an id_prefix, then create records with custom-objects.create.

```bash
# 1) Define the schema
curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "type": "tenant_fragment", "leaf_type": "campaign",
  "leaf_type_display_name": "Campaign", "is_custom_leaf_type": true,
  "id_prefix": "CAMP",
  "fields": [ { "name": "budget", "field_type": "int" } ]
}'

# 2) Create a record
curl -X POST 'https://api.devrev.ai/custom-objects.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "leaf_type": "campaign",
  "custom_schema_spec": { "tenant_fragment": true },
  "unique_key": "CAMP-1",
  "custom_fields": { "tnt__budget": 10000 } }'
```
> **Note:** Custom objects are not accessible to anyone by default (including admins). Grant object- and field-level access in Settings > Object customization and Settings > User Management > Roles.

# Phase 2 - Create parts (the product hierarchy)

Parts are the backbone of the customer's product model - almost every work item links to a part. Customer parts (product -> capability -> feature) form the hierarchy; builder parts (runnable, linkable) are the internal components that power them.

Create the product (the root; no parent):

```bash
curl -X POST 'https://api.devrev.ai/parts.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "type": "product", "name": "Acme Platform",
  "owned_by": [ "<DEVU_OWNER_ID>" ] }'
```
Save as PRODUCT_ID. Then add a capability under it, passing the product DON as parent_part:

```bash
curl -X POST 'https://api.devrev.ai/parts.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "type": "capability", "name": "Authentication",
  "parent_part": [ "<PRODUCT_ID>" ], "owned_by": [ "<DEVU_OWNER_ID>" ] }'
```
Add features under the capability (parent_part = CAP_ID), and builder parts (type runnable / linkable) which have no parent_part - they join the model via links in the next phase.

| Part type | Parent | Write scope |
| --- | --- | --- |
| product | none (root) | product:write OR product:all |
| capability | product | capability:write OR capability:all |
| feature | capability (or feature) | feature:write OR feature:all |
| runnable / linkable | none; linked in Phase 3 | (builder part scope) |


# Phase 3 - Build the Trail

A Trail is not a separate object and there is no trails.create endpoint. The Trail is the rendered view of the part hierarchy you just built plus the links between parts. So building the Trail means two things: (1) the parent_part relationships from Phase 2, and (2) connecting builder parts to the customer parts they power.


### What the resulting Trail looks like

```
Acme Platform (product)
  └── Authentication (capability)
        └── SSO Login (feature)
              ▲
              │ serves (link)
        auth-service (runnable)
```
The solid line represents a parent_part relationship built in Phase 2. The "serves" link is a builder-to-customer-part connection created below. Together they render as one connected Trail.

Link a runnable to the feature it serves with links.create using the built-in link type serves:

```bash
curl -X POST 'https://api.devrev.ai/links.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "link_type": "serves",
  "source": "<RUNNABLE_ID>",
  "target": "<FEATURE_ID>" }'
```
Common built-in link types between parts and other objects: serves, is_part_of, is_dependent_on, is_related_to. Once parts are created and linked, open Product > Trails in the app to see the connected graph rendered visually.

> **Note:** To move a part within the Trail later, use links.replace rather than delete-then-create, so you never leave a part orphaned without a parent. The replacement is atomic for part-to-part default (non-custom) link types; for custom link types or non-part endpoints it runs as a non-atomic delete-then-create and the new link must keep the same type and share an endpoint.

# Phase 4 - Define custom links & connect objects

When you need a relationship that the built-in link types don't cover - for example, tying a custom object to a ticket - define a custom link type once, then instantiate links from it. Custom link types can be created between work objects, identity objects (account, rev/dev user, rev org), part objects, and any custom object leaf type.

Step 1 - define the custom link type:

```bash
curl -X POST 'https://api.devrev.ai/link-types.custom.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "name": "Link between ticket and campaign",
  "source_types": [ { "leaf_type": "ticket" } ],
  "target_types": [ { "leaf_type": "campaign", "is_custom_leaf_type": true } ],
  "forward_name": "relates to campaign",
  "backward_name": "referenced by ticket"
}'
```
Save the returned id as CUSTOM_LINK_TYPE_ID. Step 2 - create a link instance with link_type custom_link:

```bash
curl -X POST 'https://api.devrev.ai/links.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "link_type": "custom_link",
  "custom_link_type": "<CUSTOM_LINK_TYPE_ID>",
  "source": "<TICKET_ID>",
  "target": "<CAMPAIGN_OBJECT_ID>"
}'
```
- Links require link:write or link:all, plus read access to both linked objects.
- The API verifies both objects exist, so you never create a dangling link.
- You can also restrict a custom link type to specific subtypes by adding subtype inside a source/target descriptor.
> **Note:** Custom link types cannot be deleted, only deprecated - this preserves referential integrity. Name them carefully.

# Phase 5 - Add work & verify

Attach work items to the right part so they surface on the Trail. Set applies_to_part on any ticket or issue you create:

```bash
curl -X POST 'https://api.devrev.ai/works.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "type": "ticket", "title": "Login fails for Acme",
  "applies_to_part": "<FEATURE_ID>",
  "owned_by": [ "<DEVU_OWNER_ID>" ] }'
```
Verify the setup:

- parts.list - confirm the product hierarchy exists. To filter by parent, `parent_part` is an OBJECT, not a bare array: `{"parent_part": {"parts": ["<PARENT_DON>"], "level": <optional int>}}`. Passing a plain array (`{"parent_part": ["<PARENT_DON>"]}`) returns HTTP 400 `unexpected_json_type` (verified live 2026-07-18).
- links.list on a part - confirm builder parts, custom links, and work are attached. Confirmed live: creating a part with `parent_part` set auto-creates an `is_part_of` link from child to parent, visible via `links.list?object=<child_don>` — you don't need to call `links.create` yourself for the parent_part relationship, only for cross-hierarchy connections like `serves`.
- schemas.custom.list / custom-objects.list - confirm your fragments and custom objects.

# End-to-end worked example

1. Authenticate with a PAT/Service Account token (Phase 0).
1. schemas.custom.set - add a 'bug' subtype and a tenant release_notes field to issue.
1. (Optional) schemas.custom.set + custom-objects.create - define a 'campaign' custom object.
1. parts.create product 'Acme Platform' -> PRODUCT_ID.
1. parts.create capability 'Authentication' (parent_part = PRODUCT_ID) -> CAP_ID.
1. parts.create feature 'SSO Login' (parent_part = CAP_ID) -> FEAT_ID.
1. parts.create runnable 'auth-service' -> RUN_ID; links.create serves RUN_ID -> FEAT_ID (builds the Trail).
1. link-types.custom.create ticket<->campaign; links.create a custom_link between a ticket and the campaign.
1. works.create a ticket with applies_to_part = FEAT_ID.
1. Verify with parts.list and links.list; open Product > Trails to see the graph.

# Quick API reference

| Area | Endpoint | Purpose |
| --- | --- | --- |
| Customization | schemas.custom.set | Create/update fragments, subtypes, tenant fields, overrides |
| Customization | schemas.custom.list | List custom schema fragments |
| Customization | custom-objects.create / .list | Create / list custom object records |
| Customization | stages.custom.create | Create a custom stage |
| Customization | stage-diagrams.create | Define allowed stage transitions |
| Customization | objects.bulk-upgrade | Upgrade records to the latest fragment version. **Confirmed live 2026-07-18**: exists ONLY at `/internal/objects.bulk-upgrade` (public root path 404s) — `{"type":"<obj_type>"}` returns HTTP 200 `{"id":"<job_don>"}`; poll `jobs.get` for `job_category:"bulk_upgrade"` / `state:"completed"`. Affects ALL records of that type org-wide — confirm before running; for a single record, re-save via `*.update` instead. |
| Parts | parts.create / .list / .update | Create and manage the product hierarchy |
| Trails / Links | links.create | Connect parts to each other, work, and customers |
| Trails / Links | links.list | List an object's links |
| Trails / Links | links.replace | Re-parent a part atomically |
| Custom links | link-types.custom.create / .update | Define custom relationship types |
| Work | works.create | Create tickets/issues attached to parts |


# Troubleshooting & common errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Custom field silently not set / ignored | Wrong namespace prefix on the field name | Use ctype__ for subtype fields and tnt__ for tenant fields - a mismatched prefix fails to match with no error. |
| 403 / permission denied on parts.create | Missing write scope for that part type | Confirm the token has the specific scope for the type, e.g. capability:write, not just a generic write scope. |
| Custom object empty / inaccessible even to admins | No access granted yet | Custom objects start with zero access by default. Grant object- and field-level roles in Settings > Object customization and Settings > User Management > Roles. |
| Part temporarily orphaned mid-move | Used delete-then-create to re-parent | Use links.replace instead - it re-parents atomically so the part is never briefly without a parent. |
| Old field values still showing after a schema change | Existing records still reference the old fragment | Re-save the record via its `*.update` with the current custom_schema_spec, or run `objects.bulk-upgrade` (confirmed live at `/internal/objects.bulk-upgrade`, not public root — see Phase-5-adjacent quick reference row above) for all records of a type at once. |
| Link creation fails with "object not found" | Referencing a display ID instead of a DON | Always pass the full DON id (don:core:...), not a short display ID like PROD-12345, in parent_part and link calls. |
| Can't delete a custom link type | By design | Custom link types can only be deprecated, not deleted, to preserve referential integrity. Create a new one if you need a rename. |


# Best practices & pitfalls

- Follow the phase order: customization -> parts -> Trail -> custom links -> work. Each phase yields IDs the next one needs.
- Always reference objects by DON, never by display ID, in parent_part and link calls.
- Respect namespaces: tnt__ for tenant fields, ctype__ for subtype fields - a wrong prefix silently fails to match.
- Customer parts join the Trail via parent_part; builder parts join via links (serves / is_part_of).
- Re-parent parts with links.replace, not delete-then-create, to avoid orphans.
- Custom link types can only be deprecated, never deleted - name them thoughtfully.
- Custom objects start with no access; grant object- and field-level roles explicitly.
- When evolving a schema fragment, send the full field list and list removals in deleted_fields; then re-save affected records (via their `*.update`) so they pick up the latest fragment version.
- Match the required scope to each object type or the call is rejected.

# Support & feedback

Questions, corrections, or improvements to this playbook should go to the Implementation / Solutions Engineering owner listed in the document control table. For authoritative, always-current field details, cross-check against the DevRev developer API reference before relying on any payload in production.

Prepared from DevRev's internal and public developer documentation covering Object customization, Parts & Trails, and Links.
