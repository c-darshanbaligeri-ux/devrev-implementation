# Import access rules

Source: <https://developer.devrev.ai/airsync/data-model/permissions>
Scraped: 2026-11-03

## Authorization policy capability

Map a snapshot policy record type to `unified_authorization_policy`. The platform translates policies into roles, role sets and access-control entries. Authorization-policy synchronization is forward-only; disable reverse mapping.

A usable policy requires at least one principal (`users` or `groups`) and at least one access definition (`object_access`, `field_access` or `conditional_access`). The target mapping must include `object_access`, even when a particular policy record supplies only field or conditional access.

| Target field         | EDM source type                    | Mapping method               |
| -------------------- | ---------------------------------- | ---------------------------- |
| `users`              | Collection of user references      | Compatible reference mapping |
| `groups`             | Collection of group references     | Compatible reference mapping |
| `object_access`      | `record_type_privilege` collection | `make_object_access`         |
| `field_access`       | `field_privilege` collection       | `make_field_access`          |
| `conditional_access` | `conditional_privilege` collection | `make_conditional_access`    |

Privilege field definitions must declare eligible `type_keys`: `#record:<key>` for a specific type and `#category:<key>` for a category. Rules targeting undeclared types cannot be imported through that field's mapping.

## Snapshot and continuation invariants

Set `is_snapshot: true` on authorization-policy record types. When policies change, emit the **complete current policy set**, not just changed rules. A provided snapshot replaces previously imported permissions for that type. If no policy changed, the connector can omit that policy type for the run.

Never publish an incomplete policy set after an external read failure. Persist progress and continue extraction, or fail the task. Do not substitute an empty policy snapshot for an unavailable endpoint: it can remove existing access rules. Distinguish “successfully read and empty” from “could not read.”

Policy extraction must cover the same eligible types declared in metadata. Filtered or missing principals and targets can change enforcement; validate their identity and policy dependencies explicitly.

## Permission verification

Use separate allowed and denied users to verify object visibility, field visibility, edits and conditional rules. Test membership addition/removal, a changed policy snapshot, unchanged-policy omission and failure halfway through fetching rules. Confirm incomplete runs do not replace the previous complete policy set.

For articles, verify scope, owner, individual/group sharing and customer access where the connector supports it. A successful import and correct administrator view are insufficient evidence that permissions are preserved.

See the [complete policy example](permissions-example.md), [team memberships](team-import.md), [supported targets](../supported-object-types.md#unified_authorization_policy) and [metadata extraction](../metadata-extraction.md).

<span id="groups-and-memberships" />

<span id="object-level-privileges" />

Related:

* [Groups and record sharing](groups-and-sharing.md).
* [Object and field privileges](privileges.md).

Next: [Import groups and record sharing](groups-and-sharing.md).
