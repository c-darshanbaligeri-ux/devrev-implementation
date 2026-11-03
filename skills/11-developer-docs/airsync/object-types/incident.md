# incident fields

Source: <https://developer.devrev.ai/airsync/object-types/incident>
Scraped: 2026-11-03

Field reference for the `incident` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `incident`

**Capabilities:** Can Extract, Can Load, Can Subtype

## Fields

| Field                 | Type                                        | Required | Description                                                                                |
| --------------------- | ------------------------------------------- | -------- | ------------------------------------------------------------------------------------------ |
| `acknowledged_date`   | timestamp                                   |          | Timestamp when the incident was acknowledged.                                              |
| `airsync_shared_with` | permission (collection)                     |          | List of users and groups who have explicit access to the item and the corresponding roles. |
| `applies_to_part_ids` | reference (collection) → \[#category:part]  |          | Parts to which the work is attached.                                                       |
| `body`                | rich\_text                                  |          | Body of the work object.                                                                   |
| `created_by_id`       | reference → \[#category:user]               |          | User ID of the user that created the object.                                               |
| `identified_date`     | timestamp                                   |          | Time when the incident was identified/reported.                                            |
| `item_url_field`      | text                                        |          | Link to the item in the origin system.                                                     |
| `mitigated_date`      | timestamp                                   |          | Timestamp when the incident was mitigated.                                                 |
| `modified_by_id`      | reference → \[#category:user]               |          | User ID of the user that last modified the object.                                         |
| `owned_by_ids`        | reference → \[#category:user]               | ✔︎       | User IDs of the users that own the work.                                                   |
| `pia_ids`             | reference (collection) → \[#record:article] |          | The article ids of the Post-Incident Analysis(PIA) of the incident.                        |
| `playbook_ids`        | reference (collection) → \[#record:article] |          | The article ids of the playbook(s) associated with the incident.                           |
| `related_doc_ids`     | reference (collection) → \[#record:article] |          | The article ids of other documents associated with the incident.                           |
| `reported_by`         | enum                                        |          | The entity that first reported the incident.                                               |
| `severity`            | enum                                        | ✔︎       | Severity of the work.                                                                      |
| `stage`               | enum                                        | ✔︎       |                                                                                            |
| `tags`                | reference (collection) → \[#record:tag]     |          | Tags associated with the object.                                                           |
| `target_close_date`   | timestamp                                   |          | Timestamp when the work is expected to be complete.                                        |
| `title`               | text                                        | ✔︎       | Title of the work object.                                                                  |

## Enum values

**reported\_by**

| Value | Name           | Description |
| ----- | -------------- | ----------- |
| `1`   | Customer       | -           |
| `2`   | Internal Users | -           |
| `3`   | System         | -           |

**severity**

| Value | Name  | Description |
| ----- | ----- | ----------- |
| `1`   | sev-0 | -           |
| `2`   | sev-1 | -           |
| `3`   | sev-2 | -           |
| `4`   | sev-3 | -           |

**stage**

| Value          | Name         | Description |
| -------------- | ------------ | ----------- |
| `acknowledged` | Acknowledged | -           |
| `canceled`     | Canceled     | -           |
| `duplicate`    | Duplicate    | -           |
| `fixing`       | Fixing       | -           |
| `mitigated`    | Mitigated    | -           |
| `resolved`     | Resolved     | -           |
| `triage`       | Triage       | -           |
