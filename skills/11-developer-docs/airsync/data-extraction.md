# Extract and normalize records

Source: <https://developer.devrev.ai/airsync/data-extraction>
Scraped: 2026-11-03

## Preconditions and normalized output

Declare every source record type in [metadata](metadata-extraction.md) and provide its [initial mapping](initial-domain-mapping.md). Use the source connection's permitted read scopes. Apply [record selection](extraction-scope.md) and [extraction time windows](extraction-windows.md) to the source requests and related records.

Ordinary records have this envelope:

```json
{
  "id": "task-123",
  "created_date": "2026-01-01T12:00:00.000Z",
  "modified_date": "2026-01-02T12:00:00.000Z",
  "data": {
    "title": "Example task",
    "owner": "user-456",
    "item_url_field": "https://source.example/tasks/task-123"
  }
}
```

`id`, `created_date`, `modified_date` and `data` are required by `NormalizedItem`. IDs must remain stable across runs. Timestamp strings use RFC3339; date fields use `YYYY-MM-DD`. A repo's `itemType` must exactly match the metadata record-type key. The `data` object must match that type's fields, including whether a field is required and references.

Normalize missing source values to `null` or omit optional fields; do not treat a legitimate empty string or zero as missing indiscriminately. Numbers must be JSON numbers. Collections must be arrays. Plain references are external ID strings; typed references follow their explicit metadata shape. Map a source item URL field to the target link where appropriate rather than assuming a URL is inferred from its ID.

Register a `normalize(record: object)` callback per repo or push already normalized objects. Attachment descriptors have a [different envelope](extract-attachments.md); they do not use `NormalizedItem.data`.

## Upload, state and failure invariants

Call `initializeRepos` once per invocation before output. Check required repos explicitly: optional chaining can silently discard records when a repo name is wrong. Await every `push` and upload. Repos batch at 2,000 records by default; `overriddenOptions.batchSize` is the per-repo override.

Advance a source cursor only after that page's records have uploaded. The example flushes explicitly before advancing it; the SDK also flushes remaining repos before normal result emission. A failed upload must not be swallowed as success. Recovery can replay an uploaded page if state or callback delivery failed afterwards, so stable identity and replay-safe mapping remain necessary.

Use compact JSON state for source cursors and per-type completion. Do not read extraction boundaries from connector state or recreate the SDK's historical cursors. Return progress between bounded batches and delay without consuming the rate-limited page. Return error for unrecoverable authentication, invalid source payloads or deleted source containers. See [worker results](worker-results.md) for error codes and [worker timeouts](worker-timeouts.md) for timeout behavior.

## Verification

Validate normalized records against EDM and inspect actual emitted artifacts, not merely `repo.getItems()`. Test a page boundary, an empty final page, duplicate IDs, bad timestamps, missing required values, reference resolution, a 429 response, an upload failure and start/continuation replay. A live incremental run must include changed source records in the resolved window without reprocessing unchanged history unnecessarily.

Related: [incremental and historical extraction](extraction-windows.md), [attachments](extract-attachments.md), [public template normalization](https://github.com/devrev/airsync-template/blob/main/code/src/functions/external-system/data-normalization.ts).

<span id="bounded-v2-pagination-example" />

<span id="bounded-pagination-example" />

Related:

* [Data extraction example](data-extraction-example.md).

Next: [Paginated extraction worker example](data-extraction-example.md).
