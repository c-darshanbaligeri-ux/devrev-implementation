# Access-rule import example

Source: <https://developer.devrev.ai/airsync/data-model/permissions-example>
Scraped: 2026-11-03

This example models users, groups, tasks and a complete authorization-policy snapshot. It demonstrates object-level, field-level and conditional rules in one policy. It is a schema and normalization example; API authentication and policy retrieval remain connector-specific.

## Complete example metadata

```json
{
  "schema_version": "v0.2.0",
  "record_types": {
    "users": {
      "fields": {
        "id": { "type": "text", "is_identifier": true },
        "name": { "type": "text" }
      }
    },
    "groups": {
      "fields": {
        "id": { "type": "text", "is_identifier": true },
        "name": { "type": "text" }
      }
    },
    "tasks": {
      "fields": {
        "id": { "type": "text", "is_identifier": true },
        "title": { "type": "text", "is_required": true },
        "body": { "type": "rich_text" },
        "owner": {
          "type": "reference",
          "reference": { "refers_to": { "#record:users": {} } }
        },
        "status": {
          "type": "enum",
          "enum": { "values": [{ "key": "open" }, { "key": "done" }] }
        }
      }
    },
    "access_rules": {
      "is_snapshot": true,
      "no_identifier": true,
      "fields": {
        "permission_users": {
          "type": "reference",
          "collection": {},
          "reference": { "refers_to": { "#record:users": {} } }
        },
        "permission_groups": {
          "type": "reference",
          "collection": {},
          "reference": { "refers_to": { "#record:groups": {} } }
        },
        "object_level_permissions": {
          "type": "record_type_privilege",
          "collection": {},
          "record_type_privilege": { "type_keys": ["#record:tasks"] }
        },
        "field_level_permissions": {
          "type": "field_privilege",
          "collection": {},
          "field_privilege": { "type_keys": ["#record:tasks"] }
        },
        "conditional_permissions": {
          "type": "conditional_privilege",
          "collection": {},
          "conditional_privilege": { "type_keys": ["#record:tasks"] }
        }
      }
    }
  }
}
```

All referenced keys are defined. Only `tasks` is declared an eligible policy target. Add other types to the appropriate `type_keys` only when your connector implements those policy semantics.

## Initial mapping configuration

Map users to the appropriate user type, groups to `group`, tasks to a supported work type, and `access_rules` to `unified_authorization_policy`. Build the complete file from the [public template and IDM contract](../initial-domain-mapping.md); this field-level fragment shows the required policy mappings inside its shard:

```json
{
  "users": {
    "forward": true,
    "reverse": false,
    "primary_external_field": "permission_users",
    "transformation_method_for_set": { "transformation_method": "use_directly" }
  },
  "groups": {
    "forward": true,
    "reverse": false,
    "primary_external_field": "permission_groups",
    "transformation_method_for_set": { "transformation_method": "use_directly" }
  },
  "object_access": {
    "forward": true,
    "reverse": false,
    "primary_external_field": "object_level_permissions",
    "transformation_method_for_set": { "transformation_method": "make_object_access" }
  },
  "field_access": {
    "forward": true,
    "reverse": false,
    "primary_external_field": "field_level_permissions",
    "transformation_method_for_set": { "transformation_method": "make_field_access" }
  },
  "conditional_access": {
    "forward": true,
    "reverse": false,
    "primary_external_field": "conditional_permissions",
    "transformation_method_for_set": { "transformation_method": "make_conditional_access" }
  }
}
```

The record mapping must also set `forward: true`, `reverse: false`. Include `object_access` in the mapping even if a specific policy record supplies only field or conditional rules.

## Normalized policy data

This is the policy record's `data` value, before the repo's normalized-item envelope:

```json
{
  "permission_users": ["user-1"],
  "permission_groups": ["group-1"],
  "object_level_permissions": [
    { "record_types": ["tasks"], "privileges": ["read"] }
  ],
  "field_level_permissions": [
    {
      "record_type": "tasks",
      "read_fields": ["title", "body", "owner", "status"],
      "write_fields": ["title", "body"]
    }
  ],
  "conditional_permissions": [
    {
      "record_type": "tasks",
      "object_privileges": ["update"],
      "scope_to_users_in": ["owner"]
    }
  ]
}
```

The policy names external IDs and field keys. It grants task read access, configured field access, and conditional update access when the principal is the task owner. Synchronize `user-1` and `group-1`, and preserve membership if `group-1` contains external users.

A caveat-based conditional rule is an alternative to the owner scope:

```json
{
  "record_type": "tasks",
  "field_privileges": { "read_all_fields": true, "write_fields": ["title"] },
  "field_caveats": [
    { "field": "status", "operator": "eq", "value": "open" }
  ]
}
```

Do not combine `field_caveats` with `scope_to_users_in` or `scope_to_groups_in` in the same conditional entry. Separate policies can represent distinct rules.

## Snapshot implementation

When any policy changes, retrieve and emit all currently applicable policy records. Continue fetching after pagination and timeouts without turning a partially collected set into a completed snapshot. If no policies changed, omit the policy type. A successfully fetched empty current set is different from a failed read.

See [data extraction](../data-extraction.md) for the SDK repo envelope and continuation contract. No reverse policy worker is needed: authorization-policy mapping is forward-only.

## Verification

Create tasks owned by an included and an excluded user, and test the resulting access with both identities. Confirm read/write field distinctions, owner-based updates and caveat behavior. Remove a rule from the external policy set and confirm it disappears after a complete snapshot. Interrupt retrieval halfway through and verify the old complete policy remains until the new snapshot succeeds.

The source's rule model and DevRev's permission model may differ. Validate enforcement with representative accounts before advertising equivalence; a valid JSON mapping does not prove equivalent access.

Related contracts: [permissions](permissions.md), [EDM](../external-domain-metadata.md), [transformation methods](transformation-methods.md).

Next: [Create a team for a sync unit](team-import.md).
