# How data import works

Source: <https://developer.devrev.ai/airsync/extraction-phases>
Scraped: 2026-11-03

Extraction moves data from an external system into DevRev. Implement it with the latest stable `@devrev/airsync-sdk` and Node.js 20 or later. The connector discovers source resources, describes their schema, extracts normalized records and supplies attachment streams. The SDK handles worker routing, artifact uploads, state persistence and control events.

## Extraction phase contracts

| Phase                        | Incoming event                                                    | Default worker under `workers/`     | Output                                                          |
| ---------------------------- | ----------------------------------------------------------------- | ----------------------------------- | --------------------------------------------------------------- |
| Discover external sync units | `START_EXTRACTING_EXTERNAL_SYNC_UNITS`                            | `external-sync-units-extraction.js` | `ExternalSyncUnit` records in the `external_sync_units` repo    |
| Describe metadata            | `START_EXTRACTING_METADATA`, `CONTINUE_EXTRACTING_METADATA`       | `metadata-extraction.js`            | External domain metadata in the `external_domain_metadata` repo |
| Extract records              | `START_EXTRACTING_DATA`, `CONTINUE_EXTRACTING_DATA`               | `data-extraction.js`                | Normalized records and attachment descriptors in their repos    |
| Stream attachments           | `START_EXTRACTING_ATTACHMENTS`, `CONTINUE_EXTRACTING_ATTACHMENTS` | `attachments-extraction.js`         | Uploaded bytes and SDK-generated attachment associations        |

One invocation receives one event and returns one worker result. `spawn()` starts the matching worker; `processExtractionTask()` gives it an `ExtractionAdapter`. Return `success`, `progress`, `delay` or `error`; the SDK emits the corresponding phase event. Discovery accepts only `success` or `error` and does not persist connector state.

A run starts with metadata extraction. Its resolved extraction window is reused through data and attachments. The SDK commits successful extraction boundaries when the attachments phase finishes, including when there are no attachment descriptors. Do not bypass that phase by declaring the entire run complete from the data worker.

## Connector and SDK responsibilities

The connector must retrieve only accessible source data, honor the selected sync unit and [extraction scope](extraction-scope.md), maintain resumable pagination, normalize records to its metadata and obtain authenticated streams for attachments. It must declare capabilities accurately in the [manifest](manifest.md).

The SDK buffers repo items and uploads gzipped JSONL artifacts. It flushes remaining items before saving state and emitting the worker result. A repo upload failure fails the invocation; previously uploaded artifacts are still included in the error result. Stable external IDs are essential because recovery can replay source records.

Domain normalization describes the source schema; [initial domain mapping](initial-domain-mapping.md) subsequently transforms those records to DevRev types. Neither a repo nor the SDK automatically infers that mapping.

## Implement and verify each phase

* [External sync units](external-sync-units-extraction.md): verify discovered IDs and names against resources visible to the configured credentials.
* [Metadata extraction](metadata-extraction.md): validate schema, references and every emitted record type.
* [Data extraction](data-extraction.md): inspect normalized artifacts, compare selected source records and test continuation.
* [Attachment extraction](extract-attachments.md): verify binary content, parent associations and resumed uploads.

Use the [runtime contract](runtime.md) for timeouts, results and state. Use the public [template](https://github.com/devrev/airsync-template) for the worker layout. The [example map](snap-in-examples.md) records which capabilities the public Asana example actually demonstrates.

Next: [Discover external sync units](external-sync-units-extraction.md).
