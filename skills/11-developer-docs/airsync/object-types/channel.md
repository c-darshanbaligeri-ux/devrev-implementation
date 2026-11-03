# channel fields

Source: <https://developer.devrev.ai/airsync/object-types/channel>
Scraped: 2026-11-03

Field reference for the `channel` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `chat`, `channel`

**Capabilities:** Can Load

## Fields

| Field               | Type                          | Required | Description                                                                                                                                                          |
| ------------------- | ----------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `access_level`      | enum                          |          | The access level for the channel.                                                                                                                                    |
| `created_by_id`     | reference → \[#category:user] |          | User ID of the user that created the object.                                                                                                                         |
| `last_comment_date` | timestamp                     |          | Timestamp of the last comment in the chat.                                                                                                                           |
| `modified_by_id`    | reference → \[#category:user] |          | User ID of the user that last modified the object.                                                                                                                   |
| `name`              | text                          |          | The name of the channel. If provided, this will be unique across all channels in the Dev org. It's case insensitive and must contain the characters \[A-Za-z0-9\_-]. |
| `title`             | text                          |          | The title given to the chat.                                                                                                                                         |

## Enum values

**access\_level**

| Value        | Name       | Description |
| ------------ | ---------- | ----------- |
| `EXTERNAL`   | EXTERNAL   | -           |
| `INTERNAL`   | INTERNAL   | -           |
| `PRIVATE`    | PRIVATE    | -           |
| `PUBLIC`     | PUBLIC     | -           |
| `RESTRICTED` | RESTRICTED | -           |
| `UNKNOWN`    | UNKNOWN    | -           |
