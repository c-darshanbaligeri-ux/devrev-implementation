# Look up corresponding external and DevRev records

Source: <https://developer.devrev.ai/airsync/object-mappers>
Scraped: 2026-11-03

## Mapper lookup contract

| Method            | Required parameters                                                      | Result                             |
| ----------------- | ------------------------------------------------------------------------ | ---------------------------------- |
| `getByTargetId`   | `sync_unit`, `target` (DevRev ID)                                        | `{ sync_mapper_record }` or `null` |
| `getByExternalId` | `sync_unit`, `external_id`, `target_type`                                | `{ sync_mapper_record }` or `null` |
| `create`          | `sync_unit`, `external_ids`, `targets`, `status`                         | `{ sync_mapper_record }`           |
| `update`          | `id`, `sync_unit`, `external_ids: { add }`, `targets: { add }`, `status` | `{ sync_mapper_record }`           |

Responses are unwrapped values. There is no Axios `.data` property. Lookups resolve to `null` for a missing record; other failures reject with `AirSyncHttpError`. Do not treat an authorization or network failure as “not found.”

This complete helper resolves one external ID for an existing DevRev object. Connectors supporting several IDs should select by their own labeling contract rather than assuming the first ID is appropriate.

```typescript
import type { Mappers } from '@devrev/airsync-sdk';

export async function findExternalId(
  mappers: Mappers,
  syncUnit: string,
  devrevId: string,
): Promise<string | null> {
  const result = await mappers.getByTargetId({
    sync_unit: syncUnit,
    target: devrevId,
  });
  return result?.sync_mapper_record.external_ids[0] ?? null;
}
```

For an external-ID lookup, the SDK requires the DevRev target type, not the external record-type key:

```typescript
import { Mappers, SyncMapperRecordTargetType } from '@devrev/airsync-sdk';

export async function findWork(mappers: Mappers, syncUnit: string, externalId: string) {
  return mappers.getByExternalId({
    sync_unit: syncUnit,
    external_id: externalId,
    target_type: SyncMapperRecordTargetType.WORK,
  });
}
```

## Verification

Test lookup success in both directions, `null` on absence, and rejection on a non-404 platform failure. Check scope isolation between sync units and selection of secondary IDs. Confirm standard loading persists identities once and records external versions when your callback returns `modifiedDate`.

Related contracts: [data loading](load-data.md), [loop prevention](loop-prevention.md#loop-prevention), [rich text references](data-model/rich-text-fields.md).

## Mapper persistence

The SDK manages mapper writes for standard loading callbacks. Use manual persistence only for connector-owned work that requires it.

The platform maintains mappers during import. The SDK's standard loading methods create or update mappers after external writes. Do not add duplicate mapper writes to extraction or standard loading callbacks.

For a custom operation that genuinely owns a new identity link, use this public SDK shape:

```typescript
import { Mappers, SyncMapperRecordStatus } from '@devrev/airsync-sdk';

export async function persistIdentity(
  mappers: Mappers,
  syncUnit: string,
  externalId: string,
  devrevId: string,
) {
  return mappers.create({
    sync_unit: syncUnit,
    external_ids: [externalId],
    targets: [devrevId],
    status: SyncMapperRecordStatus.OPERATIONAL,
  });
}
```

An update adds identifiers using `{ add: [...] }`. The public update contract does not expose a remove or replace operation for these arrays. Do not create a new mapper merely because a lookup failed transiently.

## Mapper record fields

Use these fields and target-type values when reading or writing mapper records.

| Field               | Meaning                                                                             |
| ------------------- | ----------------------------------------------------------------------------------- |
| `id`                | Mapper record's DevRev identity                                                     |
| `external_ids`      | External IDs indexed for lookup                                                     |
| `targets`           | Related DevRev identities                                                           |
| `status`            | `operational`, `filtered` or `ignored`                                              |
| `secondary_ids`     | Optional map labeling external IDs, such as a username versus UUID                  |
| `input_files`       | Optional source file names for locating extraction data                             |
| `external_versions` | Optional `{ recipe_version, modified_date }` versions for external-origin detection |
| `extra_data`        | Optional opaque connector-specific string                                           |

Values in `secondary_ids` are not independently indexed. Include a secondary value in `external_ids` too if it must be found by external-ID lookup. Avoid storing secrets or customer payloads in `extra_data`.

`OPERATIONAL` identifies an active link. `FILTERED` records an object excluded by user filters. `IGNORED` identifies an external object that should not be created or updated in DevRev. These statuses are not interchangeable missing-record signals.

## SDK target types

The public `SyncMapperRecordTargetType` enum includes:

| Target type                          | Value                                |
| ------------------------------------ | ------------------------------------ |
| `ACCESS_CONTROL_ENTRY`               | `access_control_entry`               |
| `ACCOUNT`                            | `account`                            |
| `AIRDROP_AUTHORIZATION_POLICY`       | `airdrop_authorization_policy`       |
| `AIRDROP_FIELD_AUTHORIZATION_POLICY` | `airdrop_field_authorization_policy` |
| `AIRDROP_PLATFORM_GROUP`             | `airdrop_platform_group`             |
| `ARTICLE`                            | `article`                            |
| `ARTIFACT`                           | `artifact`                           |
| `CHAT`                               | `chat`                               |
| `CONVERSATION`                       | `conversation`                       |
| `CUSTOM_OBJECT`                      | `custom_object`                      |
| `DIRECTORY`                          | `directory`                          |
| `GROUP`                              | `group`                              |
| `INCIDENT`                           | `incident`                           |
| `LINK`                               | `link`                               |
| `MEETING`                            | `meeting`                            |
| `OBJECT_MEMBER`                      | `object_member`                      |
| `PART`                               | `part`                               |
| `REV_ORG`                            | `rev_org`                            |
| `ROLE`                               | `role`                               |
| `ROLE_SET`                           | `role_set`                           |
| `TAG`                                | `tag`                                |
| `TIMELINE_COMMENT`                   | `timeline_comment`                   |
| `USER`                               | `user`                               |
| `WORK`                               | `work`                               |

A mapper target enum does not guarantee that a corresponding external record type is supported for import or reverse sync. Consult [supported object types](supported-object-types.md) and the recipe for that capability.
