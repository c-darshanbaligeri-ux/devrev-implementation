# Prevent repeated updates between systems

Source: <https://developer.devrev.ai/airsync/loop-prevention>
Scraped: 2026-11-03

## Loop prevention

After a successful data write, return the external system's resulting modification timestamp as `modifiedDate`. The SDK creates or updates the mapper's `external_versions` with `{ modified_date, recipe_version: 0 }`. These recorded versions identify external changes originating in DevRev when they are later imported.

The next extraction must preserve the external object's actual modification timestamp as `modified_date`. A fabricated local timestamp prevents version matching. Use the external write response, or read the written object when the API does not return its modification time. Keep timestamp representation consistent with subsequent extraction.

The SDK owns the recipe version it writes. Do not use the SDK package version as a recipe version. If the external API cannot expose a reliable modification timestamp, document and validate the connector's alternative strategy; omitting `modifiedDate` does not establish loop prevention.

Attachment loading creates an identity mapper but does not add external versions. Test attachment replay independently from data update loops.

Related: [Reverse-sync ordering](reverse-sync-ordering.md).

Next: [Retry external writes safely](write-idempotency.md).
