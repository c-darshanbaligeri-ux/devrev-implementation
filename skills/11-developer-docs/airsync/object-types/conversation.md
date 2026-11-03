# conversation fields

Source: <https://developer.devrev.ai/airsync/object-types/conversation>
Scraped: 2026-11-03

Field reference for the `conversation` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `conversation`

**Capabilities:** Can Load, Can Subtype

## Fields

| Field                              | Type                                                                           | Required | Description                                                                                                                                                          |
| ---------------------------------- | ------------------------------------------------------------------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `account_id`                       | reference → \[#record:account]                                                 |          | Globally unique ID for a DevRev account.                                                                                                                             |
| `actual_close_date`                | timestamp                                                                      |          | Timestamp when the conversation was actually completed.                                                                                                              |
| `ai_resolution_status`             | enum                                                                           |          | Status of the AI resolution for the conversation.                                                                                                                    |
| `airsync_shared_with`              | permission (collection)                                                        |          | List of users and groups who have explicit access to the item and the corresponding roles.                                                                           |
| `applies_to_part_ids`              | reference (collection) → \[#category:part]                                     |          | Details of the parts relevant to the conversation.                                                                                                                   |
| `broadcast_channels`               | text (collection)                                                              |          | Active channels for the conversation.                                                                                                                                |
| `channels`                         | reference (collection) → \[#record:external\_communication\_channel]           |          | Channel IDs of the conversation.                                                                                                                                     |
| `channels_instances`               | reference (collection) → \[#record:external\_communication\_channel\_instance] |          | Channel instance IDs of the conversation.                                                                                                                            |
| `conversation_type`                | enum                                                                           | ✔︎       | A type of object used to track conversations.                                                                                                                        |
| `created_by_id`                    | reference → \[#category:user]                                                  |          | User ID of the user that created the object.                                                                                                                         |
| `description`                      | rich\_text                                                                     |          | Description of the conversation object.                                                                                                                              |
| `first_response_time`              | timestamp                                                                      |          | Timestamp to track the first response from Dev.                                                                                                                      |
| `first_unreplied_rev_message_date` | timestamp                                                                      |          | First unreplied customer message's timestamp.                                                                                                                        |
| `group`                            | reference → \[#record:group]                                                   |          | Group that owns the conversation.                                                                                                                                    |
| `is_creator_verified`              | bool                                                                           |          | Whether the conversation is created by verified user.                                                                                                                |
| `is_spam`                          | bool                                                                           |          | Whether the conversation is spam.                                                                                                                                    |
| `last_external_message_date`       | timestamp                                                                      |          | Timestamp of the last message in external discussion.                                                                                                                |
| `last_external_message_id`         | reference → \[#record:comment]                                                 |          | ID of the last message in external discussion.                                                                                                                       |
| `last_internal_message_date`       | timestamp                                                                      |          | Timestamp of the last message in internal discussions.                                                                                                               |
| `last_internal_message_id`         | reference → \[#record:comment]                                                 |          | ID of the last message in internal discussion.                                                                                                                       |
| `last_message_id`                  | reference → \[#record:comment]                                                 |          | ID of the last message on the object.                                                                                                                                |
| `last_message_timestamp`           | timestamp                                                                      |          | Timestamp of the last message in the conversation.                                                                                                                   |
| `member_ids`                       | reference (collection) → \[#category:user]                                     | ✔︎       | User IDs of the users in the conversation.                                                                                                                           |
| `modified_by_id`                   | reference → \[#category:user]                                                  |          | User ID of the user that last modified the object.                                                                                                                   |
| `owned_by_ids`                     | reference (collection) → \[#category:user]                                     |          | Users that own the conversation.                                                                                                                                     |
| `participant_oids`                 | reference (collection) → \[#record:account]                                    |          | Globally unique IDs of participating orgs.                                                                                                                           |
| `participant_uids`                 | reference (collection) → \[#category:user]                                     |          | Globally unique ID of DevRev rev users.                                                                                                                              |
| `priority`                         | enum                                                                           |          | Priority of the conversation.                                                                                                                                        |
| `sentiment`                        | enum                                                                           |          | Sentiment of the object.                                                                                                                                             |
| `sentiment_modified_date`          | timestamp                                                                      |          | Timestamp when the sentiment was last modified.                                                                                                                      |
| `sentiment_summary`                | text                                                                           |          | Summary justifying the sentiment.                                                                                                                                    |
| `source_channel`                   | text                                                                           |          | Source channel for the conversation.                                                                                                                                 |
| `stage`                            | enum                                                                           |          | Stage of the conversation.                                                                                                                                           |
| `started_by_id`                    | reference → \[#category:user]                                                  |          | User that started the conversation.                                                                                                                                  |
| `tags`                             | reference (collection) → \[#record:tag]                                        |          | Tags associated with the object.                                                                                                                                     |
| `title`                            | text                                                                           |          | Title of the conversation object.                                                                                                                                    |
| `turing_active`                    | bool                                                                           |          | Whether Turing is active on the conversation. Will be true when Turing is active and false when it stops responding or when a dev user responds to the conversation. |

## Enum values

**ai\_resolution\_status**

| Value | Name      | Description |
| ----- | --------- | ----------- |
| `1`   | deflected | -           |
| `2`   | escalated | -           |

**conversation\_type**

| Value     | Name    | Description |
| --------- | ------- | ----------- |
| `support` | Support | -           |

**priority**

| Value | Name | Description |
| ----- | ---- | ----------- |
| `P0`  | P0   | -           |
| `P1`  | P1   | -           |
| `P2`  | P2   | -           |

**stage**

| Value             | Name            | Description |
| ----------------- | --------------- | ----------- |
| `archived`        | Archived        | -           |
| `hold`            | Hold            | -           |
| `needs_response`  | Needs Response  | -           |
| `new`             | New             | -           |
| `resolved`        | Resolved        | -           |
| `suspended`       | Suspended       | -           |
| `waiting_on_user` | Waiting On User | -           |
