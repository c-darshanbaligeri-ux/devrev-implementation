# ticket fields

Source: <https://developer.devrev.ai/airsync/object-types/ticket>
Scraped: 2026-11-03

Field reference for the `ticket` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `work`, `ticket`

**Capabilities:** Can Extract, Can Load, Can Subtype

## Fields

| Field                     | Type                                                                           | Required | Description                                                                                                                                                                                                                                                                                                       |
| ------------------------- | ------------------------------------------------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `account_id`              | reference → \[#record:account]                                                 |          | Globally unique ID for a DevRev account.                                                                                                                                                                                                                                                                          |
| `actual_close_date`       | timestamp                                                                      |          | Timestamp when the work was actually completed.                                                                                                                                                                                                                                                                   |
| `airsync_shared_with`     | permission (collection)                                                        |          | List of users and groups who have explicit access to the item and the corresponding roles.                                                                                                                                                                                                                        |
| `applies_to_part_id`      | reference → \[#category:part]                                                  | ✔︎       | Details of the part relevant to the work.                                                                                                                                                                                                                                                                         |
| `applies_to_version_ids`  | reference (collection) → \[#record:version]                                    |          | Part versions relevant to the work.                                                                                                                                                                                                                                                                               |
| `body`                    | rich\_text                                                                     |          | Body of the work object.                                                                                                                                                                                                                                                                                          |
| `channels`                | enum (collection)                                                              |          | Channels of the ticket.                                                                                                                                                                                                                                                                                           |
| `channels_v2`             | reference (collection) → \[#record:external\_communication\_channel]           |          | Channel IDs of the ticket.                                                                                                                                                                                                                                                                                        |
| `channels_v2_instances`   | reference (collection) → \[#record:external\_communication\_channel\_instance] |          | Channel instance IDs of the ticket.                                                                                                                                                                                                                                                                               |
| `created_by_id`           | reference → \[#category:user]                                                  |          | User ID of the user that created the object.                                                                                                                                                                                                                                                                      |
| `fallback_parts`          | reference → \[#category:part]                                                  |          | Other values that could serve as part if apples\_to\_part\_id is found to be invalid.                                                                                                                                                                                                                             |
| `group`                   | reference → \[#record:group]                                                   |          | Group that owns the ticket.                                                                                                                                                                                                                                                                                       |
| `is_spam`                 | bool                                                                           |          | Whether the ticket is spam.                                                                                                                                                                                                                                                                                       |
| `item_url_field`          | text                                                                           |          | Link to the item in the origin system.                                                                                                                                                                                                                                                                            |
| `modified_by_id`          | reference → \[#category:user]                                                  |          | User ID of the user that last modified the object.                                                                                                                                                                                                                                                                |
| `needs_response`          | bool                                                                           |          | Whether the ticket needs a response.                                                                                                                                                                                                                                                                              |
| `owned_by_ids`            | reference (collection) → \[#category:user]                                     | ✔︎       | User IDs of the users that own the work.                                                                                                                                                                                                                                                                          |
| `reported_by_ids`         | reference (collection) → \[#category:user]                                     |          | User IDs of the users that reported the work.                                                                                                                                                                                                                                                                     |
| `rev_oid`                 | reference → \[#record:account]                                                 |          | Globally unique ID for a DevRev rev org.                                                                                                                                                                                                                                                                          |
| `sentiment`               | enum                                                                           |          | Sentiment of the object.                                                                                                                                                                                                                                                                                          |
| `sentiment_modified_date` | timestamp                                                                      |          | Timestamp when the sentiment was last modified.                                                                                                                                                                                                                                                                   |
| `sentiment_summary`       | text                                                                           |          | Summary justifying the sentiment.                                                                                                                                                                                                                                                                                 |
| `severity`                | enum                                                                           | ✔︎       | Severity of the ticket.                                                                                                                                                                                                                                                                                           |
| `stage`                   | enum                                                                           | ✔︎       | Stage of the object.                                                                                                                                                                                                                                                                                              |
| `tags`                    | reference (collection) → \[#record:tag]                                        |          | Tags associated with the object.                                                                                                                                                                                                                                                                                  |
| `target_close_date`       | timestamp                                                                      |          | Timestamp when the work is expected to be complete.                                                                                                                                                                                                                                                               |
| `title`                   | text                                                                           | ✔︎       | Title of the work object.                                                                                                                                                                                                                                                                                         |
| `visibility`              | enum                                                                           |          | The visibility of the object. If 'internal', the object is visible within the Dev organization. If 'external', it is visible to both the Dev organization and Rev users. If 'private', only the users with whom the object is shared with will have the access. If not set, the default visibility is 'external'. |

## Enum values

**channels**

| Value   | Name | Description |
| ------- | ---- | ----------- |
| `email` | -    | -           |
| `plug`  | -    | -           |
| `slack` | -    | -           |

**severity**

| Value     | Name    | Description |
| --------- | ------- | ----------- |
| `blocker` | Blocker | -           |
| `high`    | High    | -           |
| `low`     | Low     | -           |
| `medium`  | Medium  | -           |

**stage**

| Value                        | Name                       | Description |
| ---------------------------- | -------------------------- | ----------- |
| `awaiting_customer_response` | Awaiting Customer Response | -           |
| `awaiting_development`       | Awaiting Development       | -           |
| `awaiting_product_assist`    | Awaiting Product Assist    | -           |
| `canceled`                   | Canceled                   | -           |
| `in_development`             | In Development             | -           |
| `queued`                     | Queued                     | -           |
| `resolved`                   | Resolved                   | -           |
| `work_in_progress`           | Work In Progress           | -           |

**visibility**

| Value | Name     | Description |
| ----- | -------- | ----------- |
| `1`   | internal | -           |
| `2`   | external | -           |
| `3`   | private  | -           |
