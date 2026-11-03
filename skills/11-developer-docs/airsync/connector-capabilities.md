# Choose connector capabilities

Source: <https://developer.devrev.ai/airsync/connector-capabilities>
Scraped: 2026-11-03

Implement the capabilities your integration needs. Declare and test every capability you expose.

| Capability                     | Required implementation                                                | Dependencies and verification                                                     |
| ------------------------------ | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Sync-unit discovery            | [External sync units worker](external-sync-units-extraction.md)  | Return stable units the connected account can access                              |
| Metadata                       | [Metadata worker](metadata-extraction.md)                        | Supply EDM matching extraction, including supported references and custom fields  |
| Initial/incremental extraction | [Data worker](data-extraction.md)                                | Mapping, stable IDs, pagination, continuation and resolved time windows           |
| Selective extraction           | [Scope filtering](extraction-scope.md)                           | Emit only enabled record types, including correct dependent references            |
| Historical extraction          | [Time-window filtering](extraction-scope.md)                     | Honor resolved lower and upper bounds; verify provider filtering behavior         |
| Attachment extraction          | [Attachment worker](extract-attachments.md)                      | Discover attachment metadata, resolve owners and stream authorized file content   |
| Custom attachment processing   | [Processors](customize-attachment-processing.md)                 | Stream files and preserve valid attachment/output associations                    |
| Permission import              | [Permission metadata and records](data-model/permissions.md)     | Principals, memberships and access rules; test restricted access                  |
| Team import                    | [Team schema and membership mappings](data-model/team-import.md) | Stable team/member identity and valid relationships                               |
| Reverse data sync              | [Data loader](load-data.md)                                      | External write scopes, supported operations, denormalization and identity mappers |
| Reverse attachment sync        | [Attachment loader](load-attachments.md)                         | Owner mapping, accessible file stream and provider upload endpoint                |
| Rich text/articles             | [Rich-text mapping](data-model/rich-text-fields.md)              | Target-specific format and attachment links                                       |

The template and Asana may not implement every AirSync capability. Check each example's declared coverage in the [code map](snap-in-examples.md).

## Check the external API

Record the endpoints and scopes behind every claimed operation, a sample external response for each record type, supported field mappings, unavailable provider features and expected pagination/rate-limit behavior. Validate these against a provider test account before broadening the connector's manifest capabilities.

Next: [Declare connector capabilities](manifest.md).
