# object_member fields

Source: <https://developer.devrev.ai/airsync/object-types/object_member>
Scraped: 2026-11-03

Field reference for the `object_member` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `object_member`

**Capabilities:** Can Load

## Fields

| Field                | Type                                                                                              | Required | Description                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------- |
| `add_member_ids`     | reference (collection) → \[#category:user #record:group]                                          |          | Add or update user IDs in the group.                                                     |
| `airsync_role`       | enum                                                                                              |          | User's access level on the target item.                                                  |
| `created_by_id`      | reference → \[#category:user]                                                                     |          | User ID of the user that created the object.                                             |
| `member_id`          | reference → \[#category:user #record:group]                                                       |          | ID of the user or group.                                                                 |
| `member_rev_oid`     | reference → \[#record:account]                                                                    |          | The unique ID of the member's Rev Organization.                                          |
| `modified_by_id`     | reference → \[#category:user]                                                                     |          | User ID of the user that last modified the object.                                       |
| `object_id`          | reference → \[#category:custom\_object #category:work #record:article #record:group #record:team] | ✔︎       | Globally unique DevRev Object Name (DON) for the object where the member is being added. |
| `remove_member_ids`  | reference (collection) → \[#category:user #record:group]                                          |          | Remove user IDs from the group.                                                          |
| `target_object_type` | enum                                                                                              | ✔︎       | Type of target object.                                                                   |
| `valid_from_date`    | timestamp                                                                                         |          | Timestamp when this membership is valid.                                                 |
| `valid_to_date`      | timestamp                                                                                         |          | Timestamp when this membership expires.                                                  |

## Enum values

**airsync\_role**

| Value         | Name   | Description |
| ------------- | ------ | ----------- |
| `edit_access` | Editor | -           |
| `read_access` | Viewer | -           |

**target\_object\_type**

| Value           | Name | Description |
| --------------- | ---- | ----------- |
| `group`         | -    | -           |
| `dashboard`     | -    | -           |
| `work`          | -    | -           |
| `article`       | -    | -           |
| `custom_object` | -    | -           |
| `account`       | -    | -           |
| `team`          | -    | -           |
