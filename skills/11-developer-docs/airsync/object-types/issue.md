# issue fields

Source: <https://developer.devrev.ai/airsync/object-types/issue>
Scraped: 2026-11-03

Field reference for the `issue` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `work`, `issue`

**Capabilities:** Can Extract, Can Load, Can Subtype

## Fields

| Field                    | Type                                        | Required | Description                                                                                                                                                                               |
| ------------------------ | ------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `account_ids`            | reference (collection) → \[#record:account] |          | Accounts associated to issues.                                                                                                                                                            |
| `actual_close_date`      | timestamp                                   |          | Timestamp when the work was actually completed.                                                                                                                                           |
| `actual_effort`          | float                                       |          | Actual effort to complete the issue.                                                                                                                                                      |
| `airsync_shared_with`    | permission (collection)                     |          | List of users and groups who have explicit access to the item and the corresponding roles.                                                                                                |
| `applies_to_part_id`     | reference → \[#category:part]               | ✔︎       | Details of the part relevant to the work.                                                                                                                                                 |
| `applies_to_version_ids` | reference (collection) → \[#record:version] |          | Part versions relevant to the work.                                                                                                                                                       |
| `body`                   | rich\_text                                  |          | Body of the work object.                                                                                                                                                                  |
| `created_by_id`          | reference → \[#category:user]               |          | User ID of the user that created the object.                                                                                                                                              |
| `estimated_effort`       | float                                       |          | Estimated effort to complete the issue.                                                                                                                                                   |
| `fallback_parts`         | reference → \[#category:part]               |          | Other values that could serve as part if apples\_to\_part\_id is found to be invalid.                                                                                                     |
| `item_url_field`         | text                                        |          | Link to the item in the origin system.                                                                                                                                                    |
| `last_code_activity`     | timestamp                                   |          | Timestamp of the last code push (e.g. latest commit on all PRs with this issue). Note the Git-based snap-in populates this field, and should be installed in the org for auto-population. |
| `modified_by_id`         | reference → \[#category:user]               |          | User ID of the user that last modified the object.                                                                                                                                        |
| `owned_by_ids`           | reference (collection) → \[#category:user]  | ✔︎       | User IDs of the users that own the work.                                                                                                                                                  |
| `priority`               | enum                                        | ✔︎       | Priority of the work based upon impact and criticality.                                                                                                                                   |
| `release_version_ids`    | reference (collection) → \[#record:version] |          | Versions that will contain the resolving commit IDs.                                                                                                                                      |
| `reported_by_ids`        | reference (collection) → \[#category:user]  |          | User IDs of the users that reported the work.                                                                                                                                             |
| `rev_org_ids`            | reference (collection) → \[#record:account] |          | Rev orgs associated to issues.                                                                                                                                                            |
| `sprint_id`              | reference → \[#record:sprint]               |          | Sprint to which the issue belongs.                                                                                                                                                        |
| `sprint_state`           | enum                                        |          | State of the sprint to which the issue belongs.                                                                                                                                           |
| `stage`                  | enum                                        | ✔︎       | Stage of the object.                                                                                                                                                                      |
| `tags`                   | reference (collection) → \[#record:tag]     |          | Tags associated with the object.                                                                                                                                                          |
| `target_close_date`      | timestamp                                   |          | Timestamp when the work is expected to be complete.                                                                                                                                       |
| `target_start_date`      | timestamp                                   |          | Target start date for the object.                                                                                                                                                         |
| `team_id`                | reference → \[#record:team]                 |          | The team associated with the object.                                                                                                                                                      |
| `title`                  | text                                        | ✔︎       | Title of the work object.                                                                                                                                                                 |

## Enum values

**priority**

| Value | Name | Description |
| ----- | ---- | ----------- |
| `P0`  | P0   | -           |
| `P1`  | P1   | -           |
| `P2`  | P2   | -           |
| `P3`  | P3   | -           |

**sprint\_state**

| Value       | Name      | Description |
| ----------- | --------- | ----------- |
| `active`    | active    | -           |
| `completed` | completed | -           |
| `planned`   | planned   | -           |

**stage**

| Value            | Name           | Description |
| ---------------- | -------------- | ----------- |
| `backlog`        | Backlog        | -           |
| `completed`      | Completed      | -           |
| `duplicate`      | Duplicate      | -           |
| `in_deployment`  | In Deployment  | -           |
| `in_development` | In Development | -           |
| `in_review`      | In Review      | -           |
| `in_testing`     | In Testing     | -           |
| `prioritized`    | Prioritized    | -           |
| `triage`         | Triage         | -           |
| `wont_fix`       | Won't Fix      | -           |
