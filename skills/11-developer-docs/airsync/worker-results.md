# Return worker results and handle errors

Source: <https://developer.devrev.ai/airsync/worker-results>
Scraped: 2026-11-03

Use this contract with [worker routing](runtime.md). The callback receives `{ adapter }` and returns `Promise`.

## Worker results and rate limits

| Result                                           | SDK output in a resumable phase         | Meaning                                       |
| ------------------------------------------------ | --------------------------------------- | --------------------------------------------- |
| `{ status: 'success' }`                          | `*_DONE`                                | This phase has no remaining work              |
| `{ status: 'progress' }`                         | `*_PROGRESS`                            | Checkpoint and continue in another invocation |
| `{ status: 'delay', delaySeconds: 30 }`          | `*_DELAYED` with wire field `delay: 30` | Preserve the cursor and back off              |
| `{ status: 'error', error: { message: '...' } }` | `*_ERROR`                               | Fail the phase                                |

Discovery and deletion are non-resumable: `progress` or `delay` becomes a phase error. For resumable phases, preserve the next unconsumed cursor before returning progress or delay. The next invocation receives `CONTINUE_*`; do not reset its cursor.

Parse a source `Retry-After` as seconds or an HTTP date according to the source API. Return a finite nonnegative delay in seconds; choose a safe fallback when the header is absent or invalid. Do not sleep through an entire backoff inside the worker or translate every HTTP error into a rate limit. The SDK's internal DevRev HTTP client does not implement retry behavior for the connector's external API client.

Use these error codes for permanent conditions: `error.code: AirSyncErrorCode.EXTERNAL_SYNC_UNIT_DELETED`, `EXTERNAL_SYNC_UNIT_DEACTIVATED` or `USER_DELETED`. Other codes are `EXTERNAL_SYSTEM_NO_ACCESS`, `EXTERNAL_SYSTEM_NO_PERMISSION` and `HISTORICAL_DATA_EXTRACTION_DONE`. Use codes only for the condition they describe; historical completion uses its documented error-code signal rather than a generic transient error. The SDK serializes the code for the platform and retains the human-readable message for diagnostics.

Related: [Worker routing](runtime.md).
