# Create and update external records

Source: <https://developer.devrev.ai/airsync/load-data>
Scraped: 2026-11-03

## Data loading inputs

`adapter.loadItemTypes({ itemTypesToLoad })` accepts an ordered array of `{ itemType, create, update }`. `itemType` must match the external record-type key in metadata and mapping. Order parent or dependency types before dependent types.

The standard SDK registry exposes `create` and `update`; it does not expose a record-deletion callback. Loader state cleanup is a separate operation and does not delete external data.

Each callback receives `ExternalSystemItemLoadingParams`:

| Input                                     | Meaning                                                                                              |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `item.id.devrev`                          | DevRev object identity; suitable for a stable idempotency key                                        |
| `item.id.external`                        | Optional external ID; do not assume it is populated                                                  |
| `item.created_date`, `item.modified_date` | Timestamps on the transformed item; these are not the external API response's modification timestamp |
| `item.data`                               | Fields after reverse recipe transformation, keyed by the external domain model                       |
| `mappers`                                 | SDK object mapper client for resolving DevRev IDs to external IDs                                    |
| `event`                                   | Connection, sync-unit and invocation context                                                         |

`item.data` is typed as `any` in the public SDK. Your connector must validate or narrow its fields before building an API request. Omit external read-only fields on writes. Preserve the distinction between an absent field and a deliberate clear when the external API supports partial updates.

## SDK-managed identity and reporting

The SDK looks up a mapper by `item.id.devrev`. If a mapper exists it calls `update`; otherwise it calls `create`. After success it creates or updates the mapper with the external ID and optional external version. Do not create the same mapper again inside the callback.

`loadItemTypes()` selects transformer files for the item types you registered and processes them in registration order. Unregistered types are not loaded. Register every type you declare loadable; a done outcome alone does not prove that all intended types were written.

The SDK includes per-type created, updated and failed counts, plus processed artifact IDs, in its emitted outcome. Read `adapter.reports` and `adapter.processedFiles` only when additional connector reporting is needed; do not build an emit payload manually.

## Verification

* Create a record without a mapper; confirm one external record and one mapper result.
* Update a mapped record; confirm the same external ID receives the change.
* Exercise missing required fields, read-only fields and clearing values.
* Return a delay on one item; confirm continuation retries that item without replaying completed items.
* Return a callback error; confirm the failed count increases and following records still run.
* Fail mapper persistence after a successful write; confirm your idempotency strategy prevents a duplicate on recovery.

See [reverse sync lifecycle](loading-phases.md), [object mappers](object-mappers.md) and [ordering and loop prevention](reverse-sync-ordering.md).

## Loading callback results

A callback returns success, delay or an item error. An item error and a phase failure have different recovery behavior.

Callbacks return `Promise`:

```typescript
import type { ExternalSystemItemLoadingResponse } from '@devrev/airsync-sdk';

const created: ExternalSystemItemLoadingResponse = {
  status: 'success',
  id: 'external-task-123',
  modifiedDate: '2026-10-12T10:00:00Z',
};

const rateLimited: ExternalSystemItemLoadingResponse = {
  status: 'delay',
  delaySeconds: 30,
};

const rejected: ExternalSystemItemLoadingResponse = {
  status: 'error',
  error: { message: 'The external task requires a project.' },
};
```

`id` must be the external record ID returned or confirmed by the write. `modifiedDate`, when provided, must be the external system's resulting modification timestamp. The SDK stores it on the mapper for [loop prevention](loop-prevention.md#loop-prevention).

A callback error is an **item failure**: the SDK increments the failed report and advances to the next item. It is not an automatic retry request. A callback delay leaves the current item pending and returns a delayed task outcome. A thrown error or failed mapper write fails the phase. Sanitize error messages; do not include tokens or full customer payloads.

<span id="v2-data-worker" />

<span id="data-worker" />

Related:

* [Data loading example](data-loading-example.md).

Next: [External record loading example](data-loading-example.md).
