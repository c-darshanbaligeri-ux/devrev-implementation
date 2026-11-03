# meeting fields

Source: <https://developer.devrev.ai/airsync/object-types/meeting>
Scraped: 2026-11-03

Field reference for the `meeting` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `meeting`

**Capabilities:** Can App Fragment, Can Extract, Can Load

## Fields

| Field                   | Type                                          | Required | Description                                                                                                                                                                                                                                                                                                       |
| ----------------------- | --------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `channel`               | enum                                          | ✔︎       | The channel of meeting.                                                                                                                                                                                                                                                                                           |
| `created_by_id`         | reference → \[#category:user]                 |          | User ID of the user that created the object.                                                                                                                                                                                                                                                                      |
| `description`           | rich\_text                                    |          | Description of the meeting.                                                                                                                                                                                                                                                                                       |
| `ended_date`            | timestamp                                     |          | Time at which meeting ended.                                                                                                                                                                                                                                                                                      |
| `engagement_new_ref`    | text                                          |          | Reference ID associated with the new engagement.                                                                                                                                                                                                                                                                  |
| `external_ref_id`       | text                                          |          | External reference of the meeting. This is the identifier from the meeting channel/provider.                                                                                                                                                                                                                      |
| `external_ref_ids`      | text (collection)                             |          | External reference IDs associated with the meeting.                                                                                                                                                                                                                                                               |
| `external_url`          | text                                          |          | External URL associated with the meeting.                                                                                                                                                                                                                                                                         |
| `item_url_field`        | text                                          |          | Link to the item in the origin system.                                                                                                                                                                                                                                                                            |
| `modified_by_id`        | reference → \[#category:user]                 |          | User ID of the user that last modified the object.                                                                                                                                                                                                                                                                |
| `organizer_id`          | reference → \[#category:user #record:group]   | ✔︎       | ID of the organizer of the meeting.                                                                                                                                                                                                                                                                               |
| `parent_id`             | reference → \[#category:work #record:account] |          | Parent ID of the meeting.                                                                                                                                                                                                                                                                                         |
| `parent_object_type`    | enum                                          |          | Parent Objet Type.                                                                                                                                                                                                                                                                                                |
| `participants`          | participation (collection)                    | ✔︎       | Represents the participants (devu/revu/group) of the meeting.                                                                                                                                                                                                                                                     |
| `recording_url`         | text                                          |          | Recording URL of the meeting.                                                                                                                                                                                                                                                                                     |
| `scheduled_date`        | timestamp                                     |          | Time at which meeting was scheduled to start.                                                                                                                                                                                                                                                                     |
| `source_date`           | timestamp                                     |          | The original source timestamp used for display.                                                                                                                                                                                                                                                                   |
| `state`                 | enum                                          | ✔︎       | The state of meeting.                                                                                                                                                                                                                                                                                             |
| `tags`                  | reference (collection) → \[#record:tag]       |          | Tags associated with the meeting.                                                                                                                                                                                                                                                                                 |
| `title`                 | text                                          |          | Title of the meeting object.                                                                                                                                                                                                                                                                                      |
| `transcript_article_id` | reference → \[#record:article]                |          | ID of the article for the transcript of the meeting.                                                                                                                                                                                                                                                              |
| `visibility`            | enum                                          |          | The visibility of the object. If 'internal', the object is visible within the Dev organization. If 'external', it is visible to both the Dev organization and Rev users. If 'private', only the users with whom the object is shared with will have the access. If not set, the default visibility is 'external'. |

## Enum values

**channel**

| Value            | Name            | Description |
| ---------------- | --------------- | ----------- |
| `amazon_connect` | amazon\_connect | -           |
| `devrev`         | devrev          | -           |
| `google_meet`    | google\_meet    | -           |
| `offline`        | offline         | -           |
| `other`          | other           | -           |
| `teams`          | teams           | -           |
| `zoom`           | zoom            | -           |

**parent\_object\_type**

| Value     | Name | Description |
| --------- | ---- | ----------- |
| `account` | -    | -           |
| `work`    | -    | -           |

**state**

| Value         | Name        | Description |
| ------------- | ----------- | ----------- |
| `canceled`    | canceled    | -           |
| `completed`   | completed   | -           |
| `no_show`     | no\_show    | -           |
| `ongoing`     | ongoing     | -           |
| `rejected`    | rejected    | -           |
| `rescheduled` | rescheduled | -           |
| `scheduled`   | scheduled   | -           |
| `waiting`     | waiting     | -           |

**visibility**

| Value | Name     | Description |
| ----- | -------- | ----------- |
| `1`   | internal | -           |
| `2`   | external | -           |
| `3`   | private  | -           |
