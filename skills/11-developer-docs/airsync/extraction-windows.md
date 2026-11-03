# Run incremental and historical extraction

Source: <https://developer.devrev.ai/airsync/extraction-windows>
Scraped: 2026-11-03

AirSync supplies a resolved time range for each extraction run. Your connector applies that range to source requests and keeps it unchanged across continuations.

## Initial, incremental and historical runs

Choose the extraction behavior for the run and respect its resolved time window.

`InitialSyncScope.FULL_HISTORY` and `TIME_SCOPED` identify the initial scope. A time-scoped initial run is not automatically a full-history run; respect the resolved lower boundary. An incremental run uses its resolved window for changes. Historical extraction walks earlier history without shrinking already successful boundaries. Keep source-specific pagination separate from this SDK boundary bookkeeping.

If historical extraction is genuinely exhausted, the SDK exposes `AirSyncErrorCode.HISTORICAL_DATA_EXTRACTION_DONE` as the platform completion condition. Use it only after verifying no earlier source data remains; a transient empty page, permission failure or rate limit is not historical exhaustion.

## Resolved extraction window

Use the adapter's resolved `extract_from` and `extract_to` when fetching or filtering records.

Read `adapter.event.payload.event_context.extract_from` and `extract_to`. They are optional RFC3339 timestamps resolved by the SDK before the task runs. If supplied, the source query must honor them; if unavailable, follow the source API's full-history or incremental fallback without inventing a boundary.

`extraction_start_time` and `extraction_end_time` are platform `TimeValue` inputs. Their `type` values are:

| `TimeValueType`               | Resolution                                                              |
| ----------------------------- | ----------------------------------------------------------------------- |
| `ABSOLUTE_TIME`               | ISO timestamp in `value`                                                |
| `CURRENT_TIME`                | Current time when resolved                                              |
| `WORKERS_OLDEST`              | Earliest successful historical boundary                                 |
| `WORKERS_OLDEST_MINUS_WINDOW` | Earliest boundary minus the duration in `value`                         |
| `WORKERS_NEWEST`              | Latest successful boundary, with last successful sync start as fallback |
| `WORKERS_NEWEST_PLUS_WINDOW`  | Latest boundary plus the duration in `value`                            |
| `UNBOUNDED`                   | SDK unbounded sentinel (`1970-01-01T00:00:00.000Z`)                     |

Duration values use supported Go duration units such as `30s` or `2h`. These are platform controls; ordinary connector workers consume the resolved timestamps instead of resolving `TimeValue` themselves.

The SDK resolves the pending window at metadata start and reuses it across data and attachment continuations. It commits successful boundaries only when attachment extraction finishes. A failed run must not advance the successful boundary. The SDK rejects a resolved window with `extract_from >= extract_to`. Do not replace `extract_from` with a cursor from `adapter.state`, alter SDK state or implement old reset flags.

## Source query and timestamp semantics

Use the source endpoint's supported date filters. Source APIs differ in inclusive/exclusive endpoints, timestamp precision, created-versus-updated filters and behavior for records changed during pagination. Document that endpoint's semantics in the connector, choose a consistent boundary policy and use stable IDs for overlap deduplication.

When the endpoint does not support all filters, perform local filtering without dropping required relationships. Paginate in a stable order, preserve source cursors together with the current run ID and keep the same resolved window on every continuation. Do not let each page substitute its own current time for `extract_to`.

An example request can send the resolved values as source parameters:

```typescript
const { extract_from, extract_to } = adapter.event.payload.event_context;
if (extract_from) url.searchParams.set('updated_from', extract_from);
if (extract_to) url.searchParams.set('updated_to', extract_to);
```

This fragment assumes the source contract explicitly supports these parameter names; they are not SDK-defined source API fields.

## Verify time boundaries

Test records immediately before, at and after both boundaries, source precision differences, late updates, continuations crossing midnight and a failed attachments phase followed by retry. For historical support, demonstrate adjacent windows, oldest-history exhaustion and incremental sync after backfill.

The platform determines which time controls are available to an installed import. Declare time-scoped capabilities in the [manifest](manifest.md) only when the connector implements them.

Next: [Import attachments into DevRev](extract-attachments.md).
