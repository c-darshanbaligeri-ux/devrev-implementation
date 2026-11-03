# task fields

Source: <https://developer.devrev.ai/airsync/object-types/task>
Scraped: 2026-11-03

Field reference for the `task` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `work`, `task`

**Capabilities:** Can Extract, Can Load, Can Subtype

## Fields

| Field                    | Type                                        | Required | Description                                                                                |
| ------------------------ | ------------------------------------------- | -------- | ------------------------------------------------------------------------------------------ |
| `actual_close_date`      | timestamp                                   |          | Timestamp when the work was actually completed.                                            |
| `actual_effort`          | float                                       |          | Actual effort to complete the task.                                                        |
| `airsync_shared_with`    | permission (collection)                     |          | List of users and groups who have explicit access to the item and the corresponding roles. |
| `applies_to_part_id`     | reference → \[#category:part]               |          | Details of the part relevant to the work.                                                  |
| `applies_to_version_ids` | reference (collection) → \[#record:version] |          | Part versions relevant to the work.                                                        |
| `body`                   | rich\_text                                  |          | Body of the work object.                                                                   |
| `created_by_id`          | reference → \[#category:user]               |          | User ID of the user that created the object.                                               |
| `embedded`               | bool                                        |          | Whether this task is an embedded task of another work or not.                              |
| `estimated_effort`       | float                                       |          | Estimated effort to complete the task.                                                     |
| `fallback_parts`         | reference → \[#category:part]               |          | Other values that could serve as part if apples\_to\_part\_id is found to be invalid.      |
| `item_url_field`         | text                                        |          | Link to the item in the origin system.                                                     |
| `modified_by_id`         | reference → \[#category:user]               |          | User ID of the user that last modified the object.                                         |
| `owned_by_ids`           | reference (collection) → \[#category:user]  | ✔︎       | User IDs of the users that own the work.                                                   |
| `priority`               | enum                                        |          | Priority of the work based upon impact and criticality.                                    |
| `reported_by_ids`        | reference (collection) → \[#category:user]  |          | User IDs of the users that reported the work.                                              |
| `stage`                  | enum                                        | ✔︎       | Stage of the object.                                                                       |
| `start_date`             | timestamp                                   |          | Timestamp when the task was started.                                                       |
| `tags`                   | reference (collection) → \[#record:tag]     |          | Tags associated with the object.                                                           |
| `target_close_date`      | timestamp                                   |          | Timestamp when the work is expected to be complete.                                        |
| `title`                  | text                                        | ✔︎       | Title of the work object.                                                                  |

## Enum values

**priority**

| Value | Name | Description |
| ----- | ---- | ----------- |
| `P0`  | P0   | -           |
| `P1`  | P1   | -           |
| `P2`  | P2   | -           |
| `P3`  | P3   | -           |

**stage**

| Value            | Name           | Description |
| ---------------- | -------------- | ----------- |
| `in_development` | In Development | -           |
| `open`           | Open           | -           |
| `resolved`       | Resolved       | -           |
