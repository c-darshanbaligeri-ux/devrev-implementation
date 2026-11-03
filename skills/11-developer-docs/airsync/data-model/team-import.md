# Create a team for a sync unit

Source: <https://developer.devrev.ai/airsync/data-model/team-import>
Scraped: 2026-11-03

## Sync-unit team

Add `team_data` to EDM to name the team representing the sync unit:

```json
{
  "team_data": {
    "key": "ENG",
    "name": "Engineering"
  }
}
```

This is a top-level metadata fragment. Include it alongside `record_types`, not inside a record definition. The key must be stable, unique for the intended team and match `^[A-Z]{3,5}$`. Keep the name stable across syncs and include `team_data` in subsequent metadata runs.

The platform schema supports `team_data`, while the current SDK's EDM interface does not include the extension. Model it explicitly:

```typescript
import type { ExternalDomainMetadata } from '@devrev/airsync-sdk';

type TeamMetadata = ExternalDomainMetadata & {
  team_data: { key: string; name: string };
};

export const metadata: TeamMetadata = {
  schema_version: 'v0.2.0',
  record_types: {},
  team_data: { key: 'ENG', name: 'Engineering' },
};
```

The empty `record_types` map illustrates the extension; populate it with your connector's [EDM definitions](../external-domain-metadata.md).

Imported issues, enhancements and sprints can be scoped to the sync-unit team. The associated issue/enhancement subtypes are scoped to that team; when no sync-unit team exists, their fallback scope is Global.

## Membership of the sync-unit team

Declare a membership record type mapped to `object_member`, as with [group memberships](groups-and-sharing.md#groups-and-memberships), and map the required `target_object_type` to the fixed enum value `team`. In its normalized data, use the special identity `__airsync_sync_level_team` in the field mapped to target `object_id`:

```json
{
  "object_id": "__airsync_sync_level_team",
  "add_member_ids": ["external-user-1", "external-user-2"]
}
```

This is the membership record's data, before the normalized-item envelope. The users must be imported or otherwise resolvable. The special identity resolves only in an `object_member` mapping's `object_id`; it is not a general-purpose reference for other fields.

## Verification

Import with each configuration your connector supports. Confirm the sync-unit team, mapped parent hierarchy, record team assignment and subtype scope. Add and remove members, then verify membership using their imported identities. Repeat the sync to confirm no duplicate teams appear. Test an existing-key collision and a missing parent without assuming their display values.

Related contracts: [EDM](../external-domain-metadata.md), [permissions](permissions.md), [object mappers](../object-mappers.md).

<span id="mapped-external-teams" />

Related:

* [External teams](external-teams.md).

Next: [Import external teams](external-teams.md).
