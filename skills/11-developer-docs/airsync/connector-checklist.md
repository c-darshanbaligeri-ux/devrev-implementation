# Connector implementation checklist

Source: <https://developer.devrev.ai/airsync/connector-checklist>
Scraped: 2026-11-03

## Build contract

Before writing workers, identify the external system's read/write endpoints, auth scopes, stable object IDs, pagination, incremental filtering, rate limits and attachment behavior. Declare only capabilities the connector implements and can verify.

A complete implementation must satisfy these boundaries:

* The manifest names functions and event sources that exist in the packaged code.
* External domain metadata describes the records actually emitted, and initial domain mapping defines their target fields and references.
* Each worker returns a valid SDK result. The SDK reports the phase outcome once.
* Continuation state tracks completed external work and survives a fresh invocation. A retry must not skip unprocessed records.
* Selective extraction and time windows constrain the records emitted.
* Authentication grants the minimum external access required for the declared capabilities.
* Live validation proves initial and incremental sync, plus every optional capability claimed by the connector.

Related: [connector anatomy](getting-started.md), [validation](validation.md).

Next: [Check connector release readiness](validation.md).
