# Declare connector capabilities

Source: <https://developer.devrev.ai/airsync/manifest>
Scraped: 2026-11-03

`manifest.yaml` connects the platform to your connector's exported functions and declares what an installation can do. Its `version: "2"` is the snap-in manifest schema version; it is independent of the SDK package version and the AirSync event protocol.

## Minimal import declaration

This fragment defines an extraction-only import. Add a complete connection configuration and the service account shown below to form a deployable manifest.

```yaml
version: "2"
name: Example Connector
description: Import Example records into DevRev
functions:
  - name: extraction
    description: Extract records from Example
imports:
  - slug: example-connector
    display_name: Example
    description: Import Example records
    extractor_function: extraction
    allowed_connection_types:
      - example-pat
```

`extractor_function` must name a function in `functions` and in the code's `functionFactory` exports. Every `allowed_connection_types` entry must match a declared `keyring_types[].id`. Keep the import slug stable across upgrades; it identifies the external integration.

## Service-account permissions

The public template declares these AirSync scopes. Start from the current template and retain permissions used by your SDK/platform path:

```yaml
service_account:
  display_name: Example Connector Bot
  scopes:
    self:
      - scope: sync_mapper_record:write
        optional: false
        reason: Maintain object identity mappings
      - scope: sync_mapper_record:read
        optional: false
        reason: Resolve object identity mappings
      - scope: sync_unit:read
        optional: false
        reason: Read sync unit configuration
      - scope: sync_snap_in:all
        optional: false
        reason: Execute AirSync connector operations
      - scope: sync_history:read
        optional: false
        reason: Read sync history
```

These DevRev scopes do not grant access to the external system. The external connection needs separate API permissions. Any additional DevRev operation your code performs must have the required service-account permission.

## Reverse-sync declaration

Add a loading function and its import reference only when the connector implements loading:

```yaml
functions:
  - name: extraction
    description: Extract Example records
  - name: loading
    description: Write changes to Example
imports:
  - slug: example-connector
    display_name: Example
    description: Synchronize Example records
    extractor_function: extraction
    loader_function: loading
    allowed_connection_types:
      - example-pat
```

The loading function must route the events it receives, return valid SDK results and implement the record/attachment operations you claim to support. Removing only its code while retaining `loader_function` exposes a capability that will fail at runtime. See [loading contracts](loading-phases.md).

## Time-scoped syncs

Declare `TIME_SCOPED_SYNCS` on an import when extraction honors the platform's resolved time window:

```yaml
imports:
  - slug: example-connector
    display_name: Example
    description: Import Example records within a selected time window
    extractor_function: extraction
    allowed_connection_types:
      - example-pat
    capabilities:
      - TIME_SCOPED_SYNCS
```

Test `extract_from` and `extract_to`, boundary records and historical completion before declaring this capability. A manifest flag does not implement filtering. See [data extraction](data-extraction.md).

## Connections and optional configuration

Define token verification, organization selection/subdomain behavior and OAuth or secret storage using [authentication and keyrings](authentication.md). The template's placeholder credential verifier must be replaced.

Declare inputs, developer keyrings or additional functions only when your implementation needs them. New inputs or connections can affect installation and automatic marketplace upgrades. Use the [manifest reference](../snapin-development/references/manifest.md) for the complete snap-in schema rather than inventing AirSync fields.

## Verification

Check function/export names, connection IDs and import slug before [creating a version](deploy-to-organization.md). Verify that the version reaches `ready`, connection creation rejects invalid credentials, and the installed connector offers only implemented directions and capabilities. Repeat these checks when the manifest changes.

Next: [How data import works](extraction-phases.md).
