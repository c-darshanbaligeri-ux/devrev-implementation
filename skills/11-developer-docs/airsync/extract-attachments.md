# Import attachments into DevRev

Source: <https://developer.devrev.ai/airsync/extract-attachments>
Scraped: 2026-11-03

## Descriptor contract

| `NormalizedAttachment` field    | Required | Meaning                                                             |
| ------------------------------- | -------- | ------------------------------------------------------------------- |
| `id`                            | Yes      | Stable external attachment ID                                       |
| `url`                           | Yes      | Source download URL; credentials belong in the authenticated client |
| `file_name`                     | Yes      | Filename supplied for the upload                                    |
| `parent_id`                     | Yes      | External ID of the imported parent                                  |
| `author_id`                     | No       | External actor ID                                                   |
| `inline`                        | No       | Whether content is displayed inline                                 |
| `content_type`                  | No       | MIME type override                                                  |
| `created_date`, `modified_date` | No       | RFC3339 source timestamps                                           |
| `grand_parent_id`               | No       | Source context for fetching an attachment nested under a child      |

This is descriptor data, not a `NormalizedItem` envelope. Register `{ itemType: AirSyncDefaultItemTypes.ATTACHMENTS, normalize }` and push source attachments through it, or push already normalized descriptors without a normalizer. All IDs must be strings and parent identity must match the imported record. Preserve identifiers independently of expiring URLs.

The SDK records uploaded descriptor artifacts and consumes them in the attachments phase. Its generated attachment association uses the external attachment ID, parent ID and optional author/inline flag. `grand_parent_id` is available to your source stream function; it is not automatically mapped to an additional parent association.

## SDK streaming behavior and partial failures

`streamAttachments` returns `TaskResult`; return it directly. Its `batchSize` defaults to one concurrent stream and is clamped to the range 1–50. This differs from repo batch size. The SDK obtains an upload URL, streams source bytes, confirms the upload and emits attachment associations through its own repo.

The built-in pool tracks processed `(id, parent_id)` pairs within a descriptor artifact. A per-attachment error is recorded as failed and skipped; it does not necessarily fail the whole phase. A delay stops further work and returns a delayed result. A descriptor-artifact download failure fails the phase. Validate attachment counts and failed items even when the phase reports success.

On soft timeout, the built-in pool stops scheduling attachments and leaves the current descriptor artifact unconsumed for continuation. In-flight requests and uploads are not guaranteed to stop immediately; use bounded request and stream timeouts. `processAttachment` may return success without queuing an association when `adapter.isTimeout` is true, so check the signal before marking custom work complete. See [custom processing](customize-attachment-processing.md) for stricter error handling or URL refresh.

Descriptors and source streams must remain available across continuation. For expiring URLs, refetch a fresh URL using stable IDs at download time. `processAttachment` can run in any extraction phase when content must be transferred immediately; the SDK defers associations produced before the attachments phase until attachment completion. Do not manipulate that internal queue.

## Verification

Test ordinary and inline attachments, multiple parents, empty content, revoked access, expired URLs, rate limits and a timeout mid-stream. Compare uploaded bytes, filename, MIME type, parent and actor with the source. Verify resume neither drops content nor creates incorrect associations, and reconcile failed attachments explicitly. For target content restrictions and source rate limits, validate the actual service behavior rather than treating SDK concurrency or an upload implementation constant as a universal file limit.

Related: [custom processing](customize-attachment-processing.md), [data extraction](data-extraction.md), [runtime](runtime.md), [rich text](data-model/rich-text-fields.md).

<span id="bounded-v2-streaming-example" />

<span id="bounded-streaming-example" />

Related:

* [Attachment streaming example](attachment-streaming-example.md).

Next: [Attachment import worker example](attachment-streaming-example.md).
