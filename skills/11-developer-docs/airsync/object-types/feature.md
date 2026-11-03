# feature fields

Source: <https://developer.devrev.ai/airsync/object-types/feature>
Scraped: 2026-11-03

Field reference for the `feature` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `part`, `feature`

**Capabilities:** Can Extract, Can Load, Can Subtype

## Fields

| Field                    | Type                                       | Required | Description                                                                                |
| ------------------------ | ------------------------------------------ | -------- | ------------------------------------------------------------------------------------------ |
| `airsync_shared_with`    | permission (collection)                    |          | List of users and groups who have explicit access to the item and the corresponding roles. |
| `api_endpoints`          | struct (collection)                        |          | Associated API endpoints.                                                                  |
| `api_parameters_summary` | text (collection)                          |          | Associated API parameters.                                                                 |
| `api_prefix_summary`     | text (collection)                          |          | Common Path Denominators of the Api Operations.                                            |
| `created_by_id`          | reference → \[#category:user]              |          | User ID of the user that created the object.                                               |
| `delivered_as`           | enum (collection)                          |          | Methods the product can be delivered as.                                                   |
| `description`            | rich\_text                                 |          | Description of the part.                                                                   |
| `development_owner_id`   | reference → \[#category:user]              |          | User ID of the development owner of the part.                                              |
| `discoveryevidences`     | text (collection)                          |          | A evidences that the inferer were able to find that justify the inference outcome.         |
| `docs`                   | struct (collection)                        |          | Docs associated with the part.                                                             |
| `fulfilled_by`           | reference (collection) → \[#category:part] |          | IDs of the runnables that fulfill this feature.                                            |
| `item_url_field`         | text                                       |          | Link to the item in the origin system.                                                     |
| `modified_by_id`         | reference → \[#category:user]              |          | User ID of the user that last modified the object.                                         |
| `name`                   | text                                       | ✔︎       | Name of the part.                                                                          |
| `owned_by_ids`           | reference (collection) → \[#category:user] | ✔︎       | User IDs of the users that own the part.                                                   |
| `parent_part`            | reference → \[#category:part]              | ✔︎       | Parent of this part.                                                                       |
| `parent_part_ids`        | reference (collection) → \[#category:part] |          | Parent Part Ids of the Part.                                                               |
| `pm_owner_id`            | reference → \[#category:user]              |          | User ID of the PM owner of the part.                                                       |
| `qa_owner_id`            | reference → \[#category:user]              |          | User ID of the QA owner of the part.                                                       |
| `ref_url`                | text                                       |          | URL to the part details (git url, website, etc.).                                          |
| `tags`                   | reference (collection) → \[#record:tag]    |          | Tags associated with the object.                                                           |

## Enum values

**delivered\_as**

| Value      | Name     | Description |
| ---------- | -------- | ----------- |
| `goods`    | goods    | -           |
| `service`  | service  | -           |
| `software` | software | -           |

### Structs

#### api\_endpoint

| Field            | Type   | Required | Description                                                                  |
| ---------------- | ------ | -------- | ---------------------------------------------------------------------------- |
| `api_operations` | struct |          | Operations associated with this API, such as the HTTP Verb, parameters, etc. |
| `api_path`       | text   |          | The URL of the API.                                                          |
| `host`           | text   |          | The Host of the API.                                                         |

#### api\_operation

| Field            | Type      | Required | Description                                                         |
| ---------------- | --------- | -------- | ------------------------------------------------------------------- |
| `api_parameters` | text      |          | Parameters associated with the API operation.                       |
| `api_path`       | text      |          | The RestAPI path of the discovered API operation.                   |
| `api_tags`       | text      |          | Tags associated with the API operation, as defined in the api file. |
| `fulfilled_by`   | reference |          | FulfilledBy IDs per API operation.                                  |
| `http_operation` | enum      |          | The Http verb of the discovered API operation.                      |
| `locations`      | struct    |          | Repo + file locations where the operation was detected.             |
| `name`           | text      |          | Name of the API operation.                                          |

#### doc\_field

| Field      | Type   | Required | Description           |
| ---------- | ------ | -------- | --------------------- |
| `doc_type` | enum   |          | Type of doc.          |
| `url_info` | struct | ✔︎       | URL Info for the doc. |

#### rev\_location\_summary

| Field         | Type | Required | Description                                                                                                  |
| ------------- | ---- | -------- | ------------------------------------------------------------------------------------------------------------ |
| `param_paths` | text |          | The detailed path inside an OpenAPI file where information about this API object and its version were found. |
| `repo_name`   | text |          | The name of the repo where information about this API object and its version were found.                     |
| `repo_path`   | text |          | The repo path where information about this API object and its version were found.                            |
| `source`      | text |          | The source where information about this API object and its version were found.                               |

#### url\_field

| Field   | Type | Required | Description             |
| ------- | ---- | -------- | ----------------------- |
| `title` | text |          | Title text for the url. |
| `url`   | text | ✔︎       | URL for the field.      |
