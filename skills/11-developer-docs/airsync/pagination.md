# Fetch multiple pages and resume extraction

Source: <https://developer.devrev.ai/airsync/pagination>
Scraped: 2026-11-03

## Pagination and checkpoints

Use the provider's documented pagination mechanism: a cursor, offset, page number or next-page link. Preserve the full selection and time-window filters on every request.

For each page:

1. Fetch and validate the provider response.
2. Normalize each eligible record to the external schema and await its repository write.
3. Advance connector state to the next page only after all required page records have been accepted.
4. Return `progress` when the execution budget is nearly exhausted, or continue fetching while work remains.
5. Return `success` only when the provider indicates the selection is exhausted.

Await repository writes before advancing state. Do not store the cursor for a page you have only fetched. Do not use item count alone to infer completion when the provider supplies an explicit next-page token.

For APIs without stable snapshot pagination, define how concurrent updates are handled. Stable IDs, deterministic ordering and a carefully chosen overlap window can make repeated reads safe, but cannot compensate for skipped source records. Consult the provider's guarantees and test changes made while a run is in progress.

## Incremental and selective requests

Use the adapter's resolved `extract_from` and `extract_to`, not a separately maintained legacy watermark. If the provider cannot filter both bounds, filter locally before writing records. Include boundary cases in tests and document whether the provider timestamps are creation or modification times. [Incremental and historical extraction](extraction-windows.md) defines the time-window contract.

[A disabled record type](extraction-scope.md) must not emit records. Required referenced types need a deliberate mapping/dependency design; enabling one type must not silently import every type from the provider.

## Failure and replay verification

Test an empty first page, a multi-page result, a repeated cursor, an invalid response, a mid-page error, a 429 and an aborted request. Resume in a fresh invocation and verify that no pending record was skipped. A retry may repeat already accepted records; stable external IDs must preserve their identity. See [validation](validation.md) for fixture and live-run checks.

Related: [External API clients](external-api-clients.md).

Next: [Extract selected record types](extraction-scope.md).
