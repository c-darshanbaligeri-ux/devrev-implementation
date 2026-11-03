# Customize attachment processing

Source: <https://developer.devrev.ai/airsync/customize-attachment-processing>
Scraped: 2026-11-03

## Processor input and output

| Callback                                                          | Input                                                  | Output                                             |
| ----------------------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------- |
| `ExternalSystemAttachmentReducerFunction<Batch, NewBatch, State>` | `{ attachments, adapter, batchSize? }`                 | A transformed batch; no asynchronous source calls  |
| `ExternalSystemAttachmentIteratorFunction<NewBatch, State>`       | `{ reducedAttachments, adapter, stream }`              | `Promise`             |
| `adapter.processAttachment(attachment, stream)`                   | One normalized descriptor and a source stream callback | `success`, `delay` with `delaySeconds`, or `error` |

Do not return `undefined`, `{ delay }` or `{ error }`. Do not call internal emit APIs. `streamAttachments` converts the processor response and timeout into the phase's `TaskResult`.

## Refreshing URLs and stricter recovery

For expiring links, use `parent_id`, attachment `id` and optional `grand_parent_id` to request fresh source metadata immediately before downloading. A parent-group reducer can reduce repeated source metadata requests, but asynchronous refresh belongs in the iterator or stream callback. Preserve attachment and parent identity when replacing `url`, `file_name` or MIME metadata.

Choose and document whether a source 404 is an intentional skipped attachment or a phase failure. A permission failure must not silently become an empty successful import. Propagate source rate limits using a delay result without marking that item complete. Avoid filtering descriptors out of the reducer unless omission is intentional and observable: the SDK considers the artifact consumed when the iterator completes.

Normal checkpoint persistence occurs after attachment associations have flushed. Do not call `postState` with completion markers ahead of buffered associations; a subsequent failure could suppress necessary replay. A crash between source upload and persisted completion can still repeat work, so verification must include that recovery case.

## Verification

Exercise two attachments sharing a parent, two parents sharing an attachment ID, URL expiration, an interrupted item and a delay after several successes. Verify continuation skips recorded successes, retries the incomplete item, retains correct parent associations and does not advance after your chosen error condition. Compare custom behavior with the default pool before enabling it in a live connector.

Related: [attachment contract](extract-attachments.md), [runtime state](runtime.md), [public processor types](https://github.com/devrev/airsync-sdk/blob/main/src/types/extraction.ts).

<span id="v2-custom-continuation-example" />

<span id="custom-continuation-example" />

Related:

* [Custom attachment iterator example](attachment-processing-example.md).

Next: [Custom attachment iterator example](attachment-processing-example.md).
