# article fields

Source: <https://developer.devrev.ai/airsync/object-types/article>
Scraped: 2026-11-03

Field reference for the `article` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `article`

**Capabilities:** Can Load, Can Subtype

## Fields

| Field                        | Type                                       | Required | Description                                                                                                                             |
| ---------------------------- | ------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `access_level`               | enum                                       |          | Default access level for the object.                                                                                                    |
| `aliases`                    | text (collection)                          |          | Aliases for the URL of the article.                                                                                                     |
| `applies_to_part_ids`        | reference (collection) → \[#category:part] |          | Parts relevant to the article.                                                                                                          |
| `authored_by_ids`            | reference (collection) → \[#category:user] |          | Users that authored the article.                                                                                                        |
| `created_by_id`              | reference → \[#category:user]              |          | User ID of the user that created the object.                                                                                            |
| `description`                | rich\_text                                 |          | Description of the article.                                                                                                             |
| `external_translation_group` | text                                       |          | The translation group the article belongs to.                                                                                           |
| `extracted_plain_text`       | text                                       |          | Extracted Plain Text.                                                                                                                   |
| `item_url_field`             | text                                       |          | Link to the item in the origin system.                                                                                                  |
| `language`                   | text                                       |          | Language of the article for i18n support.                                                                                               |
| `modified_by_id`             | reference → \[#category:user]              |          | User ID of the user that last modified the object.                                                                                      |
| `notify`                     | bool                                       |          | Whether to notify the user when the release notes are updated.                                                                          |
| `num_downvotes`              | int                                        |          | Number of downvotes on the article.                                                                                                     |
| `num_upvotes`                | int                                        |          | Number of upvotes on the article.                                                                                                       |
| `owned_by_ids`               | reference (collection) → \[#category:user] | ✔︎       | Users that own the article.                                                                                                             |
| `parent`                     | reference → \[#record:directory]           |          | Parent of the article.                                                                                                                  |
| `published_date`             | timestamp                                  |          | Timestamp when the article was published.                                                                                               |
| `release_notes`              | text                                       |          | Release notes for the item.                                                                                                             |
| `resource`                   | struct                                     |          | The user visible resource of the article. It can either be rich text visible in DevRev or a URL to an article hosted outside of DevRev. |
| `scope`                      | enum                                       |          | Scope of the article.                                                                                                                   |
| `shared_with`                | permission (collection)                    |          | The list of Rev user, groups and dynamic groups with whom the article is shared and the corresponding roles.                            |
| `status`                     | enum                                       |          | Status of the article.                                                                                                                  |
| `tags`                       | reference (collection) → \[#record:tag]    |          | Tags associated with the article.                                                                                                       |
| `title`                      | text                                       | ✔︎       | Title of the article.                                                                                                                   |
| `type`                       | enum                                       |          | Type of the article.                                                                                                                    |
| `visible_to`                 | enum                                       |          |                                                                                                                                         |

## Enum values

**access\_level**

| Value        | Name | Description |
| ------------ | ---- | ----------- |
| `EXTERNAL`   | -    | -           |
| `INTERNAL`   | -    | -           |
| `PRIVATE`    | -    | -           |
| `PUBLIC`     | -    | -           |
| `RESTRICTED` | -    | -           |

**scope**

| Value | Name     | Description |
| ----- | -------- | ----------- |
| `1`   | internal | -           |
| `2`   | external | -           |

**status**

| Value           | Name           | Description |
| --------------- | -------------- | ----------- |
| `archived`      | archived       | -           |
| `draft`         | draft          | -           |
| `published`     | published      | -           |
| `review_needed` | review\_needed | -           |

**type**

| Value           | Name           | Description |
| --------------- | -------------- | ----------- |
| `article`       | article        | -           |
| `content_block` | content\_block | -           |
| `page`          | page           | -           |

**visible\_to**

| Value                | Name | Description |
| -------------------- | ---- | ----------- |
| `customer_admins`    | -    | -           |
| `customers`          | -    | -           |
| `verified_customers` | -    | -           |

### Structs

#### resource

| Field     | Type       | Required | Description                                                           |
| --------- | ---------- | -------- | --------------------------------------------------------------------- |
| `content` | rich\_text |          | Rich text content of the resource (relevant only for type devrev/rt). |
| `type`    | enum       |          | The type of resource.                                                 |
| `url`     | text       |          | URL of the resource (relevant only for type url).                     |
