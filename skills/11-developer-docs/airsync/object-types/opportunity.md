# opportunity fields

Source: <https://developer.devrev.ai/airsync/object-types/opportunity>
Scraped: 2026-11-03

Field reference for the `opportunity` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `work`, `opportunity`

**Capabilities:** Can Extract, Can Load, Can Subtype

## Fields

| Field                   | Type                                       | Required | Description                                                                                |
| ----------------------- | ------------------------------------------ | -------- | ------------------------------------------------------------------------------------------ |
| `account_id`            | reference → \[#record:account]             |          | ID of the account that the opportunity is related to.                                      |
| `actual_close_date`     | timestamp                                  |          | Timestamp when the work was actually completed.                                            |
| `airsync_shared_with`   | permission (collection)                    |          | List of users and groups who have explicit access to the item and the corresponding roles. |
| `annual_contract_value` | struct                                     |          | Annual contract value of the opportunity.                                                  |
| `body`                  | rich\_text                                 |          | Body of the work object.                                                                   |
| `budget`                | struct                                     |          | Budget of the opportunity.                                                                 |
| `contact_ids`           | reference (collection) → \[#record:revu]   |          | Contacts involved in the opportunity.                                                      |
| `created_by_id`         | reference → \[#category:user]              |          | User ID of the user that created the object.                                               |
| `fallback_parts`        | reference → \[#category:part]              |          | Other values that could serve as part if apples\_to\_part\_id is found to be invalid.      |
| `forecast_category`     | enum                                       | ✔︎       | Forecast category of the opportunity.                                                      |
| `item_url_field`        | text                                       |          | Link to the item in the origin system.                                                     |
| `modified_by_id`        | reference → \[#category:user]              |          | User ID of the user that last modified the object.                                         |
| `owned_by_ids`          | reference (collection) → \[#category:user] | ✔︎       | User IDs of the users that own the work.                                                   |
| `priority`              | enum                                       | ✔︎       | Priority of the opportunity.                                                               |
| `probability`           | float                                      |          | Probability of winning the deal, value lies between 0.0% and 100.0%.                       |
| `reported_by_ids`       | reference (collection) → \[#category:user] |          | User IDs of the users that reported the work.                                              |
| `stage`                 | enum                                       | ✔︎       | Stage of the object.                                                                       |
| `tags`                  | reference (collection) → \[#record:tag]    |          | Tags associated with the object.                                                           |
| `target_close_date`     | timestamp                                  |          | Timestamp when the work is expected to be complete.                                        |
| `title`                 | text                                       | ✔︎       | Title of the work object.                                                                  |
| `value`                 | struct                                     |          | Value of the opportunity.                                                                  |

## Enum values

**forecast\_category**

| Value           | Name           | Description |
| --------------- | -------------- | ----------- |
| `commit`        | commit         | -           |
| `omitted`       | omitted        | -           |
| `pipeline`      | pipeline       | -           |
| `strong_upside` | strong\_upside | -           |
| `upside`        | upside         | -           |
| `won`           | won            | -           |

**priority**

| Value | Name | Description |
| ----- | ---- | ----------- |
| `P0`  | P0   | -           |
| `P1`  | P1   | -           |
| `P2`  | P2   | -           |
| `P3`  | P3   | -           |

**stage**

| Value           | Name          | Description |
| --------------- | ------------- | ----------- |
| `closed_lost`   | Closed Lost   | -           |
| `closed_won`    | Closed Won    | -           |
| `contract`      | Contract      | -           |
| `negotiation`   | Negotiation   | -           |
| `qualification` | Qualification | -           |
| `stalled`       | Stalled       | -           |
| `validation`    | Validation    | -           |

### Structs

#### money

| Field      | Type | Required | Description            |
| ---------- | ---- | -------- | ---------------------- |
| `amount`   | text | ✔︎       | Amount of the money.   |
| `currency` | text | ✔︎       | Currency of the money. |
