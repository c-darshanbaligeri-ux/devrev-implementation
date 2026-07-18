# DevRev Data Model & Object Customization

Use this reference when the solution needs to decide **how to model the customer's domain** — which objects to reuse, when to create custom objects, what custom fields and stages to add, and how objects relate.

## Table of contents
1. The overarching model (Atom → leaf types → three pillars)
2. Core built-in object types
3. Custom object types (custom leaf types)
4. Custom fields & schema fragments
5. Custom stages, states & stage diagrams
6. Parts hierarchy and how work maps to parts
7. Relationships and links
8. Quick reference: leaf-type strings

---

## 1. The overarching model

Every DevRev object descends from an abstract base type **Atom**. Concrete, instantiable types are **leaf types** (`leaf_type` in the API). `Work` and `Atom` are abstract parents and are NOT leaf types; `Issue`, `Ticket`, etc. are leaf types.

DevRev organizes leaf types into a **Knowledge Graph** across three pillars:
- **Identity (Who):** Dev users (internal team), Rev users (external customers/contacts), Accounts (customer companies), Rev orgs (workspaces).
- **Parts (What):** the product hierarchy — Product → Capability → Feature → Enhancement, plus builder parts (runnable, linkable, microservice, component). Every work item links to a part.
- **Work (What's being done):** Tickets, Issues, Incidents, Conversations, Opportunities, Tasks, Enhancements, Meetings.

Relationships between objects are **first-class entities** in the graph (parent/child, depends, duplicates, related), not inferred at query time. The ontology ships pre-built for the customer↔product↔engineering domain; this is what "Trails" renders and what "Computer Memory" is built on.

**Design implication:** always try to map the customer's nouns onto this graph before inventing new objects. A "support request" is a ticket; a "customer company" is an account; a "product area" is a part. Only reach for custom objects when the noun has no natural home (see §3).

---

## 2. Core built-in object types

### Identity pillar
| Object | leaf_type | Purpose |
|---|---|---|
| Account | `account` | A business entity that is a customer of the org. One account can span multiple workspaces (rev orgs). |
| Workspace / Rev org | `rev_org` | A specific customer-organization instance using the product. Holds org-level SLA entitlements. |
| Contact / Rev user | `rev_user` (`revu`) | An individual external prospect/customer/stakeholder. |
| Dev user | `dev_user` (`devu`) | An internal team member (owner, agent, builder). |
| Sys user | `sys_user` (`sysu`) | System/service identity (bots, integration app users). |
| Group | `group` | A collection of users; used for routing, access control, ownership. |
| Service account | `svcacc` | Non-human service identity. |

### Work pillar
| Object | leaf_type | Purpose |
|---|---|---|
| Ticket | `ticket` | A customer's request for assistance/support. The primary way an external user tracks their request. |
| Issue | `issue` | Internal engineering/backend work (dev, test, design, PM). **Always associated with a part.** |
| Incident | `incident` | Tracks disruptions in the use of a product or service. |
| Conversation | `conversation` | A synchronous/near-synchronous discussion (PLuG, WhatsApp, Slack, email) that may be escalated to a ticket. |
| Opportunity | `opportunity` | A potential source of revenue; customizable pipeline stages; links to tickets/conversations. |
| Task | `task` | Lightweight work item (a to-do); used to break larger work into pieces. |
| Enhancement | `enhancement` | Parent of multiple issues leading to a desired change to a part. Modeled as a **part** in the hierarchy but behaves as a work-planning object. |
| Meeting | `meeting` | An engagement representing a meeting between people. Supports custom fields/subtypes via API. |

### Content & other
| Object | leaf_type | Purpose |
|---|---|---|
| Article | `article` | Knowledge-base article / curated documentation. Has `applies_to_part_ids`, `status`, `scope` (internal/external), `shared_with`. |
| Question & Answer | `question_answer` | Community/curated Q&A knowledge; created from resolved conversations to improve deflection. |
| Tag | `tag` | Categorization/labeling applied across objects for filtering/reporting. |
| Custom object | `custom_object` + specific `leaf_type` | User-defined object types — see §3. |

---

## 3. Custom object types (custom leaf types)

**Definition:** Custom objects extend the data model **beyond** the standard Build/Support use-cases. Instead of customizing an existing object, you create a brand-new object type.

**Key concepts:**
1. **Leaf type** — the base type, e.g. `campaign`.
2. **Subtype** — a categorization of a leaf type, e.g. `promotion` / `advertising` under `campaign`.
3. **Schema fragment** — defines the schema for the object.
4. **Custom fields** — user-defined fields storing the object's data.
5. **ID prefix** (`id_prefix`) — a unique `[A-Z]{2,10}` prefix. With `id_prefix: "CAMP"`, the display ID becomes `C-CAMP-1`. The leading `C-` disambiguates custom objects from stock IDs like `ISS-001`.

DON format: `don:core:<region>:devo/<org_id>:custom_object/<leaf_type>/<id>`.

### When to use a custom object vs. extending a built-in type
- **Subtypes customize what already exists.** Use a subtype (or tenant custom fields) when your thing is fundamentally a ticket/issue/account with extra attributes — a "Bug" flavor of issue, a "Customer Escalation" ticket.
- **Custom objects create something entirely new.** Use a custom object when the thing has no natural home in Build or Support — campaigns, vendors, contracts, assets, physical inventory, loan applications, insurance claims, or imported external records with no good stock mapping.
- **Prefer customization over replication.** When integrating external channels/data, map to the best-fitting DevRev object first; only use a custom object when search/analytics is the primary use case and no stock mapping fits.

**Caveat:** custom fields on custom objects can't carry platform business logic reliably (logic keyed on a custom field breaks if an admin deletes the field). All integrations are available out of the box once a new `leaf_type` is defined.

### Creating a custom object (API lifecycle)
Create the schema first via `schemas.custom.set` with `type: "tenant_fragment"` and `is_custom_leaf_type: true`, then create instances via `custom-objects.create`. `unique_key` is an optional idempotency key. By default a custom object is accessible to no one (intentional) — admins grant access explicitly.

→ Exact payloads, full CRUD table, `.list` filter syntax, referencing via `id_type: custom_object.<leaf_type>`, access-control UI paths, plus the tags-on-custom-object and part-field-on-custom-object patterns (not covered here): `../../1-object-schema-customization/references/Custom_Objects_and_Links_API.md`.

---

## 4. Custom fields & schema fragments

DevRev customizes objects using **schema fragments** — building blocks that each contribute part of an object's overall schema. Fragments are immutable; updating creates a new version and chains it.

**Fragment types:**
| Type | API `type` | Scope / cardinality | Field prefix | Purpose |
|---|---|---|---|---|
| Stock schema fragment | (DevRev-provided) | Global, ships with every leaf type | (none) | Built-in stock fields (`title`, `status`, `severity`, `owned_by`, `target_close_date`, `applies_to_part`). |
| Tenant fragment | `tenant_fragment` | Org-wide; at most one per leaf type; all records | `tnt__<name>` | Org-defined custom fields common to all records of the type. |
| Custom type fragment | `custom_type_fragment` | Per subtype; at most one per subtype | `ctype__<name>` | Defines subtypes ("flavors") and subtype-specific fields. |
| App fragment | `app_fragment` | Per app/snap-in; any number | `app_<appname>__<name>` | Fields specific to an integration/snap-in. |

A single object carries: at most one tenant fragment + at most one custom_type fragment + any number of app fragments.

### Supported custom field types
| field_type | Example | Notes |
|---|---|---|
| `int` | `42` | Whole numbers. |
| `double` | `3.14` | Floating-point. |
| `bool` | `true`/`false` | Boolean toggle. |
| `text` | `"Hello"` | Single-line plain text; searched word-wise. |
| `tokens` | `"apple"` | String searched as a single keyword unit. |
| `rich_text` | `"**Hello**"` | Formatted text (markdown). |
| `enum` | `"apple"` | String from a fixed set; requires `allowed_values`; rendered as dropdown. |
| `date` | `"2020-10-20"` | Date only (YYYY-MM-DD). |
| `timestamp` | `"2020-10-20T00:00:00Z"` | Date + time + timezone (RFC3339). |
| `id` | a DON | Reference to another object; requires an `id_type` constraint listing allowed targets (e.g. `devu`, `revu`, `product`, `custom_object.<leaf_type>`). |
| `composite` | structured object | Structured field; nested up to ~5 levels. |
| `struct` | embedded JSON | Arbitrary JSON; limited mapping/UI support — avoid if UI rendering or Airdrop mapping needed. |

**Array variants:** all types (except `json_schema`) available as arrays — either `[]enum`, `[]text`, `[]id`, or `field_type: "array"` + `base_type: <type>`.

**Note:** `uenum` (Unified Enum, numeric-id enum with stable relabeling) is used for stock-field overrides but is NOT yet supported for user-defined custom fields. Don't model customer-facing dropdowns as `uenum` custom fields — use `enum`.

### Field descriptor structure
Each field has: `name` (immutable after creation), `field_type` (+ `base_type`/`allowed_values`/`id_type`), annotations (`is_required`, `is_filterable`, `is_immutable`), `default_value`, and UI hints (`display_name`, `description`, `placeholder`, `is_hidden`, `is_read_only`, `is_sortable`, `is_groupable`, `order`, `group_name`, `unit`).

`is_filterable` does not retroactively index existing objects — a resync/update is required.

→ Full field-descriptor payload shapes and per-field-type constraints: `../../1-object-schema-customization/references/Stock_Object_Modification_and_Schemas_API.md`.

### Dependent / conditional fields
A `conditions` array on a fragment defines conditional behavior. Each condition has an `expression` (operators `==`, `!=`, `&&`, `||`) and `effects`:
- `require` — make a field mandatory when the condition holds.
- `show` — conditionally show a field.
- `allowed_values` — restrict enum options; for stages, allowed transitions become the intersection of the stage diagram and the condition. This is how "make stage X available only when field = C" is achieved.

Expressions reference stages by **stage ID**, never display name.

### UI access
Object customization UI is at **Settings > Object customization** (requires workspace admin). UI-supported types: Issues, Tickets, Opportunity, Account, Contact, Parts. Other types (Incidents, Meetings) support custom fields/subtypes via API.

---

## 5. Custom stages, states & stage diagrams

### States (coarse-grained)
A **state** is a high-level category and the basis for metrics, SLAs, and reporting. Three built-in states ship in every org: `open`, `in_progress`, `closed`. Custom states via `states.custom.create/.update/.list/.get`. Every stage belongs to exactly one state.

### Stages (fine-grained)
A **stage** is a named lifecycle step with `name`, `ordinal` (order at org level), and `state`. Within an org no two stages share a `name` or `ordinal`. Stages are org-scoped, not bound to one object type — the same stage (e.g. `in_development`) can be referenced by both `issue` and `ticket`. Create via `stages.custom.create`.

Example mapping:
| State | Possible stages |
|---|---|
| Open | Triage, Backlog |
| In Progress | In Development, In Testing |
| Closed | Completed, Won't Fix |

### Stage diagrams (finite-state machine)
A **stage diagram** defines the stages and allowed transitions for a type.
- A vanilla object (no subtype) follows the **default** diagram for its leaf type.
- A custom diagram can be linked to a **subtype** so a "Bug" subtype can have a different lifecycle than a "Feature Request".
- **Terminal stages** have no outgoing transitions. The diagram must specify a start stage.

UI: Settings > Object customization > Stages tab.

→ Exact `stage-diagrams.create` payload (`stage_id`/`is_start`/`transitions[]`/`target_stage_id`), the custom-object stage-wiring sequence (diagram → `stage_diagram_id` on `schemas.custom.set` → `custom-objects.update` with `stage`), and subtype linkage mechanics: `../../2-stage-lifecycle-customization/references/Stages_States_and_StageDiagrams_API.md`.

**Design implication:** map the customer's business process (e.g. loan application: Submitted → Under Review → Approved/Rejected → Disbursed) directly into states + stages + a stage diagram. This is one of the most powerful and under-used customization levers.

---

## 6. Parts hierarchy and how work maps to parts

A **part** is a component of a product/service with a lifecycle, recursively composed of smaller parts. Parts are the objects almost everything links to. **Events and work items must relate to parts.**

### Customer parts (how the product is consumed)
```
Product / Service
  └─ Capability
       └─ Feature
            └─ Sub-feature (a Feature whose parent is another Feature)
```
- **Product** (`product`) — top of hierarchy; unit of P&L. A "service" variant provides an API or defines business services (IT, HR, Consulting).
- **Capability** (`capability`) — under a product; main item of customer interaction; unit of licensing/pricing.
- **Feature** (`feature`) — under a capability; unit of configuration.
- **Enhancement** (`enhancement`) — a desired change to a part; parent of multiple issues.

### Builder parts (what the developer builds)
- **Runnable** (`runnable`) — microservice/lambda/function.
- **Linkable** (`linkable`) — library/package used within a system.
- Also: `microservice`, `component`, `custom_part`.

### How work maps to parts
- Issues are **always** associated with a part (`applies_to_part`) — this routes engineering work to the right product area.
- Tickets, opportunities, incidents, articles, conversations carry `applies_to_part(_ids)` to link back to the product model.
- The part hierarchy is the routing key for "which team owns this."

**Trails** is the graph canvas that renders/manages the part hierarchy and its linked items. Managed at Product > Trails.

---

## 7. Relationships and links

**Links** create named relationships between any two objects. A link type specifies source types, target types, a `forward_name` (source→target, e.g. "is dependent on") and `backward_name` (target→source). Links are bidirectional.

Links can be created between: custom object, work (issue, ticket, task, opportunity), account, user, part.

### Default (stock) link types
Auto-provisioned and cannot be modified. Enum values include: `is_parent_of`, `is_dependent_on`, `is_related_to`, `is_duplicate_of`, `is_merged_into`, `is_follow_up_of`, `is_part_of`, `serves`, `custom_link`.

Behavior/constraints by type:
| Link type | Multiple in | Multiple out | Cycles | Max depth |
|---|---|---|---|---|
| is parent of | No | Yes | No | 2 |
| is related to | Yes | Yes | Yes | none |
| is merged into | Yes | No | No | 2 |
| is dependent on | Yes | Yes | Yes | none |

### Custom link types
Create via `link-types.custom.create` with `name`, `source_types[]`, `target_types[]`, `forward_name`, `backward_name`. Instances via `links.create`. Max 30 source and 30 target types per link type. Link types can carry their own custom fields (the relationship stores metadata). Cannot be deleted, only deprecated.

### Other relationship mechanisms
- `applies_to_part(_ids)` — work→part.
- Parent/child on work — issues spawn child issues/tasks.
- Reference (`id`) custom fields — embed a DON reference (including `custom_object.<leaf_type>`) as a field.
- `owned_by`, `created_by`, `authored_by` — user references.
- Conversation↔Ticket — convert/link.
- Tags — many-to-many categorization.

---

## 8. Quick reference: leaf-type strings

`account` · `article` · `capability` · `component` · `conversation` · `custom_part` · `devu` · `dm`/`channel` · `enhancement` · `feature` · `group` · `incident` · `issue` · `link`/`custom_link` · `linkable` · `meeting` · `microservice` · `opportunity` · `product` · `revu` · `runnable` · `sysu` · `tag` · `task` · `ticket` · `custom_object.<leaf_type>`.

---

### Gaps to verify with the customer/product docs
- `uenum` not supported for user-defined custom fields (only stock overrides).
- `composite`/`struct` have limited UI/Airdrop mapping support.
- Exact stock stage names per object type beyond issues/parts are not exhaustively documented; the three states (`open`/`in_progress`/`closed`) are authoritative.
