# Troubleshoot mappings and identity

Source: <https://developer.devrev.ai/airsync/mapping-troubleshooting>
Scraped: 2026-11-03

Use these checks when the connector fails during mapping and identity.

## Metadata and normalized records disagree

A record type represents a homogeneous schema. Normalize integer values to JSON numbers, collections to arrays and references to the reference shape declared by metadata. Strings such as `"42"` are not integer values; identifiers can legitimately be strings. A comma-separated string is not a collection.

Embedded structured data is different from an object reference. Use the declared reference type and stable external ID when the value identifies another record. Check nullability, enum values, collection elements and timestamp formats against the [external domain model](metadata-extraction.md) and [mapping contract](initial-domain-mapping.md).

## Required fields are missing after mapping

Compare the actual metadata, normalized value and chosen transformation. Check missing-value fallback, required target fields and reference targets. Defaults in the mapping file are starting choices; inspect the actual mapping selected for the import. Unmapped source fields must not be assumed to produce the intended custom fields without validating the offered choices.

## Duplicate records or repeated reverse-sync writes

Check stable external IDs, mapper lookups, create/update decisions and modified-time handling. In v2, a missing mapper resolves to `null`; lookup responses are already unwrapped. A catch-only existence check written for v1 can now silently choose the wrong branch. Verify initial import → reverse write → subsequent extraction converges to the same objects. See [object mappers](object-mappers.md) and [loading](load-data.md).

Related: [troubleshooting index](faq.md).
