# Import groups and record sharing

Source: <https://developer.devrev.ai/airsync/data-model/groups-and-sharing>
Scraped: 2026-11-03

## Groups and memberships

Represent external groups as a record type mapped to DevRev `group`. Represent membership as a separate record type mapped to `object_member`:

| Membership target field | External data contract                                                                |
| ----------------------- | ------------------------------------------------------------------------------------- |
| `object_id`             | Reference to the external group or mapped team                                        |
| `target_object_type`    | Required enum; map to the fixed value `group` or `team` for the membership target     |
| `add_member_ids`        | Collection of references to users to add                                              |
| `remove_member_ids`     | Collection of references to users to remove when the external source exposes removals |
| `member_id`             | Single-member alternative offered by the target mapping                               |

Configure `target_object_type` with a `use_fixed_value` enum mapping; see the public [Asana group membership mapping](https://github.com/devrev/airdrop-asana-snap-in/blob/ee2a31f4e4ef746c7650f9c78e2f67ac430eec19/code/src/asana/initial_domain_mapping.json#L640-L648). This target value does not require an additional field in the normalized source record.

Do not infer membership removal from an incremental list containing only changed users. Define whether the source endpoint supplies a full membership set or explicit additions/removals and normalize accordingly. Users and groups must exist or be resolvable in the same import.

Platform groups such as Dev users and Rev users already exist in DevRev. To map external default groups to these targets, declare an external record type containing an enum of default groups, map it to `airdrop_platform_group`, and reference that type in sharing fields. This lets users select the platform-group mapping rather than hard-coding org-specific identities.

## Per-record sharing

Article `shared_with` uses the `permission` type, normally as a collection. Other supported objects expose `airsync_shared_with`; inspect their [field contracts](../supported-object-types.md) instead of assuming all objects share an identical field.

A permission entry associates `member_id` with an external `role`. Declare allowed member record types and external role values in EDM, then map roles to the supported target roles:

```json
{
  "shared_with": {
    "type": "permission",
    "collection": {},
    "permission": {
      "role": {
        "values": [{ "key": "owner" }, { "key": "editor" }, { "key": "viewer" }]
      },
      "member_id": {
        "refers_to": {
          "#record:users": {},
          "#record:groups": {},
          "#record:platform_groups": {}
        }
      }
    }
  }
}
```

This is a field-definition fragment, not a complete EDM. Its referenced record types must be declared. Do not assume source role names are DevRev role identifiers; configure an explicit role mapping and verify the target role.

For articles, scope and sharing interact. An internal article's access is governed by its owner and explicit sharing. External scope is intended for customer-facing content and can expose it through Portal/PLuG when publication is configured. Test the org's actual roles, scope and publishing state before asserting that imported access mirrors the source.

Related: [Permissions](permissions.md).

Next: [Define object and field privileges](privileges.md).
